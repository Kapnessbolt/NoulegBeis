---
type: session
date: 2026-10-22
surface: cloud
topics: ["[[business-central-ai]]"]
outcome: "Step 3, lotto 2: Delivery ingerita (84 note), progetti Velo-CE e Manini creati"
---

# Primo caricamento · lotto 2 Delivery

## Obiettivo

Ingerire la libreria Delivery (SPEC 6.5, lotto 2) e creare le schede dei progetti attivi.

## Decisioni

- Ingestion selettiva di Velo-CE (scelta dell'utente): esclusi `05 Transcript` (trascrizioni grezze, riassunte nei verbali), `06 Evidenze/Export` (export grezzi di tabelle) e il progetto software `Lab AL` (SPEC 1.7, PR #7).
- 89 documenti → 84 note, scritte in parallelo da 7 agenti ingestor; docx e pdf della stessa famiglia e le copie in altre cartelle sono in `also_at`.
- Create con l'ok dell'utente le schede progetto `velo-ce-progetto-dynamics` e `manini-supply-chain-magazzino`, con log; tolta la proposta Manini da `inbox/`.
- Nuovo cliente `velo-ce`; nuove persone Cristian Schifone (BlueAge, PM), Stefano Moruzzi, Claudia Crippa, Gabriele Ranzini (Velo-CE), Luigi Sacchi (fornitore IT). Le persone citate solo con il nome (Augusto, Eleonora, Marco, Anton Nijhuis, Paola Cacciolatti) restano nel testo della nota cliente.
- Nessun dato sensibile riportato (GUID, tenant ID, IBAN, account personali).
- Nessun tema nuovo: le proposte degli agenti (fatturazione elettronica SdI, governance del tenant, migrazione e ripresa dati, So Smart/EOS, percorso supply chain e magazzino, Power BI) sono elencate qui sotto.

## File toccati

- `sources/sharepoint/delivery/` (84 note)
- `projects/velo-ce-progetto-dynamics/`, `projects/manini-supply-chain-magazzino/`
- `clients/velo-ce.md`, `clients/manini.md`, `people/` (5 nuove, leonardo-pinsone aggiornata), `topics/business-central-ai.md`
- `.state/ingest.json` (108 item SharePoint, watermark ancora null)

## Aperti

- [ ] Controllo del campione di 10 note da parte dell'utente
- [ ] Temi proposti dagli agenti, da valutare: fatturazione elettronica SdI, governance del tenant, migrazione e ripresa dati BC, So Smart/EOS (partner), percorso supply chain e magazzino (offerta), Power BI
- [ ] Lette in parte: piano attività del nuovo ambiente (righe 173–185), indice evidenze, 6 deck Manini (ultime slide)
- [ ] Prossimo lotto: Shared Documents
