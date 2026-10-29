---
type: source-doc
source: sharepoint
family: velo-ce-progetto-dynamics-e-power-bi-modelli-e-varianti
current:
  item_id: 01EFCYUZ6FZPQJV6AZ45A3CKEX22CAL6UL
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ6FZPQJV6AZ45A3CKEX22CAL6UL
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/01 Deck cliente/SAL/261021 Velo-CE - Progetto Dynamics e Power BI - Modelli e varianti - v002.pptx
  name: 261021 Velo-CE - Progetto Dynamics e Power BI - Modelli e varianti - v002.pptx
  last_modified: 2026-10-19T18:24:51Z
versions:
  - { name: "261021 Velo-CE - Progetto Dynamics e Power BI - Modelli e varianti - v002.pptx", item_id: 01EFCYUZ6FZPQJV6AZ45A3CKEX22CAL6UL, last_modified: 2026-10-19T18:24:51Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-29T06:10:26Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [deck, sal, velo-ce, codifica, colore, varianti, listino, cliente]
---

# Velo-CE · Deck SAL del 21/10: modelli e varianti (CLIENTE)

## Riassunto

Deck BlueAge di 10 slide (v002 del 21/10/2026) per [[velo-ce]], materiale per il cliente: codice della bici, colore in variante, listino e colore fino al telaio. Segue il deck del 20/10 ([[velo-ce-il-codice-della-bici-e-il-colore-cliente]]) e registra le decisioni: codice della bici in forma P1 senza il colore, colore in variante per listino, glossy e custom, un EAN per variante, colore sul telaio indicato dal back office finché manca un automatismo.

## Punti chiave

- **Verificato il 20/10 nel BC di oggi**: varianti colore presenti su ogni configurazione Veloe con RAL0000 per il custom; usate in fattura dal 2023; solo due bici fatturate senza variante nel 2025-2026; la presentazione sulla ricodifica che le dava come mai usate è corretta.
- **Codice P1**: modello, motore e batteria più allestimento (es. ML-BCX545-01) e colore in variante: 31 codici bici, una configurazione nuova si apre per copia; il codice di oggi resta nei riferimenti articolo.
- **Regole della variante**: RAL più numero, G in coda per il glossy; ogni RAL custom diventa una variante nuova di bici e telaio con la sua riga di listino, RAL0000 non si usa più; prezzo dentro la variante; un EAN per ogni variante.
- **Listino**: unico per tutti i clienti con una riga per bici e colore, da impostare da zero (oggi i listini non si usano).
- **Colore sul telaio**: il back office lo indica sulla riga del telaio dell'ordine di assemblaggio; tre strade per l'automatismo: configuratore EOS (verificato poi il 23/10, non risolve), portale B2B e configuratore Van Nicholas, estensione in BC.
- **Report**: colonna variante e modalità di analisi in BC; Power BI per colore e finitura.

## Numeri

- Ultimi 12 mesi: 1.186 bici, 31 configurazioni, 143 combinazioni con il colore, 221 custom (19%).
- Pacchetto da 1.000 EAN per i primi anni.

## Decisioni e azioni

- Decisi il 21/10: codice P1 con colore in variante; glossy come variante a sé; custom come variante nuova; un EAN per variante; prezzo nella variante; colore del telaio a mano finché manca l'automatismo.
- Da decidere dopo la call EOS del 23/10: la strada per l'automatismo del colore sul telaio.
- [ ] Preparare l'Excel delle combinazioni bici e colore da aprire all'avvio, da far confermare a Velo-CE ([[velo-ce-progetto-dynamics-e-power-bi-modelli-e-varianti]])

## Versioni

- 261021 Velo-CE - Progetto Dynamics e Power BI - Modelli e varianti - v002.pptx · 2026-10-19 · prima versione ingerita (v002); cartella `Cristian/01 Deck cliente/SAL/`
