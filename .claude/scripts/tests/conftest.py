"""Mini-vault di prova per i test degli script (SPEC 4.4, step 11 di SPEC 13.1).

Il fixture `vault` costruisce in `tmp_path` un vault valido: template copiati da `_templates/`,
configurazione minima in `.claude/`, lo stato per fonte in `.state/<fonte>.json` e una nota per
tipo, collegate tra loro e con le fonti citate, più `vault.yaml` con un tenant finto e una SPEC.md
ridotta alla tabella dei task. Gli script girano con `VAULT_ROOT` puntato lì; quelli importati
nei test leggono la stessa configurazione (fixture `configurazione_di_prova`).
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

sys.path.insert(0, str(SCRIPTS))
import config  # noqa: E402

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
    "onedrive": {"watermark": None, "items": {}},
    "outlook": {"watermark": None, "threads": {}},
    "github": {"repos": {}, "items": {}},
    "reconcile": {"last_run": None},
}

# Configurazione del vault di prova (SPEC 13.1, step 13): tenant e utente finti, un nome di
# server MCP con GUID come in locale (SPEC 2), gli stessi task e orari del vault reale.
GUID_SERVER = "6501b655-9b79-4832-8016-17eddb19e4b6"
SERVER_M365 = ("Microsoft_365", GUID_SERVER)
LETTURA = ("sharepoint_search", "sharepoint_folder_search", "outlook_email_search", "read_resource")
CALENDARIO = ("outlook_calendar_search",)
TENANT_SP = "https://example.sharepoint.com"
TENANT_OD = "https://example-my.sharepoint.com"
UTENTE_OD = "utente_prova_example_com"
CARTELLA_OD = "Lavoro"

VAULT_YAML = f"""versione: 1

vault:
  nome: Vault di prova
  utente: Utente Prova
  organizzazione: Esempio
  organizzazione_slug: esempio
  dominio_organizzazione: example.com
  fuso: Europe/Rome
  lingua: it
  titolo_cockpit: Cockpit di prova

sezioni:
  stato: Stato
  attivita: Attività
  decisioni: Decisioni
  prossimi_passi: Prossimi passi
  fonti: Fonti
  chi_sono: Chi sono
  relazione: Relazione con BlueAge
  punti_chiave: Punti chiave
  interazioni: Interazioni recenti
  novita: Novità ingerite
  esito_task: Esito dei task
  da_fare: Da fare

connettori:
  microsoft365:
    server: [{", ".join(SERVER_M365)}]
    lettura: [{", ".join(LETTURA)}]
    calendario: [{", ".join(CALENDARIO)}]
  github:
    server: [github]
    lettura: [issue_read, get_file_contents]

agenti:
  ingestor: [microsoft365.lettura, github.issue_read]
  librarian: [microsoft365.lettura, github.lettura]

fonti:
  sharepoint:
    tenant: {TENANT_SP}
    sito: internal
    librerie: [SalesMarketing, Delivery, Shared Documents]
    escluse: [Knowledge, SiteAssets]
  onedrive:
    tenant: {TENANT_OD}
    utente: {UTENTE_OD}
    libreria: Documents
    cartella: {CARTELLA_OD}
    cartella_chat_finale: chat
  esclusioni:
    cartelle: [siteassets, _originali, _sorgenti, dati]
    finali: [transcript]
    dentro: [[evidenze, export]]
  tipi_processati: [pdf, docx, pptx, xlsx, md, txt]
  firme_in_coda: [blueage]
  outlook:
    mittenti_scartati: [no-reply, noreply]
  github:
    repository:
      - repo: esempio/progetto
        branch: main
        progetto: alfa

