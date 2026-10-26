---
type: session
date: 2026-10-26
surface: cloud
topics: ["[[second-brain]]"]
outcome: "Due one pager del Second Brain in stile BlueAge: commerciale A4 in PDF e tecnico navigabile pubblicato come artifact su claude.ai; il PDF va caricato a mano su OneDrive"
---

# One pager del Second Brain, commerciale e tecnico

## Obiettivo

Realizzare due one pager in stile BlueAge del Second Brain: uno commerciale per presentare il prodotto, uno tecnico e visuale per spiegare al team architettura, strumenti e struttura del repo.

## Decisioni

- Commerciale in HTML A4 esportato in PDF; tecnico come pagina web navigabile, non A4, perché deve far capire ogni pezzo con un clic (dall'utente)
- Il commerciale vende il pacchetto Second Brain generico, non questo vault; niente prezzi né pacchetti, perché nel vault sono ancora ipotesi discordanti (dall'utente)
- Storia del commerciale: problema → soluzione e come funziona in 4 passi; esclusi il box "lo usiamo noi" e la sezione sicurezza (dall'utente)
- Nel commerciale niente nomi di tecnologie interne (Claude Code, GitHub, routine): il manager compra il risultato
- Contatto del commerciale: Silvia Fumagalli, con la mail aziendale (dall'utente)
- "Risposte con la fonte citata" resta tra i benefici anche se l'agente `librarian` non c'è ancora: le note citano già la fonte (dall'utente)
- Tecnico per il team interno, con i nomi reali di file, agenti, comandi e routine; ciò che la SPEC prevede ma non esiste è marcato "in arrivo" (dall'utente)
- Tecnico in 4 viste: architettura con pannello di dettaglio per nodo, strumenti filtrabili (35, 8 in arrivo), struttura del repo con le note contate (307), giornata tipo con gli orari reali dei task
- I due file costruiti in parallelo da due subagenti nella stessa sessione, non da due sessioni, per controllarli e pubblicarli da qui
- PDF rigenerato con i file statici di Plus Jakarta Sans: con il font variabile Chromium lo incorporava come Type 3 (200 KB → 85 KB)
- File prodotti fuori dal repo (`CLAUDE.md` §5): tecnico su claude.ai, commerciale in OneDrive `BlueAge/02_Second Brain/`
- Nel tecnico `blueage-deck`, `blueage-corso` e `blueage-animazioni` passano da "in arrivo" a "dall'account": non sono in `.claude/skills/`, ma arrivano dal plugin di claude.ai e si usano già nelle sessioni (segnalato dall'utente; artifact versione 2)

## File toccati

- `topics/`: `second-brain.md` (materiali di presentazione in `## Dove è usato`)
- `sessions/`: questo diario
- Fuori dal repo: artifact https://claude.ai/artifact/FeqbkutspXZcAds7v8iZcL (privato); PDF commerciale in OneDrive `BlueAge/02_Second Brain/`, caricato a mano da Lorenzo

## Aperti

- [x] Caricare a mano il PDF del one pager commerciale su OneDrive: il caricamento dal connettore è stato bloccato, il base64 del PDF non passa nella chiamata (chiuso: caricato da Lorenzo in `BlueAge/02_Second Brain/`)
- [ ] Condividere l'artifact del one pager tecnico con il team dal menu Share
- [x] Allineare SPEC e README alle 9 incongruenze trovate costruendo il one pager tecnico (skill blueage non nel vault, README con comandi inesistenti, branch del curator, prefissi di commit, `.githooks/` nell'albero, ingestor e 6.6, `/cockpit`, Obsidian in sola lettura, `.gitkeep`): c'è la scheda "Allinea SPEC e README ai file reali" (chiuso in [[2026-10-26-spec-e-readme-allineati]])
- [ ] Spunto per il curator: dal cloud i file binari prodotti dalle skill (PDF, pptx) non si caricano su OneDrive oltre pochi KB; serve una procedura per consegnarli
