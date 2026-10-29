---
type: source-doc
source: sharepoint
family: velo-ce-handoff-afc-voci-2-1-2-2
current:
  item_id: 01EFCYUZ3WBFADKRR3SNAJGYQZV6RY7QRA
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ3WBFADKRR3SNAJGYQZV6RY7QRA
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/00 Progetto/Handoff/handoff-2026-10-08-afc-voci-2.1-2.2.md
  name: handoff-2026-10-08-afc-voci-2.1-2.2.md
  last_modified: 2026-10-08T10:43:55Z
versions:
  - { name: handoff-2026-10-08-afc-voci-2.1-2.2.md, item_id: 01EFCYUZ3WBFADKRR3SNAJGYQZV6RY7QRA, last_modified: 2026-10-08T10:43:55Z }
also_at:
  - { web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Cristian/00 Progetto/Handoff/handoff-2026-10-08-afc-voci-2.1-2.2.md", item_id: 01EFCYUZ6FJRYH2EB5IZDYQTNG5YEUROJD }
status: active
partial: false
ingested_at: 2026-10-22T13:25:33Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [handoff, afc, ciclo-passivo, fattura-elettronica, piano-afc, interno]
---

# Velo-CE · Handoff del 08/10/2026: area AFC, analisi voce per voce, prossime voci 2.1 e 2.2

## Riassunto

Handoff principale della chat sull'area AFC del 06-07/10/2026 (il secondo file è [[velo-ce-handoff-afc-contesti-minori]]). Il filone analizza una per volta le 49 voci del perimetro AFC del Piano AFC per capire come Velo-CE lavora oggi in Business Central e che cosa serve nel nuovo tenant Premium al 01/01/2027: verifiche in sola lettura, spiegazione dei concetti, aggiornamento del Piano AFC, schede di processo, righe del piano ripresa dati e proposte per lo stato progetto. La prossima sessione affronta insieme le voci 2.1 (arrivo delle fatture elettroniche) e 2.2 (registrazione delle fatture d'acquisto), che in BC sono un solo flusso. Segnala la sovrapposizione con il [[velo-ce-piano-attivita-nuovo-ambiente-interno]] e il [[velo-ce-piano-ripresa-dati-interno]], da risolvere con Cristian.

## Punti chiave

- **Stato delle voci**: in corso 1.1-1.5, 2.1, 2.2, 2.6; tutte le altre da esplorare (la 2.3 va portata a «in corso»). La 2.6 (giro acquisti scollegato) è la più lavorata.
- **Voce 2.1 (arrivo fatture)**: fornitore → SdI → Able Tech IX-FE → BC con l'app EX063, import automatico ogni giorno con un processo ricorrente sull'utenza dell'amministrazione; restano solo 7 file vecchi da lavorare; l'utenza dell'intermediario è un account personale del titolare e la password la reinserisce l'amministrazione quando scade (rischio, proposta un'utenza aziendale); IX-FE non conserva.
- **Voce 2.2 (registrazione fatture d'acquisto)**: dal file in entrata con anteprima alla fattura registrata; registra soprattutto l'amministrazione (circa 36 fatture a settimana), il titolare circa la metà; serie FAI Italia, FAU UE, FAX extra-UE, autofatture AFA. Nessuna fattura d'acquisto ha mai avuto righe di tipo articolo: i componenti vanno su due conti C/G, una riga per fattura. Ordini d'acquisto mai fatturati e, da maggio 2026, mai ricevuti: il «ricevuto non fatturato» di BC non è reale.
- **Autofatture TD17-TD19**: Velo-CE invia allo SdI i documenti dei fornitori UE e le autofatture a lotti il 15 del mese successivo dal 12/02/2023; nel 2026 nessun documento extra-UE.
- **Decisioni del filone**: 2.1 e 2.2 insieme partendo dalla 2.2; le domande AFC vivono solo nel Piano AFC; negli open point conta «che cosa si fa e perché», non «chi lo fa»; la scheda del ciclo passivo è lo standard delle schede; link alle pagine BC sull'ambiente Educational; ripresa dati con apertura in due tempi da decidere col commercialista; terminologia «giornale articoli»; per le differite di dicembre aggiunta la strada più semplice (emissione dal BC di oggi entro il 15/01 con data di dicembre).
- **Convivenza dei piani (da decidere)**: piano attività NBC per attività, date e responsabili; piano ripresa RD per il dettaglio per oggetto; attività del Piano AFC solo dove servono a una voce, con rimando alla riga NBC; fasi RF da allineare a R0/R1.
- **Verifiche proposte per 2.1-2.2**: fatture registrate nel 2026 per serie e utente; fatture inserite a mano; come l'anteprima propone fornitore, conto e IVA; tempi fra documento, ricezione e registrazione; i 7 file fermi; note di credito d'acquisto 2026.

## Numeri

- 49 voci del perimetro AFC; ultimo open point AFC-OP41, ultima attività AFC-AT14, ultima miglioria AFC-MG10.
- Evidenze fino a E160, prossimo E161; tenant BlueAge prossimo T155; stato progetto 025.64.
- Circa 36 fatture d'acquisto a settimana registrate dall'amministrazione; 7 file fermi in entrata; un ordine con 157.136 euro ricevuti e mai fatturati.
- Codice destinatario dell'intermediario in uso dal 05/01/2023; 9 fatture su 12 del campione arrivano con il codice di Fatture in Cloud.

## Decisioni e azioni

- Decisione (Cristian, 07/10): analizzare 2.1 e 2.2 insieme, partendo dalla 2.2.
- Decisione (06/10): le domande AFC vivono solo nel Piano AFC; altrove solo rimandi.
- Decisione (07/10): link alle pagine BC sull'ambiente Educational, per non rischiare scritture in Production.
- [ ] Chiedere a Cristian come convivono piano attività, piano ripresa e attività AFC prima di aggiungere righe
- [ ] Eseguire le verifiche in sola lettura sulle voci 2.1-2.2 e aggiornare Piano AFC e scheda del ciclo passivo
- [ ] Aggiornare la riga CLA-02 del file dell'intervista (invio TD17-TD19 ora verificato) e portare la voce 2.3 a «in corso»
- [ ] Controllare RD10 e RD16 del piano ripresa dati
- [ ] Decidere prima di dicembre la data della conta (AFC-OP40) e le fatture differite (AFC-OP41)
- [ ] Poi voci 2.3, 2.4, 2.5, 2.7 e ciclo attivo 3.x

## Versioni

- handoff-2026-10-08-afc-voci-2.1-2.2.md · 2026-10-08 · prima versione ingerita
