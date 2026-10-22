# Task `ingest-sharepoint` · ogni giorno alle 06:50 (Europe/Rome)

Connettore: Microsoft 365. Prima leggi `.claude/routines/_comune.md` e seguilo.

1. Lancia l'agente `ingestor` con compito `delta`, fonti `sharepoint` e `onedrive` (una sola ricerca, smistata per `webUrl`; si aggiornano entrambi i watermark), nessuna da data, modalità `schedulata`. Algoritmo in SPEC 6.2.
2. Riga nel digest: `| ingest-sharepoint HH:MM | OK |` o gli errori.
3. Commit `ingest(sharepoint): <n> note nuove, <m> aggiornate` e push su `main`.
