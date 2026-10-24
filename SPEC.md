# SPEC · Second Brain BlueAge (personale)

Versione 1.13 · 25/10/2026 · Owner: Lorenzo Curione

Questo file è la specifica di riferimento del vault. Ogni sessione Claude Code che costruisce o modifica il sistema parte da qui. Le modifiche alla specifica si fanno con una PR dedicata.

---

## 1. Scopo

Un second brain personale sulla knowledge BlueAge, gestito da un agente, che:

1. tiene organizzati i progetti su cui lavoro e le relative attività;
2. risponde a domande sulla knowledge BlueAge;
3. produce materiali BlueAge (deck, corsi) tramite skill;
4. ingerisce in automatico le novità da SharePoint, OneDrive e Outlook;
5. tiene un diario delle sessioni e propone nuove regole, skill, agenti e hook.

Utente unico. Il repo è privato, ma i dati riservati (credenziali, coordinate bancarie, dati personali, dati reali dei clienti riga per riga) non entrano comunque nelle note: regola in `CLAUDE.md` §5.

## 2. Architettura

| Componente | Scelta | Ruolo |
|---|---|---|
| Storage del vault | Repo GitHub privato (account personale) | Fonte di verità: markdown + configurazione Claude Code |
| Esecuzione | Claude Code in cloud (claude.ai/code) e in locale (app desktop, sessione aperta sulla cartella del vault sul PC) | Sessioni interattive: in cloud da desktop, mobile e PC diversi; in locale dal PC, con mod e pannelli |
| Automazione | Task schedulati cloud (claude.ai/code/routines) | Ingestion periodica, riconciliazione, curator |
| Fonti | Connettore Microsoft 365 (tenant blueage.it) | Lettura di SharePoint, OneDrive e Outlook; upload dei file prodotti |
| Visualizzazione | Obsidian (vault = clone del repo) | Lettura, grafo, cattura veloce; `home.md` come pagina iniziale |
| Riepilogo | Dashboard Cockpit su claude.ai (artifact privato) | Calendario Outlook dal vivo, progetti e attività dal vault |
| Pannello locale | Mod `cockpit` dell'app desktop (caricata sull'account, si attiva una volta per PC) | Nelle sessioni locali aperte sul vault: calendario Outlook dal vivo, scadenze e progetti letti dai file; `/cockpit` lo dà in testo dove il pannello non si disegna |
| Documenti originali | Restano su SharePoint, OneDrive e Outlook | Nel repo vanno solo le note markdown che li citano |

Vincoli dell'ambiente cloud da rispettare:
- Ogni sessione parte da un clone nuovo. Tutto ciò che conta (regole, skill, agenti, hook, stato) deve essere committato.
- Il setup locale di Claude Code (impostazioni utente, mod) non arriva in cloud: ciò che deve valere ovunque sta in `.claude/` del vault.
- `/plugin` non è disponibile: le skill stanno in `.claude/skills/`. Le mod funzionano solo nelle sessioni locali.
- Intervallo minimo dei task schedulati: 1 ora.

