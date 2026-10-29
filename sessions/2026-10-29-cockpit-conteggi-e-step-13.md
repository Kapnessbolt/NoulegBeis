---
type: session
date: 2026-10-29
surface: cloud
topics: ["[[second-brain]]"]
outcome: "Tre difetti di conteggio del Cockpit corretti con i test (PR #40, mergiata); step 13 codificato con vault.yaml e config.py, in osservazione per tre giri dei task; script di setup cloud configurato e verificato (PR #40, #41, #42 unite); 118 note Velo-CE riallineate alla cartella rinominata prima della riconciliazione di domenica"
---

# Conteggi del Cockpit e step 13

## Obiettivo

Correggere i tre difetti di conteggio del Cockpit in scadenza il 31/10, ognuno con un test che fallisce prima e passa dopo; poi lo step 13 di SPEC 13.1 (configurazione separata dal motore in `vault.yaml`), una PR per punto.

## Decisioni

- Il codice dei tre difetti lo scrive un subagente Opus, la sessione rivede (dall'utente).
- Una nuova versione di un documento conta tra le note aggiornate, non tra le nuove: il Cockpit mostra "N note nuove · M aggiornate".
- Le decisioni del digest si contano tutte, con o senza data, tranne le righe che dicono solo che non c'è nulla ("Nessun progetto fermo…").
- Il giro del cockpit che genera la pagina è "In corso" nella pagina stessa e non entra nel totale "task OK su N"; la correzione sta in `cockpit.py` perché solo la pagina sa di essere quel giro, `/oggi` e `/verifica-task` restano su `task.json`.
- Step 13: il codice (`config.py`, script, test, setup cloud) lo scrive un subagente Opus; prosa di agenti, routine, comandi, SPEC e CLAUDE.md la sessione.
- `vault.yaml` sta alla radice, fuori da `.claude/`: il motore non contiene valori del vault, la configurazione sì. Contiene anche la sezione `agenti` (strumenti dei connettori per agente), perché ingestor e librarian non hanno gli stessi strumenti.
- I permessi dei connettori in `settings.json` e la riga `tools` degli agenti si generano da `vault.yaml` con `config.py applica`; `applica` resta fuori dai permessi automatici perché riscrive i permessi stessi, gli altri sottocomandi di `config.py` (sola lettura) ci sono.
- Gli orari dei task restano anche nella tabella di SPEC 7 finché lo step 14 non decide la fonte unica: il controllo del vault dà errore se divergono da `vault.yaml` (provato cambiando un orario in SPEC: 1 errore).
- Nella prosa il nome dell'utente e "BlueAge" come organizzazione lasciano il posto a `vault.utente` e `vault.organizzazione`; le skill `blueage-*` restano com'erano (contenuto, step 19). Le etichette del Cockpit restano in italiano nel codice (lingua: decisione commerciale, SPEC 14).
- Il quarto problema del Cockpit (righe di novità aggregate nel digest del 29/10, ammesse dalla routine `digest` oltre 30 voci) non entra in questa sessione: resta un'attività.

- Velo-CE: la rinomina di `Cristian/` in `Progetto Dynamics` non bastava, perché 64 note puntavano ancora agli ID dei file originali spariti con la copia e la riconciliazione, che ragiona per ID, le avrebbe segnate come rimosse. Riallineamento a mano delle note prima di domenica invece di rimandare la riconciliazione (dall'utente): elenco completo dei file della cartella (subagente Sonnet), abbinamento per ID, poi per copia in `also_at`, poi per famiglia ed estensione; 118 note aggiornate, 46 spostate da `cristian/` a `progetto-dynamics/`, 4 senza file lasciate alla riconciliazione. Promemoria di sabato cancellato: avrebbe detto che la riconciliazione sposta le note da sola.
- Vecchia dashboard Cockpit cancellata (dall'utente): sostituita dal Cockpit v2, nessun task la aggiornava più. La mod sul PC la disattiva l'utente.
- `perimetro.py` scriveva nel motivo la configurazione intera al posto del prefisso (regressione dello step 13, trovata nel riallineamento): corretta con un test.
- Lo script di setup su claude.ai cerca il file nel repo invece di richiamarlo con un percorso fisso, perché non è documentato se gira prima o dopo il clone; se non lo trova installa i pacchetti direttamente. Il vecchio `npm install` è tolto: il vault non ha `package.json`.

## File toccati

- `.claude/scripts/plancia.py`, `.claude/scripts/cockpit.py`, `.claude/routines/cockpit.md`
- `.claude/scripts/tests/test_plancia.py`, `.claude/scripts/tests/test_cockpit.py`
- `vault.yaml` (nuovo), `.claude/scripts/config.py` e `tests/test_config.py` (nuovi), `.claude/setup/ambiente-cloud.sh` (nuovo)
- `.claude/scripts/perimetro.py`, `famiglia.py`, `nuova-nota.py`, `controlla-vault.py`, test e `conftest.py` con un `vault.yaml` di prova
- `.claude/agents/*.md`, `.claude/routines/*.md`, `.claude/commands/*.md`, `.claude/skills/chiudi-sessione/SKILL.md`, `.claude/settings.json`, `.github/workflows/controllo-vault.yml`
- `SPEC.md` (1.23: nuova 2.1, 3, 4.4, 7, 10, 14), `CLAUDE.md` §6
- `projects/second-brain-prodotto/second-brain-prodotto.md`, `projects/second-brain-prodotto/second-brain-prodotto-log.md`
- `sources/sharepoint/delivery/customers/01-velo-ce/` (118 note, 46 spostate da `cristian/`), `.state/sharepoint.json`, `projects/velo-ce-progetto-dynamics/`
- Fuori dal repo: vecchia dashboard Cockpit (`KN8Wp48…`) cancellata; promemoria "Controllo rinomina cartella Velo-CE" del 31/10 cancellato

## Aperti

- [ ] Formato delle novità nel digest: righe aggregate del 29/10 (`Nuove (45): …`) non contate dal Cockpit
- [ ] Step 13: tre giri dei task dopo il merge (30, 31/10, 1/11) con `/verifica-task`
- [x] Script di setup dell'ambiente cloud nell'interfaccia di claude.ai: cerca `.claude/setup/ambiente-cloud.sh` e lo esegue, altrimenti installa i quattro pacchetti; verificato in una sessione nuova (yaml 6.0.3, pytest 9.2.0, pptx 1.0.2, fontTools 4.68.0)
- [ ] Step 14 solo con l'ok dell'utente
- [x] Disattivare la mod del Cockpit sull'app desktop del PC (utente): plugin rimosso, nessun plugin attivo sull'account
- [ ] Riconciliazione del 1/11: controllare che segni rimosse solo le 4 note Velo-CE senza file (Articoli version 1, Ricodifica rename o nuovo codice, App EOS quali servono, Domande per la call con So Smart)
