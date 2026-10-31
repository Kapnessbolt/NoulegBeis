---
type: source-doc
source: sharepoint
family: velo-ce-handoff-app-eos-ex063-chiusura-e-accruals
current:
  item_id: 01EFCYUZ2KROTVGYFRMVAZUUMCJOCA3QER
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ2KROTVGYFRMVAZUUMCJOCA3QER
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/00 Progetto/Handoff/handoff-2026-10-02-app-eos-ex063-chiusura-e-accruals.md
  name: handoff-2026-10-02-app-eos-ex063-chiusura-e-accruals.md
  last_modified: 2026-10-29T16:14:38Z
versions:
  - { name: handoff-2026-10-02-app-eos-ex063-chiusura-e-accruals.md, item_id: 01EFCYUZ2KROTVGYFRMVAZUUMCJOCA3QER, last_modified: 2026-10-29T16:14:38Z }
  - { name: handoff-2026-10-02-app-eos-ex063-chiusura-e-accruals.md, item_id: 01EFCYUZ54JMQSFLQO6BD2T5X6QWG2Q4ZP, last_modified: 2026-10-28T08:06:21Z }
  - { name: handoff-2026-10-02-app-eos-ex063-chiusura-e-accruals.md, item_id: 01EFCYUZ57CF5MNSHDKRG2DST2XCIN7A3Q, last_modified: 2026-10-08T10:43:54Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:25:33Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]", "[[fatturazione-elettronica-sdi]]"]
tags: [handoff, app-eos, fattura-elettronica, sdi, accruals, interno]
---

# Velo-CE · Handoff del 02/10/2026: fattura elettronica EX063 chiusa a sistema, prossima app Accruals

## Riassunto

Handoff interno BlueAge della chat del 02/10/2026 sull'app EOS Electronic Invoice for Italy (EX063), nel filone che analizza una per volta le app EOS in uso in vista del cambio tenant e di Premium. Le verifiche a sistema su EX063 sono chiuse: ricostruiti i flussi reali di uscita e di entrata delle fatture elettroniche, il ruolo dell'intermediario e della conservazione, e il fatto che le fatture del conto lavoro emesse con Fatture in Cloud non stanno nell'IVA di BC. Le domande residue vanno all'amministrazione e alla call con So Smart ed EOS del 06/10. La prossima chat analizza Accruals and Simulated Common Library (EX001) e la sua famiglia.

## Punti chiave

- **Decisione del 02/10 (Cristian)**: la fiscalità rientra nel perimetro, perché il cambio tenant obbliga ad analizzarne gli impatti; supera le note precedenti che la davano fuori perimetro.
- **Flusso in uscita (verificato)**: BC con EX063 → Able Tech IX-FE → SdI → cliente; fatture create e inviate dall'utenza del titolare a blocchi serali; notifiche aggiornate di notte da un'utenza dell'amministrazione; progressivo del nome file in crescita (ultimo visto il 01/10).
- **Flusso in entrata (verificato)**: fornitore → SdI → IX-FE → BC con qualunque codice destinatario scritto in fattura; import automatico anche di notte, 3-60 minuti dopo l'arrivo, da un processo ricorrente e non dal job EOS IXFE (in errore dal 21/04/2024); voce della coda esatta da rilevare (probabile dispatcher SOSMART).
- **Codici destinatario**: quello di Able Tech in uso dal 05/01/2023; molte fatture arrivano con il codice di Fatture in Cloud ma passano comunque da IX-FE: forte indizio che l'indirizzo telematico registrato all'Agenzia punti ad Able Tech (FE3).
- **Fatture in Cloud**: usato per il conto lavoro, emette fuori da BC; i movimenti IVA di vendita 2026 contengono solo le serie di BC (FVE, FVI, FVX, FVU, AFV, RCV).
- **Conservazione**: IX-FE non conserva (45 giorni, 90 via API); la conservazione a norma è il servizio separato IX-CE di Able Tech, non di EOS; se è attivo è da rilevare (FE1).
- **Condizioni FE1-FE5** per il nuovo tenant: conservazione IX-CE attiva, contratto Able Tech intestato a Velo-CE, indirizzo registrato all'Agenzia, canale d'invio e cambio di aprile 2024, abbonamento EX063 sul nuovo tenant.
- **Open point in file unico**: le domande interne restano nel questionario per i referenti; nel registro [[velo-ce-open-point-interno]] solo righe di rimando OP-16…OP-19.
- **Accruals (prossima app)**: scritture simulate e autostornanti su conti paralleli per bilanci infrannuali; nello standard BC i risconti si fanno con i modelli di differimento, senza contabilità simulata: da valutare con il commercialista.

## Numeri

- 11 fatture inviate alle 18:26 del 01/10; fra il 17/09 e il 02/10 112 file importati, solo 33 con il codice di Able Tech; nel campione 9 file su 12 con il codice di Fatture in Cloud.
- Excel delle app: 54 app, 2.878.068 righe in totale; Accruals Common Library 37.535 righe (terza app EOS per righe), +341 movimenti fra il 24 e il 29/09.
- Documento di progetto alla versione 025.45; prossimo codice di evidenza E129.

## Decisioni e azioni

- Decisione (02/10): fiscalità in perimetro per gli impatti del cambio tenant.
- Decisione (02/10): verifiche in BC su EX063 chiuse; non proporre altri test a sistema sul tema.
- Decisione (02/10): open point in file unico con righe di rimando al questionario interno.
- Decisione (02/10): Extended Combine Shipment segnata come non in uso; la verifica dei registri IVA cade.
- [ ] Portare FE1, FE2, FE4, FE5 alla call con So Smart ed EOS 📅 2026-10-06
- [ ] Chiarire con l'amministrazione FE3, Fatture in Cloud (fatture o DDT, registri IVA, bilancio, conservazione) e il significato delle serie FVU, AFV, RCV
- [ ] Archiviare le evidenze rimaste da E129 e aggiornare CT-18, CT-19, CT-25
- [ ] Aggiornare la riga EX063 dell'Excel delle app con l'uso reale
- [ ] Avviare l'analisi di Accruals and Simulated Common Library (EX001)

## Versioni

- handoff-2026-10-02-app-eos-ex063-chiusura-e-accruals.md · 2026-10-08 · prima versione ingerita; contenuto del 02/10/2026, data di modifica della riorganizzazione della cartella
