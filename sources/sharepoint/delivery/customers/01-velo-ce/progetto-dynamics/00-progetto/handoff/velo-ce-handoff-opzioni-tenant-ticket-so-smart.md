---
type: source-doc
source: sharepoint
family: velo-ce-handoff-opzioni-tenant-ticket-so-smart
current:
  item_id: 01EFCYUZYEADPCEISLARAJLP4BSYHPMUX4
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZYEADPCEISLARAJLP4BSYHPMUX4
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/00 Progetto/Handoff/handoff-2026-10-09-opzioni-tenant-ticket-so-smart.md
  name: handoff-2026-10-09-opzioni-tenant-ticket-so-smart.md
  last_modified: 2026-10-28T08:06:22Z
versions:
  - { name: handoff-2026-10-09-opzioni-tenant-ticket-so-smart.md, item_id: 01EFCYUZ4COZ2MRTOTFZFJ56QDMQYMCEAS, last_modified: 2026-10-28T08:06:22Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-29T06:06:44Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [handoff, velo-ce, tenant, so-smart, migrazione, interno]
---

# Velo-CE · Handoff: quattro opzioni per portare BC nel tenant Velo-CE e ticket a So Smart (09/10)

## Riassunto

Handoff interno del 09/10/2026 dalla chat sul piano attività del nuovo ambiente: analizzare le quattro opzioni per portare Business Central di [[velo-ce]] dal tenant di So Smart al tenant del cliente e preparare il ticket a So Smart per farsele quotare. È la base dell'analisi [[velo-ce-opzioni-tenant]]. Calendario di riferimento: scelta entro il 30/10, saldi al 01/01/2027, avvio R1 l'08/01/2027.

## Punti chiave

- **Le quattro opzioni**: 1 porting e riconfigurazione sul posto; 2 porting e due società (storica e nuova); 3 ambiente nuovo con il vecchio lasciato a So Smart fino al bilancio 2026; 4 ambiente nuovo con lo storico in una sandbox trasferita, più l'export del database.
- **Fatti**: So Smart ha dichiarato il 07/10 che garantisce app fiscali, AMS e connettori anche in Premium, con la configurazione della produzione a BlueAge; non confermati installazione delle app nel nuovo tenant, canale delle licenze, abbonamenti EOS sul nuovo Tenant ID, SLA.
- **Vincoli tecnici (documentali)**: il trasferimento di ambiente fra tenant lo fanno amministratori interni dei due tenant, non la delega di So Smart; non passano utenti e licenze; le sottoscrizioni non si spostano; l'export del database si fa solo da produzione; il nome della società non si cambia, solo il nome visualizzato.
- **Ticket a So Smart**: due parti (domande di fattibilità comuni e quotazione per opzione delle sole attività So Smart), non più di tre opzioni, allineamento con Stefano prima dell'invio; canone e governance fuori dal ticket.
- **Aperti**: l'opzione 1 contrasta con codici nuovi senza misto; l'opzione 2 anticipa il cambio di piattaforma nel 2026; le opzioni 3 e 4 hanno due BC verso lo SdI fino al 15/01 e doppi costi finché il vecchio resta acceso.

## Numeri

- Canone So Smart circa 768 €/mese; licenza per tenere il vecchio BC in consultazione circa 69 €/mese (dichiarato).
- Piano attività: 185 righe NBC.

## Decisioni e azioni

- Decisi: tenant di destinazione (allora `veloe.eu`, dal 20/10 `velo-ce.eu`) e Premium; le quattro opzioni da analizzare; configurazione della produzione a BlueAge.

## Versioni

- handoff-2026-10-09-opzioni-tenant-ticket-so-smart.md · 2026-10-28 · prima versione ingerita; cartella `Cristian/00 Progetto/Handoff/`; dettagli tecnici di accesso agli ambienti omessi
