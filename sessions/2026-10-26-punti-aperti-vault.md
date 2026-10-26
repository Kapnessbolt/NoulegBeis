---
type: session
date: 2026-10-26
surface: locale
topics: ["[[second-brain]]"]
outcome: "Task 24–26/10 verificati e step 4 chiuso; PyYAML garantito dall'hook di avvio; attività senza data smistate; step 3 chiuso"
---

# Punti aperti del vault, dal più urgente

## Obiettivo

Raccogliere gli aperti del vault (diari, SPEC §13–14) e chiuderli in ordine di urgenza.

## Decisioni

- Giri dei task del 24, 25 e 26/10 tutti OK: watermark sempre in avanti, nessun doppione, cockpit uguale a `plancia.py` (8 progetti, 93 attività). Chiusi lo step 4 e la verifica del primo giro del cockpit con i sei dataset.
- L'aperto "ingestor indipendente dal nome del connettore" era già risolto il 23–24/10: `tools` elenca i tre nomi del server e `controlla-vault.py` li confronta con i permessi; il carattere jolly resta scartato perché darebbe all'agente anche l'invio di mail.
- PyYAML: l'hook di avvio lo installa se manca, altrimenti lo segnala. Lo script di setup dell'ambiente cloud sta nell'interfaccia di claude.ai e non si versiona.
- Attività senza data (64): sei date dedotte dal testo (Bollazzi 30/10, Solera 18/11, riesame fornitori Manini e ripresa dati Velo-CE 30/11, interventi 3A e 3B 08/01/2027, web service VIN 15/01/2027); chiuse dall'utente quattro attività superate (calendario MTU del 19/10, parere sul caso entrata merci v3, due avvisi a Cristian).

- Smistamento delle altre attività senza data: l'utente le lascia aperte; unite le richieste a Manini in una "mail unica" (manini-automazione-ddt) e le domande a Luca del 22/10 (parts-radar-sviluppo).
- Step 3 chiuso: campione di Delivery e documenti letti in parte superati dall'uso; dei sei temi proposti SdI e supply chain esistono già, gli altri quattro (governance del tenant, migrazione dati BC, So Smart/EOS, Power BI) restano nella scheda di [[velo-ce-progetto-dynamics]] perché non sono offerte o metodi di BlueAge.

- Step 6: la decisione (skill solo nel vault, plugin cancellato, SPEC §2 corretta) era già presa nella sessione del one pager; resta la prova pratica, che va fatta in una sessione cloud e che l'aperto di [[2026-10-26-one-pager-second-brain]] già copre.

## File toccati

- `.claude/hooks/pull-inizio-sessione.sh`
- `sessions/`: aperti chiusi in `2026-10-22-watermark-e-task-schedulati`, `2026-10-24-restyling-cockpit-implementazione`, `2026-10-22-controllo-vault`, `2026-10-22-primo-caricamento-delivery`
- `projects/`: attività e log di corso-ai-mtu, corso-ai-manini, osservatorio-ai-pmi-liuc, parts-radar-sviluppo, manini-supply-chain-magazzino, manini-automazione-ddt, velo-ce-progetto-dynamics

## Aperti

- [x] Smistare le altre 54 attività senza data, progetto per progetto (chiuso: commit 4dfc482)
- [ ] Il caso in cui l'hook installa davvero PyYAML si vedrà solo in una sessione cloud a cui manca
- [ ] Prossimi aperti fattibili in locale: email delle 7 persone senza email (da Outlook), soglia dei nomi simili (0,85), ponte `00_chat` (step 5)
