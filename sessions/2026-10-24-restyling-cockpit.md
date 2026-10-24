---
type: session
date: 2026-10-24
surface: cloud
topics: []
outcome: "Ricerca per il restyling del Cockpit: contenuti da tenere, togliere e aggiungere, ruoli di dashboard e mod, monitor del piano fattibile; 6 mockup pubblicati"
---

# Restyling del Cockpit: ricerca e mockup

## Obiettivo

Rendere più professionali la dashboard Cockpit su claude.ai e il pannello della mod `cockpit`, rivedendo contenuti e funzioni, e aggiungere nella sola mod il consumo del piano Max. Questa sessione produce ricerca e mockup; l'implementazione della proposta scelta si fa in un'altra sessione.

## Fonti lette

- Dashboard Cockpit (https://claude.ai/artifact/KN8Wp48Ja6vGbShXeTpRgR): pagina `files/index.html`, dataset `calendario`, `progetti`, `attivita`, `artifact-type/reference/design-defaults.md`. Solo lettura.
- Mod `cockpit` v0.2.0 (`hooks/register.tsx`) e API delle mod di Claude Code 2.1.310 (skill `plugin-authoring`, tipi `claude-code.d.ts`).
- Documentazione della riga di stato: https://code.claude.com/docs/en/statusline
- Diari in `sessions/` dal 22 al 24/10, digest [[2026-10-23]] e [[2026-10-24]], `.state/ingest.json`, `home.md`, `.claude/scripts/plancia.py`, `.claude/routines/cockpit.md`, SPEC §7.
- Guida di stile v3 della skill `blueage-deck` (palette e font). Su SharePoint nessuna linea guida del brand (ricerche "brand guidelines", "brand identity", "logo BlueAge" in SalesMarketing).
- Calendario Outlook dal 24/10 al 07/11 (5 eventi, 3 nei prossimi 7 giorni).
- Benchmark: Sunsama (rituale del mattino), Linear Triage (inbox come coda), Grafana (stato dei sistemi), Apple HIG widget (lettura in pochi secondi).

## Decisioni

- Uso reale: la storia del vault è di 3 giorni. Il controllo più frequente è l'esito dei task schedulati (4 diari su 17 e una sessione intera); il Cockpit non lo mostra.
- Contenuti approvati: tenere agenda, scadute e scadenze, ma separare le scadenze **tue** da quelle dei progetti che osservi (2 delle 4 entro 14 giorni sono di Velo-CE, dove Lorenzo non è coinvolto); togliere i KPI "attività aperte" e "progetti coinvolto" e la griglia del calendario a 7 colonne; sostituire l'elenco progetti (tutti `attivo`) con prossima scadenza e giorni dall'ultimo log; aggiungere esito dei task, scadenze datate di `inbox/`, inbox da smistare, contatore delle proposte, riga del digest; non aggiungere aperti dei diari (38, molti già chiusi altrove), watermark di `.state/` (fuorvianti) e interazioni delle persone.
- Ruoli: dashboard = briefing in sola lettura per telefono e cloud; mod = postazione al PC dal vivo, con azioni e consumo del piano. Le viste oggi sono tre: anche `home.md` su Obsidian copre scadenze, progetti e inbox, quindi la tabella completa delle attività va in seconda scheda.
- Monitor del piano fattibile: `$.session.usage()` e l'evento `session.measure` danno `rateLimits` (`five_hour`, `seven_day`, `percentUsed`, `resetsAt`); la riga di stato riceve `rate_limits` solo con Pro/Max e dopo la prima risposta della sessione. Il dato si aggiorna solo con le risposte della sessione locale: la riga mostra l'ora della lettura. Posizione: dettaglio nella testata del pannello, riga di stato sempre visibile, banda sopra il prompt solo oltre il 90%.
- Stile: accenti BlueAge (`#2F80ED`, `#1C9EB1`) sopra i token del tema ("mix"); i colori attuali della dashboard non sono quelli del brand. Plus Jakarta Sans non si carica nell'artifact.
- Mockup: pagina di confronto https://claude.ai/artifact/TSpB98aeJteXJcoi8txn31 con 3 proposte per superficie (briefing, sala controllo, focus); le anteprime della mod sono disegnate con i soli componenti dell'app e dichiarano il componente di ogni elemento. Consumo del piano con valori di esempio: in cloud non c'è una sessione locale da cui leggerlo.
- Raccomandazione: A1 (briefing) per la dashboard; M1 con la testata di M2 (piano e sistemi) per la mod. La mod non sostituisce la dashboard finché il pannello non si vede dal telefono.

## File toccati

- `sessions/2026-10-24-restyling-cockpit.md` (nuovo)
- `inbox/2026-10-24-mod-claude-cockpit.md`

## Aperti

- [x] Scegliere le proposte dalla pagina dei mockup e implementarle in un'altra sessione (dashboard, mod, `plancia.py` con task, inbox datata e digest) 📅 2026-11-07 ([[2026-10-24-restyling-cockpit]]) (chiuso in [[2026-10-24-restyling-cockpit-implementazione]])
- [x] Leggere il consumo vero del piano in una sessione locale con la mod aggiornata e verificare che si aggiorni con le risposte ([[2026-10-24-restyling-cockpit]]) (chiuso in [[2026-10-24-restyling-cockpit-implementazione]])
- [x] Igiene degli aperti dei diari: molti sono chiusi altrove ma restano spuntati come aperti ([[2026-10-24-restyling-cockpit]]) (chiuso: agente curator con l'igiene degli aperti, commit 04f58fb del 25/10; primo giro il 25/10)