task:
  - nome: ingest-sharepoint
    orari: ["06:50"]
    giorni: ogni-giorno
    modello: opus
    connettori: [microsoft365]
  - nome: ingest-outlook
    orari: ["07:05", "13:15"]
    giorni: ogni-giorno
    modello: opus
    connettori: [microsoft365]
  - nome: ingest-github
    orari: ["07:20"]
    giorni: ogni-giorno
    modello: opus
    connettori: [github]
  - nome: cockpit
    orari: ["07:40", "13:40"]
    nome_claude: [DailyBoard, DailyBoard2]
    giorni: ogni-giorno
    modello: sonnet
    connettori: [microsoft365]
  - nome: digest
    orari: ["07:45"]
    giorni: ogni-giorno
    modello: sonnet
    connettori: []
  - nome: reconcile
    orari: ["08:45"]
    giorni: domenica
    modello: sonnet
    connettori: [microsoft365]
  - nome: curator
    orari: ["21:10"]
    giorni: domenica
    modello: opus
    connettori: [github]
    digest: false
"""

# SPEC.md ridotta alla tabella dei task (SPEC 7), coerente con VAULT_YAML
SPEC_MD = """# SPEC di prova

## 7. Task schedulati

Orari nel fuso del vault.

| Task | Quando | Connettori | Modello | Cosa fa |
|---|---|---|---|---|
| `ingest-sharepoint` | Ogni giorno alle 06:50 | Microsoft 365 | Opus | 6.2 |
| `ingest-outlook` | Ogni giorno alle 07:05 e alle 13:15 (due task) | Microsoft 365 | Opus | 6.3 |
| `digest` | Ogni giorno alle 07:45 | Nessuno | Sonnet | Digest |
| `ingest-github` | Ogni giorno alle 07:20 | GitHub | Opus | 6.6 |
| `reconcile` | Domenica alle 08:45 | Microsoft 365 | Sonnet | 6.4 |
| `cockpit` | Ogni giorno alle 07:40 e alle 13:40 (due task) | Microsoft 365 | Sonnet | Cockpit |
| `curator` | Domenica alle 21:10 | GitHub | Opus | 9.2 |

Il resto della sezione non conta.

## 8. Comandi manuali

| Comando | Quando |
|---|---|
| `/oggi` | Ogni giorno alle 09:00 |
"""

M365_LETTURA = [f"mcp__{s}__{t}" for s in SERVER_M365 for t in LETTURA]
SETTINGS = {"permissions": {"allow": [
    *(f"mcp__{s}__{t}" for s in SERVER_M365 for t in LETTURA + CALENDARIO),
    "mcp__github__issue_read", "mcp__github__get_file_contents",
    "Bash(git pull:*)",
]}}
AGENTI = {
    "ingestor": ["Read", "Write", "Bash", *M365_LETTURA, "mcp__github__issue_read"],
    # come nel vault reale prima di `config.py applica`: github in un altro ordine rispetto a vault.yaml
    "librarian": ["Read", "Bash", *M365_LETTURA, "mcp__github__get_file_contents", "mcp__github__issue_read"],
    "curator": ["Read", "Write", "Bash"],
}


def agente(nome, tools):
    return f"---\nname: {nome}\ndescription: Agente di prova.\ntools: {', '.join(tools)}\n---\n\nAgente di prova.\n"


@pytest.fixture(autouse=True)
def configurazione_di_prova():
    """Gli script importati nei test (perimetro, famiglia) leggono VAULT_YAML, non il vault reale."""
    conf = config.da_testo(VAULT_YAML)
    config.imposta(conf)
    yield conf
    config.imposta(None)


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
    (root / ".claude" / "settings.json").write_text(json.dumps(SETTINGS, indent=2) + "\n", encoding="utf-8")
    for nome, tools in AGENTI.items():
        (root / ".claude" / "agents" / f"{nome}.md").write_text(agente(nome, tools), encoding="utf-8")
    (root / "vault.yaml").write_text(VAULT_YAML, encoding="utf-8")
    (root / "SPEC.md").write_text(SPEC_MD, encoding="utf-8")
    (root / ".state").mkdir()
    for fonte, contenuto in STATO.items():
        (root / ".state" / f"{fonte}.json").write_text(json.dumps(contenuto, indent=2), encoding="utf-8")
    for rel, testo in NOTE.items():
        scrivi(root, rel, testo)
    git(root, "init", "-q")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "vault di prova")
    return root


def leggi_stato(root, fonte):
    return json.loads((root / ".state" / f"{fonte}.json").read_text(encoding="utf-8"))


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
