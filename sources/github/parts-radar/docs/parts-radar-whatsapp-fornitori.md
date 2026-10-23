---
type: source-doc
source: github
family: parts-radar-whatsapp-fornitori
current:
  item_id: "cristian-schifone/parts-radar:docs/whatsapp-fornitori.md"
  uri: "github://cristian-schifone/parts-radar/docs/whatsapp-fornitori.md@28674546e6b6aea0489bb23f984ea2805ec4e364"
  web_url: "https://github.com/cristian-schifone/parts-radar/blob/main/docs/whatsapp-fornitori.md"
  name: "docs/whatsapp-fornitori.md"
  last_modified: 2026-10-20T05:20:11Z
versions:
  - { name: "docs/whatsapp-fornitori.md@2867454", item_id: "cristian-schifone/parts-radar:docs/whatsapp-fornitori.md", last_modified: 2026-10-20T05:20:11Z }
also_at: []
status: active
partial: true
ingested_at: 2026-10-23T18:23:22Z
projects: ["[[parts-radar-sviluppo]]"]
clients: ["[[adac-bologna]]"]
topics: ["[[parts-radar]]"]
tags: []
---

# Fornitori WhatsApp: 360dialog, Uniwaba e Meta diretto (Twilio escluso)

## Riassunto

Analisi e prove dei fornitori del canale WhatsApp (16-20/10/2026). Il servizio ne supporta tre, uno per installazione: Meta diretto, Uniwaba, 360dialog. Il 19/10 Lorenzo ha scelto per il pilot 360dialog con la Coexistence, che lascia il numero di ADAC sull'app del telefono del banco; il 20/10 Twilio è stato escluso e il suo codice tolto. Letti §1-§3 e §5.

## Punti chiave

- Il nodo che decide è il numero: se il pilot gira sul numero di oggi di ADAC (meccanici e banco non cambiano nulla) serve la Coexistence, quindi 360dialog o Uniwaba; con un numero nuovo dedicato agli ordini basta Meta diretto
- Perché 360dialog: il ricambista non può perdere messaggi né un giorno di lavoro se il servizio è giù. Con la Coexistence il messaggio arriva comunque sul telefono del banco e Meta lo ripete al ritorno del servizio; con Twilio il numero lasciava l'app e il webhook non ritentava
- Twilio escluso il 20/10: niente Coexistence, nessun reinvio di default, dati solo negli USA
- Uniwaba: Coexistence sì, ma fornitore giovane (primo commit a febbraio 2026), senza SLA, webhook non firmato e nessuna API per le foto ricevute
- Vincoli della Coexistence: l'app va aperta almeno ogni 13 giorni o il collegamento si stacca; niente app desktop Windows; un numero attivato su un account non si sposta su un altro
- I gruppi WhatsApp restano fuori con tutti i fornitori: 3 clienti ADAC su 10 scrivono da un gruppo
- Domande aperte sul numero nuovo di ADAC: dove è registrato oggi, se i test passavano dal Test Number, se il banco deve rispondere dal telefono

## Numeri

- 360dialog: Regular 49 €/mese per numero; Partner da 250 €/mese con 5 canali; tariffe Meta senza ricarico (testo libero gratis dentro le 24 ore, template fuori finestra a pagamento)
- Sandbox 360dialog: gratuita, 200 messaggi, un solo destinatario, niente media né Coexistence
- Traffico stimato: circa 210 messaggi dei meccanici al giorno (circa 7 per officina, circa 30 officine al giorno)

## Decisioni e azioni

- 2026-10-19 · 360dialog con la Coexistence per il pilot, al posto di Twilio (Lorenzo); allineamento in sandbox a spesa zero, senza contattare 360dialog
- 2026-10-20 · Twilio escluso, codice tolto
- Da decidere prima di attivare il numero di ADAC: piano Regular o Partner (solo il Partner firma il webhook e include 5 canali)
- Contratto sui dati (DPA) con 360dialog da firmare: avviso per Cristian

## Versioni

- docs/whatsapp-fornitori.md@2867454 · 2026-10-20 · prima lettura nel vault (§1-§3, §5)
