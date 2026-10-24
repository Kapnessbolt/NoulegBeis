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

## Cosa abbiamo verificato (24/10)

- Una mod è un modulo TypeScript che si aggancia all'app: pannelli accanto alla chat, bande sopra il prompt, riga di stato, notifiche, slash command, hook sulle chiamate agli strumenti e sul prompt. API dichiarata "early access": può cambiare tra una versione e l'altra.
- Il pannello legge il connettore Microsoft 365 con le credenziali della sessione e il vault direttamente dai file: dati dal vivo, senza `plancia.py` né JSON caricati.
- Dove si vede il pannello: solo dove un'app si collega alla sessione come superficie (desktop, VS Code, terminale; l'app sul telefono quando si collega). Su una sessione cloud seguita dal telefono non si collega nessuna superficie: il pannello non compare.
- Ripiego che funziona anche dal telefono: il comando `/cockpit` risponde con il Cockpit in testo (calendario, scadenze, progetti). Provato con i dati veri.
- Prototipo impacchettato come `cockpit.plugin` (mod `cockpit` v0.1.0), consegnato in chat per salvarlo sull'account.
- Provato il 24/10 su una sessione locale dell'app desktop (Ubuntu): pannello con calendario, scadenze e progetti funzionante, dopo aver attivato la mod (+ → Plugin), aggiornato l'app e autorizzato la lettura del calendario con il nome locale del connettore ([[2026-10-24-cockpit-in-locale]]).

## Restyling del 24/10

- Ricerca e 6 mockup in [[2026-10-24-restyling-cockpit]] (pagina: https://claude.ai/artifact/TSpB98aeJteXJcoi8txn31). Ruoli proposti: la dashboard resta come briefing per telefono e cloud, la mod diventa la postazione al PC con piano, task e azioni.
- Raccomandazione sulla decisione qui sotto: la mod non sostituisce la dashboard finché il pannello non compare sul telefono; le routine `DailyBoard` restano perché alimentano la dashboard.

## Da fare

- [x] Approfondire le mod: cosa si può fare, come si installano, su quali superfici funzionano (desktop, telefono, cloud) 📅 2026-10-31 ([[2026-10-24-interfaccia-personalizzata]])
- [x] Verificare se un pannello mod può leggere il connettore Microsoft 365 come fa l'artifact Cockpit 📅 2026-10-31 ([[2026-10-24-interfaccia-personalizzata]])
- [x] Prototipo: Cockpit come pannello accanto alla chat 📅 2026-11-07 ([[2026-10-24-interfaccia-personalizzata]])
- [x] Salvare `cockpit.plugin` sull'account e provare il pannello dall'app desktop su una sessione locale aperta sul vault 📅 2026-10-31 ([[2026-10-24-cockpit-in-locale]])
- [ ] Provare se il telefono mostra il pannello seguendo una sessione locale (Claude Desktop o `claude remote-control`) 📅 2026-10-31 ([[2026-10-24-interfaccia-personalizzata]])
- [ ] Decidere se la mod sostituisce l'artifact Cockpit e le routine `DailyBoard` 📅 2026-11-07 ([[2026-10-24-interfaccia-personalizzata]])

Da smistare: se l'idea parte, diventa una sezione della scheda della plancia o un progetto a sé.
