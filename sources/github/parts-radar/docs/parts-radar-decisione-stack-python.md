---
type: source-doc
source: github
family: parts-radar-decisione-stack-python
current:
  item_id: "cristian-schifone/parts-radar:docs/decisione-stack-python.md"
  uri: "github://cristian-schifone/parts-radar/docs/decisione-stack-python.md@6841f618a743e1c6e5cabe8ea9a51c0a32252d4c"
  web_url: "https://github.com/cristian-schifone/parts-radar/blob/main/docs/decisione-stack-python.md"
  name: "docs/decisione-stack-python.md"
  last_modified: 2026-10-19T21:37:21Z
versions:
  - { name: "docs/decisione-stack-python.md@6841f61", item_id: "cristian-schifone/parts-radar:docs/decisione-stack-python.md", last_modified: 2026-10-19T21:37:21Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-23T18:23:22Z
projects: ["[[parts-radar-sviluppo]]"]
clients: ["[[solera]]"]
topics: ["[[parts-radar]]"]
tags: []
---

# Decisione: da n8n a un'applicazione Python

## Riassunto

Decisione presa da Lorenzo il 26/09/2026 e ratificata da [[cristian-schifone]] col lancio dello swarm di ottobre (02/10): Parts Radar diventa un servizio Python che si prende tutto il flusso (WhatsApp, OCR ed estrazione, orchestrazione, catalogo Kromeda, LLM) e n8n esce del tutto. Database e dashboard restano. Il prodotto installato è servizio Python + PostgreSQL + dashboard, un'installazione per cliente sui server di BlueAge.

## Punti chiave

- Motivo decisivo: la licenza di n8n (Sustainable Use License) ammette solo uso interno. Parts Radar si vende a più ricambisti, quindi servirebbe una licenza commerciale n8n, giudicata non sostenibile per un prodotto che parte da un pilot
- Esclusa anche la via ibrida (n8n solo per WhatsApp) e quella del server del cliente (#145): resta una zona grigia di licenza, impone l'hosting presso un cliente senza IT, non risolve gli altri problemi
- Altri motivi: tante installazioni da tenere allineate (versioni, test automatici sul golden set, revisione delle modifiche), logica Kromeda che è ragionamento sul dato, bug della piattaforma n8n già pagati, catalogo da riscrivere comunque
- Si perde la vista nodo per nodo e l'autonomia di Lorenzo sui nodi: il codice lo scrive in gran parte Claude, Lorenzo guida e verifica e tiene l'ultima parola su pipeline, LLM e prompt
- Monitoraggio tecnico solo per BlueAge, nel database dell'installazione, mai nella dashboard del cliente
- Installazione sui server BlueAge, una per cliente (single-tenant); presso il cliente solo su richiesta
- La #145 (modello commerciale) resta aperta: vale il canone, cambia dove gira il prodotto

## Numeri

- Fasi A-E: scheletro, catalogo, ingestion, cutover chiusi tra il 03 e il 05/10 in sviluppo; dismissione di n8n anticipata e fatta il 04/10
- Vincolo di calendario: demo Kromeda fino a circa il 18/11

## Decisioni e azioni

- 2026-09-26 · Python al posto di n8n per tutto il flusso (Lorenzo); ratificata da Cristian il 02/10
- 2026-10-04 · n8n fuori dal repo e dallo staging (Cristian)
- Aperte: canale degli allarmi verso il team; vista aggregata del monitoraggio al secondo cliente; data del pilot sul nuovo stack (con ADAC)

## Versioni

- docs/decisione-stack-python.md@6841f61 · 2026-10-19 · prima lettura nel vault
