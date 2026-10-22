---
type: source-doc
source: attachment
family: velo-ce-il-giro-del-telaio-in-essential-e-in-premium
current:
  item_id: "AAMkAGMyY2M5ZTczLTYwNDEtNGZiOC1iYjJjLTFhZjJhOGY1YjFiMQBGAAAAAADRF2aJ18MKT6wbnyNtwv9jBwCNJoMhLsxPT4EkGUihNeQOAAAAAAEMAACNJoMhLsxPT4EkGUihNeQOAAAm8_DyAAABEgAQAPjELV5ofnVGv9x5s6v_LvA="
  uri: "mail:///messages/AAMkAGMyY2M5ZTczLTYwNDEtNGZiOC1iYjJjLTFhZjJhOGY1YjFiMQBGAAAAAADRF2aJ18MKT6wbnyNtwv9jBwCNJoMhLsxPT4EkGUihNeQOAAAAAAEMAACNJoMhLsxPT4EkGUihNeQOAAAm8_DyAAA%3D/attachments/AAMkAGMyY2M5ZTczLTYwNDEtNGZiOC1iYjJjLTFhZjJhOGY1YjFiMQBGAAAAAADRF2aJ18MKT6wbnyNtwv9jBwCNJoMhLsxPT4EkGUihNeQOAAAAAAEMAACNJoMhLsxPT4EkGUihNeQOAAAm8_DyAAABEgAQAPjELV5ofnVGv9x5s6v_LvA%3D"
  web_url: ""
  name: "260918 Velo-CE - Il giro del telaio in Essential e in Premium - v001.docx"
  last_modified: 2026-09-18T18:21:46Z
