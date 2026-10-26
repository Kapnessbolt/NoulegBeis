#!/usr/bin/env python3
"""Ricerca nel vault: frontmatter e testo, ordinata per collegamenti (SPEC 9.3, step 17 di 13.1).

Nessun indice: scansiona le note a ogni chiamata. Salta `.git`, `.github`, `.claude`,
`_templates`, `.obsidian`, `.trash`, `sessions/_raw/` e i file `README.md`, `CLAUDE.md`,
`SPEC.md`, `home.md`.

Uso:
  python3 .claude/scripts/cerca.py <termini...> [filtri] [--limite N] [--contesto] [--json]
  python3 .claude/scripts/cerca.py --collegamenti <slug> [filtri] [--json]
      # chi collega la nota (backlink), raggruppati per type
  python3 .claude/scripts/cerca.py --nota <slug> [--json]
      # scheda: percorso, type, frontmatter, titolo, sezioni, backlink, collegamenti in uscita

Termini:
- senza maiuscole e senza accenti (`Attività` = `attivita`), cercati a inizio parola: `cors`
  trova `corso` e `corsi`, `ai` non trova `mail`;
- più termini = tutti presenti nella nota (AND);
- un termine tra virgolette è una frase: `"corso ai"` trova anche `corso-ai` e `Corso AI`;
- `-termine` (o `-"frase"`) esclude le note che lo contengono.
Si cercano nel titolo H1 e nello slug, nel frontmatter (tutti i valori, come testo) e nel corpo.

Filtri (si combinano tra loro; i ripetibili valgono in OR):
  --tipo T          `type` del frontmatter (ripetibile)
  --cartella C      prefisso del percorso relativo, per cartelle intere (`sources/mail`, ripetibile)
  --progetto S      note che collegano [[S]], nel frontmatter o nel testo; così anche
  --cliente S, --tema S, --persona S
  --da AAAA-MM-GG   data della nota da (compresa)
  --a AAAA-MM-GG    data della nota fino a (compresa)
  --tag T           valore di `tags` (ripetibile)

Data della nota: il primo campo presente tra `date`, `updated`, `last_message`,
`first_message`, `current.last_modified`, `ingested_at`, `created`; se manca, il nome del file
se inizia con AAAA-MM-GG; per i `project-log`, senza campi data, la riga di log più recente
(`- AAAA-MM-GG · …`). Una nota senza data non passa i filtri `--da` e `--a`.

Punteggio: somma, per ogni termine, del peso del posto migliore in cui compare: 10 nel titolo
o nello slug, 3 nel frontmatter, 1 nel corpo. A parità di punteggio prima chi ha più backlink
(note che la collegano con [[slug]]): così le note hub emergono; poi la data più recente.
Senza termini (solo filtri) l'ordine è per data, poi backlink.

Output: una riga per nota, `<punteggio> · <type> · [[slug]] · <titolo> · <data> · <n> backlink`;
`--contesto` aggiunge fino a 2 righe del corpo con i termini. `--limite N` (default 20, 0 = tutti).
`--json`: lista di oggetti con slug, percorso, type, titolo, data, backlink, punteggio, contesto,
frontmatter.

Uscita: 0 ok (anche senza risultati), 1 nota non trovata (`--nota`, `--collegamenti`, slug dei
filtri), 2 argomenti non validi. Una nota con il frontmatter non leggibile è saltata con un
avviso su stderr.

La variabile d'ambiente VAULT_ROOT, se presente, indica la radice del vault al posto della
cartella che contiene `.claude/` (serve ai test in `.claude/scripts/tests/`).
"""

import argparse
import datetime as dt
import difflib
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Manca PyYAML: pip install pyyaml")

sys.path.insert(0, str(Path(__file__).resolve().parent))
import nota  # noqa: E402

ROOT = Path(os.environ.get("VAULT_ROOT") or Path(__file__).resolve().parents[2]).resolve()
SKIP_DIRS = {".git", ".github", ".claude", "_templates", ".obsidian", ".trash"}
SKIP_FILES = {"README.md", "CLAUDE.md", "SPEC.md", "home.md"}
CAMPI_DATA = ("date", "updated", "last_message", "first_message", "current.last_modified",
              "ingested_at", "created")
