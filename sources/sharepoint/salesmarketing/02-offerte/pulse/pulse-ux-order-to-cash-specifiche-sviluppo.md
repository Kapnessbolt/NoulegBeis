---
type: source-doc
source: sharepoint
family: pulse-ux-order-to-cash-specifiche-sviluppo
current:
  item_id: 01EFCYUZ5JTWQN4X4VNZCJPEQ22SNLDPVD
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKVSDgPuvHRsSIc3xR8AKeVG/01EFCYUZ5JTWQN4X4VNZCJPEQ22SNLDPVD
  web_url: https://blueagesrl.sharepoint.com/sites/internal/SalesMarketing/02 - Offerte/Pulse/PULSE_UX_Order_to_Cash_Specifiche_Sviluppo_v1.docx
  name: PULSE_UX_Order_to_Cash_Specifiche_Sviluppo_v1.docx
  last_modified: 2013-12-23T23:15:00Z
versions:
  - { name: PULSE_UX_Order_to_Cash_Specifiche_Sviluppo_v1.docx, item_id: 01EFCYUZ5JTWQN4X4VNZCJPEQ22SNLDPVD, last_modified: 2013-12-23T23:15:00Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:03:10Z
projects: []
clients: []
topics: ["[[pulse]]"]
tags: [specifiche, ux, order-to-cash, sviluppo, demo, interno]
---

# Pulse · User Experience e Demo Order-to-Cash · Specifiche per lo sviluppo (v1.0)

## Riassunto

Specifica funzionale e di interfaccia interna (v1.0, 28 luglio 2026, non condivisibile integralmente con i clienti) per la prima release della UX di [[pulse]] sul processo Order-to-Cash e per la demo con snapshot del 27, 28 e 29 luglio 2026. È pensata come fonte di verità per il team di sviluppo BlueAge e per l'implementazione con Claude Code. Definisce due utenti (Customer Service Specialist e Order-to-Cash Process Owner), la riga azionabile come unità comune, sei punti di attrito, il modello dati logico, lo storyboard con valori e testi esatti delle mail, i confini tra i moduli Core, Boost e Act, requisiti e criteri di accettazione. In caso di conflitto prevale la strategia ([[pulse-strategia-icp-e-pricing]]), poi il metodo indicatori.

## Punti chiave

- **Perimetro**: dall'ordine cliente acquisito all'incasso (validazione, promessa, copertura, spedizione, consegna, fatturazione, incasso e contestazioni); escluse opportunità e offerte. Contesto demo: manifatturiera B2B con nomi neutri (Cliente Alfa, Beta…; ordini SO-1001…).
- **Due utenti**: lo Specialist riceve solo le righe su cui può agire, vede il percorso intero dell'ordine e in sola lettura gli attriti di altre funzioni; il Process Owner legge, diagnostica e coordina fuori da Pulse, senza riassegnare righe, modificare priorità o aprire workflow (scelta MVP).
- **Riga azionabile** con testata comune (snapshot, fase, punto di attrito, record, cliente, owner, valore, aging, azione, evidenza attesa, stato) e dati specifici per punto di attrito, niente griglia universale. Stessa base dati per la vista per punto di attrito e per ordine.
- **Sei punti di attrito**: ordine acquisito ma non processabile; promessa cliente a rischio; completezza dell'ordine a rischio; ordine pronto ma non spedito (owner Logistica); consegna completata ma fattura non emessa (Amministrazione); incasso bloccato da contestazione. OTIF è un sintetico read-only senza euro propri.
- **Valori sempre separati**: ancora salvabile (previsionale), già bloccato o perso (consuntivo), recuperato; mai sommati.
- **Snapshot giornalieri immutabili** e delta "cosa è cambiato da ieri" a livello globale e locale; chiusura solo da evidenza nei sistemi sorgente.
- **Moduli**: Core trova, seleziona, spiega e verifica; Boost prepara o svolge l'azione; Act registra l'azione distinta dall'esito. Non usare "Pulse AI" (si dice Pulse Boost); Pulse Drive fuori dalla prima release.
- **Lessico governato**: niente "dashboard", "alert", "task", "KPI", "risparmio totale".

## Numeri

- Specialist: 27 lug 286 ordini → 43 dispersioni → 14 azionabili → 5 priorità, €31.500 salvabili, €4.500 bloccati; 28 lug 291 → 48 → 17 → 6, €35.500 / €6.000; 29 lug 294 → 32 → 9 → 3, €18.000 / €0.
- Process Owner: 27 lug 1.240 ordini, 86 dispersioni, €110k salvabili, €22k bloccati, 3 situazioni; 28 lug 1.251, 94, €126k, €22k, 4; 29 lug 1.263, 61, €74k, €18k, 2.
- 28 lug: €26k riportati in flusso; 29 lug: €61k recuperati, €5k nuovi, riduzione netta €56k; 11 dei 15 ordini pronti non spediti partiti (esposizione da €54k a €17k).
- 18 requisiti funzionali (REQ-001…018) e criteri di accettazione per Specialist, Process Owner, dati e temporalità.

## Decisioni e azioni

- Decisioni da non riaprire in sviluppo: due utenti separati; processo dall'ordine all'incasso; sei punti di attrito; numero di priorità variabile sopra soglia (non fisso a cinque); visibilità end-to-end e azionabilità per owner; snapshot immutabile; Process Owner solo lettura e diagnosi; wording Core/Boost/Act; Prev, Cons e recuperato separati.
- Ordine di implementazione per slice: fixture e relazioni, snapshot, Specialist, Process Owner, moduli, test automatici dei criteri di accettazione.
- Demo prevista sugli snapshot del 27–29 luglio 2026.

## Versioni

- PULSE_UX_Order_to_Cash_Specifiche_Sviluppo_v1.docx · 2013-12-23 · prima versione ingerita (v1.0 del 28 luglio 2026). Attenzione: la data di modifica nei metadati di SharePoint (2013-12-23T23:15:00Z) è anomala e incoerente con la data del documento; riportata così com'è.
