---
type: source-doc
source: sharepoint
family: velo-ce-stato-progetto-03-decisioni-aperte
current:
  item_id: 01EFCYUZ6FLONC3FDJJFEIMLFVJX7MKTRZ
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ6FLONC3FDJJFEIMLFVJX7MKTRZ
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/99 Project Claude (copia)/velo-ce-stato-progetto-03-decisioni-aperte.md
  name: velo-ce-stato-progetto-03-decisioni-aperte.md
  last_modified: 2026-10-29T16:14:35Z
versions:
  - { name: velo-ce-stato-progetto-03-decisioni-aperte.md, item_id: 01EFCYUZ6FLONC3FDJJFEIMLFVJX7MKTRZ, last_modified: 2026-10-29T16:14:35Z }
  - { name: velo-ce-stato-progetto-03-decisioni-aperte.md, item_id: 01EFCYUZ4KI2E7NODW6VFZLEBW6P6ZP6KZ, last_modified: 2026-10-28T08:06:16Z }
  - { name: velo-ce-stato-progetto-03-decisioni-aperte.md, item_id: 01EFCYUZ7LPNBMHRTVJFHI467EREJPGL4B, last_modified: 2026-10-08T10:43:52Z }
also_at:
  - { web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/Claude outputs/proj18/velo-ce-stato-progetto-03-decisioni-aperte.md.txt", item_id: 01EFCYUZ6E4QZ6RF4BYFFJSK5AGDAGCLOW }
  - { web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/98 Share Team/Velo-CE - Contesto Claude per Leonardo - INTERNO - v001/velo-ce-stato-progetto-03-decisioni-aperte.md", item_id: 01EFCYUZ7WXPBVVZ2Y7BEJLKSOCAEI6DH3 }
status: active
partial: false
ingested_at: 2026-10-30T05:58:45Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]", "[[fatturazione-elettronica-sdi]]"]
tags: [velo-ce, business-central, decisioni, tenant-unico, premium, fattura-elettronica, governance, interno]
---

# Velo-CE · Stato progetto, blocco 03 · Decisioni aperte

## Riassunto

Blocco 03 (§7) dello stato progetto Velo-CE, interno BlueAge, il più aggiornato del documento (85 mila caratteri). Elenca le decisioni del cliente da istruire con lui (7.1), i punti tecnici (7.2) e di business (7.3) da chiarire e 87 punti emersi dal 16/09 (7.4), molti chiusi con evidenze a sistema. Il tema dominante di fine settembre e inizio ottobre è il passaggio a un tenant unico Microsoft di Velo-CE, con la scelta fra reimplementazione da zero in Premium e trasferimento dell'ambiente attuale, il ruolo di So Smart, le app fiscali EOS (fattura elettronica, ratei, report dei documenti, valutazione del magazzino) e la ripresa dati al 01/01/2027. Seguono i temi di governance degli accessi (app «CRM» che scrive gli ordini con l'identità del titolare), il giro d'acquisto standard e la pulizia di ordini e carichi a costo zero.

## Punti chiave