PESO_TITOLO, PESO_FRONTMATTER, PESO_CORPO = 10, 3, 1
LIMITE = 20
CONTESTO_RIGHE, CONTESTO_LARGHEZZA = 2, 160
ORDINE_TIPI = ("project", "project-log", "client", "person", "topic", "source-doc", "source-mail",
               "session", "journal", "inbox", "proposal")
# Opzioni che vogliono un valore: il token che le segue non è un termine da escludere
CON_VALORE = {"--tipo", "--cartella", "--progetto", "--cliente", "--tema", "--persona", "--da",
              "--a", "--tag", "--limite", "--collegamenti", "--nota"}

WIKILINK_RE = re.compile(r"\[\[([^\]|#^]+)(?:[#^][^\]|]*)?(?:\|[^\]]*)?\]\]")
H1_RE = re.compile(r"^# (.+)$", re.M)
DATA_NOME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")
PAROLA_RE = re.compile(r"[^\W_]+")

try:
    Loader = yaml.CSafeLoader
except AttributeError:  # PyYAML senza libyaml
    Loader = yaml.SafeLoader


# --- Testo ------------------------------------------------------------------------------

def normalizza(s):
    """Minuscolo e senza accenti (NFKD), per confrontare query e testo."""
    s = unicodedata.normalize("NFKD", str(s))
    return "".join(c for c in s if not unicodedata.combining(c)).casefold()


