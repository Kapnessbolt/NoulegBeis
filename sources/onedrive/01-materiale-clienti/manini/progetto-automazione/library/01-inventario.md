---
type: source-doc
source: onedrive
family: 01-inventario
current:
  item_id: 013UYHJHAE7SWYFK3OKFFL6BA62NSSG5W7
  uri: file:///b!2fHSoBOOE0aRvS_GntS6s6RJcyNKjAJMiRtoiZ6n5xzp8hWMRRoMQKOVYgftTbzT/013UYHJHAE7SWYFK3OKFFL6BA62NSSG5W7
  web_url: https://blueagesrl-my.sharepoint.com/personal/lorenzo_curione_blueage_it/Documents/BlueAge/01_Materiale clienti/Manini/Progetto Automazione/Library/01_inventario.md
  name: 01_inventario.md
  last_modified: 2026-10-23T11:33:34Z
versions:
  - { name: 01_inventario.md, item_id: 013UYHJHAE7SWYFK3OKFFL6BA62NSSG5W7, last_modified: 2026-10-23T11:33:34Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-23T12:05:00Z
projects: ["[[manini-automazione-ddt]]"]
clients: ["[[manini]]"]
topics: ["[[ai-nei-processi]]"]
tags: [entrata-merci, ddt, analisi-dati]
---

# Manini · caso DDT, 01 inventario del dataset

## Riassunto

Primo step di [[manini-automazione-ddt]] (21/10/2026): lettura a vista, pagina per pagina, dei 15 DDT reali inviati da [[angelo-santilli]] il 19/10. Descrive provenienza (tre flussi riconoscibili dall'etichetta QR di [[manini]]), qualità delle scansioni, presenza di ordine e codice Manini, unità di misura, colli e pesi. Conclude che la lettura si risolve con un modello che "vede" e che il vero collo di bottiglia è la corrispondenza tra codice fornitore e codice Manini. Il dettaglio campo per campo è in `inventario.json`, su OneDrive nella cartella dei dati riservati.

## Punti chiave

- Nessun PDF nativo: 10 scansioni, 3 foto da telecamera della pesa di Bastia, 2 fotocopie o fax; il 004664 è illeggibile anche per una persona e va rifiutato
- Tre flussi: Aprilia (etichetta con "Mov. 788xxx", probabile movimento AS400), Bastia, C/Esterno per commesse e cantieri
- Ordine Manini presente in 2 DDT su 3, in posizioni diverse; i 5 senza ordine sono 2 riferimenti a mail e 3 inerti dalla pesa, forse su contratti aperti
- Codice Manini esplicito solo per 2 fornitori (Hilti, MB Carpenteria), probabile in 3 (10 cifre nella descrizione); gli altri usano codici propri o generici
- Unità di misura diverse dall'ordine (m² con lunghezza, KG + NR, tonnellate, peso totale scritto come riga): servono regole di conversione per articolo
- Eccezioni già visibili: pesata Manini +1,4% sul DDT, "con riserva" scritto a mano, articolo a saldo; pagine extra e pagine mancanti da classificare prima di estrarre
- Ipotesi H1–H6, tra cui il "Mov." come numero di movimento AS400 da confermare con [[luca-zamponi]]

## Numeri

- 15 DDT, 26 pagine (17 di DDT, 9 di allegati), 14 fornitori, periodo 11/09–15/10/2026
- 91 righe articolo, mediana 2, un DDT con 45 righe
- Ordine Manini in 10 su 15; codice Manini esplicito 2, probabile 3, incerto 1, assente 9
- 027113: DDT 24.860 kg contro pesata Manini 25.220 kg (+360 kg, +1,4%)

## Decisioni e azioni

- Il benchmark si misura per campo e per tipo di acquisizione, non per fornitore (1 DDT per fornitore)
- Il file ordini simulato del matching deve contenere più ordini per DDT, ordine assente, UM diverse, codici solo del fornitore
- [ ] Chiedere a Manini: estratto AS400 dei movimenti del campione, righe d'ordine aperte dei 14 fornitori, campione di 80–100 DDT di un mese, conferma delle ipotesi H1–H5

## Versioni

- 01_inventario.md · 2026-10-23 · prima versione (analisi del 21/10)
