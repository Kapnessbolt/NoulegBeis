#!/usr/bin/env python3
"""Sposta o rinomina una nota fonte quando il documento cambia posizione o nome (SPEC 6.4).

Uso:
  python3 .claude/scripts/sposta-nota.py <nota> --web-url "<nuovo webUrl>" [--item-id <id>]
          [--uri file:///<driveId>/<itemId>] [--last-modified <ISO UTC>] [--slug <slug>] [--json]

È l'unico modo per spostare una nota `source-doc` di SharePoint o OneDrive: lo usano la
riconciliazione (`riconcilia.py --applica`), il rilevatore e le sessioni, mai `git mv` o
`rinomina-nota.py` a mano. `<nota>` è il percorso relativo (`sources/...md`) o lo slug. Se il
percorso non esiste più (spostamento già fatto) la nota si cerca per slug e poi per
`current.web_url` uguale a `--web-url`, così ripetere lo stesso comando non sbaglia.

Passi, tutti idempotenti (ripetuto con gli stessi argomenti stampa «nessuna modifica»):
1. `perimetro.py` sul nuovo `webUrl`: URL non del tenant → uscita 2; fuori perimetro o senza
   cartella di nota → uscita 1 con il motivo, e nulla si tocca (decide l'agente).
2. Nome nuovo: ultimo segmento dell'URL, decodificato. Famiglia nuova: `famiglia.py` del nome,
   con il prefisso di disambiguazione della `family` attuale se c'era (`family` che finisce con
   `-<famiglia del current.name>`); se la famiglia calcolata non cambia, `family` resta com'è.
   Se la famiglia cambia e lo slug della nota era uguale alla `family` vecchia, lo slug nuovo
   è la famiglia nuova; `--slug` lo sceglie a mano. Slug nuovo già usato → uscita 1 (passa
   `--slug`).
3. Cartella cambiata: il file va in `<cartella_nota>/<slug>.md` (rename + `git add -A`, la
   cartella si crea, quella vecchia si toglie se resta vuota) e le voci dello stato di tutte
   le fonti che puntavano al percorso vecchio passano al nuovo.
4. Slug cambiato: `rinomina-nota.py <vecchio> <nuovo> --family <nuova>` (wikilink, `family`,
   stato).
5. Frontmatter (stile delle righe invariato, validato come `aggiorna-nota.py`):
   `current.web_url`, `current.name` e, se passati, `current.item_id`, `current.uri`,
   `current.last_modified` (`--item-id` senza `--uri` cambia l'itemId in `current.uri`;
   `--uri` senza `--item-id` prende l'itemId dall'uri); la voce di `versions` uguale alla
   `current` vecchia (stesso `item_id` e `last_modified`) prende nome, `item_id` e
   `last_modified` nuovi; `family`; `status: removed` torna `active`; `source` segue la fonte
   del nuovo URL.
6. Stato: se `--item-id` o `--uri` danno una chiave nuova (`<driveId>/<itemId>` dall'uri),
   voce nuova sulla stessa nota con `--last-modified` (o `current.last_modified`) nella fonte
   del nuovo URL, come `stato.py collega`; le voci vecchie restano (SPEC 6.1). Una chiave già
   registrata su un'altra nota → uscita 1.
Niente commit.

Uscita: 0 se fatto o se non c'era niente da fare; 1 se il nuovo URL è fuori perimetro, lo slug
nuovo è occupato o la chiave nuova è di un'altra nota; 2 per errori d'uso, URL non
riconosciuto, nota non trovata o non `source-doc` di SharePoint o OneDrive, frontmatter non
valido. Con `--json` stampa:
  {"nota_prima", "nota_dopo", "cartella_cambiata": bool, "slug_cambiato": bool,
   "family_prima", "family_dopo", "chiavi_stato": ["<chiave>", ...] (voci dello stato aggiornate
   o create, in qualunque fonte),
   "campi_cambiati": ["current.web_url", "family", ...], "cambiato": bool, "avvisi": [...]}
Senza `--json` una riga.

La variabile d'ambiente VAULT_ROOT, se presente, indica la radice del vault al posto della
cartella che contiene `.claude/` (serve ai test in `.claude/scripts/tests/`).
"""

