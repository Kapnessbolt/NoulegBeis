---
type: source-doc
source: sharepoint
family: velo-ce-criticita-di-configurazione-per-macroarea
current:
  item_id: 01EFCYUZZYQPOCJSFOABDZ6FF2I2AE47U3
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZZYQPOCJSFOABDZ6FF2I2AE47U3
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/04 Partner e ambienti/App EOS/Velo-CE - Criticità di configurazione per macroarea - v004.xlsx
  name: Velo-CE - Criticità di configurazione per macroarea - v004.xlsx
  last_modified: 2026-09-28T15:31:54Z
versions:
  - { name: Velo-CE - Criticità di configurazione per macroarea - v004.xlsx, item_id: 01EFCYUZ3BKNERSEK2DBFLLRUUHRAMX6YS, last_modified: 2026-09-28T15:31:54Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:31:42Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, business-central, eos, so-smart, configurazione, rischi, rilasci]
---

# Velo-CE · Criticità di configurazione per macroarea

## Riassunto

Bozza v004 del 28/09/2026, formulata per essere condivisa con Velo-CE e So Smart (senza nomi di utenti né codici interni). Elenca 33 temi di configurazione standard di Business Central che incrociano le app EOS/So Smart, raggruppati in 8 macroaree e 7 aree di progetto, con quanto rilevato, il grado di certezza, perché è critico e le domande del questionario tecnico per So Smart (Q01-Q24). L'ordine è di urgenza secondo BlueAge: prima ciò che va chiarito prima del primo rilascio con modifiche massive sui dati. Le prime cinque macroaree sono l'elenco iniziale, le ultime tre un completamento proposto.

## Punti chiave

- **M5 Code job (Alta)**: sei voci «So Smart» e il flusso MMI girano ogni 2 minuti, 15 minuti, ora o a orari fissi; non si sa cosa esegua ogni fascia; chi riattiva una voce ne diventa proprietario; il 25/09 le voci sono tornate «Pronto» all'accesso di un utente.
- **M4 API e integrazioni (Alta)**: l'unico canale automatico verificato è il flusso MMI SALES, che crea ogni giorno ordini di vendita usando il numero articolo di BC come chiave, senza tabella di traduzione: una ricodifica non coordinata lo romperebbe. Dei 25 servizi web EOS non si sa chi li chiami; uno punta a un oggetto che non esiste più.
- **M1 Anagrafica prodotti (Alta)**: ricodifica per famiglia (Van Nicholas invariato, nuovi codici per bici Veloe e accessori) e riallineamento del Sistema di rifornimento sono modifiche massive; la rinomina standard non aggiorna le tabelle EOS non collegate. Da decidere con Velo-CE il modello del colore (variante o codice) e il rifacimento delle etichette (prodotte da Veloce-CRM).
- **M6 App ed estensioni EOS (Alta)**: 54 app EOS, compatibilità con Premium da chiudere prima del cambio di esperienza; eventi intercettati non noti; Production passa alla 29.0 entro il 01/03/2027.
- **M8 Ambienti, test e rilasci (Alta)**: nessuno slot sandbox libero; manca una procedura di rilascio concordata con referenti; ambienti di test di Veloce-CRM e dei portali B2B e B2C non noti; log modifiche non letto.
- **M7 Pianificazione e produzione Premium (Alta)**: nessun metodo di riordino popolato, il piano non propone nulla; il cambio a Premium riguarda tutti gli utenti insieme; il role center So Smart nasconde Magazzino e Produzione.
- **M3 Metodi di costo (Alta)**: il metodo di costing non si cambia su articoli con movimenti, va deciso per famiglia prima della ricodifica; categorie di registrazione parziali.
- **M2 Distinte basi (Media)**: assemblaggio in uso; da giugno 2026 il portapacchi AMFR entra con rettifiche positive invece che con ordini di assemblaggio (carico senza consumo componenti né costo).

## Numeri

- 33 temi, 15 ad alta rilevanza, 22 con parti dichiarate o da rilevare; 29 temi toccano oggetti EOS.
- 54 app EOS, 5.254 oggetti (595 estensioni di tabella, 1.093 estensioni di pagina), 17 app con dati.
- Distinte: 1.263 righe, circa 140 codici con distinta, 571 ordini di assemblaggio registrati.
- 669 codici a costo zero in un'estrazione di inizio settembre (dichiarato).
- Flusso MMI: 25 flussi configurati, solo SALES in uso dal 05/2023; ultimo movimento 26.809 al 24/09.
- 15 aggiornamenti disponibili in Production, 10 su app EOS; Production 28.5, passaggio a 29.0 entro il 01/03/2027.

## Decisioni e azioni

- [ ] Ottenere da So Smart le risposte alle domande ad alta priorità del questionario (Q01-Q24) prima del primo rilascio massivo
- [ ] Decidere con Velo-CE il modello del colore (variante o codice) e il metodo di costing per famiglia
- [ ] Coordinare la ricodifica con chi gestisce il sistema esterno del canale ordini, oppure affidarla a un mapping
- [ ] Liberare uno slot per la sandbox copia di Production e isolare le integrazioni nella copia
- [ ] Attivare il log modifiche prima dei rilasci con modifiche massive
- [ ] Chiarire chi registra le rettifiche positive su AMFR

## Versioni

- Velo-CE - Criticità di configurazione per macroarea - v004.xlsx · 2026-09-28 · prima versione ingerita
