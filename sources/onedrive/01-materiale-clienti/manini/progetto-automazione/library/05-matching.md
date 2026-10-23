---
type: source-doc
source: onedrive
family: 05-matching
current:
  item_id: 013UYHJHCUAHFAVGDSGRCIZEBM3GSUGVV4
  uri: file:///b!2fHSoBOOE0aRvS_GntS6s6RJcyNKjAJMiRtoiZ6n5xzp8hWMRRoMQKOVYgftTbzT/013UYHJHCUAHFAVGDSGRCIZEBM3GSUGVV4
  web_url: https://blueagesrl-my.sharepoint.com/personal/lorenzo_curione_blueage_it/Documents/BlueAge/01_Materiale clienti/Manini/Progetto Automazione/Library/05_matching.md
  name: 05_matching.md
  last_modified: 2026-10-23T12:50:38Z
versions:
  - { name: 05_matching.md, item_id: 013UYHJHCUAHFAVGDSGRCIZEBM3GSUGVV4, last_modified: 2026-10-23T12:50:38Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-23T12:52:00Z
projects: ["[[manini-automazione-ddt]]"]
clients: ["[[manini]]"]
topics: ["[[ai-nei-processi]]"]
tags: [entrata-merci, ddt, matching, as400]
---

# Manini · caso DDT, 05 matching con gli ordini AS400 (simulati)

## Riassunto

Quarto step di [[manini-automazione-ddt]] (23/10/2026). In attesa delle righe d'ordine vere di [[manini]], il matching si misura contro un AS400 simulato a partire dalla verità dei 15 DDT, con distrattori realistici: articoli simili, merce già evasa, ordini vecchi, contratti quadro. Il motore è deterministico: codice stampato, poi tabella codici, poi proposta per somiglianza dentro l'ordine, poi i controlli. Si confrontano due politiche (prudente, automatica con ordine) e due stati della tabella codici (avviamento vuota, regime al 75%), su 30 simulazioni. Codice e dati simulati stanno nel repo del progetto e su OneDrive; i dati reali non escono da OneDrive.

## Punti chiave

- Con il numero d'ordine sul DDT l'abbinamento riga per riga si automatizza senza errori anche a tabella codici vuota: 0 abbinamenti automatici sbagliati su 30 simulazioni, in tutti gli scenari
- All'avviamento conta più la politica della tabella: prudente 2 DDT pronti su 15, automatica con ordine 5–7
- Il limite diventa il processo: 4 DDT su 15 hanno anomalie da vedere comunque (illeggibile, pagina mancante, peso diverso dalla pesata, riserva a mano) e 1 cita solo una mail; tetto 10/15 (67%) anche con un matching perfetto
- Inerti senza ordine: una regola deterministica sul contratto quadro unico li rende pronti senza AI; i DDT con il solo riferimento a una mail richiedono un intervento organizzativo sui fornitori
- Le proposte corrette al 100% sono ottimistiche: le descrizioni dell'AS400 simulato derivano da quelle dei DDT (H22); la proposta è uno stand-in deterministico dell'AI (H23)
- Il motore è il riferimento per il flusso Power Automate del pilota; con il CSV vero degli ordini la misura si ripete senza cambiare codice
- Ipotesi H22–H29 dichiarate, tra cui la tabella a regime al 75%, E12 come avviso, due casi costruiti, minuti del deck invariati

## Numeri

- Righe abbinate in automatico: 60% (avviamento, prudente), 81–86% (avviamento, automatica), 86–93% (regime, automatica)
- DDT pronti su 15: 2 / 5–7 / 6–7; tetto con matching perfetto 10/15
- Business case sul campione: circa 1.120–1.230 ore/anno contro 1.860 di oggi; risparmio circa 630–740 ore (22–26 k€) contro 949 ore (33 k€) del prudente del deck
- Minuti per DDT: 8,9 (prudente all'avviamento), 6,6, 6,0 (regime, automatica)

## Decisioni e azioni

- Nel pilota, politica automatica solo sulle righe con ordine e proposta netta; tutto il resto in eccezione; obiettivo 0 abbinamenti automatici errati
- [ ] Ripetere la misura con le righe d'ordine vere dei 14 fornitori, appena Manini le manda
- [ ] Chiedere agli acquisti di Manini se gli inerti hanno un solo contratto quadro aperto per fornitore (H25) e se una riga a saldo può non bloccare la registrazione (H26)
- [ ] Proporre a Manini di chiedere ai fornitori il numero d'ordine sul DDT

## Versioni

- 05_matching.md · 2026-10-23 · prima versione
