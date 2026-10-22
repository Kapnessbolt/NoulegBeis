---
type: source-doc
source: sharepoint
family: velo-ce-articoli
current:
  item_id: 01EFCYUZ6O66YXIZU6CRA2A2RBXCCOSY2X
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ6O66YXIZU6CRA2A2RBXCCOSY2X
  web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/02 Configurazione/Anagrafica e codifica/Articoli version 1.xlsx"
  name: "Articoli version 1.xlsx"
  last_modified: 2026-09-23T15:30:06Z
versions:
  - { name: "Articoli version 1.xlsx", item_id: 01EFCYUZ6O66YXIZU6CRA2A2RBXCCOSY2X, last_modified: 2026-09-23T15:30:06Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:28:59Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [anagrafica, articoli, codifica, business-central, estrazione]
---

# Velo-CE · Estrazione dell'anagrafica articoli da Business Central (version 1)

## Riassunto

Estrazione in Excel dell'elenco articoli della società Velo-CE in Business Central: un solo foglio con 1.112 articoli e 16 colonne (codice, descrizione, giacenza, saldo, unità di misura, quantità in ordini di vendita e d'acquisto, costo unitario, costo medio, prezzo, flag distinta di assemblaggio, fornitore, quantità acquistate e vendute, CDC, reparto). È la base dati dell'analisi di codifica e del pilota Lungo: la nota tecnica del 23/09 la cita come fonte per riusare i codici esistenti quando il match è affidabile ([[velo-ce-pilota-lungo-bici-completa-nota-tecnica-leo]]). Il file è un'estrazione grezza, senza commenti né analisi: i conteggi sotto sono calcolati in ingestion sui dati del foglio.

## Punti chiave

- **Modello di codifica di fatto (per prefisso, regola di lavoro non anagrafica)**: codici numerici a 8 cifre ex Accell (Van Nicholas); famiglia Van Nicholas con prefissi `VN`, `NF…`, `MV…`, `HKIT`, `V26…`, `B-G-`; Bosch `BEB…`; Veloe con `VE-` + sottofamiglia (`VE-TL` telaio, `VE-LU` Lungo, `VE-HU` mozzi, `VE-AC`, `VE-MT`, `VE-SPK` raggi, `VE-BRK` freni, `VE-CK` cockpit, `VE-GT` Gates, `VE-WH` ruote, `VE-TY`, `VE-LGT`, `VE-RIM`); bici Veloe come configurazioni `M…` (`MLCA`, `MLEP`, `MEP`, `MPIB`, `MPIC`, `MBCX`, `MHPP`…); opzioni di configurazione `CNF-…`; accessori in coppia `AC…` (vendita) e `AM…` (magazzino); codici sparsi `AP…`, `ART…`.
- I codici del telaio a disegno `VE-TL` (57) e `VE-LU` (27) sono le 84 parti su cui la ricodifica propone lo scenario ibrido ([[velo-ce-ricodifica-rename-o-nuovo-codice]]).
- Campi gestionali poco usati: CDC e Reparto vuoti su tutti gli articoli; unità di misura `PZ` su tutti tranne uno (`NR`); nessuna unità a metri o chili, che servirà per tubi e lamiere del telaio.
- Le bici Veloe (`M…`) sono in gran parte senza distinta e a costo zero; molti accessori `AC…` non hanno giacenza (non inventariati), gli `AM…` sì.
- Diversi codici ripetono lo stesso oggetto (coppie AC/AM, codici telaio Multi e Lungo, due codici per il portapacchi Lungo): materiale per la ricodifica.

## Numeri

- 1.112 articoli, 16 colonne; ultima modifica del file 23/09/2026.
- 669 articoli con costo unitario zero (lo stesso numero citato nel foglio di ricodifica).
- 140 articoli con distinta di assemblaggio; 744 senza fornitore; 418 con saldo positivo; 405 con prezzo di vendita; 5 senza descrizione.
- Per gruppo di prefisso: 292 numerici a 8 cifre (223 a costo zero), circa 243 Van Nicholas e Bosch (83 con distinta), 232 `VE-` (87 a costo zero, 22 con distinta), 149 configurazioni bici `M…` (141 a costo zero, 8 con distinta), 40 `AM…` (12 con distinta), 34 `AC…`, 122 altri.
- `BEB…` (Bosch): 54 codici; `CNF-…`: 32.

## Decisioni e azioni

- Nessuna decisione nel file: è una fonte dati per [[velo-ce-ricodifica-rename-o-nuovo-codice]] e per il modello dati del pilota ([[velo-ce-pilota-bc-lungo-bosch-modello-dati-5-fogli]]).

## Versioni

- Articoli version 1.xlsx · 2026-09-23 · prima versione ingerita (nome generico del file: famiglia prefissata con velo-ce)
