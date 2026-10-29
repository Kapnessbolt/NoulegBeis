---
type: source-doc
source: sharepoint
family: velo-ce-indice-codici
current:
  item_id: 01EFCYUZZC3CHG27P26NGZNRMPDSVJFY4R
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZZC3CHG27P26NGZNRMPDSVJFY4R
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/00 Progetto/Velo-CE - Indice codici.md
  name: Velo-CE - Indice codici.md
  last_modified: 2026-10-08T10:43:47Z
versions:
  - { name: Velo-CE - Indice codici.md, item_id: 01EFCYUZZC3CHG27P26NGZNRMPDSVJFY4R, last_modified: 2026-10-08T10:43:47Z }
also_at:
  - { web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Cristian/00 Progetto/Velo-CE - Indice codici.md", item_id: 01EFCYUZYTT6HZYG7FGBDZ73J3OLHZWJGT }
status: active
partial: false
ingested_at: 2026-10-22T13:25:33Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [indice, codici, backlog, governo-progetto, interno]
---

# Velo-CE · Indice dei codici

## Riassunto

Indice interno BlueAge (v001 del 25/09/2026, non mostrabile al cliente) che dice in quale file nasce ogni codice citato nei documenti del progetto Velo-CE su Business Central. La Parte A elenca le famiglie di codici con il file di origine e le collisioni fra sigle uguali; la Parte B descrive uno per uno i codici delle famiglie senza indice proprio (backlog, assunzioni su So Smart, prerequisiti di rilascio, incongruenze, domande interne, open point per Leo, test residui sulla licenza, verifiche del 17/09). Lo stato dei codici non sta qui ma nel file di origine.

## Punti chiave

- **Sigle che collidono**: A, C, D, E, I, L, Q, S, T, V, K hanno più significati a seconda del file; regola: citare sempre il documento di origine. Esempio: D12 è la decisione Essentials o Premium della Mappa cantieri.
- **Famiglie principali**: evidenze E (tenant del cliente) e T (tenant BlueAge); temi di governance GOV-01…21; questionario a So Smart Q01…24 (PS02); divergenze DV-01…47; backlog A, L, G, C, D, K, R, S, RL, PS; cantieri C01…C31 e decisioni D01…D19 della Mappa cantieri ([[velo-ce-mappa-cantieri-dynamics]]); «porte» del piano G-LIC, G-DATI, G-COD, G-SS, G-AMB ([[velo-ce-piano-di-progetto-per-cantieri]]); confronto Essentials/Premium v008.
- **Famiglie nate a ottobre**: PL/MP (processo di lavoro dalla merce in ingresso alla contabilità, dal 05/10); RD/RQ/RF della ripresa dati al 01/01/2027 ([[velo-ce-piano-ripresa-dati-interno]], dal 07/10); NBC-001…185 del piano attività del nuovo ambiente ([[velo-ce-piano-attivita-nuovo-ambiente-interno]], dal 07/10).
- **Backlog**: anagrafica e stati articolo, profilazione utenti, codifica radice più desinenza, distinte del telaio, costi (dazi, trasporto, assemblaggio, conto lavoro, verniciatura esterna), pianificazione MRP, licenze (D12, Power BI, Team Members), accessi (GDAP, accessi permanenti di So Smart), ambienti e rilasci.
- **Assunzioni su So Smart (SS1–SS9)**: BlueAge ha autonomia sulla configurazione standard ma non sullo sviluppo; l'estensione So Smart non blocca anagrafica, codifica, distinte e costi e non vincola il passaggio a Premium.
- **Incongruenze aperte I-01…I-22**: tra dichiarato e sistema, per esempio 571 assemblaggi registrati contro «BC escluso dal flusso assemblaggio», articoli circa 1.100 o 1.112, tre Power BI Pro assegnate contro due comprate, l'utenza `admin@` che è in realtà quella del titolare.
- **Open point per Leo OP-01…OP-15**: telaio della bici pilota (Lungo o Multi), codici dei pezzi, tubi e lamiere, modellazione del verniciato sopra il sabbiato, lotti di Lungo al mese.

## Numeri

- 22 incongruenze, 15 open point per Leo, 10 prerequisiti di rilascio, 32 controlli della finestra di rilascio, 9 assunzioni su So Smart.
- Evidenze sul tenant del cliente fino a E100 (prossimo codice libero E101); prove sul tenant BlueAge T01–T76.
- Piano del nuovo ambiente: righe NBC-001…NBC-185; ripresa dati: RD01–RD26, RQ01–RQ09, RF0–RF4.
- Chiusure citate: R04 conto lavoro in Essentials il 18/09, R06 il 19/09, R02/R03/R08 e I-03 il 20/09, L02 caduta e G01b chiusa il 21/09; L04 Subcontracting gratuita.

## Decisioni e azioni

- Regola: l'indice si aggiorna quando nasce una famiglia nuova o un codice di backlog, non a ogni versione dello stato progetto.
- Le voci chiuse o cadute sono segnate come tali; lo stato corrente si legge nel file di origine.

## Versioni

- Velo-CE - Indice codici.md · 2026-10-08 · prima versione ingerita; contenuto v001 del 25/09/2026, con aggiunte delle famiglie PL/MP, RD/RQ/RF e NBC (05-07/10); data di modifica della riorganizzazione della cartella
