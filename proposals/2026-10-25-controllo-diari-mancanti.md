---
type: proposal
date: 2026-10-25
kind: agente
status: accettata
---

# Il curator controlla i diari mancanti al posto dell'hook Stop sulle trascrizioni

## Motivazione

SPEC §12 prevede come rete di sicurezza dei diari un hook `Stop` che copia la trascrizione in `sessions/_raw/`. L'hook non esiste, `sessions/_raw/` è vuota, e se esistesse porterebbe nel repo trascrizioni intere con dati riservati (`CLAUDE.md` §5). L'aperto è stato riscritto in due diari a tre giorni di distanza senza una decisione. Oggi una sessione che cambia il vault senza `/chiudi-sessione` non lascia traccia nei diari e nessuno se ne accorge. La proposta sposta la rete di sicurezza sui dati che il vault ha già: i commit. Il curator, che legge già `git log` della finestra, segnala i commit `session: <slug>` senza diario e i giorni con commit interattivi (`vault:`, `project(…)`, `spec:`) senza alcun diario. Nessun dato nuovo nel repo, nessun hook. Sulla settimana 18–25/10 il controllo non trova buchi: tutti e 7 gli slug dei commit `session:` hanno il loro diario.

## Evidenze

- [[2026-10-22-watermark-e-task-schedulati]]: aperto "valutare la raccolta delle sessioni via trascrizione (elenco sessioni della settimana → diari mancanti in `sessions/`) al posto dell'hook `Stop`"; il test mostra che le trascrizioni si leggono, ma restano fuori dal repo.
- [[2026-10-25-cockpit-v05-smistamento]]: aperto "l'hook che copia le trascrizioni in `sessions/_raw/` non esiste e porterebbe nel repo dati riservati (§5). Valutare al suo posto un controllo dei giorni con commit di sessione ma senza diario (curator o `/verifica-task`), con una PR sulla SPEC §12".
- [[2026-10-24-cockpit-in-locale]]: l'unico hook `Stop` che esiste è `promemoria-fine-turno.sh` (commit e push), non copia trascrizioni.

## Testo proposto

In `.claude/agents/curator.md`, sezione 2 (Cosa leggi), un punto in più dopo il 4:

```markdown
5. Diari mancanti: dai commit della finestra prendi gli slug dei messaggi `session: <slug>` (fino alla prima virgola) e controlla che esista `sessions/*-<slug>.md`. Poi i giorni (Europe/Rome) con commit `vault:`, `project(…)` o `spec:` e nessun diario con quella `date`. Non scrivere diari al posto della sessione: elenca ciò che manca nel resoconto, tra i "Da verificare".
```

In `.claude/agents/curator.md`, sezione 6, voce **Da verificare**, in coda:

```markdown
, commit di sessione o giorni di lavoro interattivo senza diario (sezione 2, punto 5)
```

In `SPEC.md` §12, con una PR dedicata, la riga della rete di sicurezza diventa:

```markdown
- Rete di sicurezza: il curator segnala ogni settimana i commit `session: <slug>` senza diario e i giorni con commit interattivi senza diario (9.2). Niente trascrizioni nel repo: porterebbero dati riservati (`CLAUDE.md` §5). `sessions/_raw/` resta solo per estratti puntuali.
```

Applicata il 26/10 con una variante: il controllo è per commit e non per giorno (un diario dello stesso giorno o del giorno dopo deve citare lo slug del progetto o un file toccato). Il controllo per giorno non vedeva il commit `project(manini-automazione-ddt)` delle 23:30 del 25/10, fatto in una sessione senza diario in un giorno che aveva già altri diari.
