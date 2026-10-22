#!/usr/bin/env python3
"""Rinomina una nota e aggiorna tutti i wikilink che la citano (SPEC 4.4).

Uso: python3 .claude/scripts/rinomina-nota.py <slug-vecchio> <slug-nuovo>

Per una scheda progetto rinomina cartella, scheda e log. Aggiorna anche .state/ingest.json.
Per unire due doppioni: sposta a mano il contenuto nella nota che resta, cancella l'altra
e lancia questo script con lo slug cancellato come vecchio: i link passano alla nota che resta.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".git", ".github", ".claude", "_templates", ".obsidian", ".trash"}
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def vault_notes():
    for p in ROOT.rglob("*.md"):
        rel = p.relative_to(ROOT)
        if rel.parts[0] not in SKIP_DIRS and rel.parts[:2] != ("sessions", "_raw"):
            yield p


def git_mv(src, dst):
    """Rinomina anche file non ancora tracciati; git riconosce lo spostamento con `add`."""
    src.rename(dst)
    subprocess.run(["git", "add", "-A", "--", str(src), str(dst)], cwd=ROOT, check=False,
                   capture_output=True)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    old, new = sys.argv[1], sys.argv[2]
    if not SLUG_RE.match(new):
        sys.exit(f"`{new}` non è uno slug valido")
    notes = list(vault_notes())
    if any(p.stem == new for p in notes):
        sys.exit(f"Esiste già una nota `{new}`")
    found = [p for p in notes if p.stem == old]
    if len(found) > 1:
        sys.exit(f"Slug `{old}` duplicato: " + ", ".join(str(p.relative_to(ROOT)) for p in found))

    renames = {old: new}
    moved = {}
    if found:
        src = found[0]
        if src.parent.name == old and src.parent.parent.name == "projects":
            folder = src.parent.parent / new
            git_mv(src.parent, folder)
            git_mv(folder / f"{old}.md", folder / f"{new}.md")
            moved[src] = folder / f"{new}.md"
            log = folder / f"{old}-log.md"
            if log.exists():
                git_mv(log, folder / f"{new}-log.md")
                renames[f"{old}-log"] = f"{new}-log"
        else:
            git_mv(src, src.with_name(f"{new}.md"))
            moved[src] = src.with_name(f"{new}.md")

    # Wikilink: [[vecchio]], [[vecchio|testo]], [[vecchio#sezione]]
    patterns = {o: re.compile(r"\[\[" + re.escape(o) + r"(?=[\]|#^])") for o in renames}
    changed = 0
    for p in vault_notes():
        text = p.read_text(encoding="utf-8")
        new_text = text
        for o, pat in patterns.items():
            new_text = pat.sub("[[" + renames[o], new_text)
        if new_text != text:
            p.write_text(new_text, encoding="utf-8")
            changed += 1

    state_path = ROOT / ".state" / "ingest.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    for src, dst in moved.items():
        old_rel, new_rel = str(src.relative_to(ROOT)), str(dst.relative_to(ROOT))
        for fonte in state.values():
            for coll in ("items", "threads"):
                for v in (fonte.get(coll) or {}).values():
                    if v.get("note") == old_rel:
                        v["note"] = new_rel
    state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"[[{old}]] → [[{new}]]: {'nota rinominata, ' if found else ''}{changed} note aggiornate")


if __name__ == "__main__":
    main()
