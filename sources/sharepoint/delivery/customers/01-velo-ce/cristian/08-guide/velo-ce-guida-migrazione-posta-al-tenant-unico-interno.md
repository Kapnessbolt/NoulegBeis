---
type: source-doc
source: sharepoint
family: velo-ce-guida-migrazione-posta-al-tenant-unico-interno
current:
  item_id: 01EFCYUZYJF6K5NLKSQZCZSTBGR2YZLXY4
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZYJF6K5NLKSQZCZSTBGR2YZLXY4
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Cristian/08 Guide/Velo-CE - Guida migrazione posta al tenant unico - INTERNO - v001.pdf
  name: Velo-CE - Guida migrazione posta al tenant unico - INTERNO - v001.pdf
  last_modified: 2026-10-28T08:06:12Z
versions:
  - { name: "Velo-CE - Guida migrazione posta al tenant unico - INTERNO - v001.pdf", item_id: 01EFCYUZYJF6K5NLKSQZCZSTBGR2YZLXY4, last_modified: 2026-10-28T08:06:12Z }
also_at:
  - { web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Cristian/08 Guide/Velo-CE - Guida migrazione posta al tenant unico - INTERNO - v001.docx", item_id: 01EFCYUZ5REHDM5U4PVJD24NO3ONTLLXUI }
status: active
partial: false
ingested_at: 2026-10-29T06:11:43Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [guida, velo-ce, microsoft-365, posta, tenant, migrazione, interno]
---

# Velo-CE · Guida: migrazione della posta al tenant unico (INTERNO)

## Riassunto

Guida interna BlueAge (v001 del 20/10/2026, 8 pagine, non mostrabile al cliente) per portare la posta di [[velo-ce]] da tre tenant Microsoft 365, uno per dominio, al tenant unico di `velo-ce.eu` deciso il 20/10 per posta e Business Central, tenendo i domini di brand. È lavoro Microsoft 365 fuori dal perimetro di Business Central, con esecutore da decidere. ID dei tenant e dettagli dei record omessi. Disponibile anche in Word.

## Punti chiave

- **Punto di partenza** (letture dai DNS pubblici del 20/10): tre tenant Exchange Online per velo-ce.eu, veloe.eu e vannicholas.com, più un dominio .it su hosting esterno; le caselle di velo-ce.eu restano dove sono, si spostano le altre.
- **Tre anomalie**: DKIM di vannicholas.com che punta ancora al tenant del gruppo da cui il marchio è stato acquisito; due record DMARC su vannicholas.com; firme DKIM di Microsoft 365 assenti su velo-ce.eu e veloe.eu.
- **Decisioni prima** (DM-1…DM-7): tenant di destinazione (deciso), strumento di copia (nativo Microsoft o terze parti), indirizzo principale di chi ha caselle su più domini, destino del dominio .it, chi esegue, data del cutover per dominio, caselle generiche come cassette condivise.
- **Calendario proposto**: cutover a novembre 2026, prima di portare BC nel tenant unico, perché la posta è il canale degli ordini; da evitare dicembre.
- **Prerequisiti bloccanti**: un amministratore su tutti e tre i tenant (account attesi dal fornitore che oggi segue la posta) e accesso ai DNS dei domini presso due provider.
- **Fasi**: inventario, scelta dello strumento (con una decina di caselle e solo posta conviene un tool di terze parti), preparazione del tenant unico, copia iniziale, cutover di un dominio alla volta nel fine settimana, poi DKIM e DMARC, riflessi su BC (account e-mail per l'invio dei documenti) e sui sistemi mittenti esterni, dismissione dei tenant di origine.
- **Rischio da correggere**: la registrazione So Smart chiesta su veloe.eu va portata su velo-ce.eu prima di qualunque acquisto.

## Numeri

- Tre tenant di posta più un dominio su hosting esterno; cassette condivise senza licenza fino a 50 GB (documentale).

## Decisioni e azioni

- Deciso il 20/10 (Cristian e Stefano): tenant unico `velo-ce.eu` per posta e BC.
- [ ] Far correggere a So Smart la registrazione dell'abbonamento sul tenant velo-ce.eu prima di qualunque acquisto ([[velo-ce-guida-migrazione-posta-al-tenant-unico-interno]])

## Versioni

- Velo-CE - Guida migrazione posta al tenant unico - INTERNO - v001.pdf · 2026-10-28 · prima versione ingerita; cartella `Cristian/08 Guide/`; anche in .docx
