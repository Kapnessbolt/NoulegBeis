---
type: source-doc
source: attachment
family: blueage-automation-entrata-merci
current:
  item_id: "AAMkAGMyY2M5ZTczLTYwNDEtNGZiOC1iYjJjLTFhZjJhOGY1YjFiMQBGAAAAAADRF2aJ18MKT6wbnyNtwv9jBwCNJoMhLsxPT4EkGUihNeQOAAAAAAEMAACNJoMhLsxPT4EkGUihNeQOAAA_w-NxAAABEgAQAANNK-MYC1VDuJ_gxvMPiWk="
  uri: "mail:///messages/AAMkAGMyY2M5ZTczLTYwNDEtNGZiOC1iYjJjLTFhZjJhOGY1YjFiMQBGAAAAAADRF2aJ18MKT6wbnyNtwv9jBwCNJoMhLsxPT4EkGUihNeQOAAAAAAEMAACNJoMhLsxPT4EkGUihNeQOAAA_w-NxAAA%3D/attachments/AAMkAGMyY2M5ZTczLTYwNDEtNGZiOC1iYjJjLTFhZjJhOGY1YjFiMQBGAAAAAADRF2aJ18MKT6wbnyNtwv9jBwCNJoMhLsxPT4EkGUihNeQOAAAAAAEMAACNJoMhLsxPT4EkGUihNeQOAAA_w-NxAAABEgAQAANNK-MYC1VDuJ_gxvMPiWk%3D"
  web_url: ""
  name: "BlueAge_Automation_Entrata_merci_v3.pptx"
  last_modified: 2026-10-21T19:35:37Z
versions:
  - { name: "BlueAge_Automation_Entrata_merci_v3.pptx", item_id: "AAMkAGMyY2M5ZTczLTYwNDEtNGZiOC1iYjJjLTFhZjJhOGY1YjFiMQBGAAAAAADRF2aJ18MKT6wbnyNtwv9jBwCNJoMhLsxPT4EkGUihNeQOAAAAAAEMAACNJoMhLsxPT4EkGUihNeQOAAA_w-NxAAABEgAQAANNK-MYC1VDuJ_gxvMPiWk=", last_modified: 2026-10-21T19:35:37Z }
  - { name: "BlueAge_Automation_Entrata_merci_2.pptx", item_id: "AAMkAGMyY2M5ZTczLTYwNDEtNGZiOC1iYjJjLTFhZjJhOGY1YjFiMQBGAAAAAADRF2aJ18MKT6wbnyNtwv9jBwCNJoMhLsxPT4EkGUihNeQOAAAAAAEMAACNJoMhLsxPT4EkGUihNeQOAAA_w-NqAAABEgAQAIDuYgYT9vNBoFGvZ00RSBU=", last_modified: 2026-10-20T17:10:40Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T15:21:46Z
projects: ["[[corso-ai-manini]]"]
clients: ["[[manini]]"]
topics: ["[[ai-nei-processi]]"]
tags: [caso, automazione, entrata-merci, agenti, microsoft-365]
---

# Entrata merci: dal documento di trasporto cartaceo all'agente AI

## Riassunto

Presentazione BlueAge Automation di 6 slide (ottobre 2026) preparata da [[leonardo-pinsone]] sul caso dell'entrata merci di [[manini]], anonimizzato come "industria manifatturiera da circa 100 M€" ([[automazione-entrata-merci-caso-manini]]). Descrive il processo attuale (documenti di trasporto cartacei, diversi per fornitore, registrati a mano sull'AS400 con errori che emergono in fattura dopo un mese), il processo futuro con un agente che legge, abbina e prepara mentre le persone decidono sulle eccezioni, il confronto prima/dopo in ore ed euro e l'architettura tutta su Microsoft 365. Le tre leve dell'approccio sono reengineering, orchestrazione e AI applicata ([[ai-nei-processi]]). È il caso del laboratorio del gruppo sistemi informativi nel [[corso-ai-manini]] e corrisponde all'intervento 4A della [[manini-relazione-processi-gestione-materiali]].

## Punti chiave

- **Oggi**: fino a 2 giorni con merce in magazzino senza traccia a sistema; circa 10 minuti a documento per cercare l'ordine e tradurre i codici; errori di registrazione scoperti in fattura dopo circa 30 giorni, con amministrazione, acquisti e magazzino coinvolti per ricostruire l'abbinamento.
- **Domani**: il documento entra il giorno stesso da posta o scansione; il magazzino dà un solo OK per le righe pronte; gli acquisti vedono solo le eccezioni e ogni risposta arricchisce la tabella dei codici; l'amministrazione riceve abbinamenti più puliti e una nota per ogni fattura che non torna; la scheda fornitore si aggiorna ogni mese.
- **Tecnologia**: casella condivisa e SharePoint in ingresso, AI Builder per la lettura, agente in Copilot Studio, approvazioni ed eccezioni in Teams, scrittura sull'AS400 con connettore DB2 e gateway dati locale (a cura dei sistemi informativi del cliente), Power Automate come orchestratore, archivio su SharePoint, scheda fornitore in Power BI.
- I numeri sono dichiarati da validare: caso in progettazione su un'azienda cliente, documenti reali con dati identificativi oscurati.

## Numeri

- Volume: circa 11.160 documenti all'anno (930 al mese su due stabilimenti), esclusi i documenti consegnati in cantiere.
- Oggi: 1.860 ore all'anno, circa 1,2 persone a tempo pieno, circa 65.000 € all'anno.
- Domani prudente: 910 ore, 0,6 persone (60% senza eccezioni a 1,5 minuti, 40% con eccezione a 10 minuti). Domani spinto: 520 ore, 0,3 persone (80% a 1 minuto, 20% a 10 minuti).
- Risparmio: 950-1.340 ore all'anno, 33.000-47.000 €, 0,6-0,8 persone restituite al magazzino. Ipotesi: 35 €/ora, 1.600 ore per persona.

## Decisioni e azioni

- Da presentare a voce, senza far girare le slide e senza citare il cliente ([[automazione-entrata-merci-caso-manini]]).

## Versioni

- BlueAge_Automation_Entrata_merci_v3.pptx · 2026-10-21 · numeri rivisti con le risposte di Manini: 11.000 documenti all'anno invece di 7.500, 10 minuti a documento invece di 15, conto limitato alla sola registrazione (lo sblocco fatture esce dal calcolo perché non misurato); risparmio da 50-65k a 33-47k € all'anno
- BlueAge_Automation_Entrata_merci_2.pptx · 2026-10-20 · prima versione: 7.500 documenti, una fattura su cinque bloccata, 2.275 ore oggi (1.875 registrazione + 400 sblocco fatture), risparmio 1.400-1.850 ore e 50.000-65.000 € all'anno
