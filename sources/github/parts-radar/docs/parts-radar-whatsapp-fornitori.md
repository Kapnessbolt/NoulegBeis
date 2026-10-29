---
type: source-doc
source: github
family: parts-radar-whatsapp-fornitori
current:
  item_id: "cristian-schifone/parts-radar:docs/whatsapp-fornitori.md"
  uri: "github://cristian-schifone/parts-radar/docs/whatsapp-fornitori.md@733d0a69b3c6797d3453eae26042555fadb04f2f"
  web_url: "https://github.com/cristian-schifone/parts-radar/blob/main/docs/whatsapp-fornitori.md"
  name: "docs/whatsapp-fornitori.md"
  last_modified: 2026-10-28T23:22:29Z
versions:
  - { name: docs/whatsapp-fornitori.md@733d0a6, item_id: cristian-schifone/parts-radar:docs/whatsapp-fornitori.md, last_modified: 2026-10-28T23:22:29Z }
  - { name: docs/whatsapp-fornitori.md@2867454, item_id: cristian-schifone/parts-radar:docs/whatsapp-fornitori.md, last_modified: 2026-10-20T05:20:11Z }
also_at: []
status: active
partial: true
ingested_at: 2026-10-29T06:23:58Z
projects: ["[[parts-radar-sviluppo]]"]
clients: ["[[adac-bologna]]"]
topics: ["[[parts-radar]]"]
tags: []
---

# Fornitori WhatsApp: 360dialog, Uniwaba e Meta diretto (Twilio escluso)

## Riassunto

Analisi e prove dei fornitori del canale WhatsApp (16-20/10/2026). Il servizio ne supporta tre, uno per installazione: Meta diretto, Uniwaba, 360dialog. Il 19/10 Lorenzo ha scelto per il pilot 360dialog con la Coexistence, che lascia il numero di ADAC sull'app del telefono del banco; il 20/10 Twilio è stato escluso e il suo codice tolto. Il 29/10 il piano: Regular a nome di ADAC, coi vincoli che compensano il webhook senza firma. Letti §1-§3 e §5.

## Punti chiave

- Il nodo che decide è il numero: se il pilot gira sul numero di oggi di ADAC (meccanici e banco non cambiano nulla) serve la Coexistence, quindi 360dialog o Uniwaba; con un numero nuovo dedicato agli ordini basta Meta diretto
- Perché 360dialog: il ricambista non può perdere messaggi né un giorno di lavoro se il servizio è giù. Con la Coexistence il messaggio arriva comunque sul telefono del banco e Meta lo ripete al ritorno del servizio; con Twilio il numero lasciava l'app e il webhook non ritentava
- Twilio escluso il 20/10: niente Coexistence, nessun reinvio di default, dati solo negli USA
- Uniwaba: Coexistence sì, ma fornitore giovane (primo commit a febbraio 2026), senza SLA, webhook non firmato e nessuna API per le foto ricevute
- Vincoli della Coexistence: l'app va aperta almeno ogni 13 giorni o il collegamento si stacca; niente app desktop Windows; un numero attivato su un account non si sposta su un altro
- I gruppi WhatsApp restano fuori con tutti i fornitori: 3 clienti ADAC su 10 scrivono da un gruppo
- Regular a nome di ADAC (29/10): ADAC ha co-sviluppato il sistema e il numero, l'account e il traffico sono suoi. È titolare del trattamento, 360dialog il suo fornitore, BlueAge il responsabile, che riceve solo la chiave dell'API. Il Partner di BlueAge si apre dal secondo o terzo cliente; ADAC non migra (rifarebbe da zero l'onboarding della Coexistence)
- Sul piano legale bastano tre cose: la nomina a responsabile da ADAC a BlueAge (art. 28 GDPR) coi sub-responsabili (Anthropic, Soniox e Google, il fornitore del server del pilot), che prende il posto del consenso scritto; la registrazione di ADAC su 360dialog, senza nulla da firmare per BlueAge; l'informativa di ADAC alle officine, senza consenso da chiedere ai meccanici
- Webhook senza firma sul Regular: rischio accettato con otto vincoli verificati prima dell'attivazione (cifratura che termina solo sul proxy del server, niente tunnel; segreto fuori dai log, nato sul server e ruotato; chiave dell'API con le stesse regole; solo gli IP di 360dialog se fissi; tetto alle chiamate; controlli del servizio accesi; allarme sui rifiuti). Resta scoperto solo chi ha accesso al server, come col Partner
- Domande aperte sul numero nuovo di ADAC: dove è registrato oggi, se i test passavano dal Test Number, se il banco deve rispondere dal telefono

## Numeri

- 360dialog: Regular 49 €/mese per numero (scelto per ADAC, contro 250 del Partner finché il cliente è uno); Partner da 250 €/mese con 5 canali; tariffe Meta senza ricarico (testo libero gratis dentro le 24 ore, template fuori finestra a pagamento)
- Sandbox 360dialog: gratuita, 200 messaggi, un solo destinatario, niente media né Coexistence
- Traffico stimato: circa 210 messaggi dei meccanici al giorno (circa 7 per officina, circa 30 officine al giorno)

## Decisioni e azioni

- 2026-10-19 · 360dialog con la Coexistence per il pilot, al posto di Twilio (Lorenzo); allineamento in sandbox a spesa zero, senza contattare 360dialog
- 2026-10-20 · Twilio escluso, codice tolto
- 2026-10-29 · Regular a nome di ADAC, Partner dal secondo cliente, ADAC non migra (Lorenzo)
- Prima dell'attivazione: i vincoli V1-V8 del webhook (V1, V2, V5, V6 su server e proxy a Cristian; domanda a 360dialog sugli IP fissi, segreto nuovo e controlli del servizio a Lorenzo; l'allarme sui rifiuti va col canale degli allarmi)
- ADAC si registra su 360dialog e passa la chiave; l'avviso a Cristian sul DPA di 360dialog decade
- Una domanda sola a 360dialog (IP di uscita fissi): rivede il «nessun contatto» del 19/10

## Versioni

- docs/whatsapp-fornitori.md@733d0a6 · 2026-10-29 · §1-§3 e §5: deciso il Regular a nome di ADAC, tre adempimenti legali, nuova §3.1 coi vincoli V1-V8 del webhook senza firma
- docs/whatsapp-fornitori.md@2867454 · 2026-10-20 · prima lettura nel vault (§1-§3, §5)
