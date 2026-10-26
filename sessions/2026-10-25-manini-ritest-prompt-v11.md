---
type: session
date: 2026-10-25
surface: locale
topics: ["[[ai-nei-processi]]"]
outcome: "Prompt v1.1 ritestato sui 15 DDT e matching ripetuto sull'estrazione reale (H29 chiusa); report 04, 05 ed essenziale aggiornati e ripubblicati in Library/"
---

# Manini DDT: ritest del prompt v1.1 e matching sull'estrazione

Diario ricostruito il 26/10 dai commit del repo `manini-automazione-ddt` e del vault: la sessione locale non l'aveva scritto perché lavorava dal repo di progetto, dove la skill `chiudi-sessione` non si carica. Il lavoro è partito alle 22:50 con una sessione cloud sul repo di progetto (`prepara_estrazione.py` e la regola sui PDF) ed è proseguito in locale fino alle 23:40, perché i DDT si leggono solo dalla cartella `Dati/` sincronizzata sul PC.

## Obiettivo

Chiudere i due aperti tecnici di [[manini-automazione-ddt]]: ritestare il prompt di estrazione v1.1 sui 15 DDT reali e ripetere il matching sull'output vero dell'estrazione invece che sulla verità trascritta (H29).

## Decisioni

- Ritest del prompt v1.1: con il modello standard 100% dei campi critici, 15/15 DDT pronti e 14/15 perfetti (erano 11); con il veloce dall'88% al 98% e da 8 a 11 DDT pronti. Gli errori che arrivano a un DDT pronto sono tutti segnati in `campi_incerti` ([[04-benchmark]])
- Nel flusso, un campo critico incerto manda il DDT a verifica (H30) ([[04-benchmark]])
- Il miglioramento va letto come prompt e modello insieme: i modelli del 25/10 non sono quelli del 22/10 (H32), e c'è una sola esecuzione per DDT (H31) ([[04-benchmark]])
- Matching sull'estrazione reale, H29 chiusa: con il modello standard nessun DDT cambia stato e 0 abbinamenti automatici errati, quindi i numeri del 23/10 reggono ([[05-matching]])
- Due difetti del motore da correggere prima del pilota: fornitore per ragione sociale tollerante a "S.R.L." e filiali (H33), codice stampato senza ordine in più ordini aperti → E07 (H34) ([[05-matching]])
- Regole di estrazione del prompt invariate; i candidati per una v1.2 restano da ritestare prima dell'uso ([[prompt-estrazione-ddt]])
- I PDF dei DDT sono scansioni: il connettore ne restituisce solo il testo, vuoto, quindi estrazione e benchmark si fanno da una sessione locale (`CLAUDE.md` del repo di progetto)

## File toccati

- Repo `manini-automazione-ddt`: `matching/prepara_estrazione.py` (nuovo), `report/04_benchmark.md` (§10), `report/05_matching.md` (§9), `report/essenziale.md`, `kit/prompt_estrazione_ddt.md`, `CLAUDE.md` (PR #1, #2, #3)
- OneDrive `Progetto Automazione/Library/`: copie ripubblicate di report, prompt ed essenziale, ingerite il 26/10 ([[2026-10-26]])
- Vault: `projects/manini-automazione-ddt/` (scheda e log, commit 9c9f14e)

## Aperti

- [x] Doppione di famiglia: la copia dell'essenziale in Library (25/10) è la versione successiva di quella nella cartella Manini (ferma al 23/10) (chiuso: note unite il 26/10 in [[manini-ddt-essenziale]])
