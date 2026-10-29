---
type: source-doc
source: sharepoint
family: velo-ce-verbale-giro-materiali-pilota-lungo
current:
  item_id: 01EFCYUZ5O445S5ADGIVDK4MVRXX6PTPX7
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ5O445S5ADGIVDK4MVRXX6PTPX7
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/99 Project Claude (copia)/verbali/velo-ce-verbale-260930-1503-giro-materiali-pilota-lungo.md
  name: velo-ce-verbale-260930-1503-giro-materiali-pilota-lungo.md
  last_modified: 2026-10-08T10:44:36Z
versions:
  - { name: velo-ce-verbale-260930-1503-giro-materiali-pilota-lungo.md, item_id: 01EFCYUZ5O445S5ADGIVDK4MVRXX6PTPX7, last_modified: 2026-10-08T10:44:36Z }
also_at:
  - { web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Cristian/99 Project Claude (copia)/verbali/velo-ce-verbale-260930-1503-giro-materiali-pilota-lungo.md", item_id: 01EFCYUZ5O5BAMV4MVLZHINYQTHGA76AXZ }
status: active
partial: false
ingested_at: 2026-10-22T13:25:13Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [verbale, velo-ce, business-central, produzione, distinta, ciclo, telaio, pilota-lungo, change-management, interno]
---

# Velo-CE · Verbale: giro dei materiali e pilota telaio Lungo presentati al cliente

## Riassunto

Riunione del 30/09/2026 alle 15:03 (fino alle 17:40 circa), prima parte della riunione con il cliente; la seconda è [[velo-ce-verbale-strada-premium-tenant-unico]]. Presenti per BlueAge Leo (presenta) e Cristian, per [[velo-ce]] Stefano e Claudia. Verbale da trascrizione automatica, contenuti dichiarati e non verificati, a uso interno. BlueAge presenta il giro dei materiali del telaio, il pilota bici Lungo Bosch modellato in Business Central (distinte, cicli, codici provvisori, pianificazione, scarto e costo) e l'organizzazione in reparto. Si concorda di codificare la catena completa del percorso del telaio, con l'obiettivo di avere tutte le anagrafiche a dicembre e partire a gennaio dopo l'inventario.

## Punti chiave

- Il progetto ha due blocchi; il primo si chiude con l'inventario di gennaio, con tutti i materiali a sistema e codificati secondo regole da definire. Oggi circa due terzi dei materiali (soprattutto produttivi) non esistono a sistema. Obiettivo: portare nel sistema ciò che oggi sta in testa alle persone o in Excel.
- Rilievi in reparto con Ranzini, Gabriele, Simone e Alessandro; prodotti modello dati in Excel (v008), procedura in Word, ambiente di prova sul tenant BlueAge.
- Percorso del telaio: tubi e lamiere, laser, triangolo saldato a robot, montaggio del carro, saldatura, raddrizzatura, alesatura, sabbiatura, imballo. Fino al sabbiato si lavora a scorta (push), dall'ordine del cliente si tira (pull): verniciatura e assemblaggio. Il telaio sabbiato imballato è l'ultima scorta comune.
- Il carro è una distinta fantasma (9 pezzi montati in dima, nessuna scorta), più 12 pezzi saldati.
- Modello in BC: distinta di produzione (fantasma, scarto %, legame al ciclo) per il telaio, distinta di assemblaggio per la bici. Codici provvisori LU-xxx, cicli C-…, postazioni a tre lettere più numero, categorie su tre livelli.
- Vincoli: il metodo di costo dell'articolo non si cambia dopo i primi movimenti; tracciabilità di lotti e serie resta in Veloce-CRM; magazzini e collocazioni da decidere.
- Costo: proposta di scarto di default sul materiale con registrazione delle sole differenze; tariffa al minuto della postazione da costi annui; BlueAge sconsiglia la percentuale di costi generali; il costo dell'ordine si divide sui pezzi buoni.
- Proposta di avvio: ordini di produzione manuali, poi proposte del piano. Con giacenza negativa bloccata l'ordine senza materiale non si rilascia.
- Change management: postazione con terminale e stampante, foglio di lavoro che accompagna il lotto, registrazioni a fine giornata. Velo-CE ipotizza una persona dedicata alle registrazioni; BlueAge preferisce che registri chi lavora. In reparto servirà un PC con licenza.

## Numeri

- Pilota bici Lungo Bosch: 127 righe di distinta (7 articoli esistenti, 37 nuovi, 83 da verificare); 29 righe di opzioni e fuori distinta, 51 righe nel percorso del telaio; 23 articoli nel percorso del telaio.
- Circa 30 risposte dal reparto, tutte parametriche; numeri provvisori.
- Lotto telaio da 8; 4 ore di lavoro della persona sugli 8 telai alla sabbiatrice.
- Housing da foglio intero: 91–92 pezzi, scarto stimato 5–7%; lamiera 1500×3000 da 3 mm, circa 106 kg; multiplo di riordino 91.
- Ciclo del triangolo circa 32 minuti di presidio; riprese a mano sul 15% dei triangoli e su circa un accessorio su tre.
- Tubo 38×2, taglio 250 mm, scarto 5% su barra da 4,75 m con 16 cm persi nel mandrino; costo tubi per triangolo circa 14,4 euro.
- Carro: 9 pezzi in 20–30 minuti; verniciatore lead time circa 3 giorni.
- Prova nel pilota: tubo sella 50 → 48 buoni; housing 91 pezzi da un foglio di 105,97 kg.
- Durata: circa 2 ore e 40 minuti (15:03–17:40).

## Decisioni e azioni

- Decisione: si codifica la catena completa del percorso del telaio (concordato con il cliente).
- Decisione: distinta di produzione per il telaio, distinta di assemblaggio per la bici.
- Decisione: tracciabilità di lotti e numeri di serie resta per ora in Veloce-CRM.
- Obiettivo dichiarato: tutte le anagrafiche a dicembre 2026, partenza a gennaio 2027 dopo l'inventario.
- Domande aperte: avvio con ordini manuali o con il piano MRP; chi registra in reparto e con quale postazione; tariffe delle postazioni; scarto di default o dichiarato a ogni ordine; uno o più magazzini e collocazioni.
- [ ] Completare le prove del pilota: arrotondamenti, rilascio senza materiale, registrazione alternativa dei tempi, piano su tutti i livelli (BlueAge)
- [ ] Preparare la prossima sessione sul giro dal sabbiato al verniciato all'assemblaggio (BlueAge)
- [ ] Raccogliere i dati di costo per le tariffe delle postazioni (Velo-CE, Claudia e Stefano)

## Versioni

- velo-ce-verbale-260930-1503-giro-materiali-pilota-lungo.md · 2026-10-08 · prima versione ingerita (data della riorganizzazione della cartella)
