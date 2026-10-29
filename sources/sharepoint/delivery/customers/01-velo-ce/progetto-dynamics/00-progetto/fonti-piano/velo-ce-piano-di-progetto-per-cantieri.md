---
type: source-doc
source: sharepoint
family: velo-ce-piano-di-progetto-per-cantieri
current:
  item_id: 01EFCYUZ6FOQMAVJ5VPRFJKJVMCFHILPBV
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ6FOQMAVJ5VPRFJKJVMCFHILPBV
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/00 Progetto/_fonti piano/Velo-CE - Piano di progetto per cantieri.xlsx
  name: Velo-CE - Piano di progetto per cantieri.xlsx
  last_modified: 2026-09-21T12:23:52Z
versions:
  - { name: Velo-CE - Piano di progetto per cantieri.xlsx, item_id: 01EFCYUZ4RC25RN4PTWRCZAWJLGMVCKHXI, last_modified: 2026-09-21T12:23:52Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:25:33Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [piano, cantieri, porte, onde, decisioni, interno]
---

# Velo-CE · Piano di progetto per cantieri

## Riassunto

Piano eseguibile interno BlueAge (v001 del 18/09/2026, aggiornato il 21/09) che affianca la [[velo-ce-mappa-cantieri-dynamics]] senza sostituirla: effort e prezzi restano là. Raccorda le tre numerazioni del progetto (cantieri 0-8 dello stato progetto, cantieri C01-C31 della Mappa, codici del backlog), definisce le cinque «porte» che comandano l'avvio dei cantieri, ordina gli interventi in onde per eseguibilità e riordina le decisioni per data in cui servono. Avverte che tutto poggia su un'assunzione non verificata: che la configurazione applicativa sia lavoro di BlueAge e non debba passare da So Smart. È una delle fonti del nuovo piano di progetto in `_fonti piano`.

## Punti chiave

- **Le cinque porte**: G-LIC licenza (D12 Essentials o Premium, decide il titolare, nessuna scadenza dal 21/09 perché le sottoscrizioni sono mensili, proposta BlueAge Premium); G-DATI estrazione completa degli articoli (A03, entro il 21/09); G-COD standard di codifica scritto (decide il cliente, porta più pesante, prima della ripresa dati); G-SS autonomia di BlueAge sulla configurazione (tre pagine BC, entro il 21/09); G-AMB sandbox dedicata alle prove (dall'Admin Center).
- **Raccordo dei cantieri al 18/09**: anagrafiche in corso (clienti e fornitori quasi a posto, articoli il cantiere vero); codifica saldatura ferma sulla porta G-COD; distinte avviabili in parte (assemblaggio già in uso); giro materiali e acquisti centralizzati fattibili in Essentials; MRP tecnicamente aperto in Essentials; produzione ferma sulla porta G-LIC (ordini di produzione e cicli richiedono Premium); costificazione avviabile in parte; riclassificato e controllo nel 2027.
- **Onda 0 (subito, costo zero)**: licenze Team Members già pagate, utenza nominale BlueAge con licenza (A13), delega GDAP declassata a rilievo di governance, account di amministrazione locali di So Smart nel tenant da censire (G04), prova di Premium in una sandbox del cliente (R10), decisione D12.
- **Onda 1 (ottobre, rilevazione e pulizia in Essentials)**: tre pagine BC per chiudere SS1, estrazione articoli, registro modifiche prima degli interventi massivi, set di autorizzazioni, stati articolo, categorie, bonifica degli articoli a costo zero, censimento dei software satellite.
- **Onda 2 (ottobre-dicembre, codifica)**: standard di codifica radice più desinenza, contenuto della variante, perimetro del rifacimento, codifica dell'area saldatura e delle materie prime a metro e a kg, categorie di registrazione, attributi.
- **Onda 3 (novembre-gennaio, distinte e costo del pezzo)**: criterio della realtà fisica, distinta del telaio, mozzo raggiato, risorse in distinta, sistema di rifornimento (riga più a rischio per l'impatto sugli oggetti So Smart), catena di assemblaggi a più livelli da provare.
- **Onda 4 (gennaio-marzo, giro materiali e conto lavoro)**: dazi e trasporti con gli addebiti articolo (provati in Essentials), verniciatura esterna modellata in Essentials, conto lavoro (Essentials o app Subcontracting gratuita in Premium), metodi di riordino, stock Accell da ripartire, registrazione del costo di magazzino in C/G con il commercialista.
- **Onda 5 (da aprile 2027)**: MRP, produzione (solo se Premium), blocco vendite, spedizioni e contabilità, estensioni da settembre 2027.

## Numeri

- Assemblaggio già in uso: 1.263 righe di distinta e 571 ordini registrati.
- 669 articoli con rifornimento Acquisto e costo zero da bonificare; 150.000 euro di stock Accell da ripartire sui codici.
- Prova della verniciatura esterna in Essentials (18/09): costo del pezzo da 74,86 a 86,86.
- Censimento dei software satellite: 25 righe; due licenze Team Members pagate e mai usate; tre utenze con Power BI Pro contro due in sottoscrizione aziendale.
- 18 decisioni nel foglio per data: D02 presa (colore come variante), D06 presa in parte (grezzo e verniciato codificati), le altre aperte.

## Decisioni e azioni

- Decisione presa: D02, colore come variante; D06 in parte; R06 chiusa il 19/09 (la variante si scrive sulla riga di distinta); R02 chiusa in via tecnica il 20/09 (calcolo del piano funziona con licenza Essentials); G01b e G03 chiuse il 21/09; L02 caduta il 21/09.
- [ ] Verificare l'assunzione SS1 (autonomia di BlueAge sulla configurazione) aprendo le pagine 2500, 810 e 672 📅 2026-09-21
- [ ] Estrazione completa degli articoli (A03), richiesta da Leo 📅 2026-09-21
- [ ] Decisione D12 Essentials o Premium (proposta BlueAge: Premium)
- [ ] Scrivere e far approvare lo standard di codifica (porta G-COD) prima della ripresa dati
- [ ] Creare una sandbox dedicata alle prove (porta G-AMB)

## Versioni

- Velo-CE - Piano di progetto per cantieri.xlsx · 2026-09-21 · prima versione ingerita; v001 del 18/09/2026 aggiornata il 21/09
