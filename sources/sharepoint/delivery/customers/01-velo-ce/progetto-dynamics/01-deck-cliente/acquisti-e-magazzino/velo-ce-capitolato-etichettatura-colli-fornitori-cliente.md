---
type: source-doc
source: sharepoint
family: velo-ce-capitolato-etichettatura-colli-fornitori-cliente
current:
  item_id: 01EFCYUZ7VCU77DBWVP5EYJUTLKDJNNXH3
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ7VCU77DBWVP5EYJUTLKDJNNXH3
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/01 Deck cliente/Acquisti e magazzino/Velo-CE - Capitolato etichettatura colli fornitori - CLIENTE - v001.pdf
  name: Velo-CE - Capitolato etichettatura colli fornitori - CLIENTE - v001.pdf
  last_modified: 2026-10-29T16:14:44Z
versions:
  - { name: Velo-CE - Capitolato etichettatura colli fornitori - CLIENTE - v001.pdf, item_id: 01EFCYUZ7VCU77DBWVP5EYJUTLKDJNNXH3, last_modified: 2026-10-29T16:14:44Z }
  - { name: Velo-CE - Capitolato etichettatura colli fornitori - CLIENTE - v001.pdf, item_id: 01EFCYUZZF5CB5SYZCHFGIEI2DXEPM5NFN, last_modified: 2026-10-28T08:06:30Z }
  - { name: Velo-CE - Capitolato etichettatura colli fornitori - CLIENTE - v001.pdf, item_id: 01EFCYUZ2X7PJ62VGYRZGLVIGKKY4PV47U, last_modified: 2026-10-08T10:44:29Z }
  - { name: Velo-CE - Capitolato etichettatura colli fornitori - CLIENTE - v001.docx, item_id: 01EFCYUZ5GMGQ6OKAZ2BFYP5X3JROZJR2H, last_modified: 2026-10-07T10:06:16Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:25:42Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [capitolato, fornitori, etichette, codice-a-barre, ricevimento-merci, magazzino]
---

# Velo-CE · Capitolato di etichettatura dei colli dei fornitori

## Riassunto

Bozza v001 del 07/10/2026 dei requisiti che Velo-CE chiederà ai fornitori per etichettare i colli e compilare il DDT, così che al ricevimento ogni collo sia riconosciuto con la lettura di un codice a barre (articolo, quantità, ordine). Definisce regole generali, campi dell'etichetta per livello, specifiche dei codici a barre (Code 128), contenuto del DDT, cosa fornisce Velo-CE, tre livelli di richiesta ai fornitori, la procedura di avvio con etichetta di prova e la gestione delle non conformità. In apertura una nota per Velo-CE elenca cosa va deciso prima dell'invio; in allegato un esempio di etichetta A5 in inglese.

## Punti chiave

- **Prima dell'invio** (nota da togliere): codici articolo definitivi, perché ogni cambio dopo l'invio obbliga i fornitori a rifare le etichette; versione inglese per i fornitori esteri; elenco dei fornitori con il livello e data di entrata in vigore; verifica che la stampa dell'ordine d'acquisto riporti i dati richiesti.
- **Regole**: un'etichetta per collo (quella di pallet non la sostituisce), un solo codice Velo-CE per collo salvo accordi, posizione su lato verticale visibile, fasci di tubi con etichetta a bandiera, stampa termica o laser nero su bianco, niente dati a mano nei campi con codice a barre.
- **Campi**: 11 campi, obbligatori o consigliati secondo il livello; codice Velo-CE e numero d'ordine anche come codice a barre; lotto, colata o certificato solo se l'ordine lo chiede.
- **Codici a barre**: Code 128 con il solo dato scritto come sull'ordine, GS1-128 non accettato, un codice per dato con testo leggibile, lettura al primo passaggio con lettore portatile; il fornitore può aggiungere i propri codici (EAN) in zona distinta.
- **Livelli**: A base (tutti i fornitori, solo DDT con numero d'ordine, codici Velo-CE e fornitore, quantità e numero colli); B codice a barre (fornitori ricorrenti, oppure il fornitore tiene il proprio codice comunicando la corrispondenza); C etichetta completa (fornitori strutturati e articoli ad alta rotazione).
- **Avvio**: invio del capitolato con livello ed elenco codici, etichetta di prova in PDF e primo collo etichettato, prova di lettura e conferma scritta di Velo-CE.

## Numeri

- Formato etichetta A5 (148 × 210 mm) orizzontale, A6 (105 × 148 mm) per colli piccoli.
- Valori proposti dei codici a barre: barra più sottile almeno 0,33 mm, altezza almeno 15 mm, zona libera almeno 10 volte la barra più sottile e comunque 5 mm.
- Esempi di formato: codice articolo TUB00012, ordine d'acquisto AOR27-0012.

## Decisioni e azioni

- [ ] Stabilizzare la regola di codifica e i codici definitivi prima dell'invio ai fornitori
- [ ] Preparare la versione inglese del capitolato
- [ ] Compilare l'elenco dei fornitori con il livello richiesto e la data di entrata in vigore
- [ ] Verificare che la stampa dell'ordine d'acquisto riporti codice Velo-CE, descrizione, codice del fornitore, quantità e unità di misura
- [ ] Decidere la regola sulle non conformità (rietichettatura con addebito, accettazione con riserva o respingimento)
- [ ] Definire per articolo quando servono lotto, colata o certificato
- [ ] Confermare i valori dei codici a barre dopo la prova di lettura

## Versioni

- Velo-CE - Capitolato etichettatura colli fornitori - CLIENTE - v001.pdf · 2026-10-08 · prima versione ingerita (bozza v001 del 07/10/2026); data di modifica dovuta alla riorganizzazione della cartella
- Velo-CE - Capitolato etichettatura colli fornitori - CLIENTE - v001.docx · 2026-10-07 · sorgente modificabile dello stesso documento
