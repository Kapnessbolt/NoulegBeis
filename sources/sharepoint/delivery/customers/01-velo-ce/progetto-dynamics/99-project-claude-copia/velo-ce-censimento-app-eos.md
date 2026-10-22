---
type: source-doc
source: sharepoint
family: velo-ce-censimento-app-eos
current:
  item_id: 01EFCYUZ4K5F3CAU2T7BHJAA4XADQ3RCKA
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ4K5F3CAU2T7BHJAA4XADQ3RCKA
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/99 Project Claude (copia)/velo-ce-censimento-app-eos-2026-09-24.md
  name: velo-ce-censimento-app-eos-2026-09-24.md
  last_modified: 2026-10-08T10:43:52Z
versions:
  - { name: velo-ce-censimento-app-eos-2026-09-24.md, item_id: 01EFCYUZ4K5F3CAU2T7BHJAA4XADQ3RCKA, last_modified: 2026-10-08T10:43:52Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:25:37Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, business-central, eos, so-smart, app, censimento, interno]
---

# Velo-CE · Censimento delle app EOS nel tenant

## Riassunto

Documento interno BlueAge (v004, 24-29/09/2026), non mostrabile a So Smart né al cliente. Censisce le app EOS installate nel Business Central di Velo-CE leggendo gli export delle pagine «Tutti gli oggetti» (5.254 oggetti) e «Informazioni tabella» (148 tabelle con righe): le app sono 54, non 3 come risultava allo stato progetto v024. Misura quali sono davvero usate, decodifica il «flusso MMI» di So Smart (canale di ingresso degli ordini di vendita), riporta le versioni in Production al 25/09 e l'attività delle app fra il 24 e il 29/09. Base dei «tre livelli» presentati a Velo-CE il 29/09: 54 installate, 7 in uso, 2 sui cantieri. Complementare a [[velo-ce-app-eos-documentazione-ufficiale]].

## Punti chiave

- **54 app EOS** in Production (confermato il 25/09 dall'Admin Center), tutte di tipo Global; una sola società, VELO-CE SRL.
- **Uso reale**: 17 app con dati, 12 solo setup, 25 senza righe; i dati (circa 1,9 GB) sono quasi tutti in So Smart Application, So Smart System ed Electronic Invoice for Italy.
- **Flusso MMI** (So Smart Application): interfaccia generica di import/export con 25 flussi configurati; in pratica tutti i movimenti sono del flusso SALES, cioè ordini di vendita in ingresso dal canale B2B (anche bici Veloe complete, non solo accessori). Nessun movimento su giornale articoli o assemblaggi: l'origine MMI delle rettifiche positive su AMFR è quasi esclusa.
- **So Smart System** ha un proprio strato di autorizzazioni e un sistema di distribuzione delle app (DSY): un'utenza BlueAge con permessi standard potrebbe non bastare per gli oggetti EOS (A13, Q12).
- **Inventory Valuation and Costing (IVC)** in uso, con riscrittura notturna dei costi del periodo 2026: tocca il cantiere 7 (costificazione), priorità del progetto; va capito chi lo usa e per cosa prima di disegnare K01-K03.
- Chiusi tre dubbi: Connettore WMS installato e non configurato; MDI Master Data Intercompany app separata mai attivata; Product Configurator con solo setup (rischio basso sulla ricodifica).
- **Fatturazione elettronica** (fuori perimetro): job IXFE in errore dal 2024 e job di invio in sospeso, ma i documenti in uscita ci sono: non riattivare quei job a fine finestra.
- Posted Data Administration Tool consente di modificare dati registrati: tema di governance da leggere.
- **Versioni in Production al 25/09**: 10 app su 54 hanno un aggiornamento in attesa (fra cui So Smart Application e IVC); chi decide quando si applicano è la domanda Q09.
- **Attività 24-29/09**: sette app in uso (So Smart Application, So Smart System, Electronic Invoice, Advanced Document Reporting, Accruals, VAT Management, IVC).
- Avvertenza: endpoint, chiavi o password nelle tabelle di setup non vanno fotografati né riportati.

## Numeri

- 5.254 oggetti EOS; 148 tabelle con righe; 595 estensioni di tabella.
- Flusso MMI: 25 flussi, 25.515 movimenti (ultimo n. 26.809 al 24/09), 1,43 milioni di righe di log (circa 478 MB).
- DSY: 796.256 movimenti, 25.854 righe «app installata», 28 righe di sottoscrizione.
- Fattura elettronica: 7.936 documenti in entrata, 4.398 in uscita, circa 1,1 GB.
- IVC: 2.640 righe di storico costi articoli, 1.781 di storico distinte.
- 24→29/09: +232 movimenti MMI (stima circa 33 ordini), +341 righe documenti da fatturare.
- Canone So Smart citato: 768 euro al mese.

## Decisioni e azioni

- [ ] Leggere in sola lettura le sottoscrizioni DSY (tabella 18091029) per capire quali moduli EOS sono attivi, prima dell'analisi delle fatture EOS.
- [ ] Leggere le richieste PDA (tabelle 18123826-18123827): chi ha modificato dati registrati e dove.
- [ ] Capire chi usa IVC e per cosa prima della costificazione (K01-K03).
- [ ] Inserire le autorizzazioni EOS nella richiesta A13 e nel questionario So Smart (fatto nel questionario v004 del 27/09, Q12).

## Versioni

- velo-ce-censimento-app-eos-2026-09-24.md · 2026-10-08 · prima versione ingerita (v004 del 29/09/2026); data di modifica della riorganizzazione della cartella
