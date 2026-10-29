---
description: Verifica i giri dei task schedulati (SPEC 7): riga nel digest, commit, watermark, note scritte, doppioni
argument-hint: "[task] [AAAA-MM-GG]"
---

Verifica i giri dei task schedulati. Sola lettura: non correggere niente senza l'ok dell'utente.

Argomenti: `$ARGUMENTS`

1. Argomenti: un task di `vault.yaml` (elenco del giorno con `python3 .claude/scripts/config.py task <data>`, gli stessi di SPEC 7) e una data. Senza task, tutti; senza data, oggi (`python3 .claude/scripts/config.py oggi`).
2. Giri attesi: `python3 .claude/scripts/config.py task <data>` (orari e task del giorno da `vault.yaml`; con `--digest` solo quelli che scrivono nel digest: il `curator` no, il suo esito è la PR). Ora attuale con `python3 .claude/scripts/config.py ora`: un giro la cui ora non è passata da almeno 45 minuti è "atteso", non "mancante".
3. Per ogni giro raccogli:
   - **digest**: la riga di `## Esito dei task` in `journal/<data>.md` (task, ora, esito). Il `curator` non scrive nel digest: per lui la PR verso `main` aperta quel giorno con titolo `curator: settimana …` (`gh pr list --state all --search 'curator: settimana in:title'`, o `list_pull_requests` del connettore GitHub). Il branch non dice niente: nel task schedulato è quello assegnato alla sessione (`claude/<nome>`), non `claude/curator-<data>`. Nessuna PR va bene se non ha trovato niente da proporre;
   - **commit**: `git fetch origin main`, poi `git log origin/main --since=<data> --until=<data+1> --format='%h %ad %s' --date=iso` con il prefisso del task (`ingest(sharepoint)`, `ingest(outlook)`, `ingest(github)`, `ingest(riconcilia)`, `journal:`, `cockpit:`) e `git show --stat <hash>`;
   - **stato**: per gli ingest `git show <hash> -- .state/` (un file per fonte: `sharepoint.json`, `onedrive.json`, `outlook.json`, `github.json`, `reconcile.json`), watermark prima e dopo; quello attuale con `python3 .claude/scripts/stato.py watermark <fonte>` (per `github`, che ha un watermark per repo, `python3 .claude/scripts/stato.py repo <owner/repo>`). Il watermark non torna mai indietro; resta fermo solo se il giro non ha trovato niente di nuovo o se un file è fallito (SPEC 6.2). Un ingest lanciato a mano nello stesso giorno (`/ingest`, riga "interattiva" nel digest) sposta il watermark: tienine conto prima di segnalare uno scarto;
   - **note**: le note create o aggiornate dal commit, confrontate con i numeri del messaggio di commit e della riga del digest.
4. Controlli di merito:
   - `python3 .claude/scripts/controlla-vault.py`: errori e possibili doppioni nei file toccati dal giro;
   - ingest: nessuna nota fonte doppia per la stessa famiglia o lo stesso thread; le righe nuove in `<slug>-log.md` e in `## Attività` non ripetono righe già presenti;
   - `ingest-github`: una sola riga di log per ogni giorno con voci nuove nel changelog (SPEC 6.6);
   - `digest`: ora nel fuso del vault, finestra dall'ultimo commit `journal:` (`.claude/routines/digest.md`);
   - `cockpit`: numeri di progetti e attività uguali a quelli di `python3 .claude/scripts/plancia.py "$(mktemp -d)"`;
   - `curator`: nessun commit su `main`, PR verso `main` con al massimo 5 proposte.
5. Rapporto, una riga per giro: `<task> <ora attesa> → OK | ERRORE | MANCANTE | ANOMALIA`, con la prova (commit, watermark prima → dopo, note). Per ogni anomalia: causa probabile e correzione proposta (nota, procedura in `.claude/routines/`, SPEC).
6. Aperti: cerca in `sessions/*.md` le caselle `- [ ]` che chiedono di verificare questi giri. Se la verifica le chiude, proponi di spuntarle con ` (chiuso in [[<data>]])`.
7. Correggi solo dopo l'ok. Poi controllo del vault, commit `vault: verifica task <data>` e push su `main` (`CLAUDE.md` §7).
