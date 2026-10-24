---
type: session
date: 2026-10-25
surface: locale
topics: ["[[second-brain]]"]
outcome: "Mod cockpit v0.5.0 installata e provata; sul telefono le mod non compaiono; dashboard e mod convivono; nota inbox smistata nel tema second-brain con la sezione sul banco di prova; PR #19 sulla SPEC (1.14)"
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
- PR #19 sulla SPEC (1.14): righe del Cockpit in §2 aggiornate alla mod v0.5.0 e alla dashboard con i nuovi dataset, riga `cockpit` di §7 con tutti i dataset di `plancia.py`, sezione facoltativa `## Versione personale e banco di prova` per i temi in §4.2. La sezione resta fuori dal template dei temi: ce l'ha un solo tema, e nel template comparirebbe in tutti. Verificato nella mod che `/cockpit` esiste ancora e dà il riepilogo in testo quando il pannello non si apre.
- Step 5, ponte `00_chat` per le chat di claude.ai: si tiene, dall'utente. Non serve solo a Lorenzo: chi userà il prodotto lavora ognuno a modo suo, e le chat di claude.ai sono uno degli input del Second Brain.

## File toccati

- `topics/second-brain.md`
- `inbox/2026-10-24-mod-claude-cockpit.md` (aggiornata, poi tolta)
- `sessions/2026-10-24-restyling-cockpit-implementazione.md`, `sessions/2026-10-24-interfaccia-personalizzata.md` (aperti chiusi, link)
- `sessions/2026-10-25-cockpit-v05-smistamento.md` (nuovo)
- `SPEC.md` sul branch `claude/spec-cockpit-v05` (PR #19)

## Aperti

- [x] Unire la PR #19 sulla SPEC (1.14); dopo il merge spuntare l'aperto "SPEC 7, riga `cockpit`" di [[2026-10-24-restyling-cockpit-implementazione]] (chiuso: PR #19 unita)
- [ ] Step 5, rete di sicurezza dei diari: l'hook che copia le trascrizioni in `sessions/_raw/` non esiste e porterebbe nel repo dati riservati (§5). Valutare al suo posto un controllo dei giorni con commit di sessione ma senza diario (curator o `/verifica-task`), con una PR sulla SPEC §12
- [ ] Step 5: costruire e provare il ponte `00_chat` (riassunto salvato dalla chat di claude.ai → nota `session` con `surface: claude-ai`)
