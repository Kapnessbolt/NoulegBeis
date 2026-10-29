---
type: source-doc
source: sharepoint
family: velo-ce-proposta-conti-categorie-articolo-cliente
current:
  item_id: 01EFCYUZ7PSTLPCUSZBVHKMO7S4EIFAJ4C
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ7PSTLPCUSZBVHKMO7S4EIFAJ4C
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/07 Aree/AFC/Velo-CE - Proposta conti categorie articolo - CLIENTE - v001.xlsx
  name: Velo-CE - Proposta conti categorie articolo - CLIENTE - v001.xlsx
  last_modified: 2026-10-26T13:34:09Z
versions:
  - { name: "Velo-CE - Proposta conti categorie articolo - CLIENTE - v001.xlsx", item_id: 01EFCYUZ7PSTLPCUSZBVHKMO7S4EIFAJ4C, last_modified: 2026-10-26T13:34:09Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-29T06:13:08Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, afc, piano-dei-conti, categorie, magazzino, cliente]
---

# Velo-CE · Proposta dei conti per le nuove categorie di registrazione degli articoli (CLIENTE)

## Riassunto

Proposta BlueAge per [[claudia-crippa]] (versione 1 del 26/10/2026, da rivedere con lei) dei conti da associare alle sette nuove categorie di registrazione degli articoli del nuovo Business Central di [[velo-ce]]: per ognuna su quali conti registrare acquisti, vendite e magazzino, partendo dal piano dei conti e dalle regole di oggi. Applica il modello contabile «per natura» orientato da Cristian il 26/10 ([[velo-ce-stato-progetto-03-decisioni-aperte]]).

## Punti chiave

- **Sette categorie**: RAW materie prime, COMP componenti comprati, PCK imballi ed etichette, SEMI semilavorati, FINISH prodotti finiti, RESALE merci per la rivendita, CONSUM materiali di consumo non a magazzino.
- **Regola proposta**: fatture d'acquisto e di vendita sugli stessi conti di oggi (acquisti per natura e per area, ricavi per area); il magazzino entra in contabilità a ogni movimento sul conto rimanenze della categoria, con contropartita automatica sul conto di variazione rimanenze della stessa classe: la variazione si forma mese per mese, senza il giroconto di fine anno.
- **Esempio provato** nella società di prova (solo anteprima): 100 kg di tubo a 2,50 €/kg generano la fattura su acquisti materie prime e, in automatico, rimanenze materie prime contro variazione rimanenze per 250 €.
- **Cosa si chiede a Claudia**: confermare o cambiare i conti per categoria nelle celle gialle; un foglio di domande per le scelte anche con il commercialista; fogli di controllo con il setup della società di prova.
- **Modificabilità**: i conti dei setup si possono cambiare in ogni momento per le registrazioni successive; non va cambiata la categoria di un articolo che ha già giacenza.
- **Alternativa**: conti di costo del venduto dedicati da riclassificare a fine anno; la proposta per natura evita la riclassifica.

## Numeri

- Nessun numero rilevante.

## Decisioni e azioni

- [ ] Far confermare a Claudia i conti delle nuove categorie di registrazione articolo (OP-47) ([[velo-ce-proposta-conti-categorie-articolo-cliente]])

## Versioni

- Velo-CE - Proposta conti categorie articolo - CLIENTE - v001.xlsx · 2026-10-26 · prima versione ingerita (letto il foglio Leggimi); cartella `Cristian/07 Aree/AFC/`
