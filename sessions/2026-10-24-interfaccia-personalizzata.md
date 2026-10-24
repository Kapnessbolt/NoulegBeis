---
type: session
date: 2026-10-24
surface: cloud
topics: []
outcome: "Valutata un'interfaccia personale al posto dell'app Claude: si resta sull'app e si approfondiscono le mod per integrarci il Cockpit"
---

# Interfaccia personalizzata per il brain: app Claude o interfaccia propria

## Obiettivo

Capire se conviene portare l'interazione con il brain su un'interfaccia personale (locale, con la chat e il Cockpit insieme), sfruttando l'abbonamento Max.

## Decisioni

- Si resta sull'app Claude: l'harness porta connettore Microsoft 365, task schedulati in cloud, artifact e ArtifactData (il Cockpit vive lì), app sul telefono, sessioni cloud. Rifarli costerebbe molto, e il connettore M365 richiederebbe un'app registrata nel tenant BlueAge, probabilmente con il consenso dell'amministratore.
- Abbonamento Max fuori dall'app: Claude Code sul proprio PC è consentito; un'interfaccia propria che lo pilota (Agent SDK, `claude -p`) con il login Max è tollerata per uso personale ma non esplicitamente permessa, e dal 15/06/2026 consuma un credito Agent SDK separato; app di terzi o prodotti per altri richiedono una API key (fonte: https://code.claude.com/docs/en/legal-and-compliance).
- Un'interfaccia locale non rende il servizio privato: il modello resta da Anthropic, il vault su GitHub, i dati su M365. Dà controllo sull'interfaccia, non sui dati.
- Strada scelta: approfondire le mod dell'app (pannelli accanto alla chat) per integrarci il Cockpit. Annotata in [[2026-10-24-mod-claude-cockpit]].

## File toccati

- `inbox/2026-10-24-mod-claude-cockpit.md` (nuovo)
- `sessions/2026-10-24-interfaccia-personalizzata.md` (nuovo)

## Aperti

- [ ] Approfondire le mod e provare il Cockpit come pannello (attività in [[2026-10-24-mod-claude-cockpit]])