versions:
  - { name: "260918 Velo-CE - Il giro del telaio in Essential e in Premium - v001.docx", item_id: "AAMkAGMyY2M5ZTczLTYwNDEtNGZiOC1iYjJjLTFhZjJhOGY1YjFiMQBGAAAAAADRF2aJ18MKT6wbnyNtwv9jBwCNJoMhLsxPT4EkGUihNeQOAAAAAAEMAACNJoMhLsxPT4EkGUihNeQOAAAm8_DyAAABEgAQAPjELV5ofnVGv9x5s6v_LvA=", last_modified: 2026-09-18T18:21:46Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T15:24:11Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [business-central, licenze, produzione, distinta-base, interno]
---

# Velo-CE · Il giro del telaio in Essential e in Premium

## Riassunto

Documento interno BlueAge del 18 settembre 2026 (v001), scritto da [[leonardo-pinsone]] per [[cristian-schifone]] nel [[velo-ce-progetto-dynamics]]. Ricostruisce il percorso del telaio di [[velo-ce]] dalla barra alla bici e confronta lo stesso disegno nelle licenze Essential e Premium di Business Central, sul pilota MLCA-5E-545-CDX (base Lungo BH, RAL 6029). Perimetro: reparto telai (laser, piegatura, puntatura, saldatura manuale e robot, sabbiatura) e conto lavoro di verniciatura; fuori il montaggio bici, commerciale, acquisti, magazzino e post-vendita. Il documento rende confrontabili i due disegni; la raccomandazione sulla licenza sta in una scheda decisione separata. Basi: rilievi in sede del 15/09, estrazione anagrafica dell'08/09, fatture dei fornitori di materia prima, prove a sistema T01-T51 del 17 e 18/09, documentazione Microsoft.

## Punti chiave

- **Flusso reale**: cinque basi di telaio (Lungo e Multi in versione Bosch e Shimano, più Muscolare); sei punti di sosta fra barra e bici, uno fuori azienda (il verniciatore). In reparto telai oggi nessuno registra a sistema e le materie prime non esistono come articoli.
- **Principio di disegno**: un codice articolo esiste solo dove c'è una registrazione; ciò che sta fra due registrazioni è una riga di distinta o una distinta fantasma. Scala a livelli: 0 oggi, 1 solo verniciato, 2 sabbiato e verniciato, 3 saldato, sabbiato e verniciato (bersaglio del documento), 4 anche le parti laser (solo con una persona dedicata in reparto).
- **Distinta fantasma**: esiste solo in Premium (distinta di produzione richiamata dal padre, esplode al rilascio, annidabile, costo nel padre, nessuna giacenza né costo proprio). In Essential non c'è equivalente: la distinta di assemblaggio accetta solo articoli e risorse. Candidato naturale il carro Lungo, poi l'housing; le parti laser restano articoli perché sostano nei cassoni.
- **Giro in Essential**: tre ordini di assemblaggio a cascata, trasferimenti da e verso l'ubicazione del verniciatore, ordine d'acquisto con riga Addebito articolo assegnata al carico, rettifica costo. Provato con i numeri su ambiente di test. L'articolo non di inventario in distinta non porta costo.
- **Giro in Premium**: con Make-to-Order il piano propone un ordine di produzione con tre righe collegate, i fantasmi esplodono al rilascio, l'operazione esterna del verniciato genera l'ordine d'acquisto, consumi a scarico all'indietro. Il conto lavoro completo richiede l'app Microsoft Subcontracting (solo Premium, gratuita sul Marketplace).
- **Cosa si perde in Essential**: il carro diventa un articolo fittizio o sparisce, lo sfrido resta nascosto nella quantità, le fasi non si vedono, i documenti per lotto sono il triplo. Essential arriva comunque a costo del telaio, consumi, fabbisogno e giacenza dei tre livelli, ma per una strada più lunga.
- **Passaggio a Premium in un secondo momento**: restano articoli, materie prime, movimenti, giacenze; si rifanno distinte, sistema di rifornimento e giro del verniciatore. Costi veri: doppio addestramento, calendario dell'abbonamento, costo per fase non recuperabile sui telai già fatti. Mossa consigliata: costruire subito le distinte di assemblaggio con la struttura Premium (stessi tre livelli e codici, materie prime raggruppate per futuro fantasma).
- **Impatto organizzativo**: il primo cambiamento pesante è in amministrazione (fatture delle materie prime da conto generale a righe articolo con ricevimento in metri e chili). Sequenza: materie prime, primo versamento, poi la scala dei livelli; cicli iniziali con poche operazioni e tempi grezzi.

## Numeri

- Confronto al livello 3 sullo stesso telaio: Essential 6 documenti e 8 registrazioni, Premium 2 documenti e 3 registrazioni.
- Codici bersaglio: 3 di telaio per base più circa 12 di materia prima; su cinque basi 15 codici di telaio.
- Anagrafica di partenza: 1.112 codici, 418 con giacenza (279 a costo zero), 669 a costo zero in totale; circa 140 codici con distinta di assemblaggio, 1.263 righe di distinta, 571 ordini di assemblaggio registrati (6 da ordini di vendita); circa 90 configurazioni Veloe senza distinta.
- Reparto: circa 50 finti motori Bosch e 50 Shimano come tetto al materiale in lavorazione; sabbiatura 8 telai per volta in circa 4 ore; montaggio circa 10 bici al giorno.
- Verniciatura: due prese a settimana, circa 50 pezzi fuori in media, scorta di partenza 6 per colore; prova conto lavoro con 10 pezzi, costo a pezzo da 74,86 a 86,86 dopo l'addebito.
- Passaggio a Premium a metà anno: fino a circa 2.495 euro su tre utenti, oppure attesa fino al 26/09/2027.
- Calendario proposto: livello 1 all'avvio, livello 3 entro l'inventario di gennaio, livello 4 quando c'è la persona in reparto.

## Decisioni e azioni

- Le parti laser restano articoli con entrambe le licenze; il fantasma è l'alternativa al livello 4, non una sua versione leggera.
- Le distinte di assemblaggio in Essential vanno costruite con la struttura che servirebbe in Premium.
- [ ] V1: verificare se le righe Make-to-Order finiscono nello stesso ordine di produzione (Cristian) 📅 2026-09-21
- [ ] V2: verificare la proposta a cascata del piano su due livelli di assemblaggio in Essential, prova D17 (Cristian) 📅 2026-09-21
- [ ] V3: esplosione di una parte senza ordine proprio in Essential, test F1 (Cristian)
- [ ] V4: scrittura del codice variante su una riga di distinta di assemblaggio (Cristian)
- [ ] V5: consumo da un'altra ubicazione in un ordine di assemblaggio, per decidere uno o due trasferimenti (Cristian)
- [ ] V6: diritto d'uso della pianificazione con una licenza Essential vera, o conferma scritta dal canale (Cristian)
- [ ] V7: conteggio dei documenti su un lotto reale nei due modelli, test F5 (Leonardo e Cristian)
- [ ] V8: chiedere in sede chi registra i 571 ordini di assemblaggio già presenti (Leonardo) 📅 2026-09-21

## Versioni

- 260918 Velo-CE - Il giro del telaio in Essential e in Premium - v001.docx · 2026-09-18 · prima versione, ricevuta in allegato a [[il-giro-del-telaio-in-essential-e-in-premium-documento-interno-v001]]
