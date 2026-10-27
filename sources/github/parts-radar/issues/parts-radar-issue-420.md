---
type: source-doc
source: github
family: parts-radar-issue-420
current:
  item_id: "cristian-schifone/parts-radar#420"
  uri: "github://cristian-schifone/parts-radar/issues/420"
  web_url: "https://github.com/cristian-schifone/parts-radar/issues/420"
  name: "Issue #420 · Pilot ADAC, il traguardo: test reale del flusso intero e report dei risultati"
  last_modified: 2026-10-26T15:16:56Z
versions:
  - { name: "Issue #420", item_id: "cristian-schifone/parts-radar#420", last_modified: 2026-10-26T15:16:56Z }
  - { name: "Issue #420", item_id: "cristian-schifone/parts-radar#420", last_modified: 2026-10-21T13:10:57Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-27T06:22:42Z
projects: ["[[parts-radar-sviluppo]]"]
clients: ["[[adac-bologna]]", "[[solera]]"]
topics: ["[[parts-radar]]"]
tags: []
---

# Pilot ADAC, il traguardo: test reale del flusso intero

## Riassunto

Definizione di "fatto" della milestone "Pilot ADAC" (Lorenzo, 21/10/2026): tre prove sul flusso intero e un report dei risultati. Il report serve a giustificare l'utenza Kromeda di produzione, che costa, e a dire quanto costa una richiesta. Va chiuso prima della fine della demo Kromeda, intorno al 18/11.

## Punti chiave

- Il valore sta nella catena AI: trascrizione dei vocali, comprensione e smistamento del messaggio, lettura delle foto, scelta della voce. Si misura tutta insieme: quattro anelli al 95% fanno circa l'81%
- Prova 1, controllata (verso il 04/11): il team fa da meccanico dai propri telefoni sul numero vero di 360dialog, catalogo dal vivo con 3-4 targhe; scopo, trovare i problemi d'integrazione con tre settimane di margine
- Prova 2, ascolto (dall'attivazione del numero di ADAC): la catena AI su tutto il traffico vero, il banco lavora come sempre dal telefono
- Prova 3, traffico vero con le targhe (12-17/11): catalogo dal vivo per i clienti veri, il banco guarda le proposte in dashboard; messaggi automatici spenti
- Cosa si misura: quota di richieste che arrivano al banco con targa giusta e voce giusta tra le prime tre; zero ricerche su un'auto sbagliata; precisione per anello; tempo dal messaggio alla proposta; costo per richiesta; cosa il banco conferma o corregge
- Le soglie di riuscita si fissano prima di vedere i numeri
- 26/10, primi numeri di un anello, il router sui clienti del test senza i vocali: richiesta sì/no giusta nel 93% dei gruppi, numero di pezzi nell'88%; proposte non preparate 6,6%, richieste false 8% (concentrate nella chat di gruppo di un cliente). Mancano i vocali e le soglie

## Numeri

- 17 crediti targa al 21/10; la stessa targa nello stesso giorno non consuma un altro credito
- Router sul test: circa 0,84 $ per 436 gruppi letti, 0,2 centesimi a gruppo

## Decisioni e azioni

- Fatto quando: tre prove eseguite con le chiamate registrate, soglie fissate al piano, un report unico che risponde a "la catena funziona abbastanza da giustificare Kromeda di produzione?" e "quanto costa una richiesta?"
- Prima del traffico vero: sicurezza della dashboard e del proxy, server del pilot (Cristian), allarme sulla Coexistence, manuale del banco, prova vera della Coexistence

## Versioni

- Issue #420 · 2026-10-26 · commento coi primi numeri del router sui clienti del test; testo della issue invariato
- Issue #420 · 2026-10-21 · prima lettura nel vault
