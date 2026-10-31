---
type: source-doc
source: sharepoint
family: velo-ce-handoff-costi-accessori-ciclo-acquisto
current:
  item_id: 01EFCYUZ3SMZC3N4DACRA2252SJWWRCAEO
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ3SMZC3N4DACRA2252SJWWRCAEO
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/00 Progetto/Handoff/handoff-2026-10-26-costi-accessori-ciclo-acquisto.md
  name: handoff-2026-10-26-costi-accessori-ciclo-acquisto.md
  last_modified: 2026-10-29T16:14:39Z
versions:
  - { name: handoff-2026-10-26-costi-accessori-ciclo-acquisto.md, item_id: 01EFCYUZ3SMZC3N4DACRA2252SJWWRCAEO, last_modified: 2026-10-29T16:14:39Z }
  - { name: handoff-2026-10-26-costi-accessori-ciclo-acquisto.md, item_id: 01EFCYUZ4I34DN5ZOFHZAZFAXGITY6VGWD, last_modified: 2026-10-28T08:06:23Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-29T06:08:20Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [handoff, velo-ce, afc, costi-accessori, dazi, trasporti, interno]
---

# Velo-CE · Handoff: costi accessori d'acquisto e ciclo d'acquisto (26/10)

## Riassunto

Handoff interno del 26/10/2026 della chat del 24-26/10 (Cristian con Claude) per preparare l'incontro del 27/10 con Claudia e Stefano: insegnare il ciclo d'acquisto ordine, carico, fattura e far entrare trasporti, dazi, spedizionieri e corrieri nel costo dell'articolo. Riassume letture nel BC di [[velo-ce]], prove nella società di prova BlueAge, 22 decisioni e i file prodotti: mappa per il cliente, [[velo-ce-guida-ciclo-dacquisto-ordine-ricevimento-fattura-cliente]] v003, deck [[velo-ce-costi-accessori-e-ciclo-dacquisto-cliente]] e relazione [[velo-ce-costi-accessori-e-ciclo-dacquisto-per-leonardo-interno]].

## Punti chiave

- **Strade**: costo reale con gli addebiti articolo (consigliata); stima fissa con percentuale di costi indiretti scartata come strada unica; costo standard da evitare. Stima e reale insieme contano il costo due volte (provato, +4,8%).
- **Regola**: solo due addebiti, TRASP e DAZI; fuori dal costo IVA all'importazione, bolli e spese bancarie, trasporti su vendite. Il riferimento della spedizione va nel campo del documento di trasporto dell'ordine (DDT, lettera di vettura).
- **DHL mensile**: tutte le spedizioni d'acquisto come TRASP, da automatizzare leggendo l'XML; esecutore da decidere.
- **Stima nel report, non sull'articolo**: percentuali per codice doganale e paese d'origine (dazio) e per fornitore o provenienza (trasporto); il report stimato contro reale non esiste in standard, va costruito in Power BI.
- **Pilota proposto**: tubi nel BC di oggi come articolo di magazzino, con conte a fine novembre e dicembre.
- **Aperti**: domande per il 27/10 (peso lordo sugli articoli, lettera di vettura nei PDF, frequenza della fattura prima della merce, IVA dell'addebito DAZI, percentuali per la stima, pilota); app EOS che aggancia la fattura al carico; voci anomale nella nomenclatura combinata.

## Numeri

- Trasporti su acquisti 120.059 € dal 01/01 al 03/08/2026 (2,2% degli acquisti di merce, 89% dagli spedizionieri dell'import); dazi circa 150.300 €; dazi più trasporti circa 8,7% dei componenti extra-UE.
- Prova import: forcella +16,3%, manubrio +8,7%; accessori 13,7% del valore della merce.

## Decisioni e azioni

- Decisioni D01-D22 del 24/10, fra cui: due soli addebiti TRASP e DAZI, voci fuori dal costo come righe su conto, ambiente di prova VC-NBC PROVA, fattura del trasporto registrata dopo il carico.

## Versioni

- handoff-2026-10-26-costi-accessori-ciclo-acquisto.md · 2026-10-28 · prima versione ingerita; cartella `Cristian/00 Progetto/Handoff/`; dettagli tecnici di accesso omessi
