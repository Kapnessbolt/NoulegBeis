---
type: source-doc
source: sharepoint
family: velo-ce-stato-progetto-02-cantieri-dominio
current:
  item_id: 01EFCYUZ5HJLEOWEM7CVF3LWGLI24GP6BY
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ5HJLEOWEM7CVF3LWGLI24GP6BY
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/99 Project Claude (copia)/velo-ce-stato-progetto-02-cantieri-dominio.md
  name: velo-ce-stato-progetto-02-cantieri-dominio.md
  last_modified: 2026-10-08T10:43:52Z
versions:
  - { name: velo-ce-stato-progetto-02-cantieri-dominio.md, item_id: 01EFCYUZ5HJLEOWEM7CVF3LWGLI24GP6BY, last_modified: 2026-10-08T10:43:52Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:25:37Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, business-central, cantieri, anagrafica, costificazione, distinte, codifica, etichette, interno]
---

# Velo-CE · Stato progetto, blocco 02 · Esigenza di business, cantieri, priorità operativa, regole di dominio

## Riassunto

Blocco 02 (§3-§6) dello stato progetto Velo-CE, interno BlueAge. Fissa l'esigenza di business n.1 («sempre i materiali per andare in produzione, basta mancanze»), la sequenza dei nove cantieri (0-8) con il raccordo alla mappa cantieri C01-C31, cosa costa e cosa no fra MRP e Produzione, la decisione Premium del 23/09. Descrive la priorità operativa corrente (anagrafica articoli e costificazione) con lo stato per area, le incoerenze, i costi mancanti e la rilevazione del 05/10 sul giro reale dei materiali a sistema. Chiude con le regole di dominio decise su distinte e codifica e con le prove del 07/10 sulle etichette articolo e collo in standard.

## Punti chiave

