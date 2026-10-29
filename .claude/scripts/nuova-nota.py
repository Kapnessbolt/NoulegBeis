#!/usr/bin/env python3
"""Crea una nota dal template del suo tipo, con il frontmatter validato (SPEC 4.2, CLAUDE.md §2).

Uso:
  python3 .claude/scripts/nuova-nota.py <tipo> <percorso> [--titolo "<titolo>"]
          [--campo chiave=valore ...] [--json]

- <tipo>: il `type` del frontmatter (`source-doc`, `source-mail`, `person`, `client`, `topic`,
  `inbox`, `journal`, `session`, `proposal`, `project`, `project-log`); il template è quello
  di `_templates/` per quel tipo.
- <percorso>: relativo alla radice del vault, nella cartella del tipo, con il nome in slug
  (es. `sources/sharepoint/salesmarketing/deck/company-profile.md`).
- `--titolo` sostituisce `{{title}}` (obbligatorio se il template lo usa); `{{date:YYYY-MM-DD}}`
  diventa la data di oggi nel fuso del vault (`vault.yaml`).
- `--campo chiave=valore`: valore in YAML. Liste tra quadre (`--campo 'tags=[ddt, brief]'`),
  wikilink anche senza virgolette (`--campo projects=[[manini]]` diventa `["[[manini]]"]`),
  `current.*` con la notazione a punto (`--campo current.item_id=01EF...`), istanti
  `AAAA-MM-GGTHH:MM:SSZ`.
- Per `source-doc`, se non li passi: `source` dalla cartella (`sources/<fonte>/`), `family` dal
  nome della nota, `ingested_at` all'istante attuale UTC, `versions` con la voce di `current`
  (per GitHub il nome porta il commit abbreviato preso da `current.uri`, SPEC 4.2).

Il frontmatter si valida contro il template come in `controlla-vault.py` (campi mancanti o
sconosciuti, `current` completo, valori ammessi) più il formato di istanti e wikilink: se non è
valido esce con 2 e non scrive niente. Non sovrascrive mai una nota esistente (uscita 1). I
wikilink verso note che non esistono ancora sono un avviso su stderr: vanno create prima del
commit. Il corpo resta quello del template, con le sezioni da riempire.

La variabile d'ambiente VAULT_ROOT, se presente, indica la radice del vault al posto della
cartella che contiene `.claude/` (serve ai test in `.claude/scripts/tests/`).
"""

import copy
import datetime as dt
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config  # noqa: E402
import nota  # noqa: E402
from famiglia import famiglia  # noqa: E402

try:
    OGGI = config.oggi()
except config.ConfigErrata as e:
    sys.exit("Configurazione non valida:\n" + "\n".join(f"- {m}" for m in e.errori))


def nome_versione(data):
    cur = data.get("current") or {}
    nome = cur.get("name") or ""
    if data.get("source") == "github":
        m = re.search(r"@([0-9a-f]{7,40})$", str(cur.get("uri") or ""))
        if m and "@" not in nome:
            return f"{nome}@{m.group(1)[:7]}"
    return nome


