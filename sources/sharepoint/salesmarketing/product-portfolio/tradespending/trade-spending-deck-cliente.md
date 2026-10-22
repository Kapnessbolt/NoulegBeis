---
type: source-doc
source: sharepoint
family: trade-spending-deck-cliente
current:
  item_id: 01EFCYUZYCV72TGWQMSRA3N6JSMY4GS5NN
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKVSDgPuvHRsSIc3xR8AKeVG/01EFCYUZYCV72TGWQMSRA3N6JSMY4GS5NN
  web_url: https://blueagesrl.sharepoint.com/sites/internal/SalesMarketing/Product Portfolio/TradeSpending/Trade_Spending_Deck_Cliente.pptx
  name: Trade_Spending_Deck_Cliente.pptx
  last_modified: 2026-09-07T09:15:38Z
versions:
  - { name: Trade_Spending_Deck_Cliente.pptx, item_id: 01EFCYUZYCV72TGWQMSRA3N6JSMY4GS5NN, last_modified: 2026-09-07T09:15:38Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:02:50Z
projects: []
clients: []
topics: ["[[trade-spending]]"]
tags: [trade-spending, deck-cliente, offerta, sales]
---

# Trade Spending · Presentazione cliente

## Riassunto

Deck commerciale (17 slide, settembre 2026, "Powered by BlueAge") che presenta [[trade-spending]], la piattaforma per governare premi e contributi riconosciuti dall'industria ai clienti della distribuzione. Il percorso è in quattro tappe: cos'è il trade spending, come viene gestito oggi (fogli di calcolo e accordi informali), la piattaforma (modello contratti/poste, motore di calcolo, ciclo di vita dell'accordo) e il controllo (marginalità per cliente, ruoli, integrazione). Chiude con un'adozione in tre fasi e i prossimi passi per avviare il lavoro con un cliente.

## Punti chiave

- **A chi si rivolge**: aziende che riconoscono premi e contributi ai clienti della distribuzione (presenza a scaffale, volantino, target di fatturato, smaltimento, contributi logistici, attività in store e digitali, formazione); il modello nasce da esperienza pluriennale su grande distribuzione e distributori con perimetro internazionale.
- **Problema**: gestione su fogli di calcolo, senza anagrafica comune, con calcoli manuali, liquidazioni poco tracciate, marginalità per cliente non visibile e rinnovi ricostruiti a mano ogni anno.
- **Modello**: ogni accordo è un contratto (annuale, infrannuale o pluriennale, con responsabile) che contiene le poste; ogni posta è ordinaria o straordinaria e, per natura contabile, premio (nota di credito, rettifica ricavi) o contributo (nota di debito, costo marketing). Le tipologie sono un'anagrafica aziendale con codice e conto contabile: aggiungerne una è configurazione, non sviluppo.
- **Dimensioni di applicazione**: asse cliente (fino a 3 livelli ereditati dall'ERP, cliente pagante, un livello aggiuntivo gestito in piattaforma) e asse prodotto (tutto il fatturato o singoli settori merceologici); multi-paese nello stesso modello.
- **Motore di calcolo**: ripartizione automatica di ogni posta su clienti, settori e mesi con il sell-in come driver; poste a percentuale o a valore, a consuntivo o in "Balance to Go" sul budget dei mesi futuri. Gli sconti già in fattura si marcano come statistici: visibili nel totale ma esclusi dal calcolo, per non pagare premi su una base già scontata.
- **Controllo**: conto economico a scalare per cliente e settore (fatturato lordo, pricing, netto, costi diretti, premi e contributi, margine netto cliente); versioni del piano (budget, forecast, consuntivo) con i delta; ruoli separati (KAM, customer care, controllo di gestione, amministrazione, direzione) e visibilità per area di business.
- **Architettura**: ERP, ETL e staging, Trade Spending, data warehouse aperto; non sostituisce l'ERP né impone il reporting (Power BI, Business Objects o altri).

## Numeri

- Data del deck: settembre 2026.
- Esempio di tipologie: codici O101–O108 (ordinarie) e S601–S602 (straordinarie), estratto illustrativo.
- Gerarchia cliente: fino a 3 livelli ereditati dall'ERP più un livello gestito in piattaforma.
- Esempio di calcolo: accordo del 5% su un'intera insegna, valido su tutti i settori.
- Adozione in 3 fasi: Fase 1 nucleo (anagrafica tipologie, contratti e poste, budget di fatturato, motore di calcolo), già utilizzabile da sola; Fase 2 controllo (liquidazione, conto economico, rinnovo automatico, visibilità per area, multi-valuta e multi-country); Fase 3 evoluzioni (workflow di approvazione multi-livello, simulazioni, contabilizzazione automatica verso l'ERP).

## Decisioni e azioni

- Prossimi passi proposti al cliente: analisi del processo attuale (accordi, tipologie di posta, strutture cliente), definizione del perimetro della prima fase e delle integrazioni, proposta operativa con piano, tempi e rilasci.

## Versioni

- Trade_Spending_Deck_Cliente.pptx · 2026-09-07 · prima versione ingerita
