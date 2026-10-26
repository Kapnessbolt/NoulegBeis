"""Mini-vault di prova per i test degli script (SPEC 4.4, step 11 di SPEC 13.1).

Il fixture `vault` costruisce in `tmp_path` un vault valido: template copiati da `_templates/`,
configurazione minima in `.claude/`, `.state/ingest.json` e una nota per tipo, collegate tra
loro e con le fonti citate. Gli script girano con `VAULT_ROOT` puntato lì.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1]
REPO = SCRIPTS.parents[1]

NOTE = {
    "projects/alfa/alfa.md": """---
type: project
status: attivo
role: "consulente AI"
clients: ["[[cliente-uno]]"]
people: ["[[mario-rossi]]"]
updated: 2026-10-20
---

# Progetto Alfa

## Stato

- Avviato il caso pilota sul reparto acquisti ([[doc-alfa]])

## Attività

- [ ] Inviare la proposta 📅 2026-11-05 ([[doc-alfa]])
- [ ] Preparare la demo ([[doc-alfa]])
- [x] Raccogliere i requisiti ✅ 2026-10-15 ([[doc-alfa]])

## Decisioni

- Si parte da un solo reparto ([[doc-alfa]])

## Prossimi passi

-

## Fonti

- [[doc-alfa]]
""",
    "projects/alfa/alfa-log.md": """---
type: project-log
project: "[[alfa]]"
---

# Log · Progetto Alfa

- 2026-10-20 · Avvio del caso pilota · [[doc-alfa]]
- 2026-10-15 · Requisiti raccolti · [[doc-alfa]]
""",
    "projects/beta/beta.md": """---
type: project
status: in-pausa
role: ""
clients: []
people: []
updated: 2026-10-20
---

# Progetto Beta

## Stato

- In pausa in attesa del budget ([[2026-10-20-prova]])

## Attività

- [x] Chiudere la prima fase ✅ 2026-10-10 ([[2026-10-20-prova]])

## Decisioni

-

## Prossimi passi

-

## Fonti

-
""",
    "clients/cliente-uno.md": """---
type: client
status: cliente
sector: "manifatturiero"
people: ["[[mario-rossi]]"]
projects: ["[[alfa]]"]
tags: []
updated: 2026-10-20
---

# Cliente Uno

## Chi sono

- Azienda manifatturiera con 200 persone ([[doc-alfa]])

## Relazione con BlueAge

- Cliente dal 2026, budget di 3.000 € per il pilota ([[doc-alfa]])

## Persone di riferimento

- [[mario-rossi]]

## Progetti

- [[alfa]]

## Fonti

- [[doc-alfa]]
""",
    "people/mario-rossi.md": """---
type: person
org: "[[cliente-uno]]"
role: "responsabile acquisti"
email: "mario.rossi@example.com"
projects: ["[[alfa]]"]
tags: []
updated: 2026-10-20
---

# Mario Rossi

## Ruolo e contesto

Referente del progetto [[alfa]].

## Interazioni recenti

- 2026-10-20 · avvio del pilota · [[doc-alfa]]
""",
    "topics/tema-uno.md": """---
type: topic
kind: metodo
projects: ["[[alfa]]"]
clients: ["[[cliente-uno]]"]
tags: []
updated: 2026-10-20
---

# Tema Uno

## Cos'è

Un metodo di prova.

## Punti chiave

- Si misura il tempo per documento ([[doc-alfa]])

## Dove è usato

- [[alfa]]

## Fonti

- [[doc-alfa]]
""",
    "sources/sharepoint/delivery/doc-alfa.md": """---
type: source-doc
source: sharepoint
family: "delivery/doc-alfa"
current:
  item_id: "01EFCYUZYLVH33U2NLBVGZ45BE6NPUJZD5aGVsbG8gd29ybGQgdGhpcyBpcyBhIHNlY3JldA"
  uri: "file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKVSDgPuvHRsSIc3xR8AKeVG/01EFCYUZYLVH"
  web_url: "https://example.sharepoint.com/sites/internal/Delivery/Doc_Alfa_v2.pdf"
  name: "Doc_Alfa_v2.pdf"
  last_modified: 2026-10-01T10:00:00Z
