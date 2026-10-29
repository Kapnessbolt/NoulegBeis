---
type: source-doc
source: sharepoint
family: velo-ce-guida-punto-di-riordino-e-proposte-del-piano-cliente
current:
  item_id: 01EFCYUZ66IVYPERNJSNB3EHSTQJEM56YS
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ66IVYPERNJSNB3EHSTQJEM56YS
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/08 Guide/Velo-CE - Guida punto di riordino e proposte del piano - CLIENTE - v001.pdf
  name: Velo-CE - Guida punto di riordino e proposte del piano - CLIENTE - v001.pdf
  last_modified: 2026-10-28T08:06:13Z
versions:
  - { name: "Velo-CE - Guida punto di riordino e proposte del piano - CLIENTE - v001.pdf", item_id: 01EFCYUZ66IVYPERNJSNB3EHSTQJEM56YS, last_modified: 2026-10-28T08:06:13Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-29T06:11:15Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [guida, velo-ce, pianificazione, mrp, scorte, cliente]
---

# Velo-CE · Guida: punto di riordino e proposte del piano (CLIENTE)

## Riassunto

Guida operativa BlueAge per [[velo-ce]] (v001, 9 pagine, 18/10/2026, società di prova Velo-CE S.r.l. - PROVA), preparata per Stefano: dove si impostano le scorte, come Business Central propone gli ordini con il prospetto di pianificazione e dove si trovano gli ordini creati. Esempio: telaio Lungo verniciato RAL 6011 e il telaio sabbiato che lo alimenta.

## Punti chiave

- Punto di riordino e quantità di riordino si impostano per articolo e, per i telai verniciati, per colore sull'unità di stockkeeping (articolo, colore, magazzino).
- Il piano guarda la disponibilità prevista (giacenza più ordini in arrivo meno impegni), non solo la giacenza di oggi; il report degli articoli sotto il punto di riordino elenca solo chi è già sotto.
- Il calcolo rigenerativo ricalcola tutte le proposte da zero senza toccare gli ordini già creati; la tracciabilità dell'ordine spiega perché nasce una proposta.
- Con l'esecuzione dei messaggi d'azione le proposte scelte diventano ordini veri: produzione confermati (consigliato), trasferimenti verso il magazzino del terzista, acquisti; il rilascio dell'ordine di produzione è il passo successivo.
- Il report Power BI di demo mostra per colore giacenza, punto, quantità di riordino e proposte dell'ultimo calcolo.

## Numeri

- Esempio: telaio RAL 6011 con punto di riordino 2 e quantità 4, giacenza 0: il piano propone 4 pezzi.

## Decisioni e azioni

- Nessuna decisione formale.

## Versioni

- Velo-CE - Guida punto di riordino e proposte del piano - CLIENTE - v001.pdf · 2026-10-28 · prima versione ingerita; cartella `Cristian/08 Guide/`
