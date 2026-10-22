---
type: source-doc
source: sharepoint
family: velo-ce-flusso-operativo-telaio-a-scorta-acquisto-sabbiato-interno
current:
  item_id: 01EFCYUZ4ICYLUNLDM7ZBJ5QFNSUD77DPD
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ4ICYLUNLDM7ZBJ5QFNSUD77DPD
  web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/02 Configurazione/Telaio e produzione/Velo-CE - Flusso operativo telaio a scorta, acquisto-sabbiato - INTERNO - v001.xlsx"
  name: "Velo-CE - Flusso operativo telaio a scorta, acquisto-sabbiato - INTERNO - v001.xlsx"
  last_modified: 2026-10-05T05:44:25Z
versions:
  - { name: "Velo-CE - Flusso operativo telaio a scorta, acquisto-sabbiato - INTERNO - v001.xlsx", item_id: 01EFCYUZ4ICYLUNLDM7ZBJ5QFNSUD77DPD, last_modified: 2026-10-05T05:44:25Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:28:59Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [to-be, produzione, telaio, pianificazione, mrp, sfridi, costi, business-central-premium]
---

# Velo-CE · Flusso operativo del telaio a scorta, dall'acquisto delle materie prime al telaio sabbiato

## Riassunto

Cartella di lavoro interna BlueAge del 04/10/2026 (non mostrabile al cliente) per capire e spiegare a Stefano come si lavorerà in fabbrica e a sistema sul tratto a scorta del telaio, con Business Central Premium configurato secondo il modello pilota v008 ([[velo-ce-pilota-bc-lungo-bosch-modello-dati-5-fogli]]). Racconta il flusso "a cavallo del pezzo" in 25 passi, dal prerequisito di configurazione alla conta periodica, e per ogni passo dice chi fa cosa in reparto e a sistema, quali documenti e movimenti nascono, che licenza serve e quanto è verificato. Completano il quadro 39 schede di dettaglio con pagine BC e trappole note, 24 assunti, un'analisi degli sfridi, il confronto punto di riordino contro MRP, 18 eccezioni, ruoli e cadenze e un esempio di costo di un lotto di triangoli. Avverte che le decisioni di processo sono ancora aperte: ogni scelta è un assunto.

## Punti chiave

- **Perimetro**: dall'innesco del rifornimento al telaio sabbiato imballato a scorta; fuori fattura e SdI, verniciatura, assemblaggio. Il tenant del cliente oggi è in Essentials: ordini di produzione, cicli e distinte di produzione richiedono Premium.
- **Catena**: tubi e lamiere (acquisto in KG, tubi a metri) → 5 particolari laser e housing (LU-012, multiplo 91 per foglio) → triangolo → telaio sabbiato LU-003 (lotto 8, una carica di sabbiatrice, carro come fantasma PH-CARRO-LUNGO) → consumato dall'ordine del telaio verniciato LU-002 al rilascio.
- **Pianificazione**: calcolo del piano rigenerativo il lunedì, Ranzini accetta o modifica le proposte; oggi "Qtà riordino fissa" con punto di riordino su tutta la catena (A-01), domani MRP con "Lotto per lotto". Esempio di settimana: con il punto di riordino partono 8 sabbiati e poi 16 triangoli, con l'MRP nulla.
- **Registrazioni**: componenti consumati in avanti al rilascio (A-03); tutti i centri in consuntivazione Manuale, ogni postazione dichiara i propri minuti a fine giornata dal PC di reparto e l'ultima dichiara pezzi buoni e scarti con codice (A-04, A-05, A-10); riprese come tempo sull'operazione; ordine chiuso da Ranzini con passaggio a Finito.
- **Magazzino e costi**: ubicazione unica senza collocazioni, giacenza negativa vietata (A-06); FIFO sugli articoli, tariffa al minuto per centro (persone 30, laser 60, robot 45 €/h fittizi; sabbiatrice senza tariffa); rettifica costo automatica "Sempre" già attiva sul tenant cliente; registrazione in C/G mensile (oggi disattivata); inventario annuale a gennaio più conte mensili a rotazione su tubi e lamiere; tracciabilità di lotti e seriali resta in Veloce-CRM (decisione del 30/09).
- **Sfridi**: resa standard in distinta (formula Lunghezza, resa 1,04 sui tubi; 1,1645 kg di lamiera per housing); differenze registrate sull'ordine solo oltre ±5%. Lettura chiave: la resa 1,04 regge solo se gli spezzoni si riutilizzano; se si buttano il consumo reale supera il teorico di quasi il 12%.
- **Trappole note**: metodo di costing non modificabile dopo i movimenti; categoria di registrazione vuota blocca i documenti; senza calendario l'ordine non si aggiorna; con consuntivazione Indietro alla chiusura BC registra il residuo come output; componente senza metodo di riordino blocca il Finito del padre (R01); sabbiatrice senza tariffa = sabbiatura a costo zero.
- **Ruoli**: Ranzini pianificatore di reparto; Simone montaggio carro; Augusto logistica e inventario; Claudia amministrazione e costi; Leo (BlueAge) parametri e avvio; acquisti, ricevimento e operatori da definire, licenze da rilevare (anche licenza per dispositivo condiviso).

## Numeri

- 25 passi di flusso (F00.1-F25), 39 schede di dettaglio, 24 assunti, 5 ipotesi sullo sfrido, 18 eccezioni, 11 ruoli.
- Tubo sterzo: 0,255 m × 1,04 = 0,2652 m a pezzo; lotto da 80 = 21,216 m; barra 4,75 m con 0,16 m nel mandrino, 18 pezzi a barra, 5 barre; spezzoni non riutilizzati = +2,534 m (+11,9%).
- Housing: 91 per foglio 1500×3000×3, 105,97 kg; LAS-02 225 minuti a foglio.
- Triangolo: 12 minuti in dima, robot 10 minuti di attrezzaggio + 17,5 a pezzo, 2,5 di finitura; riprese circa 15%. Esempio di lotto da 8 con uno scarto: 351,45 € totali, 50,21 € a pezzo buono (43,93 senza scarti).
- Parametri iniziali segnaposto: LU-003 punto 16, quantità 8, multiplo 8; housing 91/91/91; lamiera 3 mm punto 2 fogli (≈212 kg), quantità 5 fogli.
- Inventario di partenza: gennaio 2027; calendari 2027.

## Decisioni e azioni

- Nessuna decisione presa nel documento: le scelte sono assunti (A-01…A-24) con indicato chi decide (Ranzini, Stefano, Claudia, Leo, BlueAge).
- [ ] Chiedere a Ranzini se gli spezzoni di barra si riutilizzano prima di fissare la resa 1,04
- [ ] Concordare con Claudia i valori iniziali delle giacenze per il caricamento di gennaio 2027
- [ ] Provare in sandbox l'ordine d'acquisto in KG con conversione in metri (test 4.1) e il consumo negativo collegato
- [ ] Riportare dal file del modello v008 i codici segnati [v008] (triangolo, tubi, componenti del carro)

## Versioni

- Velo-CE - Flusso operativo telaio a scorta, acquisto-sabbiato - INTERNO - v001.xlsx · 2026-10-05 · prima versione ingerita (documento datato 04/10/2026)
