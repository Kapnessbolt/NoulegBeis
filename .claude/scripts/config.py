#!/usr/bin/env python3
"""Configurazione del vault (SPEC 13.1, step 13): legge e valida `vault.yaml` alla radice.

Tutto ciò che distingue un vault da un altro (utente, fuso, sezioni, perimetro delle fonti,
server dei connettori, task schedulati) sta in `vault.yaml`; gli script lo leggono da qui con
`carica()` e le funzioni sotto, routine e comandi con la riga di comando.

Uso:
  python3 .claude/scripts/config.py oggi                 # data di oggi nel fuso del vault (AAAA-MM-GG)
  python3 .claude/scripts/config.py ora                  # ora attuale nel fuso del vault (HH:MM)
  python3 .claude/scripts/config.py valore <chiave>      # un valore, chiave puntata (`vault.fuso`,
                                                         # `fonti.sharepoint.librerie`, `task.0.nome`);
                                                         # le liste una voce per riga, gli oggetti in JSON
  python3 .claude/scripts/config.py task [AAAA-MM-GG] [--digest] [--json]
      # giri attesi del giorno (predefinito: oggi), uno per riga `HH:MM <task>` in ordine di ora;
      # con --digest solo i task che scrivono la riga d'esito nel digest
  python3 .claude/scripts/config.py verifica             # schema, orari di SPEC 7, permessi e `tools`
  python3 .claude/scripts/config.py applica              # riscrive da vault.yaml i permessi
      # `mcp__<server>__<strumento>` di `.claude/settings.json` e la parte mcp della riga
      # `tools:` degli agenti in `agenti`; il resto resta com'è. Idempotente.

Uscita: 0 se va tutto bene; 1 se `vault.yaml` non è valido, se `verifica` trova errori o se
la chiave di `valore` non esiste; 2 se gli argomenti non sono validi. Richiede PyYAML.

Permessi attesi: in `.claude/settings.json` tutti gli strumenti di tutti i gruppi di ogni
connettore, per ogni nome di server; nei `tools` di ogni agente in `.claude/agents/` gli
strumenti elencati in `agenti` (nessuno se l'agente non c'è). Un server o uno strumento mcp in
più è un errore come uno che manca.

La variabile d'ambiente VAULT_ROOT, se presente, indica la radice del vault al posto della
cartella che contiene `.claude/` (serve ai test in `.claude/scripts/tests/`).
"""

import datetime as dt
import json
import os
import re
import sys
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

try:
    import yaml
except ImportError:
    sys.exit("Manca PyYAML: pip install pyyaml")

ROOT = Path(os.environ.get("VAULT_ROOT") or Path(__file__).resolve().parents[2]).resolve()
FILE = "vault.yaml"
SETTINGS = ".claude/settings.json"
AGENTI = ".claude/agents"
SPEC = "SPEC.md"
SPEC_TITOLO_TASK = "## 7. Task schedulati"

ORA_RE = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")
ORA_NEL_TESTO_RE = re.compile(r"\b(?:[01]\d|2[0-3]):[0-5]\d\b")
NOME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
STRUMENTO_RE = re.compile(r"^[A-Za-z0-9_-]+$")

# Giorni della settimana (0 = lunedì, come `date.weekday()`), con e senza accento
GIORNI = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]
NOMI_GIORNI = {}
for _n, _g in enumerate(GIORNI):
    for _forma in (_g, _g.replace("ì", "i"), _g[:3]):
        NOMI_GIORNI[_forma] = _n
TUTTI = frozenset(range(7))

# Sezioni che gli script leggono o controllano: chiave in `sezioni`
SEZIONI = ("stato", "attivita", "decisioni", "prossimi_passi", "fonti", "chi_sono", "relazione",
           "punti_chiave", "interazioni", "novita", "esito_task", "da_fare")


class ConfigErrata(Exception):
    """`vault.yaml` mancante o non valido: `errori` è la lista dei problemi."""

    def __init__(self, errori):
        self.errori = list(errori)
        super().__init__("\n".join(self.errori))


# --- Caricamento e validazione ------------------------------------------------------------

