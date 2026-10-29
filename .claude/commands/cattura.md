---
description: Cattura rapida in inbox/ (SPEC 8): il testo così com'è, da smistare dopo con /smista
argument-hint: "<testo>"
---

Salva una cattura in `inbox/`. Deve essere veloce: non chiedere conferma.

Testo: `$ARGUMENTS`

1. Se il testo è vuoto, chiedi cosa catturare e fermati.
2. Data: `python3 .claude/scripts/config.py oggi`.
3. Slug: `python3 .claude/scripts/famiglia.py --slug "<le prime 6 parole significative del testo>"` (minuscolo, senza accenti, trattini). Togli articoli e preposizioni in testa se allungano lo slug senza dire niente. Il file è `inbox/<data>-<slug>.md`; se esiste già, aggiungi `-2`, `-3`.
4. Titolo: una riga che dice di cosa si tratta, al massimo 8 parole, dal testo.
5. Crea la nota: `python3 .claude/scripts/nuova-nota.py inbox inbox/<data>-<slug>.md --titolo "<titolo>"`. Il frontmatter (`type: inbox`, `created`) lo scrive lo script.
6. Corpo, sotto il titolo, dopo una riga vuota (lo script non la lascia):
   - il testo dell'utente così com'è, senza riscriverlo;
   - una riga `Contesto: [[slug]]` solo se il progetto, il cliente o il tema sono certi (nominati nel testo o nella conversazione corrente) e la nota esiste (`python3 .claude/scripts/cerca.py --nota <slug>` esce con 0). Nel dubbio niente collegamenti (`CLAUDE.md` §2: non inventare);
   - se il testo è un'azione con una data, anche `## Da fare` con `- [ ] <azione> 📅 AAAA-MM-GG`: così la vedono la plancia e `/oggi`.
7. Controllo e commit:
   - `python3 .claude/scripts/controlla-vault.py`; correggi gli errori della nota (`CLAUDE.md` §7);
   - `git branch --show-current`. Su `main`: `git add inbox/<data>-<slug>.md`, commit `inbox: cattura <slug>`, `git pull --rebase origin main`, push (`CLAUDE.md` §7). Su un branch `claude/`: commit sullo stesso branch, senza push su `main`, e dillo all'utente (la cattura arriva su `main` con il branch).
8. Rispondi in una riga: file creato e collegamento (se c'è), e che si smista con `/smista`.
