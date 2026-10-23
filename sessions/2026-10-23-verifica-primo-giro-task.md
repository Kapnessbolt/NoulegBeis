---
type: session
date: 2026-10-23
surface: cloud
topics: []
outcome: "Primo giro dei task schedulati verificato: esiti corretti; corretti ordine dei comandi git, ora del digest e finestra del digest"
---

# Verifica del primo giro dei task schedulati

## Obiettivo

Chiudere l'aperto di [[2026-10-22-watermark-e-task-schedulati]] "Controllare il primo giro dei task": i task sono partiti, hanno lavorato come previsto, e cosa si può migliorare nelle procedure.

## Decisioni

- Esecuzioni del 23/10 tutte riuscite: `ingest-sharepoint` 06:50, `ingest-outlook` 07:06, `Digest` 07:47 (Europe/Rome). `ingest-outlook 2` (13:15) e `Reconcile` (domenica 25/10) non ancora partiti.
- Esiti verificati sul connettore: Outlook non ha messaggi dopo il watermark 2026-10-22T14:27:23Z (gli unici 2 della sovrapposizione erano già ingeriti); SharePoint dà gli stessi 9 risultati del task (3 nel perimetro invariati, 5 sul sito partner, 1 zip). Watermark invariati, nessuna nota creata, nessun doppione.
- Errore in entrambi gli ingest: `git pull --rebase` lanciato con il digest non committato si rifiuta; i task si sono ripresi da soli. Corretto l'ordine (commit → pull --rebase → push) in `.claude/routines/_comune.md`, `.claude/agents/ingestor.md` §9 e `CLAUDE.md` §7.
- Il digest ha scritto l'ora in UTC (05:50 invece di 07:50). Ora esplicita con `TZ=Europe/Rome` in `_comune.md`, `ingestor.md` §8 e `digest.md`; corretta la riga nel digest di oggi.
- Il digest di oggi elencava 238 note del primo caricamento (47 KB) perché la finestra era "ultime 24 ore". `digest.md`: finestra dall'ultimo commit `journal:`, esclusione delle note già nel digest di ieri (ingest-outlook delle 13:15), oltre 30 voci conteggio per cartella; attività scadute da più di 14 giorni in un blocco a parte.

## File toccati

- `.claude/routines/_comune.md`, `.claude/routines/digest.md`, `.claude/agents/ingestor.md`, `CLAUDE.md`
- `journal/2026-10-23.md` (ora del digest)

## Aperti

- [ ] Velo-CE: 3 attività scadute il 21/09 (V1, V2, V8): chiuderle o riprogrammarle
- [ ] Togliere il connettore `visualize` dai task (non serve a nessuno; SPEC 7: solo i connettori necessari), dall'interfaccia di claude.ai
- [ ] Controllare `ingest-outlook 2` di oggi e il primo `Reconcile` di domenica 25/10
- [ ] Nella PR su `SPEC.md` §7 (orari): valutare anche il watermark SharePoint che non avanza se nel perimetro non cambia nulla (la finestra di ricerca si allarga ogni giorno)
