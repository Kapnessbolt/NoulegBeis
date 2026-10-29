---
type: source-doc
source: sharepoint
family: velo-ce-handoff-app-eos-accruals-chiusura-e-pda
current:
  item_id: 01EFCYUZ5A275GXBDMXFCKOEDYJ2LYGLHQ
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ5A275GXBDMXFCKOEDYJ2LYGLHQ
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/00 Progetto/Handoff/handoff-2026-10-04-app-eos-accruals-chiusura-e-pda.md
  name: handoff-2026-10-04-app-eos-accruals-chiusura-e-pda.md
  last_modified: 2026-10-08T10:43:54Z
versions:
  - { name: handoff-2026-10-04-app-eos-accruals-chiusura-e-pda.md, item_id: 01EFCYUZ5A275GXBDMXFCKOEDYJ2LYGLHQ, last_modified: 2026-10-08T10:43:54Z }
also_at:
  - { web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Cristian/00 Progetto/Handoff/handoff-2026-10-04-app-eos-accruals-chiusura-e-pda.md", item_id: 01EFCYUZ6OBEXVJ4K3ZZELYJ5EZ6CNUMBC }
status: active
partial: false
ingested_at: 2026-10-22T13:25:33Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [handoff, app-eos, ratei-risconti, accruals, pda, interno]
---

# Velo-CE · Handoff del 04/10/2026: Accruals (EX001) chiusa, prossima app Posted Data Administration Tool

## Riassunto

Handoff interno BlueAge della chat del 02-04/10/2026 su Accruals and Simulated Common Library (EX001) e la sua famiglia di app EOS, nel filone di analisi delle app in vista del cambio tenant e di Premium. L'esito: ratei e risconti dell'app e contabilità simulata non sono usati dal 2023, i risconti oggi si fanno a mano in contabilità generale e il registro dei documenti da fatturare si alimenta da solo. EX001 è candidata all'uscita insieme a cinque app collegate, ma la decisione dipende dalla risposta dell'amministrazione alla domanda I09. La prossima chat analizza il Posted Data Administration Tool (EX065, «PDA»), strumento che modifica dati già registrati.

## Punti chiave

- **Ratei e risconti dell'app**: non usati da gennaio 2023, con template solo su contabilità simulata; la contabilità simulata è ferma dal 20/05/2023; il calcolo delle fatture da emettere e ricevere non è mai stato eseguito.
- **Registro dei documenti da fatturare**: vivo ma automatico (si riempie alla registrazione di DDT e fatture); gli acquisti si fermano al 29/04/2026, causa da rilevare. «Crescere non vuol dire essere usato».
- **Risconti oggi**: a mano in contabilità generale, con riga al 31/12 e storno unico all'1/1; la chiusura 2025 è stata registrata a settembre 2026 e la chiusura e apertura conti 2025-2026 è stata lanciata tre volte e stornata due.
- **Close Documents Without Invoicing**: mai usata. **Setup magazzino**: costo previsto e registrazione automatica dei costi in C/G disattivati; il valore di magazzino va in C/G solo con la registrazione periodica (chi la esegue da rilevare).
- **Ordini di vendita**: un caso reale mostra l'ordine che resta aperto dopo spedizione e fattura (fattura fatta dalle spedizioni).
- **Conclusione su EX001**: l'unica funzione senza equivalente standard che potrebbe servire è l'elenco dei documenti da fatturare a una data passata; se l'app esce, escono sei app (EX001, EX001.01, EX041, EX041.02, EX041.01, EX063.02).
- **PDA (prossima app)**: modifica o cancella dati di qualunque tabella anche registrati, per consulenti esperti; 7 richieste nel 2026 su liquidazione IVA, libro giornale, un movimento C/G e righe di fatture d'acquisto; tema di governance per il titolare (GOV-14) e domanda I05 all'amministrazione.
- **Metodo**: ciò che i dati non possono dire diventa una domanda al cliente nel questionario, senza aggiungere test; elenchi di test sempre riscritti per intero.
- **App ancora da analizzare**: PDA (EX065), Advanced Document Reporting (EX009), Inventory Valuation and Costing (EX053), VAT Management for Italy (EX020), Withholding Tax CU (EX036); a parte So Smart Application e System.
- **Quadro normativo** (spiegato in chat): competenza e ratei e risconti obbligatori nel bilancio d'esercizio; la contabilità simulata non è un istituto di legge; alternativa standard con scritture vere e storno automatico.

## Numeri

- 140 movimenti di ratei e risconti, tutti di gennaio 2023; 672 movimenti di contabilità simulata, fermi dal 20/05/2023.
- PDA: 4.515 righe, 7 richieste nel 2026, 2.222 righe di richiesta e log.
- Evidenze E135-E149 archiviate; prossimo codice libero E150.

## Decisioni e azioni

- Decisione (Cristian, 04/10): i casi reali rimasti su EX001 non si fanno; restano le domande nel questionario.
- Decisione (Cristian, 03/10): EX001 è candidata all'uscita, non provata inutile.
- Decisione (04/10): ciò che lo standard non copre diventa una domanda all'amministrazione, non un nuovo test; nuovo foglio «Funzioni per app» nell'Excel delle app, aggiornato sul posto.
- [ ] Analizzare il Posted Data Administration Tool (EX065): tema di dominio, uso reale da E117, impatti sul cambio tenant
- [ ] Analizzare poi EX009, EX053, EX020, EX036, una per volta
- [ ] Aggiornare gli open point CT-31 e CT-13 con l'esito di EX001, oltre ai pendenti CT-18, CT-19, CT-25
- [ ] Proporre l'aggiornamento del documento di progetto con l'esito di EX001
- [ ] Dopo la call del 06/10 chiudere FE1, FE2, FE4, FE5

## Versioni

- handoff-2026-10-04-app-eos-accruals-chiusura-e-pda.md · 2026-10-08 · prima versione ingerita; contenuto del 04/10/2026, data di modifica della riorganizzazione della cartella
