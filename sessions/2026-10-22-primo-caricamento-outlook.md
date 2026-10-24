---
type: session
date: 2026-10-22
surface: cloud
topics: ["[[blueage]]", "[[parts-radar]]", "[[ai-che-cresce-con-lazienda]]", "[[second-brain]]"]
outcome: "Step 3, lotto 5: Outlook ultimi 60 giorni, 49 thread e 15 allegati; progetto parts-radar-sviluppo creato"
---

# Primo caricamento · lotto 5 Outlook

## Obiettivo

Ingerire la casella Outlook degli ultimi 60 giorni (dal 2026-08-23), ultimo lotto del primo caricamento (SPEC 6.5).

## Decisioni

- 116 messaggi: 15 scartati dal filtro (no-reply, notifiche di servizi, Read AI, Copilot), 59 thread. L'utente ha escluso altri 10 thread: personali e con dati sensibili (contratto Walvoil, compensi UBS, file inoltrato alla Gmail), Cargood (credenziali, non è BlueAge), 6 notifiche di calendario e una bozza mai inviata. Restano 49 thread, ingeriti da 6 agenti ingestor in parallelo.
- Nuovo progetto [[parts-radar-sviluppo]] con l'ok dell'utente. Lo slug `parts-radar` resta al tema prodotto. Ruolo di Lorenzo: project manager e sviluppatore del prodotto insieme a Cristian Schifone (indicato dall'utente).
- Nuove organizzazioni approvate: [[liuc]], [[umbria-business-school]], [[tifast]], [[deepagent]], [[onepartner]]; per Parts Radar [[adac-bologna]], [[solera]], [[assoricambi]], [[qricambi]].
- Nuovi temi approvati: [[ai-che-cresce-con-lazienda]] (offerta a canone) e [[second-brain]] (pacchetto; questo vault ne è la versione personale di Lorenzo).
- Nuove persone dalle mail: [[anna-bono]], [[silvia-fumagalli]], [[angelo-santilli]], [[luciano-baccarelli]], [[andrea-marchesi]], [[maurizio-fortuna]], [[raffaele-zichella]], [[ignazio-romeo]], [[giampiero-pizza]], [[alessandro-ligabo]], [[francesco-bollazzi]]. Aggiunta l'email di [[leonardo-pinsone]].
- Versioni da allegati di mail aggiunte allo storico delle famiglie esistenti: company profile v13, v17, v19, v21 e la copia del 12/10; PULSE_Sintesi_C del 18/09; M1_v05_2 del 12/10.
- Nessun dato sensibile riportato: credenziali Solera, codici Teams, compensi, indirizzi e telefoni omessi; i CV non sono stati ingeriti.

## File toccati

- `sources/mail/2026-08`, `2026-09`, `2026-10` (49 thread), `sources/attachments/` (15 allegati)
- `projects/`: parts-radar-sviluppo (nuovo), corso-ai-manini, corso-ai-mtu, velo-ce-progetto-dynamics, manini-supply-chain-magazzino
- `clients/`: 9 nuovi, aggiornati manini e meccanotecnica-umbra
- `people/`: 11 nuove, aggiornate leonardo-pinsone, cristian-schifone, michele-padoin
- `topics/`: 2 nuovi, aggiornati blueage, pulse, compass, ai-foundation-program, giornata-in-azienda, business-central-ai, ai-nei-processi
- Fonti versioni: blueage-companyprofile, pulse-sintesi, ai-foundation-program-m1
- `.state/ingest.json`: 49 thread Outlook, watermark ancora null

## Decisioni dopo il campione

- Campione approvato. `deepagent` separato: nuova nota cliente [[concentrazione-eu]] (rete di manager di Alberto Bezzi), [[deepagent]] resta la piattaforma.
- Proposte degli agenti approvate e create: clienti [[tarkett]], [[clinicalfarma]], [[endura]], [[pettenon]]; persone [[elisabetta-monaldi]], [[daniela-rossi]], [[luca-zamponi]]; temi [[pulse-light]], [[piano-editoriale-linkedin]]; progetti [[corso-ai-tifast]] e [[osservatorio-ai-pmi-liuc]] (Lorenzo non coinvolto direttamente).
- Corso Manini: valgono 36 ore per gli utenti più 8 per i Sistemi Informativi; l'ipotesi di 48 ore è superata.
- `Ipotesi Formazione IT` è obsoleto: nota allegato rimossa, il thread lo cita solo per nome.

## Aperti

- [x] Inizializzare i watermark di SharePoint, OneDrive e Outlook e passare allo step 4 (task schedulati), in una nuova sessione (chiuso in [[2026-10-22-watermark-e-task-schedulati]])
- [x] Verificare l'esito della call con Qricambi del 05/10 (chiuso in [[2026-10-22-watermark-e-task-schedulati]])
- [x] Rivedere e togliere il tag `da-verificare` da [[cellularline]] e [[twoteam]] (chiuso in [[2026-10-22-watermark-e-task-schedulati]])
