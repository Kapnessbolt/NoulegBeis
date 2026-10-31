---
type: source-doc
source: sharepoint
family: velo-ce-progetto-dynamics-e-power-bi-la-pianificazione-dei-fabbisogni
current:
  item_id: 01EFCYUZZTRLKR6DVGIVALYK3XB2LGJZ4G
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKVSDgPuvHRsSIc3xR8AKeVG/01EFCYUZZTRLKR6DVGIVALYK3XB2LGJZ4G
  web_url: https://blueagesrl.sharepoint.com/sites/internal/SalesMarketing/03 - Casi e referenze/Velo-CE - Progetto Dynamics - presentazioni al cliente/261021 Velo-CE - Progetto Dynamics e Power BI - La pianificazione dei fabbisogni - v004.pdf
  name: 261021 Velo-CE - Progetto Dynamics e Power BI - La pianificazione dei fabbisogni - v004.pdf
  last_modified: 2026-10-30T12:01:24Z
versions:
  - { name: "261021 Velo-CE - Progetto Dynamics e Power BI - La pianificazione dei fabbisogni - v004.pdf", item_id: 01EFCYUZZTRLKR6DVGIVALYK3XB2LGJZ4G, last_modified: 2026-10-30T12:01:24Z }
also_at: []
status: active
partial: true
ingested_at: 2026-10-31T05:56:18Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [deck, velo-ce, mrp, pianificazione, conto-lavoro, subcontracting, cliente]
---

# Velo-CE · La pianificazione dei fabbisogni (21/10)

## Riassunto

Deck BlueAge di 55 slide (v004 del 21/10/2026, materiale per il cliente), presentato il 21 ottobre a [[stefano-moruzzi]] e Augusto di [[velo-ce]]. Racconta in sette capitoli la catena dall'ordine del dealer al tubo: chi tira (gli ordini) e chi spinge (le scorte), cosa propone il prospetto di pianificazione di Business Central e chi accetta, con le prove del 20 e 21 ottobre in sandbox. Lette le prime 30 slide su 55 (capitoli 1–4).

## Punti chiave

- **Un solo motore**: il prospetto parte da ordini di assemblaggio aperti e scorte sotto soglia, scende la distinta e propone ordini di produzione, d'acquisto o di trasferimento; le proposte si correggono e si accettano. Due criteri: lotto per lotto (verniciati) e quantità fissa con punto di riordino (sabbiato, tubi, componenti).
- **Regole per livello**: bici con assemblaggio su ordine dalla riga di vendita; telaio verniciato lotto per lotto con accumulo di una settimana e scorta solo su alcuni colori (Augusto accetta); forcella verniciata come il telaio; sabbiato con punto di riordino 24 e lotto 24; tubi in metri con scarto 5%; componenti dai consumi 2026; motori e batterie su ordine programmato a Universal, con il prospetto come controllo.
- **Dall'ordine alla bici**: avviso di disponibilità all'inserimento, componenti scaricati alla spedizione, giacenza negativa bloccata; fasi di montaggio nella colonna Posizione della distinta e numero di telaio come numero di serie: servono piccole modifiche di stampa (foglio di linea, fattura), dopo l'avvio.
- **Rischio**: un telaio senza colore sulla riga dell'ordine di assemblaggio fa proporre un verniciato senza variante.
- **Conto lavoro verso HS**: con l'app Microsoft Subcontracting, dall'ordine rilasciato al foglio conto lavoro, ordine d'acquisto a HS con telaio e forcella insieme, trasferimento al magazzino C/LAVORO e rientro; provato il 20/10. Mancano il listino di HS per pezzo e la prova della fattura.
- **Il piano si aggiorna**: messaggi (nuovo, modifica quantità, riprogramma, annulla) e avvisi (urgenza, eccezione, attenzione); a ogni calcolo le proposte non eseguite si rifanno; un solo prospetto lanciato da un solo utente.

## Numeri

- 55 slide, 7 capitoli; prova sul RAL 6029: scorta 8 + 6 ordinate − 1 in magazzino − 6 in ordine = proposta 7.
- Accumulo settimanale: quattro ordini al verniciatore diventano uno da 8 telai.

## Decisioni e azioni

- Scorte per colore da fissare con Stefano; scorta delle forcelle da decidere; da verificare con lo sviluppatore del portale che gli ordini B2B facciano nascere l'assemblaggio su ordine.

## Versioni

- 261021 Velo-CE - Progetto Dynamics e Power BI - La pianificazione dei fabbisogni - v004.pdf · 2026-10-30 · prima versione ingerita, PDF del deck v004 del 21/10; letta in parte (30 slide su 55)
