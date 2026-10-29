---
type: source-doc
source: sharepoint
family: velo-ce-app-so-smart-installate-e-premium-interno
current:
  item_id: 01EFCYUZ65VF7UOKXBE5BKKEDZNAMEOFWX
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ65VF7UOKXBE5BKKEDZNAMEOFWX
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/04 Partner e ambienti/App EOS/Velo-CE - App So Smart installate e Premium - INTERNO - v002.xlsx
  name: Velo-CE - App So Smart installate e Premium - INTERNO - v002.xlsx
  last_modified: 2026-10-06T11:35:37Z
versions:
  - { name: Velo-CE - App So Smart installate e Premium - INTERNO - v001.xlsx, item_id: 01EFCYUZ6QBDKWOAGRNRFIWFMFHFQHAHAU, last_modified: 2026-10-06T11:35:37Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:31:42Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]", "[[fatturazione-elettronica-sdi]]"]
tags: [velo-ce, business-central, eos, so-smart, app, premium, interno]
---

# Velo-CE · App So Smart ed EOS installate e verifica Premium

## Riassunto

Cartella di lavoro interna BlueAge (v001, compilata dal 24/09 al 06/10/2026), non mostrabile a So Smart né al cliente. Per ognuna delle 54 app EOS installate in Production riporta uso a Velo-CE, righe nelle tabelle proprie, edizione supportata secondo AppSource (Essentials e/o Premium), copertura della localizzazione italiana standard di Business Central, note per il passaggio a Premium e al nuovo tenant, e una sintesi per Claudia e Stefano. Ha cinque fogli: app EOS, funzioni per app (compilato per la famiglia Accruals), riepilogo per ambito, elenco completo delle 124 app installate con versioni e aggiornamenti, legenda e limiti. Fissa anche l'assunzione di lavoro IVC-1 sul valore delle rimanenze.

## Punti chiave

- **Perimetro**: 124 app in Production, 54 EOS Solutions e 70 Microsoft, tutte di tipo Global, nessuna estensione per-tenant. Delle 54 EOS: 17 con dati, 12 solo setup, 25 senza righe; 7 attive fra il 24 e il 29/09 (So Smart Application, So Smart System, Electronic Invoice for Italy, Advanced Document Reporting, Accruals and Simulated Common Library, VAT Management for Italy, Inventory Valuation and Costing).
- **Pacchetto So Smart**: So Smart Application (flusso ordini MMI, job «So Smart», report di DDT e fattura accompagnatoria, «C\Lavoro» e Connettore WMS spenti) e So Smart System (distribuzione app, autorizzazioni EOS) sono app Global senza documentazione pubblica: per il nuovo tenant vanno installate e riconfigurate; il supporto Premium è da chiedere.
- **Fattura elettronica (EX063)**: in uso; vendite inviate la sera con l'utenza ADMIN verso l'intermediario Able Tech, fatture fornitori importate in automatico. Premium supportato secondo AppSource; il nuovo framework e-documents per lo SdI è previsto solo per la release wave 1 del 2027, quindi non disponibile per la partenza del 01/01/2027. Va portata.
- **Accruals (EX001)**: ratei, risconti e contabilità simulata fermi dal gennaio 2023; vivo solo il registro dei documenti spediti e non fatturati. Candidata all'uscita con 5 app collegate.
- **Posted Data Administration Tool (EX065)**: strumento protetto da password per correggere dati registrati, usato nel 2026 su IVA, libro giornale, un incasso e descrizioni di fatture; non si toglie d'ufficio, si decide chi lo usa.
- **Advanced Document Reporting (EX009)**: invio quotidiano per e-mail di conferme d'ordine e fatture ai clienti esteri nella loro lingua; una sola grafica Veloe anche per Van Nicholas.
- **Inventory Valuation and Costing (EX053)**: calcola il valore di fine anno (FIFO, LIFO, medio ponderato); il magazzino di BC non è collegato alla contabilità. Assunzione IVC-1 (Cristian, 05/10): il totale delle rimanenze in bilancio viene da IVC, quindi IVC si sostituisce con la valutazione standard dopo la chiusura 2026, con lo stesso metodo; conferma attesa da Claudia (domanda I18).
- **Fiscali da verificare in sandbox Premium**: VAT Management (dichiarazioni d'intento, plafond), Certificazioni Uniche (uso a scadenza, marzo), Enasarco e Commissions solo setup.
- **Perimetro della verifica Premium** (Cristian, 01/10): le tre app fiscali segnalate da Leonardo e le cinque funzioni del deck v006; il pacchetto So Smart è un blocco a parte.

## Numeri

- 54 app EOS (5.254 oggetti) su 124 app; righe totali nelle tabelle proprie circa 2,88 milioni, di cui 2,31 milioni nel pacchetto So Smart e circa 513.000 nella fattura elettronica.
- 10 app EOS con aggiornamento disponibile; So Smart Application 28.0.67.0 → 28.0.71.0, Inventory Valuation and Costing 28.0.81.0 → 28.0.92.0.
- Rimanenze: unico saldo di 2.059.737,50 euro su «Variazione rimanenze iniziali» (fine 2025).
- Accruals: 37.535 righe, +341 movimenti fra il 24 e il 29/09.
- PDA: 7 richieste nel 2026.

## Decisioni e azioni

- Decisione (Cristian, 01/10): perimetro della verifica Premium limitato alle tre app fiscali e alle cinque funzioni del deck v006.
- Assunzione IVC-1 (Cristian, 05/10): IVC si sostituisce con continuità, non si toglie.
- [ ] Chiedere a So Smart se il pacchetto So Smart è supportato in Premium e come si installa nel nuovo tenant
- [ ] Chiedere a Claudia chi conserva a norma le fatture e come entrano in contabilità quelle di Fatture in Cloud
- [ ] Chiedere ad Anton chi invia con l'utenza ADMIN e se serve una grafica Van Nicholas
- [ ] Provare nella sandbox Premium VAT Management, Certificazioni Uniche e dichiarazioni d'intento nella fattura elettronica
- [ ] Completare il foglio «Funzioni per app» per le altre app

## Versioni

- Velo-CE - App So Smart installate e Premium - INTERNO - v001.xlsx · 2026-10-06 · prima versione ingerita
