#!/usr/bin/env python3
"""Controllo del vault (SPEC 4.4): integrità dei collegamenti, tracciabilità, schema, doppioni,
possibili dati riservati (CLAUDE.md §5) nel corpo delle note, e la configurazione: `vault.yaml`
valido, orari dei task uguali a SPEC 7, permessi mcp di `.claude/settings.json` e `tools` degli
agenti uguali a quelli che `vault.yaml` dà (config.py, `verifica`), regole di `.claude/rules/`
con il frontmatter leggibile e `paths` valido (una regola con il frontmatter rotto verrebbe
caricata in ogni sessione, senza avvisare). Dallo stato dell'ingestion (`.state/`): una
riconciliazione dovuta (`riconciliazione_dovuta`) da più di 1 giorno è un avviso, da più di 7
un errore; un watermark più di 2 giorni dietro il risultato più recente dell'ultimo giro
(`ultimo_giro` con risultati) è un avviso. Questi errori non bloccano `--modificati`: il giro
che scrive lo stato deve poter fare commit.

Dati riservati: controllo a pattern sul corpo delle note (non sul frontmatter, che contiene
legittimamente `item_id`, `uri` e `conversation_id` lunghi). Ogni corrispondenza è un errore,
con la categoria e al massimo i primi 4 caratteri del valore: IBAN; telefoni italiani (`+39`
e cellulari `3xx`, esclusi importi, ore, percentuali e numeri con separatori delle migliaia);
chiavi e token con prefisso noto (`sk-`, `ghp_`, `github_pat_`, `xox?-`, `AKIA`, JWT `eyJ`);
stringhe esadecimali o base64 di 40+ caratteri; GUID (tranne i nomi di server MCP di
`vault.yaml` e di `.claude/settings.json`); ID e passcode di riunione; password in chiaro (`password: valore`;
la parola "password" da sola è lecita, come i segnaposto `omessa`, `***`, `[...]`).

Uso:
  python3 .claude/scripts/controlla-vault.py              # rapporto in markdown
  python3 .claude/scripts/controlla-vault.py --indice     # rapporto + indice per categoria
  python3 .claude/scripts/controlla-vault.py --modificati # solo gli errori che toccano file
                                                          # modificati rispetto a HEAD (hook di commit)

Esce con codice 1 se trova errori. Richiede PyYAML.

La variabile d'ambiente VAULT_ROOT, se presente, indica la radice del vault al posto della
cartella che contiene `.claude/` (serve ai test in `.claude/scripts/tests/`).
"""

import datetime as dt
import difflib
import json
import os
import re
import subprocess
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Manca PyYAML: pip install pyyaml")

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config  # noqa: E402

ROOT = Path(os.environ.get("VAULT_ROOT") or Path(__file__).resolve().parents[2]).resolve()

# Cartelle e file fuori dal controllo
SKIP_DIRS = {".git", ".github", ".claude", "_templates", ".obsidian", ".trash"}
SKIP_PATHS = {"README.md", "CLAUDE.md", "SPEC.md", "home.md"}

# Tipo atteso per cartella e template di riferimento
TYPE_BY_DIR = {
    "inbox": {"inbox"},
    "projects": {"project", "project-log"},
    "clients": {"client"},
    "people": {"person"},
    "topics": {"topic"},
    "sources": {"source-doc", "source-mail"},
    "journal": {"journal"},
    "sessions": {"session"},
    "proposals": {"proposal"},
}
TEMPLATE_BY_TYPE = {
    "inbox": "inbox",
    "project": "project-index",
    "project-log": "project-log",
    "client": "client",
    "person": "person",
    "topic": "topic",
    "source-doc": "source-doc",
    "source-mail": "source-mail",
    "journal": "journal",
    "session": "session",
    "proposal": "proposal",
}
# Sezioni in cui ogni punto deve citare la fonte (SPEC 4.1, tracciabilità): chiavi di
# `sezioni` in vault.yaml
TRACED_SECTIONS = {
    "topic": ("punti_chiave",),
    "client": ("chi_sono", "relazione"),
    "project": ("stato", "decisioni"),
}
# Note che devono avere almeno un collegamento in entrata
NEED_INBOUND = {"client", "person", "topic"}
STUB_TAG = "da-verificare"

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
WIKILINK_RE = re.compile(r"\[\[([^\]|#^]+)(?:[#^][^\]|]*)?(?:\|[^\]]*)?\]\]")
ENUM_RE = re.compile(r"#\s*([a-z-]+(?:\s*\|\s*[a-z-]+)+)\s*$")
SIMILAR = 0.85
# Stato dell'ingestion (audit 2026-10-31, P4 e P5): giorni oltre i quali una riconciliazione
# dovuta è un avviso e poi un errore, e distacco massimo tra il watermark e il risultato più
# recente dell'ultimo giro
DOVUTA_AVVISO_GIORNI = 1
DOVUTA_ERRORE_GIORNI = 7
WATERMARK_FERMO_GIORNI = 2

