---
type: session
date: 2026-10-27
surface: cloud
topics: ["[[second-brain]]"]
outcome: "Step 17 chiuso (PR #28 e #29 unite): cerca.py, librarian, quattro comandi, 10 domande di prova corrette. Cockpit v2 deciso e costruito come step 16: pagina HTML statica generata da cockpit.py, pubblicata, task riscritto, SPEC 1.21"
---

# Step 17 · librarian, ricerca e comandi; Cockpit v2 (step 16)

## Obiettivo

Eseguire lo step 17 di SPEC §13.1 (ricerca nel vault, agente `librarian`, comandi `/oggi`, `/progetto`, `/cattura`, `/smista`) senza toccare gli script dell'ingestion in osservazione fino al 29/10; poi avviare la revisione del cockpit (dashboard e mod) per decidere il contenuto dello step 16.

## Decisioni

- Il codice (`cerca.py`, test, agente, quattro comandi) lo ha scritto un subagente Opus su brief della sessione; la sessione ha rivisto, corretto e provato. Nessuno script dello step 12 è stato modificato: i comandi li chiamano soltanto (`nuova-nota.py` per `/cattura` e per il diario in `/smista`, `famiglia.py --slug`, `plancia.py` per `/oggi`).
- `cerca.py` non ha indice: scansiona le 313 note a ogni chiamata in 0,2–0,3 s. Punteggio per termine dal posto migliore (10 titolo o slug, 3 frontmatter, 1 corpo), poi backlink, poi data; con la somma dei tre pesi il progetto hub `corso-ai-manini` finiva 11°, con il massimo è 1°. Termini a inizio parola (`ai` non trova `mail`; il prezzo è che `profile` non trova `companyprofile`). Filtri ripetibili in OR, filtri diversi in AND. Un `project-log`, senza campi data, prende la data della riga di log più recente (aggiunto in revisione).
- Prefisso di commit nuovo `inbox:` (`inbox: cattura <slug>`, `inbox: smistamento`) perché `vault:` è riservato a struttura e configurazione: in CLAUDE.md §7 e SPEC §11.
- `/smista` cita come fonte il diario della sessione: se non esiste lo crea con `nuova-nota.py session` nello stesso commit, perché un wikilink verso una nota assente blocca il commit; `/chiudi-sessione` poi lo aggiorna.
- `/cattura` non chiede conferma; su un branch `claude/` committa lì e lo dice, senza push su `main`.
- Criterio dello step 17 verificato: 10 domande di prova con risposta attesa letta prima dal vault, più una domanda di controllo fuori knowledge; 10 su 10 corrette con le fonti, il controllo ha avuto "nel vault non c'è" senza invenzioni. Tabella in `sessions/_raw/2026-10-27-librarian-10-domande.md`. Difetto: risposte lunghe; aggiunto nel librarian il limite di 3–8 righe per la risposta, il contesto solo se chiesto.
- Due lacune segnalate dal librarian corrette subito con `aggiorna-nota.py`: `pulse-light` collegato a [[velo-ce]], `manini-relazione-processi-gestione-materiali` collegata a [[manini-supply-chain-magazzino]]. Le altre sono negli aperti.
- Permessi di `.claude/settings.json` per `cerca.py` e `plancia.py` e per `mcp__github__get_file_contents` (letto dal librarian): aggiunti dopo l'ok esplicito di Lorenzo, a PR #28 già unita, con una PR a sé. Senza, `/oggi`, `/progetto`, `/smista` e il librarian chiedono il permesso a ogni chiamata.
- SPEC 1.20 nella stessa PR dello step (come lo step 12): §3 (`cerca.py`), §4.4 (riga nella tabella degli script), §8 (comandi descritti, tolta la frase "previsti ma non ancora"), §9.3 (librarian per esteso), §11 (`inbox:`). README allineato.
- Incidente del subagente, chiuso: due note di prova finite in `inbox/` del vault reale per un `cd` fallito, cancellate subito; `inbox/` ha solo `.gitkeep`.
- Revisione del cockpit. Risposte di Lorenzo alle tre domande: la mattina guarda scadenze delle attività, eventi in programma e stato dei progetti con i prossimi passi; vuole una panoramica molto visuale dove le questioni aperte saltino all'occhio e il dettaglio arrivi dopo un tocco; da PC e da telefono; la mod non gli serve; non vuole agire dalla pagina (agisce tramite Claude). Opzioni valutate: A pagina HTML statica rigenerata dal task e pubblicata come artifact; B `home.md` potenziata; C ridisegnare la dashboard attuale (scartata: resta su funzioni in early access); GitHub Pages scartata (repo pubblico o piano a pagamento, nomi dei clienti). Scelta di Lorenzo: A, con B come riserva.
- Cockpit v2 è lo step 16 per intero (SPEC 1.21): i pezzi di riproducibilità che stavano nel 16 passano allo step 13 (setup cloud, task da `vault.yaml`) e allo step 18 (guida di installazione). Mod dell'app desktop e dashboard di tipo Dashboard ritirate: via le righe in SPEC §2 e §8, via dalla decisione aperta in §14.
- Architettura: `plancia.py` resta la fonte dei dati (aggiunti `prossimi_passi`, `percorso`, `clienti_slug`, `scadute`, `prossima_fonte` in `progetti.json`); il task legge il calendario dei prossimi 7 giorni con il connettore e lo scrive in `calendario.json` (solo titolo, orari, luogo, organizzatore, risposta: mai corpi, codici o link di riunione); `cockpit.py` fonde dati e template `.claude/templates/cockpit.html` in una pagina autosufficiente (nessuna risorsa esterna, `<details>` per il dettaglio, dark mode, link alle note su GitHub) e stampa la riga per il digest; il task la ripubblica con una chiamata `Artifact` sullo stesso URL. 17 test nuovi (222 in tutto). Screenshot a 390 e 1280 px rivisti in sessione: sopra la piega stanno testata, contatori e il blocco Oggi.
- Semafori: rosso "scaduto" (attività aperte con data passata), giallo "fermo da N giorni" (log oltre 14 giorni), verde "in ordine"; prima i progetti seguiti, poi quelli osservati più compatti. Il prossimo passo nella card chiusa sta in 2 righe, non 1: con i testi reali una riga non diceva nulla. Le attività dei progetti osservati compaiono in Oggi e Settimana con l'etichetta "osservi": da rivedere all'uso.
- Prima pubblicazione fatta dalla sessione con il calendario reale letto dal connettore: https://claude.ai/artifact/7N946t8Tup2PmCApWXpZNN, URL scritto nella routine e in `home.md`. La vecchia dashboard resta finché il criterio dei 3 giorni non è verificato.
- Permessi per `cockpit.py` e per `outlook_calendar_search` sui server `Microsoft_365` e `Microsoft-365`: un primo tentativo è stato bloccato dal classificatore della modalità Auto (auto-modifica); aggiunti poi con l'ok esplicito di Lorenzo, nella stessa PR #30. I task `cockpit` su claude.ai (connettore e modello) li sistema Lorenzo.
- Il task `cockpit` su claude.ai (`DailyBoard` e `DailyBoard2`) va modificato da Lorenzo: connettore Microsoft 365 (oggi nessuno), modello Sonnet; il prompt resta `Esegui il task descritto in .claude/routines/cockpit.md…`. Fatto da Lorenzo il 27/10.
- Chiusura, dall'utente: tutte le PR della sessione unite (#28, #29, #30, #31). Il primo giro osservato del Cockpit v2 è quello delle 07:40 del 27/10; il check-in delle 08:20 con `/verifica-task` copre lo step 12 e il cockpit. Dal cloud si pusha solo sul branch della sessione: anche il diario entra in `main` con una PR.

