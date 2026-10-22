# CLAUDE.md · Istruzioni operative del vault

Questo repo è il second brain personale di Lorenzo Curione sulla knowledge BlueAge. La specifica completa è in `SPEC.md`: in caso di dubbio vince la SPEC. Questo file dice cosa fare in ogni sessione.

## 1. All'avvio di ogni sessione

1. `git pull --rebase origin main`.
2. Leggi questo file. Leggi `SPEC.md` solo nelle sezioni che servono al compito.
3. Se il compito tocca un progetto, apri prima `projects/<slug>/<slug>.md`.

## 2. Dove scrivere ogni tipo di nota

| Cosa | Dove | Template | `type` |
|---|---|---|---|
| Cattura rapida da smistare | `inbox/AAAA-MM-DD-<slug>.md` | `_templates/inbox.md` | `inbox` |
| Scheda progetto | `projects/<slug>/<slug>.md` | `_templates/project-index.md` | `project` |
| Cronologia progetto | `projects/<slug>/<slug>-log.md` | `_templates/project-log.md` | `project-log` |
| Cliente o prospect | `clients/<slug>.md` | `_templates/client.md` | `client` |
| Persona (interna o esterna) | `people/<nome-cognome>.md` | `_templates/person.md` | `person` |
| Prodotto, offerta, metodo | `topics/<slug>.md` | `_templates/topic.md` | `topic` |
| Documento SharePoint | `sources/sharepoint/<libreria>/<percorso>/<famiglia>.md` | `_templates/source-doc.md` | `source-doc` |
| Documento OneDrive | `sources/onedrive/<percorso>/<famiglia>.md` | `_templates/source-doc.md` | `source-doc` |
| Thread di posta | `sources/mail/AAAA-MM/<slug-oggetto>.md` | `_templates/source-mail.md` | `source-mail` |
| Allegato senza copia su SharePoint/OneDrive | `sources/attachments/<famiglia>.md` | `_templates/source-doc.md` | `source-doc` |
| Digest giornaliero | `journal/AAAA-MM-DD.md` | `_templates/journal.md` | `journal` |
| Diario di sessione | `sessions/AAAA-MM-DD-<slug>.md` | `_templates/session.md` | `session` |
| Trascrizione grezza (hook) | `sessions/_raw/` | nessuno | nessuno |
| Proposta del curator | `proposals/AAAA-MM-DD-<slug>.md` | `_templates/proposal.md` | `proposal` |
| Stato dell'ingestion | `.state/ingest.json` | schema in SPEC 6.1 | — |

Regole di instradamento:
- La scheda progetto si chiama come la cartella (`projects/<slug>/<slug>.md`), così `[[<slug>]]` la apre; la cronologia è `<slug>-log.md`.
- `<percorso>` riproduce le cartelle dell'originale, in slug (`Knowledge/Offerte 2026/` → `knowledge/offerte-2026/`).
- `AAAA-MM` della mail è il mese del primo messaggio del thread. `<slug-oggetto>` è l'oggetto senza prefissi di risposta e inoltro (`RE:`, `R:`, `FW:`, `FWD:`, `I:`).
- I partecipanti di un thread si collegano a `people/<nome-cognome>.md`. Se la persona non ha una nota, creala dal template.
- Se non sai a quale progetto, cliente o tema appartiene qualcosa, scrivi in `inbox/` e non inventare collegamenti.
- Un'informazione nuova su un progetto va in due posti: una riga datata in `<slug>-log.md` e, se cambia lo stato, la sezione corrispondente di `<slug>.md`.
- Un'azione o una scadenza emersa da una fonte va come checkbox in `## Attività` di `<slug>.md` (con data e fonte) e come riga in `<slug>-log.md`.
- I progetti non si creano in automatico. Se una fonte riguarda un progetto che non esiste nel vault, lascia `projects: []` e proponi di crearlo: in una sessione interattiva con una nota in `inbox/`, nell'ingestion con una riga nel digest del giorno (`journal/`), perché l'ingestor non scrive in `inbox/`.

## 3. Chi può scrivere dove

| Chi | Dove |
|---|---|
| Task di ingestion (agente `ingestor`, modalità `schedulata`) | `sources/`, `journal/`, `.state/`, note nuove in `people/`. In aggiunta, solo righe nuove: `## Interazioni recenti` di `people/*.md`, `projects/<slug>/<slug>-log.md` e la sezione `## Attività` di `projects/<slug>/<slug>.md` |
| Ingestion da sessione interattiva (`/ingest`, `/ingest-file`, modalità `interattiva`) | Come sopra, più: note nuove in `clients/`, `topics/`, `inbox/`; righe nuove in `## Fonti` (o `## Interazioni recenti`) di quelle esistenti |
| Curator | `proposals/`, `sessions/` |
| Sessione interattiva | Ovunque |