def giorni(valore):
    """Insieme dei giorni (0 = lunedì) da `ogni-giorno`, `domenica`, `lun-ven`, `lun, mer` o
    una lista di questi. ValueError se un nome non si riconosce."""
    voci = valore if isinstance(valore, list) else str(valore).split(",")
    out = set()
    for voce in voci:
        v = str(voce).strip().lower()
        if v in ("ogni-giorno", "ogni giorno", "tutti"):
            out |= TUTTI
        elif v in NOMI_GIORNI:
            out.add(NOMI_GIORNI[v])
        elif "-" in v and all(p.strip() in NOMI_GIORNI for p in v.split("-", 1)):
            a, b = (NOMI_GIORNI[p.strip()] for p in v.split("-", 1))
            out |= {(a + i) % 7 for i in range((b - a) % 7 + 1)}
        else:
            raise ValueError(f"giorno non riconosciuto: {voce!r}")
    if not out:
        raise ValueError("nessun giorno")
    return frozenset(out)


def descrivi_giorni(insieme):
    if insieme == TUTTI:
        return "ogni giorno"
    return ", ".join(GIORNI[g] for g in sorted(insieme))


def _valida(c):
    """Lista degli errori di schema (vuota se `c` è valido)."""
    errori = []

    def e(chiave, msg):
        errori.append(f"{FILE}: `{chiave}` {msg}")

    def testo(d, chiave, nome):
        v = d.get(chiave) if isinstance(d, dict) else None
        if not isinstance(v, str) or not v.strip():
            e(nome, "deve essere un testo non vuoto")
            return None
        return v

    def lista_testi(d, chiave, nome, vuota=False):
        v = d.get(chiave) if isinstance(d, dict) else None
        if not isinstance(v, list) or not all(isinstance(x, str) and x.strip() for x in v):
            e(nome, "deve essere una lista di testi")
            return []
        if not v and not vuota:
            e(nome, "non può essere vuota")
        return v

    def oggetto(d, chiave, nome):
        v = d.get(chiave) if isinstance(d, dict) else None
        if not isinstance(v, dict):
            e(nome, "manca o non è un oggetto")
            return {}
        return v

    if not isinstance(c, dict):
        return [f"{FILE}: il file deve contenere un oggetto YAML"]
    if c.get("versione") != 1:
        e("versione", f"deve essere 1 (trovato: {c.get('versione')!r})")

    v = oggetto(c, "vault", "vault")
    for k in ("nome", "utente", "organizzazione", "organizzazione_slug", "dominio_organizzazione",
              "lingua", "titolo_cockpit"):
        testo(v, k, f"vault.{k}")
    fuso = testo(v, "fuso", "vault.fuso")
    if fuso:
        try:
            ZoneInfo(fuso)
        except (ZoneInfoNotFoundError, ValueError):
            e("vault.fuso", f"non è un fuso orario IANA valido: {fuso!r} (es. Europe/Rome)")

    s = oggetto(c, "sezioni", "sezioni")
    for k in SEZIONI:
        testo(s, k, f"sezioni.{k}")

    conn = oggetto(c, "connettori", "connettori")
    for nome, d in conn.items():
        if not isinstance(d, dict):
            e(f"connettori.{nome}", "deve essere un oggetto con `server` e i gruppi di strumenti")
            continue
        for srv in lista_testi(d, "server", f"connettori.{nome}.server"):
            if not STRUMENTO_RE.match(srv):
                e(f"connettori.{nome}.server", f"nome di server non valido: {srv!r}")
        gruppi = [k for k in d if k != "server"]
        if not gruppi:
            e(f"connettori.{nome}", "non ha gruppi di strumenti (es. `lettura`)")
        for g in gruppi:
            for t in lista_testi(d, g, f"connettori.{nome}.{g}"):
                if not STRUMENTO_RE.match(t):
                    e(f"connettori.{nome}.{g}", f"nome di strumento non valido: {t!r}")

    agenti = c.get("agenti", {})
    if not isinstance(agenti, dict):
        e("agenti", "deve essere un oggetto `agente: [connettore.gruppo, …]`")
        agenti = {}
    for agente, voci in agenti.items():
        if not isinstance(voci, list):
            e(f"agenti.{agente}", "deve essere una lista")
            continue
        for voce in voci:
            nome, _, parte = str(voce).partition(".")
            d = conn.get(nome)
            if not isinstance(d, dict):
                e(f"agenti.{agente}", f"connettore sconosciuto in {voce!r}")
            elif parte == "server" or not (parte in d or any(
                    isinstance(x, list) and parte in x for k, x in d.items() if k != "server")):
                e(f"agenti.{agente}", f"{voce!r}: `{parte}` non è un gruppo né uno strumento di `{nome}`")

    f = oggetto(c, "fonti", "fonti")
    sp = oggetto(f, "sharepoint", "fonti.sharepoint")
    od = oggetto(f, "onedrive", "fonti.onedrive")
    for d, nome in ((sp, "fonti.sharepoint"), (od, "fonti.onedrive")):
        t = testo(d, "tenant", f"{nome}.tenant")
        if t and not re.match(r"^https://[^/\s]+$", t.rstrip("/")):
            e(f"{nome}.tenant", f"deve essere un indirizzo https:// senza percorso (trovato: {t!r})")
    testo(sp, "sito", "fonti.sharepoint.sito")
    lista_testi(sp, "librerie", "fonti.sharepoint.librerie")
    for k in ("utente", "libreria", "cartella", "cartella_chat_finale"):
        testo(od, k, f"fonti.onedrive.{k}")
    es = oggetto(f, "esclusioni", "fonti.esclusioni")
    lista_testi(es, "cartelle", "fonti.esclusioni.cartelle", vuota=True)
    lista_testi(es, "finali", "fonti.esclusioni.finali", vuota=True)
    dentro = es.get("dentro", [])
    if not isinstance(dentro, list) or not all(
            isinstance(p, list) and len(p) == 2 and all(isinstance(x, str) for x in p) for p in dentro):
        e("fonti.esclusioni.dentro", "deve essere una lista di coppie [genitore, cartella]")
    lista_testi(f, "tipi_processati", "fonti.tipi_processati")
    lista_testi(f, "firme_in_coda", "fonti.firme_in_coda", vuota=True)
    lista_testi(oggetto(f, "outlook", "fonti.outlook"), "mittenti_scartati",
                "fonti.outlook.mittenti_scartati", vuota=True)
    repo = oggetto(f, "github", "fonti.github").get("repository", [])
    if not isinstance(repo, list):
        e("fonti.github.repository", "deve essere una lista")
        repo = []
    for n, r in enumerate(repo):
        for k in ("repo", "branch", "progetto"):
            testo(r, k, f"fonti.github.repository.{n}.{k}")

    task = c.get("task")
    if not isinstance(task, list) or not task:
        e("task", "deve essere una lista non vuota")
        task = []
    visti = set()
    for n, t in enumerate(task):
        if not isinstance(t, dict):
            e(f"task.{n}", "deve essere un oggetto")
            continue
        nome = testo(t, "nome", f"task.{n}.nome") or f"#{n}"
        dove = f"task.{nome}"
        if not NOME_RE.match(nome):
            e(dove, "nome non in slug (minuscolo, trattini)")
        if nome in visti:
            e(dove, "task ripetuto")
        visti.add(nome)
        orari = lista_testi(t, "orari", f"{dove}.orari")
        for o in orari:
            if not ORA_RE.match(o):
                e(f"{dove}.orari", f"orario non valido: {o!r} (serve HH:MM tra virgolette)")
        if len(set(orari)) != len(orari):
            e(f"{dove}.orari", "orari ripetuti")
        try:
            giorni(t.get("giorni"))
        except ValueError as ex:
            e(f"{dove}.giorni", f"non valido ({ex}): usa ogni-giorno, domenica, lun-ven, …")
        testo(t, "modello", f"{dove}.modello")
        for k in lista_testi(t, "connettori", f"{dove}.connettori", vuota=True):
            if k not in conn:
                e(f"{dove}.connettori", f"connettore `{k}` non definito in `connettori`")
        nc = t.get("nome_claude")
        if nc is not None:
            nc_lista = nc if isinstance(nc, list) else [nc]
            if not all(isinstance(x, str) and x.strip() for x in nc_lista):
                e(f"{dove}.nome_claude", "deve essere un testo o una lista di testi")
            elif isinstance(nc, list) and len(nc) != len(orari):
                e(f"{dove}.nome_claude", f"{len(nc)} nomi per {len(orari)} orari")
        if "digest" in t and not isinstance(t["digest"], bool):
            e(f"{dove}.digest", "deve essere true o false")
    return errori


