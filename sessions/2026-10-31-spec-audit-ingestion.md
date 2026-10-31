---
type: session
date: 2026-10-31
surface: cloud
topics: ["[[second-brain]]"]
outcome: "SPEC 1.27 con le decisioni dell'audit ingestion (6.1, 6.2, 6.3, 6.4 riscritta, 4.3, 4.4, 7, 13.1), vault.yaml con profondità per libreria, soglia 5, fonti.canoniche e task reconcile-ridotta, config.py che li valida con 10 test nuovi; PR dedicata da un branch claude/"
---

# SPEC 1.27: decisioni dell'audit ingestion

## Obiettivo

Portare nella SPEC le decisioni dell'audit dell'ingestion (`proposals/2026-10-31-audit-ingestion.md` §6) e le aggiunte elencate nella PR #60 di P4 e P5, con una PR dedicata su un branch `claude/`, toccando solo `SPEC.md`, `vault.yaml` e `config.py` con i suoi test.

## Decisioni

- Versione 1.27: 6.1 descrive `riconciliazione_dovuta` e `ultimo_giro` con i comandi di `stato.py` che li scrivono e la regola del merge driver; 6.2 passo 6 affida il watermark a `set-watermark --da-giro`, passo 7 tiene il segnale finché `set-riconciliata` non lo chiude e il digest lo ripete ogni giorno; 6.3 passo 8 usa `set-giro outlook`
- 6.4 riscritta sulle decisioni 1–3 del report: identità per regola (stesso nome o famiglia nella stessa libreria = stessa nota, `removed` solo senza candidati per due riconciliazioni consecutive), cartella canonica da `fonti.canoniche`, riconciliazione ridotta come task separato con il piano di `riconcilia.py` (`--elenco`, `--fonte`, `--libreria`, `--applica`, voci `sposta`, `nuova_voce`, `copia`, `recupera`, `rimuovi`) e `sposta-nota.py`; nota di transizione: finché gli script non esistono vale la 1.26
- Task `reconcile-ridotta` alle 09:10, ogni giorno, Sonnet, Microsoft 365: dopo `ingest-sharepoint` e fuori dall'ora piena (regola di SPEC 7), non alle 09:00 del report; separato dal delta perché un riordino grande non allunghi il giro oltre il limite della sessione
- Step 13 chiuso il 31/10 (criterio verificato, il giro anomalo non è dello step); step nuovo numerato `17b` «Affidabilità ai riordini» prima del 18, per non rinumerare 18–20 citati in 13.2, 14, `vault.yaml` e negli agenti; criterio il test T11 del report
- 4.3: riga `- Da rileggere dopo [[fonte]] vN del AAAA-MM-GG` nelle hub a ogni nuova versione, rilettura in sessione, lista nel digest oltre 7 giorni (decisione 4); 4.4: controlli stato ↔ note ↔ fonti e golden test `--verifica` in CI, con nota di transizione perché `famiglia.py` oggi è sotto la soglia (82,5% secco)
- Dove la SPEC ripeteva valori di `vault.yaml` («oggi 2», «oggi 10», l'ordine delle canoniche) ora rimanda (step 14)
- `vault.yaml`: `profondita` per libreria (2 SalesMarketing, 4 Delivery, 2 Shared Documents, 2 OneDrive), `soglia_id_nuovi: 5`, `fonti.canoniche` (SalesMarketing, Delivery, Shared Documents, onedrive, `sharepoint:*` per gli altri siti). `config.py`: `profondita` intero o oggetto per libreria completato con il default, `canoniche()` con default dall'ordine del perimetro, `rango_canonico()` per scegliere la copia `current`; l'elenco deve nominare ogni libreria e `onedrive`, senza doppioni
- Agenti, routine e workflow CI non toccati in questa PR, come chiesto: li allinea la sessione di P1–P3, con il prompt nella PR

## File toccati

- `SPEC.md` (1.27: 2.1, 3, 4.3, 4.4, 6.1, 6.2, 6.3, 6.4, 7, 13.1)
- `vault.yaml`
- `.claude/scripts/config.py`, `.claude/scripts/tests/test_config.py` (10 test nuovi, 308 verdi)
- `sessions/`: questo diario

## Aperti

- [ ] Unire la PR della SPEC 1.27 e creare a mano il task `reconcile-ridotta` in claude.ai (ogni giorno 09:10, Sonnet, Microsoft 365) quando la routine `.claude/routines/reconcile-ridotta.md` esiste (sessione P1–P3)
- [ ] Sessione P1–P3 con il prompt della PR: `stato.py` (identità), `sposta-nota.py`, `riconcilia.py`, routine `reconcile-ridotta.md`, `ingestor.md` e `ingest-sharepoint.md` allineati a 6.2 e 6.4, workflow CI con `perimetro.py --verifica` e `famiglia.py --verifica`
- [ ] Dopo l'unione: riga nel log di `second-brain-prodotto` per lo step 13 chiuso e lo step 17b aperto (non scritta qui perché la PR tocca solo SPEC e configurazione)
