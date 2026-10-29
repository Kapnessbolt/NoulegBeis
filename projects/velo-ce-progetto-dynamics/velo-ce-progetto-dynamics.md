---
type: project
status: attivo
role: "Non coinvolto: seguono Cristian Schifone e Leonardo Pinsone"
clients: ["[[velo-ce]]"]
people: ["[[cristian-schifone]]", "[[leonardo-pinsone]]", "[[stefano-moruzzi]]", "[[claudia-crippa]]", "[[gabriele-ranzini]]"]
updated: 2026-10-29
---

# Velo-CE · Progetto Dynamics

## Stato

- Non è un'implementazione da zero: si riconduce allo standard un Business Central in uso dal 2023, installato da So Smart (gruppo EOS) in Essentials con 3 utenti; dall'8/09 il baricentro è anche la governance di sistemi e fornitori ([[velo-ce-stato-progetto-01-inquadramento-ambiente]])
- Esigenza numero uno del cliente: avere sempre i materiali; marginalità e reportistica rimandate al 2027 ([[velo-ce-stato-progetto-02-cantieri-dominio]])
- Cantieri 0–8: analisi giacenze, anagrafiche, codifica saldatura, distinte, giro materiali, acquisti centralizzati, MRP (Essentials) e produzione (Premium), costificazione, controllo di gestione nel 2027 ([[velo-ce-stato-progetto-02-cantieri-dominio]])
- Al SAL del 6/10: chiusi analisi e mappa dei 34 cantieri, decisione Premium, regole del giro materiali, rilievi in reparto e prime prove; in corso pilota telaio Lungo, confronto fra partner, giro contabile e fiscale; percorso critico codifica → articoli → distinte ([[velo-ce-sal-01-cliente]])
- Il 5/10 è emerso che il magazzino in Business Central non è alimentato dal ciclo passivo: fatture d'acquisto su conto contabile dal 2023, carichi manuali spesso a costo zero (669 articoli su 1.112), rimanenze di bilancio rilevate fuori dal sistema ([[velo-ce-giro-reale-dei-materiali-in-bc-interno]])
- Pilota telaio Lungo (bici Multi Lungo Bosch) provato in sandbox il 28/09: riusciti lotto laser, telaio sabbiato con distinta fantasma e conto lavoro su due colori; da risolvere il costo della verniciatura che non entra nel telaio ([[velo-ce-pilota-bc-lungo-bosch-demo-sbx-studio]])
- Quotazione BlueAge dei blocchi 1–3: 98.000 € a corpo (147,5 giornate previste); programma complessivo di circa 408 giornate ([[velo-ce-mappa-cantieri-dynamics]])
- Piano del nuovo ambiente: 185 attività (80 BlueAge, 76 cliente, 9 So Smart), 32 sul percorso critico, tutte da fare al 7/10; registro con 69 open point aperti, 31 ad alta priorità ([[velo-ce-piano-attivita-nuovo-ambiente-interno]], [[velo-ce-open-point-interno]])
- Rischio bloccante per il go-live: la fattura elettronica, perché lo standard non trasmette allo SdI e il framework e-documents arriva solo con la wave 1 del 2027 ([[velo-ce-open-point-interno]])
- Rischi principali: il canale ordini MMI usa il numero articolo come chiave e gira con l'identità del titolare, quindi ricodifica o cambio credenziali lo fermano ([[velo-ce-registro-temi-di-governance-interno]]); sviluppi So Smart senza documentazione né codice e nessun amministratore interno del tenant ([[velo-ce-sal-01-cliente]]); nessuna sandbox libera per le prove ([[velo-ce-checklist-finestra-di-rilascio-interno]])

## Attività