Il curator non modifica mai `CLAUDE.md`, `.claude/` o `SPEC.md`: propone, e le modifiche entrano con la PR.
`SPEC.md` si modifica solo con una PR dedicata, anche dalle sessioni interattive.

## 4. Regole delle note

- Lingua: italiano.
- Nomi file: slug minuscolo con trattini, senza accenti (`entrata-merci-manini.md`). Persone: `nome-cognome`.
- Collegamenti: wikilink `[[slug]]` (senza percorso e senza `.md`). Gli slug devono essere unici in tutto il vault.
- Ogni nota in `sources/` si collega ad almeno un progetto, cliente o tema con i campi `projects`, `clients`, `topics`. Se la persona, il cliente o il tema non esiste ancora, crea la nota dal template; nei task schedulati si creano solo le persone, mentre per clienti e temi si scrive il wikilink e si propone la creazione nel digest del giorno.
- Persone: prima di crearne una cerca la sua email in `people/` (`email:`). Stessa email → è la stessa persona. Nome simile senza email coincidente → non creare e segnala il possibile doppione.
- Frontmatter YAML obbligatorio, con i campi del template del suo tipo. Non togliere campi: se non c'è il valore, lascia `[]`, `""` o `null`.
- Una nota descrive, non copia: riassunto, punti chiave, numeri, decisioni, azioni. Il dettaglio si legge dall'originale con il connettore.
- Attività: checkbox con data nel formato Obsidian Tasks `- [ ] testo 📅 AAAA-MM-GG` e la fonte in coda (`([[slug-fonte]])`).
- Date nel frontmatter: `AAAA-MM-GG` per i giorni, ISO 8601 UTC (`2026-10-22T06:50:00Z`) per gli istanti.

### Versioni dei documenti (SPEC 4.3)

- Una nota per famiglia, non per versione.
- Chiave della famiglia: cartella + nome normalizzato, senza suffissi di versione (`_v15`, `v2`, `- v001`), date ed estensione. Esempio: `BlueAge_CompanyProfile_v24.pdf` → `blueage-companyprofile`.
- `current` punta all'ultima versione; `versions` tiene lo storico dalla più recente.
- Nuova versione: rigenera il riassunto e scrivi le differenze rilevanti nel `<slug>-log.md` del progetto collegato.
- Stessa famiglia in un'altra posizione: aggiungi la posizione in `also_at`, non creare un'altra nota.

## 5. Cosa non va nel repo

- I documenti originali: restano su SharePoint, OneDrive e Outlook.
- I file prodotti dalle skill (pptx, mp4, png): si caricano su SharePoint o OneDrive con il connettore, e la nota del progetto riporta il link.

## 6. Perimetro delle fonti (sintesi di SPEC 5)

- SharePoint `sites/internal`: librerie Knowledge, SalesMarketing, Delivery, Shared Documents. Esclusi SiteAssets e le cartelle `_originali` e `_sorgenti`.
- OneDrive: solo la cartella `BlueAge/`. `BlueAge/_chat/` contiene i riassunti delle chat claude.ai → note `session` con `surface: claude-ai`.
- Outlook: tutta la casella, Inviate comprese. Scarta no-reply, notifiche di servizi, newsletter e marketing.

## 7. Git

- Prima di ogni commit: `python3 .claude/scripts/controlla-vault.py` (SPEC 4.4) e correggi gli errori che hai introdotto; poi `git pull --rebase origin main`, commit e push diretto su `main`.
- Conflitto su `.state/ingest.json`: vince la versione con il watermark più avanzato. Altri conflitti: riapplica la tua modifica sulla versione remota.
- Eccezione: il curator lavora su un branch `claude/curator-AAAA-MM-DD` e apre una PR.
- Messaggi di commit: `ingest(sharepoint): 12 note aggiornate`, `session: <slug>`, `project(<slug>): <cosa>`, `vault: <cosa>` per struttura e configurazione.

## 8. Fine sessione

Prima di chiudere una sessione interattiva scrivi il diario in `sessions/AAAA-MM-DD-<slug>.md` (obiettivo, decisioni, file toccati, aperti), poi commit e push. Ogni sessione parte da un clone nuovo: ciò che non è committato è perso.
