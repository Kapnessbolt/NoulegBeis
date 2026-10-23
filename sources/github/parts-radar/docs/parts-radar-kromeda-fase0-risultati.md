---
type: source-doc
source: github
family: parts-radar-kromeda-fase0-risultati
current:
  item_id: "cristian-schifone/parts-radar:docs/kromeda-fase0-risultati.md"
  uri: "github://cristian-schifone/parts-radar/docs/kromeda-fase0-risultati.md@7777221f21b07a0337166fa83a3e9fed95924c8f"
  web_url: "https://github.com/cristian-schifone/parts-radar/blob/main/docs/kromeda-fase0-risultati.md"
  name: "docs/kromeda-fase0-risultati.md"
  last_modified: 2026-10-22T08:13:17Z
versions:
  - { name: "docs/kromeda-fase0-risultati.md@7777221", item_id: "cristian-schifone/parts-radar:docs/kromeda-fase0-risultati.md", last_modified: 2026-10-22T08:13:17Z }
also_at: []
status: active
partial: true
ingested_at: 2026-10-23T18:23:22Z
projects: ["[[parts-radar-sviluppo]]"]
clients: ["[[solera]]", "[[adac-bologna]]"]
topics: ["[[parts-radar]]"]
tags: []
---

# Kromeda_WS · risultati della Fase 0 sulla demo

## Riassunto

Report unico dei test sull'utenza demo Kromeda dal 19/09/2026: golden set di 51 richieste reali di [[adac-bologna]] su 20 veicoli e censimento di 1.847 casi veicolo × voce. Dice quanto del lavoro si chiude in automatico, dove serve l'operatore e dove serve l'LLM. Nel vault si legge solo la sintesi (§1).

## Punti chiave

- In due casi su tre Kromeda dà un solo codice originale: non serve disambiguare
- Le regole deterministiche dalla sola targa (data di immatricolazione, telaio, ABS, sostituzione dei codici) più l'intersezione dei cross aftermarket portano il deterministico all'80%
- L'LLM serve in un solo passo strutturale: trasformare la richiesta del meccanico nella voce Kromeda; può proporre un default con badge, mai confermato da solo
- Il residuo per l'operatore è quasi tutto equipaggiamento di fabbrica (dischi, fari alogeno/LED, sospensioni, batterie): il banco lo risolve già oggi su PartsLink24 col VIN, e nel pilot resta così
- Il cross va chiesto a due endpoint, ma uno dei due non è certificato al 100% da Kromeda: quegli articoli vanno proposti con un badge
- Targhe con più veicoli: mai assumere il primo, si confrontano i codici voce per voce
- Freni facili; batterie, fari e cristalli restano famiglie difficili anche sulle vendite vere

## Numeri

- Codice originale unico nel 69,1% dei casi (1.277 su 1.847)
- Deterministico 80% (1.472 su 1.847), con i default 86%, operatore 14% (21-30% su VW, 21% su BMW)
- Golden set: articolo corretto raggiungibile in 43 richieste su 51 (84%)
- Targhe multi-veicolo: 9 su 20; sull'Audi A3 anteriore vs Quattro 20 voci su 99 hanno codici diversi
- Crediti targa della demo: 20, tutti usati nella Fase 0

## Decisioni e azioni

- 2026-09-25 · fallback sui veicoli affini attivo dal pilot
- 2026-10-09 · il "D2 debole" conta come deterministico, con badge e mai certificato
- VIN via REST atteso non prima di gennaio 2027

## Versioni

- docs/kromeda-fase0-risultati.md@7777221 · 2026-10-22 · prima lettura nel vault (§1)
