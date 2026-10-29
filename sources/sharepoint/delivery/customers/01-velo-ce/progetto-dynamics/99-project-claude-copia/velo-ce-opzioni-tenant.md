---
type: source-doc
source: sharepoint
family: velo-ce-opzioni-tenant
current:
  item_id: 01EFCYUZ7L2N2XOUHLCVHKKBZQED3OSV4J
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ7L2N2XOUHLCVHKKBZQED3OSV4J
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/99 Project Claude (copia)/velo-ce-opzioni-tenant-2026-10-09.md
  name: velo-ce-opzioni-tenant-2026-10-09.md
  last_modified: 2026-10-28T08:06:15Z
versions:
  - { name: velo-ce-opzioni-tenant-2026-10-09.md, item_id: 01EFCYUZ7L2N2XOUHLCVHKKBZQED3OSV4J, last_modified: 2026-10-28T08:06:15Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-29T06:09:01Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, tenant, migrazione, premium, so-smart, interno]
---

# Velo-CE · Quattro opzioni per portare Business Central nel tenant unico

## Riassunto

Analisi interna BlueAge del 09/10/2026 (versione 1, non mostrabile al cliente né a So Smart) delle quattro opzioni per portare Business Central di [[velo-ce]] dal tenant di So Smart al tenant del cliente, con verifiche su Microsoft Learn, criteri validati da Cristian, analisi per opzione, tabella di confronto e filtro per il ticket a So Smart. Dal 20/10 il tenant di destinazione è `velo-ce.eu` e non più `veloe.eu`: l'analisi resta valida. Raccomandava l'opzione 4 con la 3 come ripiego; il 15/10 Cristian ha confermato l'opzione 3, rinviando alla primavera 2027 la scelta sul dopo-bilancio.

## Punti chiave

- **Le opzioni**: 1 porting e riconfigurazione sul posto; 2 porting e due società; 3 ambiente nuovo con il vecchio da So Smart fino al bilancio 2026 (3a spegnimento, 3b consultazione a pagamento); 4 ambiente nuovo e storico in una sandbox copiata e trasferita nel tenant unico, più l'export del database.
- **Fatti Microsoft Learn**: si può trasferire anche una sandbox, ma lo fa un amministratore interno e non la delega del partner; su app e abbonamenti ISV nel trasferimento Learn non dice nulla; da una sandbox non si esporta il database; l'esperienza Premium è per società e gli utenti Essentials non entrano in una società Premium; quota di 1 produzione e 3 sandbox per tenant; il nome della società non si cambia.
- **Criteri**: tre cancelli (storico e obblighi di legge, rischio sull'avvio dell'8 gennaio, fiscale di passaggio) e sei criteri di peso (pulizia, costi, lavoro, integrazioni e Power BI, reversibilità, dipendenze).
- **Giudizio**: la 1 è la più economica ma lascia codici vecchi e nuovi mescolati (sconsigliata); la 2 tiene storico e confronto vicini ma mette il cambio di tenant in pieno 2026; la 3 è la più sicura per l'avvio ma debole dopo il bilancio; la 4 unisce l'avvio sicuro al tenant unico dopo il bilancio.
- **Ticket a So Smart**: opzioni 2, 3 e 4, con 3 e 4 presentate come un ambiente nuovo con due varianti per il dopo-bilancio; prima allineare Stefano, perché le opzioni 3 e 4 spengono il tenant di So Smart.

## Numeri

- Licenza in consultazione 69,19 €/mese (dichiarato); differenza Premium-Essentials circa 26 €/mese per utente; ambiente di produzione aggiuntivo non a listino (stime non ufficiali 230-300 al mese).
- Spazio: 80 GB più 2 GB per licenza Essentials e 3 GB per Premium.

## Decisioni e azioni

- Raccomandazione del 09/10: opzione 4, con la 3 come ripiego; superata dalla conferma dell'opzione 3 del 15/10 ([[velo-ce-stato-progetto-03-decisioni-aperte]]).

## Versioni

- velo-ce-opzioni-tenant-2026-10-09.md · 2026-10-28 · prima versione ingerita; cartella `Cristian/99 Project Claude (copia)/`
