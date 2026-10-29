---
type: source-doc
source: sharepoint
family: velo-ce-pilota-lungo-bici-completa-nota-tecnica-leo
current:
  item_id: 01EFCYUZ75RIELC5KSFFA2YVLALKINI7LM
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ75RIELC5KSFFA2YVLALKINI7LM
  web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/02 Configurazione/Telaio e produzione/Velo-CE - Pilota Lungo bici completa - Nota tecnica Leo - v001.md"
  name: "Velo-CE - Pilota Lungo bici completa - Nota tecnica Leo - v001.md"
  last_modified: 2026-10-08T10:44:31Z
versions:
  - { name: "Velo-CE - Pilota Lungo bici completa - Nota tecnica Leo - v001.md", item_id: 01EFCYUZ75RIELC5KSFFA2YVLALKINI7LM, last_modified: 2026-10-08T10:44:31Z }
also_at:
  - { web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/99 Project Claude (copia)/velo-ce-pilota-lungo-nota-tecnica-2026-09-23.md", item_id: 01EFCYUZZBKCZATY5JT5B3R7PQXW6PRNDR }
  - { web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Cristian/99 Project Claude (copia)/velo-ce-pilota-lungo-nota-tecnica-2026-09-23.md", item_id: 01EFCYUZYDLXD6IEP5ZJEKUFF7IJVEXA2S }
  - { web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Cristian/02 Configurazione/Telaio e produzione/Velo-CE - Pilota Lungo bici completa - Nota tecnica Leo - v001.md", item_id: 01EFCYUZ4A35G73C6BC5ALSAR3HRFHVNK5 }
status: active
partial: false
ingested_at: 2026-10-22T13:28:59Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [pilota-lungo, architettura, ato, mts, conto-lavoro, codifica, business-central-premium]
---

# Velo-CE · Pilota Lungo bici completa: nota tecnica di allineamento BlueAge / Trif

## Riassunto

Nota tecnica interna del 23/09/2026 che fotografa lo stato del pilota prima di costruire l'Excel del modello dati, separando le decisioni prese dai punti da affinare in sandbox. Il pilota non è la configurazione definitiva di Velo-CE: deve costruire un modello dati e operativo eseguibile di una bici Lungo completa (riferimento MLCA-5E-545-CDX), configurabile in una sandbox BC Premium e testabile end-to-end, dall'ordine della bici alle materie prime. Principio guida: completezza strutturale prima della precisione dei parametri, con segnaposto [PH] dove il dato manca. Propone un'architettura ibrida (bici assemblata su ordine, telaio verniciato su domanda, buffer interni a scorta, verniciatura in conto lavoro) e chiude con 17 punti di sintesi della proposta BlueAge.

## Punti chiave

- **Cos'è il pilota Lungo**: una bici cargo Multi Lungo con motore Bosch modellata per intero in BC Premium per dimostrare il giro bici-telaio-materie prime prima di estenderlo a Multi, altre configurazioni e Van Nicholas.
- **Architettura**: dealer/B2B → Veloce CRM e working paper → [integrazione futura] → bici finita ATO ← telaio verniciato (su domanda, piccolo extra-stock deciso da Augusto) ← verniciatura esterna in conto lavoro ← telaio sabbiato MTS (ultimo stock comune, punto di postponement del colore) ← triangolo MTS ← 5 componenti laser + housing MTS ← 3 parti housing MTS ← materie prime. Il carro è una distinta fantasma.
- **Regola di progetto**: articolo quando esiste una vera scorta autonoma; ciclo per descrivere le lavorazioni tra una scorta e la successiva. Telaio puntato e saldato non sono articoli.
- **Planning**: parametri di riordino già su tutta la catena MTS con valori iniziali assunti; BC propone, il reparto (Ranzini) accetta, modifica o crea ordini a mano. Una sola registrazione finale per lotto dove possibile; scarico in avanti o indietro da provare.
- **Verniciatura**: conto lavoro con centro terzista provvisorio, 12 €/telaio e 3 giorni [PH], vernice inclusa; trasporto non modellato (verniciatore a circa 5 km, telai portati con il furgone).
- **Configurazione**: non reinventare il configuratore in BC; il dealer configura nel B2B e la specifica arriva al working paper di Veloce CRM, oggi non legato agli articoli BC. Modello target: base bici + ordine di assemblaggio configurato dal working paper, con effetti di sostituzione, aggiunta e gruppo coerente. Configurabili almeno colore, motorizzazione, batteria, gruppo/trasmissione, accessori.
- **Codifica**: deliberatamente non risolta; nel pilota codici provvisori LU-001…, codici BC esistenti solo se il match è affidabile, [PH] altrimenti. Il pilota servirà a decidere quali dimensioni entrano in codice, descrizione, categoria, attributi o varianti. Fonte dell'anagrafica: [[velo-ce-articoli]].
- **Esito atteso in sandbox**: MTS multilivello con proposte a cascata, lotto laser con una sola dichiarazione, confronto forward/backward, ODP di telaio con il ciclo completo, conto lavoro verniciatura, ordine di assemblaggio ATO configurato.

## Numeri

- Anagrafica di partenza: circa 1.113 righe.
- Verniciatura: 12 €/telaio, 3 giorni di calendario (segnaposto); verniciatore a circa 5 km.
- Sabbiatrice: lotto reale di 8 telai.
- Esempio di extra-stock: domanda 8 telai, ordine di verniciatura 10.

## Decisioni e azioni

- Decisioni prese: bici ATO; telaio sabbiato ultimo stock MTS comune; telaio verniciato articolo intermedio su domanda; 5 componenti laser, 3 parti housing, housing e triangolo come articoli MTS (le 3 parti housing poi superate dalla v008: housing articolo unico); carro fantasma; base bici + ordine di assemblaggio configurato, senza un codice per ogni combinazione.
- [ ] Decidere la modularità della distinta della bici (motorizzazione, trasmissione, ruote, cockpit, accessori come righe singole o moduli) prima di costruire il workbook
- [ ] Provare in sandbox forward e backward flushing sul tubo

## Versioni

- Velo-CE - Pilota Lungo bici completa - Nota tecnica Leo - v001.md · 2026-10-08 · prima versione ingerita (nota datata 23/09/2026; data di modifica dovuta alla riorganizzazione della cartella). Copia identica in "99 Project Claude (copia)" come velo-ce-pilota-lungo-nota-tecnica-2026-09-23.md, registrata in also_at.
