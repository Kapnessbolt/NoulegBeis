---
type: source-doc
source: sharepoint
family: velo-ce-guida-assemblaggio-su-ordine-dallordine-di-vendita-cliente
current:
  item_id: 01EFCYUZZZ7VF6ECJ2F5G2GTICID4UGJWQ
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZZZ7VF6ECJ2F5G2GTICID4UGJWQ
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/08 Guide/Velo-CE - Guida assemblaggio su ordine dall'ordine di vendita - CLIENTE - v001.pdf
  name: Velo-CE - Guida assemblaggio su ordine dall'ordine di vendita - CLIENTE - v001.pdf
  last_modified: 2026-10-28T08:06:10Z
versions:
  - { name: "Velo-CE - Guida assemblaggio su ordine dall'ordine di vendita - CLIENTE - v001.pdf", item_id: 01EFCYUZZCCUT5CRT3Z5DKHULR42QRZWB7, last_modified: 2026-10-28T08:06:10Z }
also_at:
  - { web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/08 Guide/Velo-CE - Guida assemblaggio su ordine dall'ordine di vendita - CLIENTE - v001.docx", item_id: 01EFCYUZ3TX4DT3OWWPBH3JHVCGBUYPCOK }
status: active
partial: false
ingested_at: 2026-10-29T06:10:47Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [guida, velo-ce, assemblaggio, business-central, cliente]
---

# Velo-CE · Guida: assemblaggio su ordine dall'ordine di vendita (CLIENTE)

## Riassunto

Guida operativa BlueAge per [[velo-ce]] (v001, 7 pagine, prova del 20/10/2026 in un ambiente dimostrativo) su come una riga dell'ordine di vendita genera da sola l'ordine di assemblaggio della bici e come lo si porta fino alla spedizione. Esempio: 10 bici Multi Lungo con telaio e forcella in RAL 1004. Disponibile anche in Word.

## Punti chiave

- Per le bici impostate con assemblaggio su ordine (campo sulla scheda articolo) la riga di vendita crea l'ordine di assemblaggio collegato, senza passaggi a mano; le bici a magazzino e i componenti non generano nulla.
- L'ordine di assemblaggio elenca i componenti della distinta con le quantità moltiplicate; il colore di telaio e forcella va scelto riga per riga (il colore della vendita non passa da solo ai componenti).
- Ordine di vendita e ordine di assemblaggio si rilasciano insieme: per correggere i componenti bisogna riaprire.
- La disponibilità dice quante bici si possono assemblare; i componenti mancanti si coprono con acquisti o ordini di produzione anche in conto lavoro.
- Una sola registrazione (spedizione dell'ordine di vendita) registra assemblaggio, consumo dei componenti, carico della bici e spedizione; i movimenti si controllano nei movimenti contabili articoli.

## Numeri

- Date: la scadenza dell'assemblaggio è la data di spedizione, inizio e fine un giorno prima.
- Esempio: 59 righe di movimento per l'assemblaggio di 10 bici.

## Decisioni e azioni

- Il colore dei componenti verniciati resta un punto da decidere nell'impostazione di codici e configurazioni.

## Versioni

- Velo-CE - Guida assemblaggio su ordine dall'ordine di vendita - CLIENTE - v001.pdf · 2026-10-28 · prima versione ingerita; cartella `Cristian/08 Guide/`; anche in .docx
