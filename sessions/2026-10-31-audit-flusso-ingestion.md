---
type: session
date: 2026-10-31
surface: cloud
topics: ["[[second-brain-prodotto]]", "[[second-brain]]"]
outcome: "Audit dell'affidabilità dinamica di ingestion e riconciliazione (PR #58 unita): 4 criticità alte, piano in 13 interventi, 7 decisioni prese da Lorenzo; step 13 chiuso, step nuovo sui riordini"
---

# Audit dell'ingestion e della riconciliazione

## Obiettivo

Verificare, solo sul repo e senza connettori, se il flusso ingestion → riconciliazione → conoscenza regge ai cambi delle fonti (riordini, copie, indice in ritardo, giri falliti o sovrapposti) senza interventi manuali, e scrivere il report con il piano in `proposals/`.

## Decisioni

- Verdetto: il flusso non è affidabile in modo dinamico. Tre cambi delle fonti in dieci giorni (copia Velo-CE 28/10, ricaricamento 29/10, riordino 30/10), tre recuperi manuali; la causa è architetturale: identità per ID dell'item, riconciliazione in quattro righe mai eseguita per intero, regole decisive (watermark, spostamenti) in prosa per l'LLM.
- Criticità alte: identità per ID (36 voci di stato orfane, 117 note con più voci); watermark oltre file non restituiti dall'indice senza segnale (fermo dal 19 al 29/10 per regola non applicata); rilevatore che consuma il segnale nello stesso giro anche se la riconciliazione fallisce (scenario sintetico); riconciliazione sottospecificata e tutta a carico dell'agente.
- Il report è una proposta `accettata` con le 7 decisioni di Lorenzo (dall'utente): identità per regola in uno script, `removed` solo dopo due riconciliazioni senza candidati; cartella canonica in `vault.yaml` per scegliere `current` tra le copie; riconciliazione ridotta come task separato con Sonnet dopo che uno script prepara il piano; hub superate rilette in sessione con la lista nel digest; profondità 4 e soglia 5 da subito; step 13 chiuso e affidabilità ai riordini come step nuovo di SPEC 13.1 prima dello step 18; nel prodotto rilevatore e riconciliazione automatica, BlueAge solo sulle eccezioni.
- Implementazione in una sessione a parte, nell'ordine del piano: P4 e P5 (segnale persistente, registro del giro), poi P1–P3 (identità e riconciliazione nel codice), poi P6 e P7, infine P8–P13 (dall'utente).
- Il diario è committato sul branch dell'audit, già unito, e arriva su `main` con una PR: la sessione non fa push su `main`.

## File toccati

- `proposals/2026-10-31-audit-ingestion.md` (nuovo, PR #58 unita)
- `projects/second-brain-prodotto/second-brain-prodotto.md`, `second-brain-prodotto-log.md`
- `sessions/2026-10-31-audit-flusso-ingestion.md`
- Fuori dal repo: scenari di prova di `stato.py` nello scratchpad della sessione

## Aperti

- [x] Implementare P4 e P5 del report (segnale di riordino persistente e registro del giro in `stato.py`, con test e controllo) in una PR, poi P1–P3 (chiuso in [[2026-10-31-spec-1-29]]): PR #60 e #62 unite
- [x] Aggiungere a SPEC 13.1 lo step sull'affidabilità ai riordini (criterio: test T11 del report) con la PR dedicata, insieme alle decisioni 1, 2 e 5 (identità, cartella canonica, soglie in `vault.yaml`) (chiuso in [[2026-10-31-spec-audit-ingestion]])
- [ ] `/verifica-task` dell'1/11 come da [[2026-10-31-riordino-sharepoint]]: con lo step 13 chiuso resta da verificare la riconciliazione e la prima fotografia delle cartelle 📅 2026-11-01