import copy
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

QUI = Path(__file__).resolve().parent
sys.path.insert(0, str(QUI))
import famiglia  # noqa: E402
import nota  # noqa: E402
import perimetro  # noqa: E402
import stato  # noqa: E402

ROOT = nota.ROOT
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
URI_RE = re.compile(r"^file:///([^/]+)/([^/]+)$")
FONTI_DOC = ("sharepoint", "onedrive")


class Uscita(Exception):
    """Errore con il suo codice di uscita (1 o 2)."""

    def __init__(self, codice, messaggio):
        super().__init__(messaggio)
        self.codice = codice


# --- Nota -------------------------------------------------------------------------------

def leggi_nota(rel):
    """(frontmatter testuale, dizionario, resto del testo) della nota."""
    try:
        fm, resto = nota.dividi((ROOT / rel).read_text(encoding="utf-8"))
        data = yaml.safe_load(fm) or {}
    except (nota.Errore, yaml.YAMLError) as e:
        raise Uscita(2, f"`{rel}`: frontmatter non valido ({str(e).splitlines()[0]})")
    if not isinstance(data, dict):
        raise Uscita(2, f"`{rel}`: frontmatter non valido")
    return fm, data, resto


def note_fonte():
    """Percorsi relativi delle note in sources/."""
    for p in sorted((ROOT / "sources").rglob("*.md")):
        yield p.relative_to(ROOT)


def url_uguali(a, b):
    return unquote(str(a or "")).strip().casefold() == unquote(str(b or "")).strip().casefold()


def trova_nota(arg, web_url):
    """Percorso relativo della nota da spostare, da percorso o slug (anche a spostamento fatto)."""
    p = Path(arg)
    if p.is_absolute():
        try:
            p = p.resolve().relative_to(ROOT)
        except ValueError:
            raise Uscita(2, f"`{arg}` non è dentro il vault")
    if p.suffix == ".md" and (ROOT / p).is_file():
        return p
    stem = p.stem if p.suffix == ".md" else str(p)
    trovate = [r for r in note_fonte() if r.stem == stem]
    if len(trovate) > 1:
        raise Uscita(2, f"slug `{stem}` duplicato: " + ", ".join(map(str, trovate)))
    if trovate:
        return trovate[0]
    if p.suffix == ".md":
        stessa_url = []
        for r in note_fonte():
            try:
                _, d, _ = leggi_nota(r)
            except Uscita:
                continue
            cur = d.get("current")
            if isinstance(cur, dict) and url_uguali(cur.get("web_url"), web_url):
                stessa_url.append(r)
        if len(stessa_url) == 1:
            return stessa_url[0]
    raise Uscita(2, f"nota `{arg}` non trovata")


# --- Calcoli ----------------------------------------------------------------------------

def nome_da_url(web_url):
    percorso = urlsplit(str(web_url).strip()).path.rstrip("/")
    return unquote(percorso.rsplit("/", 1)[-1])


def family_nuova(family, nome_vecchio, nome_nuovo):
    """`family` dopo il cambio di nome: invariata se la famiglia calcolata non cambia, con il
    prefisso di disambiguazione conservato se c'era."""
    calc_vecchia = famiglia.famiglia(nome_vecchio) if nome_vecchio else ""
    calc_nuova = famiglia.famiglia(nome_nuovo)
    if calc_nuova == calc_vecchia or not calc_nuova:
        return family
    family = str(family or "")
    if calc_vecchia and family != calc_vecchia and family.endswith(f"-{calc_vecchia}"):
        return f"{family[:-len(calc_vecchia) - 1]}-{calc_nuova}"
    return calc_nuova


def chiave_da_uri(uri):
    m = URI_RE.match(str(uri or ""))
    return f"{m.group(1)}/{m.group(2)}" if m else None


def item_da_uri(uri):
    m = URI_RE.match(str(uri or ""))
    return m.group(2) if m else None


def uri_con_item(uri, item_id):
    m = URI_RE.match(str(uri or ""))
    return f"file:///{m.group(1)}/{item_id}" if m else None


