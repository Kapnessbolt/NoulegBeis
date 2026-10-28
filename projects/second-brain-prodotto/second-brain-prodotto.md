---
type: project
status: attivo
role: "Product owner e sviluppatore: dal vault personale al prodotto Second Brain"
clients: []
people: []
updated: 2026-10-28
---

# Second Brain · dal vault al prodotto

## Stato

- Secondo giorno di osservazione (28/10) pulito: 7 giri su 7 OK, watermark di Outlook e GitHub avanzati, nessun doppione, numeri del Cockpit uguali a `plancia.py`; confermati i due difetti già tracciati per il 31/10. Il log di parts-radar ha due righe del 27/10 per nota perché il repo ha lavorato prima e dopo il watermark: non è un doppione, SPEC 6.6 da chiarire ([[2026-10-28-verifica-task-28-10]])
- Cockpit v2 costruito come step 16: pagina HTML statica generata da `cockpit.py` (template versionato, dati da `plancia.py`, fotografia del calendario dal task), pubblicata su claude.ai e ripubblicata dal task con una chiamata; mod e dashboard di tipo Dashboard ritirate; in attesa del criterio (3 giri) ([[2026-10-27-step-17-librarian]])
- Primo giorno di osservazione (27/10) pulito: 7 giri su 7 OK, watermark avanzati, nessun doppione, numeri del Cockpit uguali a `plancia.py`, calendario letto dal connettore; Lorenzo ha aperto la pagina dal telefono la mattina e funziona. Due difetti di visualizzazione da correggere dopo il criterio ([[2026-10-27-verifica-task-27-10]])
- Step 17 fatto: `cerca.py` (ricerca su titolo, frontmatter e corpo, ordinata per punteggio, backlink e data, 51 test), agente `librarian` e comandi `/oggi`, `/progetto`, `/cattura`, `/smista`; 10 domande di prova su 10 corrette con le fonti, una domanda fuori knowledge senza invenzioni; SPEC 1.20 ([[2026-10-27-step-17-librarian]])
- Il vault è la versione personale e il banco di prova dell'offerta [[second-brain]]; dopo la prima settimana ha 310 note, 0 errori di controllo, 7 task schedulati al giorno e un loop di miglioramento (diari → curator → proposte) ([[2026-10-26-piano-prodotto-second-brain]])
- Base solida da conservare: SPEC con PR, matrice delle scritture, controllo d'integrità a tre livelli, tracciabilità alla fonte, famiglia/versione, watermark con sovrapposizione, privacy by design, Obsidian in sola lettura ([[2026-10-26-piano-prodotto-second-brain]])
- Debolezze da chiudere nella fase 2: meccanica dell'ingestion affidata al modello e non al codice; codice senza test; privacy senza controllo automatico; note hub senza retention; nessuna ricerca né `librarian`; regole duplicate; pezzi fuori dal repo; 15 note parziali; account personali ([[2026-10-26-piano-prodotto-second-brain]])
- Il motore è già quasi generico: i valori BlueAge stanno in `ingestor.md`, `settings.json`, SPEC §5 e due cablature negli script; il contenuto BlueAge (skill, temi, clienti, persone) è proprietà intellettuale e resta fuori dal prodotto ([[2026-10-26-piano-prodotto-second-brain]])
- Piano in tre blocchi, step 11–20 di SPEC §13: affidabilità (11–14), uso (15–17), prodotto (18–20). Si esegue uno step alla volta, chiuso con il suo criterio di accettazione ([[2026-10-26-piano-prodotto-second-brain]])
- Step 12 fatto, in osservazione: sei script di servizio (`famiglia.py`, `perimetro.py`, `stato.py`, `nuova-nota.py`, `aggiorna-nota.py`, modulo `nota.py`) con 154 test; stato diviso per fonte con merge driver git che unisce i conflitti da solo; `ingestor.md` da 3.044 a 1.491 parole; golden test: famiglie d'accordo con il vault al 92%, cartelle al 99% ([[2026-10-26-piano-prodotto-second-brain]])
- Step 11 fatto: controllo dei dati riservati a pattern (IBAN, telefoni, chiavi, GUID, codici di riunione, password) come errore bloccante, 41 test pytest sui tre script con un mini-vault di prova, CI che esegue i test prima del controllo; sul vault reale 0 errori ([[2026-10-26-piano-prodotto-second-brain]])

## Attività

