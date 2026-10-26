"""Frontmatter delle note: schema dal template, validazione, lettura e scrittura nello stile del
vault (SPEC 4.2). Modulo condiviso da `nuova-nota.py` e `aggiorna-nota.py`: non è un comando.

Stile del frontmatter scritto (quello delle note reali):
- scalari semplici senza virgolette, tra virgolette doppie solo se servono (o se il valore
  originale le aveva, o per `conversation_id` e `subject`); istanti `2026-10-01T17:20:46Z`;
- liste inline tra quadre, con i wikilink tra virgolette: `projects: ["[[manini]]"]`;
- `versions` e `also_at` come lista di mappe inline: `  - { name: ..., item_id: ..., last_modified: ... }`;
- `current` come mappa a blocchi con due spazi di rientro.
Nell'aggiornamento le righe dei campi che non cambiano restano identiche, byte per byte.

La validazione segue `controlla-vault.py`: chiavi mancanti o sconosciute rispetto al template,
`current` completo, valori degli elenchi ammessi (commenti `# a | b | c` del template), più il
formato degli istanti e dei wikilink.
"""

import datetime as dt
import json
import os
import re
import tempfile
from pathlib import Path

import yaml

ROOT = Path(os.environ.get("VAULT_ROOT") or Path(__file__).resolve().parents[2]).resolve()

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
SOURCE_BY_DIR = {"sharepoint": "sharepoint", "onedrive": "onedrive", "attachments": "attachment", "github": "github"}
ISTANTI = {"ingested_at", "first_message", "last_message", "current.last_modified"}
LISTE_WIKILINK = {"participants", "attachments", "projects", "clients", "topics", "people"}
SEMPRE_TRA_VIRGOLETTE = {"conversation_id", "subject", "role", "sector", "email", "org", "outcome"}
LISTE_DI_MAPPE = {"versions": ("name", "item_id", "last_modified"), "also_at": ("web_url", "item_id")}

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
CHIAVE_RE = re.compile(r"^([A-Za-z_][\w-]*):(.*)$")
SOTTOCHIAVE_RE = re.compile(r"^  ([A-Za-z_][\w-]*):(.*)$")
ENUM_RE = re.compile(r"#\s*([a-z-]+(?:\s*\|\s*[a-z-]+)+)\s*$")
ISTANTE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
WIKILINK_RE = re.compile(r"^\[\[([^\[\]|#]+)\]\]$")
WIKILINK_NUDO_RE = re.compile(r'(?<!")\[\[([^\[\]"]+)\]\](?!")')


class Errore(Exception):
    pass


# --- Testo della nota -------------------------------------------------------------------

def dividi(testo):
    """(frontmatter, resto) con testo == "---\\n" + frontmatter + "\\n---" + resto."""
    if not testo.startswith("---\n"):
        raise Errore("frontmatter mancante")
    fine = testo.find("\n---", 4)
    if fine == -1:
        raise Errore("frontmatter non chiuso")
    return testo[4:fine], testo[fine + 4:]


def unisci(fm, resto):
    return "---\n" + fm + "\n---" + resto


def blocchi(fm):
    """[[chiave, [righe]]]: ogni chiave di primo livello con le sue righe di continuazione."""
    out = []
    for riga in fm.split("\n"):
        m = CHIAVE_RE.match(riga)
        if m:
            out.append([m.group(1), [riga]])
        elif out:
            out[-1][1].append(riga)
        else:
            out.append([None, [riga]])
    return out


def _umask():
    attuale = os.umask(0)
    os.umask(attuale)
    return attuale


