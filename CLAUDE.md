# CLAUDE.md · Istruzioni operative del vault

Questo repo è il second brain personale di Lorenzo Curione sulla knowledge BlueAge. La specifica completa è in `SPEC.md`: in caso di dubbio vince la SPEC. Questo file dice cosa fare in ogni sessione.

## 1. All'avvio di ogni sessione

1. `git pull --rebase origin main`. Lo fa l'hook di avvio (`.claude/hooks/pull-inizio-sessione.sh`), in cloud e in locale: se nel contesto c'è "Vault allineato" è fatto; se dice saltato o non riuscito, fallo tu.
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
| Documento o issue di un repo di progetto (SPEC 5.4) | `sources/github/<repo>/<percorso>/<repo>-<nome>.md`, issue in `issues/<repo>-issue-<n>.md` | `_templates/source-doc.md` | `source-doc` |
| Digest giornaliero | `journal/AAAA-MM-DD.md` | `_templates/journal.md` | `journal` |
| Diario di sessione | `sessions/AAAA-MM-DD-<slug>.md` | `_templates/session.md` | `session` |
| Trascrizione grezza (hook) | `sessions/_raw/` | nessuno | nessuno |
| Proposta del curator | `proposals/AAAA-MM-DD-<slug>.md` | `_templates/proposal.md` | `proposal` |
| Stato dell'ingestion | `.state/ingest.json` | schema in SPEC 6.1 | — |
| Vista Obsidian (Tasks e Dataview) | `home.md`, fuori dal controllo del vault | nessuno | `home` |

Regole di instradamento:
- La scheda progetto si chiama come la cartella (`projects/<slug>/<slug>.md`), così `[[<slug>]]` la apre; la cronologia è `<slug>-log.md`.
- `<percorso>` riproduce le cartelle dell'originale, in slug (`SalesMarketing/Offerte 2026/` → `salesmarketing/offerte-2026/`).
- `AAAA-MM` della mail è il mese del primo messaggio del thread. `<slug-oggetto>` è l'oggetto senza prefissi di risposta e inoltro (`RE:`, `R:`, `FW:`, `FWD:`, `I:`).
- I partecipanti di un thread si collegano a `people/<nome-cognome>.md`. Se la persona non ha una nota, creala dal template.
- Se non sai a quale progetto, cliente o tema appartiene qualcosa, scrivi in `inbox/` e non inventare collegamenti.
- Un'informazione nuova su un progetto va in due posti: una riga datata in `<slug>-log.md` e, se cambia lo stato, la sezione corrispondente di `<slug>.md`.
- Un'azione o una scadenza emersa da una fonte va come checkbox in `## Attività` di `<slug>.md` (con data e fonte) e come riga in `<slug>-log.md`.
- I progetti non si creano in automatico. Se una fonte riguarda un progetto che non esiste nel vault, lascia `projects: []` e proponi di crearlo: in una sessione interattiva con una nota in `inbox/`, nell'ingestion con una riga nel digest del giorno (`journal/`), perché l'ingestor non scrive in `inbox/`.

## 3. Chi può scrivere dove

| Chi | Dove |
|---|---|
| Task di ingestion (agente `ingestor`, modalità `schedulata`) | `sources/`, `journal/`, `.state/`, note nuove in `people/`, `clients/`, `topics/`. In aggiunta, solo righe nuove: `## Interazioni recenti` di `people/*.md`, `projects/<slug>/<slug>-log.md` e la sezione `## Attività` di `projects/<slug>/<slug>.md` |
| Ingestion da sessione interattiva (`/ingest`, `/ingest-file`, modalità `interattiva`) | Come sopra, più: note nuove in `inbox/`; righe nuove in `## Fonti` di clienti e temi esistenti |
| Curator | `proposals/`, `sessions/` |
| Sessione interattiva | Ovunque |

Il curator non modifica mai `CLAUDE.md`, `.claude/` o `SPEC.md`: propone, e le modifiche entrano con la PR.
`SPEC.md` si modifica solo con una PR dedicata, anche dalle sessioni interattive.

## 4. Regole delle note

