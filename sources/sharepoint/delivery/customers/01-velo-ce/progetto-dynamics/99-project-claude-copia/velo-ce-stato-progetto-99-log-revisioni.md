---
type: source-doc
source: sharepoint
family: velo-ce-stato-progetto-99-log-revisioni
current:
  item_id: 01EFCYUZ5VRUD5W5OLMZEKSLK2RYJNSLYQ
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ5VRUD5W5OLMZEKSLK2RYJNSLYQ
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/99 Project Claude (copia)/velo-ce-stato-progetto-99-log-revisioni.md
  name: velo-ce-stato-progetto-99-log-revisioni.md
  last_modified: 2026-10-08T10:43:53Z
versions:
  - { name: velo-ce-stato-progetto-99-log-revisioni.md, item_id: 01EFCYUZ5VRUD5W5OLMZEKSLK2RYJNSLYQ, last_modified: 2026-10-08T10:43:53Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:25:37Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, business-central, log, cronologia, interno]
---

# Velo-CE · Stato progetto, blocco 99 · Log revisioni

## Riassunto

Registro delle revisioni dello stato progetto Velo-CE, scritto solo in aggiunta: una riga per versione, dalla 001 dell'08/09/2026 alla 025.66 dell'08/10/2026 (circa 90 righe). È la cronologia più completa del progetto: per ogni versione dice che cosa è stato verificato o deciso, quali blocchi sono cambiati e quali file sono stati prodotti. Permette di ricostruire la sequenza delle prove a sistema, delle decisioni del cliente e di Cristian, dei materiali per So Smart e per il cliente, e anche gli incidenti di lavoro (collisione fra sessioni del 29-30/09).

## Punti chiave

- **08/09**: prima stesura dal documento di base del 01/09; licenza verificata Essentials, delega GDAP di So Smart, perimetro senza fiscale, commercialista e banche.
- **17-20/09 (008-019)**: prove Essentials/Premium sul tenant BlueAge in nove round; il conto lavoro in Essentials funziona con l'addebito articolo; l'app Subcontracting è gratuita; la cascata di pianificazione dipende dal metodo di riordino per livello; R01 diventa prerequisito; il calcolo del piano gira con la licenza Essentials reale del cliente (R02 chiusa).
- **21/09 (020-021)**: sottoscrizioni mensili via EOS (D12 senza scadenza), titolare amministratore globale, amministratore globale locale di So Smart, pagina 2500 bloccata anche al titolare, 25 servizi web EOS, 6 job So Smart e il job del flusso MMI.
- **22-23/09 (022-024)**: «C\Lavoro» attribuito a So Smart Application; D12 decisa Premium; So Smart resta su AMS e licenze; ricodifica ibrida per famiglia; impostazione della call con So Smart.
- **24/09 (025)**: documento diviso in blocchi; 54 app EOS censite senza la pagina 2500; flusso MMI = ordini di vendita in ingresso scritti con l'identità del titolare.
- **25/09 (025.5-025.13)**: canale ordini tramite l'app Entra «CRM» del cliente con due client esterni; registro di governance separato (decisione di Cristian); job So Smart come dispatcher per fasce; aggiornamenti notturni delle app da parte di So Smart; procedura di rilascio v004 e checklist; 124 app in Production.
- **27-29/09 (025.14-025.29)**: ripristino affidato a So Smart come tema interno; nessuna nuova richiesta di accesso; pilota Lungo su sandbox BlueAge (ciclo completo, poi modello v006 con GO per la demo); documenti per Velo-CE e So Smart sulle app; razionalizzazione delle app EOS (7 in uso, 20 componenti, 11 da chiarire, 16 senza ruolo); documentazione ufficiale EOS; questionario PS02 v007.
- **29-30/09 (025.30-025.34)**: ipotesi tenant unico e reimplementazione; trasferimento di ambiente e app EOS in un tenant nuovo (documentale); assistenza Microsoft; collisione fra due sessioni che ha sovrascritto una versione 025.31.
- **01-02/10 (025.35-025.50)**: direzione tenant unico condivisa con il cliente; mail per So Smart; fattura elettronica (Able Tech, XML generati in BC); riorganizzazione della cartella di progetto (745 file); open point unici; verbali delle riunioni del 29-30/09; mappa dei sistemi CLIENTE v003; canali d'ordine manuali confermati; conto lavoro fuori da BC.
- **04-06/10 (025.51-025.55)**: analisi delle app Accruals, PDA, Advanced Document Reporting; strade verso il tenant unico (deck v002) e strada 6; giro reale dei materiali; primo SAL mensile del 06/10.
- **07-08/10 (025.56-025.66)**: etichette in standard (layout Velo-CE, etichette da ordine d'acquisto, catalogo fornitori), guida e capitolato fornitori; autofatture e fatture di fornitori UE; piano della ripresa dati; risposta di So Smart su Premium; piano attività del nuovo ambiente (185 righe); demo del ciclo d'acquisto standard e guida per l'amministrazione.

## Numeri

- Versioni: dalla 001 (08/09) alla 025.66 (08/10/2026).
- Evidenze al 08/10: E01-E160 sul tenant del cliente, T01-T172 sul tenant BlueAge.
- Riorganizzazione della cartella del 02/10: 745 file spostati.
- Open point unici: 41 voci CT più 15 voci OP; registro di governance: 21-22 voci GOV.
- Piano attività del nuovo ambiente: 185 righe NBC; piano ripresa dati: 26 RD, 9 RQ, 5 RF.

## Decisioni e azioni

- 23/09: D12 Premium (Stefano); So Smart su AMS e licenze.
- 25/09 (Cristian): governance in registro separato.
- 26-27/09 (Cristian): ripristino a So Smart, tema interno; nessuna nuova richiesta di accesso.
- 29/09: razionalizzazione delle app con mandato di Stefano e Claudia; IVC da sostituire.
- 30/09 sera: direzione tenant unico condivisa con Stefano e Claudia.
- 02/10 (Cristian): fiscalità nel perimetro per il cambio tenant; conto lavoro fuori da BC come assunto di lavoro; nuova alberatura della cartella.
- 04/10 (Cristian): domande a So Smart in una lista snella per la call del 06/10.
- 07/10: orientamento alla reimplementazione; So Smart garantisce app fiscali, connettori e AMS anche in Premium (da confermare per iscritto).
- [ ] Ripristinare le modifiche perse della versione 025.31 di un'altra sessione (blocco 03, verosimilmente §7.4 p.80-82).
- [ ] Riallineare i blocchi 06 (§12.2, §13) con i fatti del 02/10 su portale B2B, configuratore Van Nicholas e API So Smart.
- [ ] Aggiornare gli open point CT-01, CT-09, CT-11, CT-13, CT-42 e OP-01 e portare i 10 open point proposti dal piano attività.
- [ ] Allineare l'etichetta «giornale articoli» con la caption «Registrazioni magazzino» (page 40).
- [ ] Riallineare sei affermazioni della SAL 01 v002 segnalate dalla revisione del piano attività.

## Versioni

- velo-ce-stato-progetto-99-log-revisioni.md · 2026-10-08 · prima versione ingerita (log fino alla 025.66); data di modifica della riorganizzazione della cartella
