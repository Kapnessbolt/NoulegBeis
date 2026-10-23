---
type: source-doc
source: onedrive
family: 04-benchmark
current:
  item_id: 013UYHJHBZ3QNAJXJJAVDJYRM6WQKBPXML
  uri: file:///b!2fHSoBOOE0aRvS_GntS6s6RJcyNKjAJMiRtoiZ6n5xzp8hWMRRoMQKOVYgftTbzT/013UYHJHBZ3QNAJXJJAVDJYRM6WQKBPXML
  web_url: https://blueagesrl-my.sharepoint.com/personal/lorenzo_curione_blueage_it/Documents/BlueAge/01_Materiale clienti/Manini/Progetto Automazione/Library/04_benchmark.md
  name: 04_benchmark.md
  last_modified: 2026-10-23T11:33:34Z
versions:
  - { name: 04_benchmark.md, item_id: 013UYHJHBZ3QNAJXJJAVDJYRM6WQKBPXML, last_modified: 2026-10-23T11:33:34Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-23T12:05:00Z
projects: ["[[manini-automazione-ddt]]"]
clients: ["[[manini]]"]
topics: ["[[ai-nei-processi]]"]
tags: [entrata-merci, ddt, benchmark]
---

# Manini · caso DDT, 04 benchmark di estrazione

## Riassunto

Terzo step di [[manini-automazione-ddt]] (22/10/2026): misura sui 15 DDT del campione tre motori di lettura, cioè un modello generativo "standard", uno "veloce" e un OCR classico con regole generiche. Si confrontano con una verità trascritta a vista. La lettura generativa con un modello capace porta tutti i DDT pronti per il matching. Il modello veloce sbaglia la struttura e l'OCR classico non è utilizzabile. Il kit (prompt, verità, scoring, motore OCR) è riusabile nella sessione IT del [[corso-ai-manini]] per misurare AI Builder e Copilot Studio con lo stesso metro.

## Punti chiave

- La lettura non è il problema con un modello generativo adeguato, anche su foto, fotocopie e scontrino termico; il DDT illeggibile viene rifiutato correttamente
- Il modello conta più del prompt: quello veloce non propaga l'ordine scritto in coda, sfasa i codici di una riga e rifiuta lo scontrino termico
- L'OCR classico senza modelli per fornitore: 0 DDT su 15 pronti
- Il tipo di acquisizione pesa poco con il modello standard e di più con quello veloce
- Il prompt v1.1 corregge gli errori trovati ma non è ancora stato ritestato
- Implicazioni: il limite del business case sarà il matching (ordine assente in 5 su 15, codici solo del fornitore); in AI Builder e Copilot Studio va scelto il modello più capace; servono controlli di coerenza deterministici
- Limiti dichiarati H17–H21: verità trascritta dalla stessa famiglia di modelli (il 100% può essere sovrastimato), motori testati Claude e non AI Builder, 1 DDT per fornitore, immagini a 110 dpi

## Numeri

- Campi critici corretti: 100% (512/512) standard, 88% (449/512) veloce, 27% (139/512) OCR
- DDT pronti per il matching: 15/15, 8/15, 0/15
- Righe perfette: 88/88, 32/88, 0/88
- Ordine della riga: 100% standard contro 44% veloce
- Per acquisizione, standard: 99% su scansioni e su foto o fotocopie; veloce: 90% contro 84%

## Decisioni e azioni

- In aula utenti bastano tre DDT: Hilti (facile), Iron Works (45 righe), 004664 (illeggibile)
- [ ] Ritestare il prompt v1.1 con lo stesso kit
- [ ] Revisione umana di 3–4 DDT difficili e confronto con i movimenti AS400 di Aprilia (H17)

## Versioni

- 04_benchmark.md · 2026-10-23 · prima versione (analisi del 22/10)
