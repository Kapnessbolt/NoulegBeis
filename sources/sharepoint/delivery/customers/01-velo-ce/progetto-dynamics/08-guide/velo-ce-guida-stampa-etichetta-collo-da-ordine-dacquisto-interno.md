---
type: source-doc
source: sharepoint
family: velo-ce-guida-stampa-etichetta-collo-da-ordine-dacquisto-interno
current:
  item_id: 01EFCYUZYNAPLSOF7VZJG32XESAVV66K6H
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZYNAPLSOF7VZJG32XESAVV66K6H
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/08 Guide/Velo-CE - Guida stampa etichetta collo da ordine d'acquisto - INTERNO - v001.pdf
  name: Velo-CE - Guida stampa etichetta collo da ordine d'acquisto - INTERNO - v001.pdf
  last_modified: 2026-10-28T08:06:13Z
versions:
  - { name: "Velo-CE - Guida stampa etichetta collo da ordine d'acquisto - INTERNO - v001.pdf", item_id: 01EFCYUZYNAPLSOF7VZJG32XESAVV66K6H, last_modified: 2026-10-28T08:06:13Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-29T06:12:29Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [guida, velo-ce, etichette, magazzino, acquisti, interno]
---

# Velo-CE · Guida: stampare l'etichetta collo dall'ordine d'acquisto (INTERNO)

## Riassunto

Guida operativa interna BlueAge (v001 dell'08/10/2026, 6 pagine, bozza da validare con [[velo-ce]]) per stampare un'etichetta collo A5 dall'ordine d'acquisto quando un collo arriva senza l'etichetta del fornitore. Usa il report standard dell'ordine d'acquisto con un layout Word di Velo-CE, senza app esterne, licenza Essentials. Provata in una società dimostrativa BlueAge.

## Punti chiave

- Il layout «VELO-CE COLLO DA ODA» si carica una volta e non va mai impostato come predefinito, perché lo stesso report invia l'ordine al fornitore; si sceglie a mano nella finestra di stampa, spegnendo la registrazione dell'interazione.
- Esce un'etichetta per riga d'ordine con codice articolo Velo-CE in grande e in codice a barre, descrizione, codice del fornitore, consegna prevista, numero d'ordine in codice a barre, fornitore e quantità ordinata; intestazioni in inglese come nel capitolato chiesto ai fornitori.
- A penna si scrivono quantità nel collo, numero del DDT, collo «n di m» e peso netto: lo standard non stampa per collo, né la quantità ricevuta, né il DDT; il codice a barre è Code 39, il Code 128 richiede un'estensione.
- Il DDT si scrive anche sull'ordine prima di registrare il carico; stampare l'etichetta dal carico registrato è un passo successivo da valutare (open point).
- Da rilevare quale layout d'ordine è in uso oggi prima di caricarlo nel nuovo ambiente.

## Numeri

- Prova: ordine di 8 righe, 8 etichette A5.

## Decisioni e azioni

- Nessuna decisione formale.

## Versioni

- Velo-CE - Guida stampa etichetta collo da ordine d'acquisto - INTERNO - v001.pdf · 2026-10-28 · prima versione ingerita; cartella `Cristian/08 Guide/`
