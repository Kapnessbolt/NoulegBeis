---
type: source-doc
source: sharepoint
family: velo-ce-guida-ciclo-dacquisto-ordine-ricevimento-fattura-cliente
current:
  item_id: 01EFCYUZ6GGXZ5TZMZTNA3DK7CD4UKMWC5
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ6GGXZ5TZMZTNA3DK7CD4UKMWC5
  web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/08 Guide/Velo-CE - Guida ciclo d'acquisto ordine ricevimento fattura - CLIENTE - v003.pdf"
  name: "Velo-CE - Guida ciclo d'acquisto ordine ricevimento fattura - CLIENTE - v003.pdf"
  last_modified: 2026-10-28T08:06:12Z
versions:
  - { name: "Velo-CE - Guida ciclo d'acquisto ordine ricevimento fattura - CLIENTE - v003.pdf", item_id: 01EFCYUZ6GGXZ5TZMZTNA3DK7CD4UKMWC5, last_modified: 2026-10-28T08:06:12Z }
  - { name: "Velo-CE - Guida ciclo d'acquisto ordine ricevimento fattura - CLIENTE - v001.pdf", item_id: 01EFCYUZ2NFY7SHZIZHNCK2HCAV2ZD6TXR, last_modified: 2026-10-08T10:43:50Z }
  - { name: "Velo-CE - Guida ciclo d'acquisto ordine ricevimento fattura - CLIENTE - v001.docx", item_id: 01EFCYUZZFBAAZ4ZQ7OBDJR4NEJPX3UNAK, last_modified: 2026-10-08T09:38:16Z }
