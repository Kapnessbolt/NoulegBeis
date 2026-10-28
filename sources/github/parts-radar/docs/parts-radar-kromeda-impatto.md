---
type: source-doc
source: github
family: parts-radar-kromeda-impatto
current:
  item_id: "cristian-schifone/parts-radar:docs/kromeda-impatto-parts-radar.md"
  uri: "github://cristian-schifone/parts-radar/docs/kromeda-impatto-parts-radar.md@cfbf3b2383cb86a26b5e4f3df57ffbefcbf9c4e6"
  web_url: "https://github.com/cristian-schifone/parts-radar/blob/main/docs/kromeda-impatto-parts-radar.md"
  name: "docs/kromeda-impatto-parts-radar.md"
  last_modified: 2026-10-27T15:11:05Z
versions:
  - { name: docs/kromeda-impatto-parts-radar.md@cfbf3b2, item_id: cristian-schifone/parts-radar:docs/kromeda-impatto-parts-radar.md, last_modified: 2026-10-27T15:11:05Z }
  - { name: docs/kromeda-impatto-parts-radar.md@48bd26c, item_id: cristian-schifone/parts-radar:docs/kromeda-impatto-parts-radar.md, last_modified: 2026-10-26T23:47:59Z }
  - { name: docs/kromeda-impatto-parts-radar.md@b8b0773, item_id: cristian-schifone/parts-radar:docs/kromeda-impatto-parts-radar.md, last_modified: 2026-10-22T16:12:54Z }
also_at: []
status: active
partial: true
ingested_at: 2026-10-28T06:23:41Z
projects: ["[[parts-radar-sviluppo]]"]
clients: ["[[solera]]", "[[adac-bologna]]"]
topics: ["[[parts-radar]]"]
tags: []
---

# Kromeda_WS · consumi e costi (stima viva)

## Riassunto

Analisi d'impatto del passaggio da TecDoc a Kromeda_WS di [[solera]]; nel vault si legge solo il §9, la stima viva di chiamate, crediti targa e costi, aggiornata a ogni dato nuovo (ultima revisione 27/10/2026 sera, con la doppia lettura dei vocali). Il resto del documento è in parte superato dal passaggio a Python.

## Punti chiave

- Il catalogo diventa OE-first: si parte dal codice originale del costruttore e si scende agli equivalenti aftermarket
- La fascia di chiamate si dimensiona sul picco: oltre la fascia Solera sospende l'account fino alle 05:00 del giorno dopo. Il servizio tiene un contatore proprio e vicino alla soglia passa le richieste all'operatore
- I crediti targa si pagano a parte; una targa già cercata nello stesso giorno non consuma credito
- La ricerca per codice (senza targa) non consuma crediti targa: in media 3,7 chiamate per codice
- Il router in ingresso costa circa 0,3 $ al giorno di LLM al ritmo del pilot e riduce le richieste false
- Con la modalità ascolto i clienti non abilitati non consumano né chiamate Kromeda né crediti targa
- Trascrizione dei vocali (integrata ma spenta): dal 27/10 ogni vocale lo leggono due motori, Soniox UE primo e Gemini 3.5 Transcribe di controllo, con un tetto di spesa di 1 $ al giorno. Costo ancora trascurabile e nessuna chiamata Kromeda: una targa da ascoltare non fa ricerche, quindi 0 crediti targa. L'effetto indiretto (più targhe vere alla ricerca, più crediti sulle richieste nate dai vocali) non è ancora misurato. Il consenso di ADAC deve nominare Soniox e Google
- Prezzi di fascia e crediti ancora da chiedere a Solera; il VIN via REST non arriva prima di gennaio 2027

## Numeri

- Volumi: circa 100 richieste e 100 targhe al giorno, 1,5 pezzi per richiesta (da misurare), 22-26 giorni lavorativi al mese, picco × 1,5
- Formula: chiamate al giorno ≈ 2 × targhe + 14 × pezzi (3 × targhe con la riserva dei crediti attiva)
- Chiamate: circa 2.300 al giorno di media, 3.500 di picco, 50.000-60.000 al mese. Fascia da chiedere per il pilot: circa 3.500 al giorno
- Crediti targa: circa 2.200-2.600 al mese
- VIN dal 2027: circa 220-330 decodifiche al mese a 1,30 €, cioè 290-430 €/mese
- Tempo operatore sui casi che vogliono il VIN: 10-15 casi al giorno, 30-45 minuti
- Trascrizione: con due motori circa 0,0068 $ al minuto (Soniox circa 0,0017 $, Gemini circa 0,0051 $), un terzo in più del solo Gemini; tetto 1 $ al giorno, 10 vocali per lavoro, 2 MB o 5 minuti per vocale. Spesa della sessione di sviluppo circa 0,06 $. Sul test di H la trascrizione fa salire la targa giusta dal 19,5% al 78,4% dei pezzi

## Decisioni e azioni

- Da chiedere a Solera: fasce e prezzi delle chiamate, prezzo dei crediti targa, se le chiamate in errore contano, URL delle foto, cache oltre le 24 ore
- Da compilare: costo dello stack legacy dismesso (TecDoc, Plate Check, OpenAPI) per il confronto

## Versioni

- docs/kromeda-impatto-parts-radar.md@cfbf3b2 · 2026-10-27 · §9: doppia lettura dei vocali (Soniox più Gemini), costo al minuto dei due motori, tetto giornaliero di 1 $, nessun effetto sui crediti targa
- docs/kromeda-impatto-parts-radar.md@48bd26c · 2026-10-27 · §9: nuova riga sul costo della trascrizione dei vocali (misurato dal vivo) e sul suo effetto sui crediti targa
- docs/kromeda-impatto-parts-radar.md@b8b0773 · 2026-10-22 · prima lettura nel vault (§9)