- [x] Chiedere a Cristian di rinominare su SharePoint la cartella `01 - Velo-CE/Cristian/` in `Progetto Dynamics`, senza cancellarla né copiarla: oggi è l'unica copia del progetto, e il nome nuovo tiene gli stessi ID dei file. Le note del vault restano sotto Progetto Dynamics (dall'utente) 📅 2026-10-31 ✅ 2026-10-29 ([[2026-10-29]], [[2026-10-29-cockpit-conteggi-e-step-13]])
- [ ] Scelta della strada verso Premium e del partner, regola di codifica 📅 2026-10-30 ([[velo-ce-sal-01-cliente]], [[velo-ce-piano-attivita-nuovo-ambiente-interno]])
- [ ] Sandbox Premium e nome definitivo della società (irreversibile) 📅 2026-10-31 ([[velo-ce-piano-attivita-nuovo-ambiente-interno]])
- [ ] Regola di taglio fiscale e saldi d'apertura decisi con il commercialista, piano dei conti e metodo di costo 📅 2026-11-13 ([[velo-ce-piano-attivita-nuovo-ambiente-interno]])
- [ ] Prima prova di ripresa dati con i dati al 31/10, a fine novembre 📅 2026-11-30 ([[velo-ce-piano-ripresa-dati-interno]])
- [ ] Prova della fattura elettronica e distinte del rilascio R1 📅 2026-12-04 ([[velo-ce-piano-attivita-nuovo-ambiente-interno]])
- [ ] Prove end-to-end e collaudo utente 📅 2026-12-11 ([[velo-ce-piano-attivita-nuovo-ambiente-interno]])
- [ ] Prova generale e piano di cut-over 📅 2026-12-18 ([[velo-ce-piano-attivita-nuovo-ambiente-interno]])
- [ ] Go/no-go 📅 2027-01-07 ([[velo-ce-piano-attivita-nuovo-ambiente-interno]])
- [ ] Ottenere da So Smart la conferma scritta sulla copertura di app fiscali, connettori e AMS in Premium ([[velo-ce-stato-progetto-06-fornitori-perimetro]])
- [ ] Decidere con Claudia Crippa e Stefano Moruzzi il giro d'acquisto standard prima di MRP e Premium ([[velo-ce-giro-reale-dei-materiali-in-bc-interno]])
- [ ] Chiedere al commercialista se servono scritture ausiliarie di magazzino ([[velo-ce-giro-reale-dei-materiali-in-bc-interno]])
- [ ] Mettere in sicurezza l'app "CRM" usata dal canale ordini, con Stefano Moruzzi ([[velo-ce-stato-progetto-03-decisioni-aperte]])
- [ ] Spiegare la rettifica di magazzino MAG26-0266 da −491.400 € ([[velo-ce-stato-progetto-02-cantieri-dominio]])
- [ ] Piano AFC pronto per il go-live: piano dei conti con un conto per banca, setup IVA, intermediario SdI, ciclo acquisti collegato 📅 2027-01-01 ([[velo-ce-piano-afc-interno]])
- [ ] Inventario d'apertura e avvio del rilascio R1 📅 2027-01-08 ([[velo-ce-sal-01-cliente]])
- [ ] Fatturare i DDT di dicembre 2026 📅 2027-01-15 ([[velo-ce-piano-afc-interno]])
- [ ] Portare Production alla versione 29.0 📅 2027-03-01 ([[velo-ce-procedura-rilascio-ripristino]])
- [x] V1 Make-to-Order nello stesso ordine di produzione o in ordini collegati (Cristian) 📅 2026-09-21 ✅ 2026-10-23 ([[il-giro-del-telaio-in-essential-e-in-premium-documento-interno-v001]])
- [x] V2 proposta a cascata su due livelli in Essential, prova D17 (Cristian) 📅 2026-09-21 ✅ 2026-10-23 ([[il-giro-del-telaio-in-essential-e-in-premium-documento-interno-v001]])
- [x] V8 chiedere in sede chi registra i 571 ordini di assemblaggio (Leonardo) 📅 2026-09-21 ✅ 2026-10-23 ([[velo-ce-il-giro-del-telaio-in-essential-e-in-premium]])
- [ ] Verificare autorizzazioni e privacy per usare i dati Velo-CE come vetrina delle automazioni (Cristian) ([[riunione-generale-blueage-19-10-sintesi-azioni-e-one-page]])
- [ ] Cercare su SharePoint o OneDrive il foglio quotazione blocchi (citato nel vault ma non ingerito) e ingerirlo con /ingest-file ([[2026-10-28-verifica-task-28-10]])
- [ ] Conferma del commercialista sul modello contabile «per natura» per l'avvio del 01/01/2027 📅 2026-11-13 ([[velo-ce-stato-progetto-03-decisioni-aperte]])
- [ ] Preparare l'Excel delle combinazioni bici con le soglie di codifica, da far decidere a Stefano ([[velo-ce-verbale-consegna-codifica-bici-etichettatura]])
- [ ] Chiedere allo sviluppatore del portale B2B una riga per bici con riferimento del cliente e numero del portale ([[velo-ce-verbale-pianificazione-giro-bici-gennaio]])
- [ ] Far mandare da Stefano a So Smart la mail per l'abbonamento sul nuovo tenant e fissare la call di attivazione ([[velo-ce-verbale-demo-product-configurator]])
- [ ] Dividere con So Smart il setup di base e di magazzino del nuovo ambiente prima che parta ([[velo-ce-verbale-demo-product-configurator]])
- [ ] Inviare a We Make Code l'Excel vecchi → nuovi codici e la regola del codice bici 📅 2026-11-05 ([[velo-ce-verbale-integrazioni-we-make-code]])
- [ ] Far decidere a Stefano se Van Nicholas entra nella ricodifica 📅 2026-10-30 ([[velo-ce-articoli-codici-nuovi]])
- [ ] Preparare la tabella di raccordo vecchi → nuovi codici articolo 📅 2026-12-04 ([[velo-ce-articoli-codici-nuovi]])
- [ ] Far confermare a Claudia i conti delle nuove categorie di registrazione articolo (OP-47) ([[velo-ce-proposta-conti-categorie-articolo-cliente]])

