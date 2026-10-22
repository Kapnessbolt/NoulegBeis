---
type: source-doc
source: sharepoint
family: velo-ce-app-eos-documentazione-ufficiale
current:
  item_id: 01EFCYUZ464D6R3ORXYZBJJ4SWZHBLV5FY
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ464D6R3ORXYZBJJ4SWZHBLV5FY
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/99 Project Claude (copia)/velo-ce-app-eos-documentazione-ufficiale-2026-09-29.md
  name: velo-ce-app-eos-documentazione-ufficiale-2026-09-29.md
  last_modified: 2026-10-08T10:43:52Z
versions:
  - { name: velo-ce-app-eos-documentazione-ufficiale-2026-09-29.md, item_id: 01EFCYUZ464D6R3ORXYZBJJ4SWZHBLV5FY, last_modified: 2026-10-08T10:43:52Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:25:37Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, business-central, eos, so-smart, app, licenze, interno]
---

# Velo-CE · Le 54 app EOS nella documentazione ufficiale

## Riassunto

Documento interno BlueAge del 29/09/2026 (v001), non mostrabile a So Smart né al cliente. Classifica le 54 app EOS installate nel tenant Business Central di Velo-CE leggendo la documentazione ufficiale EOS (help funzionale e tecnico, listino), i listing Microsoft AppSource e il sito di So Smart. Per ogni app riporta codice, livello, funzione, abbonamento, dipendenze dichiarate, kit ed edizione supportata. È complementare al censimento dei dati nel tenant ([[velo-ce-censimento-app-eos]]) e corregge la classificazione «togliere / tenere» del 29/09, già recepita nelle v002 dei due PDF dello stesso giorno.

## Punti chiave

- **Livelli**: 3 app del pacchetto So Smart, 1 EOS Administration Library (base di tutte le app EOS), 9 librerie comuni gratuite, 13 app di aggancio gratuite («… for Italy», «… for ADR»), 28 app funzionali a canone (codici EX…), vendute singolarmente o in kit. Sostituisce la lettura dei «17 componenti tecnici» del PDF del 29/09.
- **So Smart è costruita su Business Central Essentials** (verificato sul listino so-smart.it; il listing AppSource di «So Smart for Italy» la indicherebbe «solo Essential», da riaprire): pesa sulla decisione D12 (passaggio a Premium) e sui punti SS9 e R10. Il tenant oggi è Essentials, la direzione è Premium.
- **Dipendenze che cambiano la classificazione**: Enasarco richiede Commissions (Commissions e Commissions for Italy passano a «da chiarire»); Close Documents with Simulated GL è obbligatoria con Accruals (EX001, in uso), quindi le 3 app CDW restano finché resta Accruals; Packing List richiede Over/Under-Delivery (si tolgono insieme); Advanced Cash Flow richiede Invoicing Plan, non installata; Open Banking supporta solo Premium ed è installata su Essentials senza configurazione.
- So Smart System e So Smart Application non hanno documentazione pubblica; la frase «So Smart System installa e aggiorna le altre app EOS» non ha fonte.
- **Kit nel tenant**: Vendite 4 su 4, Provvigioni 2 su 2, Finance Italia 7 su 10, Magazzino 4 su 7, Finance 3 su 8, Produttività 1 su 2; sei app a canone fuori kit scelte una per una.
- Abbonamento per app o per kit, licenza valida per utenti, ambienti e società illimitati nello stesso tenant; trial di 20 giorni. Il tema del canone è fuori dalle riunioni per decisione del 29/09.
- EOS Administration Library ha un controllo che blocca le chiamate esterne negli ambienti copiati: risponde in parte alla domanda Q13 sulle copie di prova.
- Inventory Valuation and Costing (IVC) fa più della valutazione fiscale (scenari, costo medio, LIFO, full costing, WIP): la decisione «da sostituire» resta, distinguendo la parte fiscale dalla costificazione.

## Numeri

- 54 app EOS: 3 So Smart, 1 base EOS, 9 librerie, 13 aggancio, 28 funzionali.
- 6 app a canone fuori da ogni kit.
- Trial di 20 giorni.

## Decisioni e azioni

- 29/09: tema canone EOS fuori dalle riunioni (decisione).
- 29/09 sera: le sei correzioni ai due PDF del 29/09 (Commissions, CDW, So Smart System, 17 componenti, Premium/Essentials, Advanced Document Reporting) applicate nelle v002 e nel questionario PS02 v007.
- [ ] Riaprire a mano il listing AppSource di «So Smart for Italy» per confermare il vincolo «solo Essential».
- [ ] Chiarire con So Smart che cosa succede al pacchetto So Smart con il passaggio a Premium (D12, SS9, R10).
- [ ] Confermare con So Smart il comportamento delle app negli ambienti copiati (Q13).
- [ ] Leggere quali documenti produce Advanced Document Reporting in Velo-CE (TS12).

## Versioni

- velo-ce-app-eos-documentazione-ufficiale-2026-09-29.md · 2026-10-08 · prima versione ingerita (v001 del 29/09/2026); data di modifica della riorganizzazione della cartella
