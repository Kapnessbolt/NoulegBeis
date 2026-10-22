# SPEC · Second Brain BlueAge (personale)

Versione 1.3 · 22/10/2026 · Owner: Lorenzo Curione

Questo file è la specifica di riferimento del vault. Ogni sessione Claude Code che costruisce o modifica il sistema parte da qui. Le modifiche alla specifica si fanno con una PR dedicata.

---

## 1. Scopo

Un second brain personale sulla knowledge BlueAge, gestito da un agente, che:

1. tiene organizzati i progetti su cui lavoro e le relative attività;
2. risponde a domande sulla knowledge BlueAge;
3. produce materiali BlueAge (deck, corsi) tramite skill;
4. ingerisce in automatico le novità da SharePoint, OneDrive e Outlook;
5. tiene un diario delle sessioni e propone nuove regole, skill, agenti e hook.

Utente unico. Nessun materiale sensibile: il repo è privato.

## 2. Architettura

| Componente | Scelta | Ruolo |
|---|---|---|
| Storage del vault | Repo GitHub privato (account personale) | Fonte di verità: markdown + configurazione Claude Code |
| Esecuzione | Claude Code in cloud (claude.ai/code) | Sessioni interattive da desktop, mobile e PC diversi |
| Automazione | Task schedulati cloud (claude.ai/code/routines) | Ingestion periodica, riconciliazione, curator |
| Fonti | Connettore Microsoft 365 (tenant blueage.it) | Lettura di SharePoint, OneDrive e Outlook; upload dei file prodotti |
| Visualizzazione | Obsidian (vault = clone del repo) | Lettura, grafo, cattura veloce |
| Documenti originali | Restano su SharePoint, OneDrive e Outlook | Nel repo vanno solo le note markdown che li citano |

Vincoli dell'ambiente cloud da rispettare:
- Ogni sessione parte da un clone nuovo. Tutto ciò che conta (regole, skill, agenti, hook, stato) deve essere committato.
- Il setup locale di Claude Code non arriva in cloud.
- `/plugin` non è disponibile: le skill stanno in `.claude/skills/`.
- Intervallo minimo dei task schedulati: 1 ora.

## 3. Struttura del vault

```
/
├── SPEC.md                  questa specifica
├── CLAUDE.md                istruzioni operative per ogni sessione
├── README.md                guida rapida per l'utente
├── .claude/
│   ├── settings.json        hook e permessi
│   ├── commands/            comandi manuali (sezione 8)
│   ├── agents/              agenti specializzati (sezione 9)
│   ├── scripts/             script di servizio (controllo del vault, 4.4)
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
│   └── attachments/<famiglia>.md   allegati senza corrispondente su SharePoint
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
| Task di ingestion | `sources/`, `journal/`, `.state/`, note nuove in `people/` (partecipanti delle mail), e in aggiunta (solo righe nuove) `## Interazioni recenti` di `people/*.md`, `projects/<slug>/<slug>-log.md` e le sezioni "Attività" di `projects/<slug>/<slug>.md` |
| Ingestion lanciata da una sessione interattiva (`/ingest`, `/ingest-file`) | Come il task di ingestion, più: creazione di note nuove in `clients/`, `topics/` e `inbox/`; righe nuove in `## Fonti` (o `## Interazioni recenti` per le persone) di quelle esistenti |
| Curator | `proposals/`, `sessions/` |
| Sessioni interattive | Ovunque |

Nei task schedulati l'ingestion crea le persone ma non clienti e temi: per questi scrive comunque il wikilink nella nota fonte e propone la creazione nel digest del giorno. Prima di creare una persona cerca una nota con la stessa email; se trova solo un nome simile, non crea e segnala il possibile doppione nel digest. I progetti non si creano mai in automatico.

## 4. Regole delle note

### 4.1 Convenzioni generali

- Lingua: italiano.
- Nomi file: slug minuscolo con trattini (`entrata-merci-manini.md`).
- Collegamenti: wikilink Obsidian `[[slug]]`. Lo slug è il nome del file senza `.md`, quindi la scheda di un progetto si chiama come la sua cartella (`projects/corso-ai-manini/corso-ai-manini.md`) e `[[corso-ai-manini]]` la apre. Ogni nota in `sources/` deve collegarsi ad almeno un progetto, cliente o tema, tramite i campi `projects`, `clients` e `topics` del frontmatter.
- Frontmatter YAML obbligatorio su ogni nota, con i campi del suo tipo (4.2).
- Una nota descrive, non copia: riassunto, punti chiave, numeri, decisioni, azioni. Per il dettaglio si legge l'originale tramite il connettore.

### 4.2 Schemi del frontmatter

