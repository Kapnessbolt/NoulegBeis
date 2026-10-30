---
type: source-doc
source: github
family: parts-radar-issue-379
current:
  item_id: "cristian-schifone/parts-radar#379"
  uri: "github://cristian-schifone/parts-radar/issues/379"
  web_url: "https://github.com/cristian-schifone/parts-radar/issues/379"
  name: "Issue #379 · Pilot ADAC: ordine dei lavori verso il test reale (rifatto il 21/10, rivisto il 28/10)"
  last_modified: 2026-10-29T11:47:04Z
versions:
  - { name: "Issue #379", item_id: cristian-schifone/parts-radar#379, last_modified: 2026-10-29T11:47:04Z }
  - { name: "Issue #379", item_id: cristian-schifone/parts-radar#379, last_modified: 2026-10-28T23:18:54Z }
  - { name: "Issue #379", item_id: cristian-schifone/parts-radar#379, last_modified: 2026-10-27T17:13:27Z }
  - { name: "Issue #379", item_id: cristian-schifone/parts-radar#379, last_modified: 2026-10-26T08:49:21Z }
  - { name: "Issue #379", item_id: cristian-schifone/parts-radar#379, last_modified: 2026-10-25T23:26:55Z }
  - { name: "Issue #379", item_id: cristian-schifone/parts-radar#379, last_modified: 2026-10-22T13:55:33Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-30T06:30:05Z
projects: ["[[parts-radar-sviluppo]]"]
clients: ["[[adac-bologna]]", "[[solera]]"]
topics: ["[[parts-radar]]"]
tags: []
---

# Pilot ADAC: ordine dei lavori verso il test reale

## Riassunto

Issue di pianificazione della milestone "Pilot ADAC", rifatta il 21/10/2026 con Lorenzo, rivista il 27/10 e due volte il 28/10 (l'ordine in vigore è la revisione del 28/10 sera). Fissa il traguardo (il test reale della #420, prima della scadenza della demo Kromeda intorno al 18/11) e un piano in quattro settimane, più i passi fuori dal codice di Lorenzo e di [[cristian-schifone]]. Al 28/10 sera del codice della settimana 2 resta solo la voce: il percorso critico non è più il codice ma l'attivazione del numero di ADAC, che dipende dai passi fuori dal codice.

## Punti chiave

- Test in due tempi: prima una prova controllata (il team fa da meccanico, 3-4 targhe), poi il traffico vero di ADAC con le targhe che restano; in mezzo l'ascolto sul numero di ADAC in Coexistence
- Chiarimenti automatici dell'AI al meccanico accesi nella prova controllata, spenti sul traffico vero finché il router non ha numeri; dopo la demo i test continuano sulle chiamate registrate
- Fuori dal percorso del pilot, nella milestone "Prima della produzione": brand e collasso articoli, CI, veicolo sbagliato, dataset completo, messaggi oltre le 24 ore e, dal 28/10, due migliorie del percorso per codice
- Revisione del 28/10 mattina, dopo la prova a secco: cinque issue nuove; prima dell'attivazione il codice del meccanico per codice, il lessico e le varianti della voce, la misura dei vocali; nella stessa finestra dal vivo di Kromeda (utenza libera, un solo avviso a Cristian) la sonda dei modelli e il giro degli alberi
- Col credito API personale di Lorenzo (100 $ al mese dal 28/10, con l'accordo di ADAC sui dati veri): benchmark del router su 810 gruppi con Haiku, Sonnet e Opus (~50 $) ed estrazione e voce con Sonnet e Opus (~50 $), anticipando la parte costosa del confronto finale dei modelli
- Revisione del 28/10 sera: tredici voci chiuse; regole congelate di slittamento: numero non attivo entro circa l'11/11 → la prova controllata va in settimana 4; non attivo entro circa il 16/11 → niente test con le targhe prima della fine della demo
- Codice dei prossimi sette giorni (29/10-04/11), tutto senza il numero: la voce (ultimo anello senza misura), la nota per il banco, il benchmark del router; il giro degli alberi è chiuso il 29/10, restano la sonda dei modelli (6 chiamate, 0 crediti targa, con l'utenza libera da Cristian) e i codici delle voci frequenti, dopo la voce; se l'attivazione slitta oltre il 4/11 si anticipano le PR di sola estrazione, foto e modelli
- Settimana 3 alleggerita; valvola nell'ordine: seconda parte dell'estrazione strutturata, poi il pezzo senza etichetta in foto

## Numeri

- 17 crediti targa al 21/10
- Al 28/10 mancano 7 giorni al 04/11 e 14 all'11/11; traffico vero nella settimana 12-17/11; demo Kromeda fino a circa il 18/11
- Giro dal vivo degli alberi: 900 chiamate il 28/10 (221 coppie modello/anno su 268) e 767 il 29/10: alberi completi, 268 coppie su 268, crediti targa invariati (la stima di circa 1.400 era larga)

## Decisioni e azioni

Fuori dal codice, in ordine di urgenza (revisione del 28/10 sera, aggiornata al 29/10):
- 360dialog: deciso il 29/10, Regular a nome di ADAC (Partner dal secondo cliente, ADAC non migra). Ora ADAC si registra e passa la chiave
- Vincoli del webhook senza firma (#531), prima dell'attivazione: server e proxy a Cristian; domanda a 360dialog sugli IP fissi, segreto nuovo e controlli del servizio a Lorenzo; l'allarme sui rifiuti va col canale degli allarmi
- Nomina a responsabile da ADAC a BlueAge (art. 28) coi sub-responsabili (LLM, Soniox e Google, server del pilot): prende il posto del consenso scritto; l'informativa alle officine la fa ADAC
- Cristian: server del pilot raggiungibile dal webhook e rete del webhook (D46), canale degli allarmi (D4), staging allineato
- Le auto T1-T4 e i telefoni M1-M3 della prova controllata, col file fuori da git
- Progetti Soniox UE e Google a nome di BlueAge, poi l'accensione dei vocali
- Numeri delle officine come clienti attivi, all'attivazione; foto delle officine da ADAC (raccolte nel dataset: 56 di sviluppo, 23 di test)
- Kromeda di produzione: BlueAge sul piano commerciale, coi risultati della #420; brand preferiti di ADAC in attesa
- Da chiudere nei documenti (Lorenzo): mappatura dei brand (per il pilot basta l'ordine di fascia?), targhe provinciali (proposta «dritte al banco»); il cancello dei vocali resta caduto (da ascoltare al 27,1% contro il 25%), le targhe dai vocali vanno al banco nel traffico vero

## Versioni

- Issue #379 · 2026-10-29 · giro degli alberi chiuso il 29/10 (268 coppie su 268, 767 chiamate, crediti invariati); restano la sonda dei modelli e i codici delle voci frequenti dopo la voce
- Issue #379 · 2026-10-28 · due revisioni del 28/10 (dopo la prova a secco e la sera): tredici voci chiuse, percorso critico sui passi fuori dal codice, regole di slittamento (~11/11, ~16/11), benchmark col credito personale; 360dialog spuntato (Regular a nome di ADAC, 29/10), nomina a responsabile al posto del consenso, vincoli del webhook (#531)
- Issue #379 · 2026-10-27 · revisione del 27/10: piano della #420 in testa alla settimana 2, allarme Coexistence dopo l'attivazione, settimana 1 chiusa salvo la voce; nuovi passi fuori dal codice (trascrizione a nome di BlueAge, canale degli allarmi), avviso a Cristian spuntato
- Issue #379 · 2026-10-26 · settimana 1: etichettatore Opus tarato per le etichette del test; passi fuori dal codice invariati
- Issue #379 · 2026-10-25 · avanzamento della settimana 1: etichette di sviluppo fatte e riviste, prompt congelati; passi fuori dal codice invariati
- Issue #379 · 2026-10-22 · prima lettura nel vault
