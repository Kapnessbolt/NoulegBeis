---
type: source-doc
source: sharepoint
family: velo-ce-master-di-codifica-e-anagrafiche
current:
  item_id: 01EFCYUZ46LJIF6FJ2RRD26TSV5X6EDYW2
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ46LJIF6FJ2RRD26TSV5X6EDYW2
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/02 Configurazione/Anagrafica e codifica/Articoli/Velo-CE - Master di codifica e anagrafiche - INTERNO - v005.xlsx
  name: Velo-CE - Master di codifica e anagrafiche - INTERNO - v005.xlsx
  last_modified: 2026-10-26T11:56:01Z
versions:
  - { name: "Velo-CE - Master di codifica e anagrafiche - INTERNO - v005.xlsx", item_id: 01EFCYUZ46LJIF6FJ2RRD26TSV5X6EDYW2, last_modified: 2026-10-26T11:56:01Z }
  - { name: "261022 Velo-CE - Master di codifica e anagrafiche - v003.xlsx", item_id: 01EFCYUZ7WW4EXCNZQTFAZSDP4IQ3PILR4, last_modified: 2026-10-22T09:31:02Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-29T06:13:39Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, codifica, anagrafica, ripresa-dati, import, interno]
---

# Velo-CE · Master di codifica e anagrafiche degli articoli (INTERNO)

## Riassunto

File master interno BlueAge da cui nascono gli articoli del nuovo Business Central di [[velo-ce]]: una riga per codice, distinte, varianti colore con EAN, unità di misura, parametri di pianificazione per colore, nature con le sigle, tabelle di setup e spiegazione dei campi. La v005 del 26/10/2026 è costruita da BlueAge sulla v003 di Leo del 22/10 (che resta accanto, com'è), con la struttura delle categorie di Leo (L1 tipo materiale, L2 famiglia). Da qui un programma genera i file da importare con i pacchetti di configurazione e un report di controllo.

## Punti chiave

- **Fogli**: articoli, distinte (padre → figlio), varianti con EAN, unità di misura aggiuntive, SKU per colore, nature (sigla di tre lettere e categoria tipica, modelli delle bici), setup (categorie, categorie di registrazione, unità, produttori, brand), campi (cosa diventa ogni colonna in BC), note per Leo, confronto fra due strutture di categorie.
- **Come si aggiunge un articolo**: natura da tendina, progressivo a 4 cifre per sigla, marca, modello, caratteristiche e colore in inglese (descrizione composta entro 40 caratteri), tipo materiale, categoria di registrazione, categoria L2, unità di misura, sistema di rifornimento.
- **Livelli dei campi**: obbligatori per BC, necessari dall'avvio dell'8 gennaio, solo di lavoro, di controllo.
- **Fuori dal file**: prezzi, fornitori (li riprende So Smart), cicli, serie numeri, ubicazioni, catalogo fornitori.
- Il file contiene dati di anagrafica articolo riga per riga: la nota riporta solo struttura e numeri aggregati.

## Numeri

- Import provato il 26-27/10 nella società di prova VC-IMPORT PROVA: 136 articoli, 158 righe di distinta, 27 varianti, 18 SKU ([[velo-ce-stato-progetto-01-inquadramento-ambiente]]).

## Decisioni e azioni

- Nessuna decisione formale.

## Versioni

- 261022 Velo-CE - Master di codifica e anagrafiche - v003.xlsx · 2026-10-22 · versione v003 di Leo del 22/10; cartella `Cristian/02 Configurazione/Ripresa Dati/Articoli/`
- Velo-CE - Master di codifica e anagrafiche - INTERNO - v005.xlsx · 2026-10-26 · v005 di BlueAge sulla v003 di Leo, con categorie L1/L2, campi e generatore dei file di import (letto il foglio Leggimi)

