---
type: session
date: 2026-10-22
surface: cloud
topics: []
outcome: "SPEC 1.3: persone create dai task, schede progetto rinominate, controllo del vault"
---

# Persone automatiche, schede progetto e controllo del vault

## Obiettivo

Chiarire la differenza tra ingestion lanciata a mano e task automatici, far creare le persone anche ai task e introdurre un controllo che faccia emergere doppioni ed errori.

## Decisioni

- I task di ingestion creano le persone (mittenti e destinatari in A), dopo aver cercato la stessa email in `people/`. Un nome simile senza email coincidente non crea niente e diventa una segnalazione nel digest. Clienti e temi restano proposte nel digest.
- La scheda progetto diventa `projects/<slug>/<slug>.md` e il log `<slug>-log.md`: con `_index.md` il wikilink `[[<slug>]]` non apriva la scheda in Obsidian.
- Nuovo script `.claude/scripts/controlla-vault.py` (SPEC 4.4): errori bloccanti e avvisi, opzione `--indice`. Gira prima di ogni commit, nella riconciliazione settimanale e con `/controlla`.
- Al primo giro lo script ha trovato un errore vero: `outcome` non quotato nel diario dello step 2 (YAML non valido). Corretto.

## File toccati

- `SPEC.md` (1.3), `CLAUDE.md`, `README.md`
- `.claude/agents/ingestor.md`, `.claude/commands/controlla.md`, `.claude/scripts/controlla-vault.py`, `.claude/settings.json`
- `_templates/journal.md`
- `sessions/2026-10-22-step-2-ingestor.md`

## Aperti

- [x] Script di setup dell'ambiente cloud: installare `pyyaml` (oggi è già presente nell'immagine, ma non è garantito) (chiuso in [[2026-10-26]]: l'hook di avvio lo installa se manca)
- [ ] Rivedere la soglia dei nomi simili (0,85) dopo il primo caricamento delle mail
