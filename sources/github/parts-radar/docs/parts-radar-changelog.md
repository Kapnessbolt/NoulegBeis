---
type: source-doc
source: github
family: parts-radar-changelog
current:
  item_id: "cristian-schifone/parts-radar:docs/changelog.md"
  uri: "github://cristian-schifone/parts-radar/docs/changelog.md@2be8540128a7fb61cdf4f7c7b2eb2c1385ef5e9e"
  web_url: "https://github.com/cristian-schifone/parts-radar/blob/main/docs/changelog.md"
  name: "docs/changelog.md"
  last_modified: 2026-10-29T22:57:06Z
versions:
  - { name: docs/changelog.md@2be8540, item_id: cristian-schifone/parts-radar:docs/changelog.md, last_modified: 2026-10-29T22:57:06Z }
  - { name: docs/changelog.md@733d0a6, item_id: cristian-schifone/parts-radar:docs/changelog.md, last_modified: 2026-10-28T23:22:29Z }
  - { name: docs/changelog.md@a6cfb1f, item_id: cristian-schifone/parts-radar:docs/changelog.md, last_modified: 2026-10-27T22:43:07Z }
  - { name: docs/changelog.md@cd736f2, item_id: cristian-schifone/parts-radar:docs/changelog.md, last_modified: 2026-10-26T23:50:11Z }
  - { name: docs/changelog.md@21621ca, item_id: cristian-schifone/parts-radar:docs/changelog.md, last_modified: 2026-10-26T00:13:33Z }
  - { name: docs/changelog.md@61b833c, item_id: cristian-schifone/parts-radar:docs/changelog.md, last_modified: 2026-10-22T16:51:29Z }
also_at: []
status: active
partial: true
ingested_at: 2026-10-30T06:30:05Z
projects: ["[[parts-radar-sviluppo]]"]
clients: ["[[adac-bologna]]"]
topics: ["[[parts-radar]]"]
tags: []
---

# Parts Radar · changelog del repo

## Riassunto

Diario delle sessioni di sviluppo del repo, una voce per sessione, dalla più recente: obiettivo, cosa è stato fatto, decisioni, cosa resta aperto, prossimi passi. Il ritmo a ottobre è di 3-6 voci al giorno. Nel vault non si copia: ogni giorno con voci nuove diventa una riga nel log di [[parts-radar-sviluppo]], e qui restano le voci degli ultimi 30 giorni in una riga ciascuna. Ultime settimane: chiusa la migrazione a Python e Kromeda (02-05/10), lavoro sulla milestone del pilot ADAC, chat del banco e canale WhatsApp con 360dialog (18-20/10), dataset delle chat reali, router e modalità ascolto (21-22/10), metodo di lavoro e glossario (25-26/10), revisione del router sulle etichette di sviluppo con i prompt congelati (26/10), etichette del test e misura del router sul test (26/10), vocali: motore deciso e trascrizione nel servizio, spenta (26-27/10), poi doppia lettura con Soniox primo motore e targa da ascoltare (27/10); regole delle prove del pilot e prova a secco preparata (27/10); prova a secco fatta e cinque correzioni nate da lì, misura dei vocali sul test e correzioni del cancello e dei codici dettati (28/10); 360dialog Regular a nome di ADAC coi vincoli del webhook (29/10); etichette e misura della voce sulle chat, lessico della voce e ciclo di lavoro in una sessione sola (29/10).

## Punti chiave

- Ciclo di lavoro: fino al 29/10 tre sessioni per feature (A piano e implementazione, B documenti dopo il merge, C feature successiva); dal 29/10 una sessione sola per feature o fix, con i documenti nella stessa PR del codice
- Ogni voce chiude con "Lasciato aperto": è lì che compaiono le azioni fuori dal codice (avvisi a Cristian, domande ad ADAC e Solera)
- Le voci di maggio 2026 descrivono lo stack n8n + TecDoc, ormai dismesso

## Numeri

- 90 voci al 30/10/2026

