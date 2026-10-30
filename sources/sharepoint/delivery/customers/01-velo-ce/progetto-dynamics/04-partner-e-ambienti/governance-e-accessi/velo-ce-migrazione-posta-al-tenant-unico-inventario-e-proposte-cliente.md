---
type: source-doc
source: sharepoint
family: velo-ce-migrazione-posta-al-tenant-unico-inventario-e-proposte-cliente
current:
  item_id: 01EFCYUZ3VPFH2TUYV6ZH2B56ATQDLVZ5N
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ3VPFH2TUYV6ZH2B56ATQDLVZ5N
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/04 Partner e ambienti/Governance e accessi/Velo-CE - Migrazione posta al tenant unico, inventario e proposte - CLIENTE - v001.xlsx
  name: Velo-CE - Migrazione posta al tenant unico, inventario e proposte - CLIENTE - v001.xlsx
  last_modified: 2026-10-28T09:51:38Z
versions:
  - { name: "Velo-CE - Migrazione posta al tenant unico, inventario e proposte - CLIENTE - v001.xlsx", item_id: 01EFCYUZ3VPFH2TUYV6ZH2B56ATQDLVZ5N, last_modified: 2026-10-28T09:51:38Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-30T06:00:03Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, tenant-unico, posta, migrazione, cliente]
---

# Velo-CE · Migrazione della posta nel tenant unico: inventario e proposte (v001)

## Riassunto

Cartella di lavoro BlueAge del 28/10/2026 per [[luigi-sacchi]] e [[stefano-moruzzi]] di [[velo-ce]]: inventario dei tre tenant Microsoft 365 della posta (`veloe.eu`, `vannicholas.com`, `velo-ce.eu`) e di quello di Business Central, letti in sola lettura da [[cristian-schifone]], con la proposta per ogni casella nel tenant unico `velo-ce.eu` (deciso il 20/10) e le migliorie da fare con l'occasione. Fogli: Leggimi, Sintesi, Caselle (C-01…C-30), Altri oggetti (A-01…A-14), Proposte (P-01…P-13), Domande (D-01…D-12). Mostrabile a Luigi e Stefano; corretta sul posto lo stesso giorno con il tenant di BC e l'uso delle caselle di funzione. Il file contiene gli identificativi dei tenant, omessi.

## Punti chiave

- **Tre tenant di sola posta**: licenze Exchange Online Piano 1, nessun OneDrive, Teams o SharePoint compreso; nessun partner, connettore o regola di trasporto; un solo inoltro interno.
- **Sicurezza**: in `veloe.eu` impostazioni predefinite di sicurezza disattivate e MFA su una sola casella; DKIM di Microsoft 365 non configurato o disattivato, DMARC assente, debole o in conflitto; app di terze parti con consenso degli utenti.
- **Invio di Business Central**: BC Production manda le mail da una casella `noreply@` di `veloe.eu` con SMTP e autenticazione di base; la proposta P-13 (priorità alta) è passare a OAuth 2.0 prima di spostare la casella, che poi diventa condivisa.
- **Proposta**: diverse caselle di funzione diventano cassette condivise; le licenze si scelgono persona per persona se servono Office, OneDrive o Teams (D-02).
- Metodo e sequenza della migrazione nella guida [[velo-ce-guida-migrazione-posta-al-tenant-unico-interno]].

## Numeri

- Licenze Exchange: 22 assegnate oggi nei tre tenant (13, 6, 3), 7 dopo secondo la proposta.
- Posta: circa 49,3 GB in `veloe.eu`, 4,8 GB in `vannicholas.com`, 0,5 GB in `velo-ce.eu`.
- Rinnovo delle 14 licenze di `veloe.eu` il 05/12/2026; gli altri due tenant il 19/02/2027.
- Proposte: 10 cassette condivise, 3 caselle da decidere.

## Decisioni e azioni

- [ ] Risposte di Luigi Sacchi e Stefano Moruzzi alle domande D-01…D-12 e scelta delle licenze per persona
- [ ] Passare l'invio delle mail di BC a OAuth 2.0 prima di spostare la casella `noreply@` (P-13)

## Versioni

- Velo-CE - Migrazione posta al tenant unico, inventario e proposte - CLIENTE - v001.xlsx · 2026-10-28 · prima versione ingerita (v001 del 28/10, corretta sul posto lo stesso giorno); letti i fogli Leggimi e Sintesi
