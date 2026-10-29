---
type: source-doc
source: sharepoint
family: velo-ce-costi-accessori-e-ciclo-dacquisto-per-leonardo-interno
current:
  item_id: 01EFCYUZ7TUKMNCA3OKFDYMAGQIPTI7GJ4
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ7TUKMNCA3OKFDYMAGQIPTI7GJ4
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/98 Share Team/Velo-CE - Costi accessori e ciclo d'acquisto per Leonardo - INTERNO - v001.md
  name: Velo-CE - Costi accessori e ciclo d'acquisto per Leonardo - INTERNO - v001.md
  last_modified: 2026-10-28T08:06:14Z
versions:
  - { name: "Velo-CE - Costi accessori e ciclo d'acquisto per Leonardo - INTERNO - v001.md", item_id: 01EFCYUZ7TUKMNCA3OKFDYMAGQIPTI7GJ4, last_modified: 2026-10-28T08:06:14Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-29T06:09:24Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, afc, costi-accessori, dazi, trasporti, interno]
---

# Velo-CE · Costi accessori e ciclo d'acquisto: relazione per Leonardo (INTERNO)

## Riassunto

Relazione interna BlueAge del 24/10/2026 (v001) per [[leonardo-pinsone]], preparata dalla chat di Cristian con Claude in vista dell'incontro del 27/10 con Claudia e Stefano di [[velo-ce]]. Spiega perché oggi trasporti e dazi non toccano il costo del prodotto, propone il costo reale con gli addebiti articolo standard TRASP e DAZI agganciati al carico, riassume letture nel BC del cliente, cinque prove nella società di prova BlueAge, chi fa che cosa e i materiali pronti per il 27/10.

## Punti chiave

- **Oggi**: trasporti e dazi restano sui conti di costo e non arrivano all'articolo; l'89% dei trasporti su acquisti viene dagli spedizionieri dell'import.
- **Tre strade**: costo reale con gli addebiti articolo (consigliata, standard anche in Essentials); stima fissa con percentuale di costi indiretti (scartata come strada unica, insieme alla prima conta il costo due volte); costo standard (da evitare). La scelta finale può essere di Velo-CE in base al lavoro chiesto all'amministrazione.
- **Il carico è l'aggancio**: il riferimento della spedizione si scrive sull'ordine e il carico si ritrova con un filtro quando arriva la fattura dello spedizioniere.
- **Configurazione**: categorie su ogni riga della fattura dello spedizioniere (colonne nascoste nella vista standard); IVA dell'addebito DAZI da portare a quella usata oggi per i dazi.
- **Chi fa cosa**: BlueAge configura addebiti e conti; il cliente scrive il riferimento della spedizione, inserisce il peso lordo e assegna gli addebiti; lettura automatica dell'XML DHL da decidere; So Smart per l'aggancio della fattura elettronica al carico.
- **Materiali**: mappa per il cliente, [[velo-ce-guida-ciclo-dacquisto-ordine-ricevimento-fattura-cliente]] v003 e deck [[velo-ce-costi-accessori-e-ciclo-dacquisto-cliente]].

## Numeri

- Dal 01/01 al 03/08/2026: trasporti su acquisti 120.059 €, dazi circa 150.300 €; dazi più trasporti dell'import circa 8,7% dei componenti extra-UE.
- Prove: tubo da 3,90 a 4,15 €/m; forcella +16,3%, manubrio +8,7%; doppio conteggio +4,8%.
- Circa 4-5 fatture al mese degli spedizionieri fanno l'89% del valore.

## Decisioni e azioni

- Decisioni del 24/10 (Cristian): due soli addebiti TRASP e DAZI; voci fuori dal costo come righe su conto; DHL mensile con tutte le spedizioni d'acquisto come TRASP.
- Da confermare: stima solo nel report; scarico dei tubi nel pilota.

## Versioni

- Velo-CE - Costi accessori e ciclo d'acquisto per Leonardo - INTERNO - v001.md · 2026-10-28 · prima versione ingerita; cartella `Cristian/98 Share Team/`
