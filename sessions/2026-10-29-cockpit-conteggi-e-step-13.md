---
type: session
date: 2026-10-29
surface: cloud
topics: ["[[second-brain]]"]
outcome: "Tre difetti di conteggio del Cockpit corretti con i test (PR 1); step 13 in corso"
---

# Conteggi del Cockpit e step 13

## Obiettivo

Correggere i tre difetti di conteggio del Cockpit in scadenza il 31/10, ognuno con un test che fallisce prima e passa dopo; poi lo step 13 di SPEC 13.1 (configurazione separata dal motore in `vault.yaml`), una PR per punto.

## Decisioni

- Il codice dei tre difetti lo scrive un subagente Opus, la sessione rivede (dall'utente).
- Una nuova versione di un documento conta tra le note aggiornate, non tra le nuove: il Cockpit mostra "N note nuove · M aggiornate".
- Le decisioni del digest si contano tutte, con o senza data, tranne le righe che dicono solo che non c'è nulla ("Nessun progetto fermo…").
- Il giro del cockpit che genera la pagina è "In corso" nella pagina stessa e non entra nel totale "task OK su N"; la correzione sta in `cockpit.py` perché solo la pagina sa di essere quel giro, `/oggi` e `/verifica-task` restano su `task.json`.

## File toccati

- `.claude/scripts/plancia.py`, `.claude/scripts/cockpit.py`, `.claude/routines/cockpit.md`
- `.claude/scripts/tests/test_plancia.py`, `.claude/scripts/tests/test_cockpit.py`
- `projects/second-brain-prodotto/second-brain-prodotto.md`, `projects/second-brain-prodotto/second-brain-prodotto-log.md`

## Aperti

- [ ] Formato delle novità nel digest: righe aggregate del 29/10 (`Nuove (45): …`) non contate dal Cockpit