- **Esigenza n.1**: avere sempre i materiali, né troppi né pochi; marginalità, reportistica e controllo di gestione rimandati. Si serve in Essentials: la condizione vera è un metodo di riordino su ogni livello della catena (R01), identica in Premium.
- **Perché adesso**: la direzione strategica è crescere per acquisizioni (Van Nicholas è la prima); va disegnata da subito un'architettura multi-brand e multi-entità.
- **Cantieri**: 0 analisi visiva delle giacenze; 1 anagrafiche (gli articoli sono il grosso); 2 codifica della saldatura; 3 distinte che seguono la realtà; 4 giro dei materiali (il cuore); 5 acquisti centralizzati; 6a accensione MRP, 6b produzione (richiede Premium); 7 costificazione; 8 controllo di gestione e reportistica (2027).
- **D12 decisa il 23/09: Premium** (decisione di Stefano); verso So Smart si presenta come «la direzione è Premium», con il cambio di esperienza dopo la validazione su sandbox (R10). Le licenze restano a So Smart/EOS per scelta di Stefano; con le sottoscrizioni mensili D12 non ha scadenza.
- **Vincolo di dati sull'MRP**: oggi il piano non propone nulla (nessun metodo di riordino); bici Veloe a rifornimento Acquisto, AMFR a «Ordine di produzione» non eseguibile in Essentials. D01, D07 e R01 sono prerequisiti bloccanti del cantiere 6a.
- **Anagrafica per area**: bici Veloe come articoli non di inventario senza distinta e a costo zero (verificato 05/10); Van Nicholas con frame set e assemblaggio; telaio abbozzato (84 codici di parti) e senza giacenza; mancano i codici di saldatura, parti telaio, tubi, barre e lamiere, viteria speciale.
- **Costificazione**: costi accessori in un Excel di Stefano; dazi non ribaltati, valore dello stock Accell attribuito in blocco, articoli a costo zero, costo di assemblaggio e di saldatura assenti, conto lavoro gestito fuori da BC. Il meccanismo standard (risorse in distinta, addebiti articolo) esiste già in Essentials. Nodo aperto: costo standard o FIFO sui fabbricati (orientamento: FIFO sugli articoli, standard sulla tariffa di trasformazione).
- **Giro reale dei materiali (05/10)**: il magazzino di BC non è alimentato dal ciclo passivo: fatture dei componenti su conto contabile senza righe articolo; merce caricata a mano con giornale articoli per far passare assemblaggi e spedizioni, spesso a costo zero; da maggio 2026 ordini d'acquisto aperti mai ricevuti. Rimanenze di bilancio da inventario fisico, scritte a mano in contabilità. Prima di MRP e costificazione va deciso il giro d'acquisto standard (cantiere 5).
- **Regole di dominio**: la distinta segue la realtà fisica (assieme se c'è una lavorazione, acquisto se si compra montato); in Essentials un livello di distinta è una fase; la variante colore va sulla riga, basi con distinta diversa sono articoli distinti; codice radice + desinenza, mai l'anno nel codice; Van Nicholas non si tocca ora; strada ibrida per famiglia decisa il 23/09 per la ricodifica Veloe.
- **Telaio verniciato**: verniciato (variante RAL) ← sabbiato ← saldato; verniciatura esterna con addebito articolo sul rientro dal terzista, non come articolo non di inventario.
- **Etichette (07/10)**: in standard e in Essentials l'etichetta articolo con layout Velo-CE stampa il codice in Code 39 senza sviluppo; dall'ordine d'acquisto si stampano etichette per riga (A6) e un'etichetta collo A5; quantità per collo, collo «n di m» e Code 128 richiedono un'estensione (esecutore da decidere fra BlueAge e So Smart). Capitolato di etichettatura per i fornitori in bozza, da inviare solo con i codici definitivi.
- **Rischio ricodifica**: il canale ordini MMI usa il numero articolo di BC come chiave; l'etichettatura oggi è prodotta da Veloce-CRM (We Make Code).

## Numeri

- Obiettivo MRP: 70-80% di proposte accettate; volume 2027 citato 1.500-2.000 bici; produzione 6-15 bici al giorno.
- Premium: Essentials 69,30 euro contro Premium 95,30 euro per utente al mese (+78 euro al mese per 3 utenti, +936 euro l'anno, listino annuale).
- Articoli: 1.112 codici, 418 con giacenza, 669 a costo zero (279 con giacenza), valore circa 168.000 euro; circa 140 codici con distinta di assemblaggio; 1.263 righe di distinta; 571 assemblaggi registrati (6 su ordine).
- Costi mancanti: dazi circa 50.000 euro; stock Accell 150.000 euro attribuito in blocco; circa 306.000 euro di costo mancante sulle bici Van Nicholas di fine maggio-giugno 2026 (calcolato); rettifica negativa del 13/07 di 1.400 pezzi per -491.400 euro da spiegare.
- Merce entrata con giornale nel 2026: circa 2,9 milioni di euro (2,87 milioni Van Nicholas); 27 ordini d'acquisto aperti da maggio 2026 non ricevuti.
- Rimanenze di bilancio: 2.713.672 euro al 31/12/2024 e 2.059.737,50 euro al 31/12/2025.
- Cambio USD fissato a 1,14 con forward su circa 1 milione di dollari.
- Materie prime telaio: tubo E235 38x2 a 7,10 euro/m, E355 35x1,5 a 7,43 euro/m.

## Decisioni e azioni

- 23/09: D12 decisa, direzione Premium (data esatta della decisione da rilevare).
- 23/09: strada ibrida per famiglia nella ricodifica (nuovo codice per bici Veloe e accessori AC/AM, ibrido per le parti telaio, rinomina per sottogruppi e ruote, creazione per materie prime e saldatura; Van Nicholas invariato).
- 05/10 (Stefano): le rimanenze di bilancio non si prendono da BC ma dall'inventario fisico.
- [ ] Chiarire con l'amministrazione chi usa il modulo EOS di valorizzazione del magazzino e per cosa (I01).
- [ ] Decidere il giro d'acquisto standard (ricevimento sull'ordine, fattura sulle righe articolo, addebiti) prima di MRP e costificazione.
- [ ] Decidere con il cliente regola di codifica (OP-10), tracciabilità del telaio e capitolato di etichettatura dei fornitori.
- [ ] Caricare il codice del fornitore nel catalogo articoli fornitori dopo la regola di codifica (dati dal cliente, caricamento BlueAge).
- [ ] Verificare se il batch di registrazione del costo magazzino in contabilità è mai stato lanciato.
- [ ] Spiegare la rettifica negativa MAG26-0266 del 13/07 e il ritorno al giornale articoli da aprile 2026.

## Versioni

- velo-ce-stato-progetto-02-cantieri-dominio.md · 2026-10-08 · prima versione ingerita (stato progetto 025.66); data di modifica della riorganizzazione della cartella
