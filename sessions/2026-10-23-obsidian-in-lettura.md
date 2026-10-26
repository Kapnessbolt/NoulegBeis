---
type: session
date: 2026-10-23
surface: cloud
topics: []
outcome: "Obsidian solo in lettura; .obsidian/ fuori dal repo; telefono Android configurato e pull funzionante, PC rimandato"
---

# Obsidian in sola lettura su PC e telefono

## Obiettivo

Collegare Obsidian al vault per navigarlo (link, backlink, grafo, ricerca, attività) da PC e telefono.

## Decisioni

- Obsidian si usa solo in lettura: modifiche e creazioni di note passano sempre da Claude (dall'utente).
- Sincronizzazione solo in pull con il plugin Obsidian Git, su PC e telefono: niente commit, niente push dai dispositivi, quindi nessun conflitto con ingestor e sessioni.
- `.obsidian/` è tutta fuori dal repo (`.gitignore`): ogni dispositivo ha la sua configurazione, e un'impostazione cambiata in locale non blocca il pull.
- Non serve `git config core.hooksPath .githooks` sui dispositivi, perché da lì non parte nessun commit.
- Telefono Android configurato: token GitHub fine-grained in sola lettura (Contents: Read-only, solo `NoulegBeis`), clone con Obsidian Git nella radice del vault, pull all'avvio e ogni 10 minuti, commit e push automatici a 0, vista di lettura di default. Pull verificato.
- File esclusi in Obsidian: `_templates/` e `sessions/_raw/`. Le cartelle che iniziano con il punto (`.state/`, `.claude/`) Obsidian non le indicizza da sé.
- Grafo globale con filtro `-path:sources -path:journal -path:sessions` e un gruppo colore per `projects`, `clients`, `people`, `topics`; per la navigazione quotidiana il grafo locale (profondità 1-2), i backlink e i segnalibri sulle schede dei progetti attivi.

## File toccati

- `.gitignore`

## Aperti

- [ ] Utente: configurare Obsidian sul PC (Git per Windows, clone, plugin Obsidian Git solo in pull), più avanti
- [x] Valutare una nota cruscotto con Tasks e Dataview (attività in scadenza, progetti attivi): serve prima una regola sul `type` (chiuso in [[2026-10-23-plancia-dashboard]])
- [x] SPEC 8, step 8: quando il setup funziona, aggiornare con una PR il punto aperto sulla sincronizzazione mobile (soluzione: Obsidian Git solo in pull) (chiuso in [[2026-10-26-spec-e-readme-allineati]])
