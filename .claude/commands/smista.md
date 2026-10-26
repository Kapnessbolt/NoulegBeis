---
description: Smista le catture di inbox/ nei progetti, nei clienti e nei temi (SPEC 8), dopo l'ok di Lorenzo
argument-hint: "[nota di inbox]"
---

Smista `inbox/`. Proponi, poi scrivi solo dopo l'ok di Lorenzo.

Argomenti: `$ARGUMENTS` (una nota di `inbox/` da smistare da sola; senza, tutte).

1. Elenca le note di `inbox/` (`ls inbox/*.md`, esclusa `.gitkeep`) e leggile. Se non ce ne sono, dillo e fermati.
2. Diario della sessione: la fonte di ogni punto smistato è il diario di questa sessione, `sessions/<oggi>-<slug-sessione>.md` (oggi: `TZ=Europe/Rome date +%F`), citato come `([[<oggi>-<slug-sessione>]])`. Scegli lo slug della sessione ora (2–4 parole, come `/chiudi-sessione`). Se il diario non esiste ancora, dillo: un wikilink verso una nota che non c'è è un errore del controllo e blocca il commit, quindi lo crei prima del commit (passo 7).
3. Per ogni cattura trova le note candidate:
   - `python3 .claude/scripts/cerca.py <2–3 termini della cattura> --tipo project --tipo client --tipo topic --limite 5`;
   - se la cattura ha `Contesto: [[slug]]`, parti da lì (`cerca.py --nota <slug>`);
   - per i progetti apri `projects/<slug>/<slug>.md` per vedere `## Attività` e `## Stato`.
4. Proponi la destinazione, una o più:
   - progetto esistente: riga datata in `projects/<slug>/<slug>-log.md` (`- AAAA-MM-GG · cosa · [[fonte]]`, in testa al log) e, se è un'azione, checkbox in `## Attività` di `<slug>.md` (`- [ ] testo 📅 AAAA-MM-GG ([[fonte]])`); se cambia lo stato, la riga in `## Stato`;
   - tema: punto in `## Punti chiave` di `topics/<slug>.md`;
   - cliente: punto in `## Relazione con BlueAge` di `clients/<slug>.md`;
   - nota nuova da creare (progetto o tema): solo come proposta, con nome e slug; i progetti non si creano da soli (`CLAUDE.md` §2). Se Lorenzo dice sì, la crea la sessione con `nuova-nota.py`;
   - scarto: già presente nel vault (di' dove), superata, estranea a BlueAge.
   Un'informazione su un progetto va in due posti: log e, se cambia lo stato, scheda (`CLAUDE.md` §2).
5. Mostra una tabella: `cattura → destinazione → testo che scriverai`, con la fonte in coda a ogni testo. Nessuna destinazione certa: dillo e lascia la cattura in `inbox/`.
6. Applica solo dopo l'ok, nota per nota o tutte insieme, come dice Lorenzo. Per ogni cattura applicata: scrivi le righe, poi `git rm inbox/<nota>.md`. Le catture non approvate restano.
7. Se il diario del passo 2 non c'è ancora, crealo ora: `python3 .claude/scripts/nuova-nota.py session sessions/<oggi>-<slug-sessione>.md --titolo "<titolo>" --campo surface=<cloud | locale> --campo 'outcome=smistamento di inbox/'`, con `## Obiettivo` (smistare `inbox/`) e `## Decisioni` (una riga per destinazione approvata). Va nello stesso commit dello smistamento; a fine sessione `/chiudi-sessione` lo aggiorna invece di riscriverlo.
8. `python3 .claude/scripts/controlla-vault.py`; correggi gli errori introdotti.
9. Commit `inbox: smistamento` con i file toccati, il diario se l'hai creato e le catture rimosse. `git branch --show-current`: su `main`, `git pull --rebase origin main` e push; su un branch `claude/`, commit lì e dillo.
