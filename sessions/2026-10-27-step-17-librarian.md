---
type: session
date: 2026-10-27
surface: cloud
topics: ["[[second-brain]]"]
outcome: "Step 17 fatto: cerca.py con 51 test, agente librarian, comandi /oggi /progetto /cattura /smista; 10 domande di prova corrette con le fonti; SPEC 1.20 e PR aperta. Revisione del cockpit avviata con le tre domande a Lorenzo"
---

# Step 17 · librarian, ricerca e comandi; avvio della revisione del cockpit

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
- Permessi di `.claude/settings.json` per `cerca.py` e `plancia.py` e per `mcp__github__get_file_contents` (letto dal librarian): non aggiunti dalla sessione, come nello step 12; senza, `/oggi`, `/progetto`, `/smista` e il librarian chiedono il permesso a ogni chiamata. Si aggiungono con l'ok di Lorenzo.
- SPEC 1.20 nella stessa PR dello step (come lo step 12): §3 (`cerca.py`), §4.4 (riga nella tabella degli script), §8 (comandi descritti, tolta la frase "previsti ma non ancora"), §9.3 (librarian per esteso), §11 (`inbox:`). README allineato.
- Incidente del subagente, chiuso: due note di prova finite in `inbox/` del vault reale per un `cd` fallito, cancellate subito; `inbox/` ha solo `.gitkeep`.
- Revisione del cockpit: prima le tre domande a Lorenzo (cosa guarda la mattina, cosa manca, telefono o PC), poi opzioni con pro e contro; vincolo: basi stabili (markdown, git, task, `plancia.py`), niente early access; nessuna implementazione senza ok.

## File toccati

- `.claude/scripts/cerca.py`, `.claude/scripts/tests/test_cerca.py` (51 test; suite completa 205 verdi)
- `.claude/agents/librarian.md`
- `.claude/commands/oggi.md`, `progetto.md`, `cattura.md`, `smista.md`
- `SPEC.md` 1.20 (§3, §4.4, §8, §9.3, §11), `CLAUDE.md` §7, `README.md`
- `topics/pulse-light.md`, `sources/sharepoint/salesmarketing/proposals/customers/manini/manini-relazione-processi-gestione-materiali.md` (frontmatter)
- `projects/second-brain-prodotto/`: scheda e log
- `sessions/_raw/2026-10-27-librarian-10-domande.md`, questo diario
- Fuori dal repo: PR dal branch `claude/peaceful-mendel-pas0wl`

## Aperti

- [ ] Ok di Lorenzo per i permessi in `.claude/settings.json`: `Bash(python3 .claude/scripts/cerca.py:*)`, `Bash(python3 .claude/scripts/plancia.py:*)`, `mcp__github__get_file_contents`
- [ ] Unire la PR dello step 17 (SPEC 1.20)
- [ ] Revisione del cockpit: risposte di Lorenzo alle tre domande, poi opzioni e raccomandazione; il risultato diventa il contenuto dello step 16 o uno step a sé
- [ ] Lacune del vault segnalate dal librarian (`sessions/_raw/2026-10-27-librarian-10-domande.md`): nome dell'AD di Manini; riga "sei giornate" nel log di [[manini-supply-chain-magazzino]]; quale calendario MTU è stato confermato il 26/10; foglio quotazione blocchi di Velo-CE non ingerito; risposta di Bollazzi (LIUC) da ingerire quando arriva
- [ ] Provare `/oggi`, `/progetto`, `/cattura` e `/smista` in una sessione nuova (i comandi compaiono al riavvio) e correggere ciò che non torna
