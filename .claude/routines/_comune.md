# Regole comuni ai task schedulati (SPEC 7)

Valgono per tutti i file di questa cartella. Il task gira senza utente: non fare domande, lavora in autonomia.

1. **Avvio**: ogni giro gira in una sessione nuova. `git fetch origin main && git checkout -B main origin/main`. Leggi `CLAUDE.md`; la specifica è `SPEC.md`, leggi solo le sezioni citate dal task.
2. **Ingestor**: quando il task dice "lancia l'agente `ingestor`", segui tu `.claude/agents/ingestor.md` in questa sessione, non come subagente. Il connettore Microsoft 365 nelle sessioni dei task può avere un nome diverso da `mcp__Microsoft_365__*` (es. `mcp__<uuid>__outlook_email_search`): usa gli strumenti con lo stesso suffisso (`sharepoint_search`, `sharepoint_folder_search`, `outlook_email_search`, `read_resource`), solo in lettura.
3. **Limiti**: scrivi solo dove la modalità `schedulata` lo consente (`CLAUDE.md` §3). Non creare progetti, non scrivere in `inbox/`, non modificare `CLAUDE.md`, `SPEC.md` o `.claude/`.
4. **Digest**: ogni task registra l'esito in `journal/AAAA-MM-GG.md` (data Europe/Rome), sezione `## Esito dei task`, con una riga `| <task> HH:MM | OK |` oppure gli errori (file, motivo). Data e ora sempre in Europe/Rome: `TZ=Europe/Rome date +%Y-%m-%d` e `TZ=Europe/Rome date +%H:%M` (il container è in UTC). Se il digest non esiste crealo da `_templates/journal.md`; se esiste aggiungi, senza cancellare ciò che c'è.
5. **Errori**: se il connettore Microsoft 365 non risponde o manca, oppure un watermark è `null`, non inventare nulla: scrivi l'errore nel digest e fai commit e push del solo digest.
6. **Git**: `python3 .claude/scripts/controlla-vault.py` e correggi gli errori introdotti; poi `git add` e commit, **dopo** `git pull --rebase origin main` (con modifiche non committate il rebase si rifiuta), infine `git push origin HEAD:main`. Conflitto su `.state/ingest.json`: per ogni fonte vince il watermark più avanzato, con l'unione di `items`/`threads`. Altri conflitti: riapplica la tua modifica sulla versione remota. Se il push fallisce per rete riprova fino a 4 volte (2, 4, 8, 16 secondi).
7. **Risposta finale**: due righe con l'esito (note create e aggiornate, errori, nuovo watermark, push).