def da_testo(testo):
    """Configurazione da un testo YAML; ConfigErrata se non è valida."""
    try:
        c = yaml.safe_load(testo)
    except yaml.YAMLError as ex:
        raise ConfigErrata([f"{FILE}: YAML non valido ({str(ex).splitlines()[0]})"])
    errori = _valida(c)
    if errori:
        raise ConfigErrata(errori)
    return c


_cache = {}


def carica(root=None):
    """Configurazione di `<root>/vault.yaml` (predefinito: la radice del vault), validata.

    Il risultato si tiene in memoria per radice; `imposta()` lo sostituisce (serve ai test)."""
    root = Path(root or ROOT).resolve()
    if root not in _cache:
        path = root / FILE
        try:
            testo = path.read_text(encoding="utf-8")
        except FileNotFoundError:
            raise ConfigErrata([f"{FILE}: manca in {root} (è la configurazione del vault, SPEC 13.1)"])
        _cache[root] = da_testo(testo)
    return _cache[root]


def imposta(c, root=None):
    """Usa `c` come configurazione della radice (None: dimentica quella in memoria)."""
    root = Path(root or ROOT).resolve()
    if c is None:
        _cache.pop(root, None)
    else:
        _cache[root] = c


# --- Valori per gli script -----------------------------------------------------------------

