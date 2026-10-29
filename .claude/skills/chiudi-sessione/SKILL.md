---
name: chiudi-sessione
description: Chiude una sessione interattiva del vault (CLAUDE.md §8, SPEC 12) scrivendo o aggiornando il diario in sessions/, spuntando gli aperti dei diari precedenti chiusi nella sessione, poi commit e push su main. Usala quando l'utente dice "chiudiamo", "per oggi basta", "fine sessione", "scrivi il diario", o con /chiudi-sessione; anche prima di chiudere una sessione che ha cambiato file, se il diario non c'è o non è aggiornato.
argument-hint: "[slug]"
---

# Chiudi sessione

Il diario è la memoria della sessione: il curator lo legge ogni domenica (SPEC 9.2), la sessione dopo riparte da lì. Ogni sessione parte da un clone nuovo: ciò che non è committato è perso.

1. **File**: `sessions/<data>-<slug>.md`, con la data di oggi (`python3 .claude/scripts/config.py oggi`) e lo slug degli argomenti, oppure 2-4 parole dall'obiettivo. Se in questa sessione hai già scritto il diario, aggiornalo: aggiungi le decisioni nuove in coda, non riscrivere quelle di prima. Se la sessione non ha deciso né cambiato niente, dillo e non scrivere il diario.
2. **Frontmatter** dal template `_templates/session.md`: `surface` `cloud` se `CLAUDE_CODE_REMOTE=true`, altrimenti `locale`; `topics` con i wikilink ai temi toccati, tra virgolette (`["[[pulse]]"]`); `outcome` in una riga, tra virgolette.
3. **Solo le sezioni del template**:
   - `## Obiettivo`: 1-2 frasi;
   - `## Decisioni`: una riga per decisione, con il perché; "dall'utente" quando ha deciso l'utente. Niente fonte in coda alle righe: la fonte è il diario stesso;
   - `## File toccati`: dai commit della sessione e da `git status`, raggruppati per cartella; ciò che sta fuori dal repo (OneDrive, altri repo, artifact) in una riga a parte;
   - `## Aperti`: checkbox, con `📅 AAAA-MM-GG` solo se c'è una scadenza vera. Un aperto chiuso nella sessione stessa si spunta con la prova in coda (`(chiuso: PR #n unita)`), senza citare il diario stesso.
4. **Aperti dei diari precedenti** chiusi in questa sessione: spuntali nel diario d'origine e aggiungi in coda ` (chiuso in [[<slug di questo diario>]])`.
5. **Progetti**: le decisioni che cambiano lo stato di un progetto vanno anche nella scheda e nel log (`CLAUDE.md` §2): controlla che ci siano, e se mancano aggiungile.
6. **Git** come `CLAUDE.md` §7, con `git add` dei soli file della sessione e commit `session: <slug>` (`session: <slug>, <cosa>` se aggiorni).
7. **Risposta**: due righe, il percorso del diario e il commit; gli aperti rimasti.
