---
type: project
status: attivo
role: "Project manager e sviluppatore del prodotto, insieme a Cristian Schifone"
clients: ["[[adac-bologna]]", "[[solera]]", "[[assoricambi]]", "[[qricambi]]"]
people: ["[[cristian-schifone]]", "[[luca-degli-esposti]]", "[[claudio-degli-esposti]]"]
updated: 2026-10-26
---

# Parts Radar · sviluppo e pilota

## Stato

- Lorenzo Curione è project manager e sviluppatore del prodotto [[parts-radar]] insieme a [[cristian-schifone]] ([[2026-10-22-primo-caricamento-shared-documents-onedrive]]); tiene i contatti con fornitori e partner ([[ws-demo-blue-age]]). Nel repo Lorenzo ha l'ultima parola su pipeline, modelli e prompt, Cristian su database, infrastruttura e dati ([[2026-10-23-fonte-github-parts-radar]])
- Parts Radar è un middleware B2B per l'aftermarket indipendente: dal meccanico al ricambista arrivano foto della targa e richiesta a voce o per iscritto, il sistema riconosce il veicolo e propone il ricambio originale e le alternative compatibili; si affianca a qualunque gestionale ed è pensato per più ricambisti ([[presentazione-e-sintesi-progetto]], [[integrazione-api-qricambi-proposta-di-collaborazione]])
- Sviluppo nel repo GitHub [cristian-schifone/parts-radar](https://github.com/cristian-schifone/parts-radar); il vault ne legge stato, decisioni aperte, costi, piano del pilot e changelog con il task `ingest-github` ([[2026-10-23-fonte-github-parts-radar]])
- Step 1 in costruzione: il sistema identifica veicolo e pezzo e propone gli articoli, l'operatore valida, ordina e risponde a mano. Step 2 (ordine sul portale del fornitore) e Step 3 (aggiornamento del gestionale) non iniziati ([[parts-radar-architettura]])
- Dal 26/09/2026 il prodotto è un servizio Python + PostgreSQL + dashboard, un'installazione per cliente sui server BlueAge: n8n è uscito perché la sua licenza ammette solo uso interno. Migrazione chiusa in sviluppo tra il 02 e il 05/10 ([[parts-radar-decisione-stack-python]])
- Filiera: [[solera]] (Kromeda) per i dati veicolo e ricambi, con il catalogo che parte dal codice originale e scende agli equivalenti aftermarket; [[assoricambi]] come associazione che sostiene il progetto; [[adac-bologna]] come ricambista pilota; [[qricambi]] per prezzi netti e disponibilità ([[presentazione-e-sintesi-progetto]], [[parts-radar-aggiornamento-api-test]], [[integrazione-api-qricambi-proposta-di-collaborazione]], [[parts-radar-kromeda-impatto]])
- Kromeda: demo prorogata da Solera il 16/10 fino a circa il 18/11; 17 crediti targa al 21/10. Il VIN via REST non arriva prima di gennaio 2027: i casi che lo richiedono restano al banco su PartsLink24 ([[parts-radar-architettura]], [[parts-radar-issue-379]], [[parts-radar-kromeda-fase0-risultati]])
- Fase 0 sulla demo (20 targhe, 1.847 casi): 80% risolto in modo deterministico, 86% con i default, 14% all'operatore; articolo corretto raggiungibile in 43 richieste su 51 del golden set di ADAC ([[parts-radar-kromeda-fase0-risultati]])
- Costi Kromeda stimati: circa 2.300 chiamate al giorno (picco 3.500, la fascia da chiedere per il pilot) e 2.200-2.600 crediti targa al mese; i prezzi sono ancora da avere da Solera ([[parts-radar-kromeda-impatto]])
- WhatsApp: per il pilot 360dialog con la Coexistence (19/10), che lascia il numero di ADAC sull'app del banco; Twilio escluso il 20/10. Da scegliere il piano Regular (49 €/mese) o Partner (da 250 €/mese) prima di attivare il numero. I gruppi WhatsApp (3 clienti ADAC su 10) non arrivano all'API con nessun fornitore ([[parts-radar-whatsapp-fornitori]])
- Al 22/10: chat del banco nella dashboard con invio WhatsApp, router in ingresso acceso (separa i messaggi che non chiedono un pezzo), modalità ascolto con catalogo dal vivo attivabile cliente per cliente; il servizio usa Claude Haiku 5.5 ([[parts-radar-changelog]], [[parts-radar-architettura]])
- Al 26/10 la settimana 1 del piano è quasi chiusa: le 810 etichette di sviluppo delle chat reali sono corrette e riviste con la misura del router (proposte perse da 12 a 7), i prompt di router ed estrazione sono congelati; restano le etichette del test (clienti E, G, H, J), la voce e la misura della targa dei pezzi aggiunti. I passi fuori dal codice sono fermi al 22/10 ([[parts-radar-issue-379]], [[parts-radar-changelog]])
- Piano del pilot rifatto il 21/10: traguardo il test reale del flusso intero (#420) con prova controllata verso il 04/11, ascolto sul numero di ADAC e traffico vero nella settimana 12-17/11, prima della fine della demo. Il report deve giustificare l'utenza Kromeda di produzione e dire quanto costa una richiesta ([[parts-radar-issue-379]], [[parts-radar-issue-420]])
- Al 12/10/2026: dashboard a buon punto e nuova banca dati prodotto quasi integrata; precisione circa 75% deterministica, 80% con i parametri della banca dati, 83–84% con criteri meno efficienti (da tenere come suggeriti); a gennaio il fornitore rilascia l'interrogazione per allestimento ([[riunione-generale-blueage-12-10-punti-emersi-e-prossimi-passi]])
- Qricambi: call del 05/10/2026 fatta; le API si possono integrare, ma l'accesso lo deve chiedere il ricambista, che è il cliente diretto di Qricambi. La documentazione delle API è già disponibile ([[2026-10-22-watermark-e-task-schedulati]])
- Obiettivo finale: un SaaS in cui ogni cliente attiva il proprio numero WhatsApp; il ricambista pilota sarebbe disposto, in modo informale, a pagare la banca dati (oggi circa 1 € a ricerca a crediti, che resterebbero come riserva) ([[riunione-generale-blueage-12-10-punti-emersi-e-prossimi-passi]])

## Attività

- [ ] Testare il web service demo Kromeda e aggiornare Solera sui risultati ([[ws-demo-blue-age]])
- [ ] Attendere da Solera la proposta ufficiale (API di validazione con ADAC, servizio a regime con pricing) ([[parts-radar-aggiornamento-api-test]])
- [ ] Riprendere il web service VIN testuale all'uscita della beta Kromeda, prevista fine settembre / ottobre 2026; secondo il repo il REST non arriva prima di gennaio 2027 📅 2027-01-15 ([[parts-radar-aggiornamento-api-test]], [[parts-radar-kromeda-fase0-risultati]])
- [ ] Riscontro da Assoricambi sul feedback di Kromeda / Collins e sui fornitori VIN per un ambiente di test ([[presentazione-e-sintesi-progetto]])
- [x] Verificare l'esito della call con Qricambi del 05/10 ([[integrazione-api-qricambi]], [[2026-10-22-watermark-e-task-schedulati]])
- [ ] Far chiedere l'accesso alle API Qricambi dal ricambista pilota ([[adac-bologna]]), già cliente Qricambi ([[2026-10-22-watermark-e-task-schedulati]])
- [x] Rispondere a Twilio sullo stack del webhook: superata, Twilio escluso il 20/10 ([[twilio-blueage-follow-up]], [[parts-radar-whatsapp-fornitori]])
- [ ] Contattare l'aggregatore degli accordi ricambisti-distributori per il confronto prezzi, con Cristian ([[riunione-generale-blueage-28-9-sintesi-e-azioni]])
- [ ] Capire da Solera come vende il servizio; la proroga della prova è arrivata il 16/10 (demo fino al ~18/11) 📅 2026-11-18 ([[riunione-generale-blueage-12-10-punti-emersi-e-prossimi-passi]], [[parts-radar-architettura]])
- [ ] Chiarire lo step del pilota 📅 2026-11-12 ([[riunione-generale-blueage-12-10-punti-emersi-e-prossimi-passi]])
- [ ] 360dialog: scegliere il piano Partner o Regular prima di attivare il numero di ADAC (percorso critico) ([[parts-radar-issue-379]], [[parts-radar-whatsapp-fornitori]])
- [ ] Ottenere da ADAC le foto delle officine ([[parts-radar-issue-379]])
- [ ] Registrare i numeri WhatsApp delle officine come clienti attivi ([[parts-radar-issue-379]])
- [ ] Ottenere il consenso di ADAC al trattamento dal vivo con i fornitori (LLM, trascrizione, 360dialog) ([[parts-radar-issue-379]])
- [ ] Cristian: server del pilot raggiungibile dal webhook e verifica del proxy ([[parts-radar-issue-379]])
- [x] Avvisare Cristian: invio WhatsApp acceso nello Step 1, migration 075-084, ascolto sul numero di ADAC, clienti da accendere uno per uno ✅ 2026-10-26 ([[parts-radar-issue-379]], [[parts-radar-changelog]])
- [ ] Kromeda di produzione: portare BlueAge sul piano commerciale con i risultati del test reale ([[parts-radar-issue-379]], [[parts-radar-issue-420]])
- [ ] Raccogliere le risposte di Luca alle domande del 22/10: officine e operatori da abilitare, gruppi WhatsApp, data del pilot, condizioni commerciali, Rihag/Cati, gestionale, brand preferiti e listini di ADAC (CONTINENTAL, DIPA, DEPO, Pierburg, AJUSA) ([[parts-radar-changelog]], [[parts-radar-issue-379]], [[parts-radar-architettura]])
- [ ] Mandare a Solera le domande aperte: cache oltre le 24 ore, versioni degli affini, dizionario delle voci, fasce e prezzi, URL delle foto ([[parts-radar-architettura]], [[parts-radar-kromeda-impatto]])
- [x] Avvisare Cristian: prompt di router ed estrazione cambiati e certificati emSign tolti dall'immagine del servizio; rebuild sullo staging alla prossima consegna ✅ 2026-10-26 ([[parts-radar-changelog]])
- [ ] Cristian: decidere le parti 3 e 4 della #447 (decisioni in file separati, archivio del changelog) ([[parts-radar-changelog]])
- [ ] Prova controllata del flusso intero 📅 2026-11-04 ([[parts-radar-issue-379]], [[parts-radar-issue-420]])
- [ ] Traffico vero di ADAC con le targhe e report dei risultati 📅 2026-11-17 ([[parts-radar-issue-379]], [[parts-radar-issue-420]])
- [ ] Avvisare Cristian per lo staging: trascrizione dei vocali (aggiornamento del DB prima del servizio nuovo, variabili nuove, chiave all'accensione) ed etichettatore; testo preparato, lo manda Lorenzo ([[parts-radar-changelog]])
- [ ] Lorenzo: creare il progetto Google a nome di BlueAge con un account di servizio per la trascrizione dei vocali, poi cancellare la chiave di prova sull'account personale ([[parts-radar-changelog]], [[parts-radar-architettura]])
- [ ] Lorenzo: cancellare dal dispositivo le pagine autonome e i file delle etichette del test (chat e vocali veri) ([[parts-radar-changelog]])

## Decisioni

- 2026-09-07 · Chiesta a Solera una proposta ufficiale per l'API di validazione con ADAC pilota e per il servizio a regime con pricing ([[parts-radar-aggiornamento-api-test]])
- 2026-09-26 · Parts Radar passa da n8n a un servizio Python e il catalogo da TecDoc a Kromeda; installazione per cliente sui server BlueAge (Lorenzo, ratificata da Cristian il 02/10) ([[parts-radar-decisione-stack-python]])
- 2026-09-29 · Con Qricambi niente dettagli confidenziali dell'idea, su sua richiesta: sviluppa da tre anni Quoting24, un prodotto simile ([[integrazione-api-qricambi-proposta-di-collaborazione]])
- 2026-10-05 · Integrazione delle API Qricambi: l'accesso passa dal ricambista, cliente diretto di Qricambi, non da BlueAge ([[2026-10-22-watermark-e-task-schedulati]])
- 2026-10-12 · Canale WhatsApp in "build" con webhook, senza personalizzazioni lato utente ([[twilio-blueage-follow-up]])
- 2026-10-12 · Per WhatsApp ci si appoggia a un tech provider esistente, senza diventare tech provider Meta ([[riunione-generale-blueage-12-10-punti-emersi-e-prossimi-passi]])
- 2026-10-19 · Fornitore WhatsApp del pilot: 360dialog con la Coexistence, così il banco non perde messaggi se il servizio è giù ([[parts-radar-whatsapp-fornitori]])
- 2026-10-20 · Twilio escluso: niente Coexistence, nessun reinvio, dati negli USA ([[parts-radar-whatsapp-fornitori]])
- 2026-10-21 · Piano del pilot: test in due tempi (prova controllata, poi traffico vero), modalità ascolto sul numero di ADAC, messaggi automatici ai clienti veri spenti finché il router non ha numeri ([[parts-radar-issue-379]], [[parts-radar-issue-420]])
- 2026-10-22 · Router in ingresso su Claude Haiku 5.5, scelto sulla misura: richieste false da 42 a 12 ([[parts-radar-changelog]])
- 2026-10-22 · Tra articoli equivalenti senza marca indicata sceglie l'operatore tra i brand preferiti di ADAC ([[parts-radar-changelog]])
- 2026-10-26 · Prompt di router ed estrazione congelati dopo la revisione delle etichette di sviluppo: le etichette del test si fanno a prompt fermi, così la misura finale non è falsata (D43, Lorenzo) ([[parts-radar-architettura]], [[parts-radar-changelog]])

## Prossimi passi

- Settimana 22-28/10: etichette del test (clienti E, G, H, J) a prompt congelati, voce, misura della targa dei pezzi aggiunti; etichette di sviluppo e router già fatti ([[parts-radar-issue-379]])
- Settimana 29/10-04/11: vocali, attivazione del numero di ADAC in ascolto con il banco presente, prova controllata ([[parts-radar-issue-379]])
- Settimana 05-11/11: lettura delle foto, chiarimenti dell'AI al meccanico, suggerimenti all'operatore, scelta finale dei modelli ([[parts-radar-issue-379]])
- Settimana 12-17/11: sicurezza della dashboard, manuale del banco, server del pilot, traffico vero e report ([[parts-radar-issue-379]])

## Fonti

- [[presentazione-e-sintesi-progetto]]
- [[parts-radar-aggiornamento-api-test]]
- [[ws-demo-blue-age]]
- [[integrazione-api-qricambi-proposta-di-collaborazione]]
- [[integrazione-api-qricambi]]
- [[twilio-blueage-follow-up]]
- [[2026-10-22-primo-caricamento-shared-documents-onedrive]]
- [[riunione-generale-blueage-28-9-sintesi-e-azioni]]
- [[riunione-generale-blueage-12-10-punti-emersi-e-prossimi-passi]]
- [[2026-10-22-watermark-e-task-schedulati]]
- [[parts-radar-architettura]]
- [[parts-radar-decisione-stack-python]]
- [[parts-radar-whatsapp-fornitori]]
- [[parts-radar-kromeda-impatto]]
- [[parts-radar-kromeda-fase0-risultati]]
- [[parts-radar-changelog]]
- [[parts-radar-issue-379]]
- [[parts-radar-issue-420]]
- [[2026-10-23-fonte-github-parts-radar]]
