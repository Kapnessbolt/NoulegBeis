# Task `reconcile` · orari in `vault.yaml` (`task`)

Connettore: Microsoft 365. Prima leggi `.claude/routines/_comune.md` e seguilo.

1. Lancia l'agente `ingestor` con compito `riconcilia`, fonte `tutte`, modalità `schedulata`. Algoritmo in SPEC 6.4: confronto delle cartelle del perimetro con lo stato (`stato.py elenco <fonte>`), note rimosse o spostate, file mai ingeriti, controllo del vault.
2. Riga nel digest: `| reconcile HH:MM | OK |` o gli errori; il rapporto di `controlla-vault.py` va in `## Controllo del vault`.
3. Commit `ingest(riconcilia): <n> note aggiornate` e push su `main`.
