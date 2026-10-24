---
type: inbox
created: 2026-10-24
---

# Mod dell'app Claude: portarci il Cockpit, da approfondire

Idea emersa nella sessione [[2026-10-24-interfaccia-personalizzata]]: invece di costruire un'interfaccia personale fuori da Claude, usare le **mod** dell'app (pannelli fissi accanto alla chat che si aggiornano, banner, status line, slash command, hook). Le mod non le ho ancora usate.

## Perché

- Unisce in una vista sola la chat con il brain e la dashboard Cockpit (https://claude.ai/artifact/KN8Wp48Ja6vGbShXeTpRgR), che è l'obiettivo dell'interfaccia personalizzata.
- Restano connettore Microsoft 365, task schedulati, artifact, app sul telefono: niente da ricostruire.
- Alternative scartate per ora: interfaccia locale che pilota Claude Code con il login Max (zona grigia dei termini d'uso, credito Agent SDK separato dal 15/06/2026, connettori e task da rifare); interfaccia su API key (a consumo, tutto lo stack da rifare). Da riprendere solo se emerge un limite concreto dell'app.

## Da fare

- [ ] Approfondire le mod: cosa si può fare, come si installano, su quali superfici funzionano (desktop, telefono, cloud) 📅 2026-10-31 ([[2026-10-24-interfaccia-personalizzata]])
- [ ] Verificare se un pannello mod può leggere il connettore Microsoft 365 come fa l'artifact Cockpit 📅 2026-10-31 ([[2026-10-24-interfaccia-personalizzata]])
- [ ] Prototipo: Cockpit come pannello accanto alla chat 📅 2026-11-07 ([[2026-10-24-interfaccia-personalizzata]])

Da smistare: se l'idea parte, diventa una sezione della scheda della plancia o un progetto a sé.
