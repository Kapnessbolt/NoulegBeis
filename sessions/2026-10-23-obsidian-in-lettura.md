---
type: session
date: 2026-10-23
surface: cloud
topics: []
outcome: "Obsidian solo in lettura su PC e telefono; .obsidian/ fuori dal repo; guida di installazione data all'utente"
---

# Obsidian in sola lettura su PC e telefono

## Obiettivo

Collegare Obsidian al vault per navigarlo (link, backlink, grafo, ricerca, attività) da PC e telefono.

## Decisioni

- Obsidian si usa solo in lettura: modifiche e creazioni di note passano sempre da Claude (dall'utente).
- Sincronizzazione solo in pull con il plugin Obsidian Git, su PC e telefono: niente commit, niente push dai dispositivi, quindi nessun conflitto con ingestor e sessioni.
- `.obsidian/` è tutta fuori dal repo (`.gitignore`): ogni dispositivo ha la sua configurazione, e un'impostazione cambiata in locale non blocca il pull.
- Non serve `git config core.hooksPath .githooks` sui dispositivi, perché da lì non parte nessun commit.

## File toccati

- `.gitignore`

## Aperti

- [ ] Utente: installare Obsidian e Obsidian Git su PC e telefono e fare il primo pull
- [ ] SPEC 8, step 8: quando il setup funziona, aggiornare con una PR il punto aperto sulla sincronizzazione mobile (soluzione: Obsidian Git solo in pull)
