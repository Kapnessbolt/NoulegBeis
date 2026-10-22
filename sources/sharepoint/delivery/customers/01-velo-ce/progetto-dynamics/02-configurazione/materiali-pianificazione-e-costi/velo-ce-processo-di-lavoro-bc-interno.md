---
type: source-doc
source: sharepoint
family: velo-ce-processo-di-lavoro-bc-interno
current:
  item_id: 01EFCYUZ7DWFSTPPXDC5AIIGLJ7MOQUVLV
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ7DWFSTPPXDC5AIIGLJ7MOQUVLV
  web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/02 Configurazione/Materiali, pianificazione e costi/Velo-CE - Processo di lavoro BC - INTERNO - v001.xlsx"
  name: "Velo-CE - Processo di lavoro BC - INTERNO - v001.xlsx"
  last_modified: 2026-10-05T08:48:20Z
versions:
  - { name: "Velo-CE - Processo di lavoro BC - INTERNO - v001.xlsx", item_id: 01EFCYUZ7DWFSTPPXDC5AIIGLJ7MOQUVLV, last_modified: 2026-10-05T08:48:20Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:28:59Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [as-is, processo, magazzino, contabilita, so-smart, eos, controlli, business-central]
---

# Velo-CE · Processo di lavoro in Business Central: dalla merce in ingresso alla contabilità

## Riassunto

Cartella di lavoro interna BlueAge del 05/10/2026 (non mostrabile al cliente né a So Smart) che fotografa il processo AS IS in BC dal carico della merce alla contabilità, seguendo tre casi reali: A una fattura passiva di componenti da SdI, B il portapacchi anteriore AMFR (assemblaggio e rettifiche), C un frame kit Van Nicholas assemblato su ordine. Ha quattro fogli: leggimi con regole di lettura in sola lettura sull'ambiente Production, mappa del processo in 15 passi (MP01-MP15), 20 controlli a sistema da eseguire in ordine (PL01-PL20, tutti "Da fare") e il catalogo degli oggetti So Smart (app EOS) lungo il giro. Serve a disegnare il processo del nuovo tenant (CT-11, CT-13) e la costificazione (K01-K03, CT-32); è il piano operativo da cui è nata la rilevazione [[velo-ce-giro-reale-dei-materiali-in-bc-interno]].

## Punti chiave

- **Regole**: mai registrare né lanciare azioni che scrivono; non aprire i prospetti So Smart segnati ⚠ (possono ricalcolare). Ogni affermazione marcata VERIFICATO, DICHIARATO, DA RILEVARE o DOCUMENTALE; quattro segni d'uso So Smart (S1 campo EOS valorizzato, S2 tabella EOS scritta alla registrazione, S3 pagina usata da persone, S4 automatismo notturno).
- **Mappa AS IS (sintesi)**: riordino deciso a occhio da Stefano, nessun articolo con metodo di riordino; uso degli ordini d'acquisto da rilevare; ultimo carico registrato nel registro EOS il 29/04/2026; fatture passive da IX-FE importate con l'app EOS Electronic Invoice for Italy; costi accessori (trasporti, dazi) di destinazione ignota; rettifiche positive al posto degli assemblaggi su AMFR; inventario di gennaio fatto da Augusto, registrazione ignota; 571 assemblaggi registrati, per le Veloe nessun ordine di assemblaggio (working paper in Veloce-CRM); conto lavoro di verniciatura fuori da BC dal novembre 2025; "Reg. automatica costi" = No, il valore di magazzino non va in C/G; valutazione fiscale con l'app IVC (FIFO, LIFO, medio in parallelo).
- **Controlli prioritari (alta)**: PL01 come entra la merce nel 2026; PL02 uso degli ordini d'acquisto; PL03-PL05 fattura A, anteprima EOS e carico; PL07-PL09 rettifiche, costo di AMFR, inventario di gennaio; PL12-PL13 chi crea gli ordini di assemblaggio VN e se So Smart rimappa i componenti; PL16-PL18 conti di magazzino, "Registra costo magazzino in C/G", come entrano le rimanenze 2025 nel bilancio.
- **Oggetti So Smart**: usati davvero l'import delle fatture elettroniche, il registro dei documenti da fatturare, i report DDT e ordine di assemblaggio, IVC, PDA (correzioni di dati registrati), dichiarazioni d'intento; configurati ma senza movimenti i flussi MMI d'acquisto, magazzino e assemblaggio e il connettore WMS (Modula).
- PL11 coincide con TS04 del questionario interno; PL18 e PL20 si fanno una volta sola con la sessione IVC. Le domande nuove vanno nel questionario interno v003 (I12-I17).

## Numeri

- 15 passi di processo, 20 controlli (20 da fare, 0 fatti al 05/10), circa 30 oggetti So Smart catalogati.
- Documenti elettronici in entrata: 7.936 testate, 86.182 righe; 6.880 anteprime.
- Registro documenti da fatturare: 36.720 righe; plafond IVA: 102 dichiarazioni d'intento e 2.188 movimenti.
- 571 assemblaggi registrati; 7 richieste PDA nel 2026; prossima evidenza libera E154.

## Decisioni e azioni

- [ ] Eseguire i controlli PL01-PL20 in ordine, in sola lettura, compilando esito, data, evidenza e risultato e aggiornando la mappa
- [ ] Riportare le domande che i dati non chiudono nel questionario interno v003 (foglio Domande)

## Versioni

- Velo-CE - Processo di lavoro BC - INTERNO - v001.xlsx · 2026-10-05 · prima versione ingerita
