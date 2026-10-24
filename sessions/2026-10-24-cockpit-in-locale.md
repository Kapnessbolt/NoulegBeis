---
type: session
date: 2026-10-24
surface: cloud
topics: [claude-code-cloud-e-locale]
outcome: "Mod cockpit attiva in una sessione locale dell'app desktop (Ubuntu) con calendario, scadenze e progetti; allineati permessi e agente ingestor tra cloud e locale"
---

# Cockpit in locale e allineamento tra sessioni cloud e locali

## Obiettivo

Far partire sul PC la mod `cockpit` creata nella sessione [[2026-10-24-interfaccia-personalizzata]], capire cosa cambia tra sessione cloud e sessione locale e allineare permessi e configurazione, così che l'uso sia lo stesso a meno del `git pull` iniziale.

## Decisioni

- La mod gira solo nelle sessioni locali: in una sessione cloud (anche seguita dall'app desktop) "Plugin" e "Aggiungi cartella" non sono disponibili e nessuna superficie disegna il pannello; resta il riepilogo in testo di `/cockpit`.
- La mod è salvata nei "My Uploads" dell'account come disponibile, non installata: si attiva una volta per dispositivo con + → Plugin. Registra `/cockpit` e apre il pannello all'avvio della sessione, e solo se la cartella aperta è il vault (o la contiene).
- Sessione locale aperta sulla cartella `NoulegBeis`, non su una cartella che contiene i repo: impostazioni, hook e comandi del vault si leggono solo dalla cartella aperta. Gli altri repo si aggiungono con + → Aggiungi cartella, o si apre una sessione su quel repo.
- Setup del PC (Ubuntu, Dell Vostro 7570): repo in `~/Documents/BlueAge/`, login GitHub con `gh auth login` (git non accetta più la password), app `claude-desktop` aggiornata da 1.17377.1 riattivando il repository apt di Anthropic in `/etc/apt/sources.list.d/claude-desktop.list`: con la versione vecchia i modelli nuovi erano grigi e la mod non partiva.
- In locale il connettore Microsoft 365 ha un altro nome di server (`6501b655-9b79-4832-8016-17eddb19e4b6`, al posto di `Microsoft_365`): la modalità Auto bloccava la lettura del calendario della mod. Aggiunti i permessi in lettura con il nome locale, sia nelle impostazioni utente del PC sia in `.claude/settings.json` del vault.
- Lo stesso nome mancava in `tools` dell'agente `ingestor`: in locale `/ingest` sarebbe partito senza connettore. Aggiunti i quattro strumenti in lettura con il nome locale.
- GitHub in locale passa da git e `gh` con il login del PC, non dal connettore: le issue si leggono con `gh issue view`. L'agente `ingestor` lo usa quando `issue_read` manca (permesso `Bash(gh issue view:*)` nel vault), così anche `/ingest github` funziona in locale.
- Confronto cloud/locale annotato in [[claude-code-cloud-e-locale]].

## File toccati

- `.claude/agents/ingestor.md`
- `.claude/settings.json`
- `topics/claude-code-cloud-e-locale.md` (nuovo)
- `inbox/2026-10-24-mod-claude-cockpit.md`
- `sessions/2026-10-24-cockpit-in-locale.md` (nuovo)

## Aperti

- [ ] Provare `/ingest outlook` in una sessione locale dopo il pull, per verificare l'agente ingestor con il nome locale del connettore 📅 2026-10-31 ([[2026-10-24-cockpit-in-locale]])
- [ ] Controllare in una sessione locale (`/`) che ci siano le skill dell'account (blueage-deck, blueage-corso, ecc.) 📅 2026-10-31 ([[2026-10-24-cockpit-in-locale]])
- [ ] PR dedicata su `SPEC.md` §2: esecuzione anche in sessioni locali dell'app desktop, mod al posto della frase "`/plugin` non è disponibile", valore di `surface` per le sessioni locali 📅 2026-11-07 ([[2026-10-24-cockpit-in-locale]])
- [ ] Valutare in locale un hook `Stop` che avvisa se restano modifiche non committate o non spinte, come nel cloud 📅 2026-11-07 ([[2026-10-24-cockpit-in-locale]])