def senza_codice(testo):
    testo = re.sub(r"```.*?```", "", testo, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", testo)


def valori(v):
    """Tutti i valori scalari di un frontmatter (anche annidati), come testo."""
    if isinstance(v, dict):
        for x in v.values():
            yield from valori(x)
    elif isinstance(v, list):
        for x in v:
            yield from valori(x)
    elif v is not None:
        yield str(nota.normale(v))


RIGA_LOG_RE = re.compile(r"^- (\d{4}-\d{2}-\d{2}) ·", re.M)


def data_di(fm, stem, corpo=""):
    for campo in CAMPI_DATA:
        if campo.startswith("current."):
            cur = fm.get("current")
            v = cur.get(campo.split(".", 1)[1]) if isinstance(cur, dict) else None
        else:
            v = fm.get(campo)
        if v not in (None, "") and DATA_NOME_RE.match(str(nota.normale(v))):
            return str(nota.normale(v))[:10]
    m = DATA_NOME_RE.match(stem)
    if m:
        return m.group(1)
    date_log = RIGA_LOG_RE.findall(corpo)
    return max(date_log) if date_log else ""


# --- Termini ----------------------------------------------------------------------------

class Termine:
    def __init__(self, testo):
        self.testo = testo
        parole = PAROLA_RE.findall(normalizza(testo))
        if not parole:
            raise ValueError(testo)
        corpo = r"[\W_]+".join(re.escape(p) for p in parole)
        self.re = re.compile(r"(?<![^\W_])" + corpo)

    def in_(self, testo):
        return bool(self.re.search(testo))


FRASE_RE = re.compile(r'(-?)"([^"]*)"?|(\S+)')


def dividi_termini(grezzi):
    """(inclusi, esclusi) dai termini della riga di comando. Un argomento con spazi è una frase
    (la shell ha già tolto le virgolette); dentro un argomento le virgolette doppie rimaste
    delimitano le frasi (l'apostrofo resta nella parola: `l'azienda`); `-` davanti esclude."""
    pezzi = []
    for arg in grezzi:
        if '"' not in arg:
            pezzi.append(arg.strip())
            continue
        for m in FRASE_RE.finditer(arg):
            pezzi.append(m.group(1) + m.group(2) if m.group(2) is not None else m.group(3))
    inclusi, esclusi = [], []
    for p in pezzi:
        meno = p.startswith("-")
        if meno:
            p = p[1:].strip()
        if not p:
            continue
        try:
            t = Termine(p)
        except ValueError:
            print(f"avviso: termine `{p}` senza lettere né cifre, ignorato", file=sys.stderr)
            continue
        (esclusi if meno else inclusi).append(t)
    return inclusi, esclusi


# --- Vault ------------------------------------------------------------------------------

def carica():
    """(note per slug, slug delle note che collegano ogni slug). Le note con il frontmatter non
    leggibile restano fuori da tutto, anche dai backlink."""
    note = {}
    for p in sorted(ROOT.rglob("*.md")):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in SKIP_DIRS or p.name in SKIP_FILES or rel.parts[:2] == ("sessions", "_raw"):
            continue
        try:
            testo = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            print(f"avviso: {rel}: non leggibile ({e}), saltata", file=sys.stderr)
            continue
        slug = p.stem
        if slug in note:
            print(f"avviso: {rel}: slug `{slug}` già usato, saltata", file=sys.stderr)
            continue
        try:
            fm_testo, corpo = nota.dividi(testo)
            fm = yaml.load(fm_testo, Loader=Loader) or {}
            if not isinstance(fm, dict):
                raise nota.Errore("il frontmatter non è una mappa")
        except (nota.Errore, yaml.YAMLError) as e:
            motivo = str(e).splitlines()[0]
            print(f"avviso: {rel}: frontmatter non leggibile ({motivo}), saltata", file=sys.stderr)
            continue
        m = H1_RE.search(corpo)
        titolo = m.group(1).strip() if m else ""
        if m:
            corpo = corpo[:m.start()] + corpo[m.end():]
        note[slug] = {
            "slug": slug,
            "percorso": rel.as_posix(),
            "type": str(fm.get("type") or ""),
            "titolo": titolo,
            "data": data_di(fm, slug, corpo),
            "fm": fm,
            "fm_testo": fm_testo,
            "corpo": corpo,
            "uscite": {m.group(1).strip() for m in WIKILINK_RE.finditer(senza_codice(testo))} - {slug},
            "n_titolo": normalizza(f"{titolo}\n{slug}"),
            "n_fm": normalizza("\n".join(valori(fm))),
            "n_corpo": normalizza(corpo),
        }
    backlink = {}
    for s, n in note.items():
        for t in n["uscite"]:
            backlink.setdefault(t, set()).add(s)
    return note, backlink


def tags_di(fm):
    t = fm.get("tags")
    if t is None or t == "":
        return []
    return [normalizza(x) for x in (t if isinstance(t, list) else [t])]


def passa(n, a):
    if a.tipo and n["type"] not in a.tipo:
        return False
    if a.cartella and not any(n["percorso"] == c or n["percorso"].startswith(c + "/") for c in a.cartella):
        return False
    for s in a.collega:
        if s not in n["uscite"]:
            return False
    if a.da or a.a:
        if not n["data"]:
            return False
        if a.da and n["data"] < a.da:
            return False
        if a.a and n["data"] > a.a:
            return False
    if a.tag and not set(map(normalizza, a.tag)) & set(tags_di(n["fm"])):
        return False
    return True


def punteggio(n, inclusi):
    """Somma, per ogni termine, del peso del campo migliore in cui compare; None se ne manca uno."""
    tot = 0
    for t in inclusi:
        if t.in_(n["n_titolo"]):
            tot += PESO_TITOLO
        elif t.in_(n["n_fm"]):
            tot += PESO_FRONTMATTER
        elif t.in_(n["n_corpo"]):
            tot += PESO_CORPO
        else:
            return None
    return tot


def escluso(n, esclusi):
    return any(t.in_(n["n_titolo"]) or t.in_(n["n_fm"]) or t.in_(n["n_corpo"]) for t in esclusi)


def fuori_dai_link(norm, termini):
    """Posizioni dei termini nella riga normalizzata fuori dai wikilink (il testo, non gli slug)."""
    link = [m.span() for m in WIKILINK_RE.finditer(norm)]
    pos = {}
    for t in termini:
        for m in t.re.finditer(norm):
            if not any(a <= m.start() < b for a, b in link):
                pos[t.testo] = min(pos.get(t.testo, m.start()), m.start())
                break
    return pos


def taglia(riga, termini):
    riga = riga.strip()
    if len(riga) <= CONTESTO_LARGHEZZA:
        return riga
    norm = normalizza(riga)
    fuori = fuori_dai_link(norm, termini)
    pos = min(fuori.values()) if fuori else min(
        (m.start() for t in termini for m in [t.re.search(norm)] if m), default=0)
    # la normalizzazione può cambiare di poco la lunghezza: la posizione è un'approssimazione
    inizio = max(0, min(pos - 40, len(riga) - CONTESTO_LARGHEZZA))
    pezzo = riga[inizio:inizio + CONTESTO_LARGHEZZA].strip()
    return ("…" if inizio > 0 else "") + pezzo + ("…" if inizio + CONTESTO_LARGHEZZA < len(riga) else "")


def contesto(n, inclusi):
    """Fino a 2 righe del corpo con i termini: prima quelle che li hanno nel testo e non solo
    negli slug dei wikilink, poi quelle con più termini, nell'ordine della nota."""
    if not inclusi:
        return []
    righe = []
    for i, riga in enumerate(n["corpo"].splitlines()):
        if not riga.strip():
            continue
        norm = normalizza(riga)
        quanti = sum(1 for t in inclusi if t.in_(norm))
        if quanti:
            righe.append((-len(fuori_dai_link(norm, inclusi)), -quanti, i, riga))
    righe.sort()
    scelte = sorted(righe[:CONTESTO_RIGHE], key=lambda r: r[2])
    return [taglia(r[3], inclusi) for r in scelte]


def frontmatter_json(fm):
    return json.loads(json.dumps(nota.normale(fm), ensure_ascii=False, default=str))


# --- Comandi ----------------------------------------------------------------------------

def non_trovata(slug, note):
    simili = difflib.get_close_matches(slug, list(note), n=5, cutoff=0.6)
    msg = f"nota `{slug}` non trovata"
    if simili:
        msg += ": forse " + ", ".join(simili)
    print(msg, file=sys.stderr)
    return 1


def riga_risultato(r):
    return (f"{r['punteggio']} · {r['type'] or '—'} · [[{r['slug']}]] · {r['titolo'] or r['slug']} · "
            f"{r['data'] or '—'} · {r['backlink']} backlink")


def cerca(note, backlink, a, inclusi, esclusi):
    risultati = []
    for n in note.values():
        if not passa(n, a):
            continue
        p = punteggio(n, inclusi) if inclusi else 0
        if p is None or escluso(n, esclusi):
            continue
        risultati.append((p, len(backlink.get(n["slug"], ())), n))
    # ordinamenti stabili, dal criterio meno importante al più importante
    risultati.sort(key=lambda r: r[2]["slug"])
    if inclusi:
        per_data(risultati, lambda r: r[2]["data"])
        risultati.sort(key=lambda r: (-r[0], -r[1]))
    else:
        risultati.sort(key=lambda r: -r[1])
        per_data(risultati, lambda r: r[2]["data"])
    totale = len(risultati)
    if a.limite:
        risultati = risultati[:a.limite]
    out = [{
        "slug": n["slug"], "percorso": n["percorso"], "type": n["type"], "titolo": n["titolo"],
        "data": n["data"], "backlink": b, "punteggio": p,
        "contesto": contesto(n, inclusi) if (a.contesto or a.json) else [],
        "frontmatter": n["fm"],
    } for p, b, n in risultati]
    if a.json:
        for r in out:
            r["frontmatter"] = frontmatter_json(r["frontmatter"])
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 0
    if not out:
        print("nessun risultato")
        return 0
    for r in out:
        print(riga_risultato(r))
        for c in r["contesto"]:
            print(f"    > {c}")
    if totale > len(out):
        altri = totale - len(out)
        print(f"… {'altro' if altri == 1 else 'altri'} {altri} {'risultato' if altri == 1 else 'risultati'}"
              " (--limite 0 per vederli tutti)")
    return 0


def per_data(lista, data):
    """Ordina per data decrescente, stabile; le note senza data vanno in fondo."""
    lista.sort(key=lambda x: data(x) or "", reverse=True)


def collegamenti(note, backlink, a):
    slug = a.collegamenti
    if slug not in note:
        return non_trovata(slug, note)
    da = [note[s] for s in backlink.get(slug, ()) if passa(note[s], a)]
    gruppi = {}
    for n in da:
        gruppi.setdefault(n["type"] or "senza-type", []).append(n)
    ordine = sorted(gruppi, key=lambda t: (ORDINE_TIPI.index(t) if t in ORDINE_TIPI else len(ORDINE_TIPI), t))
    for t in ordine:
        gruppi[t].sort(key=lambda n: n["slug"])
        per_data(gruppi[t], lambda n: n["data"])
    n0 = note[slug]
    if a.json:
        print(json.dumps({
            "slug": slug, "percorso": n0["percorso"], "type": n0["type"], "titolo": n0["titolo"],
            "backlink": len(da),
            "per_tipo": {t: [{"slug": n["slug"], "percorso": n["percorso"], "titolo": n["titolo"],
                              "data": n["data"]} for n in gruppi[t]] for t in ordine},
        }, ensure_ascii=False, indent=1))
        return 0
    print(f"[[{slug}]] · {n0['titolo'] or slug} · {n0['type'] or '—'} · collegata da {len(da)} note")
    for t in ordine:
        print(f"\n{t} ({len(gruppi[t])})")
        for n in gruppi[t]:
            print(f"- [[{n['slug']}]] · {n['titolo'] or n['slug']} · {n['data'] or '—'}")
    return 0


def sezioni(corpo):
    out, cur = [], None
    for riga in corpo.splitlines():
        if riga.startswith("## "):
            cur = {"titolo": riga[3:].strip(), "righe": 0}
            out.append(cur)
        elif cur is not None and riga.strip() and riga.strip() != "-":
            cur["righe"] += 1
    return out


def scheda(note, backlink, slug, as_json):
    if slug not in note:
        return non_trovata(slug, note)
    n = note[slug]
    secs = sezioni(n["corpo"])
    da = sorted(backlink.get(slug, ()))
    uscite = sorted(n["uscite"])
    if as_json:
        print(json.dumps({
            "slug": slug, "percorso": n["percorso"], "type": n["type"], "titolo": n["titolo"],
            "data": n["data"], "frontmatter": frontmatter_json(n["fm"]), "sezioni": secs,
            "backlink": len(da), "collegata_da": da, "collega": uscite,
        }, ensure_ascii=False, indent=1))
        return 0
    print(f"[[{slug}]] · {n['titolo'] or slug}")
    print(f"percorso: {n['percorso']}")
    print(f"type: {n['type'] or '—'} · data: {n['data'] or '—'} · backlink: {len(da)}")
    print("frontmatter:")
    for riga in n["fm_testo"].splitlines():
        print(f"  {riga}")
    print("sezioni:")
    for s in secs:
        print(f"  - {s['titolo']} ({s['righe']} righe)")
    if not secs:
        print("  —")
    print("collega: " + (", ".join(f"[[{s}]]" for s in uscite) or "—"))
    return 0


# --- Argomenti --------------------------------------------------------------------------

class Formato(argparse.RawDescriptionHelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        return super().add_usage(usage, actions, groups, prefix="Uso: ")


class Parser(argparse.ArgumentParser):
    TRADUZIONI = (("argument ", "argomento "), ("unrecognized arguments", "argomenti non riconosciuti"),
                  ("expected one argument", "vuole un valore"), ("ambiguous option", "opzione ambigua"),
                  ("could match", "potrebbe essere"))

    def error(self, message):
        for en, it in self.TRADUZIONI:
            message = message.replace(en, it)
        self.print_usage(sys.stderr)
        self.exit(2, f"{self.prog}: errore: {message}\n")


def data_arg(v):
    try:
        return dt.date.fromisoformat(v).isoformat()
    except ValueError:
        raise argparse.ArgumentTypeError(f"`{v}` non è una data AAAA-MM-GG")


def limite_arg(v):
    try:
        n = int(v)
    except ValueError:
        raise argparse.ArgumentTypeError(f"`{v}` non è un numero")
    if n < 0:
        raise argparse.ArgumentTypeError("il limite non può essere negativo")
    return n


def parser():
    p = Parser(prog="cerca.py", formatter_class=Formato, add_help=False, allow_abbrev=False,
               usage="%(prog)s <termini...> [filtri] [--limite N] [--contesto] [--json]\n"
                     "       %(prog)s --collegamenti <slug> [filtri] [--json]\n"
                     "       %(prog)s --nota <slug> [--json]",
               description=__doc__)
    p._positionals.title = "argomenti"
    p._optionals.title = "opzioni"
    p.add_argument("-h", "--help", action="help", help="mostra questo aiuto ed esce")
    p.add_argument("termini", nargs="*", help='termini (AND), "frase", -escluso')
    p.add_argument("--tipo", action="append", default=[], metavar="T", help="type del frontmatter (ripetibile)")
    p.add_argument("--cartella", action="append", default=[], metavar="C",
                   help="prefisso del percorso relativo (ripetibile)")
    for nome, cosa in (("progetto", "il progetto"), ("cliente", "il cliente"), ("tema", "il tema"),
                       ("persona", "la persona")):
        p.add_argument(f"--{nome}", metavar="S", help=f"solo le note che collegano {cosa} [[S]]")
    p.add_argument("--da", type=data_arg, metavar="AAAA-MM-GG", help="data della nota da (compresa)")
    p.add_argument("--a", type=data_arg, metavar="AAAA-MM-GG", help="data della nota fino a (compresa)")
    p.add_argument("--tag", action="append", default=[], metavar="T", help="valore di tags (ripetibile)")
    p.add_argument("--limite", type=limite_arg, default=LIMITE, metavar="N",
                   help=f"numero massimo di risultati (default {LIMITE}, 0 = tutti)")
    p.add_argument("--contesto", action="store_true", help="fino a 2 righe del corpo con i termini")
    p.add_argument("--collegamenti", metavar="SLUG", help="note che collegano [[SLUG]], per type")
    p.add_argument("--nota", metavar="SLUG", help="scheda sintetica della nota")
    p.add_argument("--json", action="store_true", help="output JSON")
    return p


def separa_esclusi(argv):
    """Toglie da argv i termini `-termine`, che argparse leggerebbe come opzioni."""
    resto, esclusi, dopo_trattini = [], [], False
    for i, tok in enumerate(argv):
        prima = argv[i - 1] if i else ""
        if dopo_trattini:
            (esclusi if re.match(r"^-[^-]", tok) else resto).append(tok)
        elif tok == "--":
            dopo_trattini = True
        elif re.match(r"^-[^-]", tok) and tok != "-h" and prima not in CON_VALORE:
            esclusi.append(tok)
        else:
            resto.append(tok)
    return resto, esclusi


def main(argv):
    p = parser()
    resto, esclusi_grezzi = separa_esclusi(argv)
    a = p.parse_intermixed_args(resto)
    termini = a.termini + esclusi_grezzi
    a.collega = [s for s in (a.progetto, a.cliente, a.tema, a.persona) if s]
    a.tipo, a.cartella = set(a.tipo), [c.strip("/") for c in a.cartella if c.strip("/")]
    if a.nota and a.collegamenti:
        p.error("--nota e --collegamenti non vanno insieme")
    if (a.nota or a.collegamenti) and termini:
        p.error("--nota e --collegamenti non vogliono termini")
    if a.nota and (a.tipo or a.cartella or a.collega or a.da or a.a or a.tag):
        p.error("--nota non vuole filtri")
    if a.da and a.a and a.da > a.a:
        p.error(f"--da {a.da} è dopo --a {a.a}")
    inclusi, esclusi = dividi_termini(termini)
    filtri = a.tipo or a.cartella or a.collega or a.da or a.a or a.tag
    if not (a.nota or a.collegamenti) and not inclusi and not esclusi and not filtri:
        p.error("servono termini, filtri, --collegamenti o --nota")
    if not inclusi and not esclusi and termini:
        p.error("nessun termine valido")

    note, backlink = carica()
    if a.nota:
        return scheda(note, backlink, a.nota, a.json)
    for s in a.collega:
        if s not in note:
            return non_trovata(s, note)
    if a.collegamenti:
        return collegamenti(note, backlink, a)
    return cerca(note, backlink, a, inclusi, esclusi)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
