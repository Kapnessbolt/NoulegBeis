---
type: session
date: 2026-10-29
surface: cloud
topics: ["[[second-brain]]"]
outcome: "Testato il caricamento di .claude/rules/ (15 subagenti, 2 sessioni cloud, /compact); regola a percorso fonti.md per sources/, CLAUDE.md snellito, agenti e routine senza copie, controllo delle regole nel pre-commit; PR #49 e #50 unite, SPEC 1.24"
---

# Regole a percorso e istruzioni senza copie

## Obiettivo

Capire se e come spostare parte di `CLAUDE.md` in regole a percorso (`.claude/rules/` con `paths:`) per alleggerire il contesto senza perdere affidabilità, chiudendo con test riproducibili gli aperti del test canarino del pomeriggio; poi applicare la proposta con una PR (primo pezzo dello step 14 di SPEC 13.1).

## Decisioni

- Una regola con `paths:` arriva nel contesto con Read, Write, Edit e con `cat`/`head` di un singolo file via Bash; non con Glob, Grep, script Python (anche con il percorso come argomento), heredoc o redirezioni. Arriva dopo la prima operazione nella cartella e una sola volta per sessione. Glob annidati, più pattern per regola e regole sovrapposte funzionano (15 subagenti in contesto pulito, confermati dalla documentazione ufficiale).
- Dopo `/compact` la regola senza `paths:` viene reiniettata; quella a percorso no, nemmeno leggendo un altro file della cartella (test fatto a mano dall'utente su una sessione cloud). Contraddice la documentazione: ciò che deve valere sempre resta in `CLAUDE.md`.
- Le regole senza `paths:` si leggono all'avvio: un file aggiunto a sessione in corso non si carica; quelle a percorso sì.
- I subagenti e le sessioni cloud nuove ricevono `CLAUDE.md` e le regole senza `paths:` da soli: "leggi prima CLAUDE.md" in agenti e routine era una seconda copia da 11 KB. Ora si rilegge solo se non è nel contesto, perché nei task schedulati veri l'arrivo automatico è inferito (il task una tantum creato via API parte senza repo e non prova nulla).
- In una regola a percorso va solo ciò che serve mentre si scrive una nota della cartella; ciò che serve per decidere se e dove scrivere (instradamento, matrice delle scritture, dati riservati, dedup delle persone, git) resta in `CLAUDE.md`. Unica regola nuova: `fonti.md` su `sources/**` (percorso, famiglia, versioni, collegamenti). Nessuna regola `people/**`: la dedup si decide con Grep, che non la fa scattare.
- L'ingestor non cambia modo di scrivere: gli script non fanno scattare le regole, ma il corpo lo scrive con Edit/Write e le sue regole stanno nella sua definizione.
- Il risparmio delle regole a percorso è modesto (CLAUDE.md da 11,3 a 10,3 KB); il guadagno vero è nelle copie tolte da `ingestor.md`, `_comune.md`, `curator.md`, `chiudi-sessione`, `/cattura` e `/smista`, che ora rimandano a `CLAUDE.md` §3 e §7.
- `controlla-vault.py` dà errore se una regola ha il frontmatter illeggibile o `paths` non valido (Claude Code la caricherebbe in ogni sessione senza avvisare) e avviso se un pattern punta a una cartella inesistente; 4 test nuovi, 272 in tutto.
- Due PR, unite dall'utente: #49 (vault) e #50 (SPEC 1.24, PR dedicata). Branch canarino cancellato a test finiti; `/context` in una sessione nuova mostra solo `CLAUDE.md`, come atteso (dall'utente).

## File toccati

- `.claude/rules/fonti.md` (nuova); `CLAUDE.md` (§1, §2, §4, §6, §7)
- `.claude/agents/ingestor.md`, `.claude/agents/curator.md`, `.claude/routines/_comune.md`, `.claude/skills/chiudi-sessione/SKILL.md`, `.claude/commands/cattura.md`, `.claude/commands/smista.md`
- `.claude/scripts/controlla-vault.py`, `.claude/scripts/tests/test_controlla_vault.py`
- `SPEC.md` (2.1, 3, 4.1, 4.3, 4.4, 13.1 step 14; versione 1.24)
- `projects/second-brain-prodotto/second-brain-prodotto.md` e `-log.md` (stato e log dello step 14)
- Fuori dal repo: report dell'analisi nello scratchpad della sessione; sessione cloud di test e task una tantum, cancellati

## Aperti

- [x] Primo giro reale dei task con le routine senza rilettura di `CLAUDE.md`: `/verifica-task` sul 2026-10-30 📅 2026-10-30 (chiuso in [[2026-10-30]])
- [ ] Chiudere lo step 14: la matrice delle scritture è ancora in due posti (SPEC §3 e `CLAUDE.md` §3), il perimetro in prosa in SPEC §5 e in `vault.yaml`
- [ ] Rivedere le regole a percorso se una sessione lunga che compatta mostra errori ricorrenti sulle note fonte: la regola non torna dopo `/compact`
