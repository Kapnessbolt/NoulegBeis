---
type: source-doc
source: sharepoint
family: velo-ce-handoff-app-eos-adr-chiusa-e-ivc
current:
  item_id: 01EFCYUZ7YAJBOGIDLYJCLOUFYUDKEQ3LL
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ7YAJBOGIDLYJCLOUFYUDKEQ3LL
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/00 Progetto/Handoff/handoff-2026-10-05-app-eos-adr-chiusa-e-ivc.md
  name: handoff-2026-10-05-app-eos-adr-chiusa-e-ivc.md
  last_modified: 2026-10-29T16:14:39Z
versions:
  - { name: handoff-2026-10-05-app-eos-adr-chiusa-e-ivc.md, item_id: 01EFCYUZ7YAJBOGIDLYJCLOUFYUDKEQ3LL, last_modified: 2026-10-29T16:14:39Z }
  - { name: handoff-2026-10-05-app-eos-adr-chiusa-e-ivc.md, item_id: 01EFCYUZZMSJQ26GLY2FC3OZQ2TUENK6JM, last_modified: 2026-10-28T08:06:21Z }
  - { name: handoff-2026-10-05-app-eos-adr-chiusa-e-ivc.md, item_id: 01EFCYUZ4F5XHYIXXIRJEIP23DPFVJTL24, last_modified: 2026-10-08T10:43:55Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:25:33Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [handoff, app-eos, adr, ivc, valorizzazione-magazzino, interno]
---

# Velo-CE · Handoff del 05/10/2026: Advanced Document Reporting (EX009) chiusa, prossima app Inventory Valuation and Costing

## Riassunto

Handoff interno BlueAge della sessione del 04-05/10/2026 sull'app EOS Advanced Document Reporting (EX009), nel filone di analisi delle app EOS in vista del cambio tenant e di Premium, ora con una sessione per app. ADR è in uso ogni giorno per inviare per e-mail conferme d'ordine e fatture ai clienti esteri nella loro lingua, con una sola grafica Veloe anche per Van Nicholas; DDT e fattura accompagnatoria sono report di So Smart Application costruiti su ADR. ADR è il primo candidato a passare allo standard. La sessione successiva analizza Inventory Valuation and Costing (EX053, IVC), con la domanda centrale se le tabelle IVC arrivano a valorizzare il bilancio di BC.

## Punti chiave

- **ADR in uso (verificato)**: 15 richieste di invio fra il 02/10 e il 04/10 (conferme d'ordine e fatture), tutte completate senza errori e tutte dall'utenza del titolare, anche nel fine settimana (chi invia davvero: domanda I10).
- **Configurazione ADR**: 25 testi e-mail in italiano, inglese, tedesco e francese; destinatari per ruolo amministrativo e vendite; una sola casella di invio; log cancellato dopo un mese e PDF dopo due; invii schedulati e selezione rapida non usati.
- **Multi-brand**: oggi una sola grafica Veloe anche per Van Nicholas; il multi-brand è una richiesta nuova da far confermare.
- **Dipendenza da So Smart**: DDT, fattura accompagnatoria e ordine di assemblaggio sono report di So Smart Application su ADR; senza So Smart Application nel nuovo tenant il DDT va rifatto anche se ADR resta.
- **Valutazione BlueAge**: ADR passa allo standard con layout utente Word, layout documento per cliente e scenari e-mail (configurazione BlueAge); estensione di report solo se mancano dati (DDT, bollo, dichiarazioni d'intento) o serve il marchio per singolo documento.
- **IVC già noto**: modulo vivo, ricalcolato di notte verosimilmente dal job SOSMART; costi FIFO, LIFO e medio ponderato; periodi 2024 e 2025 definitivi, 2026 aperto; giacenze negative e costi a zero nello storico. Decisione del 29/09: sostituire IVC con la valutazione fiscale standard della localizzazione italiana dopo la chiusura del 2026, con il commercialista.
- **Novità dichiarata (05/10)**: l'amministrazione scarica il bilancio da BC e lo passa al commercialista; molti articoli a costo zero possono incidere sulla qualità del bilancio e vanno misurati.
- **Lettura delle app**: app sostituibili con configurazione standard (ADR, IVC, PDA, Accruals) contro nucleo fiscale (EX063 con IX-FE, EX020 IVA, EX036 CU), dove sta la vera decisione sul partner; le app EOS funzionano uguale in Essentials e Premium, il problema è chi fa da partner.

## Numeri

- ADR: 15 invii in tre giorni, 25 testi e-mail, quattro lingue, numerazione dei documenti fino a 13.379.
- IVC: 4.457 righe; storico costi articoli 2.640 righe, storico distinte 1.781, 3 periodi, 16 costi prepartenza.
- Excel delle app: righe EX009-F01…F10 nel foglio «Funzioni per app» (ultima riga 33); evidenze E151-E153, prossimo codice E154; documento di progetto 025.53.

## Decisioni e azioni

- Decisione (Cristian, 05/10): una sessione per app; ordine IVC, poi VAT Management for Italy, poi Withholding Tax CU; a parte So Smart Application e System.
- Decisione: Excel aggiornati come correzione sul posto; una evidenza per pacchetto di export.
- Decisione: il multi-brand è una richiesta nuova da confermare, non un'esigenza da conservare; nessun test aggiuntivo su ADR.
- [ ] Chiedere a So Smart se i report DDT e fattura accompagnatoria esistono fuori da So Smart Application 📅 2026-10-06
- [ ] Sessione IVC: spiegare valore fiscale e valore contabile, poi test in sola lettura su storico costi, costi prepartenza, conti di rimanenza e articoli a costo zero
- [ ] Riscrivere la domanda I01 all'amministrazione con la domanda sul bilancio
- [ ] Poi analizzare VAT Management for Italy (EX020)

## Versioni

- handoff-2026-10-05-app-eos-adr-chiusa-e-ivc.md · 2026-10-08 · prima versione ingerita; contenuto del 05/10/2026, data di modifica della riorganizzazione della cartella
