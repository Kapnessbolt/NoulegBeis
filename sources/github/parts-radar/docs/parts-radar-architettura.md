---
type: source-doc
source: github
family: parts-radar-architettura
current:
  item_id: "cristian-schifone/parts-radar:docs/architettura.md"
  uri: "github://cristian-schifone/parts-radar/docs/architettura.md@e5926bacdd88656f9091a65e1eab6fc26b9b9dd9"
  web_url: "https://github.com/cristian-schifone/parts-radar/blob/main/docs/architettura.md"
  name: "docs/architettura.md"
  last_modified: 2026-10-30T15:15:52Z
versions:
  - { name: docs/architettura.md@e5926ba, item_id: cristian-schifone/parts-radar:docs/architettura.md, last_modified: 2026-10-30T15:15:52Z }
  - { name: docs/architettura.md@2be8540, item_id: cristian-schifone/parts-radar:docs/architettura.md, last_modified: 2026-10-29T22:57:06Z }
  - { name: docs/architettura.md@733d0a6, item_id: cristian-schifone/parts-radar:docs/architettura.md, last_modified: 2026-10-28T23:22:29Z }
  - { name: docs/architettura.md@53f469d, item_id: cristian-schifone/parts-radar:docs/architettura.md, last_modified: 2026-10-27T22:36:39Z }
  - { name: docs/architettura.md@48bd26c, item_id: cristian-schifone/parts-radar:docs/architettura.md, last_modified: 2026-10-26T23:47:59Z }
  - { name: docs/architettura.md@fe70fa4, item_id: cristian-schifone/parts-radar:docs/architettura.md, last_modified: 2026-10-25T23:55:16Z }
  - { name: docs/architettura.md@61b833c, item_id: cristian-schifone/parts-radar:docs/architettura.md, last_modified: 2026-10-22T16:51:29Z }
also_at: []
status: active
partial: true
ingested_at: 2026-10-31T06:23:46Z
projects: ["[[parts-radar-sviluppo]]"]
clients: ["[[adac-bologna]]", "[[solera]]"]
topics: ["[[parts-radar]]"]
tags: []
---

# Parts Radar · architettura e stato del sistema

## Riassunto

