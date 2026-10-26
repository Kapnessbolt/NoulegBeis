# Second Brain BlueAge

Vault personale sulla knowledge BlueAge, gestito da Claude Code in cloud e in locale, consultabile in sola lettura con Obsidian.

- Specifica: [`SPEC.md`](SPEC.md)
- Istruzioni per l'agente: [`CLAUDE.md`](CLAUDE.md)

## Come si usa

1. **Lavorare**: apri una sessione su claude.ai/code su questo repo, oppure una sessione locale dell'app desktop sulla cartella del vault. L'agente legge `CLAUDE.md` e sa dove scrivere. Note, catture e smistamenti passano da qui: chiedili a parole (una cattura senza progetto va in `inbox/`).
2. **Controllare**: `/controlla` segnala errori e possibili doppioni nel vault e mostra l'indice di progetti, clienti, persone e temi. `/verifica-task [task] [data]` controlla i giri dei task schedulati: digest, commit, watermark, doppioni.
3. **Ingerire**: le novità di SharePoint, OneDrive, Outlook e dei repo GitHub di progetto entrano da sole con i task schedulati (SPEC 7), attivi dal 23/10. A mano: `/ingest [fonte] [da data]` dal watermark, `/ingest-file <url o nome>` per un singolo documento.
4. **Fare il punto**: la dashboard Cockpit su claude.ai (aggiornata dal task `cockpit` due volte al giorno) e il digest del giorno in `journal/`. Nelle sessioni locali la mod `cockpit` dell'app desktop apre il pannello e registra `/cockpit`; la mod vive fuori dal repo.
5. **Chiudere**: `/chiudi-sessione` (o "chiudiamo") scrive il diario in `sessions/`, spunta gli aperti chiusi e fa push.
6. **Migliorare il vault**: `/curator` legge i diari della settimana e apre una PR con le proposte (regole, comandi, hook) e gli aperti chiusi; gira anche da solo la domenica sera.
7. **Leggere**: Obsidian sul clone del repo, solo in lettura (sotto).

Disponibili: `/ingest`, `/ingest-file`, `/controlla`, `/verifica-task`, `/curator`, `/chiudi-sessione`. Skill nel vault: `chiudi-sessione`, `blueage-deck`, `blueage-corso`, `blueage-animazioni` (SPEC 10). Previsti dalla SPEC ma non ancora fatti: `/oggi`, `/progetto`, `/cattura`, `/smista` (SPEC 8).

## Dove sta cosa

| Cartella | Contenuto |
|---|---|
| `inbox/` | Catture rapide da smistare |
| `projects/<slug>/` | `<slug>.md` (scheda progetto) e `<slug>-log.md` (cronologia) |
| `clients/` | Clienti e prospect |
| `people/` | Persone interne ed esterne |
| `topics/` | Prodotti, offerte, metodi |
| `sources/` | Note sui documenti di SharePoint, OneDrive, posta, allegati e repo GitHub di progetto |
| `journal/` | Digest giornaliero |
| `sessions/` | Diario delle sessioni (`_raw/`: estratti di trascrizione, solo il pezzo che serve) |
| `proposals/` | Proposte del curator |
| `_templates/` | Template delle note |
| `.state/` | Stato dell'ingestion, un file per fonte (`sharepoint.json`, `onedrive.json`, `outlook.json`, `github.json`, `reconcile.json`); si legge e si scrive con `stato.py` |
| `.claude/` | Comandi, agenti, skill, hook, procedure dei task schedulati e script di Claude Code |
| `.claude/scripts/` | Script di servizio testati (`tests/`): controllo e rinomina delle note, famiglia e slug (`famiglia.py`), perimetro delle fonti (`perimetro.py`), stato dell'ingestion (`stato.py`), note dal template (`nuova-nota.py`, `aggiorna-nota.py`), dati della dashboard (`plancia.py`) |
| `.githooks/` | Pre-commit di git che lancia il controllo del vault |
| `.gitattributes` | Merge driver `stato` per i conflitti su `.state/*.json` |
| `.github/workflows/` | Controllo del vault su ogni push e PR |

## Obsidian

Obsidian serve solo a leggere il vault (link, backlink, grafo, ricerca, attività): modifiche e note nuove passano sempre da Claude. Così il clone sui dispositivi non va mai in conflitto con i task e le sessioni.

- Sincronizzazione solo in pull con il plugin Obsidian Git: pull all'avvio e ogni 10 minuti, commit e push automatici disattivati (intervallo 0). Sul telefono basta un token GitHub fine-grained in sola lettura (Contents: Read-only, solo questo repo).
- `.obsidian/` è fuori dal repo (`.gitignore`): ogni dispositivo ha la sua configurazione.
- Sui dispositivi non serve `git config core.hooksPath .githooks`: da lì non parte nessun commit. Il pre-commit lo attivano le sessioni Claude Code all'avvio.
- File esclusi (Impostazioni → File e link): `_templates/` e `sessions/_raw/`.
- `home.md` è la pagina iniziale, con le viste dei plugin Tasks e Dataview. Le attività usano il formato di Tasks (`📅 AAAA-MM-GG`).
