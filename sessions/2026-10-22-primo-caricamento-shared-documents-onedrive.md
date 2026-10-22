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
- Progetto [[corso-ai-mtu]] creato su richiesta dell'utente, sul modello di [[corso-ai-manini]]: stesso corso e stesso ruolo (AI consultant in aula con Leonardo). Proposta in `inbox/` chiusa e rimossa.
- Temi nuovi non creati. Le proposte degli agenti sono elencate negli aperti.

## File toccati

- `sources/sharepoint/_partner/partner/condivisi/`: blueage-onepage, blueage-sintesi, blueage-possibilita, blueage-condizioni-commerciali-slide, pulse-faq-vendita
- `sources/sharepoint/_partner/partner/silvia-fumagalli/`: pulse-i-en, todo-partner-e-aziende
- `sources/onedrive/01-materiale-clienti/manini/`: gruppi, istruzioni-e-informativa-ia
- `projects/corso-ai-manini/` (stato, calendario come attività, log), `clients/manini.md`, `people/michele-padoin.md`
- `topics/`: pulse, blueage (punti chiave), le altre solo `## Fonti`
- `inbox/2026-10-22-proposta-progetto-mtu-ai-foundation.md`
- `.state/ingest.json`: 2 item OneDrive, watermark ancora null
- Dopo il campione: `sources/sharepoint/salesmarketing/deck/blueage-companyprofile.md` (nuova versione), 8 note in `clients/`, 3 in `topics/`, collegamenti aggiunti in 11 fonti

## Aperti

- [ ] SPEC (5.2, 8, 13) e CLAUDE.md citano `BlueAge/_chat/`, ma la cartella ora si chiama `00_chat/`. L'utente ha approvato la PR (SPEC 1.9, con anche `01_Materiale clienti/`), ma il commit è stato bloccato dal permesso sulle modifiche alle istruzioni: le modifiche sono pronte nello stash del branch `claude/trusting-carson-ipguvp`
- [x] Company Profile: l'utente conferma che la copia del sito partner (2026-10-19) è la versione più nuova; ora è la `current` di [[blueage-companyprofile]], con la v24 nello storico
- [x] `pulse-i-en` va allineata alla K (EBITDA del caso reale 2,8 M€ contro 2,35 M€): l'utente ne ha preso atto
- [x] Proposte approvate dall'utente e create: clienti [[bertazzoni]], [[mc-bride]], [[loacker]], [[gotha]], [[fresenius-kabi]], [[eurochef]], [[b-braun]] (prospect) e [[cellularline]] (caso storico di Pulse, `da-verificare`); temi [[parts-radar]], [[manager-operativo]], [[twoteam]] (`da-verificare`: è un partner, non un tema in senso stretto)
- [x] `Attachments/Ipotesi Formazione IT.docx` nella radice di OneDrive resta fuori (decisione dell'utente)
- [ ] Prossimo lotto: Outlook, ultimi 60 giorni
