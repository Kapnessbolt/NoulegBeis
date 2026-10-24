---
description: Curator (SPEC 9.2): proposte dai diari della settimana, su un branch suo con una PR
argument-hint: "[da AAAA-MM-GG] [a AAAA-MM-GG]"
---

Esegui il curator con l'agente `curator`. Lavora su un branch suo in un worktree a parte: la cartella del vault resta su `main`, intatta (`CLAUDE.md` §3 e §7).

Argomenti: `$ARGUMENTS`

1. Finestra: le date negli argomenti; senza argomenti, gli ultimi 7 giorni fino a oggi (`TZ=Europe/Rome date +%F`).
2. Worktree sul branch del curator:
   ```bash
   D=$(TZ=Europe/Rome date +%F); B=claude/curator-$D
   git fetch origin main
   W=$(mktemp -d)/curator && git worktree add -b "$B" "$W" origin/main
   ```
   Se il branch esiste già (secondo giro nello stesso giorno), usa `claude/curator-$D-2`.
3. Lancia l'agente `curator` con radice `$W`, la finestra, modalità `interattiva`.
4. Mostra a Lorenzo il resoconto e, per ogni proposta, motivazione, evidenze e testo proposto. Per ognuna chiedi: accettata, rifiutata, da cambiare o da lasciare `proposta`. Scrivi la risposta nel `status` e applica in `$W` le modifiche chieste. Le rifiutate restano nel registro: il curator non le ripropone.
5. Dopo l'ok, in `$W`: `python3 .claude/scripts/controlla-vault.py`, `git add` dei soli file toccati in `proposals/` e `sessions/`, commit `curator: <D>, <n> proposte`, `git push -u origin "$B"`. Apri la PR verso `main` con `gh pr create` (in locale) o con lo strumento GitHub della sessione (in cloud): titolo `curator: settimana <da>–<a>, <n> proposte`, corpo il resoconto con le decisioni di Lorenzo. Il merge lo fa Lorenzo.
6. `git worktree remove "$W"`. Le proposte accettate si applicano in una sessione interattiva, sulla cartella del vault su `main`; quelle che toccano la SPEC con la sua PR dedicata.
