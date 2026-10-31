---
type: source-doc
source: sharepoint
family: velo-ce-pilota-bc-lungo-bosch-modello-dati-5-fogli
current:
  item_id: 01EFCYUZ7T342LVQDI5RFICNKT2ZKZ5LW6
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ7T342LVQDI5RFICNKT2ZKZ5LW6
  web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/02 Configurazione/Telaio e produzione/Velo-CE - Pilota BC Lungo Bosch - Modello dati 5 fogli - v008.xlsx"
  name: "Velo-CE - Pilota BC Lungo Bosch - Modello dati 5 fogli - v008.xlsx"
  last_modified: 2026-09-29T14:04:38Z
versions:
  - { name: "Velo-CE - Pilota BC Lungo Bosch - Modello dati 5 fogli - v008.xlsx", item_id: 01EFCYUZ7T342LVQDI5RFICNKT2ZKZ5LW6, last_modified: 2026-09-29T14:04:38Z }
  - { name: "Velo-CE - Pilota BC Lungo Bosch - Modello dati 5 fogli - v008.xlsx", item_id: 01EFCYUZ7RVPSSO235KRB3ZCNBGOROHLH3, last_modified: 2026-09-29T14:04:38Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:28:59Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [pilota-lungo, modello-dati, anagrafica, distinte, cicli, decisioni, business-central-premium]
---

# Velo-CE · Pilota BC Lungo Bosch: modello dati in 5 fogli (v008)

## Riassunto

Modello dati TO-BE della bici pilota MLCA-5E-545-CDX (Multi Lungo Bosch Cargo Line, batteria 545 Wh, Nexus 5, cinghia Gates CDX), versione v008 aggiornata con le risposte del reparto del 29/09/2026 e con i tempi del triangolo tarati sulla resa. Cinque fogli: articoli (anagrafica dell'intera bici con codice pilota LU-xxx, codice BC attuale, tipologia, sistema di rifornimento, politica, stato e attivazione), distinte multilivello, cicli e postazioni, campi della scheda articolo per tipologia, registro di 52 decisioni, assunzioni e verifiche (F5-01…F5-52). Il filtro attivo è sulla fetta "telaio verniciato", in lavorazione dal 27/09. È il riferimento per la prova in sandbox e per il flusso operativo del telaio ([[velo-ce-flusso-operativo-telaio-a-scorta-acquisto-sabbiato-interno]]).

## Punti chiave

- **Struttura della bici**: bici ATO (oggi senza distinta e a costo zero, 326 vendute nel periodo dell'estrazione) → telaio verniciato LU-002 (variante colore, conto lavoro, lotto per lotto) → telaio sabbiato LU-003 (candidato VE-TL-LUFR-BH-24, ultimo buffer, lotto 8) → triangolo LU-004 (articolo nuovo, 5 tubi + housing + supporto batteria) e carro come fantasma PH-CARRO-LUNGO (9 pezzi saldati da Simone in dima) → particolari laser e housing LU-012 (articolo unico, multiplo 91) → materie prime (tubi trafilati Ø38x2 e Ø35x1,5 a metri, ellittico e tubi saldati acquistati a kg, lamiere 2, 3, 5, 8 mm a kg).
- **Resto della bici** (fase successiva): ruote prodotte dalla linea ruote, moduli fantasma per motorizzazione Bosch Cargo e trasmissione Nexus 5 + Gates (forma da decidere, F5-04), batteria come articolo autonomo, freni, cockpit VE-CK-BCX, componenti non codificati (pedivelle, pedali, parafanghi), consumabili e imballi; opzioni CNF-ML, CNF-BCX, CNF-545, CNF-5E, CNF-CDX.
- **Modello di codifica nel pilota**: codici provvisori LU-xxx, PH- per le fantasme, RIS- per le risorse; riuso del codice BC solo se il match è affidabile (molti abbinamenti "Da verificare"); i 5 tubi del triangolo prendono i nomi del reparto e non hanno codice; postazioni con tre lettere più numero (LAS-01, LAS-02, PIE-01, TRA-01, ROB-01, DIM-01/02/03, SAB-01, BAN-01/02/03); cicli CI-…; categoria articolo a tre livelli tipologia › famiglia › oggetto (F5-43). Misura, lato, base BH/SH, colore e fornitore restano in descrizione e materiale, da riconsiderare in codifica (F5-02).
- **Decisioni prese (27/09 e 29/09)**: articolo prodotto solo se va a scorta (F5-05); triangolo Lungo nuovo (F5-09); FIFO (F5-21); niente collocazioni all'avvio, secondo deposito a 3 km come magazzino a parte (F5-22); verniciatura come conto lavoro nel ciclo (F5-30); un'operazione per postazione (F5-32); chi registra in reparto (F5-35); filo, gas e graniglia come costo indiretto (F5-36); imballo del sabbiato senza codice (F5-37); tre tariffe persone, laser, robot (F5-38); componenti in avanti, centri su Manuale con output dichiarato a mano sull'ultima operazione (F5-39); lotto 8 (F5-40); scarti con codice motivo, riprese come tempo (F5-42); quantità fissa con punto di riordino sui buffer, lotto per lotto sui verniciati (F5-45); housing articolo unico (F5-48); tempi di presidio tarati sulla resa giornaliera (F5-52).
- **Aperte**: diametro e spessore dei tubi (F5-09, F5-10); ruote 24" o 20" (F5-11); codice del motore Cargo Line (F5-12); set Gates e freni (F5-13, F5-14); significato del codice telaio MY24 (F5-16); serializzazione di batteria e lucchetto (F5-23, rinviata); se il pilota resta sulla Lungo MY24 (F5-24); attivazione di carro e altre parti saldate (F5-27); chi apre e chiude gli ordini (F5-50); varianti del forcellino (F5-51); export distinte da BC e working paper reale (F5-06, F5-07).

## Numeri

- Foglio 1: blocco A 127 righe (7 esistono in BC, 37 nuove, 83 da verificare), blocco B 29 righe; fetta telaio 56 righe con 25 articoli prodotti (19 passano dal laser); 44 note con domanda aperta.
- Fogli: distinte 156 righe, cicli 73 righe (9 cicli, 19 righe nella fetta), campi per tipologia 35 righe, decisioni 52.
- Costi d'acquisto dalle fatture: tubo Ø38x2 7,10 €/m, Ø35x1,5 7,43 €/m, ellittico 1,53 €/kg, lamiere 0,96-0,97 €/kg, tubo 16x1 1,476 €/kg.
- Tubi: lunghezza di taglio + 5 mm, × 1,04 di resa; 160 mm a barra nel mandrino su barre da 4,3-5 m. Lamiera per housing 1,1645 kg (91 nei 105,975 kg teorici).
- Triangolo: 32 minuti (12 + 17,5 + 2,5), circa 15 al giorno; riprese circa 15% dei triangoli, oltre 30% degli accessori. Tariffe fittizie 30, 60, 45 €/h.
- Lotti: foderi 500, piastre 150-200, campagne da circa 200 triangoli.

## Decisioni e azioni

- [ ] Confermare con Ranzini, pezzo per pezzo, gli articoli prodotti del Foglio 3c
- [ ] Fotografare la tabella di taglio per confermare lunghezze e margini dei tubi
- [ ] Far salvare a Ranzini i report dei nesting standard (housing, forcellini, piastre) prima del go-live
- [ ] Esportare da BC le distinte di VE-CDX-001, VE-WH-001, VE-CK-BCX, VE-TL-G-HU-BH, VE-MU-G-TRI-BH23 ed estrarre un working paper completo da Veloce-CRM
- [ ] Definire con l'amministrazione categorie contabili e tariffe orarie

## Versioni

- Velo-CE - Pilota BC Lungo Bosch - Modello dati 5 fogli - v008.xlsx · 2026-09-29 · prima versione ingerita (v008: risposte del reparto del 29/09, housing articolo unico, tre tariffe, tempi tarati sulla resa)
