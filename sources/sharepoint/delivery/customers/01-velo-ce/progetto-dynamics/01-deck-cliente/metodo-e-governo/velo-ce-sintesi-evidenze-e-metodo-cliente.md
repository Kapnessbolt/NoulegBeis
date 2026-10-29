---
type: source-doc
source: sharepoint
family: velo-ce-sintesi-evidenze-e-metodo-cliente
current:
  item_id: 01EFCYUZ4Z2ECSFY22O5BYT3WXEB3YLNT4
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ4Z2ECSFY22O5BYT3WXEB3YLNT4
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/01 Deck cliente/Metodo e governo/Velo-CE - Sintesi evidenze e metodo - CLIENTE - v001.pdf
  name: Velo-CE - Sintesi evidenze e metodo - CLIENTE - v001.pdf
  last_modified: 2026-09-28T12:26:28Z
versions:
  - { name: Velo-CE - Sintesi evidenze e metodo - CLIENTE - v001.pdf, item_id: 01EFCYUZYBTTYA67TK3JHZLRWW3X3YXHSU, last_modified: 2026-09-28T12:26:28Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:25:42Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [business-central, rilevazione, metodo, governo-progetto, rilasci, criticita]
---

# Velo-CE · Dove siamo: evidenze e metodo di lavoro

## Riassunto

Sintesi BlueAge in 4 pagine (versione 1, fine settembre 2026) della rilevazione di settembre su Business Central di Velo-CE: processi in sede (reparto telai e giro dell'ordine, dal rilievo del 15/09 e dalla giornata del 21/09), sistema letto in sola lettura e prove su un ambiente BlueAge con un ciclo completo ordine → bici sul telaio Lungo. Tesi: Business Central ha già le funzioni che servono (pianificazione, distinte, costo del prodotto) ma non sono configurate. Il documento elenca sei evidenze, mappa i sistemi intorno a Business Central e chi li presidia, ordina le criticità in sette aree con il primo passo per ciascuna e fissa un metodo di lavoro che protegge l'operatività.

## Punti chiave

- **Sei evidenze**: la pianificazione non propone nulla (nessun metodo di riordino); l'anagrafica non segue il processo (bici montate in casa come acquistate, materie prime del telaio senza codice); distinte parziali e carichi con rettifiche; costo del prodotto incompleto (dazi, trasporti, lavorazioni esterne fuori, stock ex Accell valorizzato in blocco); il canale automatico degli ordini usa il codice articolo, quindi ogni ricodifica va coordinata; le app del partner lavorano di continuo.
- **Sistemi intorno a Business Central**: import ordini So Smart ogni 2 minuti; Veloce-CRM e portale B2B di We Make Code (assemblaggio, post-vendita, etichette) via API So Smart; ordini via mail inseriti a mano (Van Nicholas); connettore Shopify installato e non collegato; Power BI con sorgente diretta; Fatture in Cloud per il conto lavoro, fuori da BC; webshop Van Nicholas senza integrazione.
- **Chi presidia**: So Smart (licenze, assistenza, app, API, automatismi), We Make Code (Veloce-CRM, portale B2B), fornitore IT (posta e server), marketing Van Nicholas (configuratore e webshop), Team System (Fatture in Cloud), BlueAge (processi e configurazione standard). Ogni intervento va letto anche per fornitore toccato.
- **Sette aree in ordine di lavoro**: anagrafica e codifica (estrazione articoli, regole, tabella vecchio → nuovo codice), distinte (dal telaio Lungo), pianificazione (obiettivo numero uno: materiali sempre disponibili; parametri su tre articoli pilota), costo del prodotto (metodo di costo per famiglia prima della ricodifica), integrazioni e automatismi (mappa con Stefano, domande scritte a So Smart), app del partner (tenuta in Premium da confermare), ambienti e rilasci (quota piena, serve una copia di produzione).
- **Metodo**: prima lo standard (nessuna modifica al codice delle app So Smart); prima la prova su una copia recente di produzione; rilasci per tipo (piccoli in registro condiviso, massivi con preavviso, finestra dedicata e automatismi sospesi); dopo il rilascio BlueAge segue le segnalazioni, poi assistenza ordinaria So Smart.
- **Ruoli**: Velo-CE decide codifica, priorità, rilasci, ambienti e licenze e fornisce dati; BlueAge disegna, configura, prova, rilascia e segue; So Smart licenze, assistenza, app e aggiornamenti coordinati, sviluppi quotati prima; We Make Code quando un intervento tocca i suoi sistemi.
- **Premium**: la direzione è Premium; prima si configura ciò che funziona già in Essentials (codifica, distinte, pianificazione, costi), il cambio di esperienza dopo una prova in copia. In questa versione So Smart resta il partner per licenze e assistenza.

## Numeri

- Circa 670 codici a costo zero nell'estrazione di inizio settembre (da confermare).
- Circa 140 articoli con distinta di assemblaggio, 1.263 righe, 571 assemblaggi registrati; nessuna distinta completa del telaio.
- Dazi circa 50.000 euro e stock ex Accell circa 150.000 euro fuori dal costo o valorizzati in blocco (da confermare).
- 54 app So Smart/EOS (17 con dati propri) e 70 app Microsoft; automatismi ogni 15 minuti e ogni 2 minuti, 6 voci schedulate.
- Ambienti: produzione e tre di prova, quota piena.

## Decisioni e azioni

- Proposta di metodo: prima lo standard, ogni modifica provata in copia di produzione, rilasci annunciati per tipo.
- [ ] Completare con Stefano la mappa dei sistemi: quale sistema alimenta il canale ordini automatico e chi lo gestisce
- [ ] Inviare a So Smart le domande tecniche scritte su automatismi e tenuta delle app in Premium
- [ ] Decidere con Velo-CE quale ambiente di prova sostituire con una copia di produzione e concordare con So Smart la procedura di rilascio
- [ ] Estrazione completa degli articoli, regole di codifica e tabella vecchio → nuovo codice
- [ ] Parametri di pianificazione sui tre articoli pilota, poi per famiglia
- [ ] Decidere il metodo di costo per famiglia prima della ricodifica

## Versioni

- Velo-CE - Sintesi evidenze e metodo - CLIENTE - v001.pdf · 2026-09-28 · prima versione ingerita (versione 1)
