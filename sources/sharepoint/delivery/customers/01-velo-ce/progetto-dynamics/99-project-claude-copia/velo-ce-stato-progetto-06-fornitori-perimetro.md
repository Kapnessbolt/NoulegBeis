---
type: source-doc
source: sharepoint
family: velo-ce-stato-progetto-06-fornitori-perimetro
current:
  item_id: 01EFCYUZ52Q6DWZOBUNRBKBIY2QMEV523Q
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ52Q6DWZOBUNRBKBIY2QMEV523Q
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Cristian/99 Project Claude (copia)/velo-ce-stato-progetto-06-fornitori-perimetro.md
  name: velo-ce-stato-progetto-06-fornitori-perimetro.md
  last_modified: 2026-10-28T08:06:17Z
versions:
  - { name: velo-ce-stato-progetto-06-fornitori-perimetro.md, item_id: 01EFCYUZ52Q6DWZOBUNRBKBIY2QMEV523Q, last_modified: 2026-10-28T08:06:17Z }
  - { name: velo-ce-stato-progetto-06-fornitori-perimetro.md, item_id: 01EFCYUZZAECEXU6XR6RDLODDRQ2ZDZBWV, last_modified: 2026-10-08T10:43:52Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-29T05:57:56Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, business-central, fornitori, so-smart, perimetro, responsabilita, rischi, interno]
---

# Velo-CE · Stato progetto, blocco 06 · Fornitori, perimetro, assunzioni e mappa dei fornitori

## Riassunto

Blocco 06 (§12-§13) dello stato progetto Velo-CE, interno BlueAge. Raccoglie ciò che si sa su So Smart e sugli altri fornitori (verificato e dichiarato), le assunzioni operative di lavoro SS1-SS9 e WM1, i dieci rischi tecnici da verificare prima di impegnare la quotazione, la ripartizione delle responsabilità fra BlueAge, So Smart, cliente e altri fornitori, la narrativa di relazione verso il cliente e il partner. Documenta l'impostazione della call con So Smart (prevista il 29/09, spostata e poi tenuta il 06/10), la razionalizzazione delle 54 app EOS decisa il 29/09, la possibile «strada 6» con la produzione su app So Smart, e chiude con la mappa dei fornitori e il loro rischio di continuità.

## Punti chiave

- **So Smart (verificato)**: ha creato il tenant nel 2021, ha delega GDAP, un amministratore globale locale permanente, rivende le sottoscrizioni Microsoft tramite EOS Online; nel tenant 54 app EOS (124 app in tutto, nessuna estensione per-tenant), «C\Lavoro» e Connettore WMS dentro So Smart Application; aggiorna le proprie app in produzione di notte, senza preavviso noto (05/08/2026).
- **So Smart (dichiarato)**: implementazione del 2023 ridotta a pacchetto più procedura guidata, senza analisi dei processi; il 23/09 dichiarava di non coprire Premium; **il 07/10, dopo la call del 06/10, garantisce app fiscali EOS, connettori (flusso MMI e API) e AMS anche in Premium, esclusa la configurazione della produzione che segue BlueAge**: conferma scritta da chiedere; restano da chiarire installazione delle app nel nuovo tenant, canale delle licenze, abbonamenti EOS sul nuovo tenant, SLA dell'AMS.
- **Stefano (23/09)**: mantiene So Smart su AMS e licenze; BlueAge si aggiunge su processi e configurazione, non subentra. Ricodifica ibrida per famiglia confermata (perimetro reale qualche centinaio di codici, non 1.100).
- **Assunzioni**: SS1 autonomia BlueAge sulla configurazione standard (la più fragile: serve un'utenza licenziata, i ruoli Entra non bastano); SS2 niente sviluppo sul codice So Smart; SS5 licenze via EOS con possibile acquisto diretto; SS6 l'estensione So Smart non blocca i cantieri (da verificare); SS7 installazione di app AppSource decisa dal cliente; SS8 Partner Access aperto a tutti i partner (verificato 25/09); SS9 edizione supportata delle app EOS non verificabile senza So Smart; WM1 We Make Code interviene a richiesta senza contratto.
- **Rischi tecnici**: modelli articolo «Inserimento rapido So Smart»; API So Smart che una ricodifica può rompere (incrocio oggetto-consumatore da fare con So Smart); gate della pagina 2500; governance dell'identità (il secondo fattore del tenant della posta è fuori dall'azienda: rischio di continuità più serio, la posta è il canale d'ordine principale); licenza; «C\Lavoro» da passare al criterio di ammissibilità; convivenza con l'app Subcontracting (cambio di processo da assemblaggio a produzione); due concessioni di accesso per BlueAge; automatismi So Smart in corsa (fermare i job non ferma chi scrive gli ordini).
- **Responsabilità**: BlueAge su processo, anagrafica, codifica, distinte, costificazione, setup standard, report Power BI, ricodifica e finestre di rilascio; So Smart su sviluppo AL, API, app EOS e loro aggiornamenti, AMS (anche Premium esclusa la produzione), eventuale ripristino; cliente su licenze, app AppSource, ambienti con BlueAge; We Make Code su Veloce-CRM, portale B2B ed etichettatura; società di Luigi Sacchi su posta, server e disegni; data entry da decidere.
- **Narrativa**: «l'azienda ha un ecosistema che funziona ma nessuno ne possiede il disegno d'insieme; quattro fornitori presidiano quattro pezzi; il valore di BlueAge è essere il punto in cui si guardano insieme». GDAP, accessi di So Smart e residui del 2023 si portano come governance, mai come irregolarità.
- **Call con So Smart**: obiettivo «allarghiamo il lavoro, non lo tagliamo»; fuori dalla call canone, governance, validazione Premium, richiesta di SUPER, ripristino. Proposta di notifica dei rilasci per classe con silenzio-assenso. Call del 29/09 spostata al 30/09, non tenuta; mail scritta per Stefano il 01/10; call tenuta il 06/10.
- **Razionalizzazione app EOS (29/09)**: criterio per tenere un'app (la usa Velo-CE, serve a un obbligo fiscale, o è una dipendenza di un'app che resta); IVC da sostituire con la valutazione fiscale standard italiana dopo la chiusura 2026; classificazione proposta: 7 in uso, 20 componenti e dipendenze, 11 da chiarire, 16 senza ruolo da disinstallare. Dal 01/10 la razionalizzazione passa in secondo piano.
- **Strada 6 (04/10)**: produzione sugli ordini di assemblaggio con l'app So Smart «Manufacturing and Assembly», senza Premium: in regola con la licenza ma non standard; vicina a Premium sul costo dello stock, non sul modello del pilota Lungo. Da aggiungere al deck solo se la dimostrazione regge.
- **Mappa dei fornitori**: So Smart (rischio medio, nessun contratto noto), We Make Code (rischio alto, tre processi centrali senza documentazione), società di Luigi Sacchi (rischio alto), marketing Van Nicholas Belgio (medio), Team System Fatture in Cloud per il conto lavoro (da valutare), Microsoft app Subcontracting (basso), fornitori di materie prime del telaio (basso, ordini per telefono o mail). Nessun fornitore ha un'evidenza contrattuale con il cliente.
- **Aggiornamenti dal 08/10 al 27/10** ([[velo-ce-stato-progetto-99-log-revisioni]]): §12.2 conferma scritta di So Smart (mail del 07/10, giunta il 09/10): licenza Premium rivenduta da So Smart a 30 € per utente al mese, configurazione della Produzione a BlueAge, supporto su tutto ciò che riguarda So Smart esclusa la «Produzione Avanzata», migrazione su un altro tenant fattibile con ticket; restano da chiarire edizione Premium delle app, SLA e abbonamenti EOS sul nuovo tenant. Riga del 15/10: risposta di So Smart al ticket e ripresa dei saldi a So Smart tranne gli articoli (§12.5 data entry e ricodifica).

