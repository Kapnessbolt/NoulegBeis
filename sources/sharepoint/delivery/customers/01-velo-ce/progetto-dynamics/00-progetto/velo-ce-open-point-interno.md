---
type: source-doc
source: sharepoint
family: velo-ce-open-point-interno
current:
  item_id: 01EFCYUZ76445RDSDIRNBYDZ4OUDA5XCPG
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ76445RDSDIRNBYDZ4OUDA5XCPG
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/00 Progetto/Velo-CE - Open point - INTERNO - v002.xlsx
  name: Velo-CE - Open point - INTERNO - v002.xlsx
  last_modified: 2026-10-27T15:11:01Z
versions:
  - { name: "Velo-CE - Open point - INTERNO - v002.xlsx", item_id: 01EFCYUZ76445RDSDIRNBYDZ4OUDA5XCPG, last_modified: 2026-10-27T15:11:01Z }
  - { name: "Velo-CE - Open point - INTERNO - v002.xlsx", item_id: 01EFCYUZ4AKKEZ6TRXIRH2XWAVNC2P5YRO, last_modified: 2026-10-05T21:58:41Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-29T05:59:50Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]", "[[fatturazione-elettronica-sdi]]"]
tags: [open-point, to-do, cambio-tenant, premium, fattura-elettronica, registro, interno]
---

# Velo-CE · Open point di progetto (INTERNO)

## Riassunto

Registro vivo degli open point del progetto Velo-CE (v002 del 02/10/2026, aggiornato sul posto fino al 27/10), non mostrabile al cliente né a So Smart. Le voci CT raccolgono i punti aperti del passaggio di Business Central nel tenant di Velo-CE (direzione del tenant unico del 30/09), sia con trasferimento dell'ambiente sia con reimplementazione in Premium; le voci OP gli altri punti di progetto. Ogni voce ha certezza, evidenze, strada, chi decide ed esegue, priorità e scadenza logica. Il foglio To-do traccia le azioni sui documenti (TD-001…TD-022) e un riepilogo conta le voci aperte per area e priorità.

## Punti chiave

- **Decisione (b) ancora aperta** (CT-01): trasferire l'ambiente attuale o reimplementare da zero in standard Premium. Proposta del 29/09: reimplementazione con perimetro minimo al 01/01/2027 se le condizioni 1-3 si chiudono entro metà ottobre. Il 05/10 verso l'esterno la strada è stata presentata come «nuovo tenant, scatola vuota»: narrazione da allineare.
- **Piattaforma e licenze**: amministrazione del tenant della posta veloe.eu non chiarita (CT-02, CT-03); quota ambienti piena (1 Production + 3 sandbox); le sottoscrizioni non si spostano fra tenant, in quello nuovo vanno comprate le Premium (CT-06); licenza Premium chiesta da Stefano a EOS da rileggere (CT-07).
- **Partner e AMS** (CT-09, CT-42): Microsoft non fa AMS; So Smart dichiara di non avere competenze Premium; il 05/10 EOS non prende clienti Premium per quattro licenze; sondati due fornitori alternativi per app fiscali, API e AMS (piano B), in contrasto con l'intenzione del titolare di tenere So Smart.
- **App EOS e So Smart**: 54 app EOS, razionalizzate il 29/09 in 7 in uso, 20 componenti, 11 da chiarire, 16 senza ruolo; certificazione Premium 12 sì e 42 da verificare (CT-13). EX001 Accruals candidata all'uscita; pacchetto So Smart (flusso MMI, dispatcher SOSMART, Connettore WMS) da verificare nel nuovo tenant (CT-11); abbonamenti EOS legati al Tenant ID (CT-10).
- **Fattura elettronica (vincolo bloccante)**: senza EX063 al go-live non si fattura; il framework e-documents standard per lo SdI è previsto per la 2027 release wave 1, non pronto al 01/01/2027 (CT-20). Aperti conservazione a norma IX-CE (CT-16), intestatario del contratto Able Tech (CT-17), indirizzo telematico registrato (CT-18), processo che oggi invia e importa con utenze personali (CT-19), progressivo del nome file SdI (CT-21), fatture a cavallo del passaggio e differite di dicembre (CT-22, CT-24).
- **Altri adempimenti**: taglio a inizio esercizio da confermare con il commercialista (CT-26); serie e registri IVA (CT-27); plafond (CT-28); CU, LIPE, ratei e risconti (CT-29…CT-31); valutazione fiscale del magazzino IVC, con proposta di passare alla Fiscal Inventory Valuation standard dopo la chiusura 2026 (CT-32).
- **Conto lavoro fuori da BC**: nessuna verniciatura registrata in BC nel 2026; assunto di lavoro che il conto lavoro passi da Fatture in Cloud (CT-25), con impatto sul costo del telaio verniciato.
- **Integrazioni e utenze**: app Entra «CRM» e canale ordini MMI da ricostruire (CT-33, CT-34), 25 servizi web EOS senza chiamante noto (CT-35), Power BI (CT-36), processi su utenze personali e 16 voci della coda processi (CT-37, CT-38).
- **Go-live e rilasci** (CT-40): il 05/10, con il titolare, niente big bang al 01/01 («l'azienda non lo regge»), rilasci per gradi (gennaio, marzo, giugno); gradini per gennaio sui verniciati, sabbiati e parti del sabbiato; partenza al 01/01 o dalla data dell'inventario. Vecchio tenant consultabile fino all'approvazione del bilancio 2026 (CT-41).
- **Telaio e produzione**: regola di codifica definitiva da fissare (OP-10, circa 180 componenti); avvio con ordini manuali e poi MRP (OP-20); registrazioni in reparto (OP-21); tariffe delle postazioni senza dati reali (OP-22); scarto di default (OP-23); verniciatura interna in arrivo da chiarire (OP-26); avvio a gennaio senza cicli, con ciclo unico (OP-27); taglio laser di più articoli dallo stesso foglio (OP-29).
- **Ciclo acquisti** (OP-28): proposta di partire entro circa 15 giorni dal 05/10 con ordine, entrata merci e chiusura; cautela BlueAge a farlo nel Production attuale.
- **Piano** (OP-01, OP-02): piano Excel da costruire; tappe del 30/09: prova nel tenant della posta fino a dicembre, partenza al 01/01/2027, poi produzione e pianificazione; UAT da organizzare.
- **Aggiornamenti fino al 27/10**: CT-01 chiuso il 15/10 con l'opzione 3 (ambiente nuovo, società nuova senza storico) e tenant unico `velo-ce.eu` dal 20/10 ([[velo-ce-stato-progetto-03-decisioni-aperte]]); dai verbali del 21-22/10 nuove voci OP-41 e seguenti; OP-45 prova del modello contabile «per natura»; OP-46 fattori di conversione stimati nel master articoli v005 (tubi e lamiere, lamiere in metri senza l'unità foglio); OP-47 conti delle nuove categorie articolo, proposta v001 per Claudia (Alta); OP-48 unità di stockkeeping per colore, domanda a Stefano: la prova del 27/10 mostra che il colore senza SKU è pianificato dalla domanda dell'assemblaggio.