**Documento (SharePoint, OneDrive, allegato)**
```yaml
---
type: source-doc
source: sharepoint          # sharepoint | onedrive | attachment
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
surface: cloud               # cloud | claude-ai
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

Lo script `python3 .claude/scripts/controlla-vault.py` verifica le note e stampa un rapporto in markdown (con `--indice` aggiunge l'elenco di progetti, clienti, persone e temi). Esce con codice 1 se trova errori.

| Livello | Cosa controlla |
|---|---|
| Errore | Frontmatter mancante o non valido; `type` sconosciuto o nella cartella sbagliata; campi del template mancanti; valori fuori dagli elenchi ammessi (es. `status`); nomi file non in slug; slug duplicati; scheda progetto con nome diverso dalla cartella; wikilink del frontmatter verso note inesistenti; fonti senza progetto, cliente o tema; stessa email su due persone; stessa `family`, `item_id` o `conversation_id` su due note; voci di `.state/ingest.json` che puntano a note inesistenti |
| Avviso | Campi non previsti dal template; wikilink nel testo verso note inesistenti; nomi quasi uguali nella stessa categoria (possibili doppioni); persone senza email; documenti SharePoint/OneDrive non registrati nello stato |

Quando si esegue:
- prima di ogni commit, da sessioni interattive e task: gli errori introdotti si correggono prima del push;
- nella riconciliazione settimanale (6.4), con l'esito nel digest;
- a richiesta con `/controlla`.

## 5. Perimetro delle fonti

### 5.1 SharePoint · `https://blueagesrl.sharepoint.com/sites/internal/`

| Libreria | Stato |
|---|---|
| Knowledge | Inclusa |
| SalesMarketing | Inclusa |
| Delivery | Inclusa |
| Shared Documents | Inclusa |
| SiteAssets | Esclusa (blocco appunti OneNote) |

Esclusioni in qualunque punto del percorso: cartelle `_originali`, cartelle `_sorgenti`.

Tipi di file processati: pdf, docx, pptx, xlsx, md, txt. Gli altri tipi generano solo una nota con i metadati.

### 5.2 OneDrive · cartella `BlueAge`

Prefisso: `https://blueagesrl-my.sharepoint.com/personal/lorenzo_curione_blueage_it/Documents/BlueAge/`.
Il resto di OneDrive è escluso.
La sottocartella `BlueAge/_chat/` riceve i riassunti delle chat di claude.ai (sezione 8).

### 5.3 Outlook · tutta la casella

La ricerca copre tutte le cartelle, comprese le Inviate.

Scartati sempre:
- mittenti `no-reply`, `noreply`, `notifications` e simili;
- notifiche di servizi (Teams, Azure, SaaS);
- newsletter e marketing.

Per le prime 2 settimane le mail scartate vanno elencate nel digest giornaliero, sotto "Scartate", per verificare il filtro.

## 6. Ingestion

### 6.1 Stato · `.state/ingest.json`