## Decisioni e azioni

- Le decisioni di ogni voce rimandano ad `architettura.md` §6; quelle di livello progetto sono nel log di [[parts-radar-sviluppo]]

## Voci recenti

- 2026-10-29 · Ciclo unico per feature e fix · una sessione sola, piano e documenti in sotto-agenti, documenti nella stessa PR; Lorenzo interviene su scelte, spese, giudizi di revisione e proposte della retro; il risparmio si misura sulla prima feature
- 2026-10-29 · Lessico della voce dalle chat di sviluppo · sviluppo 95,6% giusta tra le prime tre, test 93,6% (neutro, dentro il criterio deciso prima); 4,50 $ sul credito di Lorenzo; staging da allineare (Cristian), riga alzavetro da confermare (Lorenzo)
- 2026-10-29 · Misura della voce sulle chat · per pezzo 94,9% sullo sviluppo e 93,8% sul test (soglia 90%), sbagliata data per sicura 1,4% e 0,6% (soglia 2%); la chiusura della #345 la decide Lorenzo
- 2026-10-29 · Etichette della voce sulle frasi delle chat · etichettatore Opus, la frase come unità, taratura su golden e sintetico
- 2026-10-29 · Stato dell'ordine dei lavori e 360dialog Regular a nome di ADAC · percorso critico sui passi fuori dal codice; webhook senza firma accettato coi vincoli V1-V8, da fare prima dell'attivazione; restano da allineare brand e targhe provinciali
- 2026-10-28 · Codici dettati nei vocali · 16 su 20 (80%, al limite); staging da allineare (Cristian)
- 2026-10-28 · Targa letta a metà → gruppo da ascoltare · il cancello dei vocali rientra (0 targhe sbagliate), ma da ascoltare al 27,1% sopra la soglia del 25%
- 2026-10-28 · Misura dei vocali sul test · targa al limite delle soglie, codici dettati 33,3% contro 80%, cancello caduto; tre issue di correzione
- 2026-10-28 · Lato gemello sugli affini · chiude il caso delle cuffie semiasse della prova a secco; staging da allineare (Cristian)
- 2026-10-28 · Varianti della stessa voce al banco come alternative · il banco non deve più scegliere la voce ogni volta; staging da allineare (Cristian)
- 2026-10-28 · Lessico di frizione e filtri nella voce · due casi della prova a secco
- 2026-10-28 · Codice del meccanico per codice, col controllo sull'auto · non va più per voce sull'ultima auto del telefono; staging da aggiornare (Cristian)
- 2026-10-28 · Prova a secco del pilot · 38 messaggi sul flusso intero, 0 errori, 0 crediti, 0,12 $; 30 componenti su 40 giusti, 10 casi in cinque issue; conservazione delle registrazioni dal vivo la decide Cristian
- 2026-10-27 · Prova a secco con Kromeda in trasporto misto · ricerca targa solo dalle registrazioni, il resto dal vivo, e registrazione delle chiamate dal vivo per il replay dopo la demo; restano la prova breve dal vivo e la conservazione delle registrazioni (Cristian)
- 2026-10-27 · Regole delle prove del pilot · 20 scenari su 3-4 auto nostre e tre telefoni, catena intera almeno al 70%, cancello per origine della targa; la prova segue l'attivazione del numero di ADAC; il file delle auto lo compila Lorenzo
- 2026-10-27 · Graphify senza hook · strumenti di lavoro
- 2026-10-27 · Ritocchi dalla retro della #477 · regole di lavoro
- 2026-10-27 · Vocali: doppia lettura nel servizio, Soniox primo motore, targa da ascoltare · su H 0 targhe confermate sbagliate sui dettati di prova; trascrizione spenta finché non ci sono consenso di ADAC, progetti a nome di BlueAge e contratto dati con Soniox; avviso a Cristian per lo staging
- 2026-10-27 · Vocali: regola di sicurezza e doppia lettura misurata · nei gruppi con un vocale la targa si recupera solo per citazione, anche a trascrizione spenta; Soniox batte Gemini su H
- 2026-10-27 · Misura del recupero della targa sulle etichette · la finestra resta 30 minuti, la taratura passa al traffico del pilot
- 2026-10-27 · Vocali: la trascrizione nel servizio, spenta · pronta ma non accesa, prova dal vivo su due dettati (circa 0,0015 $ a giro); restano la misura finale sul test, il consenso di ADAC, il progetto Google a nome di BlueAge; avviso a Cristian per lo staging preparato, lo manda Lorenzo
- 2026-10-27 · Ritocchi dalla retro dei vocali · regole di lavoro; un punto da concordare con Cristian
- 2026-10-26 · Vocali: motore deciso e alfabeto delle città · Gemini 3.5 Transcribe; sul test di H la targa giusta passa dal 19,5% al 78,4% dei pezzi
- 2026-10-26 · Etichette del test, misura del router e revisione delegata · 550 gruppi etichettati; router d'accordo al 93% su richiesta sì/no; nuova decisione aperta sulle targhe nel vecchio formato
- 2026-10-26 · Etichettatore Opus per le etichette del test · tarato sulle chat di sviluppo, 97 su 100 d'accordo con Lorenzo; avviso a Cristian da mandare
- 2026-10-26 · Chiusura di /plan-fix in ordine e gh aggiornato · strumenti di lavoro; gh da aggiornare anche sulla macchina di Cristian
- 2026-10-26 · Revisione dei disaccordi del router e prompt congelati · 810 etichette di sviluppo corrette con Lorenzo, proposte perse dal router da 12 a 7 (4,40 $ di misure); prompt fermi per le etichette del test; Cristian da avvisare per il rebuild del servizio sullo staging
- 2026-10-26 · Istruzioni del repo come mappa e /retro nel ciclo A · istruzioni dimezzate; le parti 3 e 4 della #447 le decide Cristian
- 2026-10-26 · Glossario del dominio · circa 75 parole definite una volta sola; il cliente di BlueAge si chiama ricambista
- 2026-10-25 · Metodo di lavoro: due revisori e diagnosi dal comando rosso · regole e aderenza all'issue riviste in parallelo prima di ogni PR
- 2026-10-22 · Date della dashboard in ora di Roma · correzione: gli operatori vedevano orari indietro di 1-2 ore
- 2026-10-22 · Modalità ascolto · catalogo dal vivo e messaggi automatici accesi cliente per cliente, spenti di default; riserva di 15 crediti targa; avviso a Cristian da mandare
- 2026-10-22 · Guardia d'avvio alla migration 083 · correzione tecnica
- 2026-10-22 · Router in ingresso acceso · i messaggi che non chiedono un pezzo non diventano più richieste; il banco vede tipo e causa
- 2026-10-22 · Router: contratto e misura su Haiku 5.5 · richieste false da 42 a 12 su 162 gruppi senza richiesta; modello scelto da Lorenzo
- 2026-10-22 · Domande aperte verso ADAC · risposte di Lorenzo; brand, officine, gruppi, data del pilot e altro chiesti a Luca Degli Esposti; nasce la #430 (estrazione strutturata)
- 2026-10-21 · Tipo dentro "altro" nelle etichette · il router diventa un front office che legge
- 2026-10-21 · Targa dei pezzi aggiunti dopo · ricavata dal messaggio citato
- 2026-10-21 · Gruppi del debounce ed etichette delle chat · pagina locale per etichettare a mano
- 2026-10-21 · Chat reali di ADAC nel simulatore · con i tempi veri
- 2026-10-21 · Modello di riserva dell'LLM · il servizio non si ferma se il modello principale non risponde
- 2026-10-21 · Motivi degli esiti chiari per il banco · testi
- 2026-10-21 · Testi degli esiti per il banco · testi
- 2026-10-21 · Scelta di un veicolo suggerito dal catalogo · quando la targa non trova il veicolo
- 2026-10-20 · Aggiornamento di sicurezza di uv · da riportare sul clone e sullo staging
- 2026-10-20 · Prova dal vivo dei codici paralleli e giro degli alberi Kromeda · per la demo
- 2026-10-20 · Codici paralleli a richiesta dell'operatore · funzione nuova
- 2026-10-20 · CI per aree · meno costo di Actions
- 2026-10-20 · Codice riempito di zeri · chiusa senza codice
- 2026-10-20 · Dashboard su telefono · correzioni
- 2026-10-20 · Passaggio del servizio a Claude Haiku 5.5 · confidenza della voce a 0,85
- 2026-10-20 · Moduli della dashboard in POST · sicurezza
- 2026-10-20 · Login: seguiti della sicurezza · sicurezza
- 2026-10-20 · Login: credenziali fuori dall'indirizzo · sicurezza
- 2026-10-20 · Risposte dal telefono del banco nella chat · Twilio fuori dal codice
- 2026-10-19 · 360dialog con la Coexistence · scelto per il pilot al posto di Twilio
- 2026-10-19 · Media nella chat del banco · foto, vocali e PDF nei due sensi
- 2026-10-19 · Chat del banco con invio WhatsApp dalla dashboard · l'operatore risponde dalla dashboard
- 2026-10-18 · Avvisi per il banco · ripartenze non riuscite e contatori
- 2026-10-18 · Prima prova dal vivo con Twilio · Haiku 5.5 nel servizio
- 2026-10-17 · Fornitori WhatsApp Twilio e Uniwaba · motori di trascrizione dei vocali in prova
- 2026-10-16 · Installazione da zero sul compose di produzione · base per il server del pilot
- 2026-10-14 · Le 10 chat reali di ADAC · dataset, vocali, gruppi, primo giro degli alberi
- 2026-10-13 · Revisione delle decisioni su router, foto, targa recuperata e dataset · piano
- 2026-10-11 · Scelta del veicolo che fa ripartire le altre richieste · funzione
- 2026-10-10 · Fusione multi-veicolo e testi dei veicoli divergenti · funzione
- 2026-10-09 · Certificazione del risolutore · regole del deterministico chiuse
- 2026-10-08 · Codice venduto per ogni originale e cache Kromeda · meno chiamate
- 2026-10-07 · Prompt della voce, sessioni e credenziali · più sicurezza e voce v2
- 2026-10-06 · Dopo lo swarm: merge su main e piano verso il pilot · nasce la milestone "Pilot ADAC"
- 2026-10-05 · Swarm di ottobre · servizio Python, DB v2 e cutover in sviluppo (02-05/10)
- 2026-10-02 · Kromeda: golden mirato, 20 targhe · scala su 20 veicoli