Sessioni locali (app desktop sul PC):
- La sessione si apre sulla cartella del vault: `.claude/settings.json`, hook e comandi si leggono solo dalla cartella aperta. Gli altri repo si clonano accanto (`../<repo>`) e si aggiungono alla sessione quando servono.
- Il clone resta sul PC e va allineato: lo fa l'hook di avvio (sezione 11).
- Requisiti del PC: git, python3 (script e pre-commit, 4.4), login GitHub con `gh auth login`, app desktop aggiornata.
- GitHub passa dal login del PC, senza connettore: le issue si leggono con `gh issue view` (6.6).
- Il connettore Microsoft 365 ha un nome di server diverso per ambiente (`Microsoft_365` nelle sessioni cloud, `Microsoft-365` nei task schedulati, l'id del connettore nelle sessioni locali). I permessi in `.claude/settings.json` e i `tools` dell'agente `ingestor` li elencano tutti: un nome nuovo va aggiunto in entrambi, altrimenti la modalità Auto blocca le letture e l'ingestor parte senza connettore. Il controllo del vault (4.4) segnala come errore i nomi che non coincidono.
- I task schedulati restano in cloud qualunque sessione si usi.

## 3. Struttura del vault

```
/
├── SPEC.md                  questa specifica
├── CLAUDE.md                istruzioni operative per ogni sessione
├── .github/workflows/       controllo del vault su ogni push (4.4)
├── README.md                guida rapida per l'utente
├── home.md                  vista Obsidian con Tasks e Dataview (fuori dal controllo 4.4)
├── .claude/
│   ├── settings.json        hook e permessi
│   ├── commands/            comandi manuali (sezione 8)
│   ├── agents/              agenti specializzati (sezione 9)
│   ├── hooks/               hook di Claude Code (controllo prima del commit 4.4, pull all'avvio 11)
│   ├── routines/            procedure dei task schedulati (sezione 7)
│   ├── scripts/             script di servizio (controllo e rinomina delle note 4.4, dati della dashboard 7)
│   └── skills/              skill (sezione 10)
├── .state/
│   └── ingest.json          stato dell'ingestion (sezione 6.1)
├── inbox/                   catture rapide da smistare
├── projects/<slug>/
│   ├── <slug>.md            scheda progetto: stato, attività, prossimi passi
│   └── <slug>-log.md        cronologia degli avanzamenti
├── clients/<slug>.md        clienti e prospect (Manini, Meccanotecnica Umbra, Velo-CE…)
├── people/<slug>.md         persone (interne ed esterne)
├── topics/<slug>.md         prodotti, offerte, metodi (AI Foundation Program, Pulse, COMPASS…)
├── sources/
│   ├── sharepoint/<libreria>/<percorso>/<famiglia>.md
│   ├── onedrive/<percorso>/<famiglia>.md
│   ├── mail/<AAAA-MM>/<slug-thread>.md
│   ├── attachments/<famiglia>.md   allegati senza corrispondente su SharePoint
│   └── github/<repo>/<percorso>/<famiglia>.md   documenti e issue dei repo di progetto (5.4)
├── journal/
│   └── AAAA-MM-DD.md        digest giornaliero: novità ingerite, attività in scadenza
├── sessions/
│   ├── AAAA-MM-DD-<slug>.md diario delle sessioni
│   └── _raw/                trascrizioni grezze (retention 30 giorni)
├── proposals/               proposte del curator (regole, skill, agenti, hook)
└── _templates/              template delle note
```

Scritture per cartella, per ridurre i conflitti git:

| Chi scrive | Dove |
|---|---|
| Task di ingestion | `sources/`, `journal/`, `.state/`, note nuove in `people/`, `clients/` e `topics/`, e in aggiunta (solo righe nuove) `## Interazioni recenti` di `people/*.md`, `projects/<slug>/<slug>-log.md` e le sezioni "Attività" di `projects/<slug>/<slug>.md` |
| Ingestion lanciata da una sessione interattiva (`/ingest`, `/ingest-file`) | Come il task di ingestion, più: note nuove in `inbox/`; righe nuove in `## Fonti` di clienti e temi esistenti |
| Curator | `proposals/`, `sessions/` |
| Sessioni interattive | Ovunque |

Un collegamento non resta mai rotto: se la nota di destinazione non esiste, l'ingestion la crea. Le persone si creano complete (nome, email, organizzazione). Clienti e temi creati da un task schedulato sono note minime con il tag `da-verificare`, segnalate nel digest e da `/controlla` finché l'utente non le rivede e toglie il tag. Prima di creare una persona si cerca una nota con la stessa email. Se c'è solo un nome simile: senza email è la stessa persona e si collega quella; con un'email diversa si crea la nuova persona. In entrambi i casi il possibile doppione va nel digest. I progetti non si creano mai in automatico: la fonte resta collegata a clienti e temi e la proposta va nel digest.

## 4. Regole delle note

### 4.1 Convenzioni generali

- Lingua: italiano.
- Nomi file: slug minuscolo con trattini (`entrata-merci-manini.md`).
- Collegamenti: wikilink Obsidian `[[slug]]`. Lo slug è il nome del file senza `.md`, quindi la scheda di un progetto si chiama come la sua cartella (`projects/corso-ai-manini/corso-ai-manini.md`) e `[[corso-ai-manini]]` la apre. Ogni nota in `sources/` deve collegarsi ad almeno un progetto, cliente o tema, tramite i campi `projects`, `clients` e `topics` del frontmatter.
- Integrità: nessun wikilink può puntare a una nota inesistente, perché una nota irraggiungibile esce dal grafo e dalle ricerche. Per rinominare una nota si usa `python3 .claude/scripts/rinomina-nota.py <vecchio> <nuovo>`, che aggiorna tutti i collegamenti.
- Tracciabilità: nelle note di temi (`## Punti chiave`), clienti (`## Chi sono`, `## Relazione con BlueAge`) e progetti (`## Stato`, `## Decisioni`) ogni punto o paragrafo cita la nota fonte da cui viene, in coda: `([[slug-fonte]])`. Se l'informazione viene dall'utente, la fonte è il diario della sessione.
- Frontmatter YAML obbligatorio su ogni nota, con i campi del suo tipo (4.2).
- Una nota descrive, non copia: riassunto, punti chiave, numeri, decisioni, azioni. Per il dettaglio si legge l'originale tramite il connettore.

### 4.2 Schemi del frontmatter

**Documento (SharePoint, OneDrive, allegato)**
```yaml
---
type: source-doc
source: sharepoint          # sharepoint | onedrive | attachment | github
family: blueage-company-profile
current:
  item_id: 01EFCYUZYLVH33U2NLBVGZ45BE6NPUJZD5
  uri: file:///{driveId}/{itemId}      # per gli allegati: mail:///messages/{id}/attachments/{id}
  web_url: https://blueagesrl.sharepoint.com/sites/internal/...
  name: BlueAge_CompanyProfile_v24.pdf
  last_modified: 2026-10-01T17:20:46Z
versions:                    # dalla più recente
  - { name: BlueAge_CompanyProfile_v24.pdf, item_id: ..., last_modified: ... }
also_at: []                  # copie dello stesso documento in altre posizioni
status: active               # active | removed
partial: false               # true se il contenuto è stato letto solo in parte
ingested_at: 2026-10-22T06:50:00Z
projects: ["[[ai-foundation-program]]"]
clients: []
topics: ["[[pulse]]"]
tags: []
---
```

Per `source: github` i campi di `current` si leggono così: `item_id` è `<owner>/<repo>:<percorso>` per un file e `<owner>/<repo>#<numero>` per una issue; `uri` è `github://<owner>/<repo>/<percorso>@<commit>` per un file e `github://<owner>/<repo>/issues/<numero>` per una issue; `web_url` è la pagina su GitHub; `name` è il percorso del file (`docs/architettura.md`) o `Issue #<numero> · <titolo>`; `last_modified` è l'istante dell'ultimo commit che ha toccato il file, o `updated_at` della issue. In `versions` il `name` di un file porta il commit abbreviato (`docs/architettura.md@61b833c`).

**Thread di posta**
```yaml
---
type: source-mail
conversation_id: AAQkAGMy...
subject: Automazione Entrata Merci - Caso Manini
participants: ["[[leonardo-pinsone]]", "[[silvia-fumagalli]]"]
first_message: 2026-10-20T17:10:40Z
last_message: 2026-10-21T19:35:37Z
messages: 2
attachments: ["[[blueage-automation-entrata-merci]]"]
projects: ["[[corso-ai-manini]]"]
clients: ["[[manini]]"]
topics: []
status: active
---
```

**Progetto**
```yaml
---
type: project
status: attivo               # attivo | in-pausa | chiuso
role: <il mio ruolo>
clients: []
people: []
updated: 2026-10-22
---
```

Corpo della nota progetto: `## Stato`, `## Attività` (checkbox, con la data nel formato `📅 AAAA-MM-GG`), `## Decisioni`, `## Prossimi passi`, `## Fonti`.

**Sessione**
```yaml
---
type: session
date: 2026-10-22
surface: cloud               # cloud | locale | claude-ai
topics: []
outcome: <una riga>
---
```

Corpo della nota sessione: `## Obiettivo`, `## Decisioni`, `## File toccati`, `## Aperti`.

**Log di progetto** (`projects/<slug>/<slug>-log.md`)
```yaml
---
type: project-log
project: "[[corso-ai-manini]]"
---
```

Corpo: una riga per avanzamento, dalla più recente, nel formato `- AAAA-MM-GG · cosa è successo · [[fonte]]`.

**Cliente**
```yaml
---
type: client
status: cliente              # cliente | prospect | ex-cliente
sector: ""
people: []
projects: []
tags: []
updated: 2026-10-22
---
```

Corpo: `## Chi sono`, `## Relazione con BlueAge`, `## Persone di riferimento`, `## Progetti`, `## Fonti`.

**Persona**
```yaml
---
type: person
org: blueage                 # blueage | [[slug-cliente]] | altro
role: ""
email: ""
projects: []
tags: []
updated: 2026-10-22
---
```

Corpo: `## Ruolo e contesto`, `## Interazioni recenti`.

**Tema**
```yaml
---
type: topic
kind: prodotto               # prodotto | offerta | metodo | tema
projects: []
clients: []
tags: []
updated: 2026-10-22
---
```

Corpo: `## Cos'è`, `## Punti chiave`, `## Dove è usato`, `## Fonti`.

**Digest giornaliero**
```yaml
---
type: journal
date: 2026-10-22
---
```

Corpo: `## Novità ingerite`, `## Attività in scadenza`, `## Decisioni`, `## Scartate`, `## Controllo del vault`, `## Esito dei task`.

**Cattura** (`inbox/`)
```yaml
---
type: inbox
created: 2026-10-22
---
```

**Proposta del curator**
```yaml
---
type: proposal
date: 2026-10-22
kind: regola                 # regola | skill | agente | hook
status: proposta             # proposta | accettata | rifiutata
---
```

Corpo: `## Motivazione`, `## Evidenze`, `## Testo proposto`.

I template di tutti i tipi sono in `_templates/`. Se uno schema cambia, si aggiornano insieme questa sezione e il template.

### 4.3 Versioni dei documenti

- Una nota per famiglia di documenti, non per versione.
- Chiave della famiglia: cartella + nome normalizzato, togliendo i suffissi di versione (`_v15`, `v2`, `- v001`), le date e l'estensione.
- La nota punta sempre all'ultima versione (`current`) e tiene lo storico in `versions`.
- Quando arriva una nuova versione, il riassunto si rigenera e le differenze rilevanti vanno nel `<slug>-log.md` del progetto collegato.

### 4.4 Controllo del vault

Lo script `python3 .claude/scripts/controlla-vault.py` verifica le note (tranne `README.md`, `CLAUDE.md`, `SPEC.md` e `home.md`) e stampa un rapporto in markdown (con `--indice` aggiunge l'elenco di progetti, clienti, persone e temi, con il numero di note che li collegano). Esce con codice 1 se trova errori.

| Livello | Cosa controlla |
|---|---|
| Errore | **Integrità**: wikilink (nel frontmatter o nel testo) verso note inesistenti; wikilink con percorso o estensione; slug duplicati; voci di `.state/ingest.json` che puntano a note inesistenti. **Tracciabilità**: punti senza fonte nelle sezioni elencate in 4.1; fonti senza progetto, cliente o tema. **Schema**: frontmatter mancante o non valido; `type` sconosciuto o nella cartella sbagliata; campi del template mancanti; valori fuori dagli elenchi ammessi; nomi file non in slug; scheda progetto con nome diverso dalla cartella. **Doppioni certi**: stessa email su due persone; stessa `family`, `item_id` o `conversation_id` su due note. **Configurazione**: nomi del server Microsoft 365 diversi tra i `tools` dell'agente `ingestor` e i permessi di `.claude/settings.json`, o con uno dei 4 strumenti in lettura mancante (2) |
| Avviso | Note orfane (persone, clienti, temi che nessuna nota collega); note che citano una fonte rimossa; note più vecchie di una fonte che citano (la fonte è stata aggiornata dopo); note `da-verificare`; nomi quasi uguali nella stessa categoria (possibili doppioni); persone senza email; campi non previsti dal template; documenti SharePoint, OneDrive e GitHub non registrati nello stato |

Quando si esegue:
- **prima di ogni commit**: il pre-commit di git `.githooks/pre-commit` lancia lo script con `--modificati` e blocca il commit se ci sono errori che toccano i file modificati, compresi i collegamenti rotti da una nota cancellata o rinominata. Gira dentro `git commit`, quindi vede anche i file creati nello stesso comando. Si attiva con `git config core.hooksPath .githooks`: nelle sessioni Claude Code lo fa l'hook `SessionStart` di `.claude/settings.json`, sui PC con Obsidian va eseguito una volta dopo il clone. L'hook `PreToolUse` `.claude/hooks/controllo-pre-commit.sh` resta come primo filtro sui comandi `git commit`. Vale per sessioni interattive e task schedulati;
- **su ogni push e PR**: il workflow `.github/workflows/controllo-vault.yml` lo esegue su GitHub, così si vedono anche gli errori introdotti da Obsidian o dal web;
- nella riconciliazione settimanale (6.4), con l'esito nel digest;
- a richiesta con `/controlla`.

## 5. Perimetro delle fonti

### 5.1 SharePoint · `https://blueagesrl.sharepoint.com/sites/internal/`

| Libreria | Stato |
|---|---|
| Knowledge | Esclusa (corsi ufficiali Anthropic: materiale pubblico, si legge dall'originale quando serve) |
| SalesMarketing | Inclusa |
| Delivery | Inclusa |
| Shared Documents | Inclusa |
| SiteAssets | Esclusa (blocco appunti OneNote) |

Esclusioni in qualunque punto del percorso:
- cartelle `_originali` e `_sorgenti`;
- cartelle `Transcript` (es. `05 Transcript`): trascrizioni grezze delle riunioni, già riassunte nei verbali;
- cartelle `Evidenze/Export` (es. `06 Evidenze/Export`): export grezzi di tabelle e dati dei sistemi del cliente;
- cartelle di progetti software (contengono `app.json`, `package.json` o `.git`), es. `Lab AL/BlueAge-LabAL`;
- cartelle `Dati`: dati reali dei clienti, che restano dove sono e non generano note (`CLAUDE.md` §5).

Tipi di file processati: pdf, docx, pptx, xlsx, md, txt. Gli altri tipi (immagini, video, archivi, codice) si ignorano: non generano note, anche perché in gran parte non compaiono nella ricerca di SharePoint e l'ingestion periodica non li vedrebbe.

### 5.2 OneDrive · cartella `BlueAge`

Prefisso: `https://blueagesrl-my.sharepoint.com/personal/lorenzo_curione_blueage_it/Documents/BlueAge/`.
Il resto di OneDrive è escluso.
Tutte le sottocartelle di `BlueAge/` sono incluse e le note ne seguono il percorso (`sources/onedrive/<percorso>/`): aggiungere, rinominare o rinumerare una cartella non richiede modifiche a questa specifica.
Valgono le esclusioni di 5.1, comprese le cartelle `Dati` (es. `01_Materiale clienti/Manini/Progetto Automazione/Dati/`, con i DDT reali di Manini).
Unica cartella con un trattamento speciale: quella il cui nome finisce con `chat` (oggi `BlueAge/00_chat/`) riceve i riassunti delle chat di claude.ai (sezione 8).

### 5.3 Outlook · tutta la casella

La ricerca copre tutte le cartelle, comprese le Inviate.

Scartati sempre:
- mittenti `no-reply`, `noreply`, `notifications` e simili;
- notifiche di servizi (Teams, Azure, SaaS);
- newsletter e marketing;
- thread personali o estranei a BlueAge (`CLAUDE.md` §5); in una sessione interattiva si chiede prima di scartarli.

Per le prime 2 settimane le mail scartate vanno elencate nel digest giornaliero, sotto "Scartate", per verificare il filtro.

### 5.4 GitHub · repo di progetto

Alcuni progetti hanno la documentazione viva in un repo GitHub. Il vault non la copia: ne tiene poche note fonte, scelte una per una, e porta nel progetto collegato solo ciò che conta a livello di progetto (stato, decisioni, scadenze, azioni fuori dal codice). Il dettaglio tecnico resta nel repo.

Si legge solo il branch `main`, e solo l'elenco chiuso qui sotto. Un file o una issue in più si aggiunge a questa tabella.

| Repo | Elemento | Cosa si legge | Nota | Progetto |
|---|---|---|---|---|
| `cristian-schifone/parts-radar` | `docs/architettura.md` | §1 scopo, §5 stato e sequenza, §8 decisioni aperte, §9 rischi | `parts-radar-architettura` | `parts-radar-sviluppo` |
| | `docs/decisione-stack-python.md` | tutto | `parts-radar-decisione-stack-python` | |
| | `docs/whatsapp-fornitori.md` | §1-§3 (problema, confronto, decisione), §5 rischi | `parts-radar-whatsapp-fornitori` | |
| | `docs/kromeda-impatto-parts-radar.md` | §9 consumi e costi | `parts-radar-kromeda-impatto` | |
| | `docs/kromeda-fase0-risultati.md` | §1 sintesi | `parts-radar-kromeda-fase0-risultati` | |
| | `docs/changelog.md` | solo le voci nuove: obiettivo, decisioni, lasciato aperto | `parts-radar-changelog` | |
| | issue #379 | piano del pilot, passi fuori dal codice | `parts-radar-issue-379` | |
| | issue #420 | traguardo del pilot e cosa si misura | `parts-radar-issue-420` | |

Nome della nota: `<repo>-<nome del file senza estensione>` (togliendo dal nome il nome del repo se c'è già) oppure `<repo>-issue-<numero>`. Percorso: `sources/github/<repo>/<cartella del file>/` oppure `sources/github/<repo>/issues/`.

## 6. Ingestion

### 6.1 Stato · `.state/ingest.json`

```json
{
  "sharepoint": { "watermark": "2026-10-22T04:50:00Z", "items": { "<driveId>/<itemId>": { "last_modified": "...", "note": "sources/..." } } },
  "onedrive":   { "watermark": "...", "items": {} },
  "outlook":    { "watermark": "...", "threads": { "<conversationId>": { "last_message": "...", "note": "sources/mail/..." } } },
  "github":     { "repos": { "<owner>/<repo>": { "commit": "<sha di main letto>", "watermark": "<istante di quel commit>" } },
                  "items": { "<owner>/<repo>:<percorso>": { "last_modified": "...", "commit": "<sha>", "note": "sources/github/..." },
                             "<owner>/<repo>#<numero>":   { "last_modified": "<updated_at>", "note": "sources/github/..." } } },
  "reconcile":  { "last_run": "..." }
}
```

### 6.2 Algoritmo del delta (documenti)

1. Leggi il `watermark` della fonte.
2. Chiama `sharepoint_search` con `query: "*"` e `afterDateTime = watermark − 2 ore`. Scorri tutte le pagine. Le 2 ore di sovrapposizione recuperano i ritardi dell'indice di ricerca.
3. Tieni solo i risultati il cui `webUrl` rientra nel perimetro (sezione 5) e non contiene percorsi esclusi.
4. Per ogni file:
   - se `items[id].last_modified` è uguale a quello attuale, salta;
   - altrimenti leggi il contenuto con `read_resource`, individua la famiglia (4.3) e crea o aggiorna la nota.
5. Aggiorna i progetti, clienti e temi collegati (le righe nuove vanno in `<slug>-log.md`).
6. Imposta `watermark` all'ultimo `lastModifiedDateTime` processato con successo. Se nessun file fallisce, il watermark sale al `lastModifiedDateTime` più recente tra tutti i risultati della ricerca, compresi quelli saltati perché invariati o fuori perimetro: così la finestra di ricerca non si allarga nei giorni in cui nel perimetro non cambia nulla. Se un file fallisce, il watermark non lo supera.
7. Commit e push su `main` (sezione 11).

Limite di lettura: oltre 30 pagine o slide, leggi le prime 30 e imposta `partial: true`.

### 6.3 Algoritmo del delta (posta)

1. Chiama `outlook_email_search` con `query: "*"` e `afterDateTime = watermark − 2 ore`. Scorri tutte le pagine (25 per pagina).
2. Applica i filtri di scarto (5.3).
3. Leggi ogni messaggio con `read_resource` e raggruppalo per `conversationId`.
4. Per ogni thread:
   - se esiste, aggiorna la nota (messaggi nuovi in ordine cronologico, riassunto rigenerato);
   - se non esiste, crea `sources/mail/AAAA-MM/<slug-oggetto>.md`.
5. Allegati:
   - ignora quelli con `isInline: true` e le immagini;
   - leggi pdf, docx, pptx, xlsx con `read_resource` sull'URI dell'allegato;
   - se la famiglia esiste già tra le note di SharePoint o OneDrive, aggiungi la versione a quella nota e non crearne un'altra;
   - altrimenti crea `sources/attachments/<famiglia>.md`.
6. Estrai decisioni, azioni e scadenze e portale nel progetto collegato (`## Attività` con data e fonte).
7. Aggiorna il `watermark` e fai commit e push.

### 6.4 Riconciliazione settimanale

1. Elenca le cartelle del perimetro con `read_resource` sugli URI delle cartelle.
2. Confronta gli ID con `.state/ingest.json`:
   - ID non più presenti: la nota passa a `status: removed`;
   - `webUrl` cambiato (file spostato o rinominato): aggiorna la nota;
   - file presenti ma mai ingeriti: mettili in coda per la prossima ingestion.
3. Esegui il controllo del vault (4.4) e riporta errori e avvisi in `## Controllo del vault` del digest.
4. Scrivi l'esito nel digest del giorno.

### 6.5 Primo caricamento

Non lo fa il task schedulato. Si fa con sessioni manuali, una libreria per volta, in quest'ordine:

1. SalesMarketing
2. Delivery
3. Shared Documents
4. OneDrive/BlueAge
5. Outlook, ultimi 60 giorni

Dopo ogni lotto l'utente controlla un campione di note prima di passare al successivo. Al termine si inizializzano i watermark e si attivano i task schedulati.

### 6.6 Algoritmo del delta (GitHub)

Il repo deve essere presente nella sessione: nelle sessioni cloud si collega accanto al vault (`../<repo>`), in locale è il clone accanto al vault sul PC. Le issue si leggono in sola lettura con il connettore GitHub (`issue_read`) o, dove il connettore non c'è (sessioni locali), con `gh issue view`.

1. `git -C <clone> fetch origin main`; `head` = `git rev-parse origin/main`.
2. **File** del perimetro (5.4): `git log -1 --format='%H %cI' origin/main -- <percorso>`. Se il commit è uguale a `items[chiave].commit`, salta. Altrimenti guarda `git diff <commit vecchio>..<commit nuovo> -- <percorso>`:
   - se il diff non tocca le parti elencate in 5.4, aggiorna solo lo stato (`commit`, `last_modified`);
   - altrimenti rileggi quelle parti da `git show origin/main:<percorso>`, aggiorna la nota come nuova versione (4.3) e scrivi le differenze rilevanti nel log del progetto.
   File sparito da `main`: la nota passa a `status: removed`.
3. **Changelog**: le voci nuove sono i titoli `## ` aggiunti tra `repos[repo].commit` e `head` (`git diff`). Per ogni giorno con voci nuove, **una** riga nel log del progetto con ciò che conta a livello di progetto (funzioni chiuse, decisioni, numeri, problemi aperti), senza dettagli tecnici, con fonte la nota del changelog. Le azioni che non sono codice (avvisi, richieste a clienti e fornitori, decisioni da prendere) vanno in `## Attività`. La nota del changelog tiene in `## Voci recenti` una riga per voce degli ultimi 30 giorni.
4. **Issue** del perimetro: se `updated_at` è uguale a `items[chiave].last_modified`, salta. Altrimenti rigenera la nota. Le caselle non spuntate dei passi fuori dal codice diventano attività del progetto, se non ci sono già; quelle spuntate nel repo che nel progetto risultano ancora aperte vanno nel digest, sotto `## Decisioni`, come `- Da spuntare: <attività> · [[fonte]]` (il task non modifica righe esistenti).
5. `repos[repo]` = `head` e il suo istante; aggiorna `items`. Digest, commit e push.

Senza clone o senza connettore GitHub il task non inventa nulla: scrive l'errore nel digest. Se manca solo il connettore, processa i file e salta le issue.

## 7. Task schedulati

Orari in Europe/Rome, fuori dagli orari pieni per evitare i ritardi del sistema.

| Task | Quando | Connettori | Modello | Cosa fa |
|---|---|---|---|---|
| `ingest-sharepoint` | Ogni giorno alle 06:50 | Microsoft 365 | Opus | 6.2 su SharePoint e OneDrive |
| `ingest-outlook` | Ogni giorno alle 07:05 e alle 13:15 (due task) | Microsoft 365 | Opus | 6.3 |
| `digest` | Ogni giorno alle 07:45 | Nessuno | Sonnet | Completa `journal/AAAA-MM-GG.md`: novità, attività in scadenza, decisioni |
| `ingest-github` | Ogni giorno alle 07:20 | GitHub (il vault e i repo di 5.4 come sorgenti) | Opus | 6.6 |
| `reconcile` | Domenica alle 08:45 | Microsoft 365 | Sonnet | 6.4 |
| `cockpit` | Ogni giorno alle 07:40 e alle 13:40 (due task, `DailyBoard` e `DailyBoard2`) | Nessuno | — | Rigenera con `plancia.py` progetti e attività e li carica sulla dashboard Cockpit; riga d'esito nel digest |
| `curator` | Domenica alle 21:10 | GitHub, solo per aprire la PR | Opus | 9.2: proposte dai diari della settimana su un branch suo, con una PR |
| `sessions-cleanup` | Il 1° del mese alle 06:10 (da creare con lo step 5) | Nessuno | — | Cancella `sessions/_raw/` più vecchio di 30 giorni |

Il `cockpit` gira in un ambiente cloud dedicato, senza connettori, perché carica i dati su claude.ai; il calendario la dashboard lo legge da sé con il connettore Microsoft 365 di chi la apre. Il `digest` gira dopo gli ingest del mattino; l'ingest-outlook delle 13:15 scrive nel digest dello stesso giorno, e il digest del giorno dopo non ripete le sue note.

Ogni task:
- si crea dall'interfaccia di claude.ai con il repository e i soli connettori che gli servono, e gira in una sessione nuova a ogni esecuzione;
- ha come prompt `Esegui il task descritto in .claude/routines/<task>.md, seguendo anche .claude/routines/_comune.md.`: la procedura sta nel repo e rimanda alla sezione pertinente di questa SPEC; le regole comuni (avvio, limiti, digest, errori, git) sono in `_comune.md`;
- esegue l'agente `ingestor` dentro la propria sessione, non come subagente;
- fa commit, poi `git pull --rebase` e push su `main`;
- registra l'esito nel digest del giorno ("OK" oppure gli errori), con l'ora in Europe/Rome.

Eccezione: il `curator` non scrive nel digest e non fa push su `main` (sezione 3). Lavora su un branch `claude/curator-AAAA-MM-DD` e il suo esito è la PR; se non trova niente da proporre non apre la PR.

## 8. Comandi manuali (`.claude/commands/`)

| Comando | Funzione |
|---|---|
| `/ingest [fonte] [da data]` | Esegue l'ingestion a richiesta. Senza argomenti esegue tutte le fonti dal watermark |
| `/ingest-file <url o nome>` | Ingerisce un singolo documento, anche fuori dal perimetro |
| `/oggi` | Agenda: attività in scadenza, novità dall'ultimo digest, progetti fermi da più di 14 giorni |
| `/progetto <nome>` | Stato completo di un progetto: attività, decisioni, fonti recenti |
| `/chiudi-sessione` | Scrive o aggiorna il diario della sessione in `sessions/`, spunta gli aperti dei diari precedenti chiusi nella sessione, poi commit e push. È una skill (sezione 10): parte anche quando l'utente chiude la sessione a parole |
| `/cattura <testo>` | Nota rapida in `inbox/` |
| `/smista` | Smista `inbox/` nei progetti e nei temi |
| `/controlla` | Controllo del vault (4.4): errori, possibili doppioni e indice per categoria, con le correzioni proposte |
| `/verifica-task [task] [data]` | Verifica i giri dei task schedulati (7): riga nel digest o PR del curator, commit, watermark, note scritte, doppioni; propone le correzioni e gli aperti da spuntare |
| `/curator [da data] [a data]` | Giro del curator a mano (9.2), di default sugli ultimi 7 giorni: mostra le proposte, registra le decisioni dell'utente nel `status` e apre la PR |

**Chat di claude.ai nel vault.** Nella chat basta chiedere "salva il riassunto di questa chat nel mio OneDrive in BlueAge/00_chat". Il connettore M365 carica il file, e l'ingestion lo trasforma in una nota di tipo `session` con `surface: claude-ai`.

## 9. Agenti (`.claude/agents/`)

### 9.1 `ingestor`

Esegue le sezioni 6.2–6.4. Usato dai task schedulati (modalità `schedulata`) e da `/ingest` e `/ingest-file` (modalità `interattiva`). Scrive solo nelle cartelle consentite alla sua modalità (sezione 3).

### 9.2 `curator`

Ogni settimana (task `curator` della domenica, o a mano con `/curator`):
- legge `sessions/` dell'ultima settimana, e per gli aperti anche i diari precedenti;
- individua pattern ricorrenti, presenti in almeno 2 diari (basta uno se il diario lo indica come spunto per il curator): correzioni ripetute, procedure manuali ripetute, domande senza risposta nel vault, decisioni prese caso per caso, aperti che restano aperti. Un comando o uno step previsti da questa SPEC ma non ancora fatti non contano come già coperti;
- scrive al massimo 5 proposte per giro in `proposals/AAAA-MM-DD-<slug>.md`, ognuna con motivazione, evidenze (link alle sessioni) e testo pronto (regola per `CLAUDE.md`, skill, agente o hook); gli altri pattern vanno in una riga ciascuno nella PR;
- spunta in `sessions/` gli aperti già chiusi altrove, con la prova in coda (`(chiuso in [[<diario o digest>]])`, `(chiuso: PR #n unita)`); quelli chiusi in parte o con prova incerta vanno nella PR come "da verificare";
- apre una PR su un branch `claude/curator-AAAA-MM-DD`.

Le proposte restano in `proposals/` come registro: in revisione l'utente imposta `status` a `accettata` o `rifiutata`. Il curator non ripropone una proposta rifiutata se non ci sono evidenze nuove successive al rifiuto, e nella PR segnala le accettate non ancora applicate.

Il curator non modifica mai direttamente `CLAUDE.md`, `.claude/` o questa SPEC. Le proposte accettate le applica, dopo il merge, una sessione interattiva; quelle che toccano la SPEC con la loro PR dedicata.

### 9.3 `librarian`

Risponde alle domande sulla knowledge:
1. cerca nel vault;
2. se la nota non basta, legge l'originale tramite il connettore;
3. cita sempre le note e i documenti usati.

## 10. Skill (`.claude/skills/`)

| Skill | Origine | Intervento |
|---|---|---|
| `blueage-deck` | Plugin claude.ai | Copiata così com'è |
| `blueage-corso` | Plugin claude.ai | Snellita: `SKILL.md` breve con il flusso; i dettagli (COMPASS, RED TAG, Tocca a voi, kit docente) in file di riferimento caricati solo quando servono |
| `blueage-animazioni` | Plugin claude.ai | Da valutare dopo lo step 6 |
| `chiudi-sessione` | Proposta del curator del 25/10 | Scritta nel vault: è `/chiudi-sessione` (sezione 8) |

I file prodotti dalle skill (pptx, mp4, png) non vanno nel repo. Si caricano su SharePoint o OneDrive con il connettore, e la nota del progetto ne riporta il link. Il `.gitignore` esclude `*.pptx`, `*.mp4` e `*.png` in tutto il vault, tranne dentro `.claude/skills/` (dove stanno gli asset delle skill). Di conseguenza nemmeno le immagini incollate nelle note Obsidian entrano nel repo.

Prerequisito: lo script di setup dell'ambiente cloud installa le dipendenze delle skill (es. `python-pptx`) e `pyyaml` per il controllo del vault.

## 11. Workflow git

- All'avvio di ogni sessione, in cloud e in locale, l'hook `SessionStart` `.claude/hooks/pull-inizio-sessione.sh` fa `git pull --rebase origin main`. Con modifiche non committate lo salta, se fallisce lo annulla: in tutti e due i casi lo segnala e la sessione lo rifà a mano.
- Le sessioni interattive (cloud e locali) e i task schedulati fanno commit e push direttamente su `main`, prima con `git pull --rebase`. Il cloud vede solo ciò che è su `main`: un commit locale non spinto, o spinto su un altro branch, per i task e le sessioni cloud non esiste.
- In caso di conflitto su `.state/ingest.json`, vince la versione con il watermark più avanzato. Gli altri conflitti si risolvono riapplicando la propria modifica sulla versione remota.
- Unica eccezione: il curator lavora su un branch `claude/` e apre una PR.
- Messaggi di commit: `ingest(sharepoint): 12 note aggiornate`, `session: <slug>`, `project(<slug>): <cosa>`.

## 12. Diario delle sessioni

- Fonte primaria: la skill `chiudi-sessione` (`/chiudi-sessione`), che scrive il diario (obiettivo, decisioni, file toccati, aperti) e spunta gli aperti dei diari precedenti chiusi nella sessione.
- Rete di sicurezza: un hook `Stop` in `.claude/settings.json` copia la trascrizione in `sessions/_raw/` (il percorso arriva all'hook come `transcript_path`).
- Retention: diari per sempre; trascrizioni grezze 30 giorni.
- Da verificare nello step 5: comportamento degli hook nelle sessioni cloud quando l'ambiente scade per inattività.

## 13. Piano di sviluppo

| Step | Contenuto | Criterio di accettazione |
|---|---|---|
| 1 | Struttura del vault, `CLAUDE.md`, `README.md`, template, `.state/ingest.json` vuoto | Una sessione cloud nuova legge `CLAUDE.md` e sa dove scrivere ogni tipo di nota |
| 2 | Agente `ingestor` e comandi `/ingest`, `/ingest-file` | `/ingest-file` su `BlueAge_CompanyProfile_v24.pdf` produce una nota conforme allo schema 4.2 |
| 3 | Primo caricamento a lotti (6.5) | Campione di 10 note per lotto approvato dall'utente |
| 4 | Task schedulati di ingestion, digest e riconciliazione | 3 giorni di run senza errori e senza doppioni |
| 5 | `/chiudi-sessione`, hook di sessione, bridge della cartella chat | Le sessioni della settimana compaiono in `sessions/` |
| 6 | Skill `blueage-deck` e `blueage-corso` snellita | Un deck generato in cloud e caricato su SharePoint |
| 7 | Agente `curator`, comando `/curator` e task `curator`; agente `librarian` | Prima PR di proposte ricevuta e valutata (curator: PR #14 del 25/10) |
| 8 | Obsidian sui dispositivi (clone e sincronizzazione git) | Il grafo è visibile su PC e telefono |
| 9 | Dashboard Cockpit, task `cockpit` e nota `home.md` | 3 giorni di aggiornamenti della dashboard senza errori; `home.md` leggibile in Obsidian con Tasks e Dataview |
| 10 | Fonte GitHub (5.4, 6.6) e task `ingest-github` | 3 giorni di run senza errori; il log di `parts-radar-sviluppo` riceve una riga per giorno di lavoro sul repo |

## 14. Decisioni aperte

- Sincronizzazione di Obsidian su mobile (step 8): da verificare il plugin git su mobile oppure un'alternativa.
- `blueage-animazioni` nel vault cloud: dipende dal rendering video nell'ambiente cloud.
- Retention delle trascrizioni grezze: 30 giorni, da rivedere dopo il primo mese.
