---
type: source-doc
source: sharepoint
family: velo-ce-verbale-strada-premium-tenant-unico
current:
  item_id: 01EFCYUZYFPZMJ7TLKVJCLR5IIJIY6HEPE
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZYFPZMJ7TLKVJCLR5IIJIY6HEPE
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/99 Project Claude (copia)/verbali/velo-ce-verbale-260930-1754-strada-premium-tenant-unico.md
  name: velo-ce-verbale-260930-1754-strada-premium-tenant-unico.md
  last_modified: 2026-10-08T10:44:36Z
versions:
  - { name: velo-ce-verbale-260930-1754-strada-premium-tenant-unico.md, item_id: 01EFCYUZY7KUVQ22PWD5HY3BL6LCGXXAEG, last_modified: 2026-10-08T10:44:36Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:25:13Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]", "[[fatturazione-elettronica-sdi]]"]
tags: [verbale, velo-ce, business-central, premium, tenant, so-smart, eos, migrazione, fattura-elettronica, interno]
---

# Velo-CE · Verbale: Business Central oggi e strada verso Premium nel tenant unico

## Riassunto

Riunione del 30/09/2026 alle 17:54 (fino alle 19:05 circa), seconda parte della riunione con il cliente dopo [[velo-ce-verbale-giro-materiali-pilota-lungo]]. Presenti Cristian e Leo per BlueAge, Stefano e Claudia per [[velo-ce]]. Verbale da trascrizione automatica, contenuti dichiarati e non verificati, a uso interno. Fotografa il Business Central attuale (app So Smart/EOS, tre funzioni in uso, mappa dei sistemi) e confronta due strade per arrivare a Premium. Decisa la strada B proposta da BlueAge: nuovo BC Premium vuoto nel tenant della posta, partenza al 01/01/2027 con il perimetro amministrativo e commerciale, produzione e pianificazione dopo.

## Punti chiave

- Velo-CE ha due tenant Microsoft: uno per la posta, uno per Business Central (con l'account So Smart).
- Tre funzioni So Smart in uso: flusso ordini dal portale B2B (MMI, ordini dei dealer importati ogni due minuti come ordini di vendita, API su misura); configurazione Van Nicholas con tabelle di sostituzione dei componenti sull'ordine di assemblaggio; fattura elettronica attiva e passiva tramite intermediario.
- Installato ma fermo: valorizzazione del magazzino, conto lavoro, WMS, configuratore di prodotto del 2023 mai configurato, collegamento con il commercialista, quattro automatismi in errore da mesi, vecchio canale della fattura elettronica fermo dal 2024. Le credenziali dell'intermediario della fattura elettronica sono state aggiornate a mano nelle impostazioni.
- So Smart segue Essentials, non Premium; dietro c'è EOS Solutions. Le tre funzioni non toccano la produzione e sulla carta funzionano in Premium, ma la garanzia va chiesta a So Smart. Se servono solo quelle, il pacchetto So Smart perde senso: sono collegamenti replicabili.
- Mappa dei sistemi: portale dei dealer; ordini Van Nicholas, agenti e telefono via mail inseriti a mano; configuratore Van Nicholas senza flusso verso BC (nuovo configuratore per il cliente finale in lavorazione); Power BI legge BC; etichette da un programma sul server interno; macchinari fuori.
- Strada A: convertire il BC di oggi a Premium, tenendo le 54 app e facendo convivere codici vecchi e nuovi. Strada B (BlueAge): BC Premium nuovo nel tenant della posta, costruito a parte, con solo le tre funzioni e la localizzazione italiana; il portale manda gli ordini a entrambi i sistemi finché il nuovo non è pronto.
- Sei motivi della strada B: nessun rischio sul sistema in uso, codici e distinte nuovi senza misto, ordini su entrambi i sistemi, tenant unico, solo le app che servono, assistenza Microsoft sullo standard.
- Storico: il vecchio resta consultabile fino all'approvazione del bilancio 2026, saldi e partite aperte portati nel nuovo, storico in un data warehouse; Power BI si riaggancia.
- Assistenza dopo il passaggio: accordo come l'attuale (risposta entro 24 ore) o EOS; BlueAge osserva che chi fa il progetto potrebbe fare anche la manutenzione.
- Discrepanza da verificare: in riunione si dice che Velo-CE ha scelto Premium il 20 settembre, nel Project la decisione D12 è del 23/09.

## Numeri

- 124 app installate, di cui 54 EOS: 14 base tecnica e librerie, 11 fisco e fattura elettronica, altre per amministrazione, banche, contabilità simulata, flusso di cassa.
- Ordini B2B importati ogni 2 minuti.
- Tappe: prova gratuita del Premium fino a dicembre 2026; partenza 01/01/2027; vecchio sistema consultabile fino all'approvazione del bilancio 2026.
- Costi: licenze Premium e pacchetto So Smart sovrapposti solo nei mesi di convivenza.
- Durata: circa 1 ora e 10 minuti (17:54–19:05).

## Decisioni e azioni

- Decisione: strada B, nuovo BC Premium nel tenant della posta (già registrata nel Project, 025.35).
- Decisione: partenza al 01/01/2027 con esercizio, contabilità, IVA, fattura elettronica con lo stesso intermediario, vendite dal portale B2B, acquisti, magazzino dall'inventario di gennaio; poi produzione (ciclo, verniciatura in conto lavoro, costo del telaio, assemblaggio), poi pianificazione, costi e controllo.
- Fino a dicembre: impostazioni di base con Claudia, ricodifica degli articoli e dei materiali senza codice, distinte e cicli, caricamento Excel, tre funzioni So Smart e interfacce del portale nel nuovo ambiente.
- Piloti: Lungo Bosch, poi altri modelli, poi Van Nicholas, poi tutta la gamma.
- Domande aperte: garanzia So Smart sulle tre funzioni in Premium (CT-11); chi fa l'assistenza dopo il passaggio (CT-09); costo di rifare le integrazioni (CT-33, CT-34).
- [ ] Informare lo sviluppatore del portale B2B (Stefano o BlueAge, "la prossima settimana")
- [ ] Informare il commercialista del passaggio (il 2026 si chiude nel BC di oggi)
- [ ] Attivare la prova gratuita di Premium nel tenant della posta (Stefano)
- Mail sintetica a So Smart: già inviata (log 025.35).

## Versioni

- velo-ce-verbale-260930-1754-strada-premium-tenant-unico.md · 2026-10-08 · prima versione ingerita (data della riorganizzazione della cartella)
