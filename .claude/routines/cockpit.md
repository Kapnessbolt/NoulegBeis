# Task `cockpit` · ogni giorno alle 07:40 e alle 13:40 (Europe/Rome)

Nessun connettore. Prima leggi `.claude/routines/_comune.md` e seguilo (avvio, digest, errori, git). Gira dopo gli ingest del mattino e dopo l'ingest-outlook delle 13:15.

Aggiorna i dati del vault nella dashboard **Cockpit** (artifact di tipo Dashboard): https://claude.ai/artifact/KN8Wp48Ja6vGbShXeTpRgR. Il calendario la dashboard lo legge da sé dal connettore Microsoft 365: questo task non lo tocca. Non modifica note del vault: scrive solo la riga d'esito nel digest. Carica `ArtifactData` con ToolSearch (`select:ArtifactData`) se non è caricato.

1. `OUT=$(mktemp -d)` e `python3 .claude/scripts/plancia.py "$OUT"`: scrive `progetti.json` e `attivita.json`.
2. Per ciascun dataset, `progetti` e poi `attivita`:
   1. `ArtifactData` `get`, collection `datasets`, doc_id `<dataset>`: tieni `version` e il vecchio `source.url` (`/_blob/<id>`).
   2. `Artifact` publish con `url` della dashboard, `asset: true`, `file_path` `$OUT/<dataset>.json`: tieni il nuovo `url` (`/_blob/<id nuovo>`).
   3. `ArtifactData` `update`, collection `datasets`, doc_id `<dataset>`, `if_version` del punto 1, data `{"source": {"kind": "file", "url": "<url nuovo>", "name": "<dataset>.json"}, "updated": {"at": "<ora UTC ISO 8601>", "by": "task cockpit"}}`.
   4. Solo se l'update è riuscito: `Artifact` delete con `url` della dashboard e `path` l'id del vecchio file (i 32 caratteri dopo `_blob/`). Se la cancellazione viene negata, segnalalo nel digest e vai avanti: un file vecchio rimasto non rompe nulla.
3. Non toccare `files/index.html`, `dash/meta` né il dataset `calendario`. Non riprovare un passo fallito più di una volta: se uno strumento manca o un passo fallisce, scrivi nel digest quale e perché.
4. Riga nel digest: `| cockpit HH:MM | OK · <n> progetti, <n> attività |`, oppure l'errore.
5. Commit `cockpit: AAAA-MM-GG HH:MM` (non `journal:`, che il digest usa per la sua finestra) e push su `main`.
