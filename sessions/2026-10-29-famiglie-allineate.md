---
type: session
date: 2026-10-29
surface: cloud
topics: ["[[second-brain]]"]
outcome: "6 note source-doc rinominate per allineare slug e family alla chiave calcolata da famiglia.py; le altre 7 in disaccordo restano come sono"
---

# Famiglie allineate a famiglia.py

## Obiettivo

Chiudere l'aperto del diario [[2026-10-29-cockpit-conteggi-e-step-13]] sulle famiglie in disaccordo con `famiglia.py --verifica`: rinominare le 6 versionate come file nuovi e lasciare le 7 aggiornate sul posto. Lo step 13 resta in osservazione fino all'1/11: script e istruzioni dei task non si toccano.

## Decisioni

- `rinomina-nota.py` aggiorna wikilink e campo `note` in `.state/`, ma non il campo `family`: per non toccare gli script durante l'osservazione dello step 13, il `family` si corregge a mano dopo la rinomina.
- Rinominate, con `family` uguale al nuovo slug: `manini-corso-ai-domande-preliminari-blueage` → [[manini-corso-ai-domande-preliminari]], `manini-corso-ai-indice-sistemi-informativi-blueage` → [[manini-corso-ai-indice-sistemi-informativi]], `manini-corso-ai-quadro-interno-blueage` → [[manini-corso-ai-quadro-interno]], `manini-corso-ai-raccolta-dati-blueage` → [[manini-corso-ai-raccolta-dati]], `todo-partner-e-aziende` → [[to-do-partner-e-aziende]], `velo-ce-master-di-codifica-e-anagrafiche` → [[velo-ce-master-di-codifica-e-anagrafiche-interno]] (dall'utente).
- Restano come sono le 7 con la versione a metà nome o aggiornate sul posto: `famiglia.py --verifica` ora dà 7 "diversa" (attese) e 24 "prefisso" (voluti).
- Push sul branch della sessione invece che su `main` (dall'utente).

## File toccati

- Le 6 note rinominate in `sources/attachments/`, `sources/sharepoint/_partner/…/silvia-fumagalli/`, `sources/sharepoint/delivery/customers/01-velo-ce/…/articoli/`
- Wikilink aggiornati in `clients/`, `topics/`, `people/silvia-fumagalli.md`, `projects/corso-ai-manini/corso-ai-manini.md`, `journal/2026-10-23.md`, `journal/2026-10-29.md`, `sources/mail/` e `sources/attachments/`
- `.state/sharepoint.json` (percorso della nota Velo-CE)
- `sessions/2026-10-29-cockpit-conteggi-e-step-13.md` (aperto spuntato)

## Aperti

- [ ] Valutare con lo step 14 se `rinomina-nota.py` debba aggiornare anche il campo `family` delle note `source-doc`
