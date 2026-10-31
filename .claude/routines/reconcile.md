# Task `reconcile` · orari in `vault.yaml` (`task`)

Connettore: Microsoft 365. Prima leggi `.claude/routines/_comune.md` e seguilo.

1. Lancia l'agente `ingestor` con compito `riconcilia`, fonte `tutte`, modalità `schedulata`. Algoritmo in SPEC 6.4 (completa): per ogni libreria del perimetro e per la cartella di OneDrive, elenco delle cartelle dal connettore, piano con `riconcilia.py`, `--applica`, le voci `recupera` lette e riassunte dall'agente, controllo del vault. Una libreria per volta nell'ordine di `fonti.canoniche`, con commit e push a libreria finita come in `reconcile-ridotta.md`.
2. A fine giro `python3 .claude/scripts/stato.py set-last-run <adesso UTC>` e `set-riconciliata` per ogni libreria dovuta riconciliata fino in fondo.
3. Riga nel digest: `| reconcile HH:MM | OK · <n> note spostate, <m> rimosse, <k> recuperate, <j> in coda |` o gli errori; il rapporto di `controlla-vault.py` va in `## Controllo del vault`.
4. Commit `ingest(riconcilia): <n> note aggiornate` e push su `main`.
