---
type: project
status: attivo
role: "AI consultant: analisi, architettura e kit tecnico del caso entrata merci"
clients: ["[[manini]]"]
people: ["[[leonardo-pinsone]]", "[[luca-zamponi]]", "[[angelo-santilli]]", "[[cristian-schifone]]"]
updated: 2026-10-23
---

# Manini · automazione entrata merci da DDT

## Stato

- Caso studio sull'entrata merci di [[manini]]: leggere i DDT dei fornitori con un modello generativo, abbinarli agli ordini AS400 e lasciare alle persone solo le eccezioni. È l'intervento 4A della relazione sui materiali ed è il caso pratico del [[corso-ai-manini]] (laboratorio utenti e 8 ore con i Sistemi Informativi) ([[00-istruzioni-progetto]], [[manini-relazione-processi-gestione-materiali]])
- Lavoro tecnico nel repo GitHub privato `manini-automazione-ddt` (report, schema, prompt, script); i dati reali (DDT, verità, inventario) restano su OneDrive in `Progetto Automazione/Dati/` e non entrano mai nel repo. Le copie condivise dei report sono in `Progetto Automazione/Library/` ([[2026-10-23-manini-automazione-ddt]])
- Step 1, inventario: fatto. 15 DDT reali di 14 fornitori, nessun PDF nativo, ordine Manini presente in 10 su 15, codice Manini esplicito in 2 su 15 ([[01-inventario]])
- Step 2, schema JSON: fatto. Schema canonico più versione piatta per AI Builder e Copilot Studio, 13 codici di eccezione ([[03-schema-ddt]])
- Step 3, benchmark: fatto. Campi critici corretti al 100% con il modello generativo standard, all'88% con quello veloce, al 27% con l'OCR classico; il prompt v1.1 è da ritestare ([[04-benchmark]], [[prompt-estrazione-ddt]])
- Step 4, matching contro ordini simulati: da fare ([[manini-ddt-essenziale]])
- Step 5, output riusabili: parziale. Piano aula, sessione IT e architettura Microsoft definiti; deck da aggiornare ([[02-aula-e-architettura]])
- Business case del deck v3 di [[leonardo-pinsone]]: 1.860 ore/anno oggi, risparmio 33–47 k€/anno; poggia su due numeri non misurati, i 10 minuti a DDT e la quota del 60/80% di DDT senza eccezioni ([[manini-ddt-essenziale]], [[automazione-entrata-merci-caso-manini]])

## Attività

- [ ] Step 4: CSV ordini simulato con distrattori (residui, righe evase, UM diverse) e due scenari di tabella codici (avviamento vuota, regime 70–80%) ([[manini-ddt-essenziale]])
- [ ] Ritestare il prompt v1.1 sui 15 DDT ([[04-benchmark]])
- [ ] Revisione umana di 3–4 DDT difficili per verificare la verità del benchmark (H17) ([[04-benchmark]])
- [ ] Prova delle demo con la licenza Copilot di Angelo Santilli 📅 2026-11-05 ([[02-aula-e-architettura]])
- [ ] Preparare file ordini simulato e bozza della tabella codici per le demo in aula ([[02-aula-e-architettura]])
- [ ] Chiedere a Manini: significato del "Mov." sull'etichetta (H1), volumi e registrazione dei DDT della pesa di Bastia (H7), web service o programmi di import su AS400, gateway dati locale ([[02-aula-e-architettura]])
- [ ] Chiedere a Manini i dati: estratto AS400 dei movimenti del campione, righe d'ordine aperte dei 14 fornitori, campione di 80–100 DDT di un mese, materiale del test Sanmarco, misura dei minuti per DDT ([[01-inventario]], [[manini-ddt-essenziale]])
- [ ] Ambiente Power Platform di sviluppo con Copilot Credits nel tenant Manini per l'aula ([[02-aula-e-architettura]])
- [ ] Aggiornare il deck entrata merci: Copilot Credits al posto dei crediti AI Builder, staging al posto della scrittura DB2, ingresso da scansione invece che da casella mail ([[02-aula-e-architettura]])
- [ ] Estrarre su OneDrive i PDF dallo ZIP dei DDT, così le sessioni Claude Code li leggono con il connettore ([[2026-10-23-manini-automazione-ddt]])

## Decisioni

- Il collo di bottiglia è l'abbinamento con ordini e codici, non la lettura; l'abbinamento fatture già fatto dall'AS400 non si tocca ([[manini-ddt-essenziale]])
- Lettura generativa con schema JSON e regola "trascrivi, non dedurre": prompt AI Builder per il pilota, nodo Extract di Copilot Studio da mostrare, niente modello addestrato per layout ([[02-aula-e-architettura]], [[04-benchmark]])
- In AI Builder e Copilot Studio si sceglie il modello più capace, non quello veloce ([[04-benchmark]])
- Abbinamento deterministico dove si può, AI solo dove serve giudizio; la proposta dell'AI confermata da una persona popola la tabella codici ([[02-aula-e-architettura]])
- Scrittura su AS400 con staging su DB2 più programma RPG di import; niente INSERT diretto, RPA sul 5250 solo come ponte ([[02-aula-e-architettura]])
- Pilota in tre fasi: dati, in ombra solo su Aprilia, scrittura in staging ([[02-aula-e-architettura]])
- Benchmark per campo e per tipo di acquisizione, non per fornitore ([[01-inventario]])
- Repo GitHub dedicato per il lavoro tecnico; dati reali solo su OneDrive; vault per stato, decisioni e attività ([[2026-10-23-manini-automazione-ddt]])

## Prossimi passi

- Sessione Claude Code con i due repo (`manini-automazione-ddt` e NoulegBeis) per lo step 4

## Fonti

- [[manini-ddt-essenziale]]
- [[00-istruzioni-progetto]]
- [[01-inventario]]
- [[02-aula-e-architettura]]
- [[03-schema-ddt]]
- [[04-benchmark]]
- [[prompt-estrazione-ddt]]
- [[automazione-entrata-merci-caso-manini]]
- [[blueage-automation-entrata-merci]]
- [[manini-relazione-processi-gestione-materiali]]
- [[2026-10-23-manini-automazione-ddt]]
