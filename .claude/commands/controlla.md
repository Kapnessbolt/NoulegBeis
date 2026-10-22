---
description: Controllo del vault (SPEC 4.4): errori, possibili doppioni, indice per categoria
argument-hint: "[--indice]"
---

Controlla il vault.

1. Esegui `python3 .claude/scripts/controlla-vault.py $ARGUMENTS`.
2. Mostra all'utente il rapporto, raggruppato così:
   - **Errori**: per ognuno la correzione che proponi (campo da aggiungere, file da rinominare, collegamento da sistemare);
   - **Possibili doppioni**: per ogni coppia leggi le due note e di' se sono davvero la stessa cosa; se sì, proponi quale tenere e come unirle (contenuti, collegamenti da aggiornare con `Grep "[[slug-vecchio]]"`);
   - **Altri avvisi**: in breve.
   Con `--indice` riporta anche l'indice.
3. Correggi solo dopo l'ok dell'utente. Dopo le correzioni riesegui lo script, poi commit (`vault: correzioni dal controllo`) e push su `main`.
