---
type: source-doc
source: onedrive
family: 03-schema-ddt
current:
  item_id: 013UYHJHBMCNS5KJ7MKVGZ2WOTZ7V37FBM
  uri: file:///b!2fHSoBOOE0aRvS_GntS6s6RJcyNKjAJMiRtoiZ6n5xzp8hWMRRoMQKOVYgftTbzT/013UYHJHBMCNS5KJ7MKVGZ2WOTZ7V37FBM
  web_url: https://blueagesrl-my.sharepoint.com/personal/lorenzo_curione_blueage_it/Documents/BlueAge/01_Materiale clienti/Manini/Progetto Automazione/Library/03_schema_ddt.md
  name: 03_schema_ddt.md
  last_modified: 2026-10-23T11:33:34Z
versions:
  - { name: 03_schema_ddt.md, item_id: 013UYHJHBMCNS5KJ7MKVGZ2WOTZ7V37FBM, last_modified: 2026-10-23T11:33:34Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-23T12:05:00Z
projects: ["[[manini-automazione-ddt]]"]
clients: ["[[manini]]"]
topics: ["[[ai-nei-processi]]"]
tags: [entrata-merci, ddt, schema-json]
---

# Manini · caso DDT, 03 schema JSON standard

## Riassunto

Secondo step di [[manini-automazione-ddt]] (22/10/2026): definisce lo schema JSON di un DDT in entrata, costruito sui casi visti nell'inventario ([[01-inventario]]). Due versioni: una canonica (JSON Schema, contratto tra estrazione, matching e staging AS400) e una piatta per il prompt AI Builder e il nodo Extract di Copilot Studio. Fissa la normalizzazione, le regole di estrazione e i controlli automatici che generano le eccezioni prima del matching.

## Punti chiave

- Principi: trascrivere, non dedurre; estrazione e abbinamento separati, così l'errore dell'AI resta visibile; il documento può essere rifiutato; valore grezzo e valore normalizzato; ogni riga ha un tipo (articolo, testo, peso totale, trasporto); ordine sia in testata sia su ogni riga
- Ogni caso del campione ha un campo dedicato: pagine extra o mancanti, più ordini, riferimenti a mail, codici generici, doppia UM, inerti in tonnellate, riserve a mano, pesata Manini, etichetta con "Mov."
- Catalogo di 13 eccezioni (E01–E13): E01–E03 ed E10–E13 nascono dai controlli dopo l'estrazione, E04–E09 dal matching
- Ipotesi H2 e H13–H16: codice Manini a 10 cifre, ordine a 6 cifre, tolleranza peso ±1%, soglia di 60 giorni sulla data, staging AS400 come sottoinsieme dello schema

## Numeri

- 8 controlli deterministici (V1–V8) prima del matching
- 13 codici di eccezione
- Tolleranza peso tra DDT e pesata ±1% (ipotesi H14)

## Decisioni e azioni

- La sezione `abbinamento` la compila solo il matching deterministico, mai l'estrazione
- Il flusso Power Automate converte la versione piatta in quella canonica
- `esempi_ddt.json` (5 DDT con segnaposto) è superato dalla verità completa del benchmark ed è stato eliminato il 23/10

## Versioni

- 03_schema_ddt.md · 2026-10-23 · prima versione (analisi del 22/10)