def fuso(c=None):
    return ZoneInfo((c or carica())["vault"]["fuso"])


def adesso(c=None):
    return dt.datetime.now(fuso(c))


def oggi(c=None):
    return adesso(c).date()


def sezione(chiave, c=None):
    """Titolo (senza `## `) della sezione con quella chiave in `sezioni`."""
    return (c or carica())["sezioni"][chiave]


def valore(chiave, c=None):
    """Valore per chiave puntata (`fonti.sharepoint.tenant`, `task.0.nome`); KeyError se manca."""
    v = c or carica()
    for parte in chiave.split("."):
        if isinstance(v, dict) and parte in v:
            v = v[parte]
        elif isinstance(v, list) and parte.isdigit() and int(parte) < len(v):
            v = v[int(parte)]
        else:
            raise KeyError(chiave)
    return v


def task_del_giorno(giorno, c=None, solo_digest=False):
    """[(orario, task)] dei giri attesi in `giorno` (date), in ordine di ora.

    Con `solo_digest` esclude i task con `digest: false` (non scrivono la riga d'esito)."""
    out = []
    for t in (c or carica())["task"]:
        if solo_digest and t.get("digest") is False:
            continue
        if giorno.weekday() in giorni(t["giorni"]):
            out += [(o, t["nome"]) for o in t["orari"]]
    return sorted(out)


def perimetro(c=None):
    """Valori del perimetro di SharePoint e OneDrive (SPEC 5.1-5.2) per `perimetro.py`."""
    f = (c or carica())["fonti"]
    sp, od, es = f["sharepoint"], f["onedrive"], f["esclusioni"]
    sharepoint = sp["tenant"].rstrip("/") + "/sites/"
    onedrive = od["tenant"].rstrip("/") + "/personal/"
    cartella_od = f"{onedrive}{od['utente']}/{od['libreria']}/{od['cartella']}/"
    return {
        "sharepoint": sharepoint,
        "onedrive": onedrive,
        "sito": sp["sito"],
        "onedrive_utente": od["utente"],
        "onedrive_libreria": od["libreria"],
        "onedrive_cartella": od["cartella"],
        "prefissi": tuple(f"{sharepoint}{sp['sito']}/{lib}/" for lib in sp["librerie"]) + (cartella_od,),
        "cartelle_escluse": {x.lower() for x in es.get("cartelle", [])},
        "finali_esclusi": tuple(x.lower() for x in es.get("finali", [])),
        "dentro_escluse": tuple((a.lower(), b.lower()) for a, b in es.get("dentro", [])),
        "tipi": {x.lower().lstrip(".") for x in f["tipi_processati"]},
    }


