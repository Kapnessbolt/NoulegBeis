---
type: project
status: attivo
role: "Project manager e sviluppatore del prodotto, insieme a Cristian Schifone"
clients: ["[[adac-bologna]]", "[[solera]]", "[[assoricambi]]", "[[qricambi]]"]
people: ["[[cristian-schifone]]"]
updated: 2026-10-22
---

# Parts Radar · sviluppo e pilota

## Stato

- Lorenzo Curione è project manager e sviluppatore del prodotto [[parts-radar]] insieme a [[cristian-schifone]] ([[2026-10-22-primo-caricamento-shared-documents-onedrive]]); tiene i contatti con fornitori e partner ([[ws-demo-blue-age]])
- Parts Radar è un middleware B2B per l'aftermarket indipendente: dal meccanico al ricambista arrivano foto della targa e richiesta a voce o per iscritto, il sistema riconosce il veicolo e propone il ricambio originale e le alternative compatibili; si affianca a qualunque gestionale ed è pensato per più ricambisti ([[presentazione-e-sintesi-progetto]], [[integrazione-api-qricambi-proposta-di-collaborazione]])
- Filiera: [[solera]] (Kromeda) per i dati veicolo e ricambi (targa → VIN → codice originale → aftermarket), [[assoricambi]] come associazione che sostiene il progetto, [[adac-bologna]] come ricambista pilota, [[qricambi]] per prezzi netti e disponibilità, Twilio per il canale WhatsApp ([[presentazione-e-sintesi-progetto]], [[parts-radar-aggiornamento-api-test]], [[integrazione-api-qricambi-proposta-di-collaborazione]], [[twilio-blueage-follow-up]])
- Kromeda: web service demo attivo dal 18/09/2026; il passaggio VIN testuale → codice originale è in sviluppo, beta attesa tra fine settembre e ottobre ([[ws-demo-blue-age]], [[parts-radar-aggiornamento-api-test]])
- WhatsApp: architettura con webhook HTTPS di BlueAge che riceve testo, audio e immagini e smista per cliente sul numero di destinazione ([[twilio-blueage-follow-up]])
- Al 12/10/2026: dashboard a buon punto e nuova banca dati prodotto quasi integrata; precisione circa 75% deterministica, 80% con i parametri della banca dati, 83–84% con criteri meno efficienti (da tenere come suggeriti); a gennaio il fornitore rilascia l'interrogazione per allestimento ([[riunione-generale-blueage-12-10-punti-emersi-e-prossimi-passi]])
- Obiettivo finale: un SaaS in cui ogni cliente attiva il proprio numero WhatsApp; il ricambista pilota sarebbe disposto, in modo informale, a pagare la banca dati (oggi circa 1 € a ricerca a crediti, che resterebbero come riserva) ([[riunione-generale-blueage-12-10-punti-emersi-e-prossimi-passi]])

## Attività

- [ ] Testare il web service demo Kromeda e aggiornare Solera sui risultati ([[ws-demo-blue-age]])
- [ ] Attendere da Solera la proposta ufficiale (API di validazione con ADAC, servizio a regime con pricing) ([[parts-radar-aggiornamento-api-test]])
- [ ] Riprendere il web service VIN testuale all'uscita della beta Kromeda, prevista fine settembre / ottobre 2026 ([[parts-radar-aggiornamento-api-test]])
- [ ] Riscontro da Assoricambi sul feedback di Kromeda / Collins e sui fornitori VIN per un ambiente di test ([[presentazione-e-sintesi-progetto]])
- [ ] Verificare l'esito della call con Qricambi del 05/10 (data dedotta, non scritta nell'invito) ([[integrazione-api-qricambi]])
- [ ] Rispondere a Twilio sullo stack del webhook ([[twilio-blueage-follow-up]])
- [ ] Contattare l'aggregatore degli accordi ricambisti-distributori per il confronto prezzi, con Cristian ([[riunione-generale-blueage-28-9-sintesi-e-azioni]])
- [ ] Capire da Solera come vende il servizio e chiedere una proroga della prova ([[riunione-generale-blueage-12-10-punti-emersi-e-prossimi-passi]])
- [ ] Chiarire lo step del pilota 📅 2026-11-12 ([[riunione-generale-blueage-12-10-punti-emersi-e-prossimi-passi]])

## Decisioni

- 2026-09-07 · Chiesta a Solera una proposta ufficiale per l'API di validazione con ADAC pilota e per il servizio a regime con pricing ([[parts-radar-aggiornamento-api-test]])
- 2026-09-29 · Con Qricambi niente dettagli confidenziali dell'idea, su sua richiesta: sviluppa da tre anni Quoting24, un prodotto simile ([[integrazione-api-qricambi-proposta-di-collaborazione]])
- 2026-10-12 · Canale WhatsApp in "build" con webhook, senza personalizzazioni lato utente ([[twilio-blueage-follow-up]])
- 2026-10-12 · Per WhatsApp ci si appoggia a un tech provider esistente, senza diventare tech provider Meta ([[riunione-generale-blueage-12-10-punti-emersi-e-prossimi-passi]])

## Prossimi passi

-

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
