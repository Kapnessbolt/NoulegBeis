---
type: session
date: 2026-10-24
surface: locale
topics: []
outcome: "Restyling del Cockpit implementato: dashboard A1 con 5 dataset del vault, plancia.py con task, inbox e digest, mod cockpit v0.3.0 (M1 con la testata di M2, piano Max, riga di stato, banda oltre il 90%)"
---

# Restyling del Cockpit: implementazione

## Obiettivo

Implementare le raccomandazioni di [[2026-10-24-restyling-cockpit]], approvate da Lorenzo: A1 (briefing) per la dashboard su claude.ai, M1 con la testata di M2 per il pannello della mod.

## Decisioni

- `plancia.py` scrive cinque file: `progetti` (più attività aperte, prossima scadenza, data dell'ultima riga del log), `attivita` (più `coinvolto` e `origine`; entrano le checkbox di `## Da fare` delle note in `inbox/`), `inbox`, `task`, `digest`. ([[2026-10-24-restyling-cockpit-implementazione]])
- Esito dei task: gli orari attesi di SPEC 7 stanno in una tabella dentro `plancia.py` e dentro la mod; una riga del digest vale per un orario se arriva tra 10 minuti prima e 3 ore dopo; senza riga dopo 45 minuti il task è "mancante". Se cambiano gli orari in SPEC vanno cambiati in tutti e due. ([[2026-10-24-restyling-cockpit-implementazione]])
- Dashboard A1: frase di sintesi calcolata dai dati (primo evento di oggi, scadenze tue superate, prossima scadenza tua, task da controllare), card Oggi, Scadenze tue a 30 giorni con countdown, Prossimi 7 giorni con eventi e scadenze (quelle dei progetti che osservi attenuate), riga di stato con task, inbox e digest. Seconda scheda "Progetti e attività": progetti con ruolo, aperte, prossima e giorni dall'ultimo log; tabella completa con ricerca, filtro per progetto e "Solo le mie". Accento blu BlueAge sopra i token del tema. ([[2026-10-24-restyling-cockpit-implementazione]])
- Le scadenze "tue" sono quelle dei progetti con ruolo diverso da "Non coinvolto…" più quelle datate in `inbox/`. ([[2026-10-24-restyling-cockpit-implementazione]])
- Mod `cockpit` v0.3.0: testata con piano Max (5h e 7 giorni, barre, azzeramento, ora della lettura) e sistemi (una riga se i task vanno, una riga per task con "Indaga" se uno è in errore o mancante; contatori di scadute, inbox, proposte, digest), poi Oggi, Prossimi 7 giorni, Scadenze tue a 14 giorni con quelle che osservi sotto un pulsante, Da smistare con "Smista", Progetti tuoi. I pulsanti scrivono la richiesta nel prompt, non la mandano. Riga di stato sempre visibile (`Cockpit · 5h 34% ↻19:40 · 7g 61% ↻gio 09:00`, più `⚠ N task` se serve); banda sopra il prompt solo oltre il 90%, nascondibile. ([[2026-10-24-restyling-cockpit-implementazione]])
- Il CLI `claude` sul PATH (2.1.276) è più vecchio del motore dell'app (2.1.308) e boccia anche la v0.2.0 che funziona: validare e testare le mod con `~/.config/Claude/claude-code/2.1.308/*/claude`. Con quello la v0.3.0 passa `plugin validate`, `tsc` e 7 test su 7. ([[2026-10-24-restyling-cockpit-implementazione]])

- Prima prova della v0.3.0 (Lorenzo, 23:25): barre del piano troppo alte, percentuali indietro di un punto (3% e 13% contro 4% e 14% reali), calendario "non collegato" all'avvio. v0.3.1: barre alte 6 px, piano riletto a ogni risposta (prima solo agli scatti di un punto intero), fino a 6 nuovi tentativi del calendario ogni 30 secondi. Pacchetto `~/Scaricati/cockpit-0.3.1.plugin`. ([[2026-10-24-restyling-cockpit-implementazione]])

## File toccati

- `.claude/scripts/plancia.py`
- `.claude/routines/cockpit.md` (cinque dataset, riga d'esito con i task)
- `inbox/2026-10-24-mod-claude-cockpit.md`
- `sessions/2026-10-24-restyling-cockpit-implementazione.md` (nuovo)
- Fuori dal repo: dashboard Cockpit (pagina e dataset `inbox`, `task`, `digest`), mod in `~/.claude/dev-mods/<sessione>/cockpit/` e pacchetto `~/Scaricati/cockpit-0.3.0.plugin`

## Aperti

- [ ] Installare `cockpit-0.3.1.plugin` al posto della v0.3.0 e controllare il pannello vero, con il consumo del piano letto dopo una risposta 📅 2026-10-31 ([[2026-10-24-restyling-cockpit-implementazione]])
- [ ] SPEC 7, riga `cockpit`: dire che `plancia.py` carica anche inbox, task e digest (PR dedicata) ([[2026-10-24-restyling-cockpit-implementazione]])
- [ ] Cancellare dalla dashboard il vecchio file di `progetti` (`89132086…`): la cancellazione è stata negata dal controllo dei permessi; non rompe nulla ([[2026-10-24-restyling-cockpit-implementazione]])
- [ ] Verificare il primo giro del task `cockpit` di domani alle 07:40 con i cinque dataset ([[2026-10-24-restyling-cockpit-implementazione]])