also_at:
  - { web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/08 Guide/Velo-CE - Guida ciclo d'acquisto ordine ricevimento fattura - CLIENTE - v003.docx", item_id: 01EFCYUZ2IVKUVOYPS2JH25GXPEAKCG5OI }
status: active
partial: false
ingested_at: 2026-10-29T05:59:14Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [guida-operativa, business-central, acquisti, ricevimento-merci, fattura-passiva, magazzino]
---

# Velo-CE · Guida operativa: il ciclo d'acquisto (ordine, ricevimento, fattura)

## Riassunto

Guida operativa BlueAge per Velo-CE (v003 del 24/10/2026, 18 pagine; v001 dell'08/10, 9 pagine) su come passare dal carico di magazzino a mano con fattura su conto di costo al flusso standard di Business Central in tre passaggi: ordine d'acquisto, ricevimento sull'ordine, fattura che prende le righe del carico. Usa solo funzioni standard comprese nella licenza Essentials, nessuna app aggiuntiva. È costruita su una prova eseguita da BlueAge in un ambiente dimostrativo, con lo stesso acquisto registrato nei due modi per mostrare la differenza sul costo dell'articolo. La v003 aggiunge il capitolo 3 sui costi accessori: trasporti, dazi e spese di spedizionieri e corrieri entrano nel costo dell'articolo con due soli addebiti articolo (TRASP e DAZI), provati il 24/10 in una società dimostrativa con piano dei conti, categorie e IVA di Velo-CE. Chiude con un confronto oggi/domani, la ripartizione dei compiti e dieci punti da sapere prima di partire.

## Punti chiave

- **Oggi**: il magazzino carica a mano da Registrazioni magazzino (costo zero o scritto a mano) e l'amministrazione registra la fattura su un conto di costo: carico e fattura scollegati, il costo vero dei componenti si vede solo sul conto e non sull'articolo né sulle bici assemblate.
- **Domani**: gli acquisti inseriscono e rilasciano l'ordine con quantità e prezzi concordati; il magazzino conta i colli, confronta il DDT con l'ordine, scrive i pezzi arrivati e registra il solo carico (anche parziale); l'amministrazione usa "Prendi righe di carico", corregge il prezzo se diverso e registra.
- **Cosa si ottiene**: costo dell'articolo pari al prezzo di fattura, aggiornato da solo; ordini aperti con quanto manca; carichi non fatturati per fornitore come base delle fatture da ricevere di fine anno; controllo della fattura riga per riga; ordine, carico e fattura collegati e visibili con "Trova movimenti".
- **Messaggio**: il lavoro non sparisce, si sposta a monte dove nasce l'informazione; all'amministrazione resta il controllo, non la ricostruzione.
- **Limiti e punti da decidere**: abbinamento della fattura elettronica dallo SDI dipende dall'app fiscale del nuovo ambiente e va provato; momento di contabilizzazione del valore di magazzino da decidere con il commercialista; tenere o no l'importo totale obbligatorio in fattura; ordini aperti già caricati a mano da controllare e chiudere prima di adottare il flusso; servizi e spese restano fatture su conto; ridurre la quantità d'ordine se i residui non arriveranno.
- **Costi accessori (v003)**: TRASP raccoglie trasporto e tutte le voci di spedizionieri e corrieri, DAZI il dazio; IVA all'importazione, bolli, spese bancarie e trasporti su vendite restano righe su conto. Il trasporto si ripartisce per volume o per peso (da decidere), il dazio sempre per importo; l'addebito si aggancia a un carico registrato, ritrovato dalla lettera di vettura scritta sull'ordine nel campo del documento di trasporto.
- **Casi provati**: trasporto nella fattura del fornitore; spedizioniere dell'import con fattura della bolla (dazio come addebito, IVA e bollo su conto) e fattura del nolo; corriere espresso con fattura della bolla e fattura mensile DHL (una riga TRASP per spedizione d'acquisto, da automatizzare dall'XML); fatture arrivate dopo il consumo, con rettifiche automatiche del costo.
- **Da sapere prima di partire (v003)**: carico registrato prima delle fatture di trasporto e dazio; «% costi indiretti» a zero sugli articoli con addebiti, altrimenti il costo si conta due volte; volume e peso per pezzo sulla scheda articolo almeno per i componenti importati; IVA dell'addebito DAZI da impostare a ESC15; cambio del dollaro e anticipi ai fornitori esteri da scegliere con il commercialista.

## Numeri

- Prova: ordine di 40 copertoni a 12,50 euro, ricevuti 30, fatturati a 13,00 euro: 390,00 euro più IVA 85,80 euro, totale 475,80 euro.
- Dopo il carico parziale: carichi non fatturati 457,50 euro e ordine inevaso 152,50 euro (IVA inclusa); 10 pezzi ancora da ricevere.
- Articolo caricato a mano: 40 pezzi a costo unitario 0,00; articolo del flusso standard: costo unitario e ultimo costo diretto 13,00 euro.
- Prova costi accessori (importi inventati): trasporto di 50 € diviso per importo su due tubi, costo da 3,90 a 4,15 € al metro; nolo diviso per peso, forcella da 10,45 a 12,16 € (+16,3%) e manubrio da 8,91 a 9,68 € (+8,7%); con il 5% di costi indiretti il manubrio sale a 9,76 € invece di 9,32 €.

## Decisioni e azioni

- [ ] Provare l'abbinamento della fattura elettronica all'ordine e al carico sull'app fiscale scelta per il nuovo ambiente
- [ ] Decidere con il commercialista quando il valore di magazzino passa in contabilità (a ogni registrazione o con elaborazione periodica)
- [ ] Decidere se tenere obbligatorio l'importo totale della fattura
- [ ] Controllare uno per uno gli ordini d'acquisto aperti e chiudere quelli già evasi prima di adottare il flusso
- [ ] Decidere il criterio di ripartizione del trasporto (per volume o per peso) ([[velo-ce-guida-ciclo-dacquisto-ordine-ricevimento-fattura-cliente]])
- [ ] Scegliere con il commercialista il cambio del dollaro e la gestione degli anticipi ai fornitori esteri ([[velo-ce-guida-ciclo-dacquisto-ordine-ricevimento-fattura-cliente]])

## Versioni

- Velo-CE - Guida ciclo d'acquisto ordine ricevimento fattura - CLIENTE - v001.pdf · 2026-10-08 · prima versione ingerita (v001 dell'08/10/2026); data di modifica dovuta alla riorganizzazione della cartella
- Velo-CE - Guida ciclo d'acquisto ordine ricevimento fattura - CLIENTE - v001.docx · 2026-10-08 · sorgente modificabile dello stesso documento
- Velo-CE - Guida ciclo d'acquisto ordine ricevimento fattura - CLIENTE - v003.pdf · 2026-10-28 · v003 del 24/10: capitolo 3 sui costi accessori (TRASP e DAZI), 18 pagine; v002 del 18/10 non vista; anche in .docx del 27/10; nella cartella `Cristian/08 Guide/`

