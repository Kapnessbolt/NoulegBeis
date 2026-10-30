---
type: source-doc
source: sharepoint
family: velo-ce-conti-del-ciclo-dacquisto-per-scenario-interno
current:
  item_id: 01EFCYUZ7QXDSMGTAK4ZFLN3YEJ6ZLQLPF
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ7QXDSMGTAK4ZFLN3YEJ6ZLQLPF
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/07 Aree/AFC/Oda/Velo-CE - Conti del ciclo d'acquisto per scenario - INTERNO - v002.md
  name: Velo-CE - Conti del ciclo d'acquisto per scenario - INTERNO - v002.md
  last_modified: 2026-10-29T16:15:53Z
versions:
  - { name: "Velo-CE - Conti del ciclo d'acquisto per scenario - INTERNO - v002.md", item_id: 01EFCYUZ7QXDSMGTAK4ZFLN3YEJ6ZLQLPF, last_modified: 2026-10-29T16:15:53Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-30T06:01:05Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, afc, ciclo-acquisto, anticipi, plafond, interno]
---

# Velo-CE · Conti del ciclo d'acquisto per scenario (v002)

## Riassunto

Mappa interna BlueAge (v002 del 28/10/2026, corretta sul posto il 28/10 sera e il 29/10) dei conti mossi dal ciclo d'acquisto di [[velo-ce]] in sei scenari: Italia, Italia con plafond, UE senza plafond, UE con plafond (mai usato, non provato), extra-UE con e senza plafond. Per ogni scenario mette a confronto le scritture di oggi, lette in Production, con quelle di domani provate in sandbox nella società VC-IMPORT PROVA del tenant BlueAge, compresi pagamenti in dollari e anticipi sul fornitore. Base della scheda operativa e della guida del ciclo d'acquisto ([[velo-ce-guida-ciclo-dacquisto-ordine-ricevimento-fattura-cliente]]).

## Punti chiave

- **Il giro di domani funziona in standard per tutti gli scenari previsti**: ordine, carico con il riferimento della spedizione, fattura dal carico, addebiti TRASP e DAZI, bolla doganale chiusa dal metodo di pagamento dedicato, fattura estera in dollari, pagamento con differenze di cambio calcolate da BC. Nessuna estensione serve.
- **Conto acquisti dal Setup registrazioni COGE**, non da chi registra: nella proposta i componenti restano per area e le altre nature vanno per natura; la scelta resta aperta (D-09, [[velo-ce-conti-acquisti-per-natura-o-per-area-cliente]]).
- **Plafond**: la localizzazione italiana standard conta il plafond, ma il codice IVA si sceglie a mano sulla riga e il numero della dichiarazione d'intento non arriva sul movimento (oggi lo mette l'app EOS); resta aperto AFC-OP90.
- **Magazzino in contabilità**: con il flag acceso ogni documento aggiunge due righe e il transitorio di magazzino cresce senza chiudersi; con l'orientamento del 28/10 il flag resta spento nel 2027 e le prove valgono per l'accensione del 2028 ([[velo-ce-contabilita-di-magazzino-attivita-di-claudia-con-il-flag-acceso-e-spento-interno]]).
- **Anticipi**: sul fornitore, sempre sul conto 03038110 con la categoria alternativa ANT, collegati alla fattura (provato il 29/10, con il controllo dell'errore umano); la rettifica cambi rivaluta anche gli anticipi aperti e non li esclude: decide il commercialista ([[velo-ce-setup-anticipi-fornitori-so-smart]]).
- **Setup da portare nel nuovo BC**: metodo di pagamento della bolla con contropartita il transitorio dogana, IVA ESC15 sull'addebito DAZI, categorie fornitori alternative, conti delle differenze cambio su ogni valuta, categoria COGE sui conti usati nelle righe su conto, tabella dei cambi aggiornata (oggi ferma al 17/02/2023), colonne delle categorie visibili sulle righe.

## Numeri

- Prove del 28-29/10: evidenze T300-T334; letture in Production E256-E264.
- Esempio extra-UE di prova: costo a magazzino del componente 1.046,59 € su 200 pezzi con dazio e nolo assegnati.

## Decisioni e azioni

- [ ] Decidere con Stefano e Claudia se servono acquisti UE in plafond (AFC-OP88)
- [ ] Scegliere fra plafond standard con codice a mano e app EOS per la sostituzione automatica (AFC-OP90)
- [ ] Decidere con il commercialista il cambio della fattura estera e il trattamento degli anticipi aperti alla rettifica cambi

## Versioni

- Velo-CE - Conti del ciclo d'acquisto per scenario - INTERNO - v002.md · 2026-10-29 · prima versione ingerita (v002 del 28/10, corretta sul posto il 29/10; v001 del mattino del 28/10 superata)
