---
type: topic
kind: metodo
projects: []
clients: []
tags: [claude-code, second-brain]
updated: 2026-10-24
---

# Claude Code: sessioni in cloud e sessioni locali

## Cos'è

Le due modalità in cui si lavora sul vault con Claude Code: la sessione **cloud** gira in un ambiente temporaneo di Anthropic, la sessione **locale** gira sul PC, avviata dall'app desktop. Modello, limiti del piano, connettori e task schedulati sono gli stessi: cambia dove gira la sessione, quali file vede e con quali credenziali agisce ([[2026-10-24-cockpit-in-locale]]).

## Punti chiave

- Cloud: continua a PC chiuso, si segue e si usa dal telefono, parte da un clone nuovo (il lavoro non committato si perde), vede solo i repo collegati alla sessione, configurazione già pronta dal vault, niente mod né pannelli, niente "Aggiungi cartella" ([[2026-10-24-cockpit-in-locale]])
- Locale: si ferma con il PC, dal telefono solo con Remote Control attivo e il PC acceso, il lavoro resta nella cartella, vede tutto il PC, mod e pannelli disponibili (Cockpit), GitHub con il login del PC (`gh`) su tutti i repo dell'account: niente connettore GitHub, ma file e issue si leggono lo stesso con git e `gh`, anche da `/ingest github` ([[2026-10-24-cockpit-in-locale]])
- Il vault si apre come cartella della sessione locale (`~/Documents/BlueAge/NoulegBeis`): impostazioni, hook e comandi in `.claude/` si leggono solo dalla cartella aperta. Gli altri repo si aggiungono con + → Aggiungi cartella ([[2026-10-24-cockpit-in-locale]])
- I task schedulati (ingestion, digest, dashboard Cockpit) girano sempre in cloud, qualunque modalità si usi; per questo in locale il `git pull --rebase` a inizio sessione è indispensabile. Lo fa da solo l'hook di avvio del vault, in cloud e in locale; con modifiche non committate lo salta e lo segnala. A fine risposta un hook `Stop` rimanda Claude a fare commit e push se restano modifiche: in cloud lo fa l'ambiente, in locale l'hook del vault ([[2026-10-24-cockpit-in-locale]])
- Il connettore Microsoft 365 cambia nome di server: `Microsoft_365` nelle sessioni cloud, `Microsoft-365` nei task schedulati, `6501b655-9b79-4832-8016-17eddb19e4b6` nelle sessioni locali. Permessi (`.claude/settings.json`) e agente `ingestor` elencano tutti e tre: un nome nuovo va aggiunto in entrambi ([[2026-10-24-cockpit-in-locale]])
- In modalità Auto le azioni che non nascono da una richiesta (per esempio la mod che legge il calendario) passano da un controllo automatico, che può rifiutarle: si sbloccano con una regola `allow` per lo strumento esatto ([[2026-10-24-cockpit-in-locale]])
- Requisiti del PC: git, python3 (gli script e il pre-commit del vault), login GitHub con `gh auth login`, app desktop aggiornata; su Ubuntu l'app si aggiorna con apt se è attiva la riga del repository in `/etc/apt/sources.list.d/claude-desktop.list` ([[2026-10-24-cockpit-in-locale]])
- Quando usare cosa: al PC la sessione locale (Cockpit aperto, file del PC); dal telefono o per lavori lunghi a PC chiuso la sessione cloud ([[2026-10-24-cockpit-in-locale]])

## Dove è usato

- Questo vault, versione personale del [[second-brain]] ([[2026-10-24-cockpit-in-locale]])

## Fonti

- [[2026-10-24-cockpit-in-locale]]
- [[2026-10-24-interfaccia-personalizzata]]
