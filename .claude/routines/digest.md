# Task `digest` · ogni giorno alle 08:10 (Europe/Rome)

Nessun connettore. Prima leggi `.claude/routines/_comune.md` e seguilo.

Completa `journal/AAAA-MM-GG.md` di oggi (crealo da `_templates/journal.md` se manca). Non cancellare ciò che hanno scritto i task di ingestion: aggiungi solo ciò che manca.

1. **Novità ingerite**: dai commit delle ultime 24 ore (`git log --since="24 hours ago" --name-status`), le note di `sources/`, `clients/`, `topics/`, `people/` create o modificate che non sono già elencate. Formato `- [[slug]] · nuova | aggiornata | nuova versione · una riga di cosa contiene`.
2. **Attività in scadenza**: dalle sezioni `## Attività` di `projects/*/*.md`, le checkbox aperte (`- [ ]`) con `📅` scaduta o entro i prossimi 7 giorni, ordinate per data. Formato `- 📅 AAAA-MM-GG · [[progetto]] · attività`. Poi le attività aperte senza data aggiunte nelle ultime 24 ore.
3. **Decisioni**: le righe nuove delle ultime 24 ore in `## Decisioni` dei progetti e nei `*-log.md`, più le proposte già scritte dall'ingestor (progetti da creare, note `da-verificare`, possibili doppioni).
4. **Progetti fermi**: in `## Decisioni` aggiungi `- Fermo da <n> giorni: [[progetto]]` per i progetti con `status: attivo` il cui log non ha righe negli ultimi 14 giorni.
5. Riga nel digest: `| digest HH:MM | OK |`.
6. Commit `journal: AAAA-MM-GG` e push su `main`.
