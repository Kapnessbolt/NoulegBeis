---
paths:
  - "sources/**"
---

# Note fonte (`sources/`)

Regole che valgono quando scrivi o rileggi una nota in `sources/`. Le regole generali (dove va una nota, chi può scrivere dove, dati riservati, git) sono in `CLAUDE.md`; la specifica è in `SPEC.md` 4.2–4.3.

## Percorso

- `<percorso>` riproduce le cartelle dell'originale, in slug (`SalesMarketing/Offerte 2026/` → `salesmarketing/offerte-2026/`); lo calcola `python3 .claude/scripts/perimetro.py "<webUrl>" --json` (`cartella_nota`).
- Una nota fonte di SharePoint o OneDrive si sposta o si rinomina solo con `python3 .claude/scripts/sposta-nota.py <nota> --web-url "<nuovo webUrl>"` (cartella da `perimetro.py`, `git mv`, `current.*`, `family` e slug con i wikilink, stato; con `--item-id`/`--uri` anche la voce nuova dello stato), mai con `git mv` o `rinomina-nota.py` a mano (SPEC 6.4).
- Posta: `sources/mail/AAAA-MM/<slug-oggetto>.md`, dove `AAAA-MM` è il mese del primo messaggio del thread e `<slug-oggetto>` è l'oggetto senza prefissi di risposta e inoltro (`RE:`, `R:`, `FW:`, `FWD:`, `I:`): `python3 .claude/scripts/famiglia.py --oggetto "<oggetto>"`.
- I partecipanti di un thread si collegano a `people/<nome-cognome>.md`. Se la persona non ha una nota, creala dal template (prima cerca la sua email in `people/`, `CLAUDE.md` §4).

## Collegamenti

- Ogni nota in `sources/` si collega ad almeno un progetto, cliente o tema con i campi `projects`, `clients`, `topics`. Collega solo ciò che la fonte nomina. Se il cliente o il tema non esiste ancora, crea la nota dal template; nei task schedulati clienti e temi nuovi nascono come note minime con il tag `da-verificare`.
- Se la fonte riguarda un progetto che non esiste nel vault, lascia `projects: []` e proponi di crearlo (`CLAUDE.md` §2): i progetti non si creano in automatico.

## Versioni dei documenti (SPEC 4.3)

- Una nota per famiglia, non per versione.
- Chiave della famiglia: cartella + nome normalizzato, senza suffissi di versione (`_v15`, `v2`, `- v001`), date ed estensione. Esempio: `BlueAge_CompanyProfile_v24.pdf` → `blueage-companyprofile`. La calcola `python3 .claude/scripts/famiglia.py "<nome file>"`; prima di creare una nota, `famiglia.py --cerca "<nome file>" --cartella <cartella>` dice se la famiglia esiste già.
- `current` punta all'ultima versione; `versions` tiene lo storico dalla più recente, con la `current` come prima voce. Il frontmatter lo scrivono `nuova-nota.py` e `aggiorna-nota.py`, mai a mano: `--nuova-versione` per una nuova corrente, `--versione name=... item_id=... last_modified=...` per un ID superato dello stesso documento che resta nello stato, `--versioni-in-ordine` se il controllo avvisa che la prima voce non è la `current`.
- Le voci dello stato non si cancellano: un ID superato resta nello stato e in `versions`. Solo un ID refuso, mai esistito alla fonte, si toglie: prima `python3 .claude/scripts/stato.py rimuovi-voce <fonte> <chiave> --motivo "<perché è un refuso>"`, poi `aggiorna-nota.py <nota> --togli-versione <item_id>` (SPEC 6.1). Mai per un documento sparito: quello lo segna la riconciliazione con `status: removed`.
- Nuova versione: rigenera il riassunto e scrivi le differenze rilevanti in testa al `<slug>-log.md` del progetto collegato.
- Stessa famiglia in un'altra posizione: aggiungi la posizione in `also_at` (`aggiorna-nota.py <nota> --also-at web_url=<url> item_id=<id>`), non creare un'altra nota.

## Contenuto

- Una nota descrive, non copia: riassunto di 3–6 righe, punti chiave, numeri, decisioni, azioni. Il dettaglio si legge dall'originale con il connettore.
- Niente dati riservati, nemmeno riassunti (`CLAUDE.md` §5): la nota dice che il documento li contiene, non il valore.
- Un'azione o una scadenza emersa dalla fonte va anche nel progetto: checkbox in `## Attività` di `projects/<slug>/<slug>.md` e riga datata in `<slug>-log.md`, con la fonte in coda `([[slug-fonte]])`.