errori, avvisi = [], []


def err(paths, msg, target=None, blocca_commit=True):
    """paths: nota o note coinvolte; target: slug citato (per i link rotti); blocca_commit=False
    per gli errori che restano nel rapporto e in CI ma non fermano il pre-commit (`--modificati`)."""
    paths = [str(p) for p in (paths if isinstance(paths, (list, tuple)) else [paths])]
    errori.append({"paths": paths, "msg": msg, "target": target, "blocca_commit": blocca_commit})


def avv(path, msg):
    avvisi.append(f"`{path}` · {msg}")


def split_frontmatter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 4:]


def load_templates():
    """Chiavi ed enum (dai commenti `# a | b | c`) di ogni template."""
    out = {}
    for tipo, nome in TEMPLATE_BY_TYPE.items():
        raw = (ROOT / "_templates" / f"{nome}.md").read_text(encoding="utf-8")
        raw = raw.replace("{{date:YYYY-MM-DD}}", "2000-01-01")
        fm, _ = split_frontmatter(raw)
        data = yaml.safe_load(fm) or {}
        enums = {}
        for line in fm.splitlines():
            m = ENUM_RE.search(line)
            key = line.split(":", 1)[0].strip()
            if m and not line.startswith(" ") and key in data:
                enums[key] = {v.strip() for v in m.group(1).split("|")}
        out[tipo] = {"keys": set(data), "current": set((data.get("current") or {})), "enums": enums}
    return out


def notes():
    for p in sorted(ROOT.rglob("*.md")):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in SKIP_DIRS or str(rel) in SKIP_PATHS:
            continue
        if rel.parts[:2] == ("sessions", "_raw"):
            continue
        yield rel, p


def strip_code(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def wikilinks(text):
    return [m.group(1).strip() for m in WIKILINK_RE.finditer(strip_code(text))]


def as_list(v):
    if v is None or v == "":
        return []
    return v if isinstance(v, list) else [v]


def as_date(v):
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    try:
        return dt.date.fromisoformat(str(v)[:10])
    except ValueError:
        return None


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def sections(body):
    """{titolo ## : testo della sezione}"""
    out, cur = {}, None
    for line in body.splitlines():
        if line.startswith("## "):
            cur = line[3:].strip()
            out[cur] = []
        elif cur:
            out[cur].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def untraced_items(text, fonti):
    """Punti elenco e paragrafi che non citano una fonte (i punti vuoti `-` sono ammessi)."""
    out, para = [], []

    def traced(s):
        return any(link in fonti for link in wikilinks(s))

    def flush():
        if para:
            joined = " ".join(para)
            if not traced(joined):
                out.append(joined)
            para.clear()

    for line in text.splitlines():
        s = line.strip()
        if re.match(r"^[-*] ", s) or re.match(r"^\d+\. ", s):
            flush()
            item = re.sub(r"^([-*]|\d+\.) (\[.\] )?", "", s)
            if item and not traced(item):
                out.append(item)
        elif s in ("", "-", "*"):
            flush()
        elif line.startswith((" ", "\t")) and not para:
            continue  # riga di continuazione o sotto-punto: conta il punto principale
        else:
            para.append(s)
    flush()
    return out


def changed_files():
    """File modificati, aggiunti, cancellati o rinominati rispetto a HEAD (anche non ancora in stage)."""
    res = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"],
                         cwd=ROOT, capture_output=True, text=True, check=False)
    out = set()
    for line in res.stdout.splitlines():
        path = line[3:]
        for part in path.split(" -> "):
            out.add(part.strip().strip('"'))
    return out