- **Decisioni del cliente (7.1)**: contenuto della variante (orientamento colore); dove mettere la scorta; perimetro della ricodifica; processo ordine-spedizione-fattura; sorte del software esterno; attrito operativo accettabile; cantiere make-to-stock; automatizzare i canali d'ordine manuali (bici Van Nicholas, Shopify, WordPress/Stripe); parti laser del telaio (scenari A, C o D); verniciatura esterna (addebito sul rientro o risorsa a tariffa).
- **D12 Premium decisa il 23/09** (Stefano); resta aperto il quando del cambio di esperienza, dopo la validazione su sandbox (R10). Piano in quattro passi: licenze Premium, utenti spostati, accesso ancora in esperienza Essentials, cambio di esperienza quando il reparto è pronto.
- **Tenant unico (7.1 p.12)**: ipotesi BlueAge del 29/09, diventata direzione condivisa con il cliente dopo la presentazione del 30/09 sera a Stefano e Claudia: Business Central va spostato nel tenant Microsoft di Velo-CE (dominio della posta). Tre decisioni separate: piattaforma (tenant unico, decisa), applicativa (reimplementare o trasferire, orientamento del 07/10 alla reimplementazione da zero, in valutazione l'alternativa «due società» nello stesso ambiente), partner (ruolo di So Smart).
- **Condizioni per la reimplementazione**: Velo-CE deve amministrare tenant e dominio (oggi gestiti da un fornitore esterno, G02); decisione di Stefano su So Smart, AMS e canale delle licenze; soluzione per le app fiscali; taglio a inizio esercizio con il commercialista; canale ordini ricostruito sulle API standard.
- **So Smart in Premium (07/10)**: So Smart garantisce app fiscali, connettori e AMS anche in Premium, esclusa la configurazione della produzione: da confermare per iscritto; cade il motivo «So Smart non copre Premium».
- **Fattura elettronica**: intermediario Able Tech (IX-FE, dal 31/12/2025 «ARXivar Invoice Italia»), che non conserva; la conservazione a norma è un servizio separato (IX-CE). XML e progressivo del nome file li genera BC con l'app EOS: vanno portati nel nuovo tenant, altrimenti SdI scarta i file come duplicati. Assunzioni FE1-FE6 da chiudere (conservazione attiva, contratto intestato a Velo-CE, codice destinatario, canale d'invio, abbonamento EOS riattivabile, accesso al portale del conservatore). BC invia anche autofatture e documenti per fornitori UE.
- **Altre app EOS (04-05/10)**: ratei e risconti (Accruals) fermi dal 2023, candidata all'uscita insieme ad altre 5 app; Advanced Document Reporting usata ogni giorno per conferme e fatture ai clienti esteri, prima candidata a passare allo standard; DDT e fattura accompagnatoria si stampano con report So Smart; il modulo di valorizzazione del magazzino gira ogni notte ma non serve al bilancio (candidato all'uscita); lo strumento per modificare dati registrati è stato usato per annullare e rifare la liquidazione IVA di dicembre 2025 e per altre correzioni: non si toglie d'ufficio, decide Stefano chi lo usa.
- **Strade verso il tenant unico** (deck CLIENTE v002 del 04/10): cinque strade, dal nuovo BC con spegnimento del vecchio dopo il bilancio fino al trasferimento con ricodifica graduale. Obiettivi sullo storico: navigabile almeno fino al bilancio 2026, parallelo per sei mesi del 2027, confronto per articolo in Power BI.
- **Saldi d'apertura**: nel nuovo BC entra solo lo stato patrimoniale al 01/01/2027; proposta BlueAge: apertura in due tempi con conto transitorio. Piano della ripresa dati del 07/10 (RD01-RD26, RQ01-RQ09, RF0-RF4).
- **Piano attività del nuovo ambiente (07/10)**: 185 righe NBC con chi esegue, fase, percorso critico verso l'08/01/2027 e decisioni del cliente con data limite.
- **Governance**: il canale ordini MMI gira con l'identità personale del titolare tramite l'app Entra «CRM» del cliente, con due client esterni (uno verosimilmente We Make Code); l'app ha anche permessi di gestione degli ambienti; So Smart ha più canali sul tenant (utenze, delega GDAP, account amministratore globale, due app). I temi di governance sono stati spostati in un registro dedicato (GOV-01…GOV-21) per decisione di Cristian del 25/09.
- **Giro d'acquisto (p.84-87)**: ordini mai fatturati sulle righe, da maggio 2026 mai ricevuti; ordini aperti per merce già entrata da pulire prima dell'MRP; rivalutazione dei carichi a costo zero da decidere con il commercialista; possibile obbligo di scritture ausiliarie di magazzino. Demo del flusso standard del 08/10 e guida per l'amministrazione.
- **Pilota (p.80-83)**: costo del terzista a zero nel modello v006, regola di consuntivazione delle fasi con scarto (Manuale dove si dichiara lo scarto), righe di distinta fantasma da correggere nei pacchetti, trasferimento al terzista con l'app Subcontracting da provare.
- **Aggiornamenti dal 08/10 al 27/10** ([[velo-ce-stato-progetto-99-log-revisioni]]): §7.1 p.12 — 09/10 confermata la ripartenza di BC in Premium su un tenant nuovo con partenza al 01/01/2027; 15/10 confermata l'opzione 3 (ambiente nuovo senza storico, BC di oggi nel tenant So Smart fino al bilancio 2026) con avvio subito su una società di prova nel tenant BlueAge, CT-01 chiuso; 15/10 sera ripresa dei saldi affidata a So Smart tranne gli articoli ([[velo-ce-articoli-codici-nuovi]]); 20/10 tenant unico `velo-ce.eu`.
- §7.4: p.34 e p.47 (21/10) D22 chiusa, conto lavoro solo sugli ordini di produzione con l'app Microsoft «Subcontracting»; nuovo p.89 (26/10) sugli impatti contabili della nuova operatività con orientamento di Cristian per il modello «per natura» dal 01/01/2027, da confermare con il commercialista prima del 13/11, metodo di valutazione (FIFO o medio ponderato) ancora aperto; nota del 26/10 sera sulla proposta dei conti delle nuove categorie per Claudia (OP-47).
- **p.89, 28/10 (025.113)**: orientamento BlueAge chiuso (D-01): nel 2027 il flag «Reg. automatica costi» resta spento e il magazzino non entra in contabilità, per il lavoro in più che darebbe a Claudia; supera l'orientamento dell'08/10; da presentare a Stefano; accensione dal 01/01/2028 dopo una prova in sandbox. Conseguenza: i conti del ciclo d'acquisto restano quelli di oggi e cade per il 2027 la domanda al commercialista «per natura o costo del venduto» ([[velo-ce-contabilita-di-magazzino-attivita-di-claudia-con-il-flag-acceso-e-spento-interno]]).
- **p.89, 28/10 sera (025.115)**: il Setup registrazioni COGE arriva «come oggi» con le riprese dati di So Smart, ma non ha righe per le categorie del master nuovo e non è mai stato usato per gli acquisti; scelta D-09 fra conti per area, per natura o via di mezzo nel file per Claudia, orientamento di Claude per area nel 2027 ([[velo-ce-conti-acquisti-per-natura-o-per-area-cliente]]).
- **p.84, 24-28/10 (025.114)**: costi accessori d'acquisto chiusi con l'incontro con Claudia del 27/10 (due addebiti TRASP e DAZI, transitorio dogana verificato); conti del ciclo d'acquisto mappati per sei scenari e provati in sandbox ([[velo-ce-conti-del-ciclo-dacquisto-per-scenario-interno]]).
- **Nuovo p.90 «Anticipi ai fornitori extra-UE e cambi» (025.114-025.119)**: oggi anticipi su 03038110 senza fornitore (saldo circa 2,02 milioni al 27/10) e differenze di cambio a mano; per indicazione di Cristian (29/10) l'anticipo si traccia sul fornitore con la categoria alternativa ANT, provata in sandbox con collegamento alla fattura e differenza di cambio calcolata da BC; la rettifica cambi rivaluta anche gli anticipi aperti e non li esclude: decide il commercialista ([[velo-ce-setup-anticipi-fornitori-so-smart]]).

