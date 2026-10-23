# Task `ingest-github` · ogni giorno alle 07:20 (Europe/Rome)

Sorgenti del task: il vault e i repo elencati in SPEC 5.4 (oggi `cristian-schifone/parts-radar`). Connettore: GitHub, solo in lettura. Prima leggi `.claude/routines/_comune.md` e seguilo: il punto 5 sul connettore Microsoft 365 qui vale per il clone del repo e per il connettore GitHub.

1. Lancia l'agente `ingestor` con compito `delta`, fonte `github`, nessuna da data, modalità `schedulata`. Algoritmo in SPEC 6.6, procedura nella sezione 5b dell'agente.
2. Riga nel digest: `| ingest-github HH:MM | OK |` o gli errori (repo non clonato, connettore GitHub assente).
3. Commit `ingest(github): <n> note nuove, <m> aggiornate` e push su `main`. Nel repo di progetto non si scrive mai.
