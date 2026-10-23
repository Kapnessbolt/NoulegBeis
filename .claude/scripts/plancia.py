#!/usr/bin/env python3
"""Dati della plancia: progetti e attività del vault in due file JSON.

Uso:
  python3 .claude/scripts/plancia.py <cartella_output>

Scrive <cartella_output>/progetti.json e <cartella_output>/attivita.json, righe
pronte per la dashboard (artifact "Cockpit"). I file non vanno nel repo:
la cartella di output sta fuori dal vault. Richiede PyYAML.
"""

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Manca PyYAML: pip install pyyaml")

ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".git", ".github", ".claude", "_templates", ".obsidian", ".trash"}

LINK = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
TASK = re.compile(r"^- \[( |x|X)\] (.+)$")
DUE = re.compile(r"📅\s*(\d{4}-\d{2}-\d{2})")
SOURCE = re.compile(r"\s*\(((?:\[\[[^\]]+\]\](?:,\s*)?)+)\)\s*$")


def split_note(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    _, fm, body = text.split("---", 2)
    return yaml.safe_load(fm) or {}, body


def h1(body):
    m = re.search(r"^# (.+)$", body, re.M)
    return m.group(1).strip() if m else None


def titles():
    """slug → titolo H1 di ogni nota del vault, per rendere leggibili i wikilink."""
    out = {}
    for p in ROOT.rglob("*.md"):
        if SKIP_DIRS & set(p.relative_to(ROOT).parts):
            continue
        try:
            out[p.stem] = h1(split_note(p)[1]) or p.stem.replace("-", " ")
        except Exception:
            out[p.stem] = p.stem.replace("-", " ")
    return out


def section(body, name):
    m = re.search(rf"^## {re.escape(name)}\s*$(.*?)(?=^## |\Z)", body, re.M | re.S)
    return m.group(1) if m else ""


def slugs(value):
    return [LINK.search(v).group(1) for v in (value or []) if LINK.search(str(v))]


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    out_dir = Path(sys.argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)
    names = titles()
    plain = lambda s: LINK.sub(lambda m: names.get(m.group(1), m.group(1)), s)

    progetti, attivita = [], []
    for path in sorted((ROOT / "projects").glob("*/*.md")):
        slug = path.stem
        if slug != path.parent.name:
            continue
        fm, body = split_note(path)
        nome = h1(body) or slug
        ruolo = fm.get("role") or ""
        progetti.append({
            "progetto": slug,
            "nome": nome,
            "clienti": ", ".join(names.get(s, s) for s in slugs(fm.get("clients"))),
            "ruolo": ruolo,
            "coinvolto": not ruolo.lower().startswith("non coinvolto"),
            "stato": fm.get("status") or "",
            "aggiornato": str(fm.get("updated") or ""),
        })
        n = 0
        for line in section(body, "Attività").splitlines():
            m = TASK.match(line.strip())
            if not m:
                continue
            n += 1
            testo = m.group(2)
            fonte = SOURCE.search(testo)
            testo = SOURCE.sub("", testo)
            due = DUE.search(testo)
            testo = DUE.sub("", testo).strip()
            attivita.append({
                "id": f"{slug}-{n}",
                "progetto": slug,
                "nome_progetto": nome,
                "testo": plain(testo),
                "scadenza": due.group(1) if due else "",
                "fatta": m.group(1).lower() == "x",
                "fonte": LINK.findall(fonte.group(1))[0] if fonte else "",
            })

    for name, rows in (("progetti", progetti), ("attivita", attivita)):
        (out_dir / f"{name}.json").write_text(
            json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(progetti)} progetti, {len(attivita)} attività → {out_dir}")


if __name__ == "__main__":
    main()
