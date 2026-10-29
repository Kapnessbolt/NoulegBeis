---
type: source-doc
source: sharepoint
family: velo-ce-piano-ripresa-dati-interno
current:
  item_id: 01EFCYUZ45ABRXUWVOZZEIFLHIECSEJD7E
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ45ABRXUWVOZZEIFLHIECSEJD7E
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/00 Progetto/Velo-CE - Piano ripresa dati - INTERNO - v001.xlsx
  name: Velo-CE - Piano ripresa dati - INTERNO - v001.xlsx
  last_modified: 2026-10-08T07:59:37Z
versions:
  - { name: Velo-CE - Piano ripresa dati - INTERNO - v001.xlsx, item_id: 01EFCYUZZHZIFH3MEBO5DJCYOEUSMIKJGA, last_modified: 2026-10-08T07:59:37Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:25:33Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [ripresa-dati, migrazione, saldi-apertura, cut-over, interno]
---

# Velo-CE · Piano della ripresa dati al 01/01/2027 (INTERNO)

## Riassunto

Piano interno BlueAge (v001 del 07/10/2026, non mostrabile al cliente) che elenca, oggetto per oggetto, cosa si porta dal Business Central di oggi al nuovo tenant: come entra, da quale pagina si estrae, con quale strumento, chi lo fa, in quale fase e con quale quadratura si controlla. Propone il metodo di apertura da decidere con il commercialista: bilancio 2026 chiuso nel BC di oggi e nel nuovo solo lo stato patrimoniale d'apertura, in due tempi contro un conto transitorio. Contiene 26 oggetti RD, 9 quadrature RQ e 5 fasi di prova RF; le righe di ripresa del [[velo-ce-piano-attivita-nuovo-ambiente-interno]] coprono gli stessi oggetti e vanno riconciliate.

## Punti chiave

- **Metodo proposto**: T1 alla partenza (partite aperte di clienti e fornitori, banche, giacenze e documenti aperti contro il conto transitorio d'apertura); T2 a bilancio 2026 chiuso (altri saldi patrimoniali definitivi contro lo stesso conto, che torna a zero). Alternativa: apertura provvisoria completa e rettifica per differenza.
- **Regole**: i conti collettivi non si caricano con il saldo ma dalle righe di dettaglio; le banche si aprono con un movimento del conto bancario, mai sul conto C/G; si riportano solo i documenti davvero aperti; ogni caricamento si prova prima in sandbox; dal BC di oggi si estrae soltanto, senza scritture.
- **Strumenti BC**: «Apri in Excel» per estrarre, pacchetti di configurazione (RapidStart) per anagrafiche e documenti, funzioni che creano le righe di giornale da completare in Excel.
- **Anagrafiche (RD01-RD09)**: piano dei conti pulito con raccordo; dimensioni; conti bancari; clienti e fornitori (anagrafica dichiarata quasi a posto; IBAN dei fornitori da controllare); articoli con il nuovo codice (in corso, impatto della ricodifica sul flusso MMI e sugli oggetti So Smart da verificare); distinte di assemblaggio (in corso); ubicazioni; riferimenti e listini.
- **Saldi e partite (RD10-RD16)**: partite aperte con numero, data e scadenza originali; giacenze dalla conta fisica e non dalle quantità di BC (non affidabili); saldi degli altri conti a chiusura 2026; cespiti oggi fuori da BC; IVA a cavallo d'anno con liquidazione di dicembre nel BC di oggi.
- **Documenti aperti (RD17-RD21)**: il «ricevuto non fatturato» di BC non è reale e entra come saldo fatture da ricevere; ordini d'acquisto da ripulire (27 aperti da maggio 2026, nessuno ricevuto); ordini di vendita con il canale ordini da ripuntare; fatture differite di dicembre da decidere con il commercialista; ordini di assemblaggio da chiudere entro il 31/12.
- **Fuori dalla partenza**: dati delle app EOS e So Smart da decidere app per app (RD23); cicli e produzione nel 2027 (RD24); storico 2023-2026 e saldi mensili non si riprendono (consultazione nel BC di oggi, estrazione per Power BI).
- **Nodo giacenze**: oggi la conta si fa a gennaio; se il nuovo BC parte prima, le prime settimane girano senza giacenze. Da decidere: conta entro il 31/12 o carico provvisorio e rettifica.

## Numeri

- 26 oggetti RD: 13 da avviare, 9 prematuri, 2 in corso, 2 esclusi; 9 quadrature; 5 fasi.
- 669 articoli a costo zero nell'estrazione; 1.263 righe di componenti distinta nell'ambiente Educational; circa 180 componenti nel pilota fra telaio e bici completa.
- 10 ubicazioni in Production, di cui 9 per merce presso terzi o in viaggio.
- Un ordine con 157.136 euro ricevuti e mai fatturati; un ordine d'acquisto con 9.044 euro inevasi; 27 ordini d'acquisto aperti da maggio 2026.
- Tabelle FTE: 512.788 righe, circa 1,1 GB.
- Fasi: RF0 anagrafiche ottobre-novembre 2026; RF1 prima prova a fine novembre con dati al 31/10; RF2 prova generale cronometrata a metà dicembre con dati al 30/11; RF3 partenza nei primi giorni lavorativi di gennaio 2027 (avvio R1 proposto l'08/01/2027); RF4 saldi definitivi a chiusura 2026 (data dal commercialista).

## Decisioni e azioni

- Il metodo di apertura è una proposta BlueAge da decidere con il commercialista (CT-26).
- [ ] Decidere con il commercialista la gestione delle fatture differite di dicembre (prima di dicembre)
- [ ] Decidere la data della conta di magazzino (entro il 31/12 o carico provvisorio con rettifica)
- [ ] Verificare l'impatto della ricodifica degli articoli su flusso MMI, API e oggetti So Smart prima del caricamento
- [ ] Chiudere nel BC di oggi gli ordini d'acquisto già evasi e gli ordini di assemblaggio entro il 31/12
- [ ] Riconciliare le righe di ripresa con il piano attività del nuovo ambiente
- [ ] Prima prova di ripresa in sandbox con dati al 31/10 (RF1, fine novembre 2026)
- [ ] Prova generale cronometrata con dati al 30/11 (RF2, metà dicembre 2026)

## Versioni

- Velo-CE - Piano ripresa dati - INTERNO - v001.xlsx · 2026-10-08 · prima versione ingerita; contenuto v001 del 07/10/2026
