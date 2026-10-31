---
type: source-doc
source: sharepoint
family: velo-ce-articoli-codici-nuovi
current:
  item_id: 01EFCYUZ5P54ZT5Q7EKBEJV6JC3HOKGYDY
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ5P54ZT5Q7EKBEJV6JC3HOKGYDY
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/99 Project Claude (copia)/velo-ce-articoli-codici-nuovi-2026-10-15.md
  name: velo-ce-articoli-codici-nuovi-2026-10-15.md
  last_modified: 2026-10-29T16:14:34Z
versions:
  - { name: velo-ce-articoli-codici-nuovi-2026-10-15.md, item_id: 01EFCYUZ5P54ZT5Q7EKBEJV6JC3HOKGYDY, last_modified: 2026-10-29T16:14:34Z }
  - { name: velo-ce-articoli-codici-nuovi-2026-10-15.md, item_id: 01EFCYUZ3HHGI2R3AYBBBKGAVN7TSSHICY, last_modified: 2026-10-28T08:06:15Z }
also_at:
  - { web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/98 Share Team/Velo-CE - Contesto Claude per Leonardo - INTERNO - v001/velo-ce-articoli-codici-nuovi-2026-10-15.md", item_id: 01EFCYUZZ2MXZ7YHPSQZD35MRKA26N63HH }
status: active
partial: false
ingested_at: 2026-10-29T06:09:01Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, codifica, ripresa-dati, articoli, so-smart, interno]
---

# Velo-CE · Articoli con codici nuovi nel nuovo BC: fattibilità e impedimenti

## Riassunto

Analisi interna BlueAge del 15/10/2026 sera (versione 1, non mostrabile al cliente né a So Smart) sulla domanda di Cristian: nel nuovo BC di [[velo-ce]] (opzione 3, società nuova senza storico) si possono caricare solo articoli con i codici nuovi e solo una parte di quelli di oggi, mentre So Smart riprende saldi, partite aperte, banche, clienti e fornitori? Risposta: sì, dentro BC nessun impedimento è bloccante; i rischi veri sono fuori da BC (portale e flusso ordini, Veloce-CRM) e nella lettura alla lettera della frase di So Smart sui saldi «una volta chiuso il bilancio».

## Punti chiave

- **Il codice nuovo non è il costo grosso**: con la società nuova articoli, distinte, ordini aperti, listini e giacenze si ricaricano comunque; il codice nuovo aggiunge la tabella di raccordo vecchio → nuovo, che però non è sempre uno a uno (fusioni di accessori doppi, codici generici con merce sopra, bici Veloe oggi non di inventario, cambi di unità di misura).
- **Le partite aperte non toccano gli articoli**; eccezione possibile gli acconti legati agli ordini.
- **Fuori da BC**: il flusso ordini MMI usa il numero articolo come chiave e dall'8 gennaio il portale deve mandare i codici nuovi (altrimenti è bloccante); Veloce-CRM ricava la distinta di montaggio dal codice bici e può servire uno sviluppo; le tabelle di sostituzione di So Smart per Van Nicholas vanno tradotte.
- **Van Nicholas**: la decisione in vigore è «non si tocca»; proposta di creare i suoi articoli da zero con lo stesso codice; decide Stefano entro il 30/10.
- **Fiscale**: il valore d'apertura deve uguagliare le rimanenze di bilancio; la merce non portata va venduta, distrutta con le formalità previste o svalutata entro il 31/12, con un elenco preparato a novembre; rischio di doppio valore del magazzino in contabilità se So Smart non esclude i conti di magazzino dai saldi.
- **Divisione dei compiti**: So Smart anagrafiche clienti e fornitori, partite aperte, banche e saldi in due tempi; BlueAge articoli, varianti, distinte, modelli e tabella di raccordo; da decidere chi ricarica ordini aperti e listini.

## Numeri

- Estrazione di settembre: 1.112 articoli, 418 con giacenza, 669 a costo zero, 140 con distinta; perimetro minimo indicativo 659 articoli.
- 167 ordini di vendita con residuo (142 del 2026); 27 ordini d'acquisto aperti mai ricevuti; 25 ordini di assemblaggio aperti al 05/10.

## Decisioni e azioni

- Decisione di Cristian e Leonardo del 15/10: So Smart fa la ripresa dei saldi tranne i codici prodotto.
- [ ] Far decidere a Stefano se Van Nicholas entra nella ricodifica e il formato del codice bici 📅 2026-10-30 ([[velo-ce-articoli-codici-nuovi]])
- [ ] Preparare la tabella di raccordo vecchi → nuovi codici (NBC-147) 📅 2026-12-04 ([[velo-ce-articoli-codici-nuovi]])

## Versioni

- velo-ce-articoli-codici-nuovi-2026-10-15.md · 2026-10-28 · prima versione ingerita; cartella `Cristian/99 Project Claude (copia)/`
