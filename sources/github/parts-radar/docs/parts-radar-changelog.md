---
type: source-doc
source: github
family: parts-radar-changelog
current:
  item_id: "cristian-schifone/parts-radar:docs/changelog.md"
  uri: "github://cristian-schifone/parts-radar/docs/changelog.md@21621ca2e9a2c70fcf503015fcc6a4f180c016e4"
  web_url: "https://github.com/cristian-schifone/parts-radar/blob/main/docs/changelog.md"
  name: "docs/changelog.md"
  last_modified: 2026-10-26T00:13:33Z
versions:
  - { name: "docs/changelog.md@21621ca", item_id: "cristian-schifone/parts-radar:docs/changelog.md", last_modified: 2026-10-26T00:13:33Z }
  - { name: "docs/changelog.md@61b833c", item_id: "cristian-schifone/parts-radar:docs/changelog.md", last_modified: 2026-10-22T16:51:29Z }
also_at: []
status: active
partial: true
ingested_at: 2026-10-26T06:23:41Z
projects: ["[[parts-radar-sviluppo]]"]
clients: ["[[adac-bologna]]"]
topics: ["[[parts-radar]]"]
tags: []
---

# Parts Radar · changelog del repo

## Riassunto

Diario delle sessioni di sviluppo del repo, una voce per sessione, dalla più recente: obiettivo, cosa è stato fatto, decisioni, cosa resta aperto, prossimi passi. Il ritmo a ottobre è di 3-6 voci al giorno. Nel vault non si copia: ogni giorno con voci nuove diventa una riga nel log di [[parts-radar-sviluppo]], e qui restano le voci degli ultimi 30 giorni in una riga ciascuna. Ultime settimane: chiusa la migrazione a Python e Kromeda (02-05/10), lavoro sulla milestone del pilot ADAC, chat del banco e canale WhatsApp con 360dialog (18-20/10), dataset delle chat reali, router e modalità ascolto (21-22/10), metodo di lavoro e glossario (25-26/10), revisione del router sulle etichette di sviluppo con i prompt congelati (26/10).

## Punti chiave

- Ciclo di lavoro in tre sessioni per feature: A piano e implementazione, B documenti dopo il merge, C feature successiva
- Ogni voce chiude con "Lasciato aperto": è lì che compaiono le azioni fuori dal codice (avvisi a Cristian, domande ad ADAC e Solera)
- Le voci di maggio 2026 descrivono lo stack n8n + TecDoc, ormai dismesso

## Numeri

- 65 voci al 26/10/2026

## Decisioni e azioni

- Le decisioni di ogni voce rimandano ad `architettura.md` §6; quelle di livello progetto sono nel log di [[parts-radar-sviluppo]]

## Voci recenti

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
- 2026-09-28 · Kromeda: scala su 17 veicoli · correzione del risolutore sulle date
- 2026-09-27 · Kromeda: censimento a 17 veicoli · quadro di affidabilità della Fase 0
- 2026-09-26 · Decisione stack Python e pulizia del repo · n8n esce
- 2026-09-25 · Kromeda: terzo lotto del golden · stima di chiamate e costi, VIN rimandato
- 2026-09-24 · Kromeda: golden set esteso · report unico della Fase 0

## Versioni

- docs/changelog.md@21621ca · 2026-10-26 · 5 voci nuove (25-26/10): metodo di lavoro, glossario, istruzioni del repo, revisione del router con prompt congelati, chiusura di /plan-fix
- docs/changelog.md@61b833c · 2026-10-22 · prima lettura nel vault (voci dal 24/09; primo caricamento oltre i 30 giorni)
