---
type: source-doc
source: github
family: parts-radar-issue-379
current:
  item_id: "cristian-schifone/parts-radar#379"
  uri: "github://cristian-schifone/parts-radar/issues/379"
  web_url: "https://github.com/cristian-schifone/parts-radar/issues/379"
  name: "Issue #379 · Pilot ADAC: ordine dei lavori verso il test reale (rifatto il 21/10, rivisto il 27/10)"
  last_modified: 2026-10-27T17:13:27Z
versions:
  - { name: "Issue #379", item_id: cristian-schifone/parts-radar#379, last_modified: 2026-10-27T17:13:27Z }
  - { name: "Issue #379", item_id: cristian-schifone/parts-radar#379, last_modified: 2026-10-26T08:49:21Z }
  - { name: "Issue #379", item_id: cristian-schifone/parts-radar#379, last_modified: 2026-10-25T23:26:55Z }
  - { name: "Issue #379", item_id: cristian-schifone/parts-radar#379, last_modified: 2026-10-22T13:55:33Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-28T06:23:42Z
projects: ["[[parts-radar-sviluppo]]"]
clients: ["[[adac-bologna]]", "[[solera]]"]
topics: ["[[parts-radar]]"]
tags: []
---

# Pilot ADAC: ordine dei lavori verso il test reale

## Riassunto

Issue di pianificazione della milestone "Pilot ADAC", rifatta il 21/10/2026 con Lorenzo e rivista il 27/10 per allinearla al lavoro fatto. Fissa il traguardo (il test reale della #420, prima della scadenza della demo Kromeda intorno al 18/11) e un piano in quattro settimane, più i passi fuori dal codice che sono di Lorenzo e di [[cristian-schifone]]. Rifatta perché dal 14/10 la catena AI non era avanzata e mancava una definizione di "fatto".

## Punti chiave

- Test in due tempi: prima una prova controllata (il team fa da meccanico, inizio novembre, 3-4 targhe), poi il traffico vero di ADAC con le targhe che restano
- Modalità ascolto: il numero di ADAC in Coexistence si attiva presto, la catena AI gira su tutto il traffico vero, catalogo e messaggi automatici solo per i clienti abilitati
- Chiarimenti automatici dell'AI al meccanico accesi nella prova controllata, spenti sul traffico vero finché il router non ha numeri
- Dopo la demo i test continuano sulle chiamate registrate
- Fuori dal percorso del pilot, nella milestone "Prima della produzione": brand e collasso articoli, CI, veicolo sbagliato, dataset completo, messaggi oltre le 24 ore; dopo i numeri del pilot anche la scelta della targa da ascoltare da parte del banco (#482)
- Revisione del 27/10: il piano della #420 (scenari, soglie fissate prima dei numeri dei vocali, scheletro del report) passa in testa alla settimana 2; l'allarme sul distacco della Coexistence va dopo l'attivazione del numero, tarato sulle eco vere, e deve funzionare entro circa 10 giorni da lì; se la settimana 3 slitta escono prima la seconda parte della #430, poi il pezzo senza etichetta in foto
- Settimana 1 (22-28/10) fatta, salvo la voce: etichette di sviluppo e del test, targa dei pezzi aggiunti chiusa con la misura (taratura della finestra sul traffico del pilot)
- Settimana 2 (29/10-04/11): già fatti router, vocali nel servizio (doppia lettura Soniox più Gemini, resta l'accensione) e modalità ascolto; restano il piano della #420, la misura dei vocali sul test, la voce, un giro dal vivo degli alberi Kromeda, la nota per il banco, l'attivazione del numero di ADAC e la prova controllata
- Settimana 3 (05-11/11): allarme Coexistence, estrazione strutturata, foto, chiarimenti dell'AI (anche la domanda al meccanico sulla targa da ascoltare), suggerimenti all'operatore, confronto finale dei modelli
- Settimana 4 (12-17/11): sicurezza della dashboard, manuale del banco, server del pilot, traffico vero con le targhe, taratura della finestra di recupero della targa, report dei risultati

## Numeri

- 17 crediti targa al 21/10
- Prova controllata verso il 04/11; traffico vero nella settimana 12-17/11; demo Kromeda fino a circa il 18/11

## Decisioni e azioni

Passi fuori dal codice (al 27/10):
- 360dialog: scegliere Partner o Regular. È sul percorso critico (Lorenzo)
- Foto delle officine da ADAC (in corso)
- Numeri WhatsApp delle officine registrati come clienti attivi
- Consenso scritto di ADAC al trattamento dal vivo coi fornitori: LLM, trascrizione (deve nominare Soniox e Google), 360dialog
- Trascrizione a nome di BlueAge: progetto Soniox UE (regione UE da far approvare, contratto sui dati dalla Console) e progetto Google; poi l'accensione
- Server del pilot raggiungibile dal webhook, e cosa fa già il proxy (Cristian)
- Canale degli allarmi (Cristian, D4: email, Telegram...): serve all'allarme sulla Coexistence e a tutti gli altri
- Avviso a Cristian (invio WhatsApp nello Step 1, migration fino alla 086, variabili della trascrizione, ascolto sul numero di ADAC): spuntato, mandato da Lorenzo il 27/10, in attesa di risposta
- Kromeda di produzione: BlueAge sul piano commerciale, coi risultati della #420
- Brand preferiti di ADAC (in attesa)
- Da decidere (Lorenzo): le targhe nel vecchio formato provinciale

## Versioni

- Issue #379 · 2026-10-27 · revisione del 27/10: piano della #420 in testa alla settimana 2, allarme Coexistence dopo l'attivazione, settimana 1 chiusa salvo la voce; nuovi passi fuori dal codice (trascrizione a nome di BlueAge, canale degli allarmi), avviso a Cristian spuntato
- Issue #379 · 2026-10-26 · settimana 1: etichettatore Opus tarato per le etichette del test; passi fuori dal codice invariati
- Issue #379 · 2026-10-25 · avanzamento della settimana 1: etichette di sviluppo fatte e riviste, prompt congelati; passi fuori dal codice invariati
- Issue #379 · 2026-10-22 · prima lettura nel vault
