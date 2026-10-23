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
- Soluzione scelta: artifact privato su claude.ai ("Cockpit", https://claude.ai/artifact/KN8Wp48Ja6vGbShXeTpRgR) più, in seguito, una nota `home` in Obsidian con Dataview per la vista dal vivo sul PC.
- Le richieste arrivate per mail non si leggono a parte: l'ingestor le porta già come attività nel vault.
- Calendario: query dal vivo sul connettore Microsoft 365 (oggi + 7 giorni). Progetti e attività: due file JSON generati da `.claude/scripts/plancia.py` e caricati sull'artifact, perché GitHub non è un connettore che la pagina può interrogare.
- Stile: tecnico, blu BlueAge con ciano e ambra come colore complementare per le scadenze.

- La sessione MTU da remoto del 26/10 esce dalle attività: Lorenzo non è coinvolto.
- Il connettore Microsoft 365, interrogato dalla pagina, passa per esteso solo il primo evento della ricerca: la pagina chiede gli altri uno alla volta con l'offset.

## File toccati

- `.claude/scripts/plancia.py` (nuovo): estrae progetti e attività del vault in `progetti.json` e `attivita.json`, fuori dal repo
- `projects/corso-ai-mtu/corso-ai-mtu.md`, `projects/corso-ai-mtu/corso-ai-mtu-log.md`: tolta la sessione del 26/10
- `.claude/routines/cockpit.md` (nuovo): procedura del task schedulato che aggiorna la dashboard
- `home.md` (nuovo), `.claude/scripts/controlla-vault.py` (salta `home.md`), `CLAUDE.md` (riga della tabella)

## Aperti

- [ ] Rivedere il prototipo e decidere layout e contenuti definitivi (dopo il primo giro: nome cambiato in "Cockpit"; corretta la lettura del calendario, che mostrava solo il primo evento)
- [ ] Utente: creare dall'interfaccia di claude.ai il task `cockpit` con il repo NoulegBeis, nessun connettore, ogni giorno alle 07:40 e alle 13:40, prompt standard (`.claude/routines/cockpit.md`). Quello creato da sessione (`trig_01VYihubiEUrsws7nxBm4X6r`, disattivato) partiva senza repo: niente push, niente `.claude/settings.json`, e l'upload sulla dashboard veniva bloccato a intermittenza dal controllo dei permessi. Poi cancellare il vecchio
- `.claude/settings.json`: consentiti `Artifact` e `ArtifactData`, per l'upload del task `cockpit`
- [ ] SPEC 7 e SPEC 8: aggiungere con una PR dedicata il task `cockpit` e la nota `home.md`
- [x] Nota `home.md` per Obsidian con Tasks e Dataview
- [ ] Utente: installare i plugin Tasks e Dataview in Obsidian (ed eventualmente Homepage per aprire `home.md` all'avvio)
