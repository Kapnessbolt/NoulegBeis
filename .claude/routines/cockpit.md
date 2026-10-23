# Task `cockpit` · ogni giorno alle 07:40 e alle 13:40 (Europe/Rome)

Nessun connettore. Gira dopo gli ingest del mattino e dopo l'ingest-outlook delle 13:15.

Aggiorna i dati del vault nella dashboard **Cockpit** (artifact di tipo Dashboard): https://claude.ai/artifact/KN8Wp48Ja6vGbShXeTpRgR. Il calendario la dashboard lo legge da sé dal connettore Microsoft 365: questo task non lo tocca.

**Eccezione a `_comune.md`**: il task legge il vault e non scrive nel repo. Niente riga nel digest, niente commit, niente push: il task è creato senza il repo in scrittura. L'esito si vede nella dashboard, dove ogni fonte riporta l'ora dell'ultimo aggiornamento e diventa "vecchia" se il task salta i giri. Del file comune valgono solo l'avvio (clone fresco di `main`) e il lavoro senza domande.

1. **Avvio**: se `/home/user/NoulegBeis` non c'è, `git clone https://github.com/Kapnessbolt/NoulegBeis.git /home/user/NoulegBeis`; poi lavora lì su `origin/main` aggiornato. Carica `ArtifactData` con ToolSearch (`select:ArtifactData`) se non è caricato.
2. `OUT=$(mktemp -d)` e `python3 .claude/scripts/plancia.py "$OUT"`: scrive `progetti.json` e `attivita.json`.
3. Per ciascun dataset, `progetti` e poi `attivita`:
   1. `ArtifactData` `get`, collection `datasets`, doc_id `<dataset>`: tieni `version` e il vecchio `source.url` (`/_blob/<id>`).
   2. `Artifact` publish con `url` della dashboard, `asset: true`, `file_path` `$OUT/<dataset>.json`: tieni il nuovo `url` (`/_blob/<id nuovo>`).
   3. `ArtifactData` `update`, collection `datasets`, doc_id `<dataset>`, `if_version` del punto 1, data `{"source": {"kind": "file", "url": "<url nuovo>", "name": "<dataset>.json"}, "updated": {"at": "<ora UTC ISO 8601>", "by": "task cockpit"}}`.
   4. Solo se l'update è riuscito: `Artifact` delete con `url` della dashboard e `path` l'id del vecchio file (i 32 caratteri dopo `_blob/`). Se la cancellazione viene negata, lascia stare e vai avanti: un file vecchio rimasto non rompe nulla.
4. Non toccare `files/index.html`, `dash/meta` né il dataset `calendario`. Non riprovare un passo fallito più di una volta.
5. **Risposta finale**: due righe con l'esito (progetti e attività caricati, file vecchi cancellati o rimasti, errori).