- [x] Step 11 · Rete di sicurezza del codice: controllo privacy a regex in `controlla-vault.py` (errore bloccante), test pytest con mini-vault per `controlla-vault.py`, `rinomina-nota.py`, `plancia.py`, CI che esegue i test · modello: Opus ✅ 2026-10-26 ([[2026-10-26-piano-prodotto-second-brain]])
- [x] Step 12 · Meccanica in codice: `famiglia.py`, `perimetro.py`, `stato.py`, `nuova-nota.py`; stato per fonte in `.state/<fonte>.json`; ingestor che chiama gli script e scrive solo i riassunti; golden test sulle famiglie reali del vault · modello: Opus, revisione Fable ✅ 2026-10-26 ([[2026-10-26-piano-prodotto-second-brain]])
- [ ] Step 12 · criterio di accettazione: 3 giri dei task (27, 28, 29/10) senza differenze rispetto a prima, con `/verifica-task` 📅 2026-10-29 ([[2026-10-26-piano-prodotto-second-brain]])
- [ ] Step 12 · decidere le 11 famiglie e la nota del company profile in disaccordo con gli script (rinominare con `rinomina-nota.py` o lasciare): elenco nel diario ([[2026-10-26-piano-prodotto-second-brain]])
- [ ] Step 13 · Configurazione separata dal motore: `vault.yaml` (nome, fuso, lingua, fonti con perimetro ed esclusioni, nomi del connettore, repository, task con orari, modello e connettori); script, agenti e `cockpit.py` leggono da lì; setup cloud committato; nessun valore BlueAge in `.claude/` · modello: Fable ([[2026-10-26-piano-prodotto-second-brain]])
- [ ] Step 14 · Fonte unica delle regole: matrice delle scritture e perimetro in un posto solo, con rimandi da CLAUDE.md e dagli agenti · modello: Fable ([[2026-10-26-piano-prodotto-second-brain]])
- [ ] Step 15 · Retention delle note hub: interazioni recenti alle ultime 20, `## Fonti` da backlink o generate, ripresa delle note `partial`, archivio dei progetti chiusi · modello: Sonnet ([[2026-10-26-piano-prodotto-second-brain]])
- [x] Step 16 · Cockpit v2: `cockpit.py`, template `.claude/templates/cockpit.html`, `plancia.py` esteso, task `cockpit` riscritto con il calendario dal connettore, prima pubblicazione · modello: Opus, revisione Fable ✅ 2026-10-27 ([[2026-10-27-step-17-librarian]])
- [ ] Step 16 · criterio di accettazione: 3 giri del task `cockpit` (27, 28, 29/10) senza errori, con `/verifica-task cockpit`, e pagina aperta dal telefono la mattina 📅 2026-10-30 ([[2026-10-27-step-17-librarian]])
- [ ] Step 16 · dopo il criterio: cancellare la vecchia dashboard e disattivare la mod sul PC ([[2026-10-27-step-17-librarian]])
- [ ] Step 16 · dopo il criterio: `plancia.py` conta come note nuove anche le righe "nuova versione" del digest (il 27/10 6 invece di 2); correggere e aggiungere il test 📅 2026-10-31 ([[2026-10-27-verifica-task-27-10]])
- [ ] Step 16 · dopo il criterio: `cockpit.py` mostra il proprio giro come "Da eseguire" perché la pagina si genera prima della riga nel digest; contarlo come in corso 📅 2026-10-31 ([[2026-10-27-verifica-task-27-10]])
- [x] Step 17 · Librarian e ricerca: `cerca.py`, agente `librarian`, comandi `/oggi`, `/progetto`, `/cattura`, `/smista` · modello: Opus, revisione Fable ✅ 2026-10-27 ([[2026-10-27-step-17-librarian]])
- [x] Step 17 · permessi in `.claude/settings.json` per `cerca.py`, `plancia.py` e `mcp__github__get_file_contents`, con l'ok di Lorenzo ✅ 2026-10-27 ([[2026-10-27-step-17-librarian]])
- [ ] Step 17 · prova dei quattro comandi `/oggi`, `/progetto`, `/cattura`, `/smista` in una sessione nuova ([[2026-10-27-step-17-librarian]])
- [ ] Step 18 · Onboarding come prodotto: `/avvia` per il primo caricamento a lotti con campione di QA, controllo di qualità a campione nel curator, manuale per il manager, guida di installazione provata su un clone nuovo · modello: Fable ([[2026-10-26-piano-prodotto-second-brain]])
- [ ] Step 19 · Separazione IP e governance: repo template del motore senza contenuti BlueAge, repo nell'organizzazione BlueAge, secret scanning, policy dati, prerequisiti del cliente · modello: Fable ([[2026-10-26-piano-prodotto-second-brain]])
- [ ] Step 20 · Metriche di valore: riga settimanale nel resoconto del curator (note, giri OK, errori, domande risposte, consumo) · modello: Sonnet ([[2026-10-26-piano-prodotto-second-brain]])

## Decisioni

- Cockpit v2 (27/10): sola lettura, da telefono e da PC, pagina statica generata dal vault e pubblicata come artifact; niente funzioni in early access; `home.md` resta la riserva; la mod dell'app desktop è ritirata ([[2026-10-27-step-17-librarian]])
- Ordine: affidabilità, poi uso, poi prodotto. Il refactor "motore + configurazione" si fa quando il codice è testato, non prima ([[2026-10-26-piano-prodotto-second-brain]])
- Il piano vive qui come attività e in SPEC §13 come fase 2; il tema [[second-brain]] resta l'offerta commerciale ([[2026-10-26-piano-prodotto-second-brain]])
- La sessione guida e rivede; il codice con i test lo scrivono subagenti Opus, le modifiche meccaniche Sonnet; SPEC e regole le fa la sessione ([[2026-10-26-piano-prodotto-second-brain]])
- Il nucleo del prodotto sta su primitive stabili (markdown, git, task schedulati, connettore); dashboard e mod sono strati opzionali ([[2026-10-26-piano-prodotto-second-brain]])
- Un vault = un utente; team e fonti non Microsoft 365 sono decisioni aperte (SPEC §14) ([[2026-10-26-piano-prodotto-second-brain]])

## Prossimi passi

- Giro del 29/10 con `/verifica-task` per chiudere i criteri degli step 12 e 16 (27 e 28/10 puliti, la prova dal telefono è fatta); nella PR di chiusura chiarire SPEC 6.6 (una riga di log per giorno e per giro)
- Dopo il criterio dello step 16: i due difetti del Cockpit, poi via la vecchia dashboard e la mod
- Step 13 (configurazione separata dal motore)

## Fonti

- [[2026-10-26-piano-prodotto-second-brain]]
- [[2026-10-27-step-17-librarian]]
- [[2026-10-27-verifica-task-27-10]]
- [[2026-10-28-verifica-task-28-10]]
