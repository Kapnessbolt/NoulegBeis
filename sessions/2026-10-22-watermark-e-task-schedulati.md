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
- Task creati dall'utente dall'interfaccia, una sessione nuova per giro: `ingest-sharepoint` ogni giorno 06:50 (Opus 5.5), `ingest-outlook` 07:05 (Opus 5.5) e `ingest-outlook 2` 13:15, `Digest` 07:45 (Sonnet 5.5), `Reconcile` domenica 08:45 (Sonnet 5.5). Orari diversi da SPEC §7, da allineare con la PR sulla SPEC.
- L'ingestor ora salta i messaggi già ingeriti nelle 2 ore di sovrapposizione del delta posta.
- Test di raccolta delle sessioni: dalla sessione si possono elencare le sessioni dell'account (anche archiviate e di altri repo, es. parts-radar) e leggerne la trascrizione. Un subagente ha ricostruito il diario completo di una sessione parts-radar del 18/10 con 3 letture, filtrando con uno script (le pagine pesano 170-200 mila caratteri). Il diario non è stato salvato nel vault: era solo una prova.
- Parts Radar: il dettaglio di sviluppo resta nel repo parts-radar. Nel vault entrano solo i documenti che l'utente caricherà su OneDrive e SharePoint, oltre alla posta, come per tutte le fonti. Le sessioni di parts-radar restano fuori dalla raccolta delle sessioni.
- `curator` e `sessions-cleanup` rimandati: l'agente curator (step 7) e l'hook `Stop` (step 5) non esistono ancora.

## File toccati

- `.state/ingest.json` (watermark)
- `.claude/routines/`: `_comune.md`, `ingest-sharepoint.md`, `ingest-outlook.md`, `digest.md`, `reconcile.md`
- `projects/parts-radar-sviluppo/` (stato, attività, decisioni, log), `clients/qricambi.md`, `sources/mail/2026-10/integrazione-api-qricambi.md`
- `topics/twoteam.md`, `clients/cellularline.md`

## Aperti

- [x] Step 5: valutare la raccolta delle sessioni via trascrizione (elenco sessioni della settimana → diari mancanti in `sessions/`) al posto dell'hook `Stop`; solo sessioni sul vault e chat di claude.ai, escluse quelle di parts-radar (chiuso in [[2026-10-26-diari-mancanti-e-vault-sola-lettura]])
- [x] Controllare il primo giro dei task: digest, watermark, nessun doppione (chiuso in [[2026-10-23-verifica-primo-giro-task]])
- [ ] Rendere l'agente `ingestor` indipendente dal nome del connettore (es. togliere la restrizione `tools:`), così torna usabile come subagente
- [ ] Dopo 3 giorni di esecuzioni senza errori né doppioni, chiudere lo step 4 (SPEC 13)
- [x] PR dedicata su `SPEC.md` §7: citare `.claude/routines/` come sede dei prompt dei task e aggiornare gli orari (chiuso: PR #10 unita il 23/10)
- [ ] Far chiedere l'accesso alle API Qricambi dal ricambista pilota ([[adac-bologna]])
