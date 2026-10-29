---
type: source-doc
source: sharepoint
family: velo-ce-pilota-bc-lungo-bosch-fetta-telaio-verniciato-nota-per-trif
current:
  item_id: 01EFCYUZ7UYFCLZED26VBZBYVY7HMWOXZA
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ7UYFCLZED26VBZBYVY7HMWOXZA
  web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/02 Configurazione/Telaio e produzione/Velo-CE - Pilota BC Lungo Bosch - Fetta telaio verniciato - nota per Trif - v001.docx"
  name: "Velo-CE - Pilota BC Lungo Bosch - Fetta telaio verniciato - nota per Trif - v001.docx"
  last_modified: 2026-09-27T21:38:14Z
versions:
  - { name: "Velo-CE - Pilota BC Lungo Bosch - Fetta telaio verniciato - nota per Trif - v001.docx", item_id: 01EFCYUZ7KO4GIJ6WTZFGYAAGSST4TUV7H, last_modified: 2026-09-27T21:38:14Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:28:59Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [pilota-lungo, telaio, decisioni, sandbox, conto-lavoro, verniciatura, business-central-premium]
---

# Velo-CE · Pilota BC Lungo Bosch, fetta telaio verniciato: nota per Cristian

## Riassunto

Nota BlueAge del 27/09/2026 (v001, 7 pagine) per Cristian, che accompagna il modello dati "5 fogli" v006 e prepara la prova in ambiente di test del 28/09. Il pilota è la Multi Lungo Bosch MLCA-5E-545-CDX: bici assemblata su ordine (ATO), catena del telaio a scorta (MTS) con il telaio sabbiato come ultimo buffer comune, telaio verniciato fatto per le bici ordinate. Il lavoro del 27/09 si concentra sulla "fetta" telaio verniciato con tutta la catena e la forcella verniciata. La nota riporta i fatti raccolti in reparto (15/09 e con Leonardo il 27/09), le decisioni del 27/09, dieci prove da fare in sandbox e le domande per Velo-CE del 29-30/09. Tempi, lead time e costi sono stime o segnaposto.

## Punti chiave

- **Modello v006**: 61 articoli nella fetta (30 prodotti, 21 dei quali pezzi laser), distinta di 67 righe dal telaio verniciato a tubi e lamiere, 13 postazioni e 9 cicli, 28 campi della scheda articolo per tipologia, 47 punti di decisione. Codici pilota LU-xxx stabili dalla v003.
- **Fatti di reparto**: due laser (tubi e parti piane), il laser tubi lo usa solo Ranzini; foderi e parti laser preparati a lotti e tenuti in bocche di lupo e cassoni; carro di nove pezzi saldati a mano sul triangolo nella dima, non esiste come scorta; sabbiatura a cariche da 8; verniciatura spedita da Augusto circa due volte a settimana, flusso oggi su Fatture in Cloud; lotti decisi a occhio da Ranzini; oggi in reparto nessuno registra; licenza Premium con utente di reparto decisa il 21/09.
- **Decisioni del 27/09**: un pezzo preparato in casa è articolo prodotto quando si prepara a lotti e resta a scorta (F5-05); triangolo della Lungo articolo nuovo (F5-09); verniciatura come operazione di conto lavoro nel ciclo CI-VERNICIATURA presso il centro VER, telaio e forcella con variante colore (F5-30); filo, gas e graniglia fuori distinta (F5-36); un'operazione per postazione, codici a tre lettere più numero (F5-32, F5-33); ciclo del telaio sabbiato in 4 operazioni, lotto 8 (F5-40); scarico dei componenti in avanti, tempi e pezzi alla chiusura (F5-39); sfrido nella quantità di distinta, scarto con codice (F5-42); FIFO con costo standard solo sulla tariffa oraria (F5-21); niente collocazioni all'avvio (F5-22); categoria articolo a tre livelli (F5-43); quantità fissa con punto di riordino per i buffer, lotto per lotto per i verniciati (F5-45).
- **Prove 4.0-4.10**: preparazione Premium, scheda articolo e unità di misura (lamiera KG con FOGLIO, ellittico acquistato a KG), distinte e cicli con la fantasma del carro, lotto laser con scarico in avanti, scarto prima della chiusura, telaio sabbiato con la fantasma, verniciatura in conto lavoro, pianificazione, costo del telaio verniciato, consumabili non di magazzino, cinque domande tecniche.
- **Domande per il 29-30/09**: a Ranzini 14 punti (articoli a scorta, postazioni PIE-01, BAN-03, DIM-03, pezzi per barra o foglio, unità della lamiera, housing, foderi, scarti, tempi); ad Augusto il flusso della verniciatura in BC; a Stefano lead time e codici fornitore (Trafiltubi, Mariani, Mosca, verniciatore), significato del codice VE-TL-LUFR-BH-24, colore del pilota, ruota anteriore 24" o 20"; a Leonardo con l'amministrazione categorie contabili e costo orario.

## Numeri

- Fetta: 61 articoli, 67 righe di distinta, 13 postazioni, 9 cicli con 14 righe, 47 decisioni.
- Circa 2 ore e mezza di lavoro per telaio verniciato (stima); sabbiatura 30 minuti a telaio dal rilievo, cariche da 8 telai da circa 4 ore (da verificare).
- Verniciatura: circa 50 pezzi due volte a settimana; costo 10-12 € a telaio.
- Costi di prova: tubo trafilato 7,10 €/m, lamiera circa 1 €/kg; foglio 1500×3000 da 3 mm circa 106 kg.
- Lead time stimati: ferro e lamiere 1 settimana, tubi trafilati 2 settimane.
- Circa 50 finti motori Bosch limitano i triangoli in lavorazione; lotto dei telai oggi 25, senza ragione tecnica.

## Decisioni e azioni

- Le decisioni marcate "proposta" vanno confermate con Velo-CE il 29-30/09; confluiranno nella memoria di progetto v005.
- [ ] Prova in ambiente di test delle sezioni 4.0-4.9 📅 2026-09-28
- [ ] Raccogliere le risposte di Ranzini, Augusto, Stefano e Leonardo 📅 2026-09-30

## Versioni

- Velo-CE - Pilota BC Lungo Bosch - Fetta telaio verniciato - nota per Trif - v001.docx · 2026-09-27 · prima versione ingerita (il nome file dice "nota per Trif", il documento si intitola "nota per Cristian")
