---
type: session
date: 2026-10-23
surface: cloud
topics: ["[[ai-nei-processi]]"]
outcome: "Spiegata l'integrazione tra vault e repo di sviluppo; nel CLAUDE.md del repo la regola che ogni modifica a report e kit si ripubblica in Library/"
---

# Integrazione vault e repo di sviluppo: regola di ripubblicazione in Library

## Obiettivo

Capire come il vault e il repo `manini-automazione-ddt` sono collegati nel progetto [[manini-automazione-ddt]], e chiudere il punto debole del collegamento.

## Decisioni

- Ruoli confermati: il repo è il cantiere (report, schema, prompt, script), il vault registra stato, decisioni e attività, OneDrive tiene i dati riservati e le copie condivise in `Progetto Automazione/Library/`
- Il collegamento tra repo e vault passa da OneDrive: il vault non legge GitHub, ma le copie in `Library/` tramite l'ingestion. È un collegamento per convenzione, quindi una copia non ripubblicata lascia indietro le note fonte senza che nessun controllo se ne accorga
- Rimedio leggero adottato: nel `CLAUDE.md` del repo (sezione 5) ogni modifica a `report/` o `kit/` si chiude ripubblicando la copia in `Library/` nella stessa sessione; se non si riesce, si segnala a fine sessione e si aggiunge un'attività nella scheda del progetto
- Scartato il rimedio pesante (script che confronta le date fra repo e OneDrive): per un solo progetto non vale il costo

## File toccati

- Repo `manini-automazione-ddt`: `CLAUDE.md`, sezione 5 (commit `cc9ee7d` su `main`)
- `sessions/2026-10-23-regola-library.md` (questo diario)

## Aperti

- [x] Spunto per il curator, già aperto in [[2026-10-23-manini-automazione-ddt]]: una regola su come portare un Project claude.ai nel vault (repo dedicato, dati su OneDrive, essenziale come nota hub), da includere con la regola di ripubblicazione in `Library/` se lo schema si replica su altri clienti (proposta [[2026-10-25-progetto-claude-ai-nel-vault]])
