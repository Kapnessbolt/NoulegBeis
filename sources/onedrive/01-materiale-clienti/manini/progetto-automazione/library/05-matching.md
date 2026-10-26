---
type: source-doc
source: onedrive
family: 05-matching
current:
  item_id: 013UYHJHCUAHFAVGDSGRCIZEBM3GSUGVV4
  uri: file:///b!2fHSoBOOE0aRvS_GntS6s6RJcyNKjAJMiRtoiZ6n5xzp8hWMRRoMQKOVYgftTbzT/013UYHJHCUAHFAVGDSGRCIZEBM3GSUGVV4
  web_url: https://blueagesrl-my.sharepoint.com/personal/lorenzo_curione_blueage_it/Documents/BlueAge/01_Materiale clienti/Manini/Progetto Automazione/Library/05_matching.md
  name: 05_matching.md
  last_modified: 2026-10-25T22:16:49Z
versions:
  - { name: 05_matching.md, item_id: 013UYHJHCUAHFAVGDSGRCIZEBM3GSUGVV4, last_modified: 2026-10-25T22:16:49Z }
  - { name: 05_matching.md, item_id: 013UYHJHCUAHFAVGDSGRCIZEBM3GSUGVV4, last_modified: 2026-10-23T12:50:38Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-26T05:53:02Z
projects: ["[[manini-automazione-ddt]]"]
clients: ["[[manini]]"]
topics: ["[[ai-nei-processi]]"]
tags: [entrata-merci, ddt, matching, as400]
---

# Manini · caso DDT, 05 matching con gli ordini AS400 (simulati)

## Riassunto

Quarto step di [[manini-automazione-ddt]]. In attesa delle righe d'ordine vere di [[manini]], il matching si misura contro un AS400 simulato a partire dalla verità dei 15 DDT, con distrattori realistici. Il motore è deterministico: codice stampato, tabella codici, proposta per somiglianza dentro l'ordine, controlli; due politiche (prudente, automatica con ordine) e due stati della tabella codici (avviamento vuota, regime al 75%), su 30 simulazioni. Il nuovo §9 (25/10/2026) ripete la misura sull'output reale del prompt v1.1 dei due motori ([[04-benchmark]]) e chiude l'ipotesi H29: con la lettura del modello standard nessun DDT cambia stato e nessun abbinamento automatico è errato.

## Punti chiave

- Con il numero d'ordine sul DDT l'abbinamento riga per riga si automatizza senza errori anche a tabella codici vuota: 0 abbinamenti automatici sbagliati su 30 simulazioni
- All'avviamento conta più la politica della tabella: prudente 2 DDT pronti su 15, automatica con ordine 5–7
- Il limite diventa il processo: 4 DDT su 15 con anomalie da vedere comunque e 1 con il solo riferimento a una mail; tetto 10/15 (67%) anche con un matching perfetto
- Sull'estrazione reale (§9): i numeri del business case reggono con il modello standard; le righe automatiche calano per un difetto del motore nella ricerca del fornitore per ragione sociale con forme societarie puntate e filiali (H33), non per la lettura
- Con il veloce lo 0 è in parte fortuna: corretta la ricerca del fornitore compare 1 abbinamento errato (004663 riga 5), perché un codice stampato senza ordine viene accettato anche se presente in più ordini aperti (H34)
- Gli errori di lettura che arrivano a un DDT pronto sono valori sbagliati, non abbinamenti sbagliati, e sono tutti in `campi_incerti`: serve la regola di flusso "campo critico incerto → verifica rapida" (H30)
- Le proposte corrette al 100% sono ottimistiche: descrizioni dell'AS400 simulato derivate dai DDT (H22), proposta deterministica al posto dell'AI (H23); il §9 usa un solo AS400 simulato (H35)

## Numeri

- Righe abbinate in automatico sulla verità: 60% (avviamento, prudente), 81–86% (avviamento, automatica), 86–93% (regime, automatica)
- Sull'estrazione v1.1, seed 42, regime e politica automatica: 7/15 DDT pronti e 75/88 righe automatiche (85%) con entrambi i motori, contro 82/88 sulla verità
- Veloce all'avviamento con politica automatica: 4/15 DDT pronti invece di 5/15 (7,7 minuti per DDT invece di 7,2)
- Righe non abbinate per il difetto H33: 9 su 88 con lo standard
- Regola "campo incerto → verifica": 2 dei 7 DDT pronti con lo standard, 4 dei 7 con il veloce
- Business case sul campione: risparmio circa 630–740 ore (22–26 k€) contro 949 ore (33 k€) del prudente del deck; invariato con il modello standard

## Decisioni e azioni

- Nel pilota, politica automatica solo sulle righe con ordine e proposta netta; tutto il resto in eccezione; obiettivo 0 abbinamenti automatici errati
- I numeri del §1 valgono anche sull'estrazione reale con il modello standard: il business case non cambia
- [ ] Correggere il motore prima del pilota: ricerca del fornitore tollerante a punti e filiali (H33); codice stampato senza ordine in più ordini aperti → E07 (H34)
- [ ] Separare in `robustezza.py` la verità dall'estrazione e ripetere il §9 su 30 seed (H35)
- [ ] Ripetere la misura con le righe d'ordine vere dei 14 fornitori, appena Manini le manda
- [ ] Chiedere agli acquisti di Manini se gli inerti hanno un solo contratto quadro aperto per fornitore (H25) e se una riga a saldo può non bloccare la registrazione (H26)
- [ ] Proporre a Manini di chiedere ai fornitori il numero d'ordine sul DDT

## Versioni

- 05_matching.md · 2026-10-25 · aggiunto il §9, matching sull'output del prompt v1.1: H29 chiusa, nuovi difetti del motore H33 e H34, limite H35
- 05_matching.md · 2026-10-23 · prima versione
