---
type: source-doc
source: sharepoint
family: velo-ce-verbale-revisione-file-codifica-articoli
current:
  item_id: 01EFCYUZ5KYQQAJ7VPGZA33ULE2ZMQDX3J
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ5KYQQAJ7VPGZA33ULE2ZMQDX3J
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Cristian/99 Project Claude (copia)/verbali/velo-ce-verbale-261022-1104-revisione-file-codifica-articoli.md
  name: velo-ce-verbale-261022-1104-revisione-file-codifica-articoli.md
  last_modified: 2026-10-28T08:06:46Z
versions:
  - { name: velo-ce-verbale-261022-1104-revisione-file-codifica-articoli.md, item_id: 01EFCYUZ5KYQQAJ7VPGZA33ULE2ZMQDX3J, last_modified: 2026-10-28T08:06:46Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-29T06:04:48Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [verbale, velo-ce, codifica, anagrafica, import, interno]
---

# Velo-CE · Verbale: revisione del file di codifica degli articoli

## Riassunto

Revisione interna BlueAge (Cristian e Leo) del 22/10/2026 dalle 11:04 del file di codifica di una bici completa preparato con l'aiuto di Claude, campo per campo. Contenuti dichiarati. Il file diventa la base dei template di import da provare in una società nuova di prova; fissa gli orientamenti su sigla per natura, marca e brand commerciale, categorie a due livelli e dati logistici del collo.

## Punti chiave

- Codice: sigla della natura dell'oggetto più progressivo a 4 cifre; per una bici di circa 120 codici servono circa 80 nature, più del previsto.
- Marca del produttore come attributo e brand commerciale (Veloe, Van Nicholas) come dimensione, per avere la marginalità per marchio.
- Tipo materiale da tendina con la categoria di registrazione di magazzino; colonne di rilascio (R1-R3) e di corrispondenza con il codice di oggi; il codice di oggi va nei riferimenti articolo, senza saldi iniziali dal file.
- Categorie: L1 uguale al tipo materiale, L2 natura del pezzo, L3 non popolato (il cliente aveva detto che due livelli bastano).
- Pesi e misure: servono pezzi per collo e peso e misure del collo, da far rilevare al magazziniere.
- Il file copre un solo modello delle 31 configurazioni, che restano da verificare.

## Numeri

- Circa 120 codici e 80 nature per una bici completa.

## Decisioni e azioni

- Orientamenti interni: L3 non si popola; il file diventa il template di import.
- [ ] Rendere importabile il file di codifica e provare l'import in una società nuova di prova ([[velo-ce-verbale-revisione-file-codifica-articoli]])

## Versioni

- velo-ce-verbale-261022-1104-revisione-file-codifica-articoli.md · 2026-10-28 · prima versione ingerita; cartella `Cristian/99 Project Claude (copia)/verbali/`
