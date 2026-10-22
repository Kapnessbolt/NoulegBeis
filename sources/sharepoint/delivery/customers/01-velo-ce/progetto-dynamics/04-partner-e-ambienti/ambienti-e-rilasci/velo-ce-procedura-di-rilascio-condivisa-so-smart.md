---
type: source-doc
source: sharepoint
family: velo-ce-procedura-di-rilascio-condivisa-so-smart
current:
  item_id: 01EFCYUZ22YPHBOGH7V5GYEDKYAUC7Y2RH
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ22YPHBOGH7V5GYEDKYAUC7Y2RH
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/04 Partner e ambienti/Ambienti e rilasci/Velo-CE - Procedura di rilascio condivisa - SO SMART - v002.docx
  name: Velo-CE - Procedura di rilascio condivisa - SO SMART - v002.docx
  last_modified: 2026-09-23T11:40:40Z
versions:
  - { name: Velo-CE - Procedura di rilascio condivisa - SO SMART - v002.docx, item_id: 01EFCYUZ22YPHBOGH7V5GYEDKYAUC7Y2RH, last_modified: 2026-09-23T11:40:40Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:31:42Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, business-central, rilasci, so-smart, procedura, bozza]
---

# Velo-CE · Procedura di rilascio condivisa con So Smart

## Riassunto

Bozza da discutere (v002, intestata 29/09/2026, 2 pagine) indirizzata a So Smart, partner Microsoft/ERP di Velo-CE: propone come portare in produzione le modifiche che BlueAge fa su Business Central nel riordino di processi e dati, proteggendo l'operatività di Velo-CE e lasciando a So Smart la possibilità di continuare l'assistenza sulle proprie app. Definisce sei principi, quattro tipi di rilascio, il preavviso reciproco per i tipi 3 e 4, i sette passi della finestra, il dopo-rilascio e i referenti. I valori fra parentesi quadre sono proposte da concordare. È la versione esterna della procedura interna, operativa nella [[velo-ce-checklist-finestra-di-rilascio-interno]].

## Punti chiave

- **Principi**: standard prima del custom (BlueAge non modifica il codice delle app So Smart; codice e API restano a So Smart, concordati con Velo-CE); sandbox prima, sempre; nessuna sorpresa; stato di partenza recuperabile (export dei dati toccati e registro modifiche); tutto tracciato in un registro dei rilasci condiviso; niente finestre a ridosso degli aggiornamenti di Microsoft o delle app So Smart.
- **Tipi di rilascio**: 1 visibilità e personalizzazione e 2 setup e parametri puntuali (registro a cadenza fissa, nessuna finestra); 3 modifiche massive sui dati (ricodifica, parametri su molti articoli, distinte, bonifiche) e 4 app, estensioni ed esperienza (installazioni, passaggio a Premium): preavviso scritto e finestra dedicata.
- **Preavviso**: nota informativa a So Smart, non richiesta di analisi; eventuali interventi di So Smart si concordano e si quotano con Velo-CE. So Smart avvisa a sua volta degli aggiornamenti delle proprie app.
- **Finestra**: avvio con nessun accesso a BC per nessuna utenza, assistenza compresa; sospensione degli automatismi e fermo delle integrazioni in ingresso (oppure ordini dichiarati «da verificare»); esecuzione della sequenza provata; verifiche; ricontrollo degli automatismi; esito (decide Velo-CE); riattivazione con la propria utenza. Comunicazioni via mail e reperibilità telefonica.
- **Dopo il rilascio**: assistenza dedicata BlueAge, nota di rilascio a So Smart e passaggio di consegne per l'assistenza ordinaria.
- **Referenti**: Velo-CE, Stefano Moruzzi (titolare, decide sugli esiti); BlueAge, Cristian (project manager, rilasci) e Leonardo Pinsone (analisi dei processi); So Smart, referente di progetto e reperibile da indicare.

## Numeri

- Preavviso proposto: [5] giorni lavorativi da BlueAge a So Smart e viceversa; risposta di So Smart entro [3] giorni lavorativi.
- Assistenza dedicata BlueAge dopo il rilascio: [2-4] settimane.
- 4 tipi di rilascio, 7 passi di finestra, 6 principi.

## Decisioni e azioni

- [ ] Concordare con So Smart termini di preavviso e di risposta
- [ ] Concordare l'elenco degli automatismi da sospendere e l'utenza con cui riattivarli
- [ ] Definire come fermare le integrazioni in ingresso (canale degli ordini di vendita)
- [ ] Concordare formato e cadenza del registro dei rilasci
- [ ] Chiarire come e con quale preavviso So Smart pianifica gli aggiornamenti delle proprie app

## Versioni

- Velo-CE - Procedura di rilascio condivisa - SO SMART - v002.docx · 2026-09-23 · prima versione ingerita; il testo è datato 29/09/2026, dopo la data di ultima modifica del file
