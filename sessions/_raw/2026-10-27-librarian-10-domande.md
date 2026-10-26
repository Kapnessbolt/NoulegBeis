# Prova del librarian · 10 domande (criterio dello step 17, SPEC 13.1)

Sessione del 26–27/10/2026, diario [[2026-10-27-step-17-librarian]]. Agente `librarian` lanciato tre volte in parallelo (4 + 3 + 4 domande), solo sulle note, senza connettori. Risposta attesa letta dal vault prima della prova; esito: corretta se il dato coincide e le fonti citate sono quelle che lo reggono.

| n | Domanda | Risposta attesa | Esito | Fonti citate dal librarian (le principali) |
|---|---|---|---|---|
| 1 | Ore e gruppi del corso AI utenti Manini dopo la call del 16/10; ore per i Sistemi Informativi | 36 ore, tre gruppi da 12; IT 8 ore | corretta | manini-corso-ai-recap-della-call-del-16-10, gruppi, corso-ai-manini |
| 2 | Chi decide in Manini sul corso AI | Luciano Baccarelli (CFO) e l'amministratore delegato | corretta (segnala che il nome dell'AD non è nel vault) | manini-corso-ai-quadro-interno-blueage, manini, luciano-baccarelli |
| 3 | I tre DDT dell'aula utenti e perché | Hilti (facile), Iron Works (45 righe), 004664 (illeggibile, rifiutato) | corretta, con il perché dall'inventario | 04-benchmark, 02-aula-e-architettura, 01-inventario, prompt-estrazione-ddt |
| 4 | Cos'è Pulse Light e quale cliente fa da laboratorio | versione ridotta di Pulse; laboratorio Velo-CE | corretta | pulse-light, blueage-le-idee-per-crescere, call-di-oggi-prossimi-passi-architettura-copilot-manini-meccanotecnica-second-brain |
| 5 | Giornate del percorso supply chain Manini | 10, 11, 24, 25 settembre e 8 ottobre 2026 | corretta (segnala l'incoerenza "sei giornate" nel log) | manini-relazione-processi-gestione-materiali, manini-supply-chain-magazzino-log |
| 6 | Rischio bloccante per il go-live BC di Velo-CE | fattura elettronica: lo standard non trasmette allo SdI, e-documents con la wave 1 2027 | corretta, con gli open point collegati | velo-ce-open-point-interno, velo-ce-piano-attivita-nuovo-ambiente-interno |
| 7 | Quotazione BlueAge blocchi 1–3 Velo-CE e giornate | 98.000 € a corpo, 147,5 giornate; programma ~408 | corretta, con il dettaglio per blocco | velo-ce-mappa-cantieri-dynamics, velo-ce-stato-progetto-05-stato-info-quotazione |
| 8 | Perché Parts Radar ha lasciato n8n e quando | licenza solo uso interno; deciso 26/09, migrazione 02–05/10 | corretta | parts-radar-decisione-stack-python, parts-radar-sviluppo-log |
| 9 | Corso MTU: ore, dirigenti, scadenza, finanziamento | 48 ore, 5 dirigenti, entro 27/01/2027, Fondirigenti Avviso 1/2026 via UBS | corretta | corso-ai-mtu, avviso-1-2026-fondirigenti-meccanotecnica-umbra-docenza-leonardo-pinsone, meccanotecnica-umbra-spa-programma-didattico-azienda |
| 10 | Risposta di BlueAge alla LIUC sull'osservatorio e quando | 22/10: scala 0–4 con barometro trimestrale, pilota 3–5 aziende, bollino, due casi in aula, mini-paper | corretta | osservatorio-ai-nelle-pmi-cosa-misureremmo-e-come-partiremmo, liuc-call-con-francesco-bollazzi-e-proposta-di-osservatorio-sull-ai-nelle-pmi-idee-entro-mercoledi-sera |
| C | Controllo fuori knowledge: fatturato 2025 di Qricambi | il vault non lo sa | corretta: "nel vault non c'è", con dove potrebbe stare | qricambi, integrazione-api-qricambi-proposta-di-collaborazione |

Esito: 10 su 10 corrette con le fonti; la domanda di controllo non ha prodotto invenzioni.

Difetto rilevato: risposte lunghe (contesto non chiesto). Corretto nel librarian con il limite di 3–8 righe per la risposta.

Lacune del vault segnalate dal librarian (da decidere in sessione):
- nome dell'amministratore delegato di Manini assente;
- data e contenuti delle 8 ore IT di Manini non ancora arrivati;
- `pulse-light` senza `clients` (corretto in sessione: `[[velo-ce]]`); `manini-relazione-processi-gestione-materiali` senza `projects` (corretto: `[[manini-supply-chain-magazzino]]`);
- riga "sei giornate" nel log di `manini-supply-chain-magazzino` da precisare (cinque d'aula più la presentazione del 9/10);
- `corso-ai-mtu`: "Confermare il calendario" spuntata il 26/10 senza la riga che dice quale calendario;
- "foglio quotazione blocchi" di Velo-CE citato ma non ingerito; nessuna offerta formale a Velo-CE nel vault;
- risposta di Bollazzi (LIUC) alla mail del 22/10 non ancora nel vault.