def crea(tipo, rel, titolo, campi):
    sch = nota.schema(tipo)
    rel = Path(rel)
    if rel.is_absolute() or ".." in rel.parts or rel.suffix != ".md" or len(rel.parts) < 2:
        raise nota.Errore(f"`{rel}`: serve un percorso relativo alla radice del vault che finisce con .md")
    attesi = nota.TYPE_BY_DIR.get(rel.parts[0])
    if not attesi or tipo not in attesi:
        raise nota.Errore(f"il tipo {tipo} non va in {rel.parts[0]}/ (CLAUDE.md §2)")
    if not nota.SLUG_RE.match(rel.stem):
        raise nota.Errore(f"`{rel.stem}` non è uno slug (minuscolo, trattini, senza accenti)")
    if tipo == "project" and rel.stem != rel.parent.name:
        raise nota.Errore("la scheda progetto si chiama come la sua cartella")
    p = nota.ROOT / rel
    if p.exists():
        return None, [f"la nota `{rel}` esiste già: usa aggiorna-nota.py"]
    altre = nota.slug_esistenti().get(rel.stem)
    if altre:
        raise nota.Errore(f"slug `{rel.stem}` già usato da {', '.join(map(str, altre))} (gli slug sono unici)")

    data = copy.deepcopy(sch["default"])
    for k in data:  # `{{date:YYYY-MM-DD}}` del template: oggi
        if isinstance(data[k], dt.date) and not isinstance(data[k], dt.datetime):
            data[k] = OGGI
    passati = set()
    for arg in campi:
        k, v = nota.campo(arg)
        nota.imposta(data, sch, k, v)
        passati.add(k)

    if tipo == "source-doc":
        if "source" not in passati and len(rel.parts) > 1 and rel.parts[1] in nota.SOURCE_BY_DIR:
            data["source"] = nota.SOURCE_BY_DIR[rel.parts[1]]
        if "family" not in passati:
            data["family"] = rel.stem
        if "ingested_at" not in passati:
            data["ingested_at"] = nota.adesso()
        if "versions" not in passati:
            cur = data.get("current") or {}
            data["versions"] = [{"name": nome_versione(data), "item_id": cur.get("item_id") or "",
                                 "last_modified": cur.get("last_modified")}]

    errori, avvisi = nota.valida(data, sch)
    if tipo == "source-doc":
        nome = (data.get("current") or {}).get("name") or ""
        fam = famiglia(nome.split("@")[0]) if nome and data.get("source") != "github" else None
        if fam and data["family"] != fam and not str(data["family"]).endswith("-" + fam):
            avvisi.append(f"family `{data['family']}` diversa da quella calcolata dal nome ({fam})")
        if data.get("family") != rel.stem:
            avvisi.append(f"family `{data['family']}` diversa dal nome della nota ({rel.stem})")
    if errori:
        raise nota.Errore("frontmatter non valido: " + "; ".join(errori))

    raw = sch["template"].replace("{{date:YYYY-MM-DD}}", OGGI.isoformat())
    _, corpo = nota.dividi(raw)
    if "{{title}}" in corpo:
        if not titolo:
            raise nota.Errore(f"il template {tipo} ha il titolo: serve --titolo")
        corpo = corpo.replace("{{title}}", titolo)
    elif titolo:
        corpo = corpo.rstrip("\n") + f"\n\n# {titolo}\n"
    fm = nota.rendi_frontmatter(data, sch["ordine"])
    p.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(p, "x", encoding="utf-8") as f:  # "x": mai sovrascrivere
            f.write(nota.unisci(fm, corpo))
    except FileExistsError:
        return None, [f"la nota `{rel}` esiste già: usa aggiorna-nota.py"]
    return str(rel), avvisi


def main(argv):
    if len(argv) < 2 or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if argv and argv[0] in ("-h", "--help") else 2
    tipo, rel = argv[0], argv[1]
    titolo, campi, as_json = None, [], False
    i = 2
    while i < len(argv):
        a = argv[i]
        if a == "--json":
            as_json = True
        elif a in ("--titolo", "--campo"):
            if i + 1 >= len(argv):
                raise nota.Errore(f"{a} vuole un valore")
            if a == "--titolo":
                titolo = argv[i + 1]
            else:
                campi.append(argv[i + 1])
            i += 1
        else:
            raise nota.Errore(f"argomento non riconosciuto: {a}")
        i += 1
    creata, messaggi = crea(tipo, rel, titolo, campi)
    if creata is None:
        sys.stderr.write(f"errore: {messaggi[0]}\n")
        return 1
    for a in messaggi:
        sys.stderr.write(f"avviso: {a}\n")
    print(json.dumps({"nota": creata, "avvisi": messaggi}, ensure_ascii=False) if as_json else creata)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except nota.Errore as e:
        sys.stderr.write(f"errore: {e}\n")
        sys.exit(2)
