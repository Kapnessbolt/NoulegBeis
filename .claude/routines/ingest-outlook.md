# Task `ingest-outlook` · orari in `vault.yaml` (`task`)

Connettore: Microsoft 365. Prima leggi `.claude/routines/_comune.md` e seguilo.

1. Lancia l'agente `ingestor` con compito `delta`, fonte `outlook`, nessuna da data, modalità `schedulata`. Algoritmo in SPEC 6.3: finestra ed elenchi di scarto in `vault.yaml` (`fonti.outlook`), applicati da `scarta.py`; il giudizio sugli altri scarti in SPEC 5.3.
2. Riga nel digest: `| ingest-outlook HH:MM | OK |` o gli errori. Le mail scartate vanno in `## Scartate` solo fino al 2026-11-06 (prime 2 settimane dall'attivazione).
3. Commit `ingest(outlook): <n> note nuove, <m> aggiornate` e push su `main`.
