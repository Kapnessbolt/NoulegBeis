---
type: source-doc
source: sharepoint
family: velo-ce-giro-reale-dei-materiali-in-bc-interno
current:
  item_id: 01EFCYUZ6OFXE7KPGLDJD33VFH5FAQZAQD
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ6OFXE7KPGLDJD33VFH5FAQZAQD
  web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/02 Configurazione/Materiali, pianificazione e costi/Velo-CE - Giro reale dei materiali in BC - INTERNO - v001.md"
  name: "Velo-CE - Giro reale dei materiali in BC - INTERNO - v001.md"
  last_modified: 2026-10-08T10:44:30Z
versions:
  - { name: "Velo-CE - Giro reale dei materiali in BC - INTERNO - v001.md", item_id: 01EFCYUZ6OFXE7KPGLDJD33VFH5FAQZAQD, last_modified: 2026-10-08T10:44:30Z }
also_at:
  - { web_url: "https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Cristian/02 Configurazione/Materiali, pianificazione e costi/Velo-CE - Giro reale dei materiali in BC - INTERNO - v001.md", item_id: 01EFCYUZ4DGDZTWBEKPJDKXBWJ3N2PBO5W }
status: active
partial: false
ingested_at: 2026-10-22T13:28:59Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [as-is, magazzino, acquisti, assemblaggio, costi, rimanenze, business-central, rischi]
---

# Velo-CE · Giro reale dei materiali in Business Central (rilevazione del 05/10/2026)

## Riassunto

Rilevazione interna BlueAge (da Cristian, con Claude, per Leonardo; non mostrabile al cliente) fatta il 05/10/2026 in sola lettura sull'ambiente Production della società VELO-CE SRL. Ricostruisce come entra, si trasforma ed esce il materiale in BC, marcando ogni affermazione come verificata, dichiarata, documentale o da rilevare. Conclusione: contabilità e magazzino viaggiano separati; le bici Veloe non passano dal magazzino; il magazzino si carica a mano, spesso a costo zero, poco prima di assemblaggi o spedizioni; il bilancio regge perché le rimanenze sono una sola scrittura manuale all'anno. Chiude con quattro domande mirate e quattro proposte, la principale è decidere il giro d'acquisto standard prima di MRP e Premium.

## Punti chiave

