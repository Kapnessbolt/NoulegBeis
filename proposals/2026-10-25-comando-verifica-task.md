---
type: proposal
date: 2026-10-25
kind: skill
status: accettata
---

# Comando /verifica-task per controllare i giri dei task schedulati

## Motivazione

Verificare a mano i giri dei task schedulati è la procedura che si è ripetuta di più in settimana: ci è andata una sessione intera, più un aperto "verificare il primo giro" in altri 4 diari. Ogni volta si leggono a mano digest, `git log`, `.state/ingest.json` e le note scritte. Il Cockpit mostra solo OK, errore o mancante dalla riga del digest, non se il giro ha lavorato bene (watermark, doppioni, righe di log). Così gli errori veri (ordine dei comandi git, ora in UTC, finestra del digest) sono usciti solo con la verifica a mano. Con il comando la verifica dura un minuto, e il pulsante "Indaga" della mod `cockpit` può lanciarlo.

## Evidenze

- [[2026-10-22-watermark-e-task-schedulati]]: aperto "Controllare il primo giro dei task: digest, watermark, nessun doppione".
- [[2026-10-23-verifica-primo-giro-task]]: una sessione intera per quel controllo; trovati tre errori nelle procedure; restano due aperti di verifica (ingest-outlook delle 13:15 e Reconcile, watermark SharePoint del 24/10).
- [[2026-10-23-fonte-github-parts-radar]]: aperto "Verificare il primo giro del task: riga nel digest, watermark avanzato, una riga di log, nessuna attività doppia".
- [[2026-10-23-plancia-dashboard]]: aperto "Verificare il primo giro di DailyBoard2 (riga nel digest)".
- [[2026-10-24-restyling-cockpit-implementazione]]: aperto "Verificare il primo giro del task cockpit con i sei dataset".
- [[2026-10-24-restyling-cockpit]]: "il controllo più frequente è l'esito dei task schedulati (4 diari su 17 e una sessione intera)".
- [[2026-10-24]]: il watermark SharePoint è salito a 2026-10-19T16:22:49Z, non al 2026-10-21T06:30:14Z che si aspettava [[2026-10-23-verifica-primo-giro-task]]. È il tipo di scarto che il comando fa emergere da solo.

## Testo proposto

Nuovo file `.claude/commands/verifica-task.md`:

```markdown
---
description: Verifica i giri dei task schedulati (SPEC 7): riga nel digest, commit, watermark, note scritte, doppioni
argument-hint: "[task] [AAAA-MM-GG]"
---

Verifica i giri dei task schedulati. Sola lettura: non correggere niente senza l'ok di Lorenzo.

Argomenti: `$ARGUMENTS`

1. Argomenti: un task di SPEC 7 (`ingest-sharepoint`, `ingest-outlook`, `ingest-github`, `digest`, `cockpit`, `reconcile`) e una data. Senza task, tutti; senza data, oggi (`TZ=Europe/Rome date +%F`).
2. Giri attesi: gli orari del giorno da SPEC 7 (la domenica anche `reconcile`). Ora attuale con `TZ=Europe/Rome date +%H:%M`: un giro la cui ora non è passata da almeno 45 minuti è "atteso", non "mancante".
3. Per ogni giro raccogli:
   - **digest**: la riga di `## Esito dei task` in `journal/<data>.md` (task, ora, esito);
   - **commit**: `git fetch origin main`, poi `git log origin/main --since=<data> --until=<data+1> --format='%h %ad %s' --date=iso` con il prefisso del task (`ingest(sharepoint)`, `ingest(outlook)`, `ingest(github)`, `ingest(riconcilia)`, `journal:`, `cockpit:`) e `git show --stat <hash>`;
   - **stato**: per gli ingest `git show <hash> -- .state/ingest.json`, watermark prima e dopo. Il watermark non torna mai indietro; resta fermo solo se il giro non ha trovato niente di nuovo o se un file è fallito (SPEC 6.2);
   - **note**: le note create o aggiornate dal commit, confrontate con i numeri del messaggio di commit e della riga del digest.
4. Controlli di merito:
   - `python3 .claude/scripts/controlla-vault.py`: errori e possibili doppioni nei file toccati dal giro;
   - ingest: nessuna nota fonte doppia per la stessa famiglia o lo stesso thread; le righe nuove in `<slug>-log.md` e in `## Attività` non ripetono righe già presenti;
   - `ingest-github`: una sola riga di log per ogni giorno con voci nuove nel changelog (SPEC 6.6);
   - `digest`: ora in Europe/Rome, finestra dall'ultimo commit `journal:` (`.claude/routines/digest.md`);
   - `cockpit`: numeri di progetti e attività uguali a quelli di `python3 .claude/scripts/plancia.py "$(mktemp -d)"`.
5. Rapporto, una riga per giro: `<task> <ora attesa> → OK | ERRORE | MANCANTE | ANOMALIA`, con la prova (commit, watermark prima → dopo, note). Per ogni anomalia: causa probabile e correzione proposta (nota, procedura in `.claude/routines/`, SPEC).
6. Aperti: cerca in `sessions/*.md` le caselle `- [ ]` che chiedono di verificare questi giri. Se la verifica le chiude, proponi di spuntarle con ` (chiuso in [[<data>]])`.
7. Correggi solo dopo l'ok. Poi controllo del vault, commit `vault: verifica task <data>` e push su `main` (`CLAUDE.md` §7).
```

`SPEC.md` §8, nuova riga della tabella (PR dedicata):

```markdown
| `/verifica-task [task] [data]` | Verifica i giri dei task schedulati: riga nel digest, commit, watermark, note scritte, doppioni; propone le correzioni e gli aperti da spuntare |
```

Fuori dal repo: il pulsante "Indaga" della mod `cockpit` può scrivere nel prompt `/verifica-task <task>` al posto della richiesta libera.
