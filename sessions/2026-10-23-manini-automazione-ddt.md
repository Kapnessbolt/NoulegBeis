---
type: session
date: 2026-10-23
surface: cloud
topics: ["[[ai-nei-processi]]"]
outcome: "Progetto manini-automazione-ddt creato nel vault; repo tecnico preparato (da pubblicare); dati sensibili isolati su OneDrive"
---

# Manini automazione DDT: dal Project claude.ai al vault e a un repo dedicato

## Obiettivo

Portare nella knowledge base il caso entrata merci da DDT di [[manini]], sviluppato in un Project claude.ai (sessioni del 21 e 22/10), e poterci lavorare a 360° da Claude Code.

## Decisioni

- Il caso DDT diventa un progetto a sé, [[manini-automazione-ddt]], collegato a [[corso-ai-manini]] e a [[manini-supply-chain-magazzino]]: ha step, attività e decisioni propri e va oltre il corso
- Lavoro tecnico in un repo GitHub privato separato, `manini-automazione-ddt` (report, schema, prompt, script), non dentro NoulegBeis: il vault resta una knowledge base, il repo è il cantiere. Scartati il tutto-nel-vault e il submodule
- Dati reali (ZIP dei DDT, `verita_ddt.json`, `inventario.json`) solo su OneDrive in `Progetto Automazione/Dati/`, mai su GitHub: la policy AI di Manini ammette dati reali solo nel tenant Manini o anonimizzati. Le sessioni li leggono con il connettore e li tengono in `data/`, ignorata da git
- Master di report e kit: il repo. OneDrive `Library/` tiene le copie condivise, da cui l'ingestion crea le note fonte
- Eliminati su OneDrive (dall'utente): il doppione dell'essenziale in `Work_brain/` ed `esempi_ddt.json`, superato da `verita_ddt.json`
- Nell'essenziale corretti due sdoppiamenti di persona: Angelo e "Santilli" sono [[angelo-santilli]]; Cristian e "Trif" sono [[cristian-schifone]]
- Step 4 fatto in simulazione nel repo (`matching/`, report 05): AS400 simulato con distrattori, motore deterministico, due politiche e due stati della tabella codici, 30 simulazioni. I dati reali e simulati restano in `data/`, ignorata da git ([[05-matching]])
- Vault portato su `main`; `Gruppi.xlsx` e `Istruzioni e Informativa IA.pdf` riportati in `Manini/` su OneDrive, `Documenti/` vuota eliminata
- I report del repo possono citare fornitori, numeri DDT e ordini del campione: niente anonimizzazione, il repo è privato; restano fuori solo i dati riga per riga
- Richieste a Manini (ordini veri, contratti quadro, numero d'ordine sui DDT): rimandate, per ora nessuna mail
- Le lezioni operative su come lavorare con Claude (ZIP grandi, sandbox non persistente, subagenti) restano qui come spunto per il curator, non nella KB di progetto

## File toccati

- `projects/manini-automazione-ddt/` (scheda e log, nuovi)
- `sources/onedrive/01-materiale-clienti/manini/manini-ddt-essenziale.md` e `progetto-automazione/` (7 note fonte nuove)
- `projects/corso-ai-manini/` (rimando al progetto, audience dei gruppi B e C, caso preventivi), `projects/manini-supply-chain-magazzino/manini-supply-chain-magazzino.md`
- `clients/manini.md`, `topics/ai-nei-processi.md`, `people/angelo-santilli.md`, `people/luca-zamponi.md`, `people/leonardo-pinsone.md`, `people/cristian-schifone.md`
- `.state/ingest.json` (8 voci OneDrive, watermark invariato)
- `sources/onedrive/01-materiale-clienti/manini/progetto-automazione/library/05-matching.md` (nuova)
- OneDrive: cartella `Progetto Automazione/Dati/` creata con ZIP, verità e inventario; `manini_ddt_essenziale.md` aggiornato con le correzioni
- Repo `manini-automazione-ddt` preparato in locale con `CLAUDE.md`, `README.md`, `.gitignore`, `report/` e `kit/`: da pubblicare quando il repo esiste su GitHub

## Aperti

- [x] Creare su GitHub il repo privato `Kapnessbolt/manini-automazione-ddt` e pubblicare il contenuto preparato
- [x] Estrarre su OneDrive i PDF dallo ZIP dei DDT, in `Dati/` (fatto dall'utente; lo ZIP non c'è più)
- [x] `Gruppi.xlsx` e `Istruzioni e Informativa IA.pdf` riportati in `Manini/`: le note [[gruppi]] e [[istruzioni-e-informativa-ia]] restano valide
- [x] Report 01, 04 e 05 con tabelle per documento: non si anonimizzano (decisione dell'utente)
- [ ] Spunto per il curator: una regola su come portare un Project claude.ai nel vault (repo dedicato, dati su OneDrive, essenziale come nota hub)
