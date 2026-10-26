---
type: session
date: 2026-10-26
surface: cloud
topics: ["[[second-brain]]"]
outcome: "Analisi completa del vault; piano della fase 2 in SPEC §13 e nel progetto second-brain-prodotto; step 11 (PR #24) e step 12 (PR #25) uniti in main; step 12 in osservazione per tre giri dei task"
---

# Analisi del vault e piano della fase 2 (prodotto)

## Obiettivo

Valutare il vault com'è dopo la prima settimana (struttura, regole, codice, automazioni) e scrivere un piano per portarlo a livello di prodotto commerciale, da eseguire uno step alla volta.

## Decisioni

- Il vault ha una base solida: SPEC versionata con PR, matrice delle scritture per attore, controllo d'integrità a tre livelli (hook, pre-commit, CI) con 310 note e 0 errori, tracciabilità di ogni punto alla fonte, famiglia/versione dei documenti, ingestion a watermark con sovrapposizione, loop diari → curator → proposte, privacy by design, Obsidian in sola lettura. Queste scelte restano.
- Debolezza principale: la meccanica dell'ingestion (perimetro, famiglia, slug, watermark, merge dello stato) la esegue il modello seguendo prosa, non il codice. I bug della prima settimana (ordine git, UTC, finestra del digest) sono tutti meccanici. Il codice che c'è (`controlla-vault.py`, `plancia.py`, `rinomina-nota.py`) non ha test e la regola sui dati riservati (`CLAUDE.md` §5) non ha un controllo automatico.
- Altre debolezze: note hub che crescono senza retention (49 interazioni di Leonardo in due mesi, 44 fonti in `blueage.md`); l'obiettivo "rispondere a domande" senza `librarian` né ricerca; regole duplicate in tre posti (CLAUDE.md §3, SPEC §3, ingestor §1); pezzi del sistema fuori dal repo (mod cockpit, setup cloud, definizione dei task); 15 note `partial: true` mai completate; tutto su account personali.
- Lente prodotto: il motore è già quasi generico. I valori BlueAge stanno in tre file (`ingestor.md` per il perimetro, `settings.json` per i nomi del connettore, SPEC §5) più due cablature negli script (`"Relazione con BlueAge"` in `controlla-vault.py`, gli orari dei task in `plancia.py`). Il contenuto BlueAge (skill `blueage-*`, 580 KB; temi, clienti, persone) è proprietà intellettuale e non deve viaggiare con il prodotto. Il costo maggiore di ogni installazione è il primo caricamento, oggi manuale in cinque sessioni.
- Ordine scelto, dall'utente: prima l'affidabilità (codice per la meccanica, test, controllo privacy), poi l'uso (retention, librarian, onboarding), poi il prodotto (configurazione separata, template, governance, metriche). Il refactor "motore + configurazione" si fa quando il codice è già testato, non prima.
- Il piano è un progetto del vault, [[second-brain-prodotto]], così le attività entrano nel cockpit e in `home.md`; gli step sono anche in SPEC §13 come fase 2 (PR dedicata). Il tema [[second-brain]] resta l'offerta commerciale.
- Modelli per l'esecuzione: la sessione guida e rivede (Fable 5.1, il più capace disponibile); il codice con i test lo scrivono subagenti Opus; le modifiche meccaniche alle note (retention, metriche) Sonnet. Gli step che toccano SPEC e regole li fa la sessione stessa.
- Step 11 eseguito da un subagente Opus e rivisto in sessione: controllo dei dati riservati a pattern solo sul corpo delle note (il frontmatter ha id lunghi legittimi), un errore per categoria con al massimo 4 caratteri del valore; i GUID già in `settings.json` (nome del server del connettore locale) sono esclusi perché configurazione, non dati dei clienti; i pattern base64 escludono `_` e `-` per non prendere nomi di file e slug. Gli script leggono la radice da `VAULT_ROOT` solo per i test. Sul vault reale 0 errori; 41 test verdi; IBAN e telefono finti bloccati anche con `--modificati`.
- Rischio residuo noto: un hash git completo (40 caratteri) nel corpo di una nota verrebbe segnalato; oggi non ce ne sono.
- Step 12 eseguito da un subagente Opus e rivisto in sessione con prove su una copia del vault: nuova versione simulata con `aggiorna-nota.py --nuova-versione` (diff pulito, `current` in testa a `versions`), `stato.py set-item`, e un rebase vero tra due branch che scrivono `.state/outlook.json`: il merge driver unisce le voci e tiene il watermark più avanzato, nessun conflitto. Lo stato passa da `ingest.json` a un file per fonte; i diari e le proposte che citano il vecchio nome restano come storia.
- Golden test di `famiglia.py` sulle 134 note documento: 110 uguali, 13 differiscono solo per un prefisso messo a mano (`velo-ce-handoff-*`, `ai-foundation-program-m1`, `manini-ddt-essenziale`…), 11 disaccordi veri: quattro `Manini_Corso_AI_*_BlueAge` (il vault tiene `-blueage` in coda), due `Velo-CE - Pilota BC Lungo Bosch v006` accorciati a mano, `00 Indice evidenze Velo-CE`, `00 LEGGIMI - COPIA`, `TO DO Partner e Aziende`, `PULSE_K.pdf` (nota `pulse-presentazione-completa`), `Pulse_Strategia_ICP_e_Pricing_Blueage_v2_completo`. `perimetro.py`: 119 cartelle su 120; l'unica diversa è `blueage-companyprofile`, la cui `current` punta al sito partner mentre la nota sta in `salesmarketing/deck`. `famiglia.py --cerca` trova comunque la nota giusta anche in questi casi perché guarda anche `family` e `versions`, quindi non nascono doppioni; nessuna nota è stata rinominata, la decisione è un'attività del progetto.
- I permessi di `.claude/settings.json` per i cinque script nuovi non sono stati aggiunti: il subagente non può modificare i permessi e la sessione non li aggiunge su sua richiesta; li aggiunge Lorenzo o la sessione con il suo ok. Senza, nei task schedulati in modalità Auto le chiamate agli script possono essere bloccate.
- Il pre-commit esegue solo il controllo del vault, non i test: i test girano in CI. Da valutare se aggiungerli al pre-commit quando gli script cambiano.
- Permessi per i cinque script aggiunti in `.claude/settings.json` con l'ok esplicito di Lorenzo (commit a9e2b44), dopo una spiegazione in chiaro di cosa sono e perché servono: senza, un task schedulato in modalità Auto può fermarsi alla prima chiamata e lasciare note scritte con lo stato non aggiornato.
- Chiusura, dall'utente: gli step 13–20 nei prossimi giorni, uno alla volta. Lo step 13 (configurazione in `vault.yaml`) non parte prima di almeno un giro pulito dei task sullo step 12, perché tocca gli stessi script e un errore non si saprebbe a chi attribuire. Check-in programmato per le 08:20 del 27/10 con `/verifica-task` sul primo giro.
- Il diario aggiornato dopo il merge sta sul branch della sessione: da questa sessione cloud si pusha solo lì, quindi entra in `main` con una PR.
- Decisioni rinviate, scritte in SPEC §14: un vault = un utente (un reparto sono più vault con temi condivisi?); dipendenza da funzioni in early access (mod, dashboard con ArtifactData), da tenere come strati opzionali sopra il nucleo stabile (markdown, git, task); fonti diverse da Microsoft 365 (Google Workspace) solo con la configurazione separata.