def scrivi_atomico(p, testo):
    p = Path(p)
    fd, tmp = tempfile.mkstemp(prefix=f".{p.name}.", suffix=".tmp", dir=p.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(testo)
        os.chmod(tmp, p.stat().st_mode & 0o777 if p.exists() else 0o666 & ~_umask())
        os.replace(tmp, p)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


# --- Schema dal template ----------------------------------------------------------------

def schema(tipo):
    """Chiavi in ordine, valori di default, enum e chiavi di `current` del template del tipo."""
    if tipo not in TEMPLATE_BY_TYPE:
        raise Errore(f"tipo sconosciuto `{tipo}` (ammessi: {', '.join(TEMPLATE_BY_TYPE)})")
    p = ROOT / "_templates" / f"{TEMPLATE_BY_TYPE[tipo]}.md"
    raw = p.read_text(encoding="utf-8")
    fm, corpo = dividi(raw.replace("{{date:YYYY-MM-DD}}", "2000-01-01").replace("{{title}}", "TITOLO"))
    default = yaml.safe_load(fm) or {}
    ordine, enums = [], {}
    for riga in fm.split("\n"):
        m = CHIAVE_RE.match(riga)
        if not m:
            continue
        ordine.append(m.group(1))
        e = ENUM_RE.search(riga)
        if e and m.group(1) in default:
            enums[m.group(1)] = [v.strip() for v in e.group(1).split("|")]
    current = list((default.get("current") or {}).keys())
    return {"tipo": tipo, "template": raw, "ordine": ordine, "default": default,
            "enums": enums, "current": current}


# --- Valori -----------------------------------------------------------------------------

def a_istante(v, nome):
    """datetime UTC da un istante ISO (stringa o datetime); None resta None."""
    if v is None or v == "":
        return None
    if isinstance(v, dt.datetime):
        if v.tzinfo is not None:
            v = v.astimezone(dt.timezone.utc).replace(tzinfo=None)
        return v.replace(tzinfo=dt.timezone.utc)
    if isinstance(v, str) and ISTANTE_RE.match(v):
        return dt.datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    raise Errore(f"{nome}: `{v}` non è un istante AAAA-MM-GGTHH:MM:SSZ (UTC)")


def adesso():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def normale(v):
    """Forma confrontabile di un valore (date e istanti come stringhe)."""
    if isinstance(v, dt.datetime):
        if v.tzinfo is not None:
            v = v.astimezone(dt.timezone.utc).replace(tzinfo=None)
        return v.strftime("%Y-%m-%dT%H:%M:%SZ")
    if isinstance(v, dt.date):
        return v.isoformat()
    if isinstance(v, dict):
        return {k: normale(x) for k, x in v.items()}
    if isinstance(v, list):
        return [normale(x) for x in v]
    return v


def interpreta(raw, chiave, default):
    """Valore YAML di `--campo chiave=raw`, ricondotto al tipo del template."""
    testo = WIKILINK_NUDO_RE.sub(r'"[[\1]]"', raw)
    try:
        v = yaml.safe_load(testo) if testo.strip() else None
    except yaml.YAMLError as e:
        raise Errore(f"{chiave}: valore `{raw}` non è YAML valido ({str(e).splitlines()[0]})")
    if chiave in ISTANTI or chiave.endswith(".last_modified"):
        return a_istante(v, chiave)
    if isinstance(default, list):
        if v is None:
            return []
        return v if isinstance(v, list) else [v]
    if isinstance(default, str):
        if v is None:
            return ""
        if not isinstance(v, str):
            return raw.strip()  # `item_id=0123` resta una stringa
        return v
    if isinstance(default, bool):
        if not isinstance(v, bool):
            raise Errore(f"{chiave}: `{raw}` non è true o false")
        return v
    if isinstance(default, int):
        if not isinstance(v, int) or isinstance(v, bool):
            raise Errore(f"{chiave}: `{raw}` non è un numero intero")
        return v
    if isinstance(default, dt.date):
        if isinstance(v, str):
            try:
                v = dt.date.fromisoformat(v)
            except ValueError:
                raise Errore(f"{chiave}: `{raw}` non è una data AAAA-MM-GG")
        if not isinstance(v, dt.date) or isinstance(v, dt.datetime):
            raise Errore(f"{chiave}: `{raw}` non è una data AAAA-MM-GG")
        return v
    return v


def campo(arg):
    """`chiave=valore` → (chiave, valore grezzo)."""
    if "=" not in arg:
        raise Errore(f"`{arg}` non è nella forma chiave=valore")
    k, v = arg.split("=", 1)
    k = k.strip()
    if not k:
        raise Errore(f"`{arg}`: chiave vuota")
    return k, v


def imposta(data, sch, chiave, raw):
    """Imposta `chiave` (anche `current.<sotto>`) dal valore grezzo, validando la chiave."""
    if "." in chiave:
        padre, figlio = chiave.split(".", 1)
        if padre != "current" or "current" not in sch["default"]:
            raise Errore(f"chiave `{chiave}` non prevista dal template {sch['tipo']}")
        if figlio not in sch["current"]:
            raise Errore(f"`current.{figlio}` non previsto (ammessi: {', '.join(sch['current'])})")
        cur = data.get("current")
        if not isinstance(cur, dict):
            cur = {}
        cur[figlio] = interpreta(raw, chiave, sch["default"]["current"][figlio])
        data["current"] = cur
        return
    if chiave not in sch["default"]:
        raise Errore(f"chiave `{chiave}` non prevista dal template {sch['tipo']}")
    data[chiave] = interpreta(raw, chiave, sch["default"][chiave])


# --- Resa in YAML -----------------------------------------------------------------------

def _semplice_ok(s, flow):
    if s == "" or s != s.strip() or "\n" in s or "\t" in s:
        return False
    if s[0] in "?:,[]{}#&*!|>'\"%@`" or s.startswith("- ") or s == "-":
        return False
    if ": " in s or " #" in s or s.endswith(":"):
        return False
    if flow and (" " in s or any(c in s for c in ",[]{}")):
        return False
    try:
        return yaml.safe_load(s) == s
    except yaml.YAMLError:
        return False


def scalare(v, flow=False, virgolette=False):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, (dt.datetime, dt.date)):
        return normale(v)
    s = str(v)
    if virgolette or not _semplice_ok(s, flow):
        return json.dumps(s, ensure_ascii=False)
    return s


