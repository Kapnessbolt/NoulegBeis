# SPEC · Second Brain BlueAge (personale)

Versione 1.29 · 31/10/2026 · Owner: Lorenzo Curione

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
| Esecuzione | Claude Code in cloud (claude.ai/code) e in locale (app desktop, sessione aperta sulla cartella del vault sul PC) | Sessioni interattive: in cloud da desktop, mobile e PC diversi; in locale dal PC |
| Automazione | Task schedulati cloud (claude.ai/code/routines) | Ingestion periodica, riconciliazione, curator |
| Fonti | Connettore Microsoft 365 (tenant blueage.it) | Lettura di SharePoint, OneDrive e Outlook; upload dei file prodotti |
| Visualizzazione | Obsidian (vault = clone del repo) | Solo lettura: link, backlink, grafo, ricerca, attività; `home.md` come pagina iniziale. Sincronizzazione solo in pull con il plugin Obsidian Git, niente commit dai dispositivi: modifiche e catture passano da Claude |
| Riepilogo | Cockpit: pagina HTML statica e autosufficiente su claude.ai (artifact privato), generata dal vault da `cockpit.py` (4.4) e ripubblicata dal task `cockpit` (7) | Briefing in sola lettura, da telefono e da PC: eventi dei prossimi 7 giorni (fotografia del calendario Outlook presa dal task), attività scadute e in scadenza, progetti con semaforo e prossimi passi; il dettaglio si apre con un tocco, il resto (inbox, novità, task) in fondo. Nessuna funzione in early access: la pagina contiene i suoi dati. `home.md` in Obsidian è la vista di riserva |
| Documenti originali | Restano su SharePoint, OneDrive e Outlook | Nel repo vanno solo le note markdown che li citano |

### 2.1 Configurazione e motore

Il vault ha due parti. Il **motore** (`.claude/`: script, agenti, routine, comandi, regole di cartella, template, hook) è uguale per ogni vault e non contiene valori di questo. La **configurazione** (`vault.yaml` alla radice) contiene tutto ciò che distingue questo vault: utente e organizzazione, fuso e lingua, fonti con perimetro ed esclusioni (5), finestra e filtri di scarto della posta (5.3, 6.3), parametri del rilevatore di riordino e ordine delle posizioni canoniche (6.2, 6.4), nomi dei server del connettore, repository di progetto (5.4), task schedulati con orari, giorni, modello e connettori (7), nomi delle sezioni che gli script leggono. La sezione `agenti` dice quali strumenti dei connettori ha ogni agente: `config.py applica` ne ricava la riga `tools` degli agenti e i permessi di `.claude/settings.json`, che non si modificano a mano. `applica` non è tra i permessi automatici, perché riscrive i permessi: si lancia solo con l'ok dell'utente. Gli script la leggono con il modulo `config.py`; agenti, routine e comandi con `python3 .claude/scripts/config.py` (`oggi`, `ora`, `valore <chiave>`, `task`), al posto di date e valori scritti nel testo. Le note e la knowledge (clienti, temi, persone, skill `blueage-*`) non sono né motore né configurazione: sono il contenuto del vault.