## Decisioni

- 2026-09-23 · Velo-CE passa a Business Central Premium per gestire la produzione con le funzioni standard (decisione D12 di Stefano Moruzzi) ([[velo-ce-stato-progetto-03-decisioni-aperte]])
- 2026-09-23 · Ricodifica ibrida per famiglia di articoli ([[velo-ce-stato-progetto-02-cantieri-dominio]])
- 2026-09-27 · Pilota: un pezzo è articolo solo se va a scorta, verniciatura in conto lavoro, costo FIFO ([[velo-ce-pilota-bc-lungo-bosch-fetta-telaio-verniciato-nota-per-trif]])
- 2026-09-29 · Razionalizzazione delle 54 app EOS: 7 in uso, 16 da togliere; IVC sostituito dalla valutazione standard dopo la chiusura 2026 ([[velo-ce-app-eos-quali-servono-so-smart]])
- 2026-09-30 · Strada B: nuovo Business Central Premium nel tenant della posta, partenza 1/1/2027 con il perimetro amministrativo e commerciale, produzione dopo ([[velo-ce-verbale-strada-premium-tenant-unico]])
- 2026-09-30 · Catena del telaio codificata per intero; distinta di produzione per il telaio, di assemblaggio per la bici; tracciabilità di lotti e serie in Veloce-CRM ([[velo-ce-verbale-giro-materiali-pilota-lungo]])
- 2026-10-05 · Orientamento: niente big bang, avvio senza cicli di dettaglio, prima la bici completa, ciclo acquisti subito ([[velo-ce-verbale-rilasci-giacenze-ciclo-acquisti]])
- 2026-10-06 · Le strade diventano tre (restare con So Smart su Essentials, Premium con un partner EOS, Premium con un altro partner) e la scelta slitta al 30/10 ([[velo-ce-sal-01-cliente]])
- 2026-10-07 · Orientamento a reimplementare da zero nel tenant veloe.eu ([[velo-ce-stato-progetto-03-decisioni-aperte]])
- Aperte: reimplementare o trasferire l'ambiente; taglio e saldi d'apertura con il commercialista; costo standard o FIFO sui fabbricati; ordini manuali o MRP all'avvio; data della conta di fine anno ([[velo-ce-stato-progetto-03-decisioni-aperte]], [[velo-ce-verbale-guida-anagrafica-ondate-mrp]])

## Prossimi passi

- Rilasci mensili dopo l'avvio: R2 a febbraio, R3 a marzo, R4 ad aprile, da maggio cicli e pianificazione completa
- Vecchio Business Central consultabile fino all'approvazione del bilancio 2026

## Fonti

- Stato progetto: [[velo-ce-stato-progetto]], [[velo-ce-stato-progetto-01-inquadramento-ambiente]], [[velo-ce-stato-progetto-02-cantieri-dominio]], [[velo-ce-stato-progetto-03-decisioni-aperte]], [[velo-ce-stato-progetto-04-backlog]], [[velo-ce-stato-progetto-05-stato-info-quotazione]], [[velo-ce-stato-progetto-06-fornitori-perimetro]], [[velo-ce-stato-progetto-99-log-revisioni]]
- Piani: [[velo-ce-mappa-cantieri-dynamics]], [[velo-ce-piano-di-progetto-per-cantieri]], [[velo-ce-piano-attivita-nuovo-ambiente-interno]], [[velo-ce-piano-ripresa-dati-interno]], [[velo-ce-open-point-interno]], [[velo-ce-piano-afc-interno]]
- Deck cliente: [[velo-ce-sal-01-cliente]], [[velo-ce-business-central-oggi-e-la-strada-verso-premium-cliente]], [[velo-ce-progetto-dynamics-e-power-bi-la-strada-verso-premium]], [[velo-ce-sintesi-evidenze-e-metodo-cliente]], [[velo-ce-app-so-smart-che-cosa-serve-cliente]]
- Verbali: [[velo-ce-verbale-censimento-app-eos]], [[velo-ce-verbale-strada-premium-tenant-unico]], [[velo-ce-verbale-giro-materiali-pilota-lungo]], [[velo-ce-verbale-avvio-gennaio-senza-cicli]], [[velo-ce-verbale-rilasci-giacenze-ciclo-acquisti]]
- Tutte le fonti del progetto si trovano in `sources/sharepoint/delivery/customers/01-velo-ce/`
- [[il-giro-del-telaio-in-essential-e-in-premium-documento-interno-v001]]
- [[riunione-generale-blueage-12-10-punti-emersi-e-prossimi-passi]]
- [[riunione-generale-blueage-5-10-sintesi-e-azioni]]
- [[velo-ce-il-giro-del-telaio-in-essential-e-in-premium]]
