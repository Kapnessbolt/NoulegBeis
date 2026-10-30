---
type: source-doc
source: sharepoint
family: velo-ce-setup-anticipi-fornitori-so-smart
current:
  item_id: 01EFCYUZ7BBNKZFSQL4JDY3DXI6ILSDJFW
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ7BBNKZFSQL4JDY3DXI6ILSDJFW
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/08 Guide/Setup tecnici/Velo-CE - Setup anticipi fornitori - SO SMART - v001.xlsx
  name: Velo-CE - Setup anticipi fornitori - SO SMART - v001.xlsx
  last_modified: 2026-10-29T15:26:04Z
versions:
  - { name: "Velo-CE - Setup anticipi fornitori - SO SMART - v001.xlsx", item_id: 01EFCYUZ7BBNKZFSQL4JDY3DXI6ILSDJFW, last_modified: 2026-10-29T15:26:04Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-30T06:00:03Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, afc, anticipi, setup, so-smart]
---

# Velo-CE · Setup del nuovo Business Central: anticipi ai fornitori (v001, per So Smart)

## Riassunto

Cartella di lavoro BlueAge del 29/10/2026 per allineare con So Smart il setup del nuovo Business Central di [[velo-ce]] sugli anticipi ai fornitori esteri. Oggi l'anticipo è una scrittura sul conto 03038110 «Anticipi a Fornitori» senza il fornitore e il giroconto sul debito si fa a mano; nel nuovo ambiente l'anticipo si registra sul fornitore, sullo stesso conto, con la categoria alternativa ANT, e al collegamento con la fattura giroconto e differenza di cambio li registra BC. Primo file della cartella `08 Guide/Setup tecnici` (un file per tema). Corretto sul posto il 29/10 pomeriggio con le prove chiuse.

## Punti chiave

- Non cambia il piano dei conti: anticipi su 03038110, debiti verso fornitori esteri su 24043130, banca e conti delle differenze di cambio di oggi; la categoria dei fornitori esteri resta XE, sulla riga dell'anticipo si usa ANT.
- Fogli: Setup (pagina di BC, campo, valore di oggi e nel nuovo ambiente, stato VERIFICATO, PROVATO, PROPOSTA o DA PROVARE), Scritture, Controllo e correzione (anticipo registrato con la categoria sbagliata), Prove.
- I setup si applicano dopo l'integrazione dei pacchetti di setup e delle anagrafiche fornitori di So Smart nel nuovo ambiente (decisione del 29/10), perché nessun pacchetto riporti i valori di oggi.
- Provato il 28-29/10 nella società di prova del tenant BlueAge ([[velo-ce-conti-del-ciclo-dacquisto-per-scenario-interno]]).

## Numeri

- Nessun numero rilevante.

## Decisioni e azioni

- Decisione del 29/10: setup degli anticipi applicato da BlueAge dopo i pacchetti di So Smart
- [ ] Decidere con il commercialista come trattare gli anticipi aperti alla rettifica dei cambi di fine periodo ([[velo-ce-stato-progetto-03-decisioni-aperte]])

## Versioni

- Velo-CE - Setup anticipi fornitori - SO SMART - v001.xlsx · 2026-10-29 · prima versione ingerita (v001 del 29/10, corretta sul posto il pomeriggio); letto il foglio Leggimi
