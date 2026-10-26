---
type: session
date: 2026-10-26
surface: cloud
topics: ["[[second-brain]]"]
outcome: "README, routine del curator, CLAUDE.md §7 e /verifica-task allineati ai file reali su main; SPEC 1.16 nella PR #22"
---

# SPEC e README allineati ai file reali

## Obiettivo

Verificare sul repo le differenze tra `SPEC.md`, `README.md` e i file reali, poi correggere il README direttamente e la SPEC con una PR dedicata.

## Decisioni

- Verificati tutti e 9 i punti segnalati dall'utente. Una precisazione sul punto 6: `ingest(file)` non viene da una routine ma dall'agente `ingestor` (compito `file`, cioè `/ingest-file`). Trovato in più che mancava anche `spec:` tra i prefissi di §11
- README riscritto: tolti `/cattura`, `/smista`, `/oggi` e `/progetto` come comandi esistenti (ora sono elencati come previsti, con le skill dello step 6); l'ingestion automatica è attiva dal 23/10; Obsidian in sola lettura con Obsidian Git solo in pull, e `core.hooksPath` non serve sui dispositivi; aggiunti `.githooks/` e `.github/workflows/` alla tabella delle cartelle; Cockpit e `/cockpit` della mod
- Branch del curator schedulato allineato alla scelta del 26/10 ([[2026-10-26-diari-mancanti-e-vault-sola-lettura]]): la routine usa il branch assegnato alla sessione e `claude/curator-AAAA-MM-DD` solo se la sessione non ne assegna uno. Allineati anche `CLAUDE.md` §7 e `/verifica-task`, che cercavano la PR del curator per nome del branch: ora la cerca per titolo (`curator: settimana …`). `/curator` a mano resta su `claude/curator-AAAA-MM-DD`
- SPEC 1.16 (PR #22): Obsidian in sola lettura in §2 e §4.4; decisione aperta sulla sincronizzazione su mobile tolta da §14, perché il telefono funziona in pull dal 23/10; step 8 aperto solo per il PC; `.githooks/` nell'albero di §3; branch del curator in §7 e §9.2; in §8 i comandi previsti ma non ancora fatti e `/cockpit` della mod, che vive fuori dal repo; 6.6 in §9.1; colonna Stato in §10 con le tre skill BlueAge "previste"; tabella completa dei prefissi di commit in §11
- Tolto `.claude/skills/.gitkeep`: la cartella contiene già `chiudi-sessione`

## File toccati

- `README.md`, `CLAUDE.md` (§7)
- `.claude/routines/curator.md`, `.claude/commands/verifica-task.md`; `.claude/skills/.gitkeep` cancellato
- `SPEC.md`: versione 1.16, sul branch `claude/beautiful-edison-1yu80b` (PR #22)

## Aperti

- [x] Utente: rivedere e unire la PR #22 (SPEC 1.16); dopo il merge spuntare l'ultimo aperto di [[2026-10-23-obsidian-in-lettura]] (sincronizzazione su mobile nella SPEC) (chiuso: PR #22 unita)
- [ ] Le skill `blueage-deck`, `blueage-corso` e `blueage-animazioni` compaiono già nelle sessioni cloud come plugin claude.ai (`anthropic-skills:*`): valutare se lo step 6 (copia in `.claude/skills/`) serve ancora o se la SPEC §2 ("`/plugin` non è disponibile") va rivista
