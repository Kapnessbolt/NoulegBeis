# Task `curator` · orari in `vault.yaml` (`task`)

Nessun connettore Microsoft 365; GitHub serve solo per aprire la PR. Prima leggi `.claude/routines/_comune.md` e seguilo, con due eccezioni (`CLAUDE.md` §3, SPEC 9.2): il curator non scrive nel digest (punto 4) e non fa push su `main` (punto 6). Lavora sul branch che la sessione gli assegna e il suo esito è la PR.

1. `D=$(python3 .claude/scripts/config.py oggi)`. Branch: quello che le istruzioni della sessione assegnano (`claude/<nome>`), perché la sessione può fare push solo lì e nessuno può autorizzarne un altro; `git checkout -B <branch> origin/main`. Solo se la sessione non assegna nessun branch, `claude/curator-$D` (se esiste già su origin, `claude/curator-$D-2`).
2. Segui `.claude/agents/curator.md` in questa sessione, non come subagente: radice la cartella del repo, finestra gli ultimi 7 giorni fino a oggi, modalità `schedulata`.
3. Se l'agente non ha scritto niente: nessun commit, nessuna PR, e la risposta finale lo dice.
4. Altrimenti: `python3 .claude/scripts/controlla-vault.py`, `git add` dei soli file toccati in `proposals/` e `sessions/`, commit `curator: <D>, <n> proposte`, `git push -u origin <branch>`. Se il push fallisce per rete, riprova fino a 4 volte (2, 4, 8, 16 secondi).
5. Apri la PR verso `main` con lo strumento GitHub della sessione (`create_pull_request`) o, dove c'è, `gh pr create`: titolo `curator: settimana <da>–<a>, <n> proposte`, corpo il resoconto dell'agente. Non fare merge: lo fa l'utente.
6. Risposta finale: due righe con proposte scritte, aperti spuntati e link della PR, oppure l'errore (con push o PR non riusciti il branch resta dov'è arrivato).
