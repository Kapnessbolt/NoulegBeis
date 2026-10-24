---
type: proposal
date: 2026-10-25
kind: regola
status: proposta
---

# Regola per portare nel vault un progetto nato in un Project claude.ai

## Motivazione

Spunto esplicito per il curator, scritto in due diari. Il caso DDT di [[manini]] è passato da un Project claude.ai a un progetto del vault con uno schema scelto dopo aver scartato due alternative (tutto nel vault, submodule): repo dedicato, dati reali solo su OneDrive, sintesi "essenziale" come nota hub, copie condivise in `Library/`. Oggi lo schema esiste solo nel diario e nel `CLAUDE.md` del repo di Manini. Al prossimo Project da portare dentro (un altro corso, un altro cliente) la scelta andrebbe rifatta da zero, con il rischio di dati reali su GitHub. Un solo caso finora: se preferisci aspettare il secondo, lasciala `proposta`.

## Evidenze

- [[2026-10-23-manini-automazione-ddt]]: progetto [[manini-automazione-ddt]] creato dal Project claude.ai; repo dedicato, dati reali solo in `Progetto Automazione/Dati/` su OneDrive, master nel repo e copie in `Library/`; aperto "Spunto per il curator: una regola su come portare un Project claude.ai nel vault".
- [[2026-10-23-regola-library]]: il collegamento repo-vault passa da OneDrive ed è solo una convenzione; nel `CLAUDE.md` del repo la regola di ripubblicare in `Library/`; stesso spunto, "da includere con la regola di ripubblicazione".
- [[2026-10-24]]: l'ingest-sharepoint trova i DDT reali in `Dati/` e li salta per scelta propria, senza una regola scritta (vedi [[2026-10-25-dati-riservati-fuori-dal-vault]]).

## Testo proposto

`CLAUDE.md` §2, in coda alle regole di instradamento:

```markdown
- Lavoro nato in un Project claude.ai (o in un'altra chat lunga) che diventa un progetto. La scheda va in `projects/<slug>/` come sempre. Il lavoro tecnico (report, schema, prompt, script) va in un repo GitHub privato dedicato, mai nel vault né come submodule. I dati reali del cliente stanno solo su OneDrive, in `01_Materiale clienti/<Cliente>/<Progetto>/Dati/`, mai su GitHub. La sintesi del Project va in un file `<cliente>_<progetto>_essenziale.md` nella cartella del cliente su OneDrive: l'ingestion ne fa la nota hub del progetto.
- Il master di report e kit è il repo. Le copie condivise stanno in `<Progetto>/Library/` su OneDrive, e da lì l'ingestion crea le note fonte. Nel `CLAUDE.md` del repo scrivi la regola: ogni modifica a report o kit si chiude ripubblicando la copia in `Library/` nella stessa sessione; se non si riesce, un'attività nella scheda del progetto.
- La scheda del progetto riporta il link al repo e non ne copia il dettaglio: stato, decisioni e attività citano le note di `Library/`, l'essenziale o il diario.
```
