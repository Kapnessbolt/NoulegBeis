---
type: source-doc
source: sharepoint
family: velo-ce-guida-stampa-etichetta-articolo-con-codice-a-barre-interno
current:
  item_id: 01EFCYUZ7M6DI55WZPH5HYXKAIWYX372MK
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ7M6DI55WZPH5HYXKAIWYX372MK
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/08 Guide/Velo-CE - Guida stampa etichetta articolo con codice a barre - INTERNO - v002.pdf
  name: Velo-CE - Guida stampa etichetta articolo con codice a barre - INTERNO - v002.pdf
  last_modified: 2026-10-08T10:43:51Z
versions:
  - { name: Velo-CE - Guida stampa etichetta articolo con codice a barre - INTERNO - v002.pdf, item_id: 01EFCYUZZSGZTVDM746NGZKLZXO4KIUL22, last_modified: 2026-10-08T10:43:51Z }
  - { name: Velo-CE - Guida stampa etichetta articolo con codice a barre - INTERNO - v002.docx, item_id: 01EFCYUZ4EHWZXOABV2ZEJUZKD6XAVSQFL, last_modified: 2026-10-07T10:04:03Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:25:42Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [guida-operativa, business-central, etichette, codice-a-barre, magazzino, ricevimento-merci]
---

# Velo-CE · Guida operativa: stampare l'etichetta articolo con codice a barre

## Riassunto

Guida operativa interna BlueAge (v002 del 07/10/2026, bozza da validare con Velo-CE, 6 pagine) per stampare in Business Central un'etichetta articolo Velo-CE con il codice articolo in Code 39, usando solo il report standard "Etichetta GTIN dell'articolo" (6625) con un layout Word BlueAge, senza app esterne e con licenza Essentials. Spiega come impostare una volta il layout, stampare un'etichetta per collo dopo il controllo della merce, cosa fa il lettore di codici a barre nei vari campi, le due strade per i semilavorati, come modificare il layout e cosa lo standard non fa. In appendice l'uso del GTIN. Collegata al capitolato di etichettatura dei fornitori ([[velo-ce-capitolato-etichettatura-colli-fornitori-cliente]]).

## Punti chiave

- **Etichetta Velo-CE**: intestazione, codice articolo in grande, codice a barre del codice articolo, descrizione, data e ora di stampa; layout "VELO-CE SCATOLA CODE39", nessun GTIN da compilare.
- **Impostazione una tantum** (amministratore): caricare il layout Word sul report 6625, approvarlo (un layout in bozza non compare in stampa) e impostarlo come predefinito.
- **Stampa**: si stampa dopo aver contato i colli e confrontato il DDT con l'ordine, una copia per collo dalla finestra del browser (il report non ha un campo copie); un'etichetta per articolo selezionato.
- **Lettore**: il codice articolo letto nel campo Nr. compila la riga; il numero d'ordine letto nella ricerca filtra gli ordini d'acquisto; il codice o EAN del fornitore nel campo riferimento articolo trova l'articolo se registrato nei Riferimenti articolo.
- **Semilavorati**: dall'articolo (report 6625, Essentials) per quelli non tracciati come triangolo e telaio sabbiato; dall'output di produzione (report 99000769) solo con Premium e articolo tracciato. Numero d'ordine di produzione, telaio o lotto sull'etichetta solo con tracciabilità o con un'estensione.
- **Limiti dello standard**: non chiede le copie, non stampa per riga di carico o per collo con quantità e numero d'ordine, non stampa fornitore, peso, lunghezza o collocazione, non apre il ricevimento leggendo l'ordine e non conta i pezzi: per un ricevimento "leggi e conta" serve un'app di magazzino o uno sviluppo.
- **Code 39 e GTIN**: Code 39 accetta maiuscole, cifre e pochi segni; va provato il codice articolo più lungo. Il GTIN serve su prodotti venduti e componenti con EAN del produttore; per uso interno prefissi GS1 040–049, mai su merce venduta.

## Numeri

- Report standard 6625 (etichetta articolo) e 99000769 (etichetta output di produzione).
- Etichetta di circa 20 × 8,4 cm, su A4 o etichetta A5.
- Prove: ambiente BlueAge sbx-test-essential (Business Central 28, Essentials) e sbx-studio (Premium); evidenze T119–T142.

## Decisioni e azioni

- [ ] Validare la guida con Velo-CE (bozza interna)
- [ ] Provare la lettura in Code 39 del codice articolo più lungo prima dell'uso
- [ ] Decidere se attivare la tracciabilità (lotto o seriale) sui semilavorati che richiedono numero d'ordine o di telaio sull'etichetta
- [ ] Per stampanti a rotolo, preparare una copia del layout con la misura del rotolo

## Versioni

- Velo-CE - Guida stampa etichetta articolo con codice a barre - INTERNO - v002.pdf · 2026-10-08 · prima versione ingerita (v002 del 07/10/2026); rispetto alla v001: layout Velo-CE con codice articolo nel codice a barre, stato e layout predefinito, lettura del numero d'ordine, semilavorati, GTIN in appendice. Data di modifica dovuta alla riorganizzazione della cartella
- Velo-CE - Guida stampa etichetta articolo con codice a barre - INTERNO - v002.docx · 2026-10-07 · sorgente modificabile dello stesso documento
