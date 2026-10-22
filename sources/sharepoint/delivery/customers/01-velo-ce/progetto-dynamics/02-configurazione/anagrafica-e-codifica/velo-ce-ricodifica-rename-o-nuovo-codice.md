---
type: source-doc
source: sharepoint
family: velo-ce-ricodifica-rename-o-nuovo-codice
current:
  item_id: 01EFCYUZZFMI4MH4IOTJAIWG2Q7CC2NZP2
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZZFMI4MH4IOTJAIWG2Q7CC2NZP2
  web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/02 Configurazione/Anagrafica e codifica/Velo-CE - Ricodifica - rename o nuovo codice.xlsx"
  name: "Velo-CE - Ricodifica - rename o nuovo codice.xlsx"
  last_modified: 2026-09-20T13:52:17Z
versions:
  - { name: "Velo-CE - Ricodifica - rename o nuovo codice.xlsx", item_id: 01EFCYUZZFMI4MH4IOTJAIWG2Q7CC2NZP2, last_modified: 2026-09-20T13:52:17Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:28:59Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [codifica, ricodifica, anagrafica, costing, business-central, decisione]
---

# Velo-CE · Ricodifica degli articoli: rinominare, creare nuovi codici o un misto

## Riassunto

Foglio di lavoro BlueAge del 18/09/2026, uso interno, che prepara la scelta su come ricodificare gli articoli Velo-CE in Business Central. Mette a confronto tre strade (rinomina standard, nuovo codice, ibrido famiglia per famiglia) su undici conseguenze concrete, ognuna marcata come documentata, dichiarata o da provare. Propone per ogni famiglia di articoli una strada, lasciando la decisione a Stefano (e a Gabriele per il telaio), ed elenca sei prove da fare in sandbox prima di impegnare una quotazione sul cantiere di ricodifica. La domanda che decide è se, riaprendo fra due anni una fattura del 2024, si vuole vedere il codice di allora o quello di oggi.

## Punti chiave

- **Rinomina**: storico continuo ma riscritto (le fatture passate mostrano il codice nuovo), distinte e documenti aperti seguono, report Power BI senza lavoro; rischio alto sulle integrazioni che conoscono il codice, etichette stampate subito sbagliate.
- **Nuovo codice**: storico fedele ma spezzato, serve un raccordo vecchio ↔ nuovo; distinte da rifare; permette di scegliere da capo il metodo di costing e il valore di carico; rischio basso sulle integrazioni, reversibile.
- **Vincolo tecnico che decide**: il metodo di costing non si cambia su un articolo con movimenti; dove una famiglia deve cambiare metodo serve un codice nuovo.
- **Rischio numero uno**: le API del B2B accessori Van Nicholas che scrivono in BC (indicazione del 18/09) riguardano proprio accessori e componenti; elenco dei servizi web (page 810) da verificare. Le etichette sono prodotte da Veloce-CRM, quindi dipendono da We Make Code.
- **Proposta per famiglia** (decisione di Stefano, colonna vuota): bici Veloe configurazioni (~90 codici, senza distinta, costo zero) → nuovo codice; bici Van Nicholas → non toccare ora (si riallineano alla prossima generazione); accessori Veloe coppie AC/AM → nuovo codice (è una fusione, la rinomina non la fa); telaio parti a disegno `VE-TL`/`VE-LU` → ibrido (Stefano e Gabriele); materie prime (tubi, lamiere) → creazione ex novo; sottogruppi e ruote → rinomina; codici Shimano in dismissione con il passaggio a Bosch nel 2027 → non toccare, si bloccano.
- **Certezza**: verificati sul tenant BlueAge il 17-18/09 distinte, costi, addebiti articolo e ubicazioni; nessuna rinomina provata su un articolo con movimenti.
- **Prove in sandbox** (nessuna fatta): P1 rinomina con movimenti; P2 rinomina di un articolo esposto da un servizio web; P3 rinomina con l'estensione So Smart attiva (rischio di dati orfani); P4 nuovo codice con costing Standard invece di FIFO; P5 raccordo con i riferimenti articolo; P6 tempo di rinomina su un articolo molto movimentato. Da fare su Educational o sandbox dedicato (S04), non sul tenant BlueAge.

## Numeri

- 669 codici a costo zero; 1.263 righe di distinta a sistema.
- 84 codici telaio `VE-TL`/`VE-LU`; ~90 codici bici Veloe; almeno 20 coppie AC/AM.
- 6 prove da fare (P1-P6), 11 dimensioni di confronto, 7 famiglie con proposta.
- Transizione Shimano → Bosch prevista nel 2027.

## Decisioni e azioni

- Decisione per famiglia aperta, in capo a Stefano (telaio: Stefano con Gabriele); BlueAge propone solo per le materie prime.
- [ ] Eseguire P1, P2 e P3 in sandbox prima di quotare il cantiere di ricodifica
- [ ] Leggere l'elenco dei servizi web pubblicati (page 810) per capire quali integrazioni conoscono il codice articolo
- [ ] Scegliere una finestra con pochi ordini aperti per la ricodifica, qualunque strada si prenda

## Versioni

- Velo-CE - Ricodifica - rename o nuovo codice.xlsx · 2026-09-20 · prima versione ingerita (documento datato 18/09/2026)
