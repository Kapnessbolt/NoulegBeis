---
type: source-doc
source: sharepoint
family: velo-ce-handoff-ciclo-acquisto-per-scenario
current:
  item_id: 01EFCYUZ2MB4EBVGXU3VBL4ACUQW4U5B6F
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ2MB4EBVGXU3VBL4ACUQW4U5B6F
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/00 Progetto/Handoff/handoff-2026-10-28-ciclo-acquisto-per-scenario.md
  name: handoff-2026-10-28-ciclo-acquisto-per-scenario.md
  last_modified: 2026-10-29T16:14:40Z
versions:
  - { name: handoff-2026-10-28-ciclo-acquisto-per-scenario.md, item_id: 01EFCYUZ2MB4EBVGXU3VBL4ACUQW4U5B6F, last_modified: 2026-10-29T16:14:40Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-30T06:01:05Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [handoff, velo-ce, afc, ciclo-acquisto, interno]
---

# Velo-CE · Handoff del 28/10: ciclo d'acquisto per scenario, prove in sandbox e guida con il menu

## Riassunto

Handoff interno del 28/10/2026 della chat «Costi accessori: chiusura con l'incontro di Claudia del 27/10 e conti del ciclo d'acquisto» (Cristian con Claude, Project Velo-CE), ultimo della catena dopo [[velo-ce-handoff-costi-accessori-chiusura-incontro-claudia]]. Obiettivo dato da [[cristian-schifone]]: provare in sandbox il giro d'acquisto completo per ogni scenario (Italia, UE ed extra-UE, con e senza plafond) e rifare la guida operativa in un solo documento con un menu per lo scenario. Il contesto minore è in [[velo-ce-handoff-contesti-minori]].

## Punti chiave

- **Fatto il 28/10**: conti di oggi mappati per scenario con letture in Production in sola lettura ([[velo-ce-conti-del-ciclo-dacquisto-per-scenario-interno]]); fatture d'acquisto tutte su conto; categorie fornitori, setup IVA e plafond letti; differenze di cambio a mano; gli scenari reali sono sei (Italia con plafond in uso, UE con plafond mai usato).
- **Decisioni da non riaprire**: D40 le anomalie dei dati di oggi si tracciano nel Piano AFC e non si verificano; D38 una sola guida con un menu per scenario, dopo le prove; D28 bolla doganale e fattura della bolla documenti distinti; D16-D17 solo due addebiti TRASP e DAZI; D25 TRASP per volume o per peso, DAZI per importo; D26 carico all'arrivo prima delle fatture accessorie; D29 anticipi sul fornitore (proposta interna, decide Velo-CE con il commercialista); in Production solo letture, setup e prove in sandbox.
- **Punti aperti**: formato della guida con il menu; acquisti UE in plafond (AFC-OP88); plafond sulle righe articolo nel nuovo BC (AFC-OP90); in sandbox mancano le app EOS, quindi integrazione TD18 e invio allo SdI non si provano; magazzino in contabilità ancora aperto al momento dell'handoff (poi chiuso con la 025.113).
- Il handoff riporta indirizzi dell'ambiente del cliente con il suo identificativo e le tecniche di lettura delle liste: omessi.

## Numeri

- Plafond 2026: bolle con dichiarazione d'intento 26 movimenti per 2.180.450 €; acquisti italiani in plafond 113 movimenti per 457.481 € da 11 fornitori; nessun acquisto UE in plafond dal 2023.
- Differenze di cambio a mano 2026: utili 25.243,07 €, perdite 7.598,05 €.

## Decisioni e azioni

- Prove per scenario fatte in sandbox il 28/10 sera e guida v004 con gli scenari (025.114) ([[velo-ce-stato-progetto-99-log-revisioni]])

## Versioni

- handoff-2026-10-28-ciclo-acquisto-per-scenario.md · 2026-10-29 · prima versione ingerita
