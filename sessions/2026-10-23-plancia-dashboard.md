---
type: session
date: 2026-10-23
surface: cloud
topics: []
outcome: "Prototipo della plancia personale: artifact Dashboard su claude.ai con calendario Outlook dal vivo e progetti e attività dal vault"
---

# Plancia personale: prototipo della dashboard

## Obiettivo

Avere una vista di riepilogo sempre disponibile: calendario della settimana, progetti aperti, attività e scadenze.

## Decisioni

- La dashboard mostra i dati, non li ospita: la fonte resta il vault (attività in `## Attività` delle schede progetto) e Outlook per il calendario. Notion scartato perché diventerebbe una seconda fonte da sincronizzare.
- Soluzione scelta: artifact privato su claude.ai ("Plancia Lorenzo", https://claude.ai/artifact/KN8Wp48Ja6vGbShXeTpRgR) più, in seguito, una nota `home` in Obsidian con Dataview per la vista dal vivo sul PC.
- Le richieste arrivate per mail non si leggono a parte: l'ingestor le porta già come attività nel vault.
- Calendario: query dal vivo sul connettore Microsoft 365 (oggi + 7 giorni). Progetti e attività: due file JSON generati da `.claude/scripts/plancia.py` e caricati sull'artifact, perché GitHub non è un connettore che la pagina può interrogare.
- Stile: tecnico, blu BlueAge con ciano e ambra come colore complementare per le scadenze.

## File toccati

- `.claude/scripts/plancia.py` (nuovo): estrae progetti e attività del vault in `progetti.json` e `attivita.json`, fuori dal repo

## Aperti

- [ ] Rivedere il prototipo e decidere layout e contenuti definitivi
- [ ] Task schedulato nei giorni feriali che rigenera i JSON con `plancia.py` e li ricarica sull'artifact
- [ ] Nota `home` per Obsidian con Dataview e Tasks