def frontmatter_nuovo(vecchio, sch, fonte, web_url, nome, item_id, uri, last_modified, family):
    """Il frontmatter dopo lo spostamento (passo 5), dal frontmatter attuale."""
    nuovo = copy.deepcopy(vecchio)
    cur = dict(nuovo.get("current") or {})
    prima = dict(cur)
    if not url_uguali(cur.get("web_url"), web_url):
        cur["web_url"] = web_url
    cur["name"] = nome
    if item_id is not None:
        cur["item_id"] = item_id
    if uri is not None:
        cur["uri"] = uri
    if last_modified is not None:
        cur["last_modified"] = nota.a_istante(last_modified, "--last-modified")
    nuovo["current"] = cur
    vecchia = {"item_id": prima.get("item_id"), "last_modified": prima.get("last_modified")}
    recente = {"name": cur.get("name") or "", "item_id": cur.get("item_id") or "",
               "last_modified": cur.get("last_modified")}
    versioni, sostituita = [], False
    for v in nuovo.get("versions") or []:
        if isinstance(v, dict) and not sostituita and _stessa(v, vecchia):
            versioni.append({**v, **recente})
            sostituita = True
        elif isinstance(v, dict) and sostituita and _stessa(v, recente):
            continue  # la voce nuova c'è già: niente doppioni
        else:
            versioni.append(v)
    if "versions" in nuovo:
        nuovo["versions"] = versioni
    if nuovo.get("status") == "removed":
        nuovo["status"] = "active"
    if nuovo.get("source") != fonte:
        nuovo["source"] = fonte
    nuovo["family"] = family
    errori, avvisi = nota.valida(nuovo, sch, extra_ammesse=set(vecchio) - set(sch["default"]))
    if errori:
        raise Uscita(2, "frontmatter non valido: " + "; ".join(errori))
    return nuovo, avvisi


def _stessa(a, b):
    return (str(a.get("item_id") or "") == str(b.get("item_id") or "")
            and nota.normale(a.get("last_modified")) == nota.normale(b.get("last_modified")))


def campi_diversi(prima, dopo):
    out = []
    for k in dopo:
        a, b = prima.get(k), dopo.get(k)
        if isinstance(a, dict) and isinstance(b, dict):
            out += [f"{k}.{s}" for s in b if nota.normale(a.get(s)) != nota.normale(b.get(s))]
        elif nota.normale(a) != nota.normale(b):
            out.append(k)
    return out


# --- Azioni -----------------------------------------------------------------------------