## Versioni

- docs/changelog.md@2be8540 · 2026-10-29 · 4 voci nuove (29/10): etichette e misura della voce sulle chat, lessico della voce, ciclo unico per feature e fix
- docs/changelog.md@733d0a6 · 2026-10-29 · 9 voci nuove (28-29/10): prova a secco e le sue correzioni, misura dei vocali e correzioni del cancello e dei codici dettati, ordine dei lavori e 360dialog Regular
- docs/changelog.md@a6cfb1f · 2026-10-27 · 7 voci nuove (27/10): misura della targa, regola di sicurezza e doppia lettura dei vocali, ritocchi dalla retro, graphify, regole delle prove del pilot, prova a secco
- docs/changelog.md@cd736f2 · 2026-10-27 · 5 voci nuove (26-27/10): etichettatore Opus, etichette del test e misura del router, vocali (motore e alfabeto, poi integrazione spenta), ritocchi dalla retro
- docs/changelog.md@21621ca · 2026-10-26 · 5 voci nuove (25-26/10): metodo di lavoro, glossario, istruzioni del repo, revisione del router con prompt congelati, chiusura di /plan-fix
- docs/changelog.md@61b833c · 2026-10-22 · prima lettura nel vault (voci dal 24/09; primo caricamento oltre i 30 giorni)
