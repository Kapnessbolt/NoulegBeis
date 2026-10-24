---
type: proposal
date: 2026-10-25
kind: skill
status: proposta
---

# Comando /chiudi-sessione per scrivere il diario sempre allo stesso modo

## Motivazione

Tutti i 19 diari della settimana sono scritti a mano: ogni sessione rifà da capo la procedura di `CLAUDE.md` §8 e il risultato cambia da un diario all'altro. Ne sono usciti un YAML non valido che ha bloccato il controllo, decisioni che si citano da sole come fonte (16 righe in un solo diario), sezioni fuori template e, soprattutto, aperti chiusi da una sessione ma lasciati aperti nel diario d'origine (23 spuntati in questo giro). `/chiudi-sessione` è già previsto in SPEC §8 e nello step 5, ma non esiste: senza il comando ogni diario dipende da come la sessione interpreta §8.

## Evidenze

- [[2026-10-22-controllo-vault]]: `outcome` non quotato nel diario dello step 2, YAML non valido trovato dal controllo.
- [[2026-10-24-restyling-cockpit-implementazione]]: ogni decisione e ogni aperto finiscono con `([[2026-10-24-restyling-cockpit-implementazione]])`, cioè il diario che cita se stesso; 4 commit `session:` sullo stesso diario.
- [[2026-10-24-cockpit-in-locale]]: stessa autocitazione negli aperti, con date `📅` aggiunte dopo; 4 commit `session:`.
- [[2026-10-22-primo-caricamento-outlook]] e [[2026-10-24-restyling-cockpit]]: sezioni fuori template (`## Decisioni dopo il campione`, `## Fonti lette`).
- [[2026-10-22-watermark-e-task-schedulati]]: chiude tre aperti di [[2026-10-22-primo-caricamento-outlook]] senza spuntarli là; lo stesso in [[2026-10-23-verifica-primo-giro-task]] per gli aperti del 22/10.
- [[2026-10-24-restyling-cockpit]]: aperto "Igiene degli aperti dei diari: molti sono chiusi altrove ma restano spuntati come aperti".

## Testo proposto

Nuovo file `.claude/commands/chiudi-sessione.md` (la riga in SPEC §8 c'è già):

```markdown
---
description: Scrive o aggiorna il diario della sessione in sessions/, poi commit e push (CLAUDE.md §8, SPEC 12)
argument-hint: "[slug]"
---

Chiudi la sessione: diario, controllo, commit e push.

Argomenti: `$ARGUMENTS`

1. File: `sessions/<data>-<slug>.md`, con la data di oggi (`TZ=Europe/Rome date +%F`) e lo slug degli argomenti, oppure 2-4 parole dall'obiettivo. Se in questa sessione hai già scritto il diario, aggiornalo: aggiungi le decisioni nuove in coda, non riscrivere quelle di prima.
2. Frontmatter dal template `_templates/session.md`: `surface` `cloud` se `CLAUDE_CODE_REMOTE=true`, altrimenti `locale`; `topics` con i wikilink ai temi toccati, tra virgolette; `outcome` in una riga, tra virgolette.
3. Solo le sezioni del template:
   - `## Obiettivo`: 1-2 frasi;
   - `## Decisioni`: una riga per decisione, con il perché; "dall'utente" quando ha deciso Lorenzo. Niente fonte in coda: la fonte è il diario stesso;
   - `## File toccati`: dai commit della sessione e da `git status`, raggruppati per cartella; ciò che sta fuori dal repo in una riga a parte;
   - `## Aperti`: checkbox, con `📅 AAAA-MM-GG` solo se c'è una scadenza vera.
4. Aperti dei diari precedenti chiusi in questa sessione: spuntali nel diario d'origine e aggiungi in coda ` (chiuso in [[<slug di questo diario>]])`.
5. Le decisioni che cambiano lo stato di un progetto vanno anche nella scheda e nel log (`CLAUDE.md` §2): controlla che ci siano.
6. `python3 .claude/scripts/controlla-vault.py`, commit `session: <slug>` (`session: <slug>, <cosa>` se aggiorni), `git pull --rebase origin main`, push su `main`.
```

`CLAUDE.md` §8, al posto del paragrafo attuale:

```markdown
Prima di chiudere una sessione interattiva lancia `/chiudi-sessione`: scrive il diario in `sessions/AAAA-MM-DD-<slug>.md` (obiettivo, decisioni, file toccati, aperti), spunta gli aperti dei diari precedenti chiusi nella sessione, poi commit e push. Ogni sessione parte da un clone nuovo: ciò che non è committato è perso.
```
