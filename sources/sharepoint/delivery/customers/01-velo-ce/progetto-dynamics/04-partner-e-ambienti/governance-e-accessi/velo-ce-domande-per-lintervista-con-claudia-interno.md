---
type: source-doc
source: sharepoint
family: velo-ce-domande-per-lintervista-con-claudia-interno
current:
  item_id: 01EFCYUZ3DBW2YJEA4DFFINBCT6C66ZAZ6
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ3DBW2YJEA4DFFINBCT6C66ZAZ6
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/04 Partner e ambienti/Governance e accessi/Velo-CE - Domande per l'intervista con Claudia - INTERNO - v001.xlsx
  name: Velo-CE - Domande per l'intervista con Claudia - INTERNO - v001.xlsx
  last_modified: 2026-10-06T05:51:51Z
versions:
  - { name: Velo-CE - Domande per l'intervista con Claudia - INTERNO - v001.xlsx, item_id: 01EFCYUZ3DBW2YJEA4DFFINBCT6C66ZAZ6, last_modified: 2026-10-06T05:51:51Z }
  - { name: Velo-CE - Domande per l'intervista con Claudia - INTERNO - v001.xlsx, item_id: 01EFCYUZ5VL2AU2T4GNNB2DRTK3XZW252S, last_modified: 2026-10-06T05:51:51Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:31:42Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]", "[[fatturazione-elettronica-sdi]]"]
tags: [velo-ce, business-central, afc, fiscale, intervista, interno]
---

# Velo-CE · Domande per l'intervista con Claudia (area fiscale)

## Riassunto

Traccia interna BlueAge (v001 del 06/10/2026), non mostrabile a Claudia né al cliente, per l'intervista con la responsabile dell'amministrazione di Velo-CE. Serve a capire quali funzioni dell'area fiscale Claudia usa oggi in Business Central, per preservarle nel nuovo sistema; banche escluse, nessun tema di cambio tenant o di Essentials/Premium. Ha 18 righe: 3 conferme (si mostra quanto visto a sistema), 8 domande aperte e 7 punti chiusi da BlueAge senza domanda. Ogni riga riporta cosa è stato visto a sistema (controlli in sola lettura degli ultimi 12 mesi, 05-06/10), certezza, pagina BC, domanda e cosa cambia per il progetto. Il piano AFC ([[velo-ce-piano-afc-interno]]) rimanda a questo file.

## Punti chiave

- **Conferme**: fatture d'acquisto registrate dal file SdI con l'anteprima dell'app EOS (da preservare dal primo giorno); integrazioni IVA dei fornitori UE (serie FVU, reverse charge standard) e invio TD17/TD18; fatture di vendita manuali, di acconto e note di credito, inviate anche per e-mail dall'app EOS.
- **Domande aperte**: dichiarazioni d'intento emesse e ricevute e controllo del plafond; liquidazione IVA, chiusure e storni fatti con l'utenza ADMIN (chi la usa?); paghe registrate a blocchi fino a maggio 2026; Certificazione Unica, 770, Intrastat e cespiti fuori da BC; incassi Stripe del webshop registrati direttamente a ricavo senza IVA; conto lavoro con DDT in Fatture in Cloud e fatture dei verniciatori 2026 non trovate in BC; valorizzazione delle rimanenze (scrittura manuale di fine anno); conservazione a norma delle fatture.
- **Chiusi da BlueAge**: password dell'intermediario SdI che scade e va reinserita (l'utenza è personale del titolare: tema di governance per Stefano); bollo da 2 euro gestito dall'app EOS; l'ipotesi OSS sulle FVU cade; serie e tipi documento di vendita; in contabilità registrano solo ADMIN e AMMINISTRAZIONE; un job orario gira con l'utenza di Claudia e va spostato su un'utenza tecnica.
- **Attenzioni**: tono neutro sul tema IVA del webshop (si chiude con il commercialista); se Claudia non sa chi usa ADMIN, la domanda passa a Stefano.

## Numeri

- 18 righe: 3 conferme, 8 aperte, 7 chiuse; 11 domande da fare.
- Circa 36 fatture d'acquisto a settimana registrate da Claudia; 39 fatture di vendita in 3 mesi.
- Dichiarazioni d'intento emesse: 31 nel 2025, almeno 15 nel 2026 (due verso la dogana da 2.000.000 e 500.000 euro); una ricevuta da 120.000 euro, usati 85.600.
- Liquidazione IVA: 12 volte con ADMIN fra il 30/09/2025 e il 06/07/2026; 45 storni con ADMIN.
- Stripe: agosto 2026, 29 registrazioni per 8.100,63 euro; ricavo B2C 41.055,74 euro nel 2025 e 44.533,98 euro nel 2026 fino ad agosto.
- Rimanenze: 2.713.672,00 euro al 31/12/2024 e 2.059.737,50 euro al 31/12/2025.
- Intermediario SdI: conserva i file 45 giorni, non fa conservazione a norma.

## Decisioni e azioni

- [ ] Fare l'intervista con Claudia partendo dalle conferme CLA-01…CLA-03
- [ ] Portare a Stefano il tema dell'utenza personale dell'intermediario SdI
- [ ] Chiudere con il commercialista il trattamento IVA delle vendite web (Stripe, eventuale OSS)
- [ ] Chiedere a So Smart lo spostamento del job orario su un'utenza tecnica

## Versioni

- Velo-CE - Domande per l'intervista con Claudia - INTERNO - v001.xlsx · 2026-10-06 · prima versione ingerita
