---
type: topic
kind: tema
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
tags: [fiscale, business-central]
updated: 2026-10-22
---

# Fatturazione elettronica SdI

## Cos'è

Invio e ricezione delle fatture elettroniche tramite il Sistema di Interscambio (SdI), con intermediario e conservazione a norma. Nei progetti Business Central è un vincolo fiscale da garantire a ogni cambio di ambiente, tenant o licenza.

## Punti chiave

- Lo standard di Business Central non trasmette allo SdI: il framework e-documents è previsto solo con la release wave 1 del 2027, quindi per un avvio al 1/1/2027 serve ancora un'app di localizzazione ([[velo-ce-open-point-interno]])
- In Velo-CE l'invio passa dall'app EOS EX063 verso l'intermediario Able Tech (IX-FE), che non conserva: la conservazione a norma è un servizio separato (IX-CE) ([[velo-ce-stato-progetto-03-decisioni-aperte]])
- XML e progressivo del nome file li genera Business Central: in un nuovo tenant vanno portati, altrimenti lo SdI scarta i file come duplicati ([[velo-ce-stato-progetto-03-decisioni-aperte]])
- Cambiare app fiscali significa migrare setup e storico (progressivo SdI, storico delle fatture, plafond) ([[velo-ce-verbale-fornitore-fiscale-premium-ams]])
- Prima di confermare un passaggio a Premium va verificata app per app la compatibilità delle app fiscali: in Velo-CE 12 app EOS su 54 risultano certificate per Premium su AppSource ([[velo-ce-handoff-app-eos-premium-fattura-elettronica]])
- Volumi Velo-CE: circa 513.000 righe nelle tabelle della fattura elettronica, circa 4.400 documenti in uscita e 7.900 in entrata ([[velo-ce-open-point-interno]])

## Dove è usato

- [[velo-ce-progetto-dynamics]]: vincolo bloccante per il go-live del 1/1/2027

## Fonti

- [[velo-ce-open-point-interno]]
- [[velo-ce-stato-progetto-03-decisioni-aperte]]
- [[velo-ce-handoff-app-eos-ex063-chiusura-e-accruals]]
- [[velo-ce-handoff-app-eos-premium-fattura-elettronica]]
- [[velo-ce-app-so-smart-installate-e-premium-interno]]
- [[velo-ce-verbale-fornitore-fiscale-premium-ams]]
