---
type: session
date: 2026-10-25
surface: locale
topics: ["[[second-brain]]"]
outcome: "Mod cockpit v0.5.0 installata e provata; sul telefono le mod non compaiono; dashboard e mod convivono; nota inbox sulla mod smistata nel tema second-brain"
---

# Mod cockpit v0.5.0 e smistamento della nota inbox

## Obiettivo

Chiudere gli aperti sulla mod `cockpit` dopo l'installazione della v0.5.0 e smistare la nota inbox che ne seguiva l'idea.

## Decisioni

- Mod `cockpit` v0.5.0 installata da Lorenzo e provata sul desktop: pannello, sezione Agenti e consumo del piano riletto dopo una risposta funzionano.
- Prova sul telefono: le mod non compaiono, nemmeno seguendo una sessione locale. Per Lorenzo non è un problema: dal telefono c'è la dashboard.
- La mod non sostituisce la dashboard Cockpit, dall'utente: convivono, la dashboard con un livello di dettaglio diverso, la mod come parte operativa al PC. Le routine `DailyBoard` restano.
- Nota inbox `2026-10-24-mod-claude-cockpit` smistata nel tema [[second-brain]] (interfaccia della versione personale, limiti delle mod, alternative scartate) e tolta da `inbox/`, dall'utente: con tutti gli aperti chiusi non c'era più niente da smistare. La SPEC non prevede un archivio per l'inbox; il testo resta nella storia git. I due wikilink che la citavano ora puntano al tema e a questo diario.
- Il vault è anche il banco di prova del prodotto Second Brain, dall'utente: nel tema [[second-brain]] una sezione `## Versione personale e banco di prova` (fuori dal template dei temi) raccoglie quello che funziona e i limiti trovati qui, perché orientano l'offerta. Si arricchisce man mano.

## File toccati

- `topics/second-brain.md`
- `inbox/2026-10-24-mod-claude-cockpit.md` (aggiornata, poi tolta)
- `sessions/2026-10-24-restyling-cockpit-implementazione.md`, `sessions/2026-10-24-interfaccia-personalizzata.md` (aperti chiusi, link)
- `sessions/2026-10-25-cockpit-v05-smistamento.md` (nuovo)

## Aperti

- [ ] SPEC 1, riga "Pannello locale": descrive ancora la mod v0.2 (calendario, scadenze, progetti). Aggiornarla alla v0.5.0 (piano Max, task, prossime cose, agenti), dire che non compare sul telefono e che convive con la dashboard; verificare se `/cockpit` esiste ancora (PR dedicata)
