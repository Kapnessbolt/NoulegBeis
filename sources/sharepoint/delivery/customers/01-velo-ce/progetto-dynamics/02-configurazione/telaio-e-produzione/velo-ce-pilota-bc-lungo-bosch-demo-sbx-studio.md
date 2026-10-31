---
type: source-doc
source: sharepoint
family: velo-ce-pilota-bc-lungo-bosch-demo-sbx-studio
current:
  item_id: 01EFCYUZ5SV5SXXWRF2BBLR4IDJ7YZPS2J
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ5SV5SXXWRF2BBLR4IDJ7YZPS2J
  web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/02 Configurazione/Telaio e produzione/Velo-CE - Pilota BC Lungo Bosch v006 - Demo sbx-studio - contenuti, copione e risposte a Leo - v001.docx"
  name: "Velo-CE - Pilota BC Lungo Bosch v006 - Demo sbx-studio - contenuti, copione e risposte a Leo - v001.docx"
  last_modified: 2026-09-28T18:50:51Z
versions:
  - { name: "Velo-CE - Pilota BC Lungo Bosch v006 - Demo sbx-studio - contenuti, copione e risposte a Leo - v001.docx", item_id: 01EFCYUZ5SV5SXXWRF2BBLR4IDJ7YZPS2J, last_modified: 2026-09-28T18:50:51Z }
  - { name: "Velo-CE - Pilota BC Lungo Bosch v006 - Demo sbx-studio - contenuti, copione e risposte a Leo - v001.docx", item_id: 01EFCYUZ7D6FTGQN7DQVFZXBJUYCNSQJ55, last_modified: 2026-09-28T18:50:51Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:28:59Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [pilota-lungo, sandbox, demo, esito-prove, conto-lavoro, costi, business-central-premium]
---

# Velo-CE · Pilota BC Lungo Bosch v006 su sbx-studio: contenuti, copione della demo e risposte alle prove di Leo

## Riassunto

Documento interno di Cristian (BlueAge) del 28/09/2026, 5 pagine, che descrive il caricamento del modello dati v006 nella società di prova VC-PILOTA TELAIO dell'ambiente BlueAge sbx-studio (Sandbox, Premium, BC 28.5), il copione di una demo di circa 25 minuti e l'esito di ciascuna prova chiesta nella nota di Leo del 27/09 ([[velo-ce-pilota-bc-lungo-bosch-fetta-telaio-verniciato-nota-per-trif]]). È il primo esito concreto del pilota "Lungo" sul tratto telaio: lotto laser, telaio sabbiato con la fantasma del carro e conto lavoro con varianti colore funzionano; emergono due trappole (scarto contato due volte con consuntivazione Indietro, costo della verniciatura che non entra nel telaio) e alcune regole per la migrazione vera. Tutti i costi sono di esempio (30 €/h).

## Punti chiave

- **Cosa è stato caricato (verificato il 28/09)**: 20 articoli LU (9 d'acquisto, 11 prodotti, tutti FIFO), 33 categorie a tre livelli, 23 unità di misura articolo, varianti RAL6029 e RAL9005 su telaio e forcella verniciati, 8 fornitori di prova (tra cui il verniciatore), aree TEL e VER, 11 centri di lavoro, 9 cicli (14 operazioni), 12 distinte certificate compresa la fantasma del carro, 3 codici scarto, giacenze iniziali con documento APERTURA, 4 pacchetti di configurazione VC6-A…D, app Subcontracting installata il 27/09.
- **Esito delle prove**: 4.0 preparazione fatta (servono setup non previsti: gruppo aree, calendari, unità M, esperienza Premium); 4.1 in parte (ordine in KG e rettifica in fogli non eseguiti); 4.2 sì con correzione (riga fantasma arrivata vuota dal pacchetto); 4.3 sì (tubo esce al rilascio, costo = materiale + tempo); 4.4 no con la regola della nota, sì con fase Manuale; 4.5 sì; 4.6 in parte (un solo ordine d'acquisto per due colori, output per variante, ma prezzo a 0 e costo non entra); 4.7 non provata sulla v006 (verificata sulla v004); 4.8 in parte (colonna del conto lavoro vuota); 4.9 non provata.
- **Trappola dello scarto**: con consuntivazione Indietro, alla chiusura BC registra in automatico il residuo non dichiarato come output (40 foderi invece di 38); il flag "Finished" non lo evita. Regola da portare a Velo-CE: fase Manuale dove si dichiara lo scarto (decisione di modello §7.4 p.81, tocca F5-39).
- **Costo della verniciatura**: non entra né dall'area VER (costo diretto 0, calcolo per unità) né dal "Costo unitario per" del ciclo; da provare "Costo unitario specifico" = Sì su VER, come nel terzista CRONUS.
- **Regole per la migrazione vera**: le righe fantasma arrivano vuote dal pacchetto se hanno unità di misura; il codice gruppo aree è obbligatorio per il calendario e senza calendario l'ordine non si aggiorna; una società copiata da "My Company" nasce Essential e senza unità M; la consuntivazione sta su area e centro e passa all'ordine alla creazione, quindi la regola sullo scarto va decisa prima di caricare i centri; ordine dei passaggi setup → aree e centri → articoli → cicli e distinte → collegamenti → certificazione.
- **Domande tecniche**: lead time vuoto sugli articoli prodotti funziona (date dal ciclo); postazioni all'indietro registrano tutto ma contano due volte lo scarto; famiglia di produzione per pezzi dallo stesso foglio e DDT di conto lavorazione non provati.
- La v004 (società CRONUS IT e VC-E2E TEST) non è stata toccata ed è il ripiego per la demo.

## Numeri

- ODP 101001: 50 tubi sterzo, −11 m di tubo (−78,10 €), 100 minuti di laser (50 €), costo 128,10 € (2,562 € a pezzo).
- ODP 101002: 40 foderi, 38 buoni + 2 scarti, alla chiusura +2 in automatico. ODP 101008 (Manuale): 4 buoni a 28,50 € (7,125 € a pezzo).
- ODP 101003: 8 telai sabbiati a 886,20 € (546,20 materiale + 340,00 tempo: DIM-01 320 min, BAN-01 80, SAB-01 240, BAN-02 40).
- Ordine d'acquisto 106001 al verniciatore: due colori, prezzo arrivato a 0, scritto a mano 12 €.
- Costo del telaio verniciato LU-002: 76,07 € = materiale 13,57 + lavorazione interna 62,50 (125 minuti); conto lavoro vuoto.
- Unità: lamiera 3 mm FOGLIO = 106 kg, 5 mm = 176,625 kg; ellittico 1 kg = 1,28733 m.

## Decisioni e azioni

- Decisione di modello proposta: fase Manuale dove si dichiara lo scarto, Indietro solo dove non si dichiara.
- [ ] Non chiudere l'ODP 101007 durante la demo (rispondere No alla domanda di BC)
- [ ] Provare "Costo unitario specifico" = Sì sull'area VER e rileggere il Dettaglio costi DB
- [ ] Correggere la procedura di caricamento delle righe fantasma (senza unità di misura)
- [ ] Provare il calcolo del piano sulla v006 con righe di vendita in due colori, l'ordine d'acquisto in KG, la fattura del filo e il DDT di conto lavorazione

## Versioni

- Velo-CE - Pilota BC Lungo Bosch v006 - Demo sbx-studio - contenuti, copione e risposte a Leo - v001.docx · 2026-09-28 · prima versione ingerita