## File toccati

- `.claude/scripts/cerca.py`, `.claude/scripts/tests/test_cerca.py` (51 test; suite completa 205 verdi)
- `.claude/agents/librarian.md`
- `.claude/commands/oggi.md`, `progetto.md`, `cattura.md`, `smista.md`
- `SPEC.md` 1.20 (§3, §4.4, §8, §9.3, §11), `CLAUDE.md` §7, `README.md`
- `topics/pulse-light.md`, `sources/sharepoint/salesmarketing/proposals/customers/manini/manini-relazione-processi-gestione-materiali.md` (frontmatter)
- `projects/second-brain-prodotto/`: scheda e log
- `sessions/_raw/2026-10-27-librarian-10-domande.md`, questo diario
- `.claude/settings.json`: i tre permessi (seconda PR)
- Cockpit v2: `.claude/scripts/cockpit.py`, `.claude/templates/cockpit.html`, `.claude/scripts/tests/test_cockpit.py`, `plancia.py` e `test_plancia.py`, `.claude/routines/cockpit.md`, `home.md` (URL), `SPEC.md` 1.21 (§2, §3, §4.4, §7, §8, §13.1, §14), `README.md`
- Fuori dal repo: PR #28, #29, #30 e #31 (unite) e la PR di chiusura, dal branch `claude/peaceful-mendel-pas0wl`; artifact Cockpit v2 pubblicato; screenshot nello scratchpad della sessione, non conservati

## Aperti

- [x] Ok di Lorenzo per i permessi in `.claude/settings.json`: `Bash(python3 .claude/scripts/cerca.py:*)`, `Bash(python3 .claude/scripts/plancia.py:*)`, `mcp__github__get_file_contents` (chiuso: ok di Lorenzo, aggiunti nella PR successiva)
- [x] Unire la PR dello step 17 (SPEC 1.20) (chiuso: PR #28 unita)
- [x] Revisione del cockpit: risposte di Lorenzo alle tre domande, poi opzioni e raccomandazione; il risultato diventa il contenuto dello step 16 o uno step a sé (chiuso: opzione A scelta, è lo step 16, SPEC 1.21)
- [x] Aggiungere in `.claude/settings.json`: `Bash(python3 .claude/scripts/cockpit.py:*)`, `mcp__Microsoft_365__outlook_calendar_search`, `mcp__Microsoft-365__outlook_calendar_search` (chiuso: ok di Lorenzo, aggiunti nella PR #30)
- [x] Lorenzo: dare il connettore Microsoft 365 (e il modello Sonnet) ai due task `cockpit` su claude.ai, altrimenti la pagina esce senza calendario (chiuso: fatto da Lorenzo il 27/10)
- [x] Unire la PR dello step 16 (chiuso: PR #30 unita)
- [ ] Criterio dello step 16: 3 giri del task `cockpit` (27, 28, 29/10) senza errori, con `/verifica-task cockpit`, e pagina aperta dal telefono la mattina 📅 2026-10-30
- [ ] Dopo il criterio: cancellare la vecchia dashboard Cockpit (artifact di tipo Dashboard) e disattivare la mod sul PC
- [ ] Lacune del vault segnalate dal librarian (`sessions/_raw/2026-10-27-librarian-10-domande.md`): nome dell'AD di Manini; riga "sei giornate" nel log di [[manini-supply-chain-magazzino]]; quale calendario MTU è stato confermato il 26/10; foglio quotazione blocchi di Velo-CE non ingerito; risposta di Bollazzi (LIUC) da ingerire quando arriva
- [x] Provare `/oggi`, `/progetto`, `/cattura` e `/smista` in una sessione nuova (i comandi compaiono al riavvio) e correggere ciò che non torna (chiuso in [[2026-10-28-verifica-task-28-10]])