Documento di stato del repo di sviluppo: com'è fatto il sistema oggi, a che punto sono le fasi, le decisioni aperte e i rischi. Si aggiorna a ogni PR (la testata dice lo stato del giorno). Nel vault si leggono solo §1 (scopo), §5 (stato e sequenza), §8 (decisioni aperte) e §9 (rischi); componenti e decisioni tecniche in vigore (§4, §6) restano nel repo. Stato letto: 31/10/2026, dopo il benchmark del router per modello (30/10) e le prime misure del ciclo a sessione unica.

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
- 27/10: la targa di un pezzo aggiunto dopo (#346) chiusa con la misura sulle etichette; la finestra di recupero resta 30 minuti e si tara sul traffico del pilot. Nei gruppi con un vocale la targa si recupera solo per citazione
- 27/10: doppia lettura dei vocali, Soniox UE primo motore e Gemini di controllo; una targa che viene solo da un vocale vale se le due letture coincidono, altrimenti il gruppo va al banco come «targa da ascoltare». Tetto di spesa di 1 $ al giorno. Trascrizione ancora spenta
- 27/10: regole delle prove del pilot scritte e congelate (scenari, soglie, come si misura la catena) e scheletro del report unico; la prova controllata segue l'attivazione del numero di ADAC, prima c'è una prova a secco
- 28/10: prova a secco fatta, la prima volta del flusso intero dal vivo (dal webhook alla dashboard, ricerca targa dalle registrazioni): 38 messaggi, 39 richieste, 0 errori, 0 crediti targa, 0,12 $; 30 componenti su 40 alla proposta giusta o al banco col motivo giusto. I 10 che non tornano aprono cinque issue; quattro chiuse in giornata (codice del meccanico per codice col controllo sull'auto, lessico di frizione e filtri, varianti della stessa voce al banco come alternative, lato gemello sugli affini), resta il motivo dei kit
- 28/10: misura dei vocali sul test: targa confermata giusta 72,9% (soglia 65%), da ascoltare 20,4% (soglia 25%), codici dettati esatti 33,3% (soglia 80%). Il cancello delle targhe dai vocali è caduto su un gruppo; corretto in giornata (targa letta a metà → gruppo da ascoltare: 0 targhe sbagliate, ma da ascoltare sale al 27,1%, sopra soglia). Codici dettati portati a 16 su 20 (80%, al limite). Trascrizione ancora spenta
- 29/10: fornitore WhatsApp deciso (D47): 360dialog Regular a nome di ADAC, coi vincoli del webhook senza firma da verificare prima dell'attivazione del numero
- 29/10: misurata la voce sulle chat reali, l'ultimo anello della catena senza misura: voce giusta tra le prime tre 94,9% sullo sviluppo e 93,8% sul test (soglia 90%), voce sbagliata data per sicura 1,4% e 0,6% (soglia 2%). Il lessico dei meccanici aggiunto al prompt migliora lo sviluppo e sul test è neutro (93,6% e 0,7%)
- 29/10: metodo di lavoro, ogni feature o fix in una sessione sola con piano e documenti affidati a sotto-agenti; il risparmio si misura sulla prima feature (D50)
- 30/10: benchmark del router per modello sul test: Sonnet 5.5, Opus 5.5 e Haiku a sforzo alto non spostano le soglie del pilot; il router resta Haiku 5.5 (richieste false 6,1%, proposte non preparate 4,2%, soglie 5%). Il confronto per contratto della #319 resta aperto, con l'estrazione con Sonnet e Opus nella #526

## Numeri

- Demo Kromeda prorogata da Solera il 16/10: scade intorno al 18/11. Dopo restano solo le risposte registrate
- Fase 0: 80% dei casi risolti in modo deterministico, 86% con i default, 14% all'operatore (21-30% su VW e BMW); golden set 43 richieste raggiungibili su 51
- Gruppi WhatsApp: 3 clienti ADAC su 10 scrivono da un gruppo, che nessun fornitore porta all'API

## Decisioni e azioni

Decisioni aperte (§8) che toccano il livello di progetto:
- D1 · modello commerciale e di installazione (issue #145): Lorenzo e Cristian, blocca il modello del primo cliente
- D43 · dataset delle chat reali (Lorenzo): etichette di sviluppo e del test e misura del router fatte (25-26/10); il 29/10 anche la voce (etichette e misura sulle chat, poi il lessico). Resta da decidere come il simulatore legge le etichette della voce, e se etichettare lo storico di altri due clienti
- D13 · data del pilot e partenza direttamente sul nuovo stack: Lorenzo con ADAC (chiesta a Luca Degli Esposti il 22/10)
- D19 · mappatura dei brand di ADAC sui codici listino Kromeda: senza, la proposta esce in ordine alfabetico. Lista dei brand e listini (CONTINENTAL, DIPA, DEPO, Pierburg, AJUSA) chiesti a Luca il 22/10. Qui «blocca il pilot», mentre l'ordine dei lavori la mette «prima della produzione»: da allineare (proposta: basta l'ordine di fascia, l'operatore sceglie il brand)
- D34 · chi cambia sconti, margini e fidi dei clienti (oggi solo gli ADMIN): da confermare con ADAC
- D44 · vocali (1.233 in 9,6 ore nelle chat reali): integrazione fatta il 27/10, spenta; dalla sera del 27/10 doppia lettura, Soniox UE primo motore e Gemini 3.5 Transcribe di controllo; misurata sul test il 28/10 (sopra). Per accendere: il consenso di ADAC che nomini Soniox e Google (ogni vocale va a tutti e due), il progetto Soniox UE a nome di BlueAge (regione UE da far approvare a Soniox), il contratto sul trattamento dei dati con Soniox, il progetto Google a nome di BlueAge
- D41 · targa dei pezzi aggiunti dopo: chiusa la misura il 27/10; resta la taratura della finestra di recupero sul traffico del pilot (#472). Il banco che sceglie la targa da ascoltare e fa ripartire il gruppo è la #482, dopo i numeri del pilot
- D48 · targhe nel vecchio formato provinciale (2 casi su 550 gruppi del test): oggi nessun passo le accetta; proposta «dritte al banco», da decidere una volta (Lorenzo)
- D45 · gruppi WhatsApp: chiesto ad ADAC se quei clienti passano alla chat singola
- D46 · hosting e rete del webhook (Cristian): un server con tutto lo stack; è anche la condizione per accendere l'invio in produzione
- D50 · il ciclo a sessione unica fa risparmiare davvero? (Lorenzo) Prime misure del 30/10: la prima feature non è confrontabile (26,78 $ di misure dentro la sessione), il primo fix costa come prima (10,58 $ contro 10,47); il pianificatore costa quanto o più del piano di prima, per riscritture e cache scaduta, ora corrette. Restano da misurare una feature senza giri a pagamento e da decidere il pianificatore sui fix piccoli
- D47 · fornitore WhatsApp: 360dialog con la Coexistence (19/10); il 29/10 Lorenzo sceglie il piano Regular a nome di ADAC (Partner di BlueAge dal secondo cliente). Il webhook senza firma è un rischio accettato coi vincoli V1-V8, da verificare prima dell'attivazione (Cristian per server e proxy, Lorenzo per IP di 360dialog, segreto e controlli del servizio); il contratto sui dati con 360dialog lo accetta ADAC
- Domande a Solera ancora da mandare (Lorenzo): cache oltre le 24 ore, versioni degli affini, copia del dizionario, fasce di consumo, URL delle foto (D12)
- Nodi aperti fuori dal codice: Rihag/Cati per lo Step 2 e nome e API del gestionale ADAC per lo Step 3 (chiesti a Luca il 22/10); messaggi fuori orario; segreti e backup in produzione

Rischi principali (§9): scadenza della demo Kromeda; webhook di 360dialog senza firma sul Regular (accettato coi vincoli V1-V8); superamento della fascia di chiamate (account sospeso fino al mattino dopo); cache oltre le 24 ore in tensione col contratto Solera; brand non mappati; gruppi WhatsApp fuori dall'API; foto delle officine da raccogliere da ora.

## Versioni

- docs/architettura.md@e5926ba · 2026-10-30 · §8: D38 e D43 col benchmark del router per modello (resta Haiku 5.5), D50 con le prime misure del ciclo unico; §1, §5 e §9 invariati
- docs/architettura.md@2be8540 · 2026-10-29 · §8: D43 con la voce misurata sulle chat e il lessico (29/10), nuova D50 sul risparmio del ciclo a sessione unica; §1, §5 e §9 invariati
- docs/architettura.md@733d0a6 · 2026-10-29 · §5, §8 e §9: prova a secco del pilot e correzioni del 28/10, misura dei vocali sul test (cancello caduto e rientrato, da ascoltare sopra soglia), codici dettati all'80%; D47 decisa (Regular a nome di ADAC, vincoli V1-V8 del webhook, anche nei rischi); §1 invariato
- docs/architettura.md@53f469d · 2026-10-27 · §5 e §8: misura della targa dei pezzi aggiunti chiusa (D41), doppia lettura dei vocali con Soniox primo motore e targa da ascoltare (D44, condizioni di accensione), regole delle prove del pilot; §1 e §9 invariati
- docs/architettura.md@48bd26c · 2026-10-27 · §5 e §8: etichette del test e misura del router fatte (D43), motore dei vocali deciso e trascrizione integrata ma spenta (D44), nuova D48 sulle targhe nel vecchio formato; §1 e §9 invariati
- docs/architettura.md@fe70fa4 · 2026-10-26 · §8: D43 aggiornata con la revisione delle etichette di sviluppo e i prompt congelati; il resto delle parti lette invariato
- docs/architettura.md@61b833c · 2026-10-22 · prima lettura nel vault (§1, §5, §8, §9)
