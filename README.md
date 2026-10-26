# Second Brain BlueAge

Vault personale sulla knowledge BlueAge, gestito da Claude Code in cloud e consultabile con Obsidian.

- Specifica: [`SPEC.md`](SPEC.md)
- Istruzioni per l'agente: [`CLAUDE.md`](CLAUDE.md)

## Come si usa

1. **Lavorare**: apri una sessione su claude.ai/code su questo repo. L'agente legge `CLAUDE.md` e sa dove scrivere.
2. **Catturare**: `/cattura <testo>` crea una nota in `inbox/`; `/smista` la porta nel progetto o nel tema giusto.
3. **Fare il punto**: `/oggi` per l'agenda, `/progetto <nome>` per lo stato di un progetto.
4. **Controllare**: `/controlla` segnala errori e possibili doppioni nel vault e mostra l'indice di progetti, clienti, persone e temi. `/verifica-task [task] [data]` controlla i giri dei task schedulati: digest, commit, watermark, doppioni.
5. **Ingerire**: `/ingest [fonte] [da data]` porta nel vault le novità di SharePoint, OneDrive, Outlook e dei repo GitHub di progetto; `/ingest-file <url o nome>` un singolo documento.
6. **Chiudere**: `/chiudi-sessione` (o "chiudiamo") scrive il diario in `sessions/`, spunta gli aperti chiusi e fa push.
7. **Migliorare il vault**: `/curator` legge i diari della settimana e apre una PR con le proposte (regole, comandi, hook) e gli aperti chiusi; gira anche da solo la domenica sera.
8. **Leggere**: clona il repo e aprilo come vault in Obsidian.

Disponibili: `/ingest`, `/ingest-file`, `/controlla`, `/verifica-task`, `/curator`, `/chiudi-sessione`. Gli altri comandi e l'ingestion automatica arrivano negli step successivi del piano (SPEC 13).

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
| `.state/` | Stato dell'ingestion |
| `.claude/` | Comandi, agenti, skill e hook di Claude Code |

## Obsidian

Dopo il clone, una volta sola: `git config core.hooksPath .githooks`. Attiva il controllo del vault prima di ogni commit, anche da Obsidian.


Imposta `_templates/` come cartella dei template (Impostazioni → Template). I template usano le variabili `{{title}}` e `{{date}}` del plugin core. Le attività usano il formato del plugin Tasks (`📅 AAAA-MM-GG`).
