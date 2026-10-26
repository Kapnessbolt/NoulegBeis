---
type: session
date: 2026-10-26
surface: cloud
topics: ["[[second-brain]]"]
outcome: "Esiti di reconcile, digest e curator verificati; curator spostato alla domenica sera; rete di sicurezza dei diari affidata al curator (SPEC 1.15); il repo Manini non scrive più nel vault; essenziale Manini in una nota sola e note Manini e parts-radar rilette"
---

# Esiti dei task, diari mancanti e vault in sola lettura dai repo di progetto

## Obiettivo

Controllare gli esiti di reconcile, digest e curator, e decidere sulla proposta del curator (PR #20) per la rete di sicurezza dei diari.

## Decisioni

- Reconcile del 25/10 e digest del 26/10 OK. Il task curator girava ogni giorno alle 09:59 invece che la domenica sera: spostato dall'utente a domenica alle 21:20, perché da qui si possono modificare solo i task creati dall'agente
- Proposta `controllo-diari-mancanti` accettata dall'utente, con una variante: il controllo è per commit e non per giorno, perché quello per giorno non vedeva il commit Manini delle 23:30 del 25/10, fatto in una sessione senza diario in un giorno che aveva già altri due diari
- SPEC 1.15: la rete di sicurezza dei diari la fa il curator; niente hook `Stop` né trascrizioni intere nel repo, perché porterebbero dati riservati; `sessions/_raw/` tiene solo estratti; tolti la retention di 30 giorni e il task `sessions-cleanup`
- La sessione Manini del 25/10 non aveva agito da sola: seguiva il `CLAUDE.md` del repo di progetto, che chiedeva di scrivere nel vault e di fare push su `main`. Dall'utente: il vault lo aggiorna solo l'ingestion giornaliera, quindi il repo Manini da ora il vault lo legge e basta. Nessuna regola nuova nel `CLAUDE.md` del vault (dall'utente)
- Diario della sessione del 25/10 ricostruito dai commit dei due repo
- Il curator schedulato resta sul branch della sua sessione invece di `claude/curator-AAAA-MM-DD`: la sessione cloud riceve un branch assegnato e la regola di non fare push altrove senza permesso, e un task schedulato non ha nessuno a cui chiederlo. Lasciato così dall'utente: la PR arriva comunque
- Digest del 26/10 con "Controllo del vault" vuoto: è normale. Quella sezione la compila solo il reconcile della domenica, e `## Scartate` solo l'ingest-outlook quando scarta delle mail. Nei giorni feriali il controllo lo fa il workflow GitHub su ogni push
- Doppione `essenziale` / `manini-ddt-essenziale` unito dall'utente in [[manini-ddt-essenziale]]: resta lo slug più specifico e già citato da 9 note (`essenziale` scontrerebbe con l'essenziale di un altro progetto), con il contenuto e il file corrente del 25/10 in `Library/`; la versione del 23/10 nella cartella Manini resta nello storico e in `.state/ingest.json` i due file puntano alla stessa nota. Poi, su richiesta dell'utente, il file vecchio `Manini/manini_ddt_essenziale.md` è stato cancellato da OneDrive (cestino, recuperabile per 93 giorni) e tolto dallo stato, perché il reconcile non segni la nota come `removed`
- Rilette e aggiornate le 4 note che citavano l'essenziale: [[manini]] (matching fatto, non più da fare), [[corso-ai-manini]] (prompt v1.1 per l'aula IT, tre DDT per l'aula utenti), [[manini-automazione-ddt]] (prompt v1.1 per il pilota, business case invariato sull'estrazione reale, repo che legge il vault senza scriverci) e [[ai-nei-processi]] (il prompt riduce il distacco tra i modelli, regola "campo incerto → verifica"); `gruppi` invariato
- Rilette e aggiornate anche le note di parts-radar dopo l'ingestion GitHub del 26/10: [[parts-radar-sviluppo]] (settimana 1 quasi chiusa, decisione dei prompt congelati, prossimi passi della settimana 1) e [[adac-bologna]] (dataset delle chat e cosa resta in attesa da ADAC); [[parts-radar]] riletta senza modifiche, perché nell'architettura è cambiata solo la D43, di livello pilot

## File toccati

- `.claude/agents/curator.md`: controllo dei commit senza diario (sezione 2, punto 5) e voce nei "Da verificare"
- `CLAUDE.md`, `README.md`: `sessions/_raw/` solo per estratti di trascrizione
- `SPEC.md`: §3, §7, §9.2, §12 e §14, versione 1.15 (PR #21)
- `proposals/2026-10-25-controllo-diari-mancanti.md`: `status: accettata` con la nota sulla variante (PR #20)
- `sessions/2026-10-25-manini-ritest-prompt-v11.md` (nuovo); aperti spuntati in `sessions/2026-10-22-watermark-e-task-schedulati.md` e `sessions/2026-10-25-cockpit-v05-smistamento.md`
- `sources/onedrive/01-materiale-clienti/manini/`: `manini-ddt-essenziale.md` spostata in `progetto-automazione/library/` e unita a `essenziale.md` (cancellata); `.state/ingest.json`; collegamenti in `journal/2026-10-26.md` e nel log di `manini-automazione-ddt`
- `clients/manini.md`, `projects/corso-ai-manini/corso-ai-manini.md`, `projects/manini-automazione-ddt/` (scheda e log), `topics/ai-nei-processi.md`; `clients/adac-bologna.md`, `projects/parts-radar-sviluppo/parts-radar-sviluppo.md`, `topics/parts-radar.md` (solo `updated`)
- Fuori dal vault: repo `manini-automazione-ddt`, `CLAUDE.md` §5 (PR #4); task curator su claude.ai, orario spostato dall'utente; OneDrive, cancellato `Manini/manini_ddt_essenziale.md`

## Aperti

- [x] Orario del curator: il task gira alle 21:20, mentre la SPEC §7 e `.claude/routines/curator.md` dicono 21:10. Rimettere il task alle 21:10 oppure correggere i due file (la SPEC con una PR) (chiuso: task riportato dall'utente a domenica alle 21:10)
- [x] Il curator schedulato può fare push solo sul branch della sua sessione (`claude/<nome-casuale>`) e non su `claude/curator-AAAA-MM-DD`: allineare la SPEC 9.2 e la routine, o accettare il nome che il branch prende da solo (chiuso: lasciato così dall'utente)
- [x] Digest del 26/10 con la sezione "Controllo del vault" vuota (il 25/10 era compilata): verificare se il digest ha saltato `controlla-vault.py` (chiuso: è normale, la sezione la compila solo il reconcile)
