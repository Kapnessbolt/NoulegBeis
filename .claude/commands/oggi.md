---
description: Agenda del giorno (SPEC 8): attività scadute e in scadenza, progetti fermi, inbox, novità dall'ultimo digest, esito dei task
argument-hint: "[giorni, default 7]"
---

Dai a Lorenzo il punto della giornata. Sola lettura: non spuntare, non spostare e non scrivere niente.

Argomenti: `$ARGUMENTS` (un numero di giorni per la finestra delle scadenze; senza, 7).

1. Data e ora: `TZ=Europe/Rome date '+%F %H:%M'`. Oggi è la data di Roma, non quella UTC.
2. Dati della plancia: `python3 .claude/scripts/plancia.py "$(mktemp -d)"`. L'ultima riga dice la cartella (`→ <cartella>`): leggi da lì `attivita.json`, `progetti.json`, `inbox.json`, `task.json`, `digest.json`.
3. Raccogli:
   - **attività**: da `attivita.json` quelle con `fatta: false` e `scadenza` non vuota, fino a oggi + N giorni. Dividile in scadute (prima di oggi), oggi, entro N giorni; dentro ogni gruppo raggruppa per progetto (`nome_progetto`) e ordina per data. Per ognuna testo, scadenza e fonte (`[[fonte]]`). Quelle con `coinvolto: false` (progetti in cui Lorenzo non è coinvolto) mettile in fondo al gruppo, segnate;
   - **progetti fermi**: da `progetti.json` quelli con `stato: attivo` e `ultimo_log` vuoto o più vecchio di 14 giorni da oggi, con la data dell'ultimo log e la prossima attività (`prossima`, `prossima_testo`);
   - **inbox**: le note di `inbox.json` (titolo, creata, attività aperte): sono da smistare con `/smista`;
   - **esito dei task**: le righe di `task.json` (`stato` `ok`, `errore`, `mancante`, `atteso`). Errori e mancanti in evidenza, con il rimando a `/verifica-task`;
   - **novità dall'ultimo digest**: `digest.json` dice il giorno dell'ultimo digest (`giorno`). Leggi `journal/<giorno>.md` (`## Novità ingerite`, `## Decisioni`, `## Attività in scadenza`), poi le note arrivate dopo: `python3 .claude/scripts/cerca.py --cartella sources --da <giorno> --limite 0`. La data di `cerca.py` per le fonti è quella dei fatti (`last_message`, `current.last_modified`); tieni quelle che il digest non elenca già.
4. Riepilogo compatto, in quest'ordine, saltando i blocchi vuoti:
   1. **Scadute** (in evidenza)
   2. **Oggi**
   3. **Entro N giorni**
   4. **Progetti fermi**
   5. **Inbox da smistare**
   6. **Novità** (dal digest del <giorno> e dopo: una riga per fonte, `[[slug]] · titolo · data`, al massimo 10, poi "e altre N")
   7. **Task di oggi** (una riga: `7 attesi · 5 OK · 1 errore · 1 atteso`, poi i dettagli dei non OK)
   Una riga per voce, con il wikilink del progetto o della fonte. Niente commenti oltre i dati, tranne una riga finale con le 1–3 cose da fare per prime.
5. Se Lorenzo poi chiede di spuntare, spostare o aggiungere qualcosa, lo fa la sessione seguendo `CLAUDE.md` (checkbox in `## Attività` con la fonte, riga nel `<slug>-log.md`), non questo comando.