```json
{
  "sharepoint": { "watermark": "2026-10-22T04:50:00Z", "items": { "<driveId>/<itemId>": { "last_modified": "...", "note": "sources/..." } } },
  "onedrive":   { "watermark": "...", "items": {} },
  "outlook":    { "watermark": "...", "threads": { "<conversationId>": { "last_message": "...", "note": "sources/mail/..." } } },
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
6. Imposta `watermark` all'ultimo `lastModifiedDateTime` processato con successo. Se un file fallisce, il watermark non lo supera.
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

1. Knowledge
2. SalesMarketing
3. Delivery
4. Shared Documents
5. OneDrive/BlueAge
6. Outlook, ultimi 60 giorni

Dopo ogni lotto l'utente controlla un campione di note prima di passare al successivo. Al termine si inizializzano i watermark e si attivano i task schedulati.

## 7. Task schedulati

Orari in Europe/Rome, fuori dagli orari pieni per evitare i ritardi del sistema.

| Task | Quando | Connettori | Cosa fa |
|---|---|---|---|
| `ingest-sharepoint` | Ogni giorno alle 06:50 | Microsoft 365 | 6.2 su SharePoint e OneDrive |
| `ingest-outlook` | Ogni giorno alle 07:50 e alle 13:50 | Microsoft 365 | 6.3 |
| `digest` | Ogni giorno alle 08:10 | Nessuno | Scrive `journal/AAAA-MM-GG.md`: novità, attività in scadenza, decisioni |
| `reconcile` | Domenica alle 20:10 | Microsoft 365 | 6.4 |
| `curator` | Domenica alle 21:10 | Nessuno | Sezione 9.2 |
| `sessions-cleanup` | Il 1° del mese alle 06:10 | Nessuno | Cancella `sessions/_raw/` più vecchio di 30 giorni |

Ogni task:
- include solo i connettori che gli servono;
- ha un prompt autosufficiente che rimanda alla sezione pertinente di questa SPEC;
- fa push su `main` con rebase;
- registra l'esito nel digest del giorno ("OK" oppure gli errori).

## 8. Comandi manuali (`.claude/commands/`)

| Comando | Funzione |
|---|---|
| `/ingest [fonte] [da data]` | Esegue l'ingestion a richiesta. Senza argomenti esegue tutte le fonti dal watermark |
| `/ingest-file <url o nome>` | Ingerisce un singolo documento, anche fuori dal perimetro |
| `/oggi` | Agenda: attività in scadenza, novità dall'ultimo digest, progetti fermi da più di 14 giorni |
| `/progetto <nome>` | Stato completo di un progetto: attività, decisioni, fonti recenti |
| `/chiudi-sessione` | Scrive il diario della sessione in `sessions/` e fa commit e push |
| `/cattura <testo>` | Nota rapida in `inbox/` |
| `/smista` | Smista `inbox/` nei progetti e nei temi |
| `/controlla` | Controllo del vault (4.4): errori, possibili doppioni e indice per categoria, con le correzioni proposte |

**Chat di claude.ai nel vault.** Nella chat basta chiedere "salva il riassunto di questa chat nel mio OneDrive in BlueAge/_chat". Il connettore M365 carica il file, e l'ingestion lo trasforma in una nota di tipo `session` con `surface: claude-ai`.

## 9. Agenti (`.claude/agents/`)

### 9.1 `ingestor`

Esegue le sezioni 6.2–6.4. Usato dai task schedulati (modalità `schedulata`) e da `/ingest` e `/ingest-file` (modalità `interattiva`). Scrive solo nelle cartelle consentite alla sua modalità (sezione 3).

### 9.2 `curator`

Ogni settimana:
- legge `sessions/` dell'ultima settimana;
- individua pattern ricorrenti: correzioni ripetute, procedure manuali ripetute, domande senza risposta nel vault;
- scrive proposte in `proposals/AAAA-MM-DD-<slug>.md`, ognuna con motivazione, evidenze (link alle sessioni) e testo pronto (regola per `CLAUDE.md`, skill, agente o hook);
- apre una PR su un branch `claude/curator-AAAA-MM-DD`.

Il curator non modifica mai direttamente `CLAUDE.md`, `.claude/` o questa SPEC. Le modifiche entrano solo con il merge della PR da parte dell'utente.

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

I file prodotti dalle skill (pptx, mp4, png) non vanno nel repo. Si caricano su SharePoint o OneDrive con il connettore, e la nota del progetto ne riporta il link. Il `.gitignore` esclude `*.pptx`, `*.mp4` e `*.png` in tutto il vault, tranne dentro `.claude/skills/` (dove stanno gli asset delle skill). Di conseguenza nemmeno le immagini incollate nelle note Obsidian entrano nel repo.

Prerequisito: lo script di setup dell'ambiente cloud installa le dipendenze delle skill (es. `python-pptx`) e `pyyaml` per il controllo del vault.

## 11. Workflow git

- Le sessioni interattive e i task schedulati fanno commit e push direttamente su `main`, prima con `git pull --rebase`.
- In caso di conflitto su `.state/ingest.json`, vince la versione con il watermark più avanzato. Gli altri conflitti si risolvono riapplicando la propria modifica sulla versione remota.
- Unica eccezione: il curator lavora su un branch `claude/` e apre una PR.
- Messaggi di commit: `ingest(sharepoint): 12 note aggiornate`, `session: <slug>`, `project(<slug>): <cosa>`.

## 12. Diario delle sessioni

- Fonte primaria: `/chiudi-sessione`, che scrive il diario (obiettivo, decisioni, file toccati, aperti).
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
| 5 | `/chiudi-sessione`, hook di sessione, bridge `_chat` | Le sessioni della settimana compaiono in `sessions/` |
| 6 | Skill `blueage-deck` e `blueage-corso` snellita | Un deck generato in cloud e caricato su SharePoint |
| 7 | Agente `curator` e `librarian` | Prima PR di proposte ricevuta e valutata |
| 8 | Obsidian sui dispositivi (clone e sincronizzazione git) | Il grafo è visibile su PC e telefono |

## 14. Decisioni aperte

- Sincronizzazione di Obsidian su mobile (step 8): da verificare il plugin git su mobile oppure un'alternativa.
- `blueage-animazioni` nel vault cloud: dipende dal rendering video nell'ambiente cloud.
- Retention delle trascrizioni grezze: 30 giorni, da rivedere dopo il primo mese.
