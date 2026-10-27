---
type: source-doc
source: github
family: parts-radar-architettura
current:
  item_id: "cristian-schifone/parts-radar:docs/architettura.md"
  uri: "github://cristian-schifone/parts-radar/docs/architettura.md@48bd26c78c4f24ec80d6e25222a83a0ae99b189b"
  web_url: "https://github.com/cristian-schifone/parts-radar/blob/main/docs/architettura.md"
  name: "docs/architettura.md"
  last_modified: 2026-10-26T23:47:59Z
versions:
  - { name: docs/architettura.md@48bd26c, item_id: cristian-schifone/parts-radar:docs/architettura.md, last_modified: 2026-10-26T23:47:59Z }
  - { name: docs/architettura.md@fe70fa4, item_id: cristian-schifone/parts-radar:docs/architettura.md, last_modified: 2026-10-25T23:55:16Z }
  - { name: docs/architettura.md@61b833c, item_id: cristian-schifone/parts-radar:docs/architettura.md, last_modified: 2026-10-22T16:51:29Z }
also_at: []
status: active
partial: true
ingested_at: 2026-10-27T06:22:42Z
projects: ["[[parts-radar-sviluppo]]"]
clients: ["[[adac-bologna]]", "[[solera]]"]
topics: ["[[parts-radar]]"]
tags: []
---

# Parts Radar · architettura e stato del sistema

## Riassunto

Documento di stato del repo di sviluppo: com'è fatto il sistema oggi, a che punto sono le fasi, le decisioni aperte e i rischi. Si aggiorna a ogni PR (la testata dice lo stato del giorno). Nel vault si leggono solo §1 (scopo), §5 (stato e sequenza), §8 (decisioni aperte) e §9 (rischi); componenti e decisioni tecniche in vigore (§4, §6) restano nel repo. Stato letto: 27/10/2026, dopo l'integrazione della trascrizione dei vocali nel servizio (spenta).

## Punti chiave

- Scopo: automatizzare gli ordini ricambi di [[adac-bologna]], circa 100 richieste al giorno via WhatsApp dai meccanici (targa e descrizione del pezzo)
- Tre step: 1) identifica veicolo e pezzo, trova codici originali ed equivalenti a listino e li propone all'operatore, che valida, ordina e risponde a mano (in costruzione); 2) ordine automatico sul portale del fornitore; 3) aggiornamento del gestionale. Step 2 e 3 non iniziati
- Fuori dal sistema: la scelta commerciale finale (resta al banco) e i casi che solo il VIN risolve (il banco usa PartsLink24)
- Fasi della migrazione a Python e Kromeda tutte chiuse in sviluppo: misura (26/09), scheletro, catalogo e ingestion (03-04/10), cutover (05/10), installazione da zero sul compose di produzione (15-16/10), fornitori WhatsApp (16-20/10). n8n uscito il 04/10
- Lavoro verso il pilot nella milestone "Pilot ADAC", con l'ordine dei lavori nella issue #379 e il traguardo nella #420
- 22/10: router in ingresso acceso (separa i messaggi che non chiedono un pezzo) e modalità ascolto (catalogo dal vivo e messaggi automatici attivabili cliente per cliente, spenti di default, con una riserva di 15 crediti targa)
- 25-26/10: le 810 etichette di sviluppo delle chat reali corrette con Lorenzo; prompt di router ed estrazione congelati
- 26/10: etichette del test fatte (550 gruppi dei clienti E, G, H, J: etichettatore Opus tarato sulle chat di sviluppo, vocali di H a mano da Lorenzo) e prima misura del router sul test; della #345 resta «la voce»
- 26-27/10: vocali, motore scelto Gemini 3.5 Transcribe (Soniox e Speechmatics provati, nessuno lo batte), alfabeto delle città con una tabella fissa; il 27/10 la trascrizione entra nel servizio ma resta spenta. Mancano la misura finale sul test e l'accensione

## Numeri

- Demo Kromeda prorogata da Solera il 16/10: scade intorno al 18/11. Dopo restano solo le risposte registrate
- Fase 0: 80% dei casi risolti in modo deterministico, 86% con i default, 14% all'operatore (21-30% su VW e BMW); golden set 43 richieste raggiungibili su 51
- Gruppi WhatsApp: 3 clienti ADAC su 10 scrivono da un gruppo, che nessun fornitore porta all'API

## Decisioni e azioni

Decisioni aperte (§8) che toccano il livello di progetto:
- D1 · modello commerciale e di installazione (issue #145): Lorenzo e Cristian, blocca il modello del primo cliente
- D43 · dataset delle chat reali (Lorenzo): etichette di sviluppo riviste il 25-26/10, etichette del test e misura del router sul test fatte il 26/10 (revisione affidata a Opus su delega di Lorenzo); resta «la voce» e la lettura delle etichette nella misura della targa dei pezzi aggiunti
- D13 · data del pilot e partenza direttamente sul nuovo stack: Lorenzo con ADAC (chiesta a Luca Degli Esposti il 22/10)
- D19 · mappatura dei brand di ADAC sui codici listino Kromeda: senza, la proposta esce in ordine alfabetico. Lista dei brand e listini (CONTINENTAL, DIPA, DEPO, Pierburg, AJUSA) chiesti a Luca il 22/10. Blocca il pilot
- D34 · chi cambia sconti, margini e fidi dei clienti (oggi solo gli ADMIN): da confermare con ADAC
- D44 · vocali (1.233 in 9,6 ore nelle chat reali): motore deciso il 26/10, Gemini 3.5 Transcribe; integrazione fatta il 27/10, spenta. Restano aperti il consenso di ADAC per la produzione e il progetto Google a nome di BlueAge con un account di servizio (oggi è su un account personale)
- D48 · targhe nel vecchio formato provinciale (2 casi su 550 gruppi del test): oggi nessun passo le accetta; da capire se Kromeda le trova e come le tratta il flusso (Lorenzo, priorità bassa)
- D45 · gruppi WhatsApp: chiesto ad ADAC se quei clienti passano alla chat singola
- D46 · hosting e rete del webhook (Cristian): un server con tutto lo stack; è anche la condizione per accendere l'invio in produzione
- D47 · fornitore WhatsApp: 360dialog con la Coexistence (19/10); resta da scegliere il piano Regular o Partner prima di attivare il numero di ADAC
- Domande a Solera ancora da mandare (Lorenzo): cache oltre le 24 ore, versioni degli affini, copia del dizionario, fasce di consumo, URL delle foto (D12)
- Nodi aperti fuori dal codice: Rihag/Cati per lo Step 2 e nome e API del gestionale ADAC per lo Step 3 (chiesti a Luca il 22/10); messaggi fuori orario; segreti e backup in produzione

Rischi principali (§9): scadenza della demo Kromeda; superamento della fascia di chiamate (account sospeso fino al mattino dopo); cache oltre le 24 ore in tensione col contratto Solera; brand non mappati; gruppi WhatsApp fuori dall'API; foto delle officine da raccogliere da ora.

## Versioni

- docs/architettura.md@48bd26c · 2026-10-27 · §5 e §8: etichette del test e misura del router fatte (D43), motore dei vocali deciso e trascrizione integrata ma spenta (D44), nuova D48 sulle targhe nel vecchio formato; §1 e §9 invariati
- docs/architettura.md@fe70fa4 · 2026-10-26 · §8: D43 aggiornata con la revisione delle etichette di sviluppo e i prompt congelati; il resto delle parti lette invariato
- docs/architettura.md@61b833c · 2026-10-22 · prima lettura nel vault (§1, §5, §8, §9)
