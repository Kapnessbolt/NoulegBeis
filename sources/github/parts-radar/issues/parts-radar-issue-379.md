---
type: source-doc
source: github
family: parts-radar-issue-379
current:
  item_id: "cristian-schifone/parts-radar#379"
  uri: "github://cristian-schifone/parts-radar/issues/379"
  web_url: "https://github.com/cristian-schifone/parts-radar/issues/379"
  name: "Issue #379 · Pilot ADAC: ordine dei lavori verso il test reale (rifatto il 21/10)"
  last_modified: 2026-10-26T08:49:21Z
versions:
  - { name: "Issue #379", item_id: "cristian-schifone/parts-radar#379", last_modified: 2026-10-26T08:49:21Z }
  - { name: "Issue #379", item_id: "cristian-schifone/parts-radar#379", last_modified: 2026-10-25T23:26:55Z }
  - { name: "Issue #379", item_id: "cristian-schifone/parts-radar#379", last_modified: 2026-10-22T13:55:33Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-27T06:22:42Z
projects: ["[[parts-radar-sviluppo]]"]
clients: ["[[adac-bologna]]", "[[solera]]"]
topics: ["[[parts-radar]]"]
tags: []
---

# Pilot ADAC: ordine dei lavori verso il test reale

## Riassunto

Issue di pianificazione della milestone "Pilot ADAC", rifatta il 21/10/2026 con Lorenzo. Fissa il traguardo (il test reale della #420, prima della scadenza della demo Kromeda intorno al 18/11) e un piano in quattro settimane, più i passi fuori dal codice che sono di Lorenzo e di [[cristian-schifone]]. Rifatta perché dal 14/10 la catena AI non era avanzata e mancava una definizione di "fatto".

## Punti chiave

- Test in due tempi: prima una prova controllata (il team fa da meccanico, inizio novembre, 3-4 targhe), poi il traffico vero di ADAC con le targhe che restano
- Modalità ascolto: il numero di ADAC in Coexistence si attiva presto, la catena AI gira su tutto il traffico vero, catalogo e messaggi automatici solo per i clienti abilitati
- Chiarimenti automatici dell'AI al meccanico accesi nella prova controllata, spenti sul traffico vero finché il router non ha numeri
- Dopo la demo i test continuano sulle chiamate registrate
- Fuori dal percorso del pilot, nella milestone "Prima della produzione": brand e collasso articoli, CI, veicolo sbagliato, dataset completo, messaggi oltre le 24 ore
- 22/10: entra la #430 (estrazione strutturata di posizione, lato, preferenza, telaio), in settimana 3; la sua seconda parte è la prima cosa che esce se la settimana slitta
- Settimana 1 (22-28/10), sbloccare i dati: etichette delle chat a mano da Lorenzo, targa dei pezzi aggiunti, giro dal vivo degli alberi Kromeda. Router già fatto in anticipo il 22/10. Al 26/10: etichette di sviluppo fatte (810 gruppi) e riviste con la misura del router, prompt di router ed estrazione congelati; etichettatore Opus tarato sulle chat di sviluppo (97 su 100 d'accordo con Lorenzo su richiesta sì/no) per le etichette del test, coi vocali di H a mano da Lorenzo; restano la voce e la misura della targa dei pezzi aggiunti
- Settimana 2 (29/10-04/11): vocali, modalità ascolto, allarme sul distacco della Coexistence, attivazione del numero di ADAC col banco presente, prova controllata verso il 04/11
- Settimana 3 (05-11/11): foto, chiarimenti dell'AI, suggerimenti all'operatore, confronto finale dei modelli
- Settimana 4 (12-17/11): sicurezza della dashboard, manuale del banco, server del pilot, traffico vero con le targhe e report dei risultati

## Numeri

- 17 crediti targa al 21/10
- Prova controllata verso il 04/11; traffico vero nella settimana 12-17/11; demo Kromeda fino a circa il 18/11

## Decisioni e azioni

Passi fuori dal codice (aperti al 26/10, invariati dal 22/10):
- 360dialog: scegliere Partner o Regular. È sul percorso critico (Lorenzo)
- Foto delle officine da ADAC (in corso)
- Numeri WhatsApp delle officine registrati come clienti attivi
- Consenso di ADAC al trattamento dal vivo coi fornitori (LLM, trascrizione, 360dialog)
- Server del pilot raggiungibile dal webhook, e cosa fa già il proxy (Cristian)
- Avviso a Cristian: invio WhatsApp acceso nello Step 1, migration 075-081, ascolto sul numero di ADAC
- Kromeda di produzione: BlueAge sul piano commerciale, coi risultati della #420
- Brand preferiti di ADAC (in attesa)

## Versioni

- Issue #379 · 2026-10-26 · settimana 1: etichettatore Opus tarato per le etichette del test; passi fuori dal codice invariati
- Issue #379 · 2026-10-25 · avanzamento della settimana 1: etichette di sviluppo fatte e riviste, prompt congelati; passi fuori dal codice invariati
- Issue #379 · 2026-10-22 · prima lettura nel vault
