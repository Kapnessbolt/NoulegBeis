---
type: session
date: 2026-10-22
surface: cloud
topics: []
outcome: "SPEC 1.4: integrità dei collegamenti e tracciabilità garantite da hook, workflow e script di rinomina"
---

# Integrità dei collegamenti e tracciabilità

## Obiettivo

Garantire che link e concetti del vault siano affidabili: nessun wikilink rotto (una nota irraggiungibile non entra mai nel contesto delle ricerche sul grafo), ogni affermazione con la sua fonte, segnalazione delle note vecchie o che citano fonti rimosse.

## Decisioni

- Wikilink rotto = errore ovunque, anche nel testo. Prima era solo un avviso.
- Cambia la decisione della SPEC 1.3: i task schedulati creano anche clienti e temi mancanti, come note minime con tag `da-verificare`, invece di lasciare un link rotto e proporre la creazione nel digest. I progetti restano esclusi: la fonte si collega a clienti o temi.
- Tracciabilità: punti chiave dei temi, "Chi sono" e "Relazione con BlueAge" dei clienti, "Stato" e "Decisioni" dei progetti devono citare una nota fonte o un diario di sessione. Un link a un tema non basta.
- Controllo applicato in tre punti: hook PreToolUse che blocca `git commit` se ci sono errori nei file modificati (compresi i link rotti da cancellazioni e rinomine), workflow GitHub su ogni push e PR (copre Obsidian e il web), riconciliazione settimanale.
- Nuovo `rinomina-nota.py`: rinomina note e progetti (cartella, scheda, log) e aggiorna collegamenti e stato. Serve anche per unire i doppioni.
- Nuovi avvisi: note orfane, note che citano fonti rimosse, note più vecchie della fonte che citano, note `da-verificare`.
- Persona con nome simile ma email diversa: si crea la nuova persona (slug `<nome-cognome>-<dominio>` se occupato) e si segnala il possibile doppione.

## File toccati

- `SPEC.md` (1.4), `CLAUDE.md`
- `.claude/scripts/controlla-vault.py`, `.claude/scripts/rinomina-nota.py`, `.claude/hooks/controllo-pre-commit.sh`, `.claude/settings.json`
- `.claude/agents/ingestor.md`, `.claude/commands/controlla.md`
- `.github/workflows/controllo-vault.yml`
- `topics/pulse.md`, `topics/blueage.md` (fonte sui punti chiave)

## Aperti

- [ ] Verificare in una sessione nuova che l'hook di pre-commit sia attivo (in questa sessione la configurazione era già caricata)
- [ ] Verificare il primo run del workflow su GitHub dopo il merge
- [ ] Verifica del contenuto con un agente (opzione C), da fare allo step 7
