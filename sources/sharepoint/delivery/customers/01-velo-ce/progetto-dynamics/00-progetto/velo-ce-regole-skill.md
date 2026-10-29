---
type: source-doc
source: sharepoint
family: velo-ce-regole-skill
current:
  item_id: 01EFCYUZ75CATPRT3RDBC3T6NW6PLKG43K
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ75CATPRT3RDBC3T6NW6PLKG43K
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/00 Progetto/_regole skill.md
  name: _regole skill.md
  last_modified: 2026-10-08T10:43:48Z
versions:
  - { name: _regole skill.md, item_id: 01EFCYUZ75CATPRT3RDBC3T6NW6PLKG43K, last_modified: 2026-10-08T10:43:48Z }
also_at:
  - { web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Cristian/00 Progetto/_regole skill.md", item_id: 01EFCYUZ46KIA7WDO4RVGYBLCMOPVFQDA6 }
status: active
partial: false
ingested_at: 2026-10-22T13:25:33Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[parts-radar]]", "[[twoteam]]"]
tags: [regole, skill, metodo, glossario, transcript, interno]
---

# Velo-CE · Regole per le skill

## Riassunto

Documento interno BlueAge che le skill `transcript-ingest` e `open-point-todo` leggono prima di ogni lavoro sul progetto Velo-CE. Fissa nome e prefisso dei file, i percorsi di transcript, verbali, registro degli open point, stato progetto ed evidenze, le famiglie di codici (CT, OP, TD) e i livelli di certezza. Elenca persone e ruoli lato cliente, partner e BlueAge, un glossario per correggere gli errori della trascrizione automatica e gli altri progetti da smistare. Si aggiorna quando cambiano glossario, persone o percorsi.

## Punti chiave

- **Progetto**: cliente Velo-CE S.r.l. (marchi Veloe e Van Nicholas); per BlueAge lavorano Cristian (Trif) e Leonardo Pinsone (Leo). Prefisso dei file `Velo-CE - `.
- **Percorsi**: transcript integrali in `05 Transcript/` (nome `AAMMGG-HHMM Velo-CE - Transcript - <titolo>.txt`, export in `_originali/`, registro dedicato); verbali nel Claude Project «Velo-CE» con copia in `99 Project Claude (copia)/`; evidenze in `06 Evidenze/`; versioni sostituite in `_superato/`.
- **Registro open point e to-do**: `Velo-CE - Open point - INTERNO - v002.xlsx` (fogli Open point, To-do, To-do chiuse, Riepilogo) è un registro vivo, si aggiorna sul posto senza nuova versione (vedi [[velo-ce-open-point-interno]]).
- **Stato progetto**: nel Claude Project, indice `velo-ce-stato-progetto.md` più blocchi, log revisioni solo in aggiunta.
- **Codici**: CT-nn = cambio tenant, OP-nn = altri punti di progetto, TD-nnn = to-do. Certezza: VERIFICATO, DICHIARATO, DA RILEVARE, DOCUMENTALE; ciò che viene da un transcript è sempre DICHIARATO.
- **Partner e fornitori**: So Smart (partner Business Central dal 2023), EOS Solutions / EOS Online (casa madre e rivenditore delle app), un fornitore per posta e server, We Make Code (Veloce-CRM), lo sviluppatore del portale B2B (identità da rilevare).
- **Glossario**: corregge le storpiature ricorrenti della trascrizione (So Smart, EOS Solutions, Van Nicholas, Veloe, Veloce-CRM, Business Central, Essentials/Premium, MRP, tenant, B2B, BlueAge).
- **Altri progetti da smistare**: PartsRadar / Lume-AI, Pulse, TradeSpending, IFOA, Umbria Business School / SFCU, S.T.R.A.D.E., TwoTeam. Le conversazioni fuori tema si omettono.

## Numeri

- Quattro livelli di certezza; tre famiglie di codici (CT, OP, TD).
- So Smart partner Business Central del cliente dal 2023.

## Decisioni e azioni

- Regola: il registro degli open point non si versiona, si aggiorna sul posto.
- Regola: il link al verbale si aggiunge sulla stessa riga dell'intestazione del transcript, per non spostare i numeri di riga.
- Regola: dopo ogni scrittura nel Claude Project, copia in `99 Project Claude (copia)/` e aggiornamento di `_versione.md`.

## Versioni

- _regole skill.md · 2026-10-08 · prima versione ingerita (data della riorganizzazione della cartella)
