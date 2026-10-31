---
type: source-doc
source: sharepoint
family: velo-ce-registro-temi-di-governance-interno
current:
  item_id: 01EFCYUZ2DGKPVEMEBNFAZN2TYHMIFYK3V
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ2DGKPVEMEBNFAZN2TYHMIFYK3V
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/04 Partner e ambienti/Governance e accessi/Velo-CE - Registro temi di governance - INTERNO - v002.xlsx
  name: Velo-CE - Registro temi di governance - INTERNO - v002.xlsx
  last_modified: 2026-10-04T10:33:22Z
versions:
  - { name: Velo-CE - Registro temi di governance - INTERNO - v002.xlsx, item_id: 01EFCYUZ2DGKPVEMEBNFAZN2TYHMIFYK3V, last_modified: 2026-10-04T10:33:22Z }
  - { name: Velo-CE - Registro temi di governance - INTERNO - v002.xlsx, item_id: 01EFCYUZ7NEVGECNAS6VAYGKM3M3AROGWF, last_modified: 2026-10-04T10:33:22Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:31:42Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, business-central, governance, accessi, sicurezza, so-smart, interno]
---

# Velo-CE · Registro dei temi di governance del tenant

## Riassunto

Registro interno BlueAge (v002, prima stesura 25/09/2026, aggiornato al 04/10), non mostrabile al cliente né a So Smart. Raccoglie 22 temi di governance del tenant Microsoft di Velo-CE (identità, permessi delle app, accessi del partner, tracciabilità, dati) emersi durante le rilevazioni e tenuti fuori dal filone principale per decisione di Cristian del 25/09: sarà la base di un filone di progetto dedicato. Per ogni tema: cosa si sa, certezza, evidenze, perché conta, proposta, chi decide, priorità e se tocca anche i rilasci. Regola di comunicazione: con Stefano rilievo di governance con i dati; con So Smart domanda neutra, mai accusa.

## Punti chiave

- **Identità (Alta)**: gli ordini automatici entrano con l'identità personale del titolare, amministratore globale, tramite l'app Entra «CRM» usata da due client esterni; la stessa utenza è proprietaria dei job e usata per tutto. Proposta: separare utenza personale, utenza di amministrazione con MFA e utenze o app tecniche per integrazioni e job.
- **App e permessi (Alta)**: l'app «CRM» ha permessi applicativi di gestione degli ambienti nell'Admin Center con consenso concesso; i segreti sono in mano a terzi non identificati. Proposta: revocare dopo conferma con il fornitore del client. Segreti in scadenza fra marzo e settembre 2027 senza responsabile noto.
- **Partner (Media)**: So Smart ha un account amministratore globale permanente indipendente dalla delega GDAP, un'app autorizzata sull'Admin Center attiva di notte, un'app service-to-service abilitata in BC, l'aggiornamento Power BI con un proprio account, autorizzazioni EOS proprie; il cliente non vede le app installate (pagina 2500 chiusa); Production accetta l'accesso di tutti i partner senza gruppo di sicurezza.
- **Dati (Media)**: lo strumento PDA modifica dati contabili registrati; proposta di tenerlo solo per So Smart su richiesta scritta dell'amministrazione, esportando il log prima del taglio e preferendo storni e documenti correttivi standard.
- **Altro**: utenze condivise e nessuna profilazione (magazzino e assemblaggio senza utenza nominale); utenza BlueAge con ruolo di amministratore BC nonostante il nome «reader»; log di accesso brevi; log dell'interfaccia MMI fermo dal 27/08/2026; tenant creato dal partner senza dominio proprio (proposta veloe.eu o vannicholas.com); job in errore da oltre due anni.

## Numeri

- 22 temi aperti: 3 alta, 12 media, 7 bassa priorità; 8 toccano anche i rilasci.
- Per area: Partner 8, App e permessi 5, Identità 4, Tracciabilità 2, Dati 1, Tenant 1, Igiene 1.
- App «CRM»: 25 token al giorno; 3 segreti in scadenza (marzo, giugno, settembre 2027).
- Log MMI: 1,43 milioni di righe storiche, circa 478 MB.
- PDA: 7 richieste nel 2026 (23/01, 13/05, 14/07, 31/08).
- Tenant creato il 19/11/2021.

## Decisioni e azioni

- Decisione (Cristian, 25/09/2026): i temi di governance escono dal filone principale e vanno in questo registro.
- [ ] Portare a Stefano i temi ad alta priorità (identità del canale ordini, app «CRM», utenza personale usata per tutto)
- [ ] Chiedere a So Smart, con domande neutre, uso dell'app autorizzata e dell'accesso notturno, dell'app service-to-service e chi apre la pagina 2500
- [ ] Nominare un responsabile per la scadenza dei segreti dell'app «CRM» (prima scadenza marzo 2027)
- [ ] Spostare l'aggiornamento Power BI su un'utenza del cliente
- [ ] Leggere con l'utenza del titolare ruolo e ultimo accesso degli account So Smart e scadenza della delega GDAP

## Versioni

- Velo-CE - Registro temi di governance - INTERNO - v002.xlsx · 2026-10-04 · prima versione ingerita (v002 del 27/09, aggiornata il 04/10 su GOV-14)
