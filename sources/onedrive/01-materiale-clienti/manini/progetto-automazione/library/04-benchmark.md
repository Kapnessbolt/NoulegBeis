---
type: source-doc
source: onedrive
family: 04-benchmark
current:
  item_id: 013UYHJHBZ3QNAJXJJAVDJYRM6WQKBPXML
  uri: file:///b!2fHSoBOOE0aRvS_GntS6s6RJcyNKjAJMiRtoiZ6n5xzp8hWMRRoMQKOVYgftTbzT/013UYHJHBZ3QNAJXJJAVDJYRM6WQKBPXML
  web_url: https://blueagesrl-my.sharepoint.com/personal/lorenzo_curione_blueage_it/Documents/BlueAge/01_Materiale clienti/Manini/Progetto Automazione/Library/04_benchmark.md
  name: 04_benchmark.md
  last_modified: 2026-10-25T22:15:35Z
versions:
  - { name: 04_benchmark.md, item_id: 013UYHJHBZ3QNAJXJJAVDJYRM6WQKBPXML, last_modified: 2026-10-25T22:15:35Z }
  - { name: 04_benchmark.md, item_id: 013UYHJHBZ3QNAJXJJAVDJYRM6WQKBPXML, last_modified: 2026-10-23T11:33:34Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-26T05:53:02Z
projects: ["[[manini-automazione-ddt]]"]
clients: ["[[manini]]"]
topics: ["[[ai-nei-processi]]"]
tags: [entrata-merci, ddt, benchmark]
---

# Manini · caso DDT, 04 benchmark di estrazione

## Riassunto

Terzo step di [[manini-automazione-ddt]]: misura sui 15 DDT del campione tre motori di lettura (generativo "standard", generativo "veloce", OCR classico con regole generiche) contro una verità trascritta a vista. I §1–§9 misurano il prompt v1.0 (22/10/2026); il nuovo §10 riporta il ritest del prompt v1.1 del 25/10/2026, con lo stesso campione, metodo e scoring ma modelli diversi (alias attuali di Claude Code invece del sandbox claude.ai). Il v1.1 porta il modello standard a 14 DDT perfetti su 15 e chiude gran parte del distacco del modello veloce. Il kit (prompt, verità, scoring, motore OCR) resta lo strumento per misurare AI Builder e Copilot Studio nella sessione IT del [[corso-ai-manini]].

## Punti chiave

- La lettura non è il problema con un modello generativo adeguato, anche su foto, fotocopie e scontrino termico; il DDT illeggibile viene rifiutato correttamente
- L'OCR classico senza modelli per fornitore: 0 DDT su 15 pronti
- Ritest v1.1: con lo standard spariscono gli errori su "Mov." e colli a 0; i campi critici restano al 100%, l'unico errore residuo (peso di 004647) non tocca il matching
- Le regole strutturali del v1.1 portano il veloce dal 44% al 91% sull'ordine della riga e dal 91% al 100% sul codice Manini; resta sotto lo standard e inciampa ancora sull'ordine con intestazioni ambigue (004663, 004682)
- La regola 3 sposta il rischio: il veloce non rifiuta più lo scontrino termico ma ne legge male la quantità (11,3 t invece di 31,38), segnandola però in `campi_incerti`
- Il miglioramento v1.0 → v1.1 è di prompt e modello insieme (H32); una sola esecuzione per DDT, variabilità non misurata (H31)
- Candidati per un prompt v1.2: copiare la riga `peso_totale` nel peso netto di testata; peso a 0 solo se stampato 0; proporre come ordine un numero di 6 cifre finito tra gli altri riferimenti
- Implicazioni: scegliere il modello più capace; usare `campi_incerti` nel flusso (campo critico incerto → verifica, H30); controlli di coerenza deterministici
- Limiti dichiarati H17–H21 e H30–H32: verità trascritta dalla stessa famiglia di modelli, motori Claude e non AI Builder, 1 DDT per fornitore

## Numeri

- v1.0 (22/10), campi critici: 100% (512/512) standard, 88% (449/512) veloce, 27% (139/512) OCR; DDT pronti 15/15, 8/15, 0/15
- v1.1 (25/10), campi critici: 100% standard, 98% (500/512) veloce
- DDT pronti per il matching v1.1: 15/15 standard, 11/15 veloce
- DDT perfetti: standard da 11 a 14 su 15, veloce da 6 a 8
- Righe perfette del veloce: da 32 a 79 su 88; colli al 100% con entrambi i motori, Mov. al 100% con lo standard
- 30 estrazioni nel ritest (un subagente per DDT e per motore): `campi_incerti` segnalato per 3 errori su 9

## Decisioni e azioni

- Il prompt v1.1 è quello da usare in aula IT e nel pilota; le correzioni di §10.4 vanno in una v1.2 da ritestare prima dell'uso
- In aula utenti bastano tre DDT: Hilti (facile), Iron Works (45 righe), 004664 (illeggibile)
- [x] Ritestare il prompt v1.1 con lo stesso kit (25/10)
- [ ] Revisione umana di 3–4 DDT difficili e confronto con i movimenti AS400 di Aprilia (H17)
- [ ] Ripetere 3 volte il giro sui DDT difficili per misurare la variabilità (H31) e rifare un giro con il prompt v1.0 e i modelli di oggi (H32)

## Versioni

- 04_benchmark.md · 2026-10-25 · aggiunto il §10 con il ritest del prompt v1.1: standard 14/15 DDT perfetti, veloce 98% dei campi critici e 11/15 DDT pronti; nuove ipotesi H30–H32 e candidati per la v1.2
- 04_benchmark.md · 2026-10-23 · prima versione (analisi del 22/10)
