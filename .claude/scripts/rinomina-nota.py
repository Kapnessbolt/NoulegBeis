#!/usr/bin/env python3
"""Rinomina una nota e aggiorna tutti i wikilink che la citano (SPEC 4.4).

Uso: python3 .claude/scripts/rinomina-nota.py <slug-vecchio> <slug-nuovo>

Per una scheda progetto rinomina cartella, scheda e log. Aggiorna anche le voci dello stato
(`.state/<fonte>.json`, con `stato.py`) che puntano alla nota spostata.
Per unire due doppioni: sposta a mano il contenuto nella nota che resta, cancella l'altra
e lancia questo script con lo slug cancellato come vecchio: i link passano alla nota che resta.

La variabile d'ambiente VAULT_ROOT, se presente, indica la radice del vault al posto della
cartella che contiene `.claude/` (serve ai test in `.claude/scripts/tests/`).
"""

import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import stato  # noqa: E402

ROOT = Path(os.environ.get("VAULT_ROOT") or Path(__file__).resolve().parents[2]).resolve()
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

    stato_aggiornato = 0
    if moved:
        spostate = {str(src.relative_to(ROOT)): str(dst.relative_to(ROOT)) for src, dst in moved.items()}
        for fonte, coll in stato.COLLEZIONE.items():
            if not stato.percorso(fonte).exists():
                continue
            data = stato.leggi(fonte)
            cambiato = False
            for v in data[coll].values():
                if v.get("note") in spostate:
                    v["note"] = spostate[v["note"]]
                    cambiato = True
            if cambiato:
                stato.scrivi(fonte, data)
                stato_aggiornato += 1

    extra = f", {stato_aggiornato} file di stato aggiornati" if stato_aggiornato else ""
    print(f"[[{old}]] → [[{new}]]: {'nota rinominata, ' if found else ''}{changed} note aggiornate{extra}")


if __name__ == "__main__":
    main()
