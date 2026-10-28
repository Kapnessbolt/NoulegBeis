---
type: source-doc
source: github
family: parts-radar-issue-420
current:
  item_id: "cristian-schifone/parts-radar#420"
  uri: "github://cristian-schifone/parts-radar/issues/420"
  web_url: "https://github.com/cristian-schifone/parts-radar/issues/420"
  name: "Issue #420 · Pilot ADAC, il traguardo: test reale del flusso intero e report dei risultati"
  last_modified: 2026-10-27T18:02:06Z
versions:
  - { name: "Issue #420", item_id: cristian-schifone/parts-radar#420, last_modified: 2026-10-27T18:02:06Z }
  - { name: "Issue #420", item_id: cristian-schifone/parts-radar#420, last_modified: 2026-10-26T15:16:56Z }
  - { name: "Issue #420", item_id: cristian-schifone/parts-radar#420, last_modified: 2026-10-21T13:10:57Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-28T06:23:42Z
projects: ["[[parts-radar-sviluppo]]"]
clients: ["[[adac-bologna]]", "[[solera]]"]
topics: ["[[parts-radar]]"]
tags: []
---

# Pilot ADAC, il traguardo: test reale del flusso intero

## Riassunto

Definizione di "fatto" della milestone "Pilot ADAC" (Lorenzo, 21/10/2026): tre prove sul flusso intero e un report dei risultati. Il report serve a giustificare l'utenza Kromeda di produzione, che costa, e a dire quanto costa una richiesta. Va chiuso prima della fine della demo Kromeda, intorno al 18/11. Il 27/10 il piano è fatto: le regole delle prove e lo scheletro del report sono nel repo, congelate.

## Punti chiave

- Il valore sta nella catena AI: trascrizione dei vocali, comprensione e smistamento del messaggio, lettura delle foto, scelta della voce. Si misura tutta insieme: quattro anelli al 95% fanno circa l'81%
- Prova 1, controllata: il team fa da meccanico dai propri telefoni sul numero vero di 360dialog. Dal piano del 27/10: 3-4 auto nostre (almeno una del gruppo VW), 20 scenari scritti dal modo di scrivere delle chat di sviluppo, tre telefoni, un giorno solo. La prova segue l'attivazione del numero di ADAC, non la data; prima si fa una prova a secco (0 crediti, sandbox di 360dialog e servizio locale)
- Al 04/11 le foto provano l'integrazione (targa e libretto); etichetta e pezzo senza etichetta vanno al banco e si rifanno nella settimana 4, come i chiarimenti dell'AI
- Vocali nella prova: la trascrizione si accende mentre i soli clienti attivi sono i nostri numeri e si spegne prima di registrare le officine
- Prova 2, ascolto (dall'attivazione del numero di ADAC): la catena AI su tutto il traffico vero, il banco lavora come sempre dal telefono. Parte subito dopo la prova controllata
- Prova 3, traffico vero con le targhe (12-17/11): catalogo dal vivo per i clienti veri, il banco guarda le proposte in dashboard; messaggi automatici spenti
- Le chiamate Kromeda dal vivo delle prove si registrano per il replay dopo la demo
- Cosa si misura: quota di richieste che arrivano al banco con targa giusta e voce giusta tra le prime tre; il cancello, zero ricerche su un'auto sbagliata, che se cade manda al banco solo le targhe di quell'origine (vocale, recuperata, foto, scritta), non ferma il pilot; precisione per anello; tempo, costo per richiesta, cosa il banco conferma o corregge
- 26/10, primi numeri di un anello, il router sui clienti del test senza i vocali: richiesta sì/no giusta nel 93% dei gruppi, numero di pezzi nell'88%; proposte non preparate 6,6%, richieste false 8% (concentrate nella chat di gruppo di un cliente)

## Numeri

- Soglia della catena intera: almeno il 70%, congelata prima della misura dei vocali; per alcuni anelli (router, targa dei pezzi aggiunti, targa dei vocali) la soglia è nata dopo aver visto i numeri, ed è dichiarato
- 17 crediti targa al 21/10; la prova controllata ne usa 3-4 in un giorno; la stessa targa nello stesso giorno non consuma un altro credito
- Router sul test: circa 0,84 $ per 436 gruppi letti, 0,2 centesimi a gruppo

## Decisioni e azioni

- Fatto quando: tre prove eseguite con le chiamate registrate, soglie fissate al piano, un report unico che risponde a "la catena funziona abbastanza da giustificare Kromeda di produzione?" e "quanto costa una richiesta?"
- Passi aperti al 27/10: registrazione delle chiamate dal vivo nel servizio (seconda PR), prova a secco appena ci sono le auto, prova controllata dopo l'attivazione del numero di ADAC, ascolto, traffico vero con le targhe (12-17/11), report
- Prima del traffico vero: sicurezza della dashboard e del proxy, server del pilot (Cristian), allarme sulla Coexistence, manuale del banco, prova vera della Coexistence

## Versioni

- Issue #420 · 2026-10-27 · commento col piano (Lorenzo, 27/10): auto e scenari della prova controllata, soglie congelate (catena almeno 70%), cancello per origine della targa, la prova segue l'attivazione del numero; prima PR fatta, passi delle prove aperti
- Issue #420 · 2026-10-26 · commento coi primi numeri del router sui clienti del test; testo della issue invariato
- Issue #420 · 2026-10-21 · prima lettura nel vault
