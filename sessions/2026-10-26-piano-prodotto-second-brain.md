---
type: session
date: 2026-10-26
surface: cloud
topics: ["[[second-brain]]"]
outcome: "Analisi completa del vault (forza, debolezze, lente prodotto); piano della fase 2 scritto in SPEC §13 e nel progetto second-brain-prodotto; avviato lo step 11"
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
- Decisioni rinviate, scritte in SPEC §14: un vault = un utente (un reparto sono più vault con temi condivisi?); dipendenza da funzioni in early access (mod, dashboard con ArtifactData), da tenere come strati opzionali sopra il nucleo stabile (markdown, git, task); fonti diverse da Microsoft 365 (Google Workspace) solo con la configurazione separata.

## File toccati

- `sessions/`: questo diario
- `projects/second-brain-prodotto/`: scheda e log (nuovi)
- `topics/second-brain.md`: collegamento al progetto
- `SPEC.md`: §13 fase 2 (step 11–20), §14 decisioni aperte, §4.4 dati riservati e test in CI, versione 1.18, sul branch `claude/affectionate-ritchie-v0im3q`
- `.claude/scripts/`: controllo dei dati riservati in `controlla-vault.py`, `VAULT_ROOT` nei tre script, `tests/` (step 11)
- `.github/workflows/controllo-vault.yml`, `.gitignore`, `CLAUDE.md` §7

## Aperti

- [x] Unire la PR della SPEC 1.18 (fase 2 del piano, step 11) e del progetto `second-brain-prodotto` (chiuso: PR #24 unita)
- [ ] Eseguire gli step 12–20 uno alla volta, ognuno chiuso con il suo criterio di accettazione (attività nella scheda del progetto)
