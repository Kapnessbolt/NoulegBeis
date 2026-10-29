---
type: source-doc
source: sharepoint
family: velo-ce-stato-progetto-01-inquadramento-ambiente
current:
  item_id: 01EFCYUZ2AQVYH6QUXYND3XMXYVVPPTTRA
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ2AQVYH6QUXYND3XMXYVVPPTTRA
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/99 Project Claude (copia)/velo-ce-stato-progetto-01-inquadramento-ambiente.md
  name: velo-ce-stato-progetto-01-inquadramento-ambiente.md
  last_modified: 2026-10-28T08:06:16Z
versions:
  - { name: velo-ce-stato-progetto-01-inquadramento-ambiente.md, item_id: 01EFCYUZ2AQVYH6QUXYND3XMXYVVPPTTRA, last_modified: 2026-10-28T08:06:16Z }
  - { name: velo-ce-stato-progetto-01-inquadramento-ambiente.md, item_id: 01EFCYUZ3MUEM32WVBQRHZKSGTLF2AKPUO, last_modified: 2026-10-08T10:43:53Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-29T05:57:56Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, business-central, ambiente, licenze, essentials, premium, so-smart, interno]
---

# Velo-CE · Stato progetto, blocco 01 · Inquadramento, ambiente e vincoli di sistema

## Riassunto