- Lingua: italiano.
- Nomi file: slug minuscolo con trattini, senza accenti (`entrata-merci-manini.md`). Persone: `nome-cognome`.
- Collegamenti: wikilink `[[slug]]` (senza percorso e senza `.md`). Gli slug devono essere unici in tutto il vault.
- Integrità: mai un wikilink verso una nota che non esiste. Se la destinazione manca, creala. Per rinominare una nota usa `python3 .claude/scripts/rinomina-nota.py <vecchio> <nuovo>`: aggiorna tutti i collegamenti e lo stato.
- Tracciabilità: nei temi (`## Punti chiave`), clienti (`## Chi sono`, `## Relazione con BlueAge`) e progetti (`## Stato`, `## Decisioni`) ogni punto finisce con la fonte, `([[slug-fonte]])`. Se l'informazione viene da te in sessione, la fonte è il diario della sessione.
- Ogni nota in `sources/` si collega ad almeno un progetto, cliente o tema con i campi `projects`, `clients`, `topics`. Se la persona, il cliente o il tema non esiste ancora, crea la nota dal template. Nei task schedulati clienti e temi nuovi nascono come note minime con il tag `da-verificare`: rivedile e togli il tag.
- Persone: prima di crearne una cerca la sua email in `people/` (`email:`). Stessa email → è la stessa persona. Nome simile in una nota senza email → è la stessa persona. Nome simile con email diversa → crea la nuova persona. Negli ultimi due casi segnala il possibile doppione.
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
- Dati riservati, nemmeno riassunti: credenziali, token, codici di accesso e di riunione; IBAN e coordinate bancarie; GUID, tenant ID e account dei sistemi dei clienti; compensi e contratti personali; indirizzi e telefoni personali; CV. La nota dice che il documento li contiene ("credenziali del web service demo, omesse"), non il valore.
- Dati reali dei clienti riga per riga (DDT, ordini, anagrafiche, export di tabelle): restano su OneDrive nelle cartelle `Dati/` e non generano note. La nota del progetto cita solo la cartella e i numeri aggregati. Se la policy AI del cliente limita l'uso dei dati, scrivilo nella nota del cliente.
- Thread personali o estranei a BlueAge: non si ingeriscono. Nel dubbio, in sessione chiedi; nei task schedulati scartali e annotali come gli altri scarti (mittente · oggetto).

## 6. Perimetro delle fonti (sintesi di SPEC 5)

- SharePoint `sites/internal`: librerie SalesMarketing, Delivery, Shared Documents. Escluse le librerie Knowledge (corsi Anthropic) e SiteAssets, e le cartelle `_originali` e `_sorgenti`.
- OneDrive: solo la cartella `BlueAge/`, con tutte le sue sottocartelle tranne le cartelle `Dati` (dati reali dei clienti, §5). La cartella il cui nome finisce con `chat` (oggi `BlueAge/00_chat/`) contiene i riassunti delle chat claude.ai → note `session` con `surface: claude-ai`.
- Outlook: tutta la casella, Inviate comprese. Scarta no-reply, notifiche di servizi, newsletter e marketing.
- GitHub: solo i file e le issue elencati in SPEC 5.4 (oggi il repo `cristian-schifone/parts-radar`, branch `main`). Nel vault va il livello di progetto (stato, decisioni, scadenze, azioni fuori dal codice), mai il dettaglio tecnico.

## 7. Git

- Prima di ogni commit: `python3 .claude/scripts/controlla-vault.py` (SPEC 4.4) e correggi gli errori che hai introdotto. Il pre-commit di git (`.githooks/pre-commit`, attivato a inizio sessione) blocca comunque il commit se restano errori nei file modificati. Poi commit, `git pull --rebase origin main` (dopo il commit: con modifiche non committate il rebase si rifiuta) e push diretto su `main`.
- Conflitto su `.state/ingest.json`: vince la versione con il watermark più avanzato. Altri conflitti: riapplica la tua modifica sulla versione remota.
- Eccezione: il curator lavora su un branch `claude/curator-AAAA-MM-DD` e apre una PR.
- Messaggi di commit: `ingest(sharepoint): 12 note aggiornate`, `session: <slug>`, `project(<slug>): <cosa>`, `vault: <cosa>` per struttura e configurazione.

## 8. Fine sessione

Prima di chiudere una sessione interattiva usa la skill `chiudi-sessione` (`/chiudi-sessione`, o quando Lorenzo dice "chiudiamo"): scrive il diario in `sessions/AAAA-MM-DD-<slug>.md` (obiettivo, decisioni, file toccati, aperti), spunta gli aperti dei diari precedenti chiusi nella sessione, poi commit e push. Ogni sessione parte da un clone nuovo: ciò che non è committato è perso.
