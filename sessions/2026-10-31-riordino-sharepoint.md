---
type: session
date: 2026-10-31
surface: cloud
topics: ["[[second-brain-prodotto]]", "[[blueage]]"]
outcome: "Riordino SharePoint del 30/10 recepito: 25 note spostate, 5 file recuperati, «99 - old versions» esclusa"
---

# Verifica dell'ingestion dopo il riordino di SharePoint

## Obiettivo

Verificare l'ingestion del 31/10 dopo il riordino delle librerie SharePoint fatto da Leonardo il 30/10 ([[sharepoint-cartelle-semplificate-e-ultimi-materiali-commerciali]]).

## Decisioni

- Il giro `ingest-sharepoint` del 31/10 è un'ANOMALIA: la ricerca non ha restituito 5 file modificati il 30/10 tra le 13:11 e le 13:13Z (indice non ancora aggiornato dopo lo spostamento) e il watermark è andato oltre. Recuperati in sessione con l'ingestor, senza toccare il watermark.
- Gli spostamenti non cambiano la data di modifica, quindi il delta quotidiano non li vede: 25 note spostate a mano nelle cartelle nuove (percorso da `perimetro.py`), con `current.web_url` e il percorso nello stato aggiornati. Il deck Trade Spending cliente resta nella cartella vecchia: la ricerca non dà ancora la nuova posizione, lo sistema la riconciliazione.
- «99 - old versions» esclusa dal perimetro (`old versions` in `vault.yaml`, esclusioni delle cartelle): le versioni superate non generano note.
- Le note di Sintesi, OnePage e Possibilità (sito partner) e di AI che cresce (allegato) sono state spostate in SalesMarketing e hanno come `current` la copia interna; la copia precedente resta in `versions` e `also_at`. Niente note doppie per cartella.
- L'esempio sull'entrata merci della v4 di [[blueage-ai-che-cresce-onepage]] è il caso [[manini]]: collegato il cliente.
- Cockpit delle 07:40 mancante (nessun commit).

## Decisioni sul rilevatore di riordino

- Niente agente nuovo: il rilevatore è un passo del delta di SharePoint (SPEC 6.2 passo 7) e il lavoro grosso resta la riconciliazione dell'`ingestor`, ridotta a una libreria (6.4). Segnali: fotografia delle cartelle fino a 2 livelli in `.state/sharepoint.json` (`stato.py set-cartelle`), almeno 10 ID nuovi in famiglie già note nella stessa cartella; GitHub con `git diff -M`; la posta segnala nel digest un riordino annunciato dopo il giro.
- Finestra del delta di SharePoint da 2 a 48 ore; parametri in `vault.yaml` (`fonti.rilevatore`), letti con `config.py rilevatore`.
- La riconciliazione ridotta gira dentro `ingest-sharepoint`, quindi con Opus; quella settimanale resta con Sonnet. A mano: `/ingest riconcilia sharepoint:<libreria>`, senza un comando nuovo.

## File toccati

- `vault.yaml` (esclusione `old versions`)
- 25 note in `sources/sharepoint/` spostate; 5 note aggiornate come nuove versioni: [[blueage-companyprofile]], [[blueage-sintesi]], [[blueage-onepage]], [[blueage-possibilita]], [[blueage-ai-che-cresce-onepage]]
- `.state/sharepoint.json`
- `journal/2026-10-31.md` (esito dei task)
- Rilevatore: `SPEC.md` (1.26: 5, 6.1–6.4, 6.6, 7, 8), `.claude/agents/ingestor.md`, `.claude/routines/ingest-sharepoint.md`, `.claude/commands/ingest.md`, `.claude/scripts/stato.py` e `config.py` con i test, `vault.yaml`

## Aperti

- [ ] Rileggere `## Punti chiave` di [[ai-che-cresce-con-lazienda]] (descrive ancora la v2) e dei temi segnalati da `controlla-vault.py`: [[pulse]], [[parts-radar]], [[trade-spending]], [[manager-operativo]]
- [ ] `famiglia.py` non riconosce `_MEETING` come suffisso (Possibilità v3 attribuita a mano alla famiglia `blueage-possibilita`)
- [x] SPEC 5 (cartelle escluse) da allineare con `old versions`, con una PR dedicata (chiuso in [[2026-10-31-riordino-sharepoint]])
- [x] Regola del delta dopo un riordino: finestra di 48 ore e rilevatore di riordino con riconciliazione ridotta, SPEC 1.26 (chiuso in [[2026-10-31-riordino-sharepoint]])
- [x] Criterio dello step 13: il giro anomalo del 31/10 non conta come errore dello step, verifica confermata all'1/11 (chiuso in [[2026-10-31-riordino-sharepoint]])
- [ ] Verificare che la riconciliazione del 01/11 sistemi il deck Trade Spending cliente e non generi note dalle versioni vecchie
