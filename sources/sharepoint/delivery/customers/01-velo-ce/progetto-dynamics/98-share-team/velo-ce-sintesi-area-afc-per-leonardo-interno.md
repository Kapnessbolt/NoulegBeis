---
type: source-doc
source: sharepoint
family: velo-ce-sintesi-area-afc-per-leonardo-interno
current:
  item_id: 01EFCYUZ2EIXRT76BHWRB37PUGYJE6XMYT
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ2EIXRT76BHWRB37PUGYJE6XMYT
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/98 Share Team/Velo-CE - Sintesi area AFC per Leonardo - INTERNO - v001.md
  name: Velo-CE - Sintesi area AFC per Leonardo - INTERNO - v001.md
  last_modified: 2026-10-08T10:43:50Z
versions:
  - { name: Velo-CE - Sintesi area AFC per Leonardo - INTERNO - v001.md, item_id: 01EFCYUZ2EIXRT76BHWRB37PUGYJE6XMYT, last_modified: 2026-10-08T10:43:50Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:31:42Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]", "[[fatturazione-elettronica-sdi]]"]
tags: [velo-ce, business-central, afc, sintesi, ciclo-passivo, interno]
---

# Velo-CE · Sintesi dell'area AFC per Leonardo

## Riassunto

Nota interna BlueAge (v001 dell'08/10/2026) che riassume per Leonardo Pinsone lo stato dell'area AFC del progetto Velo-CE, ricavata dal [[velo-ce-piano-afc-interno]], dall'[[velo-ce-indice-evidenze]] e dallo stato progetto. Riporta in breve le conclusioni (ciclo passivo scollegato, valore del magazzino fuori dalla contabilità, app EOS dell'area poco usate), le evidenze dal 04 all'08/10 per tema, la demo del ciclo d'acquisto standard fatta l'08/10 sul tenant BlueAge, le 11 migliorie, le decisioni e domande ad alta priorità ancora aperte, i documenti prodotti e i prossimi passi.

## Punti chiave

- **Ciclo passivo scollegato** (verificato): fatture di merce su conto senza numero d'ordine; carico da Registrazioni magazzino spesso a costo zero; ricevimento sull'ordine usato solo da maggio 2025 ad aprile 2026; fattura sulle righe del carico mai usata.
- **Magazzino fuori dalla contabilità**: registrazione automatica dei costi disattivata; tutte le combinazioni del setup puntano a un conto transitorio a saldo zero; le rimanenze di bilancio vengono dall'inventario fisico con un giroconto annuale (dichiarato da Stefano).
- **App EOS dell'area**: Accruals ferma dal 2023 (se esce, escono 6 app); PDA con 7 correzioni nel 2026; Advanced Document Reporting viva ogni giorno, primo candidato a passare allo standard (ma i report So Smart di DDT, fattura accompagnatoria e ordine di assemblaggio vanno rifatti comunque); IVC non serve al bilancio ma gira di notte.
- **Fatture estere**: oltre alle vendite, l'app invia allo SdI le integrazioni dei fornitori UE e le autofatture, a lotti il 15 del mese con ADMIN; la nuova app fiscale dovrà farlo dal ciclo passivo.
- **Demo dell'08/10** (Essentials, senza app): stesso acquisto registrato nei due modi; con ordine, carico parziale e «Prendi righe di carico» la fattura porta il costo reale sull'articolo (13,00 contro 0,00 del carico a mano). Guida per Claudia nella cartella delle guide. Limite: l'abbinamento della fattura elettronica importata dipende dall'app fiscale.
- **Decisioni aperte**: piano dei conti pulito con un conto per banca; ciclo acquisti collegato; data della conta di fine anno; DDT di dicembre 2026.

## Numeri

- 11 migliorie; 15 decisioni e domande ad alta priorità aperte; 41 open point AFC.
- Costo AMFR da assemblaggio: 990,00 euro per 200 pezzi (4,95 euro al pezzo).
- Demo: ordine di 40 pezzi a 12,50, carico parziale di 30, carichi non fatturati 457,50, fattura a 13,00.
- 29 accrediti Stripe registrati a mano ad agosto 2026; 10 ubicazioni in Production.
- Integrazioni e autofatture inviate allo SdI dal 12/02/2023.

## Decisioni e azioni

- [ ] Intervista con Claudia sulle domande ad alta priorità, partendo da AFC-OP37 (perché da aprile 2026 non si riceve più sull'ordine) e AFC-OP26
- [ ] Call con So Smart su AFC-OP28 (import della fattura elettronica) e AFC-OP24 (contratto Able Tech)
- [ ] Decidere con Stefano ciclo acquisti (AFC-OP30) e conta di fine anno (AFC-OP40)
- [ ] Decidere con il commercialista fatture differite (AFC-OP41) e registro di magazzino (AFC-OP31)
- [ ] Misurare la quota di acquisti da fornitori italiani contro esteri per pesare la fase 2 (AFC-MG11)

## Versioni

- Velo-CE - Sintesi area AFC per Leonardo - INTERNO - v001.md · 2026-10-08 · prima versione ingerita; data di modifica della riorganizzazione della cartella