# Dati riservati (CLAUDE.md §5): pattern cercati nel corpo delle note
CONTESTO = 10  # caratteri attorno a un numero di telefono da guardare per scartare importi e ore
IBAN_RE = re.compile(r"\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){2,7} ?[A-Z0-9]{1,4}\b")
TEL_RE = re.compile(r"(?<![\w+])(?:\+39[ .]?\d(?:[ .]?\d){8,9}|3\d{2}[ .]?\d{3}[ .]?\d{3,4})\b")
NON_TEL_DOPO = re.compile(r"^\s*(?:€|k€|%|ore\b)", re.I)
CHIAVE_RE = re.compile(r"(?<![\w-])(?:sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}"
                       r"|xox[abp]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16}|eyJ[A-Za-z0-9_-]{20,})")
HEX_RE = re.compile(r"(?<![\w-])[0-9a-fA-F]{40,}(?![\w-])")
B64_RE = re.compile(r"(?<![A-Za-z0-9+/=_-])[A-Za-z0-9+/]{40,}={0,2}(?![A-Za-z0-9+/=_-])")
GUID_RE = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
RIUNIONE_RE = re.compile(r"(?i)\b(?:ID (?:della )?riunione|Meeting ID)\s*:?\s*(\d{3,4}(?: ?\d{3,4}){2,3})\b")
PASSCODE_RE = re.compile(r"(?i)\b(?:passcode|codice (?:di )?accesso)\b\s*(?:[:=]\s*)?([A-Za-z0-9]{4,})\b")
PASSWORD_RE = re.compile(r"(?i)\b(?:password|pwd|passcode)\s*[:=]\s*(\S+)")
SEGNAPOSTO = {"omessa", "omesso", "omesse", "omessi", "riservata", "riservato", "nessuna", "n/d", "-"}


def guid_noti(conf=None):
    """GUID già in configurazione (nomi di server MCP in vault.yaml e in settings.json): non
    sono dati dei clienti."""
    noti = {s.lower() for s in config.server_noti(conf)} if conf else set()
    try:
        testo = (ROOT / ".claude" / "settings.json").read_text(encoding="utf-8")
    except OSError:
        return noti
    # `mcp__<guid>__strumento`: il trattino basso è una lettera per \b, quindi qui niente confini
    return noti | {g.lower() for g in re.findall(GUID_RE.pattern.replace(r"\b", ""), testo, re.I)}


def dati_riservati(body, noti=frozenset()):
    """[(categoria, valore, posizione)] dei possibili dati riservati nel testo.

    Le categorie sono in ordine di priorità: se due corrispondenze si sovrappongono (l'ID di
    una riunione che sembra anche un telefono) resta solo la prima.
    """
    trovati = []

    def add(cat, m, gruppo=0):
        trovati.append((cat, m.group(gruppo), m.start(gruppo), m.end(gruppo)))

    for m in CHIAVE_RE.finditer(body):
        v = m.group(0)
        if v.startswith("sk-") and not (re.search(r"\d", v) and re.search(r"[A-Z]", v)):
            continue  # `sk-` seguito da parole: uno slug, non una chiave
        add("chiave o token", m)
    for m in IBAN_RE.finditer(body):
        if sum(c.isalnum() for c in m.group(0)) >= 15:
            add("IBAN", m)
    for m in RIUNIONE_RE.finditer(body):
        if 9 <= sum(c.isdigit() for c in m.group(1)) <= 12:
            add("ID di riunione", m, 1)
    for m in PASSCODE_RE.finditer(body):
        if re.search(r"\d", m.group(1)):
            add("codice di accesso", m, 1)
    for m in PASSWORD_RE.finditer(body):
        v = m.group(1).strip("`*_\"'.,;:)")
        if not v or v.lower() in SEGNAPOSTO or v[0] in "[<(*" or set(v) <= {"*", "x", "X", "."}:
            continue  # segnaposto: il valore non c'è
        add("password in chiaro", m, 1)
    for m in GUID_RE.finditer(body):
        if m.group(0).lower() not in noti:
            add("GUID", m)
    for m in HEX_RE.finditer(body):
        if re.search(r"\d", m.group(0)) and re.search(r"[a-fA-F]", m.group(0)):
            add("stringa esadecimale lunga", m)
    for m in B64_RE.finditer(body):
        v = m.group(0)
        if v.count("/") >= 3:
            continue  # un percorso, non una chiave
        if re.search(r"[A-Z]", v) and re.search(r"[a-z]", v) and re.search(r"\d", v):
            add("stringa base64 lunga", m)
    for m in TEL_RE.finditer(body):
        prima = body[max(0, m.start() - CONTESTO):m.start()]
        dopo = body[m.end():m.end() + CONTESTO]
        if NON_TEL_DOPO.match(dopo) or re.search(r"\d[.,]$", prima) or re.match(r"[.,]\d", dopo):
            continue  # importo, ore, percentuale o parte di un numero con separatori delle migliaia
        add("telefono", m)

    out, presi = [], []
    for cat, v, a, b in trovati:
        if any(a < y and x < b for x, y in presi):
            continue
        presi.append((a, b))
        out.append((cat, v, a))
    return out


