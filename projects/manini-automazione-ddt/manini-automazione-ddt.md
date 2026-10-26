---
type: project
status: attivo
role: "AI consultant: analisi, architettura e kit tecnico del caso entrata merci"
clients: ["[[manini]]"]
people: ["[[leonardo-pinsone]]", "[[luca-zamponi]]", "[[angelo-santilli]]", "[[cristian-schifone]]"]
updated: 2026-10-26
---

# Manini · automazione entrata merci da DDT

## Stato

- Caso studio sull'entrata merci di [[manini]]: leggere i DDT dei fornitori con un modello generativo, abbinarli agli ordini AS400 e lasciare alle persone solo le eccezioni. È l'intervento 4A della relazione sui materiali ed è il caso pratico del [[corso-ai-manini]] (laboratorio utenti e 8 ore con i Sistemi Informativi) ([[00-istruzioni-progetto]], [[manini-relazione-processi-gestione-materiali]])
- Lavoro tecnico nel repo GitHub privato [manini-automazione-ddt](https://github.com/Kapnessbolt/manini-automazione-ddt) (report, schema, prompt, script); i dati reali (DDT, verità, inventario) restano su OneDrive in `Progetto Automazione/Dati/` e non entrano mai nel repo. Le copie condivise dei report sono in `Progetto Automazione/Library/` ([[2026-10-23-manini-automazione-ddt]])
- Step 1, inventario: fatto. 15 DDT reali di 14 fornitori, nessun PDF nativo, ordine Manini presente in 10 su 15, codice Manini esplicito in 2 su 15 ([[01-inventario]])
- Step 2, schema JSON: fatto. Schema canonico più versione piatta per AI Builder e Copilot Studio, 13 codici di eccezione ([[03-schema-ddt]])
- Step 3, benchmark: fatto. Campi critici corretti al 100% con il modello generativo standard, all'88% con quello veloce, al 27% con l'OCR classico. Prompt v1.1 ritestato il 25/10: standard 100% e 15/15 DDT pronti (perfetti da 11 a 14), veloce dall'88% al 98% e da 8 a 11 DDT pronti; gli errori che arrivano a un DDT pronto sono tutti segnati in `campi_incerti` ([[04-benchmark]], [[prompt-estrazione-ddt]])
- Step 4, matching contro ordini simulati: fatto in simulazione. Con l'ordine sul DDT l'abbinamento si automatizza senza errori anche a tabella codici vuota (0 errori su 30 simulazioni); DDT pronti 5–7 su 15 all'avviamento con politica automatica, 6–7 a regime; tetto 10/15 per anomalie di processo e DDT senza ordine. Ripetuto il 25/10 sull'output reale dell'estrazione (H29 chiusa): con il modello standard nessun DDT cambia stato e 0 abbinamenti automatici errati; emersi due difetti del motore da correggere (H33, H34). Da ripetere con le righe d'ordine vere ([[05-matching]])
- Step 5, output riusabili: parziale. Piano aula, sessione IT e architettura Microsoft definiti; deck da aggiornare ([[02-aula-e-architettura]])
- Business case del deck v3 di [[leonardo-pinsone]]: 1.860 ore/anno oggi, risparmio 33–47 k€/anno; poggia su due numeri non misurati, i 10 minuti a DDT e la quota del 60/80% di DDT senza eccezioni ([[manini-ddt-essenziale]], [[automazione-entrata-merci-caso-manini]])
- Sul campione il matching simulato porta a un risparmio di circa 630–740 ore/anno (22–26 k€) contro 949 ore (33 k€) del prudente: il 60% è raggiungibile, l'80% no a meno che il campione sovrarappresenti le anomalie. Sull'estrazione reale con il modello standard il risultato non cambia ([[05-matching]])

## Attività

- [x] Step 4: CSV ordini simulato con distrattori (residui, righe evase, UM diverse) e due scenari di tabella codici (avviamento vuota, regime 70–80%) ([[manini-ddt-essenziale]], [[05-matching]])
- [ ] Ripetere il matching con le righe d'ordine vere dei 14 fornitori ([[05-matching]])
- [ ] Chiedere agli acquisti di Manini: un solo contratto quadro aperto per gli inerti (H25), riga a saldo come avviso (H26) ([[05-matching]])
- [ ] Proporre a Manini di chiedere ai fornitori il numero d'ordine sul DDT ([[05-matching]])
- [x] Ritestare il prompt v1.1 sui 15 DDT ✅ 2026-10-25 ([[04-benchmark]])
- [ ] Correggere il motore di matching: ricerca del fornitore per ragione sociale (H33), codice stampato senza ordine in più ordini aperti → E07 (H34); poi rimisurare ([[05-matching]])
- [ ] Nel flusso, mandare a verifica i DDT con un campo critico in `campi_incerti` (H30) ([[04-benchmark]])
- [ ] Revisione umana di 3–4 DDT difficili per verificare la verità del benchmark (H17) ([[04-benchmark]])
- [ ] Prova delle demo con la licenza Copilot di Angelo Santilli 📅 2026-11-05 ([[02-aula-e-architettura]])
- [ ] Preparare file ordini simulato e bozza della tabella codici per le demo in aula ([[02-aula-e-architettura]])
- [ ] Chiedere a Manini: significato del "Mov." sull'etichetta (H1), volumi e registrazione dei DDT della pesa di Bastia (H7), web service o programmi di import su AS400, gateway dati locale ([[02-aula-e-architettura]])
- [ ] Chiedere a Manini i dati: estratto AS400 dei movimenti del campione, righe d'ordine aperte dei 14 fornitori, campione di 80–100 DDT di un mese, materiale del test Sanmarco, misura dei minuti per DDT ([[01-inventario]], [[manini-ddt-essenziale]])
- [ ] Ambiente Power Platform di sviluppo con Copilot Credits nel tenant Manini per l'aula ([[02-aula-e-architettura]])
- [ ] Aggiornare il deck entrata merci: Copilot Credits al posto dei crediti AI Builder, staging al posto della scrittura DB2, ingresso da scansione invece che da casella mail ([[02-aula-e-architettura]])
- [x] Estrarre su OneDrive i PDF dallo ZIP dei DDT, così le sessioni Claude Code li leggono con il connettore ([[2026-10-23-manini-automazione-ddt]])
- [ ] Prompt v1.2 con le correzioni del ritest (peso totale in testata, peso 0 solo se stampato, ordine tra gli altri riferimenti), da ritestare prima dell'uso ([[04-benchmark]])
- [ ] Misurare la variabilità: 3 giri sui DDT difficili (H31), un giro v1.0 con i modelli di oggi (H32), matching sull'estrazione su 30 seed (H35) ([[04-benchmark]], [[05-matching]])

## Decisioni

- Il collo di bottiglia è l'abbinamento con ordini e codici, non la lettura; l'abbinamento fatture già fatto dall'AS400 non si tocca ([[manini-ddt-essenziale]])
- Lettura generativa con schema JSON e regola "trascrivi, non dedurre": prompt AI Builder per il pilota, nodo Extract di Copilot Studio da mostrare, niente modello addestrato per layout ([[02-aula-e-architettura]], [[04-benchmark]])
- In AI Builder e Copilot Studio si sceglie il modello più capace, non quello veloce ([[04-benchmark]])
- Il prompt v1.1 è quello da usare in aula IT e nel pilota; le correzioni candidate vanno in una v1.2, da ritestare prima dell'uso ([[04-benchmark]], [[prompt-estrazione-ddt]])
- Abbinamento deterministico dove si può, AI solo dove serve giudizio; la proposta dell'AI confermata da una persona popola la tabella codici ([[02-aula-e-architettura]])
- Scrittura su AS400 con staging su DB2 più programma RPG di import; niente INSERT diretto, RPA sul 5250 solo come ponte ([[02-aula-e-architettura]])
- Pilota in tre fasi: dati, in ombra solo su Aprilia, scrittura in staging ([[02-aula-e-architettura]])
- Benchmark per campo e per tipo di acquisizione, non per fornitore ([[01-inventario]])
- Nel pilota, abbinamento automatico solo sulle righe con ordine e proposta netta; tutto il resto in eccezione; obiettivo 0 abbinamenti automatici errati ([[05-matching]])
- Repo GitHub dedicato per il lavoro tecnico; dati reali solo su OneDrive; vault per stato, decisioni e attività ([[2026-10-23-manini-automazione-ddt]])
- Il repo legge il vault ma non lo modifica: scheda e log li aggiorna solo l'ingestion giornaliera, dalle copie dei report in `Library/`; ciò che non passa da un report la sessione lo riferisce a Lorenzo (`CLAUDE.md` del repo, §5) ([[2026-10-26-diari-mancanti-e-vault-sola-lettura]])
- Nei report del repo niente anonimizzazione di fornitori, numeri DDT e ordini del campione; i dati riga per riga restano su OneDrive ([[2026-10-23-manini-automazione-ddt]])

## Prossimi passi

- Correggere il motore di matching (H33, H34), poi ripetere il matching con le righe d'ordine vere
- Eventuale prompt v1.2 con le correzioni del ritest (report 04 §10.4), da ritestare prima dell'uso

## Fonti

- [[manini-ddt-essenziale]]
- [[00-istruzioni-progetto]]
- [[01-inventario]]
- [[02-aula-e-architettura]]
- [[03-schema-ddt]]
- [[04-benchmark]]
- [[prompt-estrazione-ddt]]
- [[05-matching]]
- [[automazione-entrata-merci-caso-manini]]
- [[blueage-automation-entrata-merci]]
- [[manini-relazione-processi-gestione-materiali]]
- [[2026-10-23-manini-automazione-ddt]]
- [[2026-10-26-diari-mancanti-e-vault-sola-lettura]]
