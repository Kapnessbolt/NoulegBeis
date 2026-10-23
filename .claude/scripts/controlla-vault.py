#!/usr/bin/env python3
"""Controllo del vault (SPEC 4.4): integrità dei collegamenti, tracciabilità, schema, doppioni.

Uso:
  python3 .claude/scripts/controlla-vault.py              # rapporto in markdown
  python3 .claude/scripts/controlla-vault.py --indice     # rapporto + indice per categoria
  python3 .claude/scripts/controlla-vault.py --modificati # solo gli errori che toccano file
                                                          # modificati rispetto a HEAD (hook di commit)

Esce con codice 1 se trova errori. Richiede PyYAML.
"""

import datetime as dt
import difflib
import json
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

ROOT = Path(__file__).resolve().parents[2]

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
# Sezioni in cui ogni punto deve citare la fonte (SPEC 4.1, tracciabilità)
TRACED_SECTIONS = {
    "topic": ("Punti chiave",),
    "client": ("Chi sono", "Relazione con BlueAge"),
    "project": ("Stato", "Decisioni"),
}
# Note che devono avere almeno un collegamento in entrata
NEED_INBOUND = {"client", "person", "topic"}
STUB_TAG = "da-verificare"

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
WIKILINK_RE = re.compile(r"\[\[([^\]|#^]+)(?:[#^][^\]|]*)?(?:\|[^\]]*)?\]\]")
ENUM_RE = re.compile(r"#\s*([a-z-]+(?:\s*\|\s*[a-z-]+)+)\s*$")
SIMILAR = 0.85

errori, avvisi = [], []


def err(paths, msg, target=None):
    """paths: nota o note coinvolte; target: slug citato (per i link rotti)."""
    paths = [str(p) for p in (paths if isinstance(paths, (list, tuple)) else [paths])]
    errori.append({"paths": paths, "msg": msg, "target": target})


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


def main():
    indice = "--indice" in sys.argv
    solo_modificati = "--modificati" in sys.argv
    templates = load_templates()
    by_slug = defaultdict(list)
    parsed = {}

    # 1. Lettura, frontmatter, tipo, slug
    for rel, p in notes():
        by_slug[p.stem].append(rel)
        if not SLUG_RE.match(p.stem):
            err(rel, "nome file non in slug (minuscolo, trattini, senza accenti)")
        text = p.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
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
        for name in TRACED_SECTIONS.get(tipo, ()):
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

    # 6. Stato dell'ingestion
    state_path = ROOT / ".state" / "ingest.json"
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        err(".state/ingest.json", f"illeggibile ({e})")
        state = {}
    tracked = set()
    for fonte, coll in (("sharepoint", "items"), ("onedrive", "items"), ("outlook", "threads")):
        for key, v in (state.get(fonte) or {}).get(coll, {}).items():
            note = v.get("note", "")
            tracked.add(note)
            if not (ROOT / note).is_file():
                err([".state/ingest.json", note], f"{fonte} `{key}` punta a una nota inesistente: `{note}`")
    for rel, (d, _) in parsed.items():
        if rel.parts[0] != "sources" or d.get("type") != "source-doc":
            continue
        if d.get("source") in ("sharepoint", "onedrive") and "fuori-perimetro" not in as_list(d.get("tags")):
            if str(rel) not in tracked:
                avv(rel, "documento non registrato in .state/ingest.json")

    # Solo gli errori che dipendono dalle modifiche in corso (hook di commit)
    if solo_modificati:
        changed = changed_files()
        changed_stems = {Path(c).stem for c in changed}
        mostrati = [e for e in errori
                    if set(e["paths"]) & changed or (e["target"] and e["target"] in changed_stems)]
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