def controlla_riservati(rel, text, body, noti):
    """Un errore per categoria, con la riga della prima occorrenza e solo i primi 4 caratteri."""
    offset = text.count("\n", 0, len(text) - len(body))
    per_cat = defaultdict(list)
    for cat, valore, pos in dati_riservati(body, noti):
        per_cat[cat].append((pos, valore))
    for cat, trovati in per_cat.items():
        pos, valore = min(trovati)
        riga = offset + body.count("\n", 0, pos) + 1
        altre = f", {len(trovati)} occorrenze" if len(trovati) > 1 else ""
        err(rel, f"possibile dato riservato: {cat} (riga {riga}, `{valore[:4]}…`{altre}; CLAUDE.md §5)")


def controlla_configurazione():
    """`vault.yaml` valido, coerente con SPEC 7 e con i permessi mcp (config.py). La
    configurazione, o None se non è valida (gli errori sono già nel rapporto)."""
    try:
        conf = config.carica(ROOT)
    except config.ConfigErrata as e:
        for m in e.errori:
            err(config.FILE, m)
        return None
    for m in config.problemi_spec(ROOT, conf):
        err([config.SPEC, config.FILE], m)
    for dove, m in config.problemi_permessi(ROOT, conf):
        err([dove, config.FILE], m)
    return conf


def controlla_regole():
    """Regole di `.claude/rules/**/*.md` (CLAUDE.md §1): frontmatter leggibile e `paths` una lista
    di pattern (o una stringa separata da virgole). Claude Code tratta una regola con il
    frontmatter illeggibile come una regola senza `paths`, cioè caricata in ogni sessione."""
    cartella = ROOT / ".claude" / "rules"
    if not cartella.is_dir():
        return
    for p in sorted(cartella.rglob("*.md")):
        rel = p.relative_to(ROOT)
        text = p.read_text(encoding="utf-8")
        fm, _ = split_frontmatter(text)
        if fm is None:
            if text.startswith("---"):
                err(rel, "frontmatter non chiuso: la regola verrebbe caricata in ogni sessione")
            continue
        try:
            data = yaml.safe_load(fm)
        except yaml.YAMLError as e:
            err(rel, f"frontmatter non valido ({str(e).splitlines()[0]}): la regola verrebbe caricata in ogni sessione")
            continue
        if not isinstance(data, dict):
            err(rel, "frontmatter non valido (non è una mappa): la regola verrebbe caricata in ogni sessione")
            continue
        if "paths" not in data:
            continue
        paths = data["paths"]
        if isinstance(paths, str):
            paths = [s.strip() for s in paths.split(",")]
        if not isinstance(paths, list) or not paths or not all(isinstance(s, str) and s.strip() for s in paths):
            err(rel, "`paths` deve essere una lista di pattern (stringhe), es. `[\"sources/**\"]`")
            continue
        for pat in paths:
            base = pat.split("*")[0].split("{")[0].split("[")[0].rstrip("/")
            if base and not (ROOT / base).exists():
                avv(rel, f"`paths` `{pat}`: `{base}` non esiste nel vault")