Blocco 01 (§1-§2) dello stato progetto Velo-CE, interno BlueAge. Inquadra il cliente (produttore di biciclette con i brand Veloe e Van Nicholas), la natura del progetto (riconduzione allo standard di un Business Central in uso dal 2023 con il partner So Smart, non un'implementazione) e le persone coinvolte. Raccoglie i fatti verificati sul tenant: licenze Essentials, canale d'acquisto tramite EOS, ambienti, utenti, estensioni, setup magazzino, funzioni disponibili e non possedute. Documenta le prove a sistema sul perimetro Essentials/Premium fatte sul tenant BlueAge (conto lavoro, costo dell'assemblato, cascata di pianificazione, pilota Lungo), le prove sugli accessi, i job schedulati e il censimento delle app EOS.

## Punti chiave

- **Natura del progetto**: non è un'implementazione ERP ma una riconduzione allo standard, pezzo per pezzo; dopo l'8 settembre il baricentro è la governance dei sistemi e dei fornitori (Velo-CE non possiede né amministra l'infrastruttura su cui gira).
- **Perimetro deciso l'08/09**: esclusi fatturazione elettronica e SDI, rapporto con il commercialista e flussi bancari; dentro ciclo commerciale, produzione, magazzino, costo di prodotto e governance dei sistemi.
- **Criterio di ammissibilità**: ogni personalizzazione si tiene se serve al business, non se nel 2023 era la via più veloce.
- **Metodo**: seguire una bici dall'inizio alla fine; piloti scelti il 15/09: bici Veloe Multi Lungo Bosch CX (MLCA-5E-545-CDX), bici Van Nicholas Backroads e-Performance MY26 (V26BEP52), portapacchi anteriore AMFR.
- **Orizzonte**: chiudere tutto entro dicembre 2026 non è realistico; l'obiettivo è instradare entro dicembre i blocchi di valore perché il 2027 parta con il sistema in ordine; nel 2027 controllo di gestione, marginalità e reportistica.
- **Tenant**: creato da So Smart nel 2021, senza dominio proprio; licenza Essentials (3 utenti), sottoscrizioni mensili acquistate tramite il rivenditore EOS Online (società di So Smart): ogni modifica passa da EOS. Costo dichiarato 768 euro al mese contro circa 270-300 di listino Microsoft, differenza non spiegata (L06).
- **Ambienti**: Production più tre sandbox (Educational, Educational2906, TestTemp1509); quota piena. Production alla 28.5, Partner Access aperto a tutti i partner, nessun gruppo di sicurezza.
- **Accessi**: So Smart ha delega GDAP e un account locale con ruolo di amministratore globale nel tenant; BlueAge entra con un'utenza propria senza licenza, con ruoli di amministrazione BC e lettura globale. 21 utenti BC contro 3 licenze; magazzino e assemblaggio lavorano senza utenza nominale; profilazione assente.
- **Setup magazzino**: registrazione automatica costi disattivata (magazzino e contabilità scollegati), costing FIFO, giacenza negativa vietata ma rettifiche libere: AMFR da giugno 2026 si carica con rettifiche positive invece che con assemblaggi.
- **Essentials vs Premium (prove su tenant BlueAge)**: la pianificazione MRP con esplosione delle distinte è nel diritto d'uso Essentials (provato anche sul tenant del cliente il 20/09); la cascata su più livelli dipende dal metodo di riordino per livello, non dalla licenza; in Essentials il conto lavoro si gestisce con ubicazione terzista, trasferimento e addebito articolo (la fattura del terzista entra nel costo); Premium aggiunge davvero ordini di produzione con cicli e capacità, fasi misurate, scarto, distinta fantasma, conto lavoro gestito (app Microsoft Subcontracting, gratuita) e Assistenza.
- **Pilota Lungo**: modello v004 caricato su sandbox BlueAge per la demo del 29/09 con ciclo completo ordine → bici registrato; modello v006 caricato in una società in esperienza Premium (GO per la demo); con il modello v008 di Leonardo (consuntivazione manuale su tutti i centri, tre tariffe, housing da foglio) i numeri delle prove vanno rifatti.
- **Accessi (round 6)**: ruoli Entra e set di autorizzazioni BC sono strati separati; la pagina Gestione estensioni (2500) resta chiusa anche al titolare con licenza: domanda aperta a So Smart (R11).
- **Job schedulati**: sei job So Smart (dispatcher per fasce) e il job del flusso MMI ogni 2 minuti; quattro job in errore da oltre due anni (indicatore di manutenzione assente).
- **Flusso MMI**: canale automatico degli ordini di vendita (anche bici Veloe complete), scritto da due client esterni tramite l'app «CRM» con l'identità del titolare: rischio di governance (un cambio di password o MFA può fermare gli ordini) e vincolo sulla ricodifica (il canale usa il numero articolo di BC senza traduzione).
- **Aggiornamenti dal 08/10 al 27/10** ([[velo-ce-stato-progetto-99-log-revisioni]]): posta su tre tenant Microsoft 365, tenant unico per BC e posta deciso il 20/10: `velo-ce.eu` (§2.1); nuovo §2.5 j) del 27/10 sull'import del master articoli v005 nella società di prova VC-IMPORT PROVA del tenant BlueAge con i pacchetti di configurazione (136 articoli, distinte, conti delle nuove categorie con il pacchetto VC-CONTI-01), con il limite che il pacchetto creato da Excel scrive anche i campi assenti.

## Numeri

- Licenze: 3 Essentials assegnate, 2 Team Members non assegnate, Power BI Pro 2 (usato da 3 persone).
- Circa 1.100 articoli a sistema (1.112 nell'estrazione dell'08/09); 1.263 righe di distinta di assemblaggio, 10 ordini di assemblaggio aperti, 571 registrati.
- Premium: +26 euro per utente al mese a listino (impegno annuale).
- Conto lavoro in Essentials, prova: costo unitario da 74,86 a 86,86 con l'addebito del terzista.
- 124 app in Production (54 EOS, 70 Microsoft); 117 servizi web pubblicati, 25 custom EOS; 16 job in coda.
- Ordine OVC26-1358 seguito nel flusso MMI: bici 1.940 euro + colore custom 50 + portapacchi 45.

## Decisioni e azioni

- 08/09: perimetro dell'analisi senza fatturazione elettronica, commercialista e banche.
- 15/09: scelti i tre piloti.
- 20/09: decaduta la regola di non appoggiare la quotazione sull'MRP in Essentials; non serve più la richiesta scritta a Microsoft (R02).
- 21/09 (Cristian): niente SUPER all'utenza BlueAge; il blocco della pagina 2500 va portato come domanda a So Smart (R11).
- [ ] Estrazione articoli con sistema di rifornimento, distinta, metodo di costing, costo, tipo e metodo di riordino (V05a).
- [ ] Prova di esplosione della distinta in Essentials su un articolo con metodo di riordino (da autorizzare: tocca un dato del cliente in copia).
- [ ] Verificare la sorgente dei report Power BI aprendo un file .pbix (S07).
- [ ] Caricare il modello v008 in una società nuova (proposta, non decisa).

## Versioni

- velo-ce-stato-progetto-01-inquadramento-ambiente.md · 2026-10-08 · prima versione ingerita (stato progetto 025.66); data di modifica della riorganizzazione della cartella
- velo-ce-stato-progetto-01-inquadramento-ambiente.md · 2026-10-28 · stato progetto 025.109 del 27/10; tenant velo-ce.eu e §2.5 j) sull'import del master articoli (differenze ricavate dal log revisioni, blocco non riletto per intero); copia della cartella in `Cristian/`

