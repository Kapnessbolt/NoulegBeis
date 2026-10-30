---
type: source-doc
source: sharepoint
family: velo-ce-costi-accessori-e-ciclo-dacquisto-cliente
current:
  item_id: 01EFCYUZ6WOGRCY5AUJJC2BOPA3GTTFBI2
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ6WOGRCY5AUJJC2BOPA3GTTFBI2
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/01 Deck cliente/SAL/261027 Velo-CE - Costi accessori e ciclo d'acquisto - CLIENTE - v002.pptx
  name: 261027 Velo-CE - Costi accessori e ciclo d'acquisto - CLIENTE - v002.pptx
  last_modified: 2026-10-29T13:49:26Z
versions:
  - { name: "261027 Velo-CE - Costi accessori e ciclo d'acquisto - CLIENTE - v002.pptx", item_id: 01EFCYUZ6WOGRCY5AUJJC2BOPA3GTTFBI2, last_modified: 2026-10-29T13:49:26Z }
  - { name: "261027 Velo-CE - Costi accessori e ciclo d'acquisto - CLIENTE - v001.pptx", item_id: 01EFCYUZ5ML3I3W52BA5AL4H4ZHOLCOY5Q, last_modified: 2026-10-27T21:34:28Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-30T05:59:10Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [deck, sal, velo-ce, afc, costi-accessori, dazi, anticipi, cliente]
---

# Velo-CE · Deck SAL del 27/10: costi accessori e ciclo d'acquisto (CLIENTE)

## Riassunto

Deck BlueAge di 16 slide (v002 del 28/10, corretta il 29/10; v001 di 14 slide) per l'incontro del 27/10/2026 con [[claudia-crippa]] e [[stefano-moruzzi]] di [[velo-ce]], materiale per il cliente. Spiega come trasporti e dazi entrano nel costo del prodotto con gli addebiti articolo, come si gestiscono anticipi e cambio dell'import, mostra le prove fatte in una società di prova BlueAge e chiude con dieci punti da decidere insieme e i prossimi passi.

## Punti chiave

- **Punto di partenza**: trasporti e dazi pesano ma oggi restano sui conti di costo del periodo, non sul componente né sulla bici; il legame fra bolla, fattura e merce è solo nella descrizione.
- **Tre strade**: costo reale con gli addebiti articolo (consigliata), stima fissa con percentuale di costi indiretti (da sola non basta), costo standard (da evitare); la stima dei costi in arrivo va nel report, non sull'articolo.
- **Regola**: due soli addebiti, TRASP (trasporti, criterio per volume o peso) e DAZI (per importo); fuori dal costo IVA all'importazione, bolli, spese bancarie e trasporti su vendite. La contabilità non cambia.
- **Flusso**: ordine, carico con il DDT o la lettera di vettura sull'ordine, fattura della merce dal carico, fatture di trasporto e bolla assegnate al carico ritrovato dal riferimento; casi per fonte del costo (fornitore, vettore, corriere mensile DHL, spedizioniere con nolo e bolla).
- **Prove**: tubi con trasporto in fattura (da 3,90 a 4,15 €/m); import in dollari (forcella +16,3%, manubrio +8,7%); DHL con bolla e fattura mensile; rettifiche automatiche dopo il consumo; doppio conteggio con la stima (+4,8%).
- **Anticipi e cambio**: oggi anticipi su un conto generale senza fornitore e cambi fermi al 2023; domani due strade per gli anticipi (pagamento sul fornitore o pagamenti anticipati sull'ordine) da scegliere con il commercialista.
- **Dieci punti da decidere**: volume o peso, lettera di vettura nei PDF, DHL e lettura dell'XML, bolle con voci diverse, stima nel report, pilota (tubi e un fornitore con trasporto in fattura), packing list, trasporto su strada in Italia, anticipi, cambio.
- **v002 (28-29/10)**: due soli addebiti (TRASP per volume o per peso, DAZI per importo) e quattro voci fuori dal costo (IVA all'importazione, bolli, spese bancarie, trasporti su vendite); il carico si registra all'arrivo della merce, prima di tutte le fatture; anticipi in dollari sul fornitore, strada A provata (giroconto e differenza di cambio li registra BC), strada B pagamenti anticipati sull'ordine da valutare; dieci domande per Stefano, Claudia e il commercialista. Dazi e trasporti dell'import valgono circa l'8,7% degli acquisti di componenti extra-UE (120.059 € di trasporti e 150.299 € di dazi dal 01/01 al 03/08/2026).

## Numeri

- Dal 01/01 al 03/08/2026: trasporti su acquisti 120.059 €, dazi circa 150.300 €; 89% dei trasporti dagli spedizionieri; 8,7% su componenti extra-UE.
- Prova import: accessori 1.082,45 € su 7.900 € di merce (13,7%).

## Decisioni e azioni

- Proposta BlueAge: costo reale con gli addebiti, stima solo nel report.
- Prossimi passi BlueAge: configurare TRASP e DAZI, preparare l'ambiente per le prove, valutare la lettura dell'XML DHL, proporre il report del costo atteso e reale, provare le due strade per gli anticipi.

## Versioni

- 261027 Velo-CE - Costi accessori e ciclo d'acquisto - CLIENTE - v001.pptx · 2026-10-27 · prima versione ingerita; cartella `Cristian/01 Deck cliente/SAL/`
- 261027 Velo-CE - Costi accessori e ciclo d'acquisto - CLIENTE - v002.pptx · 2026-10-29 · v002 del 28/10, 16 pagine, corretta sul posto il 29/10 (pagine 6, 12, 15, 16): anticipi sul fornitore provati, rettifica cambi da vedere con il commercialista; non ancora consegnata
