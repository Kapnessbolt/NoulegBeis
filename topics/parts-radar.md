---
type: topic
kind: prodotto
projects: ["[[parts-radar-sviluppo]]"]
clients: ["[[adac-bologna]]"]
tags: [ricambi, post-vendita]
updated: 2026-10-26
---

# Parts Radar

## Cos'è

Prodotto di [[ai-nei-processi]] per il banco ricambi: riceve la richiesta per messaggio, vocale o foto della targa, riconosce il veicolo e propone il codice originale e le alternative compatibili; l'operatore conferma.

## Punti chiave

- Flusso in quattro passi (riceve e interpreta, cerca nei sistemi, gestisce l'eccezione, registra), replicabile su fatture e conferme fornitori, ricevimento merci, solleciti, reclami ([[blueage-possibilita]])
- Da 5 a 2 le persone impegnate nel processo ricambi e post-vendita ([[blueage-sintesi]], [[blueage-possibilita]])
- Indicato come "in uso" nel company profile, nel settore della distribuzione di ricambi auto ([[blueage-companyprofile]])
- Citato insieme a Lume-AI tra i progetti da smistare nelle regole della skill Velo-CE ([[velo-ce-regole-skill]])
- Prodotto installato: servizio Python + PostgreSQL + dashboard, un'installazione per cliente sui server BlueAge; il monitoraggio tecnico resta interno e non compare al cliente ([[parts-radar-decisione-stack-python]])
- Catalogo Kromeda di Solera con approccio OE-first: dal codice originale del costruttore agli equivalenti aftermarket, filtrati sui brand a listino del ricambista ([[parts-radar-kromeda-impatto]])
- Sulla demo l'80% dei casi si risolve in modo deterministico dalla sola targa e il 14% resta all'operatore, quasi tutto equipaggiamento di fabbrica ([[parts-radar-kromeda-fase0-risultati]])
- Canale WhatsApp con un tech provider (360dialog, Coexistence): il numero del ricambista resta sull'app del banco ([[parts-radar-whatsapp-fornitori]])

## Dove è usato

- [[adac-bologna]], pilota: [[parts-radar-sviluppo]]

## Fonti

- [[blueage-possibilita]]
- [[blueage-sintesi]]
- [[blueage-companyprofile]]
- [[velo-ce-regole-skill]]
- [[presentazione-e-sintesi-progetto]]
- [[integrazione-api-qricambi-proposta-di-collaborazione]]
- [[parts-radar-aggiornamento-api-test]]
- [[riunione-generale-blueage-28-9-sintesi-e-azioni]]
- [[ws-demo-blue-age]]
- [[2026-10-deepagent]]
- [[ieri-sera-e-oggi-idee-su-cui-ragionare]]
- [[integrazione-api-qricambi]]
- [[riunione-generale-blueage-12-10-punti-emersi-e-prossimi-passi]]
- [[riunione-generale-blueage-19-10-sintesi-azioni-e-one-page]]
- [[twilio-blueage-follow-up]]
- [[parts-radar-architettura]]
- [[parts-radar-decisione-stack-python]]
- [[parts-radar-kromeda-impatto]]
- [[parts-radar-kromeda-fase0-risultati]]
- [[parts-radar-whatsapp-fornitori]]