def git_mv(src, dst):
    """Come in rinomina-nota.py: rename, poi `git add -A` perché git veda lo spostamento."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    src.rename(dst)
    subprocess.run(["git", "add", "-A", "--", str(src), str(dst)], cwd=ROOT, check=False,
                   capture_output=True)
    cartella = src.parent
    while len(cartella.relative_to(ROOT).parts) > 2 and not any(cartella.iterdir()):
        cartella.rmdir()
        cartella = cartella.parent


def voci_della_nota(rel):
    """[(fonte, chiave)] delle voci dello stato che puntano alla nota."""
    out = []
    for fonte, coll in stato.COLLEZIONE.items():
        if stato.percorso(fonte).exists():
            out += [(fonte, k) for k, v in stato.leggi(fonte)[coll].items() if v.get("note") == str(rel)]
    return out


def sposta_nello_stato(prima, dopo):
    cambiate = []
    for fonte, coll in stato.COLLEZIONE.items():
        if not stato.percorso(fonte).exists():
            continue
        data = stato.leggi(fonte)
        chiavi = [k for k, v in data[coll].items() if v.get("note") == str(prima)]
        for k in chiavi:
            data[coll][k]["note"] = str(dopo)
        if chiavi:
            stato.scrivi(fonte, data)
            cambiate += [k for k in chiavi if k not in cambiate]
    return cambiate


def rinomina(vecchio, nuovo, family):
    res = subprocess.run([sys.executable, str(QUI / "rinomina-nota.py"), vecchio, nuovo, "--family", family],
                         cwd=ROOT, capture_output=True, text=True)
    if res.returncode != 0:
        raise Uscita(2, f"rinomina-nota.py non riuscito: {(res.stderr or res.stdout).strip()}")


def sposta(arg, web_url, item_id=None, uri=None, last_modified=None, slug_scelto=None):
    web_url = str(web_url).strip()
    if last_modified is not None:
        try:
            stato.istante(last_modified, "--last-modified")
        except stato.Errore as e:
            raise Uscita(2, str(e))
    if uri is not None and not URI_RE.match(uri):
        raise Uscita(2, f"--uri `{uri}` non è nella forma file:///<driveId>/<itemId>")
    if item_id is not None and "/" in item_id:
        raise Uscita(2, f"--item-id `{item_id}` non valido: è l'itemId, senza il driveId")
    if slug_scelto is not None and not SLUG_RE.match(slug_scelto):
        raise Uscita(2, f"--slug `{slug_scelto}` non è uno slug valido")

    # 1. perimetro
    an = perimetro.analizza(web_url)
    if not an.get("riconosciuto", True):
        raise Uscita(2, f"URL non riconosciuto: {an['motivo']}")
    if not an["dentro"] or not an["cartella_nota"]:
        motivo = an["motivo"] or "nessuna cartella di nota per questo URL"
        raise Uscita(1, f"fuori perimetro ({motivo}): la nota non si sposta, decide l'agente")
    fonte = an["fonte"]

    rel = trova_nota(arg, web_url)
    fm, vecchio, _ = leggi_nota(rel)
    if vecchio.get("type") != "source-doc" or vecchio.get("source") not in FONTI_DOC:
        raise Uscita(2, f"`{rel}` non è una nota source-doc di SharePoint o OneDrive")
    sch = nota.schema("source-doc")
    cur = vecchio.get("current") or {}
    avvisi = []

    # 2. nome, famiglia, slug
    nome = nome_da_url(web_url)
    family_prima = vecchio.get("family")
    family = family_nuova(family_prima, cur.get("name"), nome)
    slug = rel.stem
    if slug_scelto:
        slug = slug_scelto
    elif family != family_prima and rel.stem == family_prima and SLUG_RE.match(str(family or "")):
        slug = family
    slug_cambiato = slug != rel.stem
    if slug_cambiato and slug in nota.slug_esistenti():
        raise Uscita(1, f"lo slug `{slug}` è già di un'altra nota: passa --slug <slug libero>")
    cartella = Path(an["cartella_nota"])
    cartella_cambiata = cartella != rel.parent
    dopo = cartella / f"{slug}.md"
    if cartella_cambiata and (ROOT / cartella / rel.name).exists():
        raise Uscita(1, f"`{cartella / rel.name}` esiste già")

    # identità: itemId, uri e chiave dello stato
    if item_id is not None and uri is None:
        uri = uri_con_item(cur.get("uri"), item_id)
        if uri is None:
            avvisi.append(f"current.uri `{cur.get('uri')}` non è file:///<driveId>/<itemId>: passa --uri")
    elif uri is not None and item_id is None and uri != cur.get("uri"):
        item_id = item_da_uri(uri)
    if uri is not None and uri == cur.get("uri"):
        uri = None
    if fonte != vecchio.get("source") and uri is None:
        avvisi.append(f"la nota passa da {vecchio.get('source')} a {fonte}: passa anche --uri")
    chiave_nuova = chiave_da_uri(uri) if uri else None
    istante = last_modified or nota.normale(cur.get("last_modified"))
    if chiave_nuova and not istante:
        raise Uscita(2, "chiave nuova nello stato senza istante: passa --last-modified")
    if chiave_nuova:
        voce = stato.leggi(fonte)[stato.COLLEZIONE[fonte]].get(chiave_nuova)
        if voce and voce.get("note") not in (str(rel), str(dopo), str(rel.parent / f"{slug}.md")):
            raise Uscita(1, f"la chiave {fonte}:{chiave_nuova} è già registrata su `{voce.get('note')}`")
    # frontmatter validato prima di toccare qualcosa
    _, avv = frontmatter_nuovo(vecchio, sch, fonte, web_url, nome, item_id, uri, last_modified, family)
    avvisi += avv

    chiavi_stato = []
    # 3. cartella
    attuale = rel
    if cartella_cambiata:
        git_mv(ROOT / rel, ROOT / cartella / rel.name)
        attuale = cartella / rel.name
        chiavi_stato += sposta_nello_stato(rel, attuale)
    # 4. slug (rinomina-nota aggiorna wikilink, family e stato)
    if slug_cambiato:
        chiavi_stato += [k for _, k in voci_della_nota(attuale) if k not in chiavi_stato]
        rinomina(attuale.stem, slug, family)
        attuale = dopo
    # 5. frontmatter, riletto dopo lo spostamento
    fm, attuale_fm, resto = leggi_nota(attuale)
    nuovo, _ = frontmatter_nuovo(attuale_fm, sch, fonte, web_url, nome, item_id, uri, last_modified, family)
    if nota.normale(nuovo) != nota.normale(attuale_fm):
        nota.scrivi_atomico(ROOT / attuale, nota.unisci(nota.riscrivi_frontmatter(fm, attuale_fm, nuovo), resto))
    # 6. voce nuova nello stato
    if chiave_nuova:
        data = stato.leggi(fonte)
        coll = data[stato.COLLEZIONE[fonte]]
        voce = dict(coll.get(chiave_nuova) or {})
        if voce.get("note") != str(attuale) or "assente" in voce:
            voce.pop("assente", None)
            voce["note"] = str(attuale)
            if stato.piu_recente(istante, voce.get("last_modified")):
                voce["last_modified"] = istante
            coll[chiave_nuova] = voce
            stato.scrivi(fonte, data)
            if chiave_nuova not in chiavi_stato:
                chiavi_stato.append(chiave_nuova)

    campi = campi_diversi(vecchio, nuovo)
    return {
        "nota_prima": str(rel),
        "nota_dopo": str(attuale),
        "cartella_cambiata": cartella_cambiata,
        "slug_cambiato": slug_cambiato,
        "family_prima": family_prima,
        "family_dopo": nuovo.get("family"),
        "chiavi_stato": chiavi_stato,
        "campi_cambiati": campi,
        "cambiato": bool(cartella_cambiata or slug_cambiato or campi or chiavi_stato),
        "avvisi": avvisi,
    }


# --- Riga di comando --------------------------------------------------------------------

OPZIONI = {"--web-url": "web_url", "--item-id": "item_id", "--uri": "uri",
           "--last-modified": "last_modified", "--slug": "slug_scelto"}


def main(argv):
    if not argv or any(a in ("-h", "--help") for a in argv):
        print(__doc__)
        return 0 if argv else 2
    pos, opt, as_json = [], {}, False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--json":
            as_json = True
        elif a in OPZIONI:
            if i + 1 >= len(argv) or not argv[i + 1].strip():
                raise Uscita(2, f"{a} vuole un valore")
            opt[OPZIONI[a]] = argv[i + 1].strip()
            i += 1
        elif a.startswith("--"):
            raise Uscita(2, f"opzione sconosciuta: {a}")
        else:
            pos.append(a)
        i += 1
    if len(pos) != 1:
        raise Uscita(2, "serve una nota: sposta-nota.py <nota> --web-url <nuovo webUrl> (--help)")
    if "web_url" not in opt:
        raise Uscita(2, "--web-url è obbligatorio")
    esito = sposta(pos[0], **opt)
    for a in esito["avvisi"]:
        sys.stderr.write(f"avviso: {a}\n")
    if as_json:
        print(json.dumps(esito, ensure_ascii=False, indent=2))
    elif not esito["cambiato"]:
        print(f"{esito['nota_dopo']}: nessuna modifica")
    else:
        parti = []
        if esito["nota_dopo"] != esito["nota_prima"]:
            parti.append(f"→ {esito['nota_dopo']}")
        if esito["campi_cambiati"]:
            parti.append("campi: " + ", ".join(esito["campi_cambiati"]))
        if esito["chiavi_stato"]:
            parti.append("stato: " + ", ".join(esito["chiavi_stato"]))
        print(f"{esito['nota_prima']}: " + "; ".join(parti))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Uscita as e:
        sys.stderr.write(f"errore: {e}\n")
        sys.exit(e.codice)
    except (nota.Errore, stato.Errore) as e:
        sys.stderr.write(f"errore: {e}\n")
        sys.exit(2)
