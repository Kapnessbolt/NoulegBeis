---
type: source-doc
source: onedrive
family: prompt-estrazione-ddt
current:
  item_id: 013UYHJHAYMOFSUFLWPFEKGISCDSRECKIU
  uri: file:///b!2fHSoBOOE0aRvS_GntS6s6RJcyNKjAJMiRtoiZ6n5xzp8hWMRRoMQKOVYgftTbzT/013UYHJHAYMOFSUFLWPFEKGISCDSRECKIU
  web_url: https://blueagesrl-my.sharepoint.com/personal/lorenzo_curione_blueage_it/Documents/BlueAge/01_Materiale clienti/Manini/Progetto Automazione/Library/prompt_estrazione_ddt.md
  name: prompt_estrazione_ddt.md
  last_modified: 2026-10-25T22:14:31Z
versions:
  - { name: prompt_estrazione_ddt.md, item_id: 013UYHJHAYMOFSUFLWPFEKGISCDSRECKIU, last_modified: 2026-10-25T22:14:31Z }
  - { name: prompt_estrazione_ddt.md, item_id: 013UYHJHAYMOFSUFLWPFEKGISCDSRECKIU, last_modified: 2026-10-23T11:33:35Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-26T05:53:02Z
projects: ["[[manini-automazione-ddt]]"]
clients: ["[[manini]]"]
topics: ["[[ai-nei-processi]]"]
tags: [entrata-merci, ddt, prompt]
---

# Manini · prompt di estrazione DDT v1.1

## Riassunto

Prompt di estrazione dei DDT di [[manini-automazione-ddt]], versione 1.1 con le correzioni emerse dal benchmark ([[04-benchmark]]). Si usa in tre modi: nell'azione "Esegui un prompt" di AI Builder, nelle descrizioni dei campi del nodo Extract di Copilot Studio, oppure in Copilot Chat per la demo del [[corso-ai-manini]]. Restituisce solo un JSON conforme al template piatto dello schema ([[03-schema-ddt]]). Ritestato il 25/10/2026: 15/15 DDT pronti per il matching con il modello standard; è la versione da usare in aula IT e nel pilota.

## Punti chiave

- 15 regole: Manini è sempre il destinatario e mai il fornitore; si classificano le pagine prima di estrarre; si rifiuta se il documento è illeggibile; non si inventa (dato assente = null, lettura dubbia = campo incerto)
- Ordini Manini solo se indicati come ordine del cliente; gli ordini del fornitore e i riferimenti a mail vanno negli altri riferimenti; un ordine unico si propaga a tutte le righe
- Codice Manini solo se stampato come codice del cliente o come codice a 10 cifre nella descrizione, mai dedotto
- Normalizzazione di quantità e unità di misura, doppia quantità, dimensioni; colli e pesi stampati a 0 restano 0
- L'etichetta Manini distingue protocollo e numero "Mov."; codici e descrizioni su righe alternate si abbinano nell'ordine

## Numeri

- Regole modificate rispetto alla v1.0: 3, 5, 6, 10, 13 e 15
- Ritest del 25/10: 15/15 DDT pronti per il matching con il modello standard

## Decisioni e azioni

- [x] Ritestare la v1.1 sui 15 DDT prima di usarla in aula (25/10, [[04-benchmark]])
- Le correzioni candidate per una v1.2 sono in [[04-benchmark]] §10.4, da ritestare prima dell'uso

## Versioni

- prompt_estrazione_ddt.md · 2026-10-25 · regole invariate; l'intestazione registra il ritest del 25/10 (15/15 DDT pronti con lo standard)
- prompt_estrazione_ddt.md · 2026-10-23 · v1.1, prima versione nel vault