## Numeri

- Riepilogo al 27/10: 91 voci, 87 aperte (43 alta, 36 media, 8 bassa); le aree più cariche sono telaio e produzione (15), dati e cut-over (14), app EOS e So Smart (11), fattura elettronica (10); per scadenza 8 per la decisione (b), 13 per la call con So Smart, 52 prima del go-live, 7 al cut-over, 2 dopo il go-live. To-do aperte 88 (32 alta), di cui 27 da portare nel piano e 16 domande.
- Al 05/10: 71 voci, 69 aperte; to-do aperte 19.
- Canone So Smart 768 euro al mese contro circa 270-300 euro di licenze Microsoft (OP-04, dichiarato).
- Fattura elettronica: FTE con 512.788 righe (circa 1,1 GB); storico circa 4.400 documenti in uscita e 7.900 in entrata; dati IX-FE garantiti 45 giorni (90 via API); job EOS IXFE in errore dal 21/04/2024; 9 fatture passive su 12 dell'export arrivano con il codice di Fatture in Cloud.
- Differite di dicembre 2026 da emettere entro il 15/01/2027; conservazione per almeno 10 anni.
- Coda processi: 16 voci, 6 SOSMART, MMI ogni 2 minuti, 4 in errore da oltre due anni; So Smart System con 336 righe di permessi propri.
- Accruals: 140 movimenti, tutti di gennaio 2023; EX065 usato 4 volte nel 2026.
- Prova di trasferimento: accettazione entro 8 ore; prova EOS di 20 giorni.

## Decisioni e azioni

- Decisione (30/09): direzione del tenant unico, condivisa con il titolare e l'amministrazione.
- Decisione (02/10, Cristian): la fiscalità rientra nel perimetro del cambio tenant; il file è un registro vivo senza nuove versioni.
- Decisione (27/09): nessuna utenza SUPER da chiedere a So Smart (OP-12, chiuso); nessuna nuova richiesta di accesso per ora.
- Decisione (29/09): il canone So Smart resta fuori dalla call con So Smart.
- Orientamento (05/10): niente big bang, rilasci per gradi, partenza senza cicli di dettaglio, ciclo acquisti da subito.
- [ ] Allineamento interno prima della call con So Smart del 06/10 su narrazione del tenant, fornitori alternativi e dati da non dare per certi (TD-014) 📅 2026-10-06
- [ ] Costruire il calendario dei rilasci (01/01 o inventario, marzo, giugno) da discutere con il titolare (TD-019)
- [ ] Preparare la procedura del ciclo acquisti per chi fa gli ordini (TD-020)
- [ ] Provare in sandbox Premium ciclo unico contro assemblaggio, proposte del piano e famiglia di produzione (TD-022)
- [ ] Pianificare le sessioni sulla codifica di telaio e bici completa (TD-021)
- [ ] Preparare la sessione con il reparto dal sabbiato all'assemblaggio, obiettivo tutte le anagrafiche entro dicembre (TD-008)
- [ ] Informare il commercialista: chiusura 2026 nel BC attuale, partenza al 01/01/2027 con saldi e partite aperte (TD-009)
- [ ] Chiarire chi è lo sviluppatore del portale B2B e come porta le interfacce (TD-006)
- [ ] Ricontattare il fornitore alternativo con il perimetro di app fiscali, connettori e AMS (TD-012, TD-013)

## Versioni

- Velo-CE - Open point - INTERNO - v002.xlsx · 2026-10-05 · prima versione ingerita; v002 del 02/10 aggiornata sul posto fino al 05/10 (CT-42, OP-25…OP-29, TD-012…TD-022)
- Velo-CE - Open point - INTERNO - v002.xlsx · 2026-10-27 · registro aggiornato sul posto fino al 27/10 (OP-45…OP-48), 87 voci aperte su 91 e 88 to-do aperte (letti Leggimi e Riepilogo); nella cartella `Cristian/00 Progetto/`