def firme_in_coda(c=None):
    return tuple((c or carica())["fonti"].get("firme_in_coda", []))


# --- Permessi e strumenti dei connettori ------------------------------------------------------

def _strumenti(d, parte=None):
    """Strumenti di un connettore: tutti i gruppi, un gruppo, o uno strumento singolo."""
    gruppi = {k: v for k, v in d.items() if k != "server"}
    if parte is None:
        return [t for g in gruppi.values() for t in g]
    return list(gruppi[parte]) if parte in gruppi else [parte]


def _nomi(d, strumenti):
    out = []
    for srv in d["server"]:
        out += [f"mcp__{srv}__{t}" for t in strumenti if f"mcp__{srv}__{t}" not in out]
    return out


def permessi_attesi(c=None):
    """Nomi `mcp__<server>__<strumento>` dei permessi di settings.json, nell'ordine di vault.yaml."""
    out = []
    for d in (c or carica())["connettori"].values():
        out += [n for n in _nomi(d, _strumenti(d)) if n not in out]
    return out


def tools_attesi(agente, c=None):
    """Nomi mcp della riga `tools:` dell'agente (lista vuota se l'agente non è in `agenti`)."""
    c = c or carica()
    out = []
    for voce in (c.get("agenti") or {}).get(agente, []):
        nome, _, parte = voce.partition(".")
        d = c["connettori"][nome]
        out += [n for n in _nomi(d, _strumenti(d, parte)) if n not in out]
    return out


def server_noti(c=None):
    return {s for d in (c or carica())["connettori"].values() for s in d["server"]}


def _mcp(nomi):
    return [n.strip() for n in nomi if n.strip().startswith("mcp__")]


def _riga_tools(testo):
    """(indice di inizio, indice di fine, valori) della riga `tools:` nel frontmatter, o None."""
    if not testo.startswith("---\n"):
        return None
    fine_fm = testo.find("\n---", 4)
    m = re.compile(r"^tools:[ \t]*(.*)$", re.M).search(testo, 4, fine_fm if fine_fm != -1 else len(testo))
    if not m:
        return None
    return m.start(), m.end(), [t.strip() for t in m.group(1).split(",") if t.strip()]


def problemi_permessi(root=None, c=None):
    """[(file, messaggio)]: permessi e `tools` mcp che non coincidono con vault.yaml."""
    root = Path(root or ROOT)
    c = c or carica(root)
    out = []

    def confronta(dove, trovati, attesi):
        trovati, attesi = set(_mcp(trovati)), set(attesi)
        for n in sorted(attesi - trovati):
            out.append((dove, f"manca `{n}` (vault.yaml; `config.py applica` lo aggiunge)"))
        for n in sorted(trovati - attesi):
            srv = n.split("__")[1] if n.count("__") >= 2 else n
            perche = "server" if srv not in server_noti(c) else "strumento"
            out.append((dove, f"`{n}`: {perche} non previsto in vault.yaml (`config.py applica` lo toglie)"))

    try:
        allow = json.loads((root / SETTINGS).read_text(encoding="utf-8")).get("permissions", {}).get("allow", [])
    except (OSError, json.JSONDecodeError) as ex:
        out.append((SETTINGS, f"illeggibile ({ex})"))
    else:
        confronta(SETTINGS, allow, permessi_attesi(c))

    cartella = root / AGENTI
    file_agenti = {p.stem: p for p in sorted(cartella.glob("*.md"))} if cartella.is_dir() else {}
    for agente in (c.get("agenti") or {}):
        if agente not in file_agenti:
            out.append((f"{AGENTI}/{agente}.md", f"agente `{agente}` in vault.yaml ma il file non c'è"))
    for agente, p in file_agenti.items():
        dove = f"{AGENTI}/{p.name}"
        riga = _riga_tools(p.read_text(encoding="utf-8"))
        confronta(dove, riga[2] if riga else [], tools_attesi(agente, c))
    return out