## Numeri

- 54 app EOS su 124 in Production; classificazione 7 / 20 / 11 / 16.
- So Smart nel tenant: 8 persone e 5 tecnici GDAP fra gli utenti BC.
- Punti critici per la call: 53 in nove aree; criticità di configurazione: 36 temi, 31 incrociano oggetti EOS.
- Questionario PS02 v007: 24 domande, 12 ad alta priorità.
- Proposta di notifica: preavviso 5 giorni, risposta 3 giorni (bozza PS01).
- Canone So Smart/EOS: 768 euro al mese (fuori dalle riunioni).

## Decisioni e azioni

- 23/09 (Stefano): So Smart resta su AMS e licenze; ricodifica ibrida per famiglia.
- 25/09 (Cristian): temi di governance fuori dalla call, nel registro dedicato.
- 27/09 (Cristian): SUPER non si chiede; il ripristino non si nomina con So Smart.
- 29/09: razionalizzazione delle app EOS con mandato di Stefano e Claudia; canone fuori; IVC da sostituire dopo la chiusura 2026 con il commercialista.
- 29/09 (Cristian): l'app «CRM» esce dal documento sulle app So Smart (non è di So Smart).
- 01/10 (Cristian): la mail per So Smart non promette nulla sul ruolo di So Smart e non chiede chi coinvolgere; kit e questionario da rifare più snelli.
- [ ] Ottenere da So Smart conferma scritta della copertura in Premium (app fiscali, connettori, AMS) e lo SLA dell'AMS.
- [ ] Fissare il confine fra BlueAge e So Smart sulla configurazione non di produzione nel nuovo tenant.
- [ ] Chiarire la ragione sociale di So Smart e il rapporto con EOS Online.
- [ ] Rilevare contratti e perimetri di We Make Code, società di Luigi Sacchi e Fatture in Cloud.
- [ ] Classificare ogni intervento anche per fornitore impattato e sequenziare quelli che attraversano due contratti.

## Versioni

- velo-ce-stato-progetto-06-fornitori-perimetro.md · 2026-10-08 · prima versione ingerita (stato progetto 025.66); data di modifica della riorganizzazione della cartella
- velo-ce-stato-progetto-06-fornitori-perimetro.md · 2026-10-28 · stato progetto 025.109 del 27/10; conferma scritta di So Smart e riga del 15/10 (differenze ricavate dal log revisioni, blocco non riletto per intero); copia della cartella in `Cristian/`

