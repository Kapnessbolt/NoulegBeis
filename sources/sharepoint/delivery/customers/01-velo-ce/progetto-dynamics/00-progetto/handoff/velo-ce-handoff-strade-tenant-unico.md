---
type: source-doc
source: sharepoint
family: velo-ce-handoff-strade-tenant-unico
current:
  item_id: 01EFCYUZ2RDIVUAJPUQBF3SJU5LELKQZSG
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ2RDIVUAJPUQBF3SJU5LELKQZSG
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/00 Progetto/Handoff/handoff-2026-10-04-strade-tenant-unico.md
  name: handoff-2026-10-04-strade-tenant-unico.md
  last_modified: 2026-10-08T10:43:55Z
versions:
  - { name: handoff-2026-10-04-strade-tenant-unico.md, item_id: 01EFCYUZZMWFPWXVPJRVHYVI5IO4PBTNDU, last_modified: 2026-10-08T10:43:55Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:25:33Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [handoff, tenant-unico, storico, migrazione, conservazione, interno]
---

# Velo-CE · Handoff del 04/10/2026: strade verso il tenant unico, storico e criticità

## Riassunto

Handoff interno BlueAge di una chat del Project Velo-CE del 04/10/2026 su come portare Business Central nel tenant unico di Velo-CE (quello della posta, veloe.eu) garantendo la consultazione dello storico 2023-2026. La chat ha definito cinque strade, le ha messe in sequenza senza date e ha prodotto il deck per il cliente «Strade verso il tenant unico» v002 (11 slide), senza costi, pro e contro. Ha portato lo stato progetto alla 025.51 e preparato domande per So Smart e per i referenti interni. Il passo successivo è il documento su criticità, prerequisiti, pro e contro per strada, base della scelta del titolare.

## Punti chiave

- **Obiettivi sullo storico (Cristian)**: navigabile in BC almeno fino al bilancio 2026; parallelo dei due sistemi per almeno sei mesi del 2027; interrogazione dal 2023 con dettaglio completo; confronto per articolo almeno in Power BI con il raccordo dei codici; il taglio al 01/01/2027 è una scelta di pulizia, da confermare col commercialista; il data warehouse non è un prerequisito.
- **Le cinque strade**: 1 nuovo BC e il vecchio si spegne dopo il bilancio 2026; 2 come la 1 ma il vecchio resta acceso in sola consultazione con una licenza («coda lunga»); 3 il vecchio ambiente si trasferisce accanto al nuovo nel nuovo tenant; 4 due società nello stesso ambiente; 5 trasferimento subito e ricodifica graduale. Escluse senza citarle: ripresa dello storico registrato con rimappatura dei codici (non esiste uno strumento standard) e saldi mensili 2026.
- **Strada 6 «Essentials più app So Smart»**: produzione costruita sugli ordini di assemblaggio; giudicata «strada sporca» perché i dati finiscono in tabelle So Smart e complicano un futuro passaggio a Premium; da validare con la dimostrazione della call con So Smart del 06/10. Sul costo dello stock si avvicina a Premium, sul modello del pilota Lungo no.
- **Assistenza su Premium**: So Smart non la dà, EOS non interviene per quattro licenze, il cliente non vuole BlueAge: va trovato un partner terzo.
- **Saldi d'apertura (proposta BlueAge)**: apertura in due tempi, con partite aperte e giacenze alla partenza contro un conto transitorio e saldi patrimoniali definitivi a chiusura 2026; decide il commercialista.
- **Fatti documentali**: l'export del database produce un BACPAC su Azure Storage, al massimo 10 al mese, e non ricrea un BC funzionante; le tabelle SQL non corrispondono alle liste dei report (alternativa: estrazione una tantum o bc2adls); conservazione per 10 anni indipendente da BC e affidata al conservatore (atteso Able Tech IX-CE); il framework e-documents per l'Italia ha data «TBD»; le app di produzione EOS presuppongono Premium.
- **Punti aperti**: partner per l'assistenza Premium; chi esegue le rettifiche dei saldi; blocco in scrittura del vecchio BC dopo il taglio; amministrazione effettiva di veloe.eu (accesso fallito l'08/09); coordinamento della chiave articolo del flusso MMI; regola contro ordini persi o duplicati nel parallelo; perimetro dei dati alla partenza; IVC; fatturazione a cavallo d'anno; archivio Power BI come progetto a sé; raccordo dei codici non sempre 1:1; criteri di go-live e di rientro.

## Numeri

- Deck v002: 11 slide; sei tappe (preparazione, partenza, parallelo e chiusura 2026, bilancio 2026 approvato, spegnimento, dopo lo spegnimento) su quattro corsie.
- Coda lunga: licenza dichiarata a 69,19 euro al mese, più gli abbonamenti EOS sul Tenant ID.
- Domande a So Smart Q25-Q32; conservazione 10 anni; IX-FE mantiene i dati 45 giorni (90 via API).
- Stato progetto alla versione 025.51.

## Decisioni e azioni

- Decisione (Cristian, 04/10): coda lunga come strada autonoma; strada 3 tenuta; strade scartate non citate nel deck; il deck non contiene costi, pro, contro né raccomandazione.
- Decisione: destinatari del deck il titolare e l'amministrazione; condivisione con So Smart solo dopo il via libera del titolare, con una slide in più.
- [ ] Sistemare i file prodotti nelle cartelle, caricare i blocchi 025.51 nel Project e copiare le domande nei questionari
- [ ] Analisi delle criticità e documento su prerequisiti, pro e contro per strada (prima interno, poi per il cliente)
- [ ] Call con So Smart: dimostrazione della strada 6 e domande Q25-Q32 📅 2026-10-06
- [ ] Domande all'amministrazione e al commercialista su conservazione, registri, taglio, saldi d'apertura e fatture passive 2026 arrivate nel 2027
- [ ] Aprire nel registro [[velo-ce-open-point-interno]] le righe su strada, assistenza Premium, saldi d'apertura, registri, conservazione, abbonamenti EOS, archivio Power BI, strada 6

## Versioni

- handoff-2026-10-04-strade-tenant-unico.md · 2026-10-08 · prima versione ingerita; contenuto del 04/10/2026, data di modifica della riorganizzazione della cartella
