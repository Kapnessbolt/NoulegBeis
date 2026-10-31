---
type: source-doc
source: sharepoint
family: velo-ce-checklist-finestra-di-rilascio-interno
current:
  item_id: 01EFCYUZ6J3Z66K5RK4FH3IYLL3FKXXVPM
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ6J3Z66K5RK4FH3IYLL3FKXXVPM
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/04 Partner e ambienti/Ambienti e rilasci/Velo-CE - Checklist finestra di rilascio - INTERNO - v002.xlsx
  name: Velo-CE - Checklist finestra di rilascio - INTERNO - v002.xlsx
  last_modified: 2026-09-27T18:32:52Z
versions:
  - { name: Velo-CE - Checklist finestra di rilascio - INTERNO - v002.xlsx, item_id: 01EFCYUZ6J3Z66K5RK4FH3IYLL3FKXXVPM, last_modified: 2026-09-27T18:32:52Z }
  - { name: Velo-CE - Checklist finestra di rilascio - INTERNO - v002.xlsx, item_id: 01EFCYUZ7SV6SW3MXQ3VD2XDOXE5BUVOXN, last_modified: 2026-09-27T18:32:52Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:31:42Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, business-central, rilasci, ambienti, so-smart, checklist, interno]
---

# Velo-CE · Checklist della finestra di rilascio (classi 3 e 4)

## Riassunto

Cartella di lavoro interna BlueAge (v002 del 27/09/2026, v001 del 25/09), non mostrabile al cliente. Traduce in controlli operativi la procedura interna di rilascio e ripristino PRR-0922 v004, per i rilasci di classe 3 (modifiche massive sui dati) e 4 (app ed esperienza) sul Business Central di Velo-CE. Ha quattro fogli: istruzioni, 10 prerequisiti una tantum (RL-P01…RL-P10), la checklist di finestra in otto fasi (dalla preparazione alla riattivazione o al rientro) e il registro da compilare per ogni finestra. Ogni riga cita il paragrafo della PRR e lo stato dell'informazione (verificato, dichiarato, da rilevare). Va tenuta allineata alla procedura esterna condivisa con So Smart ([[velo-ce-procedura-di-rilascio-condivisa-so-smart]]).

## Punti chiave

- **Tre documenti allineati**: PRR-0922 (interna, con ripristino e assunzioni), PS01 «Procedura di rilascio condivisa - SO SMART» (esterna), questa checklist (operativa).
- **Prerequisiti**: quota ambienti (1 Production + 3 sandbox, nessuno slot libero); sandbox copia di Production da liberare (Educational2906 e TestTemp1509 eliminabili, decide Stefano); utenza licenziata del cliente per sospendere e riattivare la coda processi (l'utenza BlueAge non scrive in BC); log modifiche su Articolo, distinte, setup magazzino e parametri di pianificazione; inventario delle integrazioni; domande a So Smart; foto delle impostazioni dell'Admin Center; prova generale di restore sul tenant BlueAge (ferma: il tenant BlueAge non ha un piano BC a pagamento); finestra standard da concordare con Stefano.
- **Controlli nati dalle letture del 25/09**: le voci della coda «So Smart» tornano in «Pronto» quando un utente entra in BC; So Smart aggiorna le sue app in Production di notte senza preavviso noto; il canale ordini scrive 24 ore su 24 tramite i due client dell'app Entra «CRM»; fasce fisse dei job So Smart da evitare (01:00-01:30, 07:00-07:30, lunedì 07:00-07:30, domenica 23:00-23:30).
- **Fasi della finestra**: prima (prova in sandbox su copia fresca, criteri di go/no-go, foto prima, avvisi a utenti, So Smart, gestore dei client «CRM», We Make Code per i portali e responsabile della fatturazione elettronica); apertura (nessuna sessione, sospensione dei 6 job So Smart e del flusso MMI); T0; esecuzione della sequenza provata; verifiche; go/no-go (propone Cristian, decide Stefano se serve lo scambio della produzione); riattivazione voce per voce con l'utenza proprietaria; rientro su tre strade (correzione mirata, restore in sandbox, scambio della produzione).
- **Decisioni interne**: se servisse un ripristino lo esegue So Smart (Cristian, 26/09); restore e rename restano temi interni, non se ne parla con So Smart né con il cliente (27/09).
- La voce di invio delle fatture elettroniche in uscita è già in sospeso e non va toccata.

## Numeri

- 10 prerequisiti, 8 fasi, circa 35 controlli di finestra, 16 campi di registro.
- 4 ambienti: 1 Production + 3 sandbox; finestra di aggiornamento Microsoft 20:00-06:00.
- Elenco app in Production: 124 app.
- Prova di restore: fasi PG-00…PG-06, verificate PG-00 e PG-02.

## Decisioni e azioni

- [ ] Chiudere i prerequisiti RL-P01…RL-P10 prima della prima finestra reale
- [ ] Chiudere le righe «DA RILEVARE» con le risposte di So Smart (Q10, Q11, Q12, Q17, Q24)
- [ ] Decidere con Stefano l'eliminazione di Educational2906 e TestTemp1509 per liberare uno slot sandbox
- [ ] Concordare con Stefano la finestra standard (giorno, ora, durata, reperibili)
- [ ] Attivare il log modifiche sulle tabelle toccate dai rilasci
- [ ] Individuare chi gestisce i due client dell'app «CRM»

## Versioni

- Velo-CE - Checklist finestra di rilascio - INTERNO - v002.xlsx · 2026-09-27 · prima versione ingerita (v002; la v001 è del 25/09)
