---
type: session
date: 2026-10-22
surface: cloud
topics: ["[[blueage]]", "[[pulse]]", "[[ai-foundation-program]]", "[[trade-spending]]"]
outcome: "Step 3, lotto 1: SalesMarketing ingerita (17 fonti), 6 temi, 2 clienti, 2 persone"
---

# Primo caricamento · lotto 1 SalesMarketing

## Obiettivo

Avviare lo step 3 (SPEC 6.5): inventario delle librerie e primo lotto di ingestion.

## Decisioni

- Knowledge esclusa dal perimetro: contiene solo i corsi ufficiali Anthropic e progetti software di esercizio (SPEC 1.5, PR #5).
- SalesMarketing: 16 documenti nuovi ingeriti in parallelo da 4 agenti ingestor, che hanno scritto solo le note fonte; temi, clienti, persone, stato e commit li ha gestiti la sessione.
- Slug generici rinominati: `M1_v15.pptx` → `ai-foundation-program-m1`, `PULSE_K.pdf` → `pulse-presentazione-completa`. Le lettere finali dei deck Pulse (G, K, H, C) sono trattate come suffissi di versione.
- Le due relazioni Manini (testo e slide) sono due famiglie distinte.
- Le 5 immagini di Brand Assets non sono state ingerite: non compaiono nella ricerca di SharePoint, quindi l'ingestion periodica non le vedrebbe mai.
- Nuovi temi: ai-foundation-program, compass, giornata-in-azienda, ai-nei-processi, business-central-ai, trade-spending. Nuovi clienti: manini, meccanotecnica-umbra. Nuove persone: leonardo-pinsone, michele-padoin.
- Progetti non creati: due proposte in `inbox/` (Manini supply chain e magazzino, AI Foundation Program per MTU).

## File toccati

- `sources/sharepoint/salesmarketing/` (16 note nuove)
- `topics/` (6 nuovi, pulse e blueage aggiornati), `clients/`, `people/`, `inbox/`
- `.state/ingest.json` (17 item SharePoint, watermark ancora null)

## Aperti

- [ ] Controllo del campione di 10 note da parte dell'utente
- [ ] Il one-pager Formazione AI è collegato ad ai-foundation-program anche se il nome non compare nel documento: confermare
- [ ] Immagini di Brand Assets: decidere se escludere dalla SPEC i file non indicizzati dalla ricerca
- [ ] M1 letto solo nelle prime 30 slide su 113 (partial)
- [ ] Incoerenza Pulse: "dal 2009" nella presentazione completa, "dal 2012" negli altri documenti
- [ ] Temi proposti dagli agenti e non creati: incentivi e finanza agevolata, canale partner, order-to-cash, Digital Bridge Group
- [ ] Prossimo lotto: Delivery
