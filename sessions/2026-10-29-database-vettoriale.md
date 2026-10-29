---
type: session
date: 2026-10-29
surface: cloud
topics: ["[[second-brain]]"]
outcome: "Valutato il database vettoriale per il prodotto Second Brain: oggi non serve; ricerca lessicale potenziata subito, ricerca ibrida locale solo al primo trigger misurato; decisione in scheda, tema e SPEC 1.25 §14, in PR"
---

# Database vettoriale per il Second Brain

## Obiettivo

Capire se, quando e come il Second Brain commerciale richiede un database vettoriale per la ricerca semantica, e quale soluzione conviene per costo, comodità, adoption e posizionamento.

## Decisioni

- Oggi niente database vettoriale: il vault è già uno strato curato (riassunti, frontmatter, wikilink, note hub) e il librarian fa ricerca agentica con `cerca.py`, i collegamenti e la riformulazione dei termini; con 424 note (circa 300k token) la scansione costa millisecondi, il limite possibile è la recall, non la velocità (proposta della sessione, confermata dall'utente)
- Sugli originali (SharePoint, OneDrive, Outlook) l'indice semantico c'è già: il connettore usa Microsoft Search e, per chi ha Copilot, il semantic index. Un RAG nostro sugli originali rifarebbe Copilot e violerebbe "la nota descrive, non copia": escluso
- Approccio scelto (dall'utente): ricerca lessicale potenziata adesso (BM25 in `cerca.py` al posto dei pesi fissi 10/3/1, `aliases:` nelle note hub), ricerca ibrida locale solo al primo trigger misurato: indice vettoriale come file derivato (sqlite-vec o LanceDB) dietro `cerca.py`, ricostruibile dalle note, embedding con un modello locale multilingue se la rete dell'ambiente lo permette (nessun nuovo responsabile del trattamento), altrimenti via API (Voyage) con accordo sul trattamento dei dati. Agenti e comandi non cambiano
- Trigger della ricerca ibrida: recall sotto il 90% (note attese nei primi 5 risultati) sul set di prova per colpa del vocabolario; oltre circa 5.000 note o più di 4–5 giri di ricerca in media per risposta; primo cliente a più persone (più vault); note in lingue miste. Con 10–50 note al giorno un utente intenso arriva a 5.000 note in 6–12 mesi
- Esclusi: database vettoriale gestito (Pinecone, Qdrant Cloud, pgvector) perché aggiunge server, account, costo mensile e accordo sui dati per cliente e rompe il principio delle primitive stabili; ha senso solo se BlueAge diventa piattaforma che ospita più clienti o vault di team, che è un altro prodotto
- Variante commerciale per i clienti con licenze Copilot: copia del vault su SharePoint indicizzata da Copilot, senza infrastruttura nostra
- Posizionamento: non si vende "il RAG vettoriale" (commodity, terreno di Copilot) ma lo strato curato e tracciato alla fonte con la gestione mensile; al cliente tecnico si risponde che la ricerca è predisposta per diventare ibrida e si attiva quando il volume lo giustifica
- Predisposizione senza rimpianti: set di valutazione (circa 50 domande con le note attese e script di recall), registro dei "non trovato" e dei giri di ricerca del librarian nelle metriche dello step 20, `cerca.py` unico punto di ingresso; la struttura delle note (brevi, a sezioni, slug unici) è già adatta agli embedding e va mantenuta

## File toccati

- `sessions/`: questo diario
- `projects/second-brain-prodotto/`: scheda (decisione, tre attività, fonti) e log
- `topics/second-brain.md`: punto chiave sul posizionamento della ricerca
- `SPEC.md`: 1.25, §14 decisione aperta sulla ricerca vettoriale con i trigger; sul branch della sessione, entra in `main` con una PR

## Aperti

- [ ] Unire la PR di questa sessione (SPEC 1.25, scheda, tema)
- [ ] Set di valutazione della ricerca: circa 50 domande con le note attese e script che calcola la recall dei primi 5 risultati
- [ ] Registro dei "non trovato" e dei giri di ricerca del librarian, nelle metriche dello step 20
- [ ] BM25 in `cerca.py` e `aliases:` nei template di cliente, tema e progetto
