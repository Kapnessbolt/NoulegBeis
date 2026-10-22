---
type: source-doc
source: sharepoint
family: velo-ce-app-eos-quali-servono-so-smart
current:
  item_id: 01EFCYUZZ6PNEMXCXRLRALRAWY7XAXV23T
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZZ6PNEMXCXRLRALRAWY7XAXV23T
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/04 Partner e ambienti/So Smart/Velo-CE - App EOS, quali servono - SO SMART - v002.pdf
  name: "Velo-CE - App EOS, quali servono - SO SMART - v002.pdf"
  last_modified: 2026-09-29T18:02:46Z
versions:
  - { name: "Velo-CE - App EOS, quali servono - SO SMART - v002.pdf", item_id: 01EFCYUZZ6PNEMXCXRLRALRAWY7XAXV23T, last_modified: 2026-09-29T18:02:46Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:31:42Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, business-central, eos, so-smart, app, premium]
---

# Velo-CE · Le app EOS: quali servono (documento per So Smart)

## Riassunto

Documento BlueAge per So Smart (versione 2, 5 pagine) preparato per la call del 30 settembre 2026. Velo-CE riordina processi e dati in Business Central con direzione Premium e, prima del cambio di esperienza e dei rilasci su articoli, distinte e costi, vuole tenere nel tenant solo le app con un ruolo. Presenta le 54 app EOS in Production una per una, con dati nel tenant, funzione secondo la documentazione EOS, funzione standard da confrontare e dipendenze, e chiede a So Smart per ognuna tre risposte: cosa fa in Velo-CE, perché al posto dello standard, cosa lo standard non copre. Le app sono divise in quattro gruppi: senza ruolo (da disinstallare), da chiarire, in uso, componenti e dipendenze.

## Punti chiave

- **Regola proposta**: si tengono le app usate ogni giorno, quelle che servono a un obbligo fiscale (anche se lavorano a scadenza) e quelle richieste da un'app che resta; le altre si disinstallano prima in una copia dell'ambiente, poi in Production. L'elenco finale lo approva Velo-CE.
- **Gruppo A (16 app senza ruolo, da disinstallare)**: fra le altre Product Configurator, Custom Defined Fields, MDI Master Data Intercompany (una sola società), estratti conto, file bancari, Open Banking (supporta solo Premium, installata su un tenant Essentials), Advanced Cash Flow (richiede un'app non installata), compensazioni, packing list, eliminazioni intercompany, cambi BCE, fatture a importo zero.
- **Gruppo B (11 app da chiarire)**: provvigioni e Enasarco (tenere se ci sono agenti), strumento di modifica dei dati registrati, Certificazioni Uniche e LIPE (obblighi fiscali: chi li usa?), fatturazione cumulativa estesa, omaggi, registro di magazzino.
- **Gruppo C (7 app in uso, si tengono)**: So Smart Application (import ordini MMI, job, «C\Lavoro» e Connettore WMS da disattivare), So Smart System, fattura elettronica, Advanced Document Reporting, IVA italiana, Accruals, Inventory Valuation and Costing (proposta: passare alla valutazione fiscale standard dopo la chiusura del 2026).
- **Gruppo D (20 componenti)**: base EOS (richiesta da tutte), librerie e agganci, So Smart for Italy (offerta per micro-PMI con configurazioni predefinite).
- **Tre temi trasversali**: comportamento del pacchetto So Smart dopo il cambio a Premium (il listino So Smart indica «Business Central Essentials inclusa»); scenari IVC usati oggi e chi li legge; possibilità di disattivare Connettore WMS e «C\Lavoro».
- **Come si procede**: risposte scritte riga per riga, prima i gruppi A e B; disinstallazione in copia con export dei dati, poi in Production in una finestra concordata.

## Numeri

- 54 app EOS su 124 installate, 70 Microsoft; tutte Global; 5.254 oggetti.
- 7 app al lavoro dal 24 al 29/09; gruppi A 16, B 11, C 7, D 20.
- Attività 24-29/09: 232 movimenti di ordini in ingresso, 261 movimenti di distribuzione e 90 messaggi So Smart, 24 fatture in entrata e 20 in uscita, 21 richieste di documenti, 3 movimenti di plafond, 341 movimenti «documenti da fatturare».

## Decisioni e azioni

- [ ] So Smart risponde per iscritto app per app, prima i gruppi A e B
- [ ] Preparare con So Smart l'elenco finale delle app da tenere e farlo approvare a Velo-CE
- [ ] Disinstallare prima in una copia dell'ambiente, con export dei dati, poi in Production in finestra concordata

## Versioni

- Velo-CE - App EOS, quali servono - SO SMART - v002.pdf · 2026-09-29 · prima versione ingerita