versions: []
also_at: []
status: active
partial: false
ingested_at: 2026-10-02
projects: ["[[alfa]]"]
clients: ["[[cliente-uno]]"]
topics: ["[[tema-uno]]"]
tags: []
---

# Documento Alfa

## Riassunto

Proposta per il pilota di [[cliente-uno]], seguita da [[mario-rossi]].

## Punti chiave

- Il carico stimato è di 1.860 ore all'anno

## Numeri

- 3.000 € di budget, 15% di risparmio atteso

## Decisioni e azioni

-

## Versioni

- Doc_Alfa_v2.pdf · 2026-10-01
""",
    "sessions/2026-10-20-prova.md": """---
type: session
date: 2026-10-20
surface: cloud
topics: ["[[tema-uno]]"]
outcome: ""
---

# Sessione di prova

## Obiettivo

Provare il vault.

## Decisioni

-

## File toccati

-

## Aperti

- [ ] Rivedere [[beta]]
""",
    "inbox/2026-10-20-idea.md": """---
type: inbox
created: 2026-10-20
---

# Idea da smistare

## Da fare

- [ ] Valutare [[tema-uno]] per un altro cliente 📅 2026-11-01
""",
    "journal/2026-10-20.md": """---
type: journal
date: 2026-10-20
---

# Digest 2026-10-20

## Novità ingerite

- [[doc-alfa]] · nuova · documento del pilota

## Attività in scadenza

-

## Decisioni

-

## Scartate

-

## Controllo del vault

-

## Esito dei task

| Task | Esito |
|---|---|
| ingest-sharepoint 06:50 | OK · 1 nota nuova |
""",
}

STATO = {
    "sharepoint": {"watermark": "2026-10-02T06:50:00Z", "items": {
        "item-1": {"last_modified": "2026-10-01T10:00:00Z", "note": "sources/sharepoint/delivery/doc-alfa.md"},
    }},
    "onedrive": {"watermark": "", "items": {}},
    "outlook": {"watermark": "", "threads": {}},
    "github": {"repos": {}, "items": {}},
    "reconcile": {"last_run": ""},
}

# Configurazione minima: un nome di server MCP con GUID, come in locale (SPEC 2)
GUID_SERVER = "6501b655-9b79-4832-8016-17eddb19e4b6"
LETTURA = ("sharepoint_search", "sharepoint_folder_search", "outlook_email_search", "read_resource")
SETTINGS = {"permissions": {"allow": [f"mcp__{s}__{t}" for s in ("Microsoft_365", GUID_SERVER) for t in LETTURA]}}
INGESTOR = "---\nname: ingestor\ntools: Read, " + ", ".join(
    f"mcp__{s}__{t}" for s in ("Microsoft_365", GUID_SERVER) for t in LETTURA) + "\n---\n\nAgente di prova.\n"


def git(root, *args):
    return subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.com",
                           "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", *args],
                          cwd=root, capture_output=True, text=True, check=True)


@pytest.fixture
def vault(tmp_path):
    """Mini-vault valido, già committato in un repo git (serve a `--modificati`)."""
    root = tmp_path / "vault"
    shutil.copytree(REPO / "_templates", root / "_templates")
    (root / ".claude" / "agents").mkdir(parents=True)
    (root / ".claude" / "settings.json").write_text(json.dumps(SETTINGS, indent=2), encoding="utf-8")
    (root / ".claude" / "agents" / "ingestor.md").write_text(INGESTOR, encoding="utf-8")
    (root / ".state").mkdir()
    (root / ".state" / "ingest.json").write_text(json.dumps(STATO, indent=2), encoding="utf-8")
    for rel, testo in NOTE.items():
        scrivi(root, rel, testo)
    git(root, "init", "-q")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "vault di prova")
    return root


def scrivi(root, rel, testo):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(testo, encoding="utf-8")
    return p


def aggiungi(root, rel, testo):
    """Aggiunge testo in coda al corpo di una nota."""
    p = root / rel
    p.write_text(p.read_text(encoding="utf-8") + "\n" + testo + "\n", encoding="utf-8")


def esegui(script, root, *args):
    env = {**os.environ, "VAULT_ROOT": str(root)}
    return subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)],
                          cwd=root, env=env, capture_output=True, text=True)
