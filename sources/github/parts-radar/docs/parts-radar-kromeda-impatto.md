---
type: source-doc
source: github
family: parts-radar-kromeda-impatto
current:
  item_id: "cristian-schifone/parts-radar:docs/kromeda-impatto-parts-radar.md"
  uri: "github://cristian-schifone/parts-radar/docs/kromeda-impatto-parts-radar.md@48bd26c78c4f24ec80d6e25222a83a0ae99b189b"
  web_url: "https://github.com/cristian-schifone/parts-radar/blob/main/docs/kromeda-impatto-parts-radar.md"
  name: "docs/kromeda-impatto-parts-radar.md"
  last_modified: 2026-10-26T23:47:59Z
versions:
  - { name: docs/kromeda-impatto-parts-radar.md@48bd26c, item_id: cristian-schifone/parts-radar:docs/kromeda-impatto-parts-radar.md, last_modified: 2026-10-26T23:47:59Z }
  - { name: docs/kromeda-impatto-parts-radar.md@b8b0773, item_id: cristian-schifone/parts-radar:docs/kromeda-impatto-parts-radar.md, last_modified: 2026-10-22T16:12:54Z }
also_at: []
status: active
partial: true
ingested_at: 2026-10-27T06:22:42Z
projects: ["[[parts-radar-sviluppo]]"]
clients: ["[[solera]]", "[[adac-bologna]]"]
topics: ["[[parts-radar]]"]
tags: []
---

# Kromeda_WS · consumi e costi (stima viva)

## Riassunto

Analisi d'impatto del passaggio da TecDoc a Kromeda_WS di [[solera]]; nel vault si legge solo il §9, la stima viva di chiamate, crediti targa e costi, aggiornata a ogni dato nuovo (ultima revisione 27/10/2026, con il costo della trascrizione dei vocali). Il resto del documento è in parte superato dal passaggio a Python.

## Punti chiave

- Il catalogo diventa OE-first: si parte dal codice originale del costruttore e si scende agli equivalenti aftermarket
- La fascia di chiamate si dimensiona sul picco: oltre la fascia Solera sospende l'account fino alle 05:00 del giorno dopo. Il servizio tiene un contatore proprio e vicino alla soglia passa le richieste all'operatore
- I crediti targa si pagano a parte; una targa già cercata nello stesso giorno non consuma credito
- La ricerca per codice (senza targa) non consuma crediti targa: in media 3,7 chiamate per codice
- Il router in ingresso costa circa 0,3 $ al giorno di LLM al ritmo del pilot e riduce le richieste false
- Con la modalità ascolto i clienti non abilitati non consumano né chiamate Kromeda né crediti targa
- Trascrizione dei vocali (Gemini 3.5 Transcribe, integrata ma spenta): costo trascurabile e nessuna chiamata Kromeda; l'effetto indiretto è che più targhe vere arrivano alla ricerca, quindi più crediti targa sulle richieste nate dai vocali, non ancora misurato. Manca un tetto giornaliero di spesa
- Prezzi di fascia e crediti ancora da chiedere a Solera; il VIN via REST non arriva prima di gennaio 2027

## Numeri

- Volumi: circa 100 richieste e 100 targhe al giorno, 1,5 pezzi per richiesta (da misurare), 22-26 giorni lavorativi al mese, picco × 1,5
- Formula: chiamate al giorno ≈ 2 × targhe + 14 × pezzi (3 × targhe con la riserva dei crediti attiva)
- Chiamate: circa 2.300 al giorno di media, 3.500 di picco, 50.000-60.000 al mese. Fascia da chiedere per il pilot: circa 3.500 al giorno
- Crediti targa: circa 2.200-2.600 al mese
- VIN dal 2027: circa 220-330 decodifiche al mese a 1,30 €, cioè 290-430 €/mese
- Tempo operatore sui casi che vogliono il VIN: 10-15 casi al giorno, 30-45 minuti
- Trascrizione: circa 0,0051 $ al minuto (misurato dal vivo il 27/10), circa 1 $ al mese al volume del pilot. Sul test di H la trascrizione fa salire la targa giusta dal 19,5% al 78,4% dei pezzi

## Decisioni e azioni

- Da chiedere a Solera: fasce e prezzi delle chiamate, prezzo dei crediti targa, se le chiamate in errore contano, URL delle foto, cache oltre le 24 ore
- Da compilare: costo dello stack legacy dismesso (TecDoc, Plate Check, OpenAPI) per il confronto

## Versioni

- docs/kromeda-impatto-parts-radar.md@48bd26c · 2026-10-27 · §9: nuova riga sul costo della trascrizione dei vocali (misurato dal vivo) e sul suo effetto sui crediti targa
- docs/kromeda-impatto-parts-radar.md@b8b0773 · 2026-10-22 · prima lettura nel vault (§9)
