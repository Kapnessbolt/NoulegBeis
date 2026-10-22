---
type: source-doc
source: sharepoint
family: velo-ce-guida-ciclo-dacquisto-ordine-ricevimento-fattura-cliente
current:
  item_id: 01EFCYUZ2NFY7SHZIZHNCK2HCAV2ZD6TXR
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ2NFY7SHZIZHNCK2HCAV2ZD6TXR
  web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/08 Guide/Velo-CE - Guida ciclo d'acquisto ordine ricevimento fattura - CLIENTE - v001.pdf"
  name: "Velo-CE - Guida ciclo d'acquisto ordine ricevimento fattura - CLIENTE - v001.pdf"
  last_modified: 2026-10-08T10:43:50Z
versions:
  - { name: "Velo-CE - Guida ciclo d'acquisto ordine ricevimento fattura - CLIENTE - v001.pdf", item_id: 01EFCYUZ2NFY7SHZIZHNCK2HCAV2ZD6TXR, last_modified: 2026-10-08T10:43:50Z }
  - { name: "Velo-CE - Guida ciclo d'acquisto ordine ricevimento fattura - CLIENTE - v001.docx", item_id: 01EFCYUZZFBAAZ4ZQ7OBDJR4NEJPX3UNAK, last_modified: 2026-10-08T09:38:16Z }
also_at:
  - { web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/08 Guide/Velo-CE - Guida ciclo d'acquisto ordine ricevimento fattura - CLIENTE - v001.docx", item_id: 01EFCYUZZFBAAZ4ZQ7OBDJR4NEJPX3UNAK }
status: active
partial: false
ingested_at: 2026-10-22T13:25:42Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [guida-operativa, business-central, acquisti, ricevimento-merci, fattura-passiva, magazzino]
---

# Velo-CE · Guida operativa: il ciclo d'acquisto (ordine, ricevimento, fattura)

## Riassunto

Guida operativa BlueAge per Velo-CE (v001 dell'08/10/2026, 9 pagine) su come passare dal carico di magazzino a mano con fattura su conto di costo al flusso standard di Business Central in tre passaggi: ordine d'acquisto, ricevimento sull'ordine, fattura che prende le righe del carico. Usa solo funzioni standard comprese nella licenza Essentials, nessuna app aggiuntiva. È costruita su una prova eseguita da BlueAge in un ambiente dimostrativo, con lo stesso acquisto registrato nei due modi per mostrare la differenza sul costo dell'articolo. Chiude con un confronto oggi/domani, la ripartizione dei compiti e sette limiti o punti da decidere.

## Punti chiave

- **Oggi**: il magazzino carica a mano da Registrazioni magazzino (costo zero o scritto a mano) e l'amministrazione registra la fattura su un conto di costo: carico e fattura scollegati, il costo vero dei componenti si vede solo sul conto e non sull'articolo né sulle bici assemblate.
- **Domani**: gli acquisti inseriscono e rilasciano l'ordine con quantità e prezzi concordati; il magazzino conta i colli, confronta il DDT con l'ordine, scrive i pezzi arrivati e registra il solo carico (anche parziale); l'amministrazione usa "Prendi righe di carico", corregge il prezzo se diverso e registra.
- **Cosa si ottiene**: costo dell'articolo pari al prezzo di fattura, aggiornato da solo; ordini aperti con quanto manca; carichi non fatturati per fornitore come base delle fatture da ricevere di fine anno; controllo della fattura riga per riga; ordine, carico e fattura collegati e visibili con "Trova movimenti".
- **Messaggio**: il lavoro non sparisce, si sposta a monte dove nasce l'informazione; all'amministrazione resta il controllo, non la ricostruzione.
- **Limiti e punti da decidere**: abbinamento della fattura elettronica dallo SDI dipende dall'app fiscale del nuovo ambiente e va provato; momento di contabilizzazione del valore di magazzino da decidere con il commercialista; tenere o no l'importo totale obbligatorio in fattura; ordini aperti già caricati a mano da controllare e chiudere prima di adottare il flusso; servizi e spese restano fatture su conto; ridurre la quantità d'ordine se i residui non arriveranno.

## Numeri

- Prova: ordine di 40 copertoni a 12,50 euro, ricevuti 30, fatturati a 13,00 euro: 390,00 euro più IVA 85,80 euro, totale 475,80 euro.
- Dopo il carico parziale: carichi non fatturati 457,50 euro e ordine inevaso 152,50 euro (IVA inclusa); 10 pezzi ancora da ricevere.
- Articolo caricato a mano: 40 pezzi a costo unitario 0,00; articolo del flusso standard: costo unitario e ultimo costo diretto 13,00 euro.

## Decisioni e azioni

- [ ] Provare l'abbinamento della fattura elettronica all'ordine e al carico sull'app fiscale scelta per il nuovo ambiente
- [ ] Decidere con il commercialista quando il valore di magazzino passa in contabilità (a ogni registrazione o con elaborazione periodica)
- [ ] Decidere se tenere obbligatorio l'importo totale della fattura
- [ ] Controllare uno per uno gli ordini d'acquisto aperti e chiudere quelli già evasi prima di adottare il flusso

## Versioni

- Velo-CE - Guida ciclo d'acquisto ordine ricevimento fattura - CLIENTE - v001.pdf · 2026-10-08 · prima versione ingerita (v001 dell'08/10/2026); data di modifica dovuta alla riorganizzazione della cartella
- Velo-CE - Guida ciclo d'acquisto ordine ricevimento fattura - CLIENTE - v001.docx · 2026-10-08 · sorgente modificabile dello stesso documento
