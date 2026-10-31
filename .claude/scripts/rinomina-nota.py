#!/usr/bin/env python3
"""Rinomina una nota e aggiorna tutti i wikilink che la citano (SPEC 4.4).

Uso: python3 .claude/scripts/rinomina-nota.py <slug-vecchio> <slug-nuovo> [--family <f>]

Per una scheda progetto rinomina cartella, scheda e log. Aggiorna anche le voci dello stato
(`.state/<fonte>.json`, con `stato.py`) che puntano alla nota spostata.
Per una nota `source-doc` aggiorna anche il campo `family` (con `aggiorna-nota.py`, le altre
righe del frontmatter restano identiche): con `--family` al valore passato; senza, solo se
`family` era uguale allo slug vecchio, e allora diventa lo slug nuovo. `--family` vale solo per
le note `source-doc`.
Le note fonte di SharePoint e OneDrive che seguono un documento spostato o rinominato non si
rinominano a mano: lo fa `sposta-nota.py` (SPEC 6.4), che chiama questo script.
Per unire due doppioni: sposta a mano il contenuto nella nota che resta, cancella l'altra
e lancia questo script con lo slug cancellato come vecchio: i link passano alla nota che resta.

Uscita: 0 se fatto, 2 per un errore d'uso, 1 per gli altri errori (slug non valido o già
usato, slug vecchio duplicato, `family` non aggiornabile).

La variabile d'ambiente VAULT_ROOT, se presente, indica la radice del vault al posto della
cartella che contiene `.claude/` (serve ai test in `.claude/scripts/tests/`).
"""

import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import nota  # noqa: E402
import stato  # noqa: E402

ROOT = Path(os.environ.get("VAULT_ROOT") or Path(__file__).resolve().parents[2]).resolve()
SKIP_DIRS = {".git", ".github", ".claude", "_templates", ".obsidian", ".trash"}
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def _modulo(nome_file, nome):
    spec = importlib.util.spec_from_file_location(nome, Path(__file__).resolve().parent / nome_file)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


aggiorna_nota = _modulo("aggiorna-nota.py", "aggiorna_nota")


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


def frontmatter(p):
    """Frontmatter della nota come dizionario, o None se manca o non si legge."""
    try:
        fm, _ = nota.dividi(p.read_text(encoding="utf-8"))
        data = yaml.safe_load(fm)
    except (nota.Errore, yaml.YAMLError, OSError):
        return None
    return data if isinstance(data, dict) else None


def argomenti(argv):
    if any(a in ("-h", "--help") for a in argv):
        print(__doc__)
        sys.exit(0)
    pos, family = [], None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--family":
            if i + 1 >= len(argv) or not argv[i + 1].strip():
                sys.stderr.write("--family vuole un valore\n")
                sys.exit(2)
            family = argv[i + 1].strip()
            i += 1
        elif a.startswith("--"):
            sys.stderr.write(f"opzione sconosciuta: {a}\n\n{__doc__}")
            sys.exit(2)
        else:
            pos.append(a)
        i += 1
    if len(pos) != 2:
        sys.stderr.write(__doc__)
        sys.exit(2)
    return pos[0], pos[1], family


def nuova_family(data, old, new, family):
    """Valore di `family` dopo la rinomina, o None se resta com'è."""
    if family is not None:
        return family if data.get("family") != family else None
    return new if data.get("family") == old else None


def main():
    old, new, family = argomenti(sys.argv[1:])
    if not SLUG_RE.match(new):
        sys.exit(f"`{new}` non è uno slug valido")
    notes = list(vault_notes())
    if any(p.stem == new for p in notes):
        sys.exit(f"Esiste già una nota `{new}`")
    found = [p for p in notes if p.stem == old]
    if len(found) > 1:
        sys.exit(f"Slug `{old}` duplicato: " + ", ".join(str(p.relative_to(ROOT)) for p in found))
    data = frontmatter(found[0]) if found else None
    fonte_doc = bool(data) and data.get("type") == "source-doc"
    if family is not None and not fonte_doc:
        sys.stderr.write(f"--family vale solo per una nota source-doc esistente, non per `{old}`\n")
        sys.exit(2)

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

    # family delle note fonte: dal frontmatter, non con una sostituzione nel testo
    family_aggiornata, errore_family = None, None
    if fonte_doc:
        valore = nuova_family(data, old, new, family)
        if valore is not None:
            rel = str(moved[found[0]].relative_to(ROOT))
            try:
                aggiorna_nota.aggiorna(rel, [f"family={json.dumps(valore, ensure_ascii=False)}"], [], {}, False)
                family_aggiornata = valore
            except nota.Errore as e:
                errore_family = f"family non aggiornata in `{rel}`: {e}"

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
            data_stato = stato.leggi(fonte)
            cambiato = False
            for v in data_stato[coll].values():
                if v.get("note") in spostate:
                    v["note"] = spostate[v["note"]]
                    cambiato = True
            if cambiato:
                stato.scrivi(fonte, data_stato)
                stato_aggiornato += 1

    extra = f", {stato_aggiornato} file di stato aggiornati" if stato_aggiornato else ""
    if family_aggiornata is not None:
        extra += f", family `{family_aggiornata}`"
    print(f"[[{old}]] → [[{new}]]: {'nota rinominata, ' if found else ''}{changed} note aggiornate{extra}")
    if errore_family:
        sys.exit(errore_family)


if __name__ == "__main__":
    main()
