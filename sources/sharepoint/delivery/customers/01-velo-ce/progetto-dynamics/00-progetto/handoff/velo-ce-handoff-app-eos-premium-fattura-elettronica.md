---
type: source-doc
source: sharepoint
family: velo-ce-handoff-app-eos-premium-fattura-elettronica
current:
  item_id: 01EFCYUZYY6KXQ5KB5D5AYYSZNFUPX5CAN
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZYY6KXQ5KB5D5AYYSZNFUPX5CAN
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/00 Progetto/Handoff/handoff-2026-10-01-app-eos-premium-fattura-elettronica.md
  name: handoff-2026-10-01-app-eos-premium-fattura-elettronica.md
  last_modified: 2026-10-08T10:43:54Z
versions:
  - { name: handoff-2026-10-01-app-eos-premium-fattura-elettronica.md, item_id: 01EFCYUZZW4SDQETT3RFHLBAOIUDQSTLQT, last_modified: 2026-10-08T10:43:54Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:25:33Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]", "[[fatturazione-elettronica-sdi]]"]
tags: [handoff, app-eos, premium, fattura-elettronica, interno]
---

# Velo-CE · Handoff del 01/10/2026: app EOS su Premium, partenza da Electronic Invoice for Italy

## Riassunto

Handoff interno BlueAge di una chat del 01/10/2026 sul Project Velo-CE, non mostrabile a So Smart né al cliente. La chat chiusa ha cercato evidenza documentale, app per app, che le app EOS in uso nel Business Central di Velo-CE supportino l'esperienza Premium, in vista della «Strada B»: nuovo BC Premium nel tenant della posta con partenza il 01/01/2027. La chat successiva deve analizzare le app fiscali una alla volta, partendo da Electronic Invoice for Italy (EX063): il tema fiscale sottostante e l'uso reale in Velo-CE, con verifiche a sistema in sola lettura.

## Punti chiave

- **Certificazione Premium**: 12 app su 54 hanno la scheda AppSource che dichiara Essentials e Premium (tra cui EX063 fattura elettronica, EX020 IVA, EX036 Certificazione Unica, EX009 Advanced Document Reporting, EX001.01 ratei e risconti, EX065 Posted Data Administration Tool, EX018 LIPE); le altre 42 sono da verificare. È un'evidenza documentale, non provata a sistema: al cliente si dice «dichiarate compatibili dalla documentazione ufficiale».
- **App EOS sì, pacchetto So Smart no**: tutte le 54 app sono di EOS Solutions, globali, installabili singolarmente da AppSource con le dipendenze; l'installazione in blocco del 2023 viene dal modello commerciale So Smart. Il flusso ordini MMI è un modulo di So Smart Application, non codice su misura: nel nuovo tenant si installa e si riconfigura.
- **Uso delle app**: Posted Data Administration Tool in uso (tema di governance per il titolare); Extended Combine Shipment configurata ma non usata (le fatture differite passano dallo standard); app transazionali con righe solo di setup (Enasarco, provvigioni, omaggi, LIPE) marcate «No – solo setup».
- **Fattura elettronica oggi**: intermediario IX-FE di Able Tech a contratto separato (So Smart usa Able Tech); il job IX-FE è in errore dal 21/04/2024 e quello di creazione e invio è in sospeso, eppure le fatture passano ogni giorno: canale reale da rilevare. Lo standard BC esporta solo l'XML FatturaPA; il framework e-documents per lo SdI è previsto per la 2027 release wave 1, non pronto al 01/01/2027.
- **So Smart Application e System**: la prima contiene MMI, i sei job SOSMART, il campo «C\Lavoro» non usato e il Connettore WMS; la seconda permessi EOS propri, il sistema DSY e il catalogo processi So Smart. So Smart for Italy è un'altra app, il cui listing va letto (il deck v006 inviato al cliente dice «solo Essentials»).
- **Dichiarazioni d'intento**: spiegato il meccanismo dell'esportatore abituale e del plafond; da chiarire se Velo-CE le emette o le riceve.

## Numeri

- 54 app EOS installate: 12 certificate Premium su AppSource, 42 da verificare; nel tenant 124 app in tutto con versioni.
- EX063: 512.788 righe nelle tabelle proprie, circa 1,1 GB; 7.936 documenti in entrata e 4.398 in uscita al 24/09 (4.418 al 29/09).
- Listino So Smart: fatturazione elettronica 1.200 fatture l'anno a 20 euro.
- So Smart System: 336 righe di permessi propri; DSY con 796.256 movimenti, 25.854 righe «App installata», 28 righe di sottoscrizione; catalogo di 382 processi in 35 moduli.
- Posted Data Administration Tool: 7 richieste nel 2026 su liquidazione IVA, libro giornale, C/G e fatture d'acquisto.
- Evidenze E117-E123 salvate il 01/10; prossimo codice libero E124. Versione del Project 025.37.

## Decisioni e azioni

- Decisione (Cristian): perimetro dell'analisi = tre app fiscali citate da Leonardo più le cinque funzioni del deck v006; MMI e configurazione Van Nicholas sono un blocco a parte da chiedere a So Smart in call.
- Decisione: la sola fonte di «certificazione» è la sezione «Supported editions» della scheda AppSource.
- Decisione: Extended Combine Shipment = non in uso; PDA = in uso, tema di governance.
- [ ] Spiegare il ciclo della fattura elettronica italiana (SdI, FatturaPA, conservazione, bollo, autofatture, esterometro)
- [ ] Preparare i controlli a sistema in sola lettura sull'uso reale di EX063 (setup IX-FE, coda processi, un caso attivo e uno passivo)
- [ ] Aggiornare l'Excel delle app (Extended Combine Shipment = No) a file chiuso
- [ ] Ripetere l'analisi per VAT Management, Certificazione Unica e LIPE
- [ ] Leggere il listing di So Smart for Italy e verificare le app ancora «da verificare» per la call con So Smart

## Versioni

- handoff-2026-10-01-app-eos-premium-fattura-elettronica.md · 2026-10-08 · prima versione ingerita; contenuto del 01/10/2026, data di modifica della riorganizzazione della cartella