def istante_utc(v):
    try:
        return dt.datetime.strptime(str(v), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    except ValueError:
        return None


def controlla_giro_e_riconciliazione(fonte, rel_stato, state, adesso=None):
    """Riconciliazione dovuta da troppo tempo (P4) e watermark fermo dietro l'ultimo giro (P5).
    Gli errori non bloccano il pre-commit: fermare il giro che scrive lo stato perderebbe le
    sue note e allargherebbe il ritardo; restano nel rapporto, nel digest e in CI."""
    adesso = adesso or dt.datetime.now(dt.timezone.utc)
    dovute = state.get("riconciliazione_dovuta") or {}
    if not isinstance(dovute, dict):
        err(rel_stato, "`riconciliazione_dovuta` illeggibile: deve essere {libreria: istante}", blocca_commit=False)
        dovute = {}
    for libreria, ist in sorted(dovute.items()):
        t = istante_utc(ist)
        if t is None:
            err(rel_stato, f"`riconciliazione_dovuta` di {libreria}: istante `{ist}` non valido", blocca_commit=False)
            continue
        giorni = (adesso - t).total_seconds() / 86400
        comando = "/ingest riconcilia onedrive" if fonte == "onedrive" else f"/ingest riconcilia sharepoint:{libreria}"
        msg = (f"riconciliazione dovuta per {libreria} dal {ist} ({int(giorni)} giorni): {comando}, "
               f"poi `stato.py set-riconciliata {fonte} \"{libreria}\"`")
        if giorni > DOVUTA_ERRORE_GIORNI:
            err(rel_stato, msg, blocca_commit=False)
        elif giorni > DOVUTA_AVVISO_GIORNI:
            avv(rel_stato, msg)
    giro = state.get("ultimo_giro")
    if not isinstance(giro, dict) or not giro.get("risultati"):
        return
    wm, piu_rec = istante_utc(state.get("watermark")), istante_utc(giro.get("piu_recente"))
    if wm and piu_rec and (piu_rec - wm).total_seconds() > WATERMARK_FERMO_GIORNI * 86400:
        falliti = giro.get("falliti") or 0
        causa = (f"{falliti} falliti lo tengono fermo: riprova quei file" if falliti
                 else "nessun fallito: `stato.py set-watermark " + fonte + " --da-giro`")
        avv(rel_stato, f"watermark di {fonte} fermo al {state.get('watermark')}: l'ultimo giro "
                       f"({giro.get('fine')}) ha {giro.get('risultati')} risultati fino al "
                       f"{giro.get('piu_recente')}, più di {WATERMARK_FERMO_GIORNI} giorni dopo ({causa})")


def main():
    indice = "--indice" in sys.argv
    solo_modificati = "--modificati" in sys.argv
    templates = load_templates()
    conf = controlla_configurazione()
    controlla_regole()
    noti = guid_noti(conf)
    by_slug = defaultdict(list)
    parsed = {}

    # 1. Lettura, frontmatter, tipo, slug
    for rel, p in notes():
        by_slug[p.stem].append(rel)
        if not SLUG_RE.match(p.stem):
            err(rel, "nome file non in slug (minuscolo, trattini, senza accenti)")
        text = p.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        controlla_riservati(rel, text, body, noti)
        if fm is None:
            err(rel, "frontmatter mancante")
            continue
        try:
            data = yaml.safe_load(fm) or {}
        except yaml.YAMLError as e:
            err(rel, f"frontmatter non valido ({str(e).splitlines()[0]})")
            continue
        tipo = data.get("type")
        attesi = TYPE_BY_DIR.get(rel.parts[0])
        if tipo not in templates:
            err(rel, f"type sconosciuto: {tipo!r}")
            continue
        if attesi and tipo not in attesi:
            err(rel, f"type {tipo} fuori posto in {rel.parts[0]}/")
        t = templates[tipo]
        mancanti = t["keys"] - set(data)
        extra = set(data) - t["keys"]
        if mancanti:
            err(rel, f"campi mancanti: {', '.join(sorted(mancanti))}")
        if extra:
            avv(rel, f"campi non previsti dal template: {', '.join(sorted(extra))}")
        if t["current"]:
            cur = data.get("current") or {}
            if not isinstance(cur, dict) or t["current"] - set(cur):
                err(rel, "`current` incompleto")
        for key, valori in t["enums"].items():
            if key in data and data[key] not in valori:
                err(rel, f"{key}: {data[key]!r} non è tra {' | '.join(sorted(valori))}")
        if tipo == "project" and rel.parts[0] == "projects" and p.stem != p.parent.name:
            err(rel, "la scheda progetto deve chiamarsi come la cartella")
        parsed[rel] = (data, body)

    # 2. Slug unici
    for slug, paths in by_slug.items():
        if len(paths) > 1:
            err(paths, f"slug `{slug}` duplicato: " + ", ".join(f"`{x}`" for x in paths))

    # 3. Integrità dei collegamenti
    inbound = defaultdict(set)
    links_of = {}
    for rel, (data, body) in parsed.items():
        fm_links = []
        for v in data.values():
            for item in as_list(v):
                if isinstance(item, str):
                    fm_links += wikilinks(item)
        all_links = set(fm_links) | set(wikilinks(body))
        links_of[rel] = all_links
        for target in sorted(all_links):
            if "/" in target or target.endswith(".md"):
                err(rel, f"wikilink con percorso o estensione: [[{target}]] (usa solo lo slug)", target)
            elif target not in by_slug:
                err(rel, f"collegamento rotto: [[{target}]]", target)
            elif rel.stem != target:
                inbound[target].add(rel)
        if data.get("type") in ("source-doc", "source-mail"):
            if not any(as_list(data.get(k)) for k in ("projects", "clients", "topics")):
                err(rel, "fonte senza progetto, cliente o tema")

    # 4. Tracciabilità e affidabilità
    sources = {rel.stem: d for rel, (d, _) in parsed.items() if d.get("type") in ("source-doc", "source-mail")}
    citabili = set(sources) | {rel.stem for rel, (d, _) in parsed.items() if d.get("type") == "session"}
    for rel, (data, body) in parsed.items():
        tipo = data.get("type")
        secs = sections(body)
        for chiave in TRACED_SECTIONS.get(tipo, ()) if conf else ():
            name = conf["sezioni"][chiave]
            for item in untraced_items(secs.get(name, ""), citabili):
                err(rel, f"`## {name}`: punto senza fonte ({item[:60]}…)")
        if tipo in NEED_INBOUND and not inbound.get(rel.stem):
            avv(rel, "nota orfana: nessuna nota la collega")
        if STUB_TAG in as_list(data.get("tags")):
            avv(rel, f"nota creata in automatico, da verificare (tag `{STUB_TAG}`)")
        if tipo in ("source-doc", "source-mail"):
            continue
        updated = as_date(data.get("updated"))
        for target in links_of.get(rel, ()):
            src = sources.get(target)
            if not src:
                continue
            if src.get("status") == "removed":
                avv(rel, f"cita una fonte rimossa: [[{target}]]")
            ingested = as_date(src.get("ingested_at"))
            if updated and ingested and ingested > updated and tipo in ("topic", "client", "project"):
                avv(rel, f"[[{target}]] è stata aggiornata il {ingested} dopo questa nota ({updated}): da rileggere")

    # 5. Doppioni per categoria
    def of_type(tipo):
        return [(rel, d) for rel, (d, _) in parsed.items() if d.get("type") == tipo]

    emails = defaultdict(list)
    for rel, d in of_type("person"):
        e = str(d.get("email") or "").strip().lower()
        if e:
            emails[e].append(rel)
        else:
            avv(rel, "persona senza email")
    for e, paths in emails.items():
        if len(paths) > 1:
            err(paths, f"stessa email {e} in " + ", ".join(f"`{x}`" for x in paths))

    for tipo in ("person", "client", "topic", "project"):
        items = [(rel, norm(rel.stem)) for rel, _ in of_type(tipo)]
        for i, (a, na) in enumerate(items):
            for b, nb in items[i + 1:]:
                if difflib.SequenceMatcher(None, na, nb).ratio() >= SIMILAR:
                    avv(a, f"nome molto simile a `{b}`: possibile doppione")

    for key, tipo in (("family", "source-doc"), ("conversation_id", "source-mail")):
        seen = defaultdict(list)
        for rel, d in of_type(tipo):
            if d.get(key):
                seen[d[key]].append(rel)
        for v, paths in seen.items():
            if len(paths) > 1:
                err(paths, f"{key} `{v}` ripetuto in " + ", ".join(f"`{x}`" for x in paths))
    ids = defaultdict(list)
    for rel, d in of_type("source-doc"):
        iid = (d.get("current") or {}).get("item_id")
        if iid:
            ids[iid].append(rel)
    for iid, paths in ids.items():
        if len(paths) > 1:
            err(paths, f"stesso file (item_id {iid}) in " + ", ".join(f"`{x}`" for x in paths))

    # 6. Stato dell'ingestion: un file per fonte in .state/ (SPEC 6.1)
    tracked = set()
    for fonte, coll in (("sharepoint", "items"), ("onedrive", "items"), ("outlook", "threads"), ("github", "items")):
        rel_stato = f".state/{fonte}.json"
        try:
            state = json.loads((ROOT / rel_stato).read_text(encoding="utf-8"))
        except FileNotFoundError:
            continue  # fonte mai ingerita: stato vuoto
        except (OSError, json.JSONDecodeError) as e:
            err(rel_stato, f"illeggibile ({e})")
            continue
        for key, v in (state.get(coll) or {}).items():
            note = v.get("note", "")
            tracked.add(note)
            if not (ROOT / note).is_file():
                err([rel_stato, note], f"{fonte} `{key}` punta a una nota inesistente: `{note}`")
        controlla_giro_e_riconciliazione(fonte, rel_stato, state)
    for rel, (d, _) in parsed.items():
        if rel.parts[0] != "sources" or d.get("type") != "source-doc":
            continue
        fonte = d.get("source")
        if fonte in ("sharepoint", "onedrive", "github") and "fuori-perimetro" not in as_list(d.get("tags")):
            if str(rel) not in tracked:
                avv(rel, f"documento non registrato nello stato (.state/{fonte}.json)")

    # Solo gli errori che dipendono dalle modifiche in corso (hook di commit)
    if solo_modificati:
        changed = changed_files()
        changed_stems = {Path(c).stem for c in changed}
        mostrati = [e for e in errori if e["blocca_commit"] and (
                    set(e["paths"]) & changed or (e["target"] and e["target"] in changed_stems))]
        if mostrati:
            print("Controllo del vault: errori nei file che stai per committare.\n")
            print("\n".join(f"- `{e['paths'][0]}` · {e['msg']}" for e in mostrati))
            print("\nCorreggili e riprova (per rinominare una nota: .claude/scripts/rinomina-nota.py).")
        return 1 if mostrati else 0

    # Rapporto
    print(f"# Controllo del vault\n\n{len(parsed)} note lette · {len(errori)} errori · {len(avvisi)} avvisi\n")
    print("## Errori\n")
    print("\n".join(f"- `{e['paths'][0]}` · {e['msg']}" for e in errori) or "- nessuno")
    print("\n## Avvisi\n")
    print("\n".join(f"- {a}" for a in avvisi) or "- nessuno")

    if indice:
        print("\n## Indice\n")
        for tipo, titolo, campi in (
            ("project", "Progetti", ("status", "clients")),
            ("client", "Clienti", ("status", "sector")),
            ("person", "Persone", ("org", "email")),
            ("topic", "Temi", ("kind",)),
        ):
            righe = of_type(tipo)
            print(f"### {titolo} ({len(righe)})\n")
            if not righe:
                print("- nessuno\n")
                continue
            print("| Nota | " + " | ".join(campi) + " | Collegata da |")
            print("|---|" + "---|" * len(campi) + "---|")
            for rel, d in sorted(righe, key=lambda x: x[0].stem):
                vals = [", ".join(map(str, as_list(d.get(c)))) for c in campi]
                print(f"| [[{rel.stem}]] | " + " | ".join(vals) + f" | {len(inbound.get(rel.stem, ()))} |")
            print()
        fonti = defaultdict(int)
        for rel in parsed:
            if rel.parts[0] == "sources":
                fonti[rel.parts[1]] += 1
        print("### Fonti\n")
        print("\n".join(f"- {k}: {v}" for k, v in sorted(fonti.items())) or "- nessuna")

    return 1 if errori else 0


if __name__ == "__main__":
    sys.exit(main())
