---
type: source-doc
source: sharepoint
family: velo-ce-integrazioni-we-make-code-specifiche
current:
  item_id: 01EFCYUZ7EJYTZY4TSZ5DLK2UW5ZZZ7IKL
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ7EJYTZY4TSZ5DLK2UW5ZZZ7IKL
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/99 Project Claude (copia)/velo-ce-integrazioni-we-make-code-specifiche-2026-10-29.md
  name: velo-ce-integrazioni-we-make-code-specifiche-2026-10-29.md
  last_modified: 2026-10-29T16:14:34Z
versions:
  - { name: velo-ce-integrazioni-we-make-code-specifiche-2026-10-29.md, item_id: 01EFCYUZ7EJYTZY4TSZ5DLK2UW5ZZZ7IKL, last_modified: 2026-10-29T16:14:34Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-30T06:01:05Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, integrazioni, we-make-code, b2b, interno]
---

# Velo-CE · Integrazioni We Make Code con Business Central: specifiche tecniche (29/10)

## Riassunto

Documento interno BlueAge del 29/10/2026, preparato da Claude per [[cristian-schifone]] dalla mail del CTO di We Make Code del 26/10 (risposta alle domande di [[leonardo-pinsone]] del 23/10, con gli schemi dei configuratori Van Nicholas e Veloe). Descrive chi chiama che cosa fra i portali B2B, Veloce-CRM e Business Central, i flussi dell'ordine di vendita e dell'ordine di assemblaggio, le scelte del dealer nei configuratori, gli impatti sul nuovo BC e le domande aperte. Fonti collegate: [[velo-ce-verbale-integrazioni-we-make-code]], [[velo-ce-verbale-debrief-we-make-code]], [[velo-ce-verbale-demo-product-configurator]]. Non mostrabile così com'è al cliente né ai fornitori.

## Punti chiave

- **Le scritture in BC passano dal modulo MMI di EOS** (dentro So Smart Application): ordine di vendita e aggiornamento dell'ordine di assemblaggio con due chiamate di scrittura; le API di So Smart sono solo tre letture. Per il nuovo ambiente vanno chiesti i flussi MMI configurati, non solo «le API».
- **Scrittura asincrona**: il movimento entra in una coda elaborata ogni 2 minuti; dal 23/10 la coda è bloccata da un errore di setup IVA e nessun ordine del portale entra in BC: la coda è un punto unico di blocco.
- **Togli-metti in due tempi**: BC crea l'ordine di assemblaggio dal modello standard, poi il B2B lo rilegge e lo riscrive aggiungendo accessori o sostituendo componenti. Oggi funziona solo con una bici per ordine. Se gira in Production o solo in prova su Educational è da verificare.
- **Il dealer sceglie più di sei cose**: Van Nicholas 18 posizioni, Veloe 7 passi con tipo e modello del comando cambio: lo shifter non sta nel codice bici proposto, quindi il togli-metti serve anche a Veloe.
- **Articoli CNF-** non solo per il RAL: identificano anche modello e shifter ed entrano nell'ordine di assemblaggio; vanno creati anche nel nuovo BC.
- **Veloce-CRM** mappa il codice bici in una sua tabella (bici muscolare, valori predefiniti): con i codici nuovi va ricaricata, oppure l'informazione si sposta in BC.
- **Impatti sul nuovo BC**: prerequisiti P1-P6 (So Smart Application, flussi e job MMI con utenza tecnica, nuova app Entra per i client, nuovi identificativi, ambiente di prova con le app EOS: le sandbox BlueAge non le hanno), anagrafica A1-A5, regole R1-R4 (accessorio montato solo sull'ordine di assemblaggio, una riga per bici, variante prima della riga, variante su telaio e forcella).
- Cinque differenze con lo stato progetto, recepite al blocco 06 ([[velo-ce-stato-progetto-06-fornitori-perimetro]]).

## Numeri

- Domande aperte: 10 a We Make Code (W1-W10), 4 a So Smart (S1-S4), 3 interne (I1-I3); 4 verifiche a sistema in sola lettura.
- Dal 23/10 14 ordini del portale in errore nella coda MMI.

## Decisioni e azioni

- [ ] Rispondere a We Make Code con le domande W1-W10 non coperte dalla mail
- [ ] Dire a We Make Code che la prova delle integrazioni non si può fare nelle sandbox BlueAge (mancano le app EOS) e serve una sandbox nel tenant `velo-ce.eu` con So Smart Application
- [ ] Aggiornare open point e to-do collegati (CT-33, CT-34, OP-08, OP-33, OP-34, OP-43, TD-072, TD-073, TD-075, TD-077) con la skill `open-point-todo`

## Versioni

- velo-ce-integrazioni-we-make-code-specifiche-2026-10-29.md · 2026-10-29 · prima versione ingerita (documento del 29/10, stato progetto 025.118)
