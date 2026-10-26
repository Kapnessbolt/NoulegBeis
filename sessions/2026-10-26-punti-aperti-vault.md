---
type: session
date: 2026-10-26
surface: locale
topics: ["[[second-brain]]"]
outcome: "Giri dei task 24–26/10 verificati e step 4 chiuso; PyYAML garantito dall'hook di avvio; attività senza data in smistamento (in corso)"
---

# Punti aperti del vault, dal più urgente

## Obiettivo

Raccogliere gli aperti del vault (diari, SPEC §13–14) e chiuderli in ordine di urgenza.

## Decisioni

- Giri dei task del 24, 25 e 26/10 tutti OK: watermark sempre in avanti, nessun doppione, cockpit uguale a `plancia.py` (8 progetti, 93 attività). Chiusi lo step 4 e la verifica del primo giro del cockpit con i sei dataset.
- L'aperto "ingestor indipendente dal nome del connettore" era già risolto il 23–24/10: `tools` elenca i tre nomi del server e `controlla-vault.py` li confronta con i permessi; il carattere jolly resta scartato perché darebbe all'agente anche l'invio di mail.
- PyYAML: l'hook di avvio lo installa se manca, altrimenti lo segnala. Lo script di setup dell'ambiente cloud sta nell'interfaccia di claude.ai e non si versiona.
- Attività senza data (64): sei date dedotte dal testo (Bollazzi 30/10, Solera 18/11, riesame fornitori Manini e ripresa dati Velo-CE 30/11, interventi 3A e 3B 08/01/2027, web service VIN 15/01/2027); chiuse dall'utente quattro attività superate (calendario MTU del 19/10, parere sul caso entrata merci v3, due avvisi a Cristian).

## File toccati

- `.claude/hooks/pull-inizio-sessione.sh`
- `sessions/2026-10-22-watermark-e-task-schedulati.md`, `sessions/2026-10-24-restyling-cockpit-implementazione.md`, `sessions/2026-10-22-controllo-vault.md` (aperti chiusi)
- `projects/*/` di corso-ai-mtu, corso-ai-manini, osservatorio-ai-pmi-liuc, parts-radar-sviluppo, manini-supply-chain-magazzino, velo-ce-progetto-dynamics (attività e log)

## Aperti

- [ ] Smistare le altre 54 attività senza data, progetto per progetto (in corso)
- [ ] Il caso in cui l'hook installa davvero PyYAML si vedrà solo in una sessione cloud a cui manca
