# Task `digest` · ogni giorno alle 07:45 (Europe/Rome)

Nessun connettore. Prima leggi `.claude/routines/_comune.md` e seguilo.

Completa `journal/AAAA-MM-GG.md` di oggi (crealo da `_templates/journal.md` se manca). Non cancellare ciò che hanno scritto i task di ingestion: aggiungi solo ciò che manca.

**Finestra**: i commit successivi all'ultimo commit del digest, `B=$(git log -1 --format=%H --grep='^journal: ')`, cioè `git log $B..HEAD`. Se non c'è un commit `journal:`, le ultime 24 ore. Nei punti seguenti "nella finestra" vuol dire questo.

1. **Novità ingerite**: dai commit nella finestra (`git log $B..HEAD --name-status`), le note di `sources/`, `clients/`, `topics/`, `people/` create o modificate che non sono già elencate nel digest di oggi né in quello di ieri (lo scrive l'ingest-outlook delle 13:15). Formato `- [[slug]] · nuova | aggiornata | nuova versione · una riga di cosa contiene`. Oltre 30 voci: elenca per esteso solo le note nuove di `clients/` e `topics/` e le nuove versioni; per il resto una riga per cartella con il numero (`- sources/mail: 42 nuove, 3 aggiornate`).
2. **Attività in scadenza**: dalle sezioni `## Attività` di `projects/*/*.md`, le checkbox aperte (`- [ ]`) con `📅` scaduta o entro i prossimi 7 giorni, ordinate per data; quelle scadute da più di 14 giorni in coda, sotto `Scadute da più di 14 giorni (chiudere o riprogrammare):`. Formato `- 📅 AAAA-MM-GG · [[progetto]] · attività`. Poi le attività aperte senza data aggiunte nella finestra (oltre 15: solo il numero per progetto).
3. **Decisioni**: le righe nuove nella finestra in `## Decisioni` dei progetti e nei `*-log.md`, più le proposte già scritte dall'ingestor (progetti da creare, note `da-verificare`, possibili doppioni).
4. **Progetti fermi**: in `## Decisioni` aggiungi `- Fermo da <n> giorni: [[progetto]]` per i progetti con `status: attivo` il cui log non ha righe negli ultimi 14 giorni.
5. Riga nel digest: `| digest HH:MM | OK |`, con l'ora di `TZ=Europe/Rome date +%H:%M`.
6. Commit `journal: AAAA-MM-GG` e push su `main`.
