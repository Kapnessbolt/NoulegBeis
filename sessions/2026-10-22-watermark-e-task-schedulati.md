---
type: session
date: 2026-10-22
surface: cloud
topics: ["[[parts-radar]]", "[[twoteam]]", "[[pulse]]"]
outcome: "Chiusi gli aperti del lotto 5: watermark inizializzati, esito Qricambi, TwoTeam e Cellularline verificati; procedure dei task schedulati in .claude/routines/"
---

# Watermark e task schedulati

## Obiettivo

Chiudere i punti aperti di [[2026-10-22-primo-caricamento-outlook]]: watermark e step 4, esito della call Qricambi, revisione di [[cellularline]] e [[twoteam]].

## Decisioni

- Watermark inizializzati all'ultima modifica ingerita per ogni fonte: SharePoint 2026-10-19T10:13:54Z, OneDrive 2026-10-19T09:26:43Z, Outlook 2026-10-22T14:27:23Z. Il primo delta riparte da lì con 2 ore di sovrapposizione; i file già ingeriti si saltano grazie a `last_modified`.
- Call con [[qricambi]] fatta il 05/10/2026, dalle 17:15 alle 17:45 (dal calendario). Dall'utente: le API si possono integrare in [[parts-radar]], ma l'accesso lo deve chiedere il ricambista, che è il cliente diretto di Qricambi; la documentazione delle API è già disponibile (Ligabò l'ha condivisa nella chat della riunione). La trascrizione Teams non è leggibile: l'accesso Graph alle trascrizioni è disattivato sul tenant.
- [[twoteam]]: dall'utente, prima di BlueAge lo stesso progetto era in TwoTeam; vista la direzione presa si è scelto di aprire una nuova società. Dalle mail di luglio 2026: [[cristian-schifone]] aveva un indirizzo @twoteam.it, non più attivo ad agosto. Tolto il tag `da-verificare`.
- [[cellularline]]: confermata dall'utente così com'è, tolto il tag `da-verificare`.
- Step 4: i task schedulati creati da una sessione cloud nascono senza repository e senza connettori (in questa organizzazione non si passano i connettori da sessione). Provata una sessione di servizio unica a cui legare i 4 task: funzionava, ma l'utente preferisce una sessione nuova per ogni giro. Task e sessione di servizio rimossi; l'utente crea i 4 task dall'interfaccia di claude.ai, con repository e connettore Microsoft 365, e come prompt il file della procedura.
- Nelle sessioni cloud il connettore Microsoft 365 può avere un nome tecnico (`mcp__<uuid>__*`) diverso da quello dichiarato dall'agente `ingestor` (`mcp__Microsoft_365__*`): le procedure in `.claude/routines/` fanno eseguire l'ingestor direttamente dalla sessione.
- Cancellato su richiesta dell'utente il task disattivato `placeholder`, legato al PC pcita1881.
- L'ingestor ora salta i messaggi già ingeriti nelle 2 ore di sovrapposizione del delta posta.
- `curator` e `sessions-cleanup` rimandati: l'agente curator (step 7) e l'hook `Stop` (step 5) non esistono ancora.

## File toccati

- `.state/ingest.json` (watermark)
- `.claude/routines/`: `_comune.md`, `ingest-sharepoint.md`, `ingest-outlook.md`, `digest.md`, `reconcile.md`
- `projects/parts-radar-sviluppo/` (stato, attività, decisioni, log), `clients/qricambi.md`, `sources/mail/2026-10/integrazione-api-qricambi.md`
- `topics/twoteam.md`, `clients/cellularline.md`

## Aperti

- [ ] Creare dall'interfaccia di claude.ai i 4 task (ingest-sharepoint, ingest-outlook, digest, reconcile), una sessione nuova per giro
- [ ] Controllare il primo giro dei task: digest, watermark, nessun doppione
- [ ] Rendere l'agente `ingestor` indipendente dal nome del connettore (es. togliere la restrizione `tools:`), così torna usabile come subagente
- [ ] Dopo 3 giorni di esecuzioni senza errori né doppioni, chiudere lo step 4 (SPEC 13)
- [ ] PR dedicata su `SPEC.md` §7: citare `.claude/routines/` come sede dei prompt dei task
- [ ] Far chiedere l'accesso alle API Qricambi dal ricambista pilota ([[adac-bologna]])