def _tra_virgolette(riga):
    """True se il valore della riga `chiave: valore` era tra virgolette."""
    valore = riga.split(":", 1)[1].strip() if ":" in riga else ""
    return valore.startswith('"') or valore.startswith("'")


def rendi(chiave, v, righe_orig=None, orig=None):
    """Righe YAML del campo; con le righe originali conserva quelle che non cambiano."""
    if isinstance(v, dict):
        vecchie = {}
        if righe_orig and isinstance(orig, dict):
            for r in righe_orig[1:]:
                m = SOTTOCHIAVE_RE.match(r)
                if m:
                    vecchie[m.group(1)] = r
        out = [f"{chiave}:"]
        for k, x in v.items():
            r = vecchie.get(k)
            if r is not None and k in orig and normale(orig[k]) == normale(x):
                out.append(r)
            else:
                out.append(f"  {k}: {scalare(x, virgolette=r is not None and _tra_virgolette(r))}")
        return out
    if isinstance(v, list):
        if not v:
            return [f"{chiave}: []"]
        if any(isinstance(x, dict) for x in v):
            out = [f"{chiave}:"]
            for x in v:
                if not isinstance(x, dict):
                    raise Errore(f"{chiave}: lista con mappe e valori semplici insieme")
                coppie = ", ".join(f"{k}: {scalare(y, flow=True)}" for k, y in x.items())
                out.append(f"  - {{ {coppie} }}")
            return out
        voci = ", ".join(scalare(x, flow=True, virgolette=isinstance(x, str) and x.startswith("[["))
                         for x in v)
        return [f"{chiave}: [{voci}]"]
    virg = chiave in SEMPRE_TRA_VIRGOLETTE or bool(righe_orig and _tra_virgolette(righe_orig[0]))
    if isinstance(v, str) and v.startswith("[["):
        virg = True
    return [f"{chiave}: {scalare(v, virgolette=virg and isinstance(v, str))}"]


def rendi_frontmatter(data, ordine):
    """Frontmatter completo da zero, nell'ordine del template (note nuove)."""
    chiavi = [k for k in ordine if k in data] + [k for k in data if k not in ordine]
    righe = []
    for k in chiavi:
        righe += rendi(k, data[k])
    return "\n".join(righe)


