---
description: Stato completo di un progetto (SPEC 8): stato, attività aperte, ultimi passi del log, fonti recenti, persone, cose che non tornano
argument-hint: "<nome o slug del progetto>"
---

Mostra lo stato di un progetto. Sola lettura: non correggere niente senza l'ok di Lorenzo.

Argomenti: `$ARGUMENTS`

1. Trova lo slug:
   - se esiste `projects/<argomento>/<argomento>.md`, è quello;
   - altrimenti cerca tra le cartelle di `projects/` quelle il cui nome contiene le parole dell'argomento (`ls projects/`), poi `python3 .claude/scripts/cerca.py --tipo project $ARGUMENTS --limite 5`;
   - un solo candidato: usalo. Più di uno: elencali (slug e titolo) e chiedi quale. Nessuno: dillo, mostra l'elenco dei progetti (`ls projects/`) e, se l'argomento è un cliente o un tema (`cerca.py --tipo client --tipo topic $ARGUMENTS --limite 3`), dillo. Non creare progetti (`CLAUDE.md` §2).
2. Leggi `projects/<slug>/<slug>.md` per intero e `projects/<slug>/<slug>-log.md`.
3. Collegamenti:
   - fonti recenti: `python3 .claude/scripts/cerca.py --progetto <slug> --cartella sources --da <oggi − 30 giorni> --limite 0` (oggi: `TZ=Europe/Rome date +%F`; 30 giorni fa: `TZ=Europe/Rome date -d '30 days ago' +%F`);
   - chi collega il progetto: `python3 .claude/scripts/cerca.py --collegamenti <slug>`: persone (`person`), clienti (`client`), temi (`topic`), sessioni.
4. Risposta, in quest'ordine:
   - **Stato**: 3–5 righe da `## Stato` e `## Decisioni`, con `status` e `role` del frontmatter e i clienti;
   - **Attività aperte**: le `- [ ]` di `## Attività` ordinate per data (`📅`), le scadute prima e in evidenza, quelle senza data in fondo; ognuna con la fonte;
   - **Ultimi passi**: le 5 righe più recenti del log;
   - **Fonti recenti**: una riga per fonte degli ultimi 30 giorni, `[[slug]] · titolo · data`, dalla più recente;
   - **Persone**: dal frontmatter `people` e dai backlink di tipo `person`, con il ruolo se la nota lo dice;
   - **Cose che non tornano**: attività aperte senza data; log fermo da più di 14 giorni con `status: attivo`; fonti recenti che non compaiono nel log; note collegate con `partial: true` (`cerca.py --progetto <slug> --json` e il campo `frontmatter.partial`); `updated` del progetto più vecchio dell'ultima riga del log.
5. Se Lorenzo chiede di aggiornare il progetto, lo fa la sessione seguendo `CLAUDE.md` §2 (riga datata nel log, sezione della scheda, fonte in coda), poi controllo del vault e commit `project(<slug>): <cosa>`.