Questa SPEC descrive le regole e, finché lo step 14 non decide la fonte unica, ripete in prosa perimetro (5) e task (7). Gli orari dei task stanno in tre posti, `vault.yaml`, la tabella di 7 e l'interfaccia di claude.ai: il controllo del vault (4.4) dà errore se `vault.yaml` e la tabella di 7 divergono; i task di claude.ai si cambiano a mano.

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
- Il connettore Microsoft 365 ha un nome di server diverso per ambiente (`Microsoft_365` nelle sessioni cloud, `Microsoft-365` nei task schedulati, l'id del connettore nelle sessioni locali). I nomi stanno in `vault.yaml` (`connettori`); `python3 .claude/scripts/config.py applica` li riscrive nei permessi di `.claude/settings.json` e nei `tools` degli agenti `ingestor` e `librarian`. Un nome nuovo va aggiunto in `vault.yaml` e applicato, altrimenti la modalità Auto blocca le letture e l'ingestor parte senza connettore. Il controllo del vault (4.4) segnala come errore i nomi che non coincidono con `vault.yaml`.
- I task schedulati restano in cloud qualunque sessione si usi.

## 3. Struttura del vault

```
/
├── SPEC.md                  questa specifica
├── CLAUDE.md                istruzioni operative per ogni sessione
├── vault.yaml               configurazione del vault (2.1): perimetro, connettori, task, fuso, lingua, sezioni
├── .github/workflows/       controllo del vault su ogni push (4.4)
├── .githooks/pre-commit     controllo del vault prima di ogni commit (4.4)
├── .gitattributes           merge driver `stato` per i file di `.state/` (6.1, 11)
├── README.md                guida rapida per l'utente
├── home.md                  vista Obsidian con Tasks e Dataview (fuori dal controllo 4.4)
├── .claude/
│   ├── settings.json        hook e permessi (i permessi dei connettori generati da `vault.yaml`)
│   ├── setup/               script di setup dell'ambiente cloud (`ambiente-cloud.sh`)
│   ├── commands/            comandi manuali (sezione 8)
│   ├── agents/              agenti specializzati (sezione 9)
│   ├── hooks/               hook di Claude Code (controllo prima del commit 4.4, pull all'avvio 11)
│   ├── routines/            procedure dei task schedulati (sezione 7)
│   ├── rules/               regole di cartella (4.1): `fonti.md` per `sources/`, caricata quando una sessione legge o modifica una nota lì
│   ├── templates/           template della pagina Cockpit (`cockpit.html`, 4.4)
│   ├── scripts/             script di servizio testati (4.4): configurazione, controllo, rinomina e spostamento delle note (`rinomina-nota.py`, `sposta-nota.py`), famiglia, perimetro, stato, riconciliazione (`riconcilia.py`, 6.4), filtri di scarto della posta (`scarta.py`, 5.3), anomalie dei giri (`anomalie.py`), note dal template, ricerca (9.3), dati della dashboard e del digest (`plancia.py`, 7)
│   └── skills/              skill (sezione 10): `chiudi-sessione`, `blueage-deck`, `blueage-corso`, `blueage-animazioni`
├── .state/                  stato dell'ingestion, un file per fonte (6.1)
│   ├── sharepoint.json
│   ├── onedrive.json
│   ├── outlook.json
│   ├── github.json
│   └── reconcile.json
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
│   └── _raw/                estratti di trascrizione, solo il pezzo che serve
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
- Dove stanno le regole: `CLAUDE.md` contiene ciò che serve prima di scrivere (dove va una nota, chi scrive dove, dati riservati, git) e arriva in ogni sessione e in ogni subagente; ciò che serve solo mentre si scrive in una cartella sta in `.claude/rules/<nome>.md` con il frontmatter `paths:`, che Claude Code carica quando la sessione legge o modifica un file corrispondente (Read, Write, Edit, `cat` o `head` di un file via Bash; non Glob, Grep, script o redirezioni). Oggi `fonti.md` per `sources/**` (4.3). Una regola a percorso arriva dopo la prima operazione nella cartella, una sola volta per sessione, e dopo la compattazione del contesto non torna (test del 29/10: nessuna reiniezione alle letture successive, anche su file diversi; `CLAUDE.md` e le regole senza `paths:` invece vengono reiniettati): ciò che deve valere sempre resta in `CLAUDE.md`. Agenti, routine e comandi non rileggono `CLAUDE.md` e rimandano alle sue sezioni invece di copiarle (13.1, step 14).

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
versions:                    # dalla più recente; la prima voce è la current
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

Corpo: `## Cos'è`, `## Punti chiave`, `## Dove è usato`, `## Fonti`. Facoltativa, per un prodotto o un'offerta che ha una versione interna usata come banco di prova (oggi `second-brain`, con questo vault): `## Versione personale e banco di prova`, prima di `## Fonti`, con quello che funziona e i limiti trovati, ogni punto con la fonte.

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
- La nota punta sempre all'ultima versione (`current`) e tiene lo storico in `versions`, dalla più recente, con la `current` come prima voce (4.2). `versions` lo scrive solo `aggiorna-nota.py`: `--nuova-versione` per una nuova corrente; `--versione name=... item_id=... last_modified=...` per registrare un ID superato dello stesso documento (un file ricaricato o una copia sparita, il cui ID resta nello stato, 6.4); `--versioni-in-ordine` per rimettere la `current` in testa e le altre voci per `last_modified` decrescente, senza doppioni (`--versione` lo applica da sé); `--togli-versione <item_id>` solo per un ID refuso, mai esistito alla fonte, dopo averlo tolto dallo stato con `stato.py rimuovi-voce` (6.1). Un ID superato vero resta in `versions`.
- Quando arriva una nuova versione, il riassunto si rigenera e le differenze rilevanti vanno nel `<slug>-log.md` del progetto collegato.
- Una nuova versione non si propaga da sola alle note hub che la citano (temi, clienti, progetti): il loro testo resta quello della versione precedente con la fonte apparentemente valida. Per questo, a ogni nuova versione, l'ingestor scrive in ogni hub che cita la fonte una riga `- Da rileggere dopo [[<slug-fonte>]] v<N> del AAAA-MM-GG` (in `## Fonti`, oppure in coda a `## Punti chiave` dove `## Fonti` non c'è). Le hub con una riga «Da rileggere» da più di 7 giorni le elenca `plancia.py --anomalie` (regola e soglia in `anomalie.py`, 4.4) e il task `digest` le copia in `## Decisioni` (7); il curator ne riporta i numeri nelle metriche del resoconto (9.2). La rilettura la fa una sessione interattiva: aggiorna i punti della hub e toglie la riga; l'avviso del controllo (4.4, «nota più vecchia di una fonte che cita») sparisce con essa. La riscrittura automatica dei punti chiave da parte di un task è rimandata al prodotto (decisione del 31/10, `proposals/2026-10-31-audit-ingestion.md` §6).
- La regola operativa (percorso, famiglia, collegamenti, versioni, con gli script che li calcolano) è `.claude/rules/fonti.md`, caricata quando la sessione tocca `sources/` (4.1); l'agente `ingestor` la ripete nella sua procedura.

### 4.4 Controllo del vault

Lo script `python3 .claude/scripts/controlla-vault.py` verifica le note (tranne `README.md`, `CLAUDE.md`, `SPEC.md` e `home.md`) e stampa un rapporto in markdown (con `--indice` aggiunge l'elenco di progetti, clienti, persone e temi, con il numero di note che li collegano). Esce con codice 1 se trova errori.

| Livello | Cosa controlla |
|---|---|
| Errore | **Integrità**: wikilink (nel frontmatter o nel testo) verso note inesistenti; wikilink con percorso o estensione; slug duplicati; voci dello stato (`.state/<fonte>.json`) che puntano a note inesistenti, file di stato illeggibili. **Tracciabilità**: punti senza fonte nelle sezioni elencate in 4.1; fonti senza progetto, cliente o tema. **Schema**: frontmatter mancante o non valido; `type` sconosciuto o nella cartella sbagliata; campi del template mancanti; valori fuori dagli elenchi ammessi; nomi file non in slug; scheda progetto con nome diverso dalla cartella. **Doppioni certi**: stessa email su due persone; stessa `family`, `item_id` o `conversation_id` su due note. **Configurazione**: `vault.yaml` illeggibile o non valido (2.1); orari, giorni o task diversi tra `vault.yaml` e la tabella di 7; nomi del server Microsoft 365 nei `tools` degli agenti `ingestor` e `librarian` e nei permessi di `.claude/settings.json` diversi da quelli di `vault.yaml`, o con uno strumento in lettura mancante (2). **Regole**: file di `.claude/rules/` con il frontmatter illeggibile o `paths` non valido (Claude Code li caricherebbe in ogni sessione, 4.1). **Stato ↔ note ↔ fonti**: `riconciliazione_dovuta` illeggibile o dovuta da più di 7 giorni (6.2, passo 7); cartella della nota diversa da quella che `perimetro.py` calcola dal suo `current.web_url` (la nota non ha seguito il file, 6.4). Gli errori sullo stato non bloccano il pre-commit `--modificati`: fermare il giro che scrive lo stato perderebbe le sue note; restano nel rapporto, in CI e nel digest. **Dati riservati** (CLAUDE.md §5), solo nel corpo delle note e non nel frontmatter: IBAN, telefoni italiani (`+39` e cellulari, esclusi importi, ore e percentuali), chiavi e token con prefisso noto (`sk-`, `ghp_`, `github_pat_`, `xox?-`, `AKIA`, JWT) o stringhe esadecimali e base64 di 40+ caratteri, GUID (tranne i nomi di server MCP già in `.claude/settings.json`), ID e passcode di riunione, password in chiaro (`password: valore`); il messaggio dice la categoria e la riga, del valore al massimo i primi 4 caratteri |
| Avviso | Note orfane (persone, clienti, temi che nessuna nota collega); note che citano una fonte rimossa; note più vecchie di una fonte che citano (la fonte è stata aggiornata dopo); note `da-verificare`; nomi quasi uguali nella stessa categoria (possibili doppioni); persone senza email; campi non previsti dal template; documenti SharePoint, OneDrive e GitHub non registrati nello stato; regole di `.claude/rules/` con un pattern verso una cartella inesistente. **Stato ↔ note ↔ fonti** (6.1, 6.4): riconciliazione dovuta da più di 1 giorno; watermark fermo, cioè più di 2 giorni dietro il risultato più recente dell'ultimo giro con risultati (`ultimo_giro`), con la causa (file falliti, oppure regola del passo 6 di 6.2 non applicata); voce dello stato il cui ID non compare né in `current`, né in `versions`, né in `also_at` della nota a cui punta; `family` della nota diversa da quella che `famiglia.py` calcola dal `current.name`, salvo il prefisso di disambiguazione; nota con più voci nello stato senza le `versions` o le `also_at` corrispondenti; nota `source-doc` con `versions` vuoto o con la prima voce diversa dalla `current` (per GitHub, dove l'`item_id` è lo stesso per tutte le versioni, anche un `last_modified` diverso), con il comando che la riallinea (`aggiorna-nota.py <nota> --versioni-in-ordine`, 4.3); documenti con lo stesso nome in cartelle diverse registrati su note diverse (candidati alla stessa nota, 6.4) |

Le regole e le soglie della riconciliazione dovuta, del watermark fermo e delle voci orfane stanno solo nel modulo `anomalie.py`, che le condivide con `plancia.py --anomalie` (le righe del digest, 7): il controllo ne fa errori e avvisi del rapporto, il digest anomalie dei giri, e le due viste non possono divergere. Lo stesso modulo tiene la regola delle hub da rileggere (4.3), che vede solo il digest.

Quando si esegue:
- **prima di ogni commit**: il pre-commit di git `.githooks/pre-commit` lancia lo script con `--modificati` e blocca il commit se ci sono errori che toccano i file modificati, compresi i collegamenti rotti da una nota cancellata o rinominata. Gira dentro `git commit`, quindi vede anche i file creati nello stesso comando. Si attiva con `git config core.hooksPath .githooks`: nelle sessioni Claude Code lo fa l'hook `SessionStart` di `.claude/settings.json`. Sui dispositivi con Obsidian non serve, perché da lì non parte nessun commit (2). L'hook `PreToolUse` `.claude/hooks/controllo-pre-commit.sh` resta come primo filtro sui comandi `git commit`. Vale per sessioni interattive e task schedulati;
- **su ogni push e PR**: il workflow `.github/workflows/controllo-vault.yml` lo esegue su GitHub, così si vedono anche gli errori dei commit fatti fuori dalle sessioni (per esempio dal web di GitHub);
- **test degli script in CI**: prima del controllo lo stesso workflow esegue `python3 -m pytest .claude/scripts/tests -q`, i test di tutti gli script di servizio (sotto) su un mini-vault di prova (gli script leggono la radice dalla variabile `VAULT_ROOT`); se un test fallisce la CI è rossa. Dopo i test lo stesso workflow esegue i golden test sul vault reale, `perimetro.py --verifica` e `famiglia.py --verifica`: un accordo sotto la soglia dello script è CI rossa, perché un disaccordo tra ciò che gli script calcolano e ciò che le note registrano è il punto in cui una riconciliazione sbaglia cartella o famiglia (6.4). Soglie: `perimetro.py` 90%, `famiglia.py` 95% sull'accordo con il prefisso di disambiguazione;
- nella riconciliazione settimanale (6.4), con l'esito nel digest;
- a richiesta con `/controlla`.

**Script di servizio** (`.claude/scripts/`, step 12 di 13.1). Il codice fa la meccanica, il modello il giudizio: l'agente `ingestor` chiama questi script invece di applicare a mano le regole, e scrive solo riassunti, collegamenti, attività e log. Ognuno ha `--help`, argomenti espliciti, output JSON con `--json` dove il risultato è strutturato, nessuna domanda interattiva, codice di uscita diverso da 0 in caso di errore, ed è coperto dai test in `.claude/scripts/tests/`.

| Script | Cosa fa |
|---|---|
| `config.py` | Legge e valida `vault.yaml` (2.1) per gli altri script; da riga di comando data e ora nel fuso del vault, un valore, i giri attesi del giorno, `verifica` e `applica` (permessi dei connettori in `settings.json` e nei `tools` degli agenti) |
| `controlla-vault.py` | Controllo del vault (questa sezione) |
| `rinomina-nota.py` | Rinomina una nota, aggiorna wikilink e stato (4.1) |
| `famiglia.py` | Chiave di famiglia da un nome di file (4.3), slug di un testo o dell'oggetto di una mail, ricerca delle note della stessa famiglia (`--cerca`), golden test sulle famiglie del vault (`--verifica`, accordo minimo 95% con il prefisso di disambiguazione, in CI) |
| `perimetro.py` | Dentro o fuori perimetro da un `webUrl` (5.1-5.2) e cartella della nota, scorrendo la lista ordinata di prefissi `posizioni` di `config.perimetro()` (una voce per libreria di SharePoint e per la cartella di OneDrive, poi i riconoscitori fuori perimetro; vince il primo prefisso che apre l'URL); golden test sulle cartelle del vault (`--verifica`, accordo minimo 90%, in CI); `--profondita <elenco.json>` misura la profondità del rilevatore «fino alla prima cartella con file» per libreria su un elenco nel formato di `riconcilia.py --elenco` e stampa lo snippet per `fonti.rilevatore.profondita` (6.2, passo 7; 13.1, step 18). La cartella di un progetto software non si vede dall'URL e resta all'agente |
| `stato.py` | Lettura e scrittura dello stato (6.1) con validazione degli istanti e dei percorsi; indice inverso nota → voci (`voci`, `indice`) e regola dell'identità di 6.4 (`trova` per nome, famiglia e cartella; `collega` per una voce nuova sulla stessa nota; `set-assente` per il conteggio delle assenze); fotografia delle cartelle e segnale di riconciliazione dovuta (6.2, passo 7: `set-cartelle`, `set-riconciliazione-dovuta` per gli ID nuovi, `set-riconciliata`); registro del giro e watermark calcolato dal giro (6.2, passo 6); `rimuovi-voce` per i refusi (6.1); migrazione dal vecchio file unico; merge driver dei conflitti con l'unione per campo (6.1, 11) |
| `sposta-nota.py` | Unico modo per spostare o rinominare una nota `source-doc` di SharePoint o OneDrive quando il documento cambia posizione o nome (6.4): cartella da `perimetro.py` sul nuovo `webUrl` (fuori perimetro: non tocca niente ed esce con 1), file spostato e aggiunto a git, `current.web_url`, `name` e, se passati, `item_id`, `uri` e `last_modified`; `family` e slug se cambiano (chiama `rinomina-nota.py`, che aggiorna wikilink, `family` e stato); le voci dello stato che puntavano al percorso vecchio passano al nuovo e, se `--item-id` o `--uri` danno una chiave nuova, voce nuova sulla stessa nota come `stato.py collega` (le vecchie restano, 6.1). Idempotente: ripetuto con gli stessi argomenti non cambia niente, e se la nota è già stata spostata la ritrova per slug o per `current.web_url`. Niente commit. Lo usano la riconciliazione, il rilevatore e le sessioni, mai `git mv` o `rinomina-nota.py` a mano |
| `riconcilia.py` | Piano di riconciliazione (6.4) in JSON dal confronto tra l'elenco delle cartelle letto dal connettore e stato e note, con la regola dell'identità e la cartella canonica; `--applica` esegue la parte meccanica con `sposta-nota.py`, `aggiorna-nota.py` e `stato.py`, voce per voce e in modo idempotente (ciò che è fatto si salta con `già fatto`, un errore su una voce non ferma le altre); `--piano <file>` salva il piano e, con `--applica`, riprende lo stesso piano (stessa impronta, meno di 24 ore) invece di ricalcolarlo, così una ripresa non conta due volte le assenze. Non tocca watermark, `riconciliazione_dovuta` né `reconcile.last_run` |
| `scarta.py` | Filtri di scarto della posta (5.3, 6.3 passo 2): con `--mittente` e `--oggetto` applica gli elenchi di `fonti.outlook` (mittenti, domini, oggetti); uscita 0 tieni, 1 scarta, 2 mittente non filtrabile (senza `@`) o configurazione non valida. Il resto del giudizio resta all'agente |
| `nuova-nota.py` | Nota nuova dal template del suo tipo, con il frontmatter validato come nel controllo; per `source-doc` completa `source`, `family`, `ingested_at` e `versions`; non sovrascrive |
| `aggiorna-nota.py` | Modifica il frontmatter di una nota esistente senza toccare il corpo: campi, aggiunte alle liste, posizioni in `also_at`, nuova versione (`current` in `versions`, 4.3), ID superati in `versions` (`--versione`), riordino con la `current` in testa (`--versioni-in-ordine`) e ID refusi tolti (`--togli-versione`), 4.3. Le righe dei campi invariati restano identiche |
| `cerca.py` | Ricerca nel vault (9.3): termini su titolo, frontmatter e corpo, filtri per tipo, cartella, progetto, cliente, tema, persona, data e tag; ordine per punteggio, poi backlink, poi data; `--collegamenti` (chi collega una nota) e `--nota` (scheda sintetica). Usato dal `librarian` e dai comandi `/oggi`, `/progetto`, `/cattura`, `/smista` |
| `plancia.py` | Dati del Cockpit (7) in JSON: progetti con attività, prossimi passi e scadute, attività, log, inbox, task del giorno con l'`ultimo_giro` per fonte (6.1), digest. Con `--anomalie` non scrive file e stampa le righe del digest (7), con le regole di `anomalie.py`: giri mancanti o in errore di oggi e di ieri (ieri fino alle 23:59, così il digest del mattino vede la giornata intera), watermark fermo, riconciliazione dovuta da più di 1 giorno, stato illeggibile, voci orfane come conteggio, per `## Esito dei task`; hub con una riga «Da rileggere» da più di 7 giorni (e il numero di quelle più recenti) per `## Decisioni` (4.3). Con `--json` gli stessi dati e i `conteggi` (9.2) |
| `nota.py`, `anomalie.py` | Moduli condivisi, non comandi. `nota.py`: schema del frontmatter dal template, validazione, lettura e scrittura nello stile del vault, per `nuova-nota.py` e `aggiorna-nota.py`. `anomalie.py`: regole e soglie delle anomalie dell'ingestion (riconciliazione dovuta, watermark fermo, voci orfane, hub da rileggere, giri anomali), funzioni pure usate da `controlla-vault.py` e da `plancia.py --anomalie` |
| `cockpit.py` | Pagina HTML del Cockpit dai JSON di `plancia.py` e da `calendario.json` (scritto dal task con il connettore), con il template `.claude/templates/cockpit.html`; nessuna risorsa esterna; stampa la riga di riepilogo per il digest |

Prefissi ed esclusioni del perimetro, tipi processati, parametri del rilevatore (`fonti.rilevatore`, con la profondità per libreria), ordine delle posizioni canoniche (`fonti.canoniche`), finestra della posta ed elenchi di scarto (`fonti.outlook`), fuso, task attesi e nomi delle sezioni li prendono da `vault.yaml` (2.1, step 13), tramite `config.py` (`perimetro()`, `rilevatore`, `profondita()`, `canoniche()`, `rango_canonico()`, `outlook`), che li valida.

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
- cartelle `old versions` (es. `99 - old versions`): versioni superate, che la cartella tiene accanto all'ultima;
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

Gli elenchi di scarto sono configurazione: `fonti.outlook` di `vault.yaml` (`mittenti_scartati`, oggi `no-reply`, `noreply`, `notifications` e simili; `domini_scartati`; `oggetti_scartati`), letti con `config.py outlook`. Li applica `scarta.py --mittente "<mittente>" --oggetto "<oggetto>"` (4.4): uscita 0 tieni, 1 scarta, 2 mittente non filtrabile (un indirizzo senza `@`, come quelli X500 di Exchange), che l'agente giudica da sé.

Sulle mail che lo script tiene, l'agente scarta ancora:
- notifiche di servizi (Teams, Azure, SaaS);
- newsletter e marketing;
- thread personali o estranei a BlueAge (`CLAUDE.md` §5); in una sessione interattiva si chiede prima di scartarli.

Ogni scarto si annota (mittente · oggetto). Fino al 6/11/2026 (prime 2 settimane dall'attivazione) le mail scartate vanno elencate nel digest giornaliero, sotto "Scartate", per verificare il filtro.

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

### 6.1 Stato · `.state/<fonte>.json`

Un file per fonte, così due task che lavorano su fonti diverse non toccano lo stesso file. Ogni file ha il contenuto che prima aveva la sua chiave nel file unico:

```jsonc
// .state/sharepoint.json (uguale .state/onedrive.json); "assente" è facoltativo (6.4)
{ "watermark": "2026-10-22T04:50:00Z", "items": { "<driveId>/<itemId>": { "last_modified": "...", "note": "sources/...", "assente": 1 } },
  "cartelle": { "<driveId>": { "libreria": "SalesMarketing", "profondita": 2, "istante": "...",
                               "elenco": { "<folderId>": "<percorso relativo alla libreria>" } } },
  "riconciliazione_dovuta": { "<libreria>": "<istante del riordino rilevato>" },
  "ultimo_giro": { "inizio": "...", "fine": "...", "risultati": 0, "piu_recente": "...", "falliti": 0 } }
// .state/outlook.json
{ "watermark": "...", "threads": { "<conversationId>": { "last_message": "...", "note": "sources/mail/..." } },
  "ultimo_giro": { "inizio": "...", "fine": "...", "risultati": 0, "piu_recente": "...", "falliti": 0 } }
// .state/github.json
{ "repos": { "<owner>/<repo>": { "commit": "<sha di main letto>", "watermark": "<istante di quel commit>" } },
  "items": { "<owner>/<repo>:<percorso>": { "last_modified": "...", "commit": "<sha>", "note": "sources/github/..." },
             "<owner>/<repo>#<numero>":   { "last_modified": "<updated_at>", "note": "sources/github/..." } } }
// .state/reconcile.json
{ "last_run": "..." }
```

Regole:
- lo stato si legge e si scrive solo con `python3 .claude/scripts/stato.py` (`watermark`, `item`, `repo`, `elenco`, `voci`, `indice`, `trova`, `last-run`, `cartelle`, `riconciliazione-dovuta`; `set-item`, `collega`, `set-assente`, `set-watermark` anche con `--da-giro`, `set-repo`, `set-last-run`, `set-cartelle`, `set-riconciliazione-dovuta`, `set-riconciliata`, `set-giro`), mai a mano; `stato.py <comando> --help` descrive ogni comando;
- indice inverso nota → voci (sharepoint e onedrive): `voci <fonte> <nota>` stampa le voci che puntano a una nota, `indice <fonte>` tutto l'indice; `trova <fonte> [--nome] [--famiglia] [--cartella] [--libreria]` (almeno uno dei primi due) applica la regola dell'identità di 6.4 (note con lo stesso nome o la stessa famiglia, prima quelle della stessa cartella, poi della stessa libreria; una `family` con il prefisso di disambiguazione si ritrova dalla famiglia calcolata dai nomi, il solo suffisso non basta); `collega <fonte> <chiave nuova> --stessa-nota-di <chiave vecchia> --istante` scrive una voce nuova sulla stessa nota della vecchia, che resta;
- `assente` (sharepoint e onedrive, facoltativo) conta le riconciliazioni consecutive che non hanno trovato la voce: lo incrementa `set-assente <fonte> <chiave>`, lo toglie `set-assente --azzera` quando la nota è ritrovata, e anche `set-item` e `collega` lo tolgono dalla voce che scrivono, perché la voce è stata rivista. `status: removed` arriva al valore 2 (6.4);
- `riconciliazione_dovuta` (per libreria di SharePoint, o la cartella di OneDrive) la scrivono `set-cartelle`, quando il confronto delle fotografie dà un riordino, e `set-riconciliazione-dovuta <fonte> <libreria> --istante [--motivo]` per il segnale degli ID nuovi (6.2, passo 7); la toglie solo `set-riconciliata <fonte> <libreria>` a riconciliazione finita (6.4); una seconda fotografia identica non la consuma e un secondo riordino non ne sposta l'istante. `riconciliazione-dovuta <fonte>` la stampa, una riga per libreria;
- `ultimo_giro` lo scrive `set-giro <fonte> --inizio --fine --risultati --piu-recente --falliti` a fine ricerca (sharepoint, onedrive, outlook): risultati e istante più recente di tutta la ricerca, anche dei risultati saltati, fuori perimetro o scartati, e i file o thread falliti della fonte. È il registro da cui `set-watermark --da-giro` calcola il watermark (6.2, passo 6) e da cui il controllo (4.4) e `plancia.py` vedono un giro che non ha visto tutto;
- istanti nel formato `AAAA-MM-GGTHH:MM:SSZ`, `note` è un percorso relativo dentro `sources/`;
- il watermark non scende mai: un valore più vecchio si ignora con un avviso (`--forza` solo per correggere a mano);
- le voci non si cancellano (6.4): una nota rimossa ha `status: removed` e la sua voce resta. L'unica eccezione è `rimuovi-voce <fonte> <chiave> --motivo "<testo>"`, solo per una chiave che non è mai esistita alla fonte (un refuso di un riallineamento a mano, provato dalla storia git o dal connettore), mai per un documento sparito: `--motivo` è obbligatorio e finisce nell'uscita con la voce tolta, e il comando rifiuta (esce con 1 senza scrivere) una chiave che non c'è, che punta a una nota inesistente o che è l'ID corrente della nota (`current.item_id`, per la posta `conversation_id`). Dopo, l'ID si toglie anche da `versions` con `aggiorna-nota.py --togli-versione` (4.3);
- scrittura atomica, JSON con indentazione 2 e chiavi ordinate, perché i diff restino leggibili;
- conflitti git: merge driver `stato` (`.gitattributes`: `.state/*.json merge=stato`; il comando `python3 .claude/scripts/stato.py merge-driver %O %A %B` lo registra nel clone l'hook `SessionStart`). Il watermark e `last_run` più avanzati vincono; `items`, `threads` e `repos` si uniscono, salvo una voce di `items` o `threads` tolta da un lato con `rimuovi-voce` e lasciata uguale alla base dall'altro: quella resta tolta (se l'altro lato l'ha cambiata, la voce torna, perché non era un refuso). Per la stessa chiave di `items` e `threads` l'unione è campo per campo: `last_modified` e `last_message` il più recente; `note` e `assente` dal lato che li ha cambiati rispetto alla base (cambiati da entrambi: il lato con l'istante più recente, a parità il nostro; per `assente` vince chi l'ha tolto, perché la nota è stata ritrovata); `commit` e gli altri campi dal lato con l'istante più recente, a parità da chi li ha cambiati. Così uno spostamento della nota non si perde contro una versione nuova registrata dall'altro lato. Per i repo vince la voce con il watermark più recente, a parità quella cambiata rispetto alla base; per `cartelle` vince, drive per drive, la fotografia più recente; `riconciliazione_dovuta` si unisce (tutte le librerie dei due lati, per la stessa libreria l'istante più vecchio: se un lato toglie il segnale mentre l'altro scrive lo stesso file, il segnale torna e costa una riconciliazione in più, ma non si perde mai); per `ultimo_giro` vince quello con la `fine` più recente. Se il driver non è registrato o un file non si legge, il rebase si ferma e `stato.py risolvi` applica la stessa unione dagli stadi dell'indice (11).

### 6.2 Algoritmo del delta (documenti)

1. Leggi il `watermark` della fonte.
2. Chiama `sharepoint_search` con `query: "*"` e `afterDateTime = watermark − finestra` (`fonti.rilevatore.finestra_ore` di `vault.yaml`, oggi 48 ore; `config.py rilevatore`). Scorri tutte le pagine. La sovrapposizione recupera i file che l'indice di ricerca restituisce in ritardo: il 31/10 cinque file caricati il pomeriggio prima, durante un riordino, non comparivano ancora la mattina dopo, mentre il watermark era già oltre. I file già registrati con lo stesso `last_modified` si saltano (passo 4), quindi la finestra larga costa solo la ricerca.
3. Tieni solo i risultati il cui `webUrl` rientra nel perimetro (sezione 5) e non contiene percorsi esclusi.
4. Per ogni file:
   - se `items[id].last_modified` è uguale a quello attuale, salta;
   - altrimenti leggi il contenuto con `read_resource`, individua la famiglia (4.3) e crea o aggiorna la nota.
5. Aggiorna i progetti, clienti e temi collegati (le righe nuove vanno in `<slug>-log.md`).
6. Registra il giro con `stato.py set-giro <fonte>` (6.1) e poi calcola il watermark con `stato.py set-watermark <fonte> --da-giro`: la regola la applica lo script, non l'agente. Senza file falliti il watermark sale al `lastModifiedDateTime` più recente tra tutti i risultati della ricerca, compresi quelli saltati perché invariati o fuori perimetro, così la finestra di ricerca non si allarga nei giorni in cui nel perimetro non cambia nulla; con file falliti l'agente passa l'istante dell'ultimo file riuscito prima del primo fallimento e il watermark non lo supera; un giro senza risultati lascia il watermark com'è; il watermark non scende mai e non va mai oltre il risultato più recente. Un watermark fermo dietro l'ultimo giro è un avviso del controllo (4.4).
7. **Rilevatore di riordino.** Gli spostamenti e le rinomine non cambiano la data di modifica dei file, quindi il delta non li vede (riordino del 30/10: 25 note con il percorso vecchio). Il rilevatore guarda le fonti di `fonti.rilevatore.fonti` (`sharepoint`, `onedrive`, `github`): quali sorvegliare lo sceglie il cliente all'installazione (13.1, step 18), e una fonte tolta dall'elenco resta coperta solo dalla riconciliazione settimanale. Due segnali, controllati a ogni giro su SharePoint e OneDrive:
   - **cartelle**: per ogni libreria del perimetro e per la cartella di OneDrive elenca con `read_resource` le cartelle fino alla profondità della libreria (`fonti.rilevatore.profondita` di `vault.yaml`, un valore per libreria perché le librerie hanno strutture diverse: `config.py rilevatore`), saltando le escluse, e salva la fotografia con `stato.py set-cartelle`, che la confronta con la precedente: cartelle nuove, sparite o con lo stesso ID e un percorso diverso sono un riordino, e lo script segna la libreria in `riconciliazione_dovuta` (6.1). La prima fotografia non fa scattare niente;
   - **ID nuovi**: almeno `fonti.rilevatore.soglia_id_nuovi` file dei risultati del passo 2 hanno un ID che lo stato non conosce ma una famiglia che esiste già nella stessa cartella (`famiglia.py --cerca`): la cartella è stata ricaricata (Velo-CE il 29/10, 68 note con ID nuovi). Lo registra `stato.py set-riconciliazione-dovuta <fonte> <libreria>` (6.1), con la stessa regola di `set-cartelle`.
   Un segnale non si consuma con il giro che lo rileva: la libreria resta in `riconciliazione_dovuta` finché la riconciliazione (6.4) non la chiude con `set-riconciliata`, e il digest ripete ogni giorno in `## Decisioni`, così come la stampa `stato.py riconciliazione-dovuta`, la riga `- Riconciliazione dovuta: <libreria> dal <data>`. Il giorno del rilevamento il digest riporta anche `- Riordino rilevato in <libreria | OneDrive>: <segnale>`. La riconciliazione ridotta delle librerie dovute la fa il task `reconcile-ridotta` (7) dopo il giro, non il giro stesso.
8. Commit e push su `main` (sezione 11).

Limite di lettura: oltre 30 pagine o slide, leggi le prime 30 e imposta `partial: true`.

### 6.3 Algoritmo del delta (posta)

1. Chiama `outlook_email_search` con `query: "*"` e `afterDateTime = watermark − finestra` (`fonti.outlook.finestra_ore` di `vault.yaml`, oggi 2 ore; `config.py outlook`). Scorri tutte le pagine (25 per pagina).
2. Filtri di scarto (5.3): `scarta.py` applica gli elenchi di `vault.yaml`; l'agente giudica il resto e annota ogni scarto.
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
7. Un thread che annuncia un riordino di SharePoint o OneDrive (cartelle spostate, rinominate, ricaricate) non fa niente da solo, perché il rilevatore (6.2, passo 7) se ne accorge dal giro dopo; se però arriva dopo il giro di `ingest-sharepoint` del giorno, il digest lo segnala in `## Decisioni` con `- Riordino annunciato: <libreria | OneDrive> · /ingest riconcilia sharepoint:<libreria> | onedrive · [[fonte]]`.
8. Registra il giro e calcola il watermark con `stato.py set-giro outlook` e `stato.py set-watermark outlook --da-giro` (6.2, passo 6), poi commit e push.

### 6.4 Riconciliazione

La riconciliazione è la rete di sicurezza del delta: ritrova i file che la ricerca non ha restituito e assorbe ciò che il delta non vede, perché spostamenti, rinomine, copie e ricaricamenti non cambiano la data di modifica dei file. Due forme:

- **completa**: settimanale (task `reconcile`, 7), su tutte le fonti;
- **ridotta**: una sola libreria di SharePoint o la cartella di OneDrive. La fa il task `reconcile-ridotta` (7) per ogni libreria in `riconciliazione_dovuta` (6.1): se non ce ne sono, il task finisce subito con la sola riga d'esito nel digest. A mano: `/ingest riconcilia sharepoint:<libreria>` o `/ingest riconcilia onedrive`.

In entrambe il codice fa la meccanica e il modello il giudizio: il piano lo prepara `riconcilia.py`, le note le sposta `sposta-nota.py` (4.4); l'agente `ingestor` legge dal connettore, esegue il piano e scrive i riassunti delle note nuove o cambiate.

**Identità di un documento.** Lo stato lega una nota all'ID dell'item (6.1), ma SharePoint non conserva l'ID nelle copie, nei ricaricamenti e nelle esportazioni. L'identità la decide quindi una regola, applicata dallo script e non dall'agente:

- un ID sparito dallo stato che ritrova nell'elenco un file con lo stesso nome o la stessa famiglia (`famiglia.py`) è la stessa nota (`stato.py trova`: prima i candidati della stessa cartella, poi della stessa libreria, poi del resto della fonte): voce nuova nello stato sulla stessa nota (la vecchia resta, 6.1) e, nella nota, una versione in `versions` se il file è lo stesso documento aggiornato, una posizione in `also_at` se è una copia (4.3);
- `status: removed` solo senza candidati, e solo se l'ID manca per due riconciliazioni consecutive: una ricerca o un elenco incompleti non devono rimuovere una nota;
- le voci dello stato non si cancellano: un ID superato resta nello stato e in `versions`; solo un ID refuso, mai esistito alla fonte, si toglie, con `stato.py rimuovi-voce` e poi `aggiorna-nota.py --togli-versione` (6.1, 4.3), e mai dalla riconciliazione;
- il controllo del vault (4.4) segnala i documenti con lo stesso nome in cartelle diverse registrati su note diverse, perché sono i candidati che la regola potrebbe aver mancato.

**Cartella canonica.** Quando lo stesso documento sta in più posti, quale copia è `current` lo decide l'ordine di `fonti.canoniche` in `vault.yaml` (librerie del sito del perimetro, OneDrive e gli altri siti del tenant, letti con `config.py canoniche()` e `rango_canonico()`): vince la posizione più alta nell'elenco, non l'ultima modificata, e le altre copie vanno in `also_at`. L'ordine è configurazione, non regola: un altro vault lo sceglie all'installazione (13.1, step 18). La nota sta nella cartella della copia `current` (`perimetro.py`).

**Procedura.**

1. L'agente elenca con `read_resource` le cartelle del perimetro della libreria (o di tutte, nella completa), saltando le escluse, e scrive l'elenco in un file JSON nello scratchpad: per ogni file ID, `webUrl`, nome e `lastModifiedDateTime`.
2. `riconcilia.py --elenco <file.json> --fonte <sharepoint | onedrive> [--libreria <nome>] --piano <file>` confronta l'elenco con lo stato e con le note, stampa il piano in JSON e lo salva in `--piano`, una voce per azione:
   - `sposta`: stesso ID, `webUrl` cambiato (file spostato o rinominato): `current.web_url` e `uri` nuovi; se cambia la cartella la nota segue il file nella `cartella_nota` di `perimetro.py`, se cambia la famiglia cambiano `family` e slug (con i wikilink, tramite `rinomina-nota.py`);
   - `nuova_voce`: ID nuovo con un candidato per nome o famiglia nella stessa cartella (regola dell'identità, `stato.py trova`): voce nuova nello stato sulla stessa nota, come versione (`diventa_current` per la più recente);
   - `copia`: ID nuovo con un candidato in un'altra cartella, o stesso documento in due posizioni: `current` sulla copia nella cartella canonica, l'altra in `also_at`;
   - `recupera`: file presente e mai ingerito, più vecchio del watermark (il watermark lo ha superato): si ingerisce come compito `file`, senza toccare il watermark; se è più recente del watermark lo prende il prossimo delta e il piano lo lascia `in_coda`. Con più candidati e nessuno con lo stesso nome (più note con la stessa famiglia), o più candidati con lo stesso nome, lo script non sceglie: la voce è `recupera` o `in_coda` con `candidati_ambigui`, e la nota la sceglie l'agente;
   - `rimuovi`: nota attiva nessuna delle cui voci è nell'elenco e che nessun candidato ritrova, quando il conteggio `assente` della sua voce corrente (6.1) arriva a 2: `status: removed`; alla prima riconciliazione che non la trova il piano la segna `in_attesa` (`assente` 1);
   - `azzera`: nota ritrovata con `assente` su qualche voce: il conteggio si toglie (`stato.py set-assente --azzera`).
3. `riconcilia.py --applica` con lo stesso `--piano` esegue la parte meccanica con `sposta-nota.py`, `aggiorna-nota.py` e `stato.py`, voce per voce e in modo idempotente: prima di ogni passo guarda lo stato attuale e salta ciò che è fatto, e un errore su una voce non ferma le altre. Se il file del piano contiene già il piano dello stesso elenco (meno di 24 ore), lo riprende invece di ricalcolarlo, così una riconciliazione interrotta (connettore, limite della sessione, push fallito) riparte da dove si era fermata senza contare due volte le assenze. All'agente restano le voci `recupera` (lettura e riassunto, e la scelta della nota tra i `candidati_ambigui`) e i riassunti delle note cambiate.
4. Controllo del vault (4.4) con il rapporto in `## Controllo del vault` del digest.
5. Esito nel digest del giorno, con i numeri del piano (`<n> note spostate, <m> rimosse, <k> recuperate`). Per ogni libreria (o la cartella di OneDrive) riconciliata fino in fondo, `stato.py set-riconciliata <fonte> <libreria>`; interrotta o parziale, il segnale resta e il task del giorno dopo la riprende. Solo la completa aggiorna `reconcile.last_run`.

Le note `fuori-perimetro` ingerite a richiesta con `/ingest-file` non stanno nello stato e la riconciliazione le ignora.

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
   File sparito da `main`: se `github` è tra le fonti del rilevatore (6.2, passo 7), prima di segnarlo `status: removed` guarda `git diff --name-status -M <commit vecchio>..<head>`. Se il file è stato spostato o rinominato (`R`), la nota lo segue: `current.uri` sul percorso nuovo, voce nuova nello stato con la stessa nota (la vecchia resta, 6.1) e una riga nel digest `- Da aggiornare: SPEC 5.4, <percorso vecchio> → <percorso nuovo>`, perché l'elenco dei file del perimetro sta qui.
3. **Changelog**: le voci nuove sono i titoli `## ` aggiunti tra `repos[repo].commit` e `head` (`git diff`). Per ogni giorno con voci nuove, **una** riga nel log del progetto con ciò che conta a livello di progetto (funzioni chiuse, decisioni, numeri, problemi aperti), senza dettagli tecnici, con fonte la nota del changelog. Le azioni che non sono codice (avvisi, richieste a clienti e fornitori, decisioni da prendere) vanno in `## Attività`. La nota del changelog tiene in `## Voci recenti` una riga per voce degli ultimi 30 giorni.
4. **Issue** del perimetro: se `updated_at` è uguale a `items[chiave].last_modified`, salta. Altrimenti rigenera la nota. Le caselle non spuntate dei passi fuori dal codice diventano attività del progetto, se non ci sono già; quelle spuntate nel repo che nel progetto risultano ancora aperte vanno nel digest, sotto `## Decisioni`, come `- Da spuntare: <attività> · [[fonte]]` (il task non modifica righe esistenti).
5. `repos[repo]` = `head` e il suo istante; aggiorna `items`. Digest, commit e push.

Senza clone o senza connettore GitHub il task non inventa nulla: scrive l'errore nel digest. Se manca solo il connettore, processa i file e salta le issue.

## 7. Task schedulati

Orari nel fuso del vault (`vault.yaml`, oggi Europe/Rome), fuori dagli orari pieni per evitare i ritardi del sistema. Questa tabella e `task` di `vault.yaml` devono coincidere su task, orari e giorni: il controllo del vault (4.4) dà errore se divergono.

| Task | Quando | Connettori | Modello | Cosa fa |
|---|---|---|---|---|
| `ingest-sharepoint` | Ogni giorno alle 06:50 | Microsoft 365 | Opus | 6.2 su SharePoint e OneDrive, con il rilevatore di riordino (passo 7), che lascia il segnale di riconciliazione dovuta |
| `ingest-outlook` | Ogni giorno alle 07:05 e alle 13:15 (due task) | Microsoft 365 | Opus | 6.3 |
| `digest` | Ogni giorno alle 07:45 | Nessuno | Sonnet | Completa `journal/AAAA-MM-GG.md`: novità, attività in scadenza, decisioni, progetti fermi; anomalie dei giri da `plancia.py --anomalie` in `## Esito dei task` e hub da rileggere in `## Decisioni` (4.3, 4.4) |
| `ingest-github` | Ogni giorno alle 07:20 | GitHub (il vault e i repo di 5.4 come sorgenti) | Opus | 6.6 |
| `reconcile` | Domenica alle 08:45 | Microsoft 365 | Sonnet | 6.4, completa |
| `reconcile-ridotta` | Ogni giorno alle 09:10 | Microsoft 365 | Sonnet | 6.4, ridotta: solo le librerie in `riconciliazione_dovuta` (una libreria per volta, nell'ordine di `fonti.canoniche`), con `riconcilia.py` e il suo `--piano`; ogni libreria finita si chiude con `set-riconciliata`, commit e push prima della successiva; senza segnale finisce subito con la riga d'esito |
| `cockpit` | Ogni giorno alle 07:40 e alle 13:40 (due task, `DailyBoard` e `DailyBoard2`) | Microsoft 365, solo lettura del calendario | Sonnet | Rigenera i dati con `plancia.py`, fotografa il calendario dei prossimi 7 giorni in `calendario.json`, genera la pagina con `cockpit.py` e la ripubblica sull'artifact Cockpit; riga d'esito nel digest |
| `curator` | Domenica alle 21:10 | GitHub, solo per aprire la PR | Opus | 9.2: proposte dai diari della settimana su un branch suo, con una PR |

Il `cockpit` legge il calendario con il connettore nel giro e lo scrive nella pagina: il Cockpit mostra la fotografia dell'ultimo giro, non il calendario dal vivo. Il `digest` gira dopo gli ingest del mattino; l'ingest-outlook delle 13:15 e il `reconcile-ridotta` delle 09:10 scrivono nel digest dello stesso giorno, e il digest del giorno dopo non ripete le loro note. Il `reconcile-ridotta` gira dopo `ingest-sharepoint` e separato da esso perché un riordino grande (una libreria intera) non allunghi il giro del delta oltre il limite della sessione: il delta lascia il segnale, la riconciliazione lo chiude.

Ogni task:
- si crea dall'interfaccia di claude.ai con il repository e i soli connettori che gli servono, e gira in una sessione nuova a ogni esecuzione;
- ha come prompt `Esegui il task descritto in .claude/routines/<task>.md, seguendo anche .claude/routines/_comune.md.`: la procedura sta nel repo e rimanda alla sezione pertinente di questa SPEC; le regole comuni (avvio, limiti, digest, errori, git) sono in `_comune.md`;
- esegue l'agente `ingestor` dentro la propria sessione, non come subagente;
- fa commit, poi `git pull --rebase` e push su `main`;
- registra l'esito nel digest del giorno ("OK" oppure gli errori), con l'ora nel fuso del vault.

Eccezione: il `curator` non scrive nel digest e non fa push su `main` (sezione 3). Lavora sul branch che la sessione del task gli assegna (`claude/<nome>`) e il suo esito è la PR; se non trova niente da proporre non apre la PR.

## 8. Comandi manuali (`.claude/commands/`)

| Comando | Funzione |
|---|---|
| `/ingest [fonte] [da data]` | Esegue l'ingestion a richiesta. Senza argomenti esegue tutte le fonti dal watermark. `/ingest riconcilia [sharepoint:<libreria> | onedrive]` esegue la riconciliazione (6.4), completa o ridotta a una libreria o alla cartella di OneDrive |
| `/ingest-file <url o nome>` | Ingerisce un singolo documento, anche fuori dal perimetro |
| `/oggi [giorni]` | Agenda del giorno, sola lettura: attività scadute, di oggi e entro N giorni (default 7) per progetto, progetti fermi da più di 14 giorni, inbox da smistare, novità dall'ultimo digest, esito dei task; dati da `plancia.py` e `cerca.py` |
| `/progetto <nome>` | Stato completo di un progetto, sola lettura: stato e decisioni, attività aperte per data, ultimi passi del log, fonti degli ultimi 30 giorni, persone, cose che non tornano (attività senza data, log fermo, note `partial`) |
| `/chiudi-sessione` | Scrive o aggiorna il diario della sessione in `sessions/`, spunta gli aperti dei diari precedenti chiusi nella sessione, poi commit e push. È una skill (sezione 10): parte anche quando l'utente chiude la sessione a parole |
| `/cattura <testo>` | Nota rapida in `inbox/AAAA-MM-GG-<slug>.md` con `nuova-nota.py`, il testo così com'è e `Contesto: [[slug]]` solo se certo; commit `inbox: cattura <slug>` senza chiedere conferma |
| `/smista [nota]` | Smista `inbox/` nei progetti (log e attività), clienti e temi: propone la tabella cattura → destinazione → testo, con il diario della sessione come fonte, e scrive solo dopo l'ok; i progetti nuovi li propone soltanto; commit `inbox: smistamento` |
| `/controlla` | Controllo del vault (4.4): errori, possibili doppioni e indice per categoria, con le correzioni proposte |
| `/verifica-task [task] [data]` | Verifica i giri dei task schedulati (7): riga nel digest o PR del curator, commit, watermark, note scritte, doppioni; propone le correzioni e gli aperti da spuntare |
| `/curator [da data] [a data]` | Giro del curator a mano (9.2), di default sugli ultimi 7 giorni: mostra le proposte, registra le decisioni dell'utente nel `status` e apre la PR |

Le domande sulla knowledge ("cosa sappiamo di X", "quando è stato deciso Y") non hanno un comando: la sessione le passa all'agente `librarian` (9.3), che risponde con le fonti.

**Chat di claude.ai nel vault.** Nella chat basta chiedere "salva il riassunto di questa chat nel mio OneDrive in BlueAge/00_chat". Il connettore M365 carica il file, e l'ingestion lo trasforma in una nota di tipo `session` con `surface: claude-ai`.

## 9. Agenti (`.claude/agents/`)

### 9.1 `ingestor`

Esegue le sezioni 6.2–6.4 e 6.6 (GitHub): la meccanica (perimetro, famiglia, frontmatter, versioni, stato) con gli script di servizio (4.4), il giudizio (riassunti, collegamenti, persone, attività, log) da sé. Usato dai task schedulati (modalità `schedulata`) e da `/ingest` e `/ingest-file` (modalità `interattiva`). Scrive solo nelle cartelle consentite alla sua modalità (sezione 3).

### 9.2 `curator`

Ogni settimana (task `curator` della domenica, o a mano con `/curator`):
- legge `sessions/` dell'ultima settimana, e per gli aperti anche i diari precedenti;
- individua pattern ricorrenti, presenti in almeno 2 diari (basta uno se il diario lo indica come spunto per il curator): correzioni ripetute, procedure manuali ripetute, domande senza risposta nel vault, decisioni prese caso per caso, aperti che restano aperti. Un comando o uno step previsti da questa SPEC ma non ancora fatti non contano come già coperti;
- scrive al massimo 5 proposte per giro in `proposals/AAAA-MM-DD-<slug>.md`, ognuna con motivazione, evidenze (link alle sessioni) e testo pronto (regola per `CLAUDE.md`, skill, agente o hook); gli altri pattern vanno in una riga ciascuno nella PR;
- segnala nella PR come "da verificare" i commit `session: <slug>` senza diario e i commit `vault:`, `project(<slug>)` e `spec:` che nessun diario dello stesso giorno o del giorno dopo cita (per slug o per file toccato);
- riporta nel resoconto una riga di metriche dai `conteggi` di `plancia.py --anomalie --json` (4.4): hub da rileggere, totali e da più di 7 giorni (4.3), riconciliazioni dovute, note con voci dello stato orfane, giri mancanti o in errore di oggi e di ieri; è la base delle metriche dello step 20 (13.1);
- spunta in `sessions/` gli aperti già chiusi altrove, con la prova in coda (`(chiuso in [[<diario o digest>]])`, `(chiuso: PR #n unita)`); quelli chiusi in parte o con prova incerta vanno nella PR come "da verificare";
- apre una PR da un branch suo: `claude/curator-AAAA-MM-DD` con `/curator`; nel task schedulato il branch che la sessione gli assegna (`claude/<nome>`), perché la sessione cloud può fare push solo lì e senza utente nessuno può autorizzarne un altro.

Le proposte restano in `proposals/` come registro: in revisione l'utente imposta `status` a `accettata` o `rifiutata`. Il curator non ripropone una proposta rifiutata se non ci sono evidenze nuove successive al rifiuto, e nella PR segnala le accettate non ancora applicate.

Il curator non modifica mai direttamente `CLAUDE.md`, `.claude/` o questa SPEC. Le proposte accettate le applica, dopo il merge, una sessione interattiva; quelle che toccano la SPEC con la loro PR dedicata.

### 9.3 `librarian`

Risponde alle domande sulla knowledge, in sola lettura (nessuna scrittura nel vault, nessun commit):
1. cerca nel vault con `cerca.py` (4.4): prima le note hub (progetto, cliente, tema, persona) e i loro collegamenti, poi le fonti citate dai punti che reggono la risposta;
2. se la nota non basta (un numero, il testo esatto, un allegato, una nota `partial`), legge l'originale con il connettore dai riferimenti del frontmatter (`current.web_url`, `conversation_id`, `current.item_id`) e lo dice; non riporta dati riservati (CLAUDE.md §5);
3. risponde in breve, con la fonte in coda a ogni affermazione `([[slug]])`, le date dei fatti e non dell'ingestion, le contraddizioni tra note con entrambe le versioni; se il vault non lo sa lo dice e indica dove potrebbe stare, senza inventare;
4. chiude con **Fonti** (note e documenti usati) e, se servono, **Lacune** (cosa manca nel vault, da ingerire o da catturare in `inbox/`).

Lo usano la sessione interattiva, per le domande di Lorenzo, e in prospettiva i comandi che hanno bisogno di una risposta con le fonti. Criterio dello step 17 (13.1): 10 domande di prova con risposta corretta e fonti citate.

## 10. Skill (`.claude/skills/`)

| Skill | Origine | Intervento | Stato |
|---|---|---|---|
| `chiudi-sessione` | Proposta del curator del 25/10 | Scritta nel vault: è `/chiudi-sessione` (sezione 8) | Nel vault |
| `blueage-deck` | Plugin claude.ai | Copiata così com'è | Nel vault (26/10) |
| `blueage-corso` | Plugin claude.ai | Snellita: `SKILL.md` breve con il flusso; i dettagli (COMPASS, RED TAG, Tocca a voi, kit docente) in file di riferimento caricati solo quando servono (`principi.md`, `cartella.md`, `linee_guida.md`, `compass.md`, `modelli.md`) | Nel vault (26/10) |
| `blueage-animazioni` | Plugin claude.ai | Copiata così com'è; il rendering video nelle sessioni cloud è da provare (14) | Nel vault (26/10) |

**Fonte unica.** Le skill stanno solo nel vault, che viaggia con il repo quando il Second Brain si condivide come strumento BlueAge: l'account claude.ai è personale e un plugin non si condivide. Il plugin claude.ai da cui sono nate le skill blueage è disattivato. Una modifica a una skill, anche di metodo (linee guida, COMPASS, style guide, generatore), si fa nel vault con un commit `vault:`; se un giorno servisse un plugin per la chat, è una copia generata dal vault, mai modificata a parte.

I file prodotti dalle skill (pptx, mp4, png) non vanno nel repo. Si caricano su SharePoint o OneDrive con il connettore, e la nota del progetto ne riporta il link. Il `.gitignore` esclude `*.pptx`, `*.mp4` e `*.png` in tutto il vault, tranne dentro `.claude/skills/` (dove stanno gli asset delle skill).

Prerequisito: lo script di setup dell'ambiente cloud installa le dipendenze delle skill (es. `python-pptx`), `pyyaml` e `pytest`. È committato in `.claude/setup/ambiente-cloud.sh`; nell'interfaccia di claude.ai lo script di setup dell'ambiente lo richiama. L'hook di avvio installa `pyyaml` se manca, come rete di sicurezza.

## 11. Workflow git

- All'avvio di ogni sessione, in cloud e in locale, l'hook `SessionStart` `.claude/hooks/pull-inizio-sessione.sh` fa `git pull --rebase origin main`. Con modifiche non committate lo salta, se fallisce lo annulla: in tutti e due i casi lo segnala e la sessione lo rifà a mano.
- Le sessioni interattive (cloud e locali) e i task schedulati fanno commit e push direttamente su `main`, prima con `git pull --rebase`. Il cloud vede solo ciò che è su `main`: un commit locale non spinto, o spinto su un altro branch, per i task e le sessioni cloud non esiste.
- I conflitti sullo stato (`.state/<fonte>.json`) li risolve il merge driver `stato` (6.1): vince il watermark più avanzato e le voci si uniscono. Se il rebase si ferma comunque su un file di stato: `python3 .claude/scripts/stato.py risolvi`, poi `git rebase --continue`. Gli altri conflitti si risolvono riapplicando la propria modifica sulla versione remota.
- Eccezioni: il curator lavora su un branch `claude/` e apre una PR (9.2); le modifiche a questa SPEC passano da una PR dedicata.
- Messaggi di commit:

| Prefisso | Chi | Esempio |
|---|---|---|
| `ingest(<fonte>)` | Ingestor, fonti `sharepoint`, `outlook`, `github` | `ingest(sharepoint): 3 note nuove, 12 aggiornate` |
| `ingest(riconcilia)` | Task `reconcile` | `ingest(riconcilia): 4 note aggiornate` |
| `ingest(file)` | Ingestor, compito `file` (`/ingest-file`) | `ingest(file): blueage-companyprofile` |
| `journal:` | Task `digest` (la sua finestra parte dall'ultimo commit `journal:`) | `journal: 2026-10-26` |
| `cockpit:` | Task `cockpit` | `cockpit: 2026-10-26 07:40` |
| `curator:` | Curator | `curator: 2026-10-25, 3 proposte` |
| `session:` | Diario di sessione (`/chiudi-sessione`) | `session: <slug>` |
| `project(<slug>)` | Sessione interattiva su un progetto | `project(<slug>): <cosa>` |
| `inbox:` | `/cattura` e `/smista` (8) | `inbox: cattura <slug>`, `inbox: smistamento` |
| `vault:` | Struttura e configurazione (`CLAUDE.md`, `.claude/`, template, `README.md`) | `vault: <cosa>` |
| `spec:` | PR dedicata alla SPEC | `spec: <cosa> (1.16)` |

## 12. Diario delle sessioni

- Fonte primaria: la skill `chiudi-sessione` (`/chiudi-sessione`), che scrive il diario (obiettivo, decisioni, file toccati, aperti) e spunta gli aperti dei diari precedenti chiusi nella sessione.
- Rete di sicurezza: il curator segnala ogni settimana i commit di sessione e di lavoro interattivo senza diario (9.2). Niente trascrizioni intere nel repo: porterebbero dati riservati (`CLAUDE.md` §5). `sessions/_raw/` tiene solo estratti puntuali, senza dati riservati.
- Retention: diari ed estratti per sempre.
- Da verificare nello step 5: comportamento degli hook nelle sessioni cloud quando l'ambiente scade per inattività.

## 13. Piano di sviluppo

| Step | Contenuto | Criterio di accettazione |
|---|---|---|
| 1 | Struttura del vault, `CLAUDE.md`, `README.md`, template, stato dell'ingestion vuoto | Una sessione cloud nuova legge `CLAUDE.md` e sa dove scrivere ogni tipo di nota |
| 2 | Agente `ingestor` e comandi `/ingest`, `/ingest-file` | `/ingest-file` su `BlueAge_CompanyProfile_v24.pdf` produce una nota conforme allo schema 4.2 |
| 3 | Primo caricamento a lotti (6.5) | Campione di 10 note per lotto approvato dall'utente |
| 4 | Task schedulati di ingestion, digest e riconciliazione | 3 giorni di run senza errori e senza doppioni |
| 5 | `/chiudi-sessione`, hook di sessione, bridge della cartella chat | Le sessioni della settimana compaiono in `sessions/` |
| 6 | Skill `blueage-deck`, `blueage-corso` snellita e `blueage-animazioni` (nel vault dal 26/10) | Un deck generato in cloud e caricato su SharePoint |
| 7 | Agente `curator`, comando `/curator` e task `curator`; agente `librarian` | Prima PR di proposte ricevuta e valutata (curator: PR #14 del 25/10) |
| 8 | Obsidian sui dispositivi in sola lettura (clone e Obsidian Git solo in pull) | Il grafo è visibile su PC e telefono (telefono fatto il 23/10, PC da configurare) |
| 9 | Dashboard Cockpit, task `cockpit` e nota `home.md` | 3 giorni di aggiornamenti della dashboard senza errori; `home.md` leggibile in Obsidian con Tasks e Dataview |
| 10 | Fonte GitHub (5.4, 6.6) e task `ingest-github` | 3 giorni di run senza errori; il log di `parts-radar-sviluppo` riceve una riga per giorno di lavoro sul repo |

### 13.1 Fase 2 · dal vault al prodotto

Gli step 1–10 hanno costruito il vault personale. La fase 2 lo porta a prodotto (tema `second-brain`, progetto `second-brain-prodotto`): prima l'affidabilità, poi l'uso, poi il prodotto. Si esegue uno step alla volta, nell'ordine, e uno step è chiuso solo quando il suo criterio è verificato. Principio guida: **il codice fa la meccanica, il modello fa il giudizio**. Perimetro, chiave di famiglia, slug, watermark, stato e controlli sono script testati; al modello restano lettura, riassunto, collegamenti e decisioni.

| Step | Blocco | Contenuto | Criterio di accettazione |
|---|---|---|---|
| 11 | Affidabilità | Rete di sicurezza del codice: controllo dei dati riservati a pattern (IBAN, telefoni, token e chiavi, codici di riunione, GUID) in `controlla-vault.py` come errore bloccante; test pytest con un mini-vault di prova per `controlla-vault.py`, `rinomina-nota.py` e `plancia.py`; il workflow CI esegue i test prima del controllo | La CI è rossa su una nota di prova con un IBAN finto; i test passano in CI e nel pre-commit non cambia nulla per le note esistenti |
| 12 | Affidabilità | Meccanica in codice: `famiglia.py` (chiave di famiglia e slug da un nome di file, 3.2 dell'ingestor), `perimetro.py` (dentro o fuori perimetro da un `webUrl`), `stato.py` (lettura e scrittura di watermark e voci con validazione e unione dei conflitti), `nuova-nota.py` (scheletro di una nota dal template con frontmatter validato); stato diviso per fonte in `.state/<fonte>.json`; l'ingestor chiama gli script e scrive solo riassunti e collegamenti; golden test sulle famiglie reali del vault | 3 giri dei task senza differenze rispetto a prima; `ingestor.md` sotto le 1.500 parole; nessuna modifica a mano di `.state/` |
| 13 | Affidabilità | Configurazione separata dal motore: `vault.yaml` con nome, fuso, lingua, fonti (perimetro ed esclusioni), nomi del connettore, repository, task (orari, modello, connettori); script, agenti, routine, `plancia.py` e `cockpit.py` leggono da lì; script di setup dell'ambiente cloud committato (prima nello step 16). Chiuso il 31/10: criterio verificato; il giro anomalo del 31/10 (file non restituiti dall'indice) non è dello step ma dell'affidabilità ai riordini (step sotto) | Nessun valore BlueAge in `.claude/` fuori da `vault.yaml` (`grep -ri blueagesrl .claude` vuoto); la CI segnala se SPEC e `vault.yaml` divergono sugli orari dei task |
| 14 | Affidabilità | Fonte unica delle regole: la matrice delle scritture e il perimetro vivono in un posto solo (SPEC §3 e `vault.yaml`); `CLAUDE.md` e gli agenti rimandano invece di copiare. Dal 29/10: `ingestor`, routine comune, `curator`, `chiudi-sessione`, `/cattura` e `/smista` rimandano a `CLAUDE.md` §3 e §7 senza copiarli né rileggere `CLAUDE.md`; le regole che servono solo in una cartella stanno in `.claude/rules/` (4.1) | Una sola copia della matrice nel repo |
| 15 | Uso | Retention delle note hub: `## Interazioni recenti` alle ultime 20 righe (il resto si legge dai backlink); `## Fonti` di clienti e temi generate dallo script o sostituite da una query Dataview; le note `partial: true` riprese a lotti dalla riconciliazione o segnate come sufficienti; regola di archivio per i progetti `chiuso` | Nessuna sezione hub oltre le 20 righe; le 15 note parziali del 26/10 completate o segnate |
| 16 | Uso | Cockpit v2 (2): pagina HTML statica generata da `cockpit.py` con il template versionato in `.claude/templates/`, dati da `plancia.py` e fotografia del calendario dal task; blocchi Oggi, Settimana, Progetti con semaforo e prossimi passi, dettaglio a un tocco; task `cockpit` riscritto (una pubblicazione, niente dataset); mod dell'app desktop e dashboard di tipo Dashboard ritirate. Decisione del 27/10 dopo la revisione con l'utente: sola lettura, da telefono e da PC, basi stabili | 3 giorni di giri senza errori; l'utente apre la pagina dal telefono la mattina e trova scadenze, eventi e stato dei progetti senza chiedere nulla a Claude |
| 17 | Uso | Librarian e ricerca: `cerca.py` (frontmatter e testo, ordinato per collegamenti), agente `librarian` (9.3), comandi `/oggi`, `/progetto`, `/cattura`, `/smista` (8) | 10 domande di prova sulla knowledge con risposta corretta e fonti citate; i quattro comandi in `.claude/commands/` |
| 17b | Affidabilità | Affidabilità ai riordini (audit del 31/10, `proposals/2026-10-31-audit-ingestion.md` §4 e §6). Fatto il 31/10: P4 e P5 (PR #60); P1–P3, P6, P7 e P9 (PR #62): identità per regola in `stato.py` (indice inverso nota → voci, `trova`, `collega`, conteggio `assente`, 6.1 e 6.4), `sposta-nota.py` come unico modo per spostare una nota fonte, `riconcilia.py` con il piano in JSON, `--piano` e `--applica` e il task `reconcile-ridotta` che lo usa, controlli incrociati stato ↔ note di 4.4 con `perimetro.py --verifica` e `famiglia.py --verifica` in CI (soglia 95%), merge per campo nel driver dello stato; P8, P10, P11 e P13 (PR #63): hub da rileggere e anomalie dei giri nel digest con `plancia.py --anomalie` e `anomalie.py`, `scarta.py` e `fonti.outlook` in `vault.yaml`, `perimetro.py` a lista di prefissi con `--profondita`; routine e agente allineati a 6.2, 6.4 e 7, agente sotto le 1.500 parole. Test di collaudo T1–T10 del report su un mini-vault, e T11 simulato sul mini-vault (`test_t11_riordino_delivery.py`: riordino rilevato, piano con 3 `sposta`, `--applica`, `set-riconciliata`, riga d'esito OK, 0 errori del controllo). Aperto: il T11 reale, che richiede il task `reconcile-ridotta` creato in claude.ai | T11 del report: un riordino reale di una cartella di prova in Delivery (spostata e rinominata da Leonardo) viene rilevato dal giro del mattino e riconciliato dal `reconcile-ridotta`, il digest dice quante note ha spostato, nessun intervento in sessione |
| 18 | Prodotto | Onboarding come prodotto (13.2): comando `/installa` (wizard del briefing che scrive `vault.yaml`, comprese le fonti e le librerie da ingerire e quelle che il rilevatore di riordino sorveglia, `fonti.rilevatore.fonti`, con la profondità per libreria misurata fino alla prima cartella con file da `perimetro.py --profondita <elenco.json>` sull'elenco letto dal connettore, e l'ordine delle posizioni canoniche `fonti.canoniche` (6.2, passo 7; 6.4), creazione dei task schedulati dalla sessione, controllo dei nomi del connettore e dei permessi, giro di prova); comando `/avvia` per il primo caricamento a lotti (6.5) con campione di qualità integrato; chiusura automatica delle sessioni (hook di fine turno con commit e push; task notturno che scrive diario, log e attività dalle sessioni del giorno); integrità invisibile (la sessione corregge gli errori del controllo senza esporli al cliente); cattura via mail con oggetto `Appunto: …` in `inbox/`; controllo di qualità a campione nel giro del curator (5 note rilette contro l'originale); manuale d'uso per il manager sui tre gesti; guida di installazione da zero provata su un account e un clone nuovi. Prerequisito: consegna dei file prodotti (scheda scaricabile nella chat e nome nella nota del progetto, o connettore che carica i binari) | Primo caricamento di un vault nuovo in una giornata; una sessione chiusa senza "chiudiamo" lascia diario e commit; un deck prodotto in cloud arriva al cliente; manuale letto e capito da una persona non tecnica |
| 19 | Prodotto | Separazione della proprietà intellettuale e governance (13.2): repo template del motore (`.claude/`, script, template, SPEC generica, `vault.yaml` d'esempio) senza contenuti BlueAge (skill `blueage-*`, temi, clienti, persone); procedura di upgrade del motore nei vault installati senza toccare `vault.yaml` e note; skill del cliente generata dal suo template pptx durante l'installazione; repo dei clienti nell'organizzazione GitHub di BlueAge, un team per cliente, secret scanning attivo; accordo sul trattamento dei dati (nomina a responsabile, base giuridica delle email in `people/`) come documento contrattuale; prerequisiti del cliente scritti (piano Claude con Code e task schedulati, da verificare quale; account GitHub anche gratuito; connettore Microsoft 365; Obsidian facoltativo) | Template installabile; nessun file BlueAge nel template; un upgrade del motore applicato a questo vault senza modifiche alle note; prerequisiti verificati sulla prima installazione interna (Leonardo), con la giornata cronometrata e i passi manuali annotati |
| 20 | Prodotto | Metriche di valore: riga settimanale nel resoconto del curator con note totali e nuove, giri dei task OK ed errori, domande risposte, consumo del piano se leggibile; base per il prezzo e per il rapporto al cliente | 4 settimane consecutive di metriche nel registro delle PR del curator |

Modelli consigliati per l'esecuzione: la sessione guida e rivede (il modello più capace disponibile); il codice con i test lo scrivono subagenti Opus; le modifiche meccaniche alle note (15, 20) Sonnet; gli step che toccano SPEC e regole (13, 14, 17b, 18, 19) li fa la sessione.

### 13.2 Forma del prodotto

Decisioni prese con l'utente il 28/10 (diario `2026-10-28-second-brain-forma-del-prodotto`); guidano gli step 18–20.

- **Chi installa e chi gestisce.** Il prodotto non è self-installing per il cliente: BlueAge lo installa in una giornata e lo gestisce ogni mese (PR del curator, upgrade del motore, metriche, guasti). La gestione è parte del prodotto, non un accessorio. Il self-install (`/installa`) è lo strumento interno con cui BlueAge installa in modo ripetibile.
- **Tre gesti del cliente.** Leggi: il Cockpit (2) dal telefono. Chiedi: una chat sul vault, risposte con le fonti (`librarian`, 9.3). Lavora: una chat sul vault in cui il cliente fa le sue attività con Claude (deck, documenti, analisi) e tutto resta nel vault. Git, PR, SPEC, permessi, verifica dei giri e curator non li vede mai. La cattura via mail (oggetto `Appunto: …`, scritta in `inbox/` dal task di Outlook) è una comodità dal telefono.
- **Dalla disciplina alla macchina.** Perché "Lavora" regga senza che il cliente conosca le regole: (a) chiusura automatica: hook di fine turno che fa commit e push di ciò che è cambiato, e task notturno che rilegge le sessioni del giorno e scrive diario, righe di log e attività; (b) consegna dei file prodotti: scheda scaricabile nella chat e nome del file nella nota del progetto finché il connettore non carica i binari (14); (c) integrità invisibile: la sessione corregge da sola gli errori del controllo (4.4) e non li espone al cliente, il curator segnala a BlueAge quello che resta; (d) skill del cliente: il template pptx raccolto nel briefing diventa una skill durante l'installazione. I file sono salvati a ogni turno; la knowledge (decisioni, stato dei progetti) entra a fine sessione o la notte.
- **Installazione.** Quattro passi restano a mano perché sono azioni di account: piano Claude del cliente, repo creato dal template con l'app GitHub di Claude installata, ambiente cloud, autorizzazione del connettore Microsoft 365 (circa 15 minuti in condivisione schermo). Il resto lo fa `/installa` da una sessione: wizard che elenca librerie e cartelle viste dal connettore e chiede sì/no, nome, fuso, lingua e repository di progetto, e scrive `vault.yaml` (step 13); creazione dei task schedulati con orario, modello e connettori; controllo dei nomi del connettore e dei permessi; giro di prova. Con BlueAge presente il wizard è il briefing; senza, è la stessa conversazione.
- **Repo del cliente.** Repo privato nell'organizzazione GitHub di BlueAge, uno per cliente, con il cliente come collaboratore; si trasferisce alla sua organizzazione se lo chiede o se se ne va. Condizioni: accordo sul trattamento dei dati (nomina a responsabile) come documento contrattuale; accesso minimo di BlueAge (un team GitHub per cliente, un collaboratore per vault). Il repo nell'organizzazione del cliente solo per chi ha un IT.
- **Vincoli.** Sessioni e task girano sull'account Claude del cliente: il consumo è suo e BlueAge non può lanciare sessioni al suo posto; la gestione passa dal repo e, per i guasti, da un intervento con il cliente collegato. Il piano Claude necessario per sessioni cloud e task schedulati è da verificare (oggi il vault gira su un piano Max). Il cliente ha un account GitHub, anche gratuito, solo per collegare l'ambiente al repo.
- **Tier.** Si distinguono per le skill, non per le ore di incontro: Start senza skill, Completo con la skill deck sul template del cliente, Executive con più skill.
- **Prova.** La prova di "installabile" è la prima installazione interna (Leonardo) con template e wizard: giornata cronometrata e ogni passo manuale annotato. Quella lista è la guida di installazione e il perimetro del contratto di gestione.

## 14. Decisioni aperte

- `blueage-animazioni` è nel vault, ma il rendering video (HTML → MP4) nelle sessioni cloud è da provare.
- Consegna dei file prodotti dalle skill: dal cloud il connettore non carica su OneDrive un PDF o un pptx oltre pochi KB (26/10), quindi il criterio dello step 6 ("deck caricato su SharePoint") per ora richiede il caricamento a mano. Dal 28/10 la consegna dei file prodotti è un prerequisito dello step 18 (13.2).
- Un vault = un utente (1). Un reparto o un team sono più vault, forse con temi condivisi: da decidere con il primo cliente a più persone, dopo lo step 19.
- Il Cockpit v2 (step 16) è una pagina statica pubblicata come artifact su claude.ai: dipende da claude.ai solo come hosting, non da funzioni in early access. Se anche quello cambiasse, la stessa pagina si può pubblicare altrove senza toccare lo script; `home.md` e il digest restano la vista di riserva. La dashboard di tipo Dashboard con `ArtifactData` e la mod dell'app desktop sono ritirate il 27/10.
- Fonti diverse da Microsoft 365 (Google Workspace, altri repository): dallo step 13 il perimetro è configurazione (`vault.yaml`), e dal 31/10 (P13) `perimetro.py` scorre una lista di prefissi (`config.perimetro()["posizioni"]`) invece di due rami: una libreria o una cartella nuove, o un tenant diverso al posto di questo, sono voci della lista costruite da `vault.yaml`, senza codice (due tenant insieme richiedono una modifica a `config.perimetro()`). Una fonte di tipo nuovo (Google Drive) richiede ancora le sue voci in `config.perimetro()`, i suoi messaggi e il suo ramo nell'ingestor.
- Ricerca vettoriale (29/10, diario `2026-10-29-database-vettoriale`): oggi la ricerca è lessicale (`cerca.py`) e agentica (`librarian`, 9.3), senza indice. Si passa alla ricerca ibrida al primo di questi trigger: recall sotto il 90% (note attese nei primi 5 risultati) sul set di valutazione per colpa del vocabolario; oltre circa 5.000 note o più di 4–5 giri di ricerca in media per risposta; primo cliente a più persone; note in lingue miste. Forma prevista: indice vettoriale come file derivato e ricostruibile (sqlite-vec o LanceDB) dietro `cerca.py`, ricerca BM25 + vettori, embedding con un modello locale multilingue o via API (Voyage) con accordo sul trattamento dei dati; agenti e comandi non cambiano. Da decidere al momento: indice committato o ricostruito all'avvio del container. Esclusi un database vettoriale gestito (solo se BlueAge ospita più clienti o vault di team) e un indice sugli originali, già coperto dal connettore (Microsoft Search, semantic index di Copilot).
- Lingua: regole, template e etichette del Cockpit sono in italiano. Dallo step 13 i nomi delle sezioni che gli script leggono stanno in `vault.yaml` (`sezioni`) e la lingua è un campo (`vault.lingua`); una versione in altra lingua (template, regole, etichette) è una decisione commerciale, non tecnica.