def riscrivi_frontmatter(fm, vecchio, nuovo):
    """Frontmatter aggiornato: i blocchi dei campi invariati restano come erano."""
    righe = []
    visti = set()
    for chiave, linee in blocchi(fm):
        if chiave is None:
            righe += linee
            continue
        visti.add(chiave)
        if chiave not in nuovo:
            continue
        if chiave in vecchio and normale(vecchio[chiave]) == normale(nuovo[chiave]):
            righe += linee
        else:
            righe += rendi(chiave, nuovo[chiave], linee, vecchio.get(chiave))
    for chiave in nuovo:
        if chiave not in visti:
            righe += rendi(chiave, nuovo[chiave])
    return "\n".join(righe)


# --- Validazione ------------------------------------------------------------------------

def slug_esistenti():
    out = {}
    salta = {".git", ".github", ".claude", "_templates", ".obsidian", ".trash"}
    for p in ROOT.rglob("*.md"):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in salta or rel.parts[:2] == ("sessions", "_raw"):
            continue
        out.setdefault(p.stem, []).append(rel)
    return out


def valida(data, sch, extra_ammesse=()):
    """(errori, avvisi) del frontmatter rispetto al template del tipo."""
    errori, avvisi = [], []
    chiavi = set(sch["default"])
    mancanti = chiavi - set(data)
    extra = set(data) - chiavi
    if mancanti:
        errori.append(f"campi mancanti: {', '.join(sorted(mancanti))}")
    for k in sorted(extra):
        (avvisi if k in extra_ammesse else errori).append(f"campo non previsto dal template: {k}")
    if data.get("type") != sch["tipo"]:
        errori.append(f"type {data.get('type')!r} diverso da {sch['tipo']!r}")
    for k, valori in sch["enums"].items():
        if k in data and data[k] not in valori:
            errori.append(f"{k}: {data[k]!r} non è tra {' | '.join(valori)}")
    if sch["current"]:
        cur = data.get("current")
        if not isinstance(cur, dict):
            errori.append("`current` deve essere una mappa")
        else:
            manca = [k for k in sch["current"] if k not in cur]
            troppo = [k for k in cur if k not in sch["current"]]
            if manca:
                errori.append(f"`current` incompleto: manca {', '.join(manca)}")
            if troppo:
                errori.append(f"`current`: campi non previsti {', '.join(troppo)}")
    for nome in ISTANTI:
        if nome.startswith("current."):
            v = (data.get("current") or {}).get(nome.split(".", 1)[1]) if isinstance(data.get("current"), dict) else None
        else:
            v = data.get(nome)
        if isinstance(v, str) and v and not ISTANTE_RE.match(v):
            errori.append(f"{nome}: `{v}` non è un istante AAAA-MM-GGTHH:MM:SSZ")
    for k, campi in LISTE_DI_MAPPE.items():
        if k not in data:
            continue
        if not isinstance(data[k], list):
            errori.append(f"{k} deve essere una lista")
            continue
        for x in data[k]:
            if not isinstance(x, dict) or set(x) - set(campi):
                errori.append(f"{k}: ogni voce è una mappa con {', '.join(campi)}")
                break
    esistenti = None
    for k in LISTE_WIKILINK:
        if k not in data:
            continue
        v = data[k]
        if not isinstance(v, list):
            errori.append(f"{k} deve essere una lista")
            continue
        for x in v:
            m = WIKILINK_RE.match(str(x)) if isinstance(x, str) else None
            if not m:
                errori.append(f"{k}: `{x}` non è un wikilink [[slug]]")
                continue
            if esistenti is None:
                esistenti = slug_esistenti()
            if m.group(1) not in esistenti:
                avvisi.append(f"{k}: [[{m.group(1)}]] non esiste ancora: creala prima del commit")
    if sch["tipo"] in ("source-doc", "source-mail"):
        if not any(data.get(k) for k in ("projects", "clients", "topics")):
            errori.append("fonte senza progetto, cliente o tema (projects, clients, topics)")
    return errori, avvisi
