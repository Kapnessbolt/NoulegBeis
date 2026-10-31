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

## File toccati

- `vault.yaml` (esclusione `old versions`)
- 25 note in `sources/sharepoint/` spostate; 5 note aggiornate come nuove versioni: [[blueage-companyprofile]], [[blueage-sintesi]], [[blueage-onepage]], [[blueage-possibilita]], [[blueage-ai-che-cresce-onepage]]
- `.state/sharepoint.json`
- `journal/2026-10-31.md` (esito dei task)

## Aperti

- [ ] Rileggere `## Punti chiave` di [[ai-che-cresce-con-lazienda]] (descrive ancora la v2) e dei temi segnalati da `controlla-vault.py`: [[pulse]], [[parts-radar]], [[trade-spending]], [[manager-operativo]]
- [ ] `famiglia.py` non riconosce `_MEETING` come suffisso (Possibilità v3 attribuita a mano alla famiglia `blueage-possibilita`)
- [ ] SPEC 5 (cartelle escluse) da allineare con `old versions`, con una PR dedicata
- [ ] Regola del delta dopo un riordino: il watermark non deve superare file che la ricerca non ha ancora restituito
- [x] Criterio dello step 13: il giro anomalo del 31/10 non conta come errore dello step, verifica confermata all'1/11 (chiuso in [[2026-10-31-riordino-sharepoint]])
- [ ] Verificare che la riconciliazione del 01/11 sistemi il deck Trade Spending cliente e non generi note dalle versioni vecchie
