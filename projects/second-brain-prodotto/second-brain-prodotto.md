---
type: project
status: attivo
role: "Product owner e sviluppatore: dal vault personale al prodotto Second Brain"
clients: []
people: []
updated: 2026-10-27
---

# Second Brain · dal vault al prodotto

## Stato

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
- [ ] Step 13 · Configurazione separata dal motore: `vault.yaml` (nome, fuso, lingua, fonti con perimetro ed esclusioni, nomi del connettore, task con orari, modello e connettori); script e agenti leggono da lì; nessun valore BlueAge in `.claude/` · modello: Fable ([[2026-10-26-piano-prodotto-second-brain]])
- [ ] Step 14 · Fonte unica delle regole: matrice delle scritture e perimetro in un posto solo, con rimandi da CLAUDE.md e dagli agenti · modello: Fable ([[2026-10-26-piano-prodotto-second-brain]])
- [ ] Step 15 · Retention delle note hub: interazioni recenti alle ultime 20, `## Fonti` da backlink o generate, ripresa delle note `partial`, archivio dei progetti chiusi · modello: Sonnet ([[2026-10-26-piano-prodotto-second-brain]])
- [ ] Step 16 · Riproducibilità: mod cockpit versionata, setup cloud committato, task letti da `vault.yaml`, guida di installazione provata su un clone nuovo · modello: Opus ([[2026-10-26-piano-prodotto-second-brain]])
- [x] Step 17 · Librarian e ricerca: `cerca.py`, agente `librarian`, comandi `/oggi`, `/progetto`, `/cattura`, `/smista` · modello: Opus, revisione Fable ✅ 2026-10-27 ([[2026-10-27-step-17-librarian]])
- [x] Step 17 · permessi in `.claude/settings.json` per `cerca.py`, `plancia.py` e `mcp__github__get_file_contents`, con l'ok di Lorenzo ✅ 2026-10-27 ([[2026-10-27-step-17-librarian]])
- [ ] Step 17 · prova dei quattro comandi `/oggi`, `/progetto`, `/cattura`, `/smista` in una sessione nuova ([[2026-10-27-step-17-librarian]])
- [ ] Step 18 · Onboarding come prodotto: `/avvia` per il primo caricamento a lotti con campione di QA, controllo di qualità a campione nel curator, manuale per il manager · modello: Fable ([[2026-10-26-piano-prodotto-second-brain]])
- [ ] Step 19 · Separazione IP e governance: repo template del motore senza contenuti BlueAge, repo nell'organizzazione BlueAge, secret scanning, policy dati, prerequisiti del cliente · modello: Fable ([[2026-10-26-piano-prodotto-second-brain]])
- [ ] Step 20 · Metriche di valore: riga settimanale nel resoconto del curator (note, giri OK, errori, domande risposte, consumo) · modello: Sonnet ([[2026-10-26-piano-prodotto-second-brain]])

## Decisioni

- Ordine: affidabilità, poi uso, poi prodotto. Il refactor "motore + configurazione" si fa quando il codice è testato, non prima ([[2026-10-26-piano-prodotto-second-brain]])
- Il piano vive qui come attività e in SPEC §13 come fase 2; il tema [[second-brain]] resta l'offerta commerciale ([[2026-10-26-piano-prodotto-second-brain]])
- La sessione guida e rivede; il codice con i test lo scrivono subagenti Opus, le modifiche meccaniche Sonnet; SPEC e regole le fa la sessione ([[2026-10-26-piano-prodotto-second-brain]])
- Il nucleo del prodotto sta su primitive stabili (markdown, git, task schedulati, connettore); dashboard e mod sono strati opzionali ([[2026-10-26-piano-prodotto-second-brain]])
- Un vault = un utente; team e fonti non Microsoft 365 sono decisioni aperte (SPEC §14) ([[2026-10-26-piano-prodotto-second-brain]])

## Prossimi passi

- Revisione del cockpit (tre domande a Lorenzo, poi opzioni) prima dello step 16: il risultato ne diventa il contenuto, o uno step a sé
- Verifica dei 3 giri dei task sullo step 12, poi step 13 (configurazione separata dal motore)

## Fonti

- [[2026-10-26-piano-prodotto-second-brain]]
- [[2026-10-27-step-17-librarian]]