## Numeri

- 87 punti nel §7.4; 23 punti tecnici in 7.2; 9 domande di business in 7.3; 47 domande nell'elenco operativo.
- Premium: +78 euro al mese per 3 utenti (+936 euro l'anno) a listino.
- Fattura elettronica: dati garantiti 45 giorni dall'intermediario (90 via API); circa 1,1 GB di storico EOS in BC; sanzione per autofatture tardive 2 euro a documento, massimo 400 euro al mese.
- Trasferimento di ambiente: fermo tipico entro 30 minuti, accettazione entro 8 ore.
- Licenza di consultazione del vecchio BC: circa 69 euro al mese più abbonamenti EOS.
- Piano nuovo ambiente: 185 attività (BlueAge 80, cliente 76, da decidere 14, So Smart 9, altri 6).
- Ordine AOR26-0011: 400 motori aperti mentre la merce risulta già caricata.
- Soglie scritture ausiliarie di magazzino: 5,16 milioni di ricavi e 1,03 milioni di rimanenze per due esercizi.

## Decisioni e azioni

- 23/09: D12 decisa, Premium.
- 25/09 (Cristian): temi di governance fuori dal filone principale, in un registro dedicato.
- 26/09 (Cristian): il restore, se servisse, lo esegue So Smart; tema interno.
- 29/09 (Cristian): l'app «CRM» esce dal documento per Velo-CE sulle app So Smart; verifica dell'URI rinviata.
- 30/09 sera: definita con Stefano e Claudia la direzione del tenant unico.
- 01/10: Stefano ha chiesto a EOS una licenza Premium (prova o acquisto da chiarire).
- 02/10 (Cristian): la fiscalità rientra nel perimetro per gli impatti del cambio tenant; assunto di lavoro: conto lavoro gestito fuori da BC.
- 04/10 (Cristian): domande a So Smart in una lista snella (Q25-Q32) per la call del 06/10.
- 05/10 (Stefano): le rimanenze di bilancio non arrivano dal modulo EOS (I01 chiusa).
- 07/10: orientamento alla reimplementazione da zero nel nuovo tenant.
- [ ] Chiudere le assunzioni sulla fattura elettronica FE1-FE6 (contratto Able Tech e conservazione con l'amministrazione, il resto con So Smart).
- [ ] Ottenere per iscritto da So Smart la copertura di app fiscali, connettori e AMS in Premium.
- [ ] Definire con il commercialista metodo dei saldi d'apertura, taglio, conservazione dei registri e obbligo delle scritture di magazzino.
- [ ] Decidere la data della conta di fine anno (AFC-OP40) e le fatture differite di dicembre (AFC-OP41).
- [ ] Chiarire con l'amministrazione perché da aprile 2026 si carica con il giornale e perché le fatture non si agganciano ai carichi.
- [ ] Pulire gli ordini d'acquisto aperti per merce già entrata prima di qualunque calcolo MRP.
- [ ] Decidere con Stefano la messa in sicurezza dell'app «CRM» (permessi non usati, segreto vecchio, utenza dedicata al canale).
- [ ] Rischi dell'avvio: settimana 01-08/01/2027 (giacenze negative e carico d'apertura con l'inventario dell'08/01) e due BC che inviano allo SdI con la stessa partita IVA fino al 15/01.
- 09/10: BC riparte in Premium sul nuovo tenant, partenza 01/01/2027 (Cristian).
- 15/10: opzione 3 per il nuovo tenant, avvio su società di prova BlueAge; CT-01 chiuso.
- 20/10: tenant unico `velo-ce.eu` (Cristian, confermato da Stefano).
- 21/10: D22 chiusa, conto lavoro con l'app Microsoft «Subcontracting».
- [ ] Conferma del commercialista sul modello contabile «per natura» 📅 2026-11-13 ([[velo-ce-stato-progetto-99-log-revisioni]])

## Versioni

- velo-ce-stato-progetto-03-decisioni-aperte.md · 2026-10-08 · prima versione ingerita (stato progetto 025.66); data di modifica della riorganizzazione della cartella
- velo-ce-stato-progetto-03-decisioni-aperte.md · 2026-10-28 · stato progetto 025.109 del 27/10; p.12 su tenant e opzione 3, D22 chiusa, p.89 sul giro contabile (differenze ricavate dal log revisioni, blocco non riletto per intero); copia della cartella in `Cristian/`
- velo-ce-stato-progetto-03-decisioni-aperte.md · 2026-10-29 · stato progetto 025.119; p.89 (magazzino fuori dalla contabilità nel 2027, conto acquisti per natura o per area), p.84 (costi accessori chiusi, conti per scenario) e nuovo p.90 (anticipi ai fornitori extra-UE e cambi); aggiornato dalle righe del log revisioni, blocco non riletto per intero
