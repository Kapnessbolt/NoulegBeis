---
type: source-doc
source: sharepoint
family: velo-ce-verbale-integrazioni-we-make-code
current:
  item_id: 01EFCYUZYZGPERU3YQX5HKGLQVPCBVMX5D
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZYZGPERU3YQX5HKGLQVPCBVMX5D
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/99 Project Claude (copia)/verbali/velo-ce-verbale-261022-1530-integrazioni-we-make-code.md
  name: velo-ce-verbale-261022-1530-integrazioni-we-make-code.md
  last_modified: 2026-10-29T16:15:51Z
versions:
  - { name: velo-ce-verbale-261022-1530-integrazioni-we-make-code.md, item_id: 01EFCYUZYZGPERU3YQX5HKGLQVPCBVMX5D, last_modified: 2026-10-29T16:15:51Z }
  - { name: velo-ce-verbale-261022-1530-integrazioni-we-make-code.md, item_id: 01EFCYUZYMTBRLHGQIQ5DIM6KFFXCVBVYR, last_modified: 2026-10-28T08:06:45Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-29T06:05:26Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [verbale, velo-ce, integrazioni, b2b, we-make-code, varianti, tracciabilita]
---

# Velo-CE · Verbale: call con We Make Code sulle integrazioni (portali B2B, Veloce-CRM, assemblaggio)

## Riassunto

Prima call del 22/10/2026 dalle 15:30 fra BlueAge (Cristian conduce, Leo) e Nicolò, sviluppatore di We Make Code, fornitore dei portali di [[velo-ce]]; assente Leonardo Marchesini di We Make Code (il «Leonardo di Venezia» dei verbali precedenti). Contenuti di We Make Code dichiarati, quelli di BlueAge proposte. Obiettivo: capire i flussi verso BC per valutare l'impatto della ricodifica e il configuratore rispetto alle varianti sull'ordine di assemblaggio. Chiude con nove punti cruciali per la struttura di BC, valutati da Claude e da discutere fra Cristian e Leo.

## Punti chiave

- **Integrazioni attive**: quattro, tutte di We Make Code: clienti, Veloce-CRM (sul server in azienda), B2B Veloe e B2B Van Nicholas; prodotti letti con l'API standard Microsoft, ordini di vendita e modifiche dell'ordine di assemblaggio con chiamate custom di So Smart.
- **Configuratore**: compone oggi il codice della bici concatenando i codici dei componenti scelti; con un codice a progressivo serve una tabella configurazione → codice tenuta allineata fra BC e portale.
- **Van Nicholas**: ordine di assemblaggio creato in automatico sul modello standard e corretto dal B2B togliendo e aggiungendo righe, solo per ordini con una bici. **Veloe**: nessun ordine di assemblaggio, le variazioni sono righe di vendita in più: con l'assemblaggio su ordine del nuovo BC questo darebbe giacenze sbagliate.
- **Prodotti e prezzi**: il B2B importa tutti gli articoli e la visibilità si imposta a mano; articoli CNF per le configurazioni (es. CNF-RAL per il custom); il prezzo viene dalla scheda articolo, non dal portale: con i listini per colore la lettura va cambiata.
- **Ordini con più bici**: frequenti, oggi bici con quantità 2 e accessori sotto per posizione; BlueAge chiede ordini di assemblaggio distinti per bici, cioè una riga per bici con quantità 1, per la tracciabilità.
- **Tracciabilità**: oggi frame number, lucchetto e batteria in Veloce-CRM; domani BC diventa master e restituisce i dati, Veloce-CRM resta; il verso dei dati si inverte ed è sviluppo di We Make Code.
- **Nuovo ambiente**: le API non cambiano fra Essentials e Premium, ma il passaggio al tenant nuovo cambia indirizzi, ID, app e credenziali; le chiamate custom esistono solo se So Smart installa le sue app nel nuovo ambiente.

## Numeri

- Nessun numero rilevante.

## Decisioni e azioni

- Concordati: Excel vecchi → nuovi codici a We Make Code fra circa due settimane, mail di riepilogo con Stefano in copia, nuova call dopo l'Excel.
- [ ] Inviare a We Make Code l'Excel di corrispondenza vecchi → nuovi codici e la regola del codice bici ([[velo-ce-verbale-integrazioni-we-make-code]])

## Versioni

- velo-ce-verbale-261022-1530-integrazioni-we-make-code.md · 2026-10-28 · prima versione ingerita; cartella `Cristian/99 Project Claude (copia)/verbali/`
