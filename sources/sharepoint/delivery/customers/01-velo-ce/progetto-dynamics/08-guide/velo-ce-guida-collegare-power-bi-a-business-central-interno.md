---
type: source-doc
source: sharepoint
family: velo-ce-guida-collegare-power-bi-a-business-central-interno
current:
  item_id: 01EFCYUZ42IW7O5PBDVNEYRYXDLTGVKKLT
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ42IW7O5PBDVNEYRYXDLTGVKKLT
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/08 Guide/Velo-CE - Guida collegare Power BI a Business Central - INTERNO - v001.pdf
  name: Velo-CE - Guida collegare Power BI a Business Central - INTERNO - v001.pdf
  last_modified: 2026-10-28T08:06:11Z
versions:
  - { name: "Velo-CE - Guida collegare Power BI a Business Central - INTERNO - v001.pdf", item_id: 01EFCYUZYCEAIHYCKPZJDY2MG7URD4IQOS, last_modified: 2026-10-28T08:06:11Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-29T06:12:02Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [guida, velo-ce, power-bi, business-central, api, interno]
---

# Velo-CE · Guida tecnica: collegare Power BI a Business Central (INTERNO)

## Riassunto

Guida tecnica interna BlueAge (v001 del 18/10/2026, 5 pagine) su quale fonte usare per collegare Power BI al Business Central di [[velo-ce]] e come farlo, nata dalla demo del 17-18/10 nella società di prova. Regola: connettore Dynamics 365 Business Central e API standard v2.0; solo se un dato manca si scende di gradino.

## Punti chiave

- **Scala delle fonti**: API standard v2.0 (prima scelta) · pagine e query API nuove in un'estensione (sviluppo, le migliori per volumi grandi) · query standard pubblicate come servizio web (configurazione) · pagine pubblicate come servizio web (le più lente, sconsigliate da Microsoft, solo per demo e prove).
- **Limite per Velo-CE**: l'API degli articoli non ha punto e quantità di riordino e non c'è un'entità per le unità di stockkeeping; per le scorte per colore servirà una pagina API, cioè sviluppo (zona grigia con il partner che ha l'estensione nel tenant).
- **Connettore**: account aziendale; la società si sceglie per nome, quindi in un ambiente nuovo il report si ripunta cambiando un passo; il connettore legge anche i servizi web pubblicati; rimedio provato per la finestra di accesso che si blocca.
- **Pubblicare un oggetto esistente come servizio web** è configurazione, ma in Production si fa solo con l'autorizzazione del cliente.
- **Demo e report vero**: nella demo vendite per colore da API standard e scorte e proposte da pagine pubblicate; nel report vero pagine API dedicate per unità di stockkeeping e righe del prospetto.

## Numeri

- Le API sono fino al 25% più veloci dei servizi web (documentale).

## Decisioni e azioni

- Nessuna decisione formale.

## Versioni

- Velo-CE - Guida collegare Power BI a Business Central - INTERNO - v001.pdf · 2026-10-28 · prima versione ingerita; cartella `Cristian/08 Guide/`
