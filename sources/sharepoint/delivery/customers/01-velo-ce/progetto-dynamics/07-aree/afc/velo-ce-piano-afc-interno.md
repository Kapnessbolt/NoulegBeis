---
type: source-doc
source: sharepoint
family: velo-ce-piano-afc-interno
current:
  item_id: 01EFCYUZ4GGPB2NBLNDVBYD2UAQ5RMTQOQ
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ4GGPB2NBLNDVBYD2UAQ5RMTQOQ
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/07 Aree/AFC/Velo-CE - Piano AFC - INTERNO - v002.xlsx
  name: Velo-CE - Piano AFC - INTERNO - v002.xlsx
  last_modified: 2026-10-27T15:31:20Z
versions:
  - { name: "Velo-CE - Piano AFC - INTERNO - v002.xlsx", item_id: 01EFCYUZ4GGPB2NBLNDVBYD2UAQ5RMTQOQ, last_modified: 2026-10-27T15:31:20Z }
  - { name: "Velo-CE - Piano AFC - INTERNO - v001.xlsx", item_id: 01EFCYUZYPBI7EHCTPQNDZ7CQE7FFQCEZJ, last_modified: 2026-10-08T10:29:45Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-29T05:58:41Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, business-central, afc, contabilita, ciclo-passivo, interno]
---

# Velo-CE · Piano AFC (amministrazione, finanza e controllo)

## Riassunto

Guida di lavoro interna BlueAge per l'area AFC del progetto Velo-CE (v001 del 06/10/2026, file salvato l'08/10), non mostrabile al cliente. Raccoglie in cinque fogli le 49 voci del perimetro AFC in nove aree, gli open point (domande a Claudia, al commercialista, a Stefano e a So Smart, controlli a sistema, decisioni), le attività da fare nel nuovo tenant con il go-live del 01/01/2027 e le migliorie proposte. Per decisione del 06/10 le domande AFC vivono solo qui. Ogni attività nasce da una decisione; senza decisione è «Prematura». L'autonomia di BlueAge sulla configurazione del nuovo tenant è un'assunzione non ancora verificata. Sintesi per il team in [[velo-ce-sintesi-area-afc-per-leonardo-interno]].

## Punti chiave

- **Ciclo passivo scollegato**: le fatture di merce vanno su conti di costo, una riga per fattura, mai su articoli; ordini d'acquisto ricevuti e mai fatturati; da aprile 2026 la merce si carica con Registrazioni magazzino, spesso a costo zero; il valore di magazzino non va in contabilità al carico.
- **Contabilità generale**: piano dei conti da mantenere e pulire (conti senza categoria o classificati in modo incoerente); un conto per ogni banca invece delle 4 banche su un conto (richiesta di Claudia; il limite indicato da So Smart non esiste nello standard); scritture manuali ricorrenti nel batch VARIE (interessi, Stripe, TFR); risconti a mano con storno al 1° gennaio; contabilità simulata ferma dal 2023 (proposta: non portarla); correzioni con 45 storni e lo strumento PDA.
- **Fatture elettroniche**: utenza dell'intermediario personale del titolare; contratto Able Tech da chiarire (il collegamento l'ha fatto So Smart); invii TD17-TD19 per gli acquisti esteri il 15 del mese con ADMIN.
- **Obblighi**: probabile obbligo di scritture ausiliarie di magazzino (rimanenze 2024 e 2025 sopra soglia), registro oggi non prodotto da BC.
- **Decisioni ad alta priorità**: piano dei conti attuale pulito (AFC-OP08); ciclo acquisti standard con fatture di merce collegate a ordine e ricevimento (AFC-OP30); conta di fine anno entro il 31/12 o giacenza provvisoria rettificata a gennaio (AFC-OP40); DDT di dicembre 2026 da fatturare entro il 15/01/2027, con tre strade (AFC-OP41).
- **Migliorie (11)**: conto per banca, piano dei conti pulito, dimensioni per il controllo di gestione, automazione delle scritture ricorrenti, risconti con modelli di differimento, utenze nominative al posto di ADMIN, utenza aziendale per l'intermediario SdI, ciclo acquisti collegato (fase 1), registro di magazzino, IVA delle vendite web, fattura elettronica abbinata agli articoli (fase 2).
- **v002 (09/10, file aggiornato fino al 27/10)**: le voci del perimetro passano a 65 (16 aggiunte il 13/10 dal confronto con la WBS); nuovi fogli «Traccia Claudia» (traccia dell'incontro del 13/10 sul ciclo passivo), «Anomalie» (dati che non dovrebbero esserci, codici AFC-AN, con impatto sulla ripresa dati e azione prima del taglio) e «Playbook» (le attività AFC che oggi si fanno in BC, con il test da fare nel nuovo ambiente); le migliorie sono classificate per impatto e necessità al 1/1 e dicono cosa si porta nel deck AFC per il cliente. Le letture in Educational dal 09/10 valgono per i dati fino al 06/08/2026.

## Numeri

- v002: 65 voci in 9 aree; 55 open point aperti (23 sul ciclo passivo, 12 sul ciclo attivo, 11 sulla contabilità generale); 14 attività da fare (12 su contabilità generale, 2 sul ciclo passivo); 14 controlli BlueAge aperti.
- v001: 49 voci; 41 open point (39 aperti); 14 attività; 11 migliorie.
- Go-live del nuovo tenant: 01/01/2027.
- Ordine ricevuto e mai fatturato di esempio: CAR26-0039 da 157.136 euro a costo previsto.
- 29 registrazioni Stripe ad agosto 2026; 45 storni con ADMIN in 12 mesi; 7 correzioni PDA nel 2026.
- Ricevimento sugli ordini usato da maggio 2025 ad aprile 2026; registro documenti da fatturare lato acquisti fermo al 29/04/2026.

## Decisioni e azioni

- Decisione (06/10): le domande AFC vivono solo nel piano AFC.
- Orientamento BlueAge (06/10, da confermare): mantenere il piano dei conti attuale, pulito, con un conto per banca; non portare la contabilità simulata.
- [ ] Confermare con Velo-CE e il commercialista il piano dei conti pulito (prima del setup)
- [ ] Preparare e importare piano dei conti, categorie e conto per ogni banca nel nuovo tenant 📅 2027-01-01
- [ ] Ricreare categorie e setup delle registrazioni generali e IVA 📅 2027-01-01
- [ ] Collegare il nuovo tenant all'intermediario SdI con un'utenza aziendale 📅 2027-01-01
- [ ] Configurare il ciclo acquisti standard ordine → ricevimento → fattura 📅 2027-01-01
- [ ] Chiedere al commercialista se c'è l'obbligo delle scritture ausiliarie di magazzino
- [ ] Decidere la data della conta di fine anno e il trattamento dei DDT di dicembre 2026

## Versioni

- Velo-CE - Piano AFC - INTERNO - v001.xlsx · 2026-10-08 · prima versione ingerita (contenuto v001 del 06/10)
- Velo-CE - Piano AFC - INTERNO - v002.xlsx · 2026-10-27 · v002 del 09/10: 65 voci, fogli Traccia Claudia, Anomalie e Playbook; 55 open point aperti (letto il foglio Leggimi); nella cartella `Cristian/07 Aree/AFC/`