def applica(root=None, c=None):
    """Riscrive i permessi mcp di settings.json e le righe `tools:` degli agenti. File cambiati."""
    root = Path(root or ROOT)
    c = c or carica(root)
    cambiati = []

    p = root / SETTINGS
    testo = p.read_text(encoding="utf-8")
    dati = json.loads(testo)
    allow = dati.setdefault("permissions", {}).setdefault("allow", [])
    primo = next((i for i, n in enumerate(allow) if n.startswith("mcp__")), 0)
    resto = [n for n in allow if not n.startswith("mcp__")]
    nuovo = resto[:primo] + permessi_attesi(c) + resto[primo:]
    if nuovo != allow:
        dati["permissions"]["allow"] = nuovo
        p.write_text(json.dumps(dati, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cambiati.append(SETTINGS)

    cartella = root / AGENTI
    for p in sorted(cartella.glob("*.md")) if cartella.is_dir() else []:
        testo = p.read_text(encoding="utf-8")
        riga = _riga_tools(testo)
        attesi = tools_attesi(p.stem, c)
        if riga is None:
            if attesi:
                raise ConfigErrata([f"{AGENTI}/{p.name}: manca la riga `tools:` nel frontmatter"])
            continue
        inizio, fine, valori = riga
        nuovi = [t for t in valori if not t.startswith("mcp__")] + attesi
        if nuovi != valori:
            p.write_text(testo[:inizio] + "tools: " + ", ".join(nuovi) + testo[fine:], encoding="utf-8")
            cambiati.append(f"{AGENTI}/{p.name}")
    return cambiati


# --- Coerenza con SPEC 7 ----------------------------------------------------------------------

def giorni_da_testo(testo):
    """Giorni dalla colonna "Quando" di SPEC 7 ("Ogni giorno alle…", "Domenica alle…",
    "Dal lunedì al venerdì alle…"). Insieme vuoto se non ne trova."""
    t = testo.lower()
    if "ogni giorno" in t:
        return TUTTI
    m = re.search(r"dal (\w+) al (\w+)", t)
    if m and m.group(1) in NOMI_GIORNI and m.group(2) in NOMI_GIORNI:
        return giorni(f"{m.group(1)}-{m.group(2)}")
    interi = {g: n for n, g in enumerate(GIORNI)} | {g.replace("ì", "i"): n for n, g in enumerate(GIORNI)}
    return frozenset(interi[w] for w in re.findall(r"\w+", t) if w in interi)


def task_della_spec(testo):
    """{task: (giorni, orari)} dalla tabella sotto `## 7. Task schedulati` di SPEC.md.

    ValueError se la sezione o la colonna "Quando" mancano."""
    inizio = testo.find(SPEC_TITOLO_TASK)
    if inizio == -1:
        raise ValueError(f"manca la sezione `{SPEC_TITOLO_TASK}`")
    fine = testo.find("\n## ", inizio + len(SPEC_TITOLO_TASK))
    righe = testo[inizio:fine if fine != -1 else len(testo)].splitlines()
    out, quando = {}, None
    for riga in righe:
        if not riga.strip().startswith("|"):
            continue
        celle = [x.strip() for x in riga.strip().strip("|").split("|")]
        if quando is None:
            if "Quando" in celle:
                quando = celle.index("Quando")
            continue
        m = re.fullmatch(r"`([^`]+)`", celle[0])
        if not m or len(celle) <= quando:
            continue
        out[m.group(1)] = (giorni_da_testo(celle[quando]), tuple(sorted(ORA_NEL_TESTO_RE.findall(celle[quando]))))
    if quando is None:
        raise ValueError(f"nella tabella di `{SPEC_TITOLO_TASK}` manca la colonna \"Quando\"")
    return out


def problemi_spec(root=None, c=None):
    """Messaggi sulle differenze tra la tabella dei task di SPEC 7 e `task` di vault.yaml.

    Lista vuota se SPEC.md non c'è (un vault senza SPEC non ha niente da confrontare)."""
    root = Path(root or ROOT)
    c = c or carica(root)
    try:
        testo = (root / SPEC).read_text(encoding="utf-8")
    except FileNotFoundError:
        return []
    try:
        spec = task_della_spec(testo)
    except ValueError as ex:
        return [f"SPEC 7: {ex}"]
    conf = {t["nome"]: (giorni(t["giorni"]), tuple(sorted(t["orari"]))) for t in c["task"]}
    out = []
    for nome in sorted(set(spec) | set(conf)):
        if nome not in conf:
            out.append(f"task `{nome}` in SPEC 7 ma non in vault.yaml")
        elif nome not in spec:
            out.append(f"task `{nome}` in vault.yaml ma non in SPEC 7")
        else:
            (gs, os_), (gc, oc) = spec[nome], conf[nome]
            if not gs:
                out.append(f"task `{nome}`: in SPEC 7 i giorni non si riconoscono")
            elif gs != gc:
                out.append(f"task `{nome}`: giorni diversi (SPEC 7 {descrivi_giorni(gs)}, "
                           f"vault.yaml {descrivi_giorni(gc)})")
            if os_ != oc:
                out.append(f"task `{nome}`: orari diversi (SPEC 7 {', '.join(os_) or 'nessuno'}, "
                           f"vault.yaml {', '.join(oc)})")
    return out


def verifica(root=None):
    """[(file, messaggio)] di tutti i problemi: schema, SPEC 7, permessi."""
    root = Path(root or ROOT)
    try:
        c = carica(root)
    except ConfigErrata as ex:
        return [(FILE, m) for m in ex.errori]
    return [(SPEC, m) for m in problemi_spec(root, c)] + problemi_permessi(root, c)


# --- Riga di comando ----------------------------------------------------------------------------

def stampa(v):
    if isinstance(v, list) and all(not isinstance(x, (dict, list)) for x in v):
        print("\n".join(str(x) for x in v))
    elif isinstance(v, (dict, list)):
        print(json.dumps(v, ensure_ascii=False, indent=2, default=str))
    elif isinstance(v, bool):
        print("true" if v else "false")
    else:
        print("" if v is None else v)


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if argv else 2
    cmd, args = argv[0], argv[1:]
    try:
        if cmd == "verifica" and not args:
            problemi = verifica()
            for dove, msg in problemi:
                print(f"- `{dove}` · {msg}")
            print(f"{len(problemi)} errori" if problemi else "vault.yaml valido, coerente con SPEC 7 e con i permessi")
            return 1 if problemi else 0
        c = carica()
        if cmd == "oggi" and not args:
            print(oggi(c).isoformat())
        elif cmd == "ora" and not args:
            print(adesso(c).strftime("%H:%M"))
        elif cmd == "valore" and len(args) == 1:
            try:
                stampa(valore(args[0], c))
            except KeyError:
                print(f"Chiave non trovata in {FILE}: {args[0]}", file=sys.stderr)
                return 1
        elif cmd == "task":
            come_json, solo_digest = "--json" in args, "--digest" in args
            resto = [a for a in args if a not in ("--json", "--digest")]
            if len(resto) > 1:
                raise ValueError("al massimo una data")
            try:
                giorno = dt.date.fromisoformat(resto[0]) if resto else oggi(c)
            except ValueError:
                raise ValueError(f"data non valida: {resto[0]} (serve AAAA-MM-GG)")
            righe = task_del_giorno(giorno, c, solo_digest)
            if come_json:
                print(json.dumps([{"ora": o, "task": t} for o, t in righe], ensure_ascii=False))
            else:
                for o, t in righe:
                    print(f"{o} {t}")
        elif cmd == "applica" and not args:
            cambiati = applica(c=c)
            print("Aggiornati: " + ", ".join(cambiati) if cambiati else "Niente da cambiare")
        else:
            raise ValueError(f"comando non valido: {' '.join(argv)} (vedi --help)")
    except ConfigErrata as ex:
        print("Configurazione non valida:\n" + "\n".join(f"- {m}" for m in ex.errori), file=sys.stderr)
        return 1
    except ValueError as ex:
        print(f"Errore: {ex}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
