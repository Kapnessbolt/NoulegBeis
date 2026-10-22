---
type: session
date: 2026-10-22
surface: cloud
topics: ["[[blueage]]", "[[pulse]]"]
outcome: "Step 3, lotti 3 e 4: Shared Documents vuota, OneDrive/BlueAge 2 note, 7 note fuori perimetro dal sito partner"
---

# Primo caricamento · lotti 3 Shared Documents e 4 OneDrive

## Obiettivo

Ingerire la libreria Shared Documents di `sites/internal` (lotto 3) e la cartella OneDrive `BlueAge/` (lotto 4), SPEC 6.5.

## Decisioni

- Shared Documents è vuota: contiene solo la cartella `General` del canale Teams, senza file. Resta nel perimetro (scelta dell'utente).
- Sito `sites/partner`, fuori perimetro: ingerite con il compito `file` e il tag `fuori-perimetro` solo le famiglie che il vault non aveva (7 note in `sources/sharepoint/_partner/`). Le copie del materiale già presente restano fuori e non vanno nello stato.
- OneDrive: vale solo `BlueAge/` (decisione dell'utente). Contiene `00_chat/` (vuota, prima `_chat/`) e `01_Materiale clienti/`, la cartella con il materiale inviato dai clienti. Da `01_Materiale clienti/Manini/` sono entrate 2 note; `Documenti di Trasporto.zip` è ignorato perché è un tipo non processato.
- `Formazione AI/` nella radice di OneDrive resta fuori: è il cantiere da cui è nato il deck, ora superato da `M1_v15` di Leonardo ([[ai-foundation-program-m1]]). Secondo l'utente i corsi MTU e Manini sono uguali.
- Il progetto MTU non è stato creato; la proposta in `inbox/` è aggiornata.
- Temi nuovi non creati. Le proposte degli agenti sono elencate negli aperti.

## File toccati

- `sources/sharepoint/_partner/partner/condivisi/`: blueage-onepage, blueage-sintesi, blueage-possibilita, blueage-condizioni-commerciali-slide, pulse-faq-vendita
- `sources/sharepoint/_partner/partner/silvia-fumagalli/`: pulse-i-en, todo-partner-e-aziende
- `sources/onedrive/01-materiale-clienti/manini/`: gruppi, istruzioni-e-informativa-ia
- `projects/corso-ai-manini/` (stato, calendario come attività, log), `clients/manini.md`, `people/michele-padoin.md`
- `topics/`: pulse, blueage (punti chiave), le altre solo `## Fonti`
- `inbox/2026-10-22-proposta-progetto-mtu-ai-foundation.md`
- `.state/ingest.json`: 2 item OneDrive, watermark ancora null

## Aperti

- [ ] La SPEC (5.2, 8), CLAUDE.md e l'ingestor citano `BlueAge/_chat/`, ma la cartella ora si chiama `00_chat/`: serve una PR di allineamento
- [ ] Il `BlueAge_CompanyProfile.pdf` del sito partner è del 2026-10-19 e ha un incipit diverso dalla v24 del 2026-10-01 su SalesMarketing: potrebbe essere una versione più nuova non ancora caricata su SalesMarketing
- [ ] `pulse-i-en` va allineata alla K: EBITDA del caso reale 2,8 M€ contro 2,35 M€
- [ ] Proposte degli agenti: cliente Bertazzoni (prospect Pulse, incontro del 2026-07-30); note cliente per i prospect già incontrati (MC Bride, Loacker, Gotha, Fresenius Kabi, Eurochef, B. Braun); temi Parts Radar, manager operativo / fractional, Cellularline (caso storico di Pulse), TwoTeam (partner per le implementazioni enterprise)
- [ ] Fuori perimetro su OneDrive: `Attachments/Ipotesi Formazione IT.docx`, forse il programma del gruppo IT Manini
- [ ] Prossimo lotto: Outlook, ultimi 60 giorni
