# Task `ingest-sharepoint` · orari in `vault.yaml` (`task`)

Connettore: Microsoft 365. Prima leggi `.claude/routines/_comune.md` e seguilo.

1. Lancia l'agente `ingestor` con compito `delta`, fonti `sharepoint` e `onedrive` (una sola ricerca, smistata per `webUrl`; si aggiornano entrambi i watermark), nessuna da data, modalità `schedulata`. Algoritmo in SPEC 6.2, compreso il rilevatore di riordino (passo 7): se scatta, l'agente lascia il segnale in `riconciliazione_dovuta` e lo scrive nel digest; la riconciliazione la fa il task `reconcile-ridotta` (SPEC 7), non questo giro.
2. Riga nel digest: `| ingest-sharepoint HH:MM | OK |` o gli errori; con un riordino rilevato, `OK · riordino in <libreria>, riconciliazione dovuta`.
3. Commit `ingest(sharepoint): <n> note nuove, <m> aggiornate` e push su `main`.
