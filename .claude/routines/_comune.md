# Regole comuni ai task schedulati (SPEC 7)

Valgono per tutti i file di questa cartella. Il task gira senza utente: non fare domande, lavora in autonomia.

1. **Avvio**: `git fetch origin main && git checkout -B main origin/main`. Leggi `CLAUDE.md`; la specifica è `SPEC.md`, leggi solo le sezioni citate dal task.
2. **Limiti**: scrivi solo dove la modalità `schedulata` lo consente (`CLAUDE.md` §3). Non creare progetti, non scrivere in `inbox/`, non modificare `CLAUDE.md`, `SPEC.md` o `.claude/`.
3. **Digest**: ogni task registra l'esito in `journal/AAAA-MM-GG.md` (data Europe/Rome), sezione `## Esito dei task`, con una riga `| <task> HH:MM | OK |` oppure gli errori (file, motivo). Se il digest non esiste crealo da `_templates/journal.md`; se esiste aggiungi, senza cancellare ciò che c'è.
4. **Errori**: se il connettore Microsoft 365 non risponde o manca, oppure un watermark è `null`, non inventare nulla: scrivi l'errore nel digest e fai commit e push del solo digest.
5. **Git**: `python3 .claude/scripts/controlla-vault.py` e correggi gli errori introdotti; poi `git pull --rebase origin main`, commit e `git push origin HEAD:main`. Conflitto su `.state/ingest.json`: per ogni fonte vince il watermark più avanzato, con l'unione di `items`/`threads`. Altri conflitti: riapplica la tua modifica sulla versione remota. Se il push fallisce per rete riprova fino a 4 volte (2, 4, 8, 16 secondi).
6. **Risposta finale**: due righe con l'esito (note create e aggiornate, errori, nuovo watermark, push).
