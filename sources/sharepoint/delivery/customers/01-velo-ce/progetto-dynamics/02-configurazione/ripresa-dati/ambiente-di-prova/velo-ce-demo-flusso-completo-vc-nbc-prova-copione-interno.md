---
type: source-doc
source: sharepoint
family: velo-ce-demo-flusso-completo-vc-nbc-prova-copione-interno
current:
  item_id: 01EFCYUZZV73IGQAD5YBAKG3BJFLEUUX2R
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZZV73IGQAD5YBAKG3BJFLEUUX2R
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/02 Configurazione/Ripresa Dati/Ambiente di prova/Velo-CE - Demo flusso completo VC-NBC PROVA - copione - INTERNO - v001.md
  name: Velo-CE - Demo flusso completo VC-NBC PROVA - copione - INTERNO - v001.md
  last_modified: 2026-10-28T08:06:49Z
versions:
  - { name: "Velo-CE - Demo flusso completo VC-NBC PROVA - copione - INTERNO - v001.md", item_id: 01EFCYUZZV73IGQAD5YBAKG3BJFLEUUX2R, last_modified: 2026-10-28T08:06:49Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-29T06:13:53Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, demo, pianificazione, conto-lavoro, varianti, power-bi, interno]
---

# Velo-CE · Copione della demo del flusso completo in VC-NBC PROVA (INTERNO)

## Riassunto

Copione interno BlueAge (v001, preparato da Claude il 17/10/2026 su richiesta di Cristian, aggiornato il 18/10) per la demo a Stefano di [[velo-ce]] prevista il 20/10, nella società di prova VC-NBC PROVA dell'ambiente BlueAge in esperienza Premium. Mostra un giro completo in BC standard: acquisto dei tubi, telaio sabbiato a scorta, telaio verniciato per colore in conto lavoro, bici in assemblaggio su ordine con il colore in variante, fattura e report.

## Punti chiave

- **Messaggio**: il colore come variante regge il processo (fabbisogno, ordine al verniciatore e prezzo per colore); il punto debole è il report delle vendite per colore, che passa da Power BI sulle API standard.
- **Dati preparati**: 40 articoli e 2 servizi con codici nuovi collegati al codice di oggi; clienti e fornitori rivenditori presi da Educational; 7 colori di listino più un custom; listino con una riga per bici e colore; scorte per colore sulle unità di stockkeeping (standard a scorta, glossy e custom su ordine); verniciatore come area di produzione in conto lavoro.
- **Sei atti** (30-40 minuti): struttura, pianificazione, telaio sabbiato, verniciato in conto lavoro, vendita con il colore, report.
- **Limiti da dichiarare**: valori segnaposto per verniciatura e tempi; verniciato a scorta per colore come opzione, in contrasto con la nota tecnica del pilota; variante del telaio da mettere a mano sull'assemblaggio su ordine; servizi creati per errore come articoli di magazzino; registrazione automatica dei costi spenta come oggi; famiglia e finitura calcolate in Power BI, non in BC.
- **Power BI**: report a quattro pagine (vendite per colore, scorte e punto di riordino, proposte del piano, articoli).

## Numeri

- Costo standard del telaio verniciato 118,56 € (sabbiato 73,16 + forcella 10,40 + verniciatura 35,00); bici 1.383-1.521 €; prezzi bici 2.470-2.923 € (inventati).
- Fatturato del mese in prova 14.262 €; Power BI: 5 bici, 13.862 €, 20% glossy.

## Decisioni e azioni

- Nessuna decisione formale.

## Versioni

- Velo-CE - Demo flusso completo VC-NBC PROVA - copione - INTERNO - v001.md · 2026-10-28 · prima versione ingerita; cartella `Cristian/02 Configurazione/Telaio e produzione/Ambiente di prova/`
