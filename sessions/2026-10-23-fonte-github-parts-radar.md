---
type: session
date: 2026-10-23
surface: cloud
topics: ["[[parts-radar]]"]
outcome: "Fonte GitHub nel vault (SPEC 5.4, 6.6), task ingest-github e primo caricamento del repo parts-radar"
---

# Fonte GitHub: il repo di Parts Radar nel vault

## Obiettivo

Portare nel vault lo stato del progetto [[parts-radar-sviluppo]] che vive nel repo di sviluppo `cristian-schifone/parts-radar` (circa 90 documenti, 3-6 voci di changelog al giorno) e decidere come mantenerlo aggiornato.

## Decisioni

- Scartata la copia su OneDrive (modello Manini): il repo è condiviso con Cristian e cambia più volte al giorno, nessuno pubblicherebbe le copie
- Scartato un passo in `/update-docs` del repo: tocca comandi condivisi e le sessioni di sviluppo non hanno il vault
- Scelta: GitHub come nuova fonte del vault (`source: github`), con un elenco chiuso di file e issue (SPEC 5.4) e un task giornaliero `ingest-github` alle 07:20 (SPEC 6.6). Nel vault va solo il livello di progetto
- Dal changelog del repo: una sola riga al giorno nel log del progetto, non una per PR; le azioni fuori dal codice vanno in `## Attività`
- Le caselle spuntate nel repo non si spuntano da sole nel vault (il task scrive solo righe nuove): finiscono nel digest come "Da spuntare"
- Contesto ADAC appreso in sessione dal `CLAUDE.md` del repo: Claudio Degli Esposti è il titolare, Luca Degli Esposti il vice e referente per informazioni e dati; nel repo Lorenzo ha l'ultima parola su pipeline, modelli e prompt, Cristian su database e dati

## File toccati

- `SPEC.md` (3, 4.2, 4.4, 5.4 nuova, 6.1, 6.6 nuova, 7, 13), `CLAUDE.md` (§2, §6), `README.md`, `_templates/source-doc.md`
- `.claude/scripts/controlla-vault.py`, `.claude/agents/ingestor.md` (sezione 5b), `.claude/commands/ingest.md`, `.claude/routines/ingest-github.md` (nuovo), `.claude/settings.json`, `.state/ingest.json`
- 8 note fonte in `sources/github/parts-radar/`
- [[parts-radar-sviluppo]] (stato, attività, decisioni, prossimi passi riscritti col repo) e il suo log; [[parts-radar]], [[adac-bologna]]; persone nuove [[luca-degli-esposti]] e [[claudio-degli-esposti]]

## Aperti

- [x] Fare il merge della PR della fonte GitHub (PR #12, 23/10)
- [x] Creare su claude.ai il task schedulato `ingest-github` (ogni giorno alle 07:20, Opus, sorgenti: NoulegBeis e parts-radar, connettore GitHub) con il prompt standard di SPEC 7: creato il 23/10 come `Ingest-github`, primo giro il 24/10 alle 07:20
- [x] Verificare il primo giro del task 📅 2026-10-24: riga `ingest-github` nel digest, watermark avanzato, una riga di log per il 23/10, nessuna attività doppia (chiuso in [[2026-10-24]])
- [ ] Email di Luca e Claudio Degli Esposti da aggiungere alle loro note