## File toccati

- `sessions/`: questo diario
- `projects/second-brain-prodotto/`: scheda e log (nuovi)
- `topics/second-brain.md`: collegamento al progetto
- `SPEC.md`: §13 fase 2 (step 11–20), §14 decisioni aperte, §4.4 dati riservati e test in CI, versione 1.18, sul branch `claude/affectionate-ritchie-v0im3q`
- `.claude/scripts/`: controllo dei dati riservati in `controlla-vault.py`, `VAULT_ROOT` nei tre script, `tests/` (step 11)
- `.github/workflows/controllo-vault.yml`, `.gitignore`, `CLAUDE.md` §7
- `.claude/settings.json`: permessi dei cinque script (commit a9e2b44)
- Step 12: `.claude/scripts/` (`famiglia.py`, `perimetro.py`, `stato.py`, `nuova-nota.py`, `aggiorna-nota.py`, `nota.py`, test), `.state/<fonte>.json` al posto di `ingest.json`, `.gitattributes`, `.claude/settings.json` (hook del merge driver), `.claude/agents/ingestor.md`, routine `_comune` e `reconcile`, comando `verifica-task`, `CLAUDE.md` §2 e §7, `README.md`, `SPEC.md` 1.19 (§3, §4.4, §6.1, §11)
- Fuori dal repo: PR #24 e #25 su GitHub, unite; copia di prova del vault nello scratchpad della sessione, non conservata

## Aperti

- [x] Unire la PR della SPEC 1.18 (fase 2 del piano, step 11) e del progetto `second-brain-prodotto` (chiuso: PR #24 unita)
- [x] Unire la PR dello step 12 (SPEC 1.19) prima dei task delle 06:50, così il primo giro osservato è quello del 27/10 (chiuso: PR #25 unita)
- [x] Aggiungere in `.claude/settings.json` i permessi `Bash(python3 .claude/scripts/<script>.py:*)` per famiglia, perimetro, stato, nuova-nota e aggiorna-nota (chiuso: ok di Lorenzo, commit a9e2b44)
- [ ] Verificare i tre giri dei task del 27, 28 e 29/10 con `/verifica-task` e chiudere il criterio dello step 12 📅 2026-10-29
- [ ] Decidere le 11 famiglie e la nota `blueage-companyprofile` in disaccordo con gli script (rinominare o lasciare)
- [ ] Eseguire gli step 13–20 uno alla volta, ognuno chiuso con il suo criterio di accettazione (attività nella scheda del progetto); step 13 solo dopo un giro pulito dello step 12
