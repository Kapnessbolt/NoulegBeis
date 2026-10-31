---
type: source-doc
source: sharepoint
family: velo-ce-procedura-rilascio-ripristino
current:
  item_id: 01EFCYUZ4RI5VDEVDAURFIZZKE4SVN2LII
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ4RI5VDEVDAURFIZZKE4SVN2LII
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/99 Project Claude (copia)/velo-ce-procedura-rilascio-ripristino-2026-09-22.md
  name: velo-ce-procedura-rilascio-ripristino-2026-09-22.md
  last_modified: 2026-10-08T10:43:53Z
versions:
  - { name: velo-ce-procedura-rilascio-ripristino-2026-09-22.md, item_id: 01EFCYUZ65RXRKSPMBORFYWBVYZIOCXIUJ, last_modified: 2026-10-08T10:43:53Z }
  - { name: velo-ce-procedura-rilascio-ripristino-2026-09-22.md, item_id: 01EFCYUZ5K2FUQZDBRGVHIXP6PZIXGEQZD, last_modified: 2026-10-28T08:06:16Z }
also_at:
  - { web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/98 Share Team/Velo-CE - Contesto Claude per Leonardo - INTERNO - v001/velo-ce-procedura-rilascio-ripristino-2026-09-22.md", item_id: 01EFCYUZZLYVEQQSDPNJHKJFEE7BLVY5YT }
status: active
partial: false
ingested_at: 2026-10-22T13:25:37Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, business-central, rilascio, restore, ambienti, governance, interno]
---

# Velo-CE · Procedura di rilascio in produzione e strade di rientro (PRR-0922)

## Riassunto

Nota interna BlueAge (sigla PRR-0922, v005 del 27/09/2026, prima versione del 22/09), non mostrabile al cliente. Definisce come si rilasciano in produzione le modifiche al Business Central di Velo-CE e come si torna indietro se qualcosa va storto. La tesi è che il backup non protegge un rilascio: lo protegge una finestra di rilascio a sistema fermo, con «foto prima», sandbox di prova e go/no-go scritto. Classifica i rilasci in quattro classi, elenca i prerequisiti mancanti, cosa fermare e riaccendere (job So Smart, flusso MMI degli ordini, client esterni) e tre strade di rientro con un runbook per lo scambio della produzione. È il prerequisito operativo di ogni intervento massivo (ricodifica, sistema di rifornimento, distinte del telaio, bonifica costi).

## Punti chiave

- **Principi**: sandbox prima, sempre; foto prima di ogni modifica; finestra a sistema fermo per le classi 3 e 4; punto di ripristino (T0) annotato; go/no-go su criteri scritti prima; si riattiva solo ciò che era attivo al T0.
- **Quattro classi di rilascio**: 1 visibilità e personalizzazione (senza finestra); 2 setup e parametri puntuali (foto e sandbox); 3 modifiche massive sui dati (finestra completa, foto obbligatoria, sandbox su copia fresca); 4 app, estensioni ed esperienza, compreso il passaggio a Premium (finestra completa).
- **Tre strade di rientro**: R1 correzione mirata dalla foto prima (preferita); R2 restore di Production in una sandbox e riparazione; R3 scambio della produzione, solo dentro la finestra e prima di riaprire, su decisione del titolare. Oltre 28 giorni resta solo R1.
- **Prerequisiti mancanti**: sapere chi ha il set di autorizzazioni per backup/restore; uno slot sandbox libero (quota piena: 1 produzione + 3 sandbox, due sandbox di test eliminabili su decisione del titolare); log modifiche attivo; risposte di So Smart sulla sospensione dei job.
- **Trappole**: i job So Smart (sei «SOSMART», dispatcher per fasce) tornano «Pronto» da soli nella sessione di chi entra in BC; il canale ordini B2B lavora 24 ore su 24, con due client esterni che scrivono gli ordini nel flusso MMI attraverso un'app Entra «CRM» con l'identità del titolare.
- **Fasce da evitare** per la finestra: 01:00-01:30, 07:00-07:30, lunedì 07:00-07:30, domenica 23:00-23:30.
- Gli aggiornamenti delle app fatti da So Smart (es. 05/08/2026 di notte, senza preavviso) sono rilasci di classe 4 esterni: preavviso reciproco da concordare (Q09).
- **Decisione 26-27/09**: se servisse, il restore lo esegue So Smart; ripristino e strade di rientro sono un tema interno, da non portare al cliente né a So Smart per non creare allarmismi; la copertura passa dall'allineamento con So Smart sulle date dei rilasci (PS01).
- Strumento operativo collegato: checklist della finestra di rilascio (RL03); tre documenti da tenere allineati: PRR-0922 interna, PS01 per So Smart, checklist.
- Prova generale sul tenant BlueAge (PG-00…PG-06): PG-00 e PG-02 verificati il 25/09; ferma perché il tenant BlueAge non ha un piano BC a pagamento.

## Numeri

- Restore: al massimo 10 per ambiente al mese; punto nel tempo fino a 28 giorni prima; produzione oltre quota da rientrare entro 30 giorni.
- Job: sei job So Smart ogni 15-60 minuti; «Esegui movimenti flusso MMI» ogni 2 minuti; client esterno Python ogni 60-95 minuti per 24 ore.
- Production alla versione 28.5, aggiornamento major a 29.0 entro il 01/03/2027; finestra di aggiornamento Microsoft 20:00-06:00.
- 10 app EOS con aggiornamento disponibile al 25/09; 124 app installate in Production.
- Export database (BACPAC): massimo 10 al mese, non è una strada di rientro.

## Decisioni e azioni

- 26/09 (Cristian): il restore, se servisse, lo esegue So Smart.
- 27/09 (Cristian): strade di rientro e ripristino restano interne.
- [ ] RL-P03: assegnare il set backup/restore all'utenza che esegue il restore.
- [ ] RL-P02: liberare uno slot sandbox (decide il titolare).
- [ ] RL-P05: attivare il log modifiche su articolo, distinte, setup magazzino, SKU e parametri di pianificazione (A15).
- [ ] RL-P07: inviare le domande a So Smart su sospensione dei job, restore e rename (insieme a R11).
- [ ] RL-P06: inventario delle integrazioni da fermare in finestra (BlueAge, So Smart, We Make Code).
- [ ] RL-P10: concordare con il titolare una finestra standard (giorno, ora, durata, reperibili).
- [ ] Prima di ogni finestra avvisare utenti, So Smart, We Make Code, gestori dei client «CRM» e la referente della fatturazione elettronica.
- Nessuna finestra di classe 3 o 4 a ridosso dell'aggiornamento Microsoft di ottobre (2026 release wave 2).

## Versioni

- velo-ce-procedura-rilascio-ripristino-2026-09-22.md · 2026-10-08 · prima versione ingerita (v005 del 27/09/2026); data di modifica della riorganizzazione della cartella