- **Bici Veloe**: articoli "Non di inventario" senza distinta; in BC c'è solo la vendita (DDT e fattura) a costo zero. Telaio, motore e componenti Veloe non passano dal magazzino; BC per Veloe è un sistema di fatturazione. Gli accessori Veloe (`AM…`) invece sono articoli di magazzino assemblati.
- **Acquisti**: dal 2023 nessuna fattura d'acquisto con righe di articolo; tutte vanno su conto contabile (es. "comp ass UE"), una riga per fattura, senza numero d'ordine. Gli ordini d'acquisto servono solo a ordinare al fornitore: da maggio 2026, 27 ordini tutti aperti e mai ricevuti.
- **Tre fasi delle entrate**: apr 2024-apr 2025 giornale "Acquisto"; mag 2025-apr 2026 ricevimenti su ordine (l'eccezione); da apr 2026 di nuovo giornale "Acquisto" (serie MAG26) con volumi alti, soprattutto Van Nicholas.
- **Van Nicholas non gira correttamente**: assemblaggi reali, ma stock ex Accell caricato a costo zero il 03/02 e lotti di componenti entrati a zero (es. 400 motori Bosch il 24/05): costo delle bici VN sottostimato. Caso del motore BEB1110000V: kit Bosch passato da 826,49 a 60,11 €/kit dopo la rettifica costi automatica.
- **Rischio ordine fantasma**: AOR26-0011 (400 motori) risulta aperto con 400 da ricevere; se qualcuno lo riceve per registrare la fattura entrano 400 motori inesistenti.
- **Assemblaggio**: il portale B2B dei dealer (flusso MMI) non crea ordini di assemblaggio; quelli legati a ordini di vendita sono solo Van Nicholas, creati dalla funzione standard "Assemblaggio su ordine" da luglio; il resto è montaggio a lotti per magazzino creato a mano. Nessun sistema esterno inizializza assemblaggi; l'API So Smart di remap dei componenti (dichiarata il 02/10) non è stata osservata.
- **Bilancio e fisco**: "Reg. automatica costi" disattivata; rimanenze finali come un'unica scrittura manuale all'anno sul conto rimanenze materiali di produzione. Origine del valore da rilevare (conta di gennaio o modulo EOS IVC). Punto da far verificare al commercialista: possibile obbligo di scritture ausiliarie di magazzino (art. 14 DPR 600/73), perché le rimanenze superano la soglia.
- **Limiti**: liste lette scorrendo la griglia; 2023 non coperto; famiglie assegnate per prefisso; legame carico → assemblaggio misurato per utente e tempo; massimo 2 sessioni per utente sullo stesso client (controllo non standard, probabile app EOS).

## Numeri

- Carichi con giornale "Acquisto" da aprile 2026: circa 2,9 M€ (Van Nicholas ~171 righe, 2,87 M€; Veloe ~77 righe, ~66 k€).
- Carico iniziale ex Accell del 03/02: 123 righe, 3.223 pezzi, 0 € (valore dichiarato in blocco 150 k€).
- Rettifica negativa MAG26-0266 del 13/07: −1.400 pezzi, −491.400 €.
- Output di assemblaggio 2026: Van Nicholas 5,09 M€, Veloe 62 k€; circa 270 assemblaggi registrati; assemblaggi per mese da 908 movimenti a maggio a 0 a settembre.
- Kit Bosch: 400 kit, 826,49 €/kit alla registrazione, 60,11 €/kit dopo la rettifica; componenti caricati a zero per circa 306.000 € sul lotto.
- Ordini d'acquisto aperti grandi: Hebei Hanglun ≈ 960 k€, CHM ≈ 148 k€.
- Rimanenze: 2.713.672,00 € al 31/12/2024; 2.059.737,50 € al 31/12/2025.
- Uscite 2026: 4.026 registri (2.110 vendite, 266 assemblaggi, 389 giornali, 51 ricevimenti, 1.204 rettifiche costi); 25 ordini di assemblaggio aperti, 16 collegati a 11 ordini di vendita.

## Decisioni e azioni

- Proposta: inserire il giro reale nello stato progetto (blocco 02) e i rischi nel blocco 03 (costi a zero sugli assemblati VN, AOR26-0011 da non ricevere, rimanenze extracontabili).
- Proposta: prima di MRP e Premium decidere con Claudia e Stefano il giro d'acquisto standard (ricevimento sull'ordine, fattura sulle righe articolo, costi accessori come addebiti articolo). È processo, non configurazione.
- Correzione dei costi a zero e chiusura degli ordini fantasma: da decidere con Claudia e il commercialista; chi esegue da decidere.
- [ ] Chiedere a Claudia da quale report o file viene il valore delle rimanenze al 31/12/2025
- [ ] Chiedere a chi carica il magazzino perché da aprile 2026 si usa il giornale "Acquisto" e con quale costo
- [ ] Chiedere a Stefano cosa sono il carico "1" del 03/02 e la rettifica MAG26-0266 del 13/07
- [ ] Far verificare al commercialista l'obbligo delle scritture ausiliarie di magazzino
- [ ] Archiviare le evidenze dalla E154 in poi (movimenti del motore, registri del 24/05, table 904, fatture su conto, giroconti delle rimanenze, articoli ML non di inventario)

## Versioni

- Velo-CE - Giro reale dei materiali in BC - INTERNO - v001.md · 2026-10-08 · prima versione ingerita (rilevazione del 05/10/2026; data di modifica dovuta alla riorganizzazione della cartella)
