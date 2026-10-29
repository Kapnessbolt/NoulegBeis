---
type: source-doc
source: sharepoint
family: velo-ce-mappa-cantieri-dynamics
current:
  item_id: 01EFCYUZ4UNOICTXQBCJAILWMKOEIYEMH6
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ4UNOICTXQBCJAILWMKOEIYEMH6
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/00 Progetto/_fonti piano/Velo-CE - Mappa cantieri Dynamics.xlsx
  name: Velo-CE - Mappa cantieri Dynamics.xlsx
  last_modified: 2026-09-15T14:11:58Z
versions:
  - { name: Velo-CE - Mappa cantieri Dynamics.xlsx, item_id: 01EFCYUZ7R7D4RG2YY4FEJJDJY5HCZQUVO, last_modified: 2026-09-15T14:11:58Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:25:33Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [cantieri, piano, quotazione, decisioni, power-bi]
---

# Velo-CE · Mappa dei cantieri del Progetto Dynamics e Power BI

## Riassunto

Documento di lavoro BlueAge del 09/09/2026 che scompone il Progetto Dynamics e Power BI di Velo-CE (chiamata «Veloce» nel file) in 34 cantieri raggruppati in sei macroblocchi, dai prerequisiti tecnici alle estensioni. Per ogni cantiere indica obiettivo di business, percorso critico, impatto, prerequisiti, effort in giornate Analyst e Sviluppo con una quota di extra effort, owner, fascia temporale e rischio principale; il dettaglio sta in 147 macro attività. Contiene anche 19 decisioni che spettano al cliente con l'orientamento BlueAge, un calendario di massima e la quotazione per macroblocchi. È una delle fonti del nuovo piano di progetto (cartella `_fonti piano`), da mandare in superato quando il piano nuovo è pronto.

## Punti chiave

- **Obiettivo n.1**: avere sempre i materiali per produrre e sapere quanto costa ciò che si produce; i cantieri sul percorso critico sono C01-C11.
- **Macroblocchi**: 1 Prerequisiti tecnici (C01 ambiente, licenze, utenze; C02 integrazioni e fornitori) · 2 Fondamenta (C03 codifica, C04 anagrafiche, C05 distinte) · 3 Ripresa dati (C04.1, C05.1) · 4 Gestione materiali (C06 conto lavoro, C07 ciclo passivo, C08 valorizzazione, C09 magazzino, C10 riordino, C11 produzione) · 5 Vendite, spedizioni, contabilità (C12-C16) · 6 Estensioni (MRP, cicli e capacità, radiofrequenza, tracciabilità seriale, budget, agenti, fidi, estero e plafond, tesoreria e cespiti, controllo di gestione, marginalità, reportistica, conformità, post-vendita, qualità, governance del dato).
- **Situazione rilevata**: codici creati da una sola persona; circa 1.100 articoli; saldatura e carrozzeria senza ordini né distinte; conto lavoro di verniciatura gestito con Fatture in Cloud fuori da Dynamics; fattura fornitore mai collegata all'ordine; registrazione del costo di magazzino in contabilità disattivata; approvvigionamenti a vista; ordini quasi tutti via mail; piano dei conti del commercialista del 2023 senza riclassificato; Power BI attendibile solo sulle vendite; due utenze su quattro aperte su tutto.
- **Decisioni con orientamento BlueAge**: D12 Premium invece di Essentials (sottoscrizioni mensili, nessuna scadenza); D19 controllo amministrativo del tenant in casa; D01 ricodificare Veloe e riallineare Van Nicholas alla prossima generazione; D14 switch della codifica a una data con inventario; D15 caricamento dati eseguito da BlueAge; D03 materie prime a metro lineare; D04 tutte le aree fuori sistema a perimetro; D05 seconda persona abilitata a creare codici; D07 kit come assieme con distinta; D17 regola scritta ordine-entrata-fattura; D09 ordini dove c'è un cambio di stato da costificare; D13 spegnere Fatture in Cloud con il conto lavoro a sistema; D18 accendere la registrazione del costo di magazzino in C/G; D10 ordini B2C a sistema dopo le Fondamenta; D08 Veloce-CRM da decidere a valle dell'architettura; D11 solo i ricambi rientrano a sistema.
- **Decisioni prese**: D02 colore come variante, non come codice; D06 in parte: grezzo e verniciato codificati.
- **Calendario**: prerequisiti settembre-ottobre 2026; Fondamenta settembre-novembre; ripresa dati novembre 2026-gennaio 2027; gestione materiali gennaio-marzo 2027; vendite e contabilità aprile-giugno 2027; estensioni da settembre 2027. L'inventario di gennaio 2027 è la finestra naturale per passare alla nuova codifica e rietichettare.
- **Offerta**: si quotano solo i blocchi 1, 2 e 3; i successivi si quotano quando si aprono.

## Numeri

- 34 cantieri, 147 macro attività, 19 decisioni.
- Giornate per macroblocco (previste / con extra / quotazione a corpo): prerequisiti 15,5 / 19,4 / 10.000 euro; Fondamenta 73 / 81,4 / 47.000 euro; ripresa dati 59 / 76,7 / 41.000 euro; gestione materiali 90,5 / 106,2 / 57.500 euro; vendite e contabilità 64 / 75,7 / 41.000 euro; estensioni 106 / 120,2 / 65.500 euro.
- Avvio del programma (blocchi 1-3): 147,5 giornate previste, 177,5 con extra, quotazione a corpo 98.000 euro.
- Tariffe giornaliere: Analyst 650 euro, Sviluppo 500 euro; quotazione a corpo a metà fra previsto ed extra, arrotondata a 500 euro.
- Circa 1.100 articoli; nuovi codici stimati fra 430 e 600; distinte da costruire fra 150 e 250; un centinaio di fornitori, 40 di materiali, 20 esteri; 47 accessori a catalogo; B2C 50.000 euro l'anno di accessori; circa cento ordini al mese su Veloe; un cliente pesa il 95% di Van Nicholas.

## Decisioni e azioni

- Decisione presa: D02, colore come variante con logica univoca.
- Decisione presa in parte: D06, grezzo e verniciato con codice e giacenza.
- Le altre 17 decisioni sono aperte, quasi tutte con un orientamento BlueAge; D12 (Premium) risulta poi decisa il 23/09 secondo [[velo-ce-riorganizzazione-cartella-mappa-file]].

## Versioni

- Velo-CE - Mappa cantieri Dynamics.xlsx · 2026-09-15 · prima versione ingerita; documento del 09/09/2026 con aggiornamenti al 21/09 nel testo, nonostante la data di modifica del 15/09; nella vecchia cartella si chiamava «Veloce - Mappa cantieri Dynamics.xlsx»
