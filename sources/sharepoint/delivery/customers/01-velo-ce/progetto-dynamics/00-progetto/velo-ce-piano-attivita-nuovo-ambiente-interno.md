---
type: source-doc
source: sharepoint
family: velo-ce-piano-attivita-nuovo-ambiente-interno
current:
  item_id: 01EFCYUZ6HSI2ZXMOWNRH2PGTDI6ZENUEE
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ6HSI2ZXMOWNRH2PGTDI6ZENUEE
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Cristian/00 Progetto/Velo-CE - Piano attività nuovo ambiente - INTERNO - v001.xlsx
  name: Velo-CE - Piano attività nuovo ambiente - INTERNO - v001.xlsx
  last_modified: 2026-10-27T05:19:47Z
versions:
  - { name: "Velo-CE - Piano attività nuovo ambiente - INTERNO - v001.xlsx", item_id: 01EFCYUZ6HSI2ZXMOWNRH2PGTDI6ZENUEE, last_modified: 2026-10-27T05:19:47Z }
  - { name: "Velo-CE - Piano attività nuovo ambiente - INTERNO - v001.xlsx", item_id: 01EFCYUZ6RIEAUZIVBTFALWN7QUVTPOXUO, last_modified: 2026-10-07T17:32:19Z }
also_at: []
status: active
partial: true
ingested_at: 2026-10-29T06:00:34Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]", "[[fatturazione-elettronica-sdi]]"]
tags: [piano, go-live, premium, cut-over, percorso-critico, interno]
---

# Velo-CE · Piano attività del nuovo ambiente Business Central (INTERNO)

## Riassunto

Piano interno BlueAge (v001 del 07/10/2026, registro vivo, non mostrabile al cliente né a So Smart) di tutto ciò che va deciso, raccolto, configurato, caricato, provato e insegnato per avviare il nuovo Business Central Premium nel tenant di Velo-CE (veloe.eu), dai primi setup fino all'avvio dell'08/01/2027 e ai rilasci R2-R4. È il primo blocco del piano di progetto in Excel (OP-01 del registro [[velo-ce-open-point-interno]]): 185 righe NBC con chi esegue, chi decide, fase, data proposta, prerequisiti, dove in BC, strada ed edizione. Nasce da tre analisi parallele (piattaforma e partner; società, contabilità e fiscale; magazzino, acquisti, produzione e dati) e da una revisione indipendente, documentata in un foglio di note. Letto in parte: il foglio Attività si interrompe a NBC-172, le righe NBC-173…NBC-185 non sono state lette.

## Punti chiave

- **Calendario (dal SAL 01 del 06/10)**: scelta della strada il 30/10; saldi al 01/01/2027; inventario e avvio R1 l'08/01/2027; rilasci R2-R4 febbraio-aprile; cicli e pianificazione da maggio.
- **Fasi**: R0-a ambiente pronto (entro 31/10) · R0-b setup di base e prove (entro 30/11) · R0-c configurazione completa, caricamenti di prova, prova generale e formazione (entro 18/12) · R1 avvio (08/01/2027) · R2-R4 (entro 30/04/2027) · Dopo (da maggio).
- **Fatti su cui poggia** (dichiarati da Cristian il 07/10): So Smart garantisce le app fiscali EOS, l'AMS e i connettori anche in Premium e dà supporto sull'ambiente tranne la configurazione della produzione, che segue BlueAge. Non confermati: chi installa le app nel nuovo tenant e il canale delle licenze. Orientamento alla reimplementazione in un ambiente nuovo, con in valutazione l'alternativa «Due società» (trasferimento dell'ambiente attuale più società nuova).
- **Percorso critico (15 passi, 32 righe)**: amministratore globale interno di veloe.eu e MFA (17/10) → canale licenze e prima licenza Premium (24/10) → autonomia e utenze BlueAge, sandbox Premium (24-31/10) → scelta di strada e partner con conferma scritta di So Smart (30/10) → regola di codifica (30/10) → commercialista e regola di taglio fiscale (31/10-13/11) → società definitiva in esperienza Premium (07/11) → prova del conto lavoro e ubicazioni (14/11) → abbonamenti e app EOS (14/11) → modelli articolo e articoli con il vecchio codice (21/11-04/12) → fattura elettronica configurata e provata (27/11-04/12) → distinte di R1, prove end-to-end e UAT (04-11/12) → prova generale tecnica e fiscale (18/12) → piano di cut-over e go/no-go (18/12) → partite aperte, go/no-go, inventario e giacenze (07-08/01/2027).
- **Decisioni del cliente con data limite**: amministratore interno (17/10), dove avviare le procedure d'acquisto (17/10), autonomia BlueAge e canale licenze (24/10), strada e partner e regola di codifica (30/10), nome della società (31/10, irreversibile online), varianti e codici colore (06/11), documenti con app EOS ADR o standard (07/11), piano dei conti, dimensioni, magazzino in contabilità, metodo di costo e regola di taglio (13/11), ubicazioni (14/11), ritenute, Intrastat e plafond, settimana 01-08/01 e registrazioni in reparto (27/11), vecchio BC dopo il passaggio (11/12).
- **Fattura elettronica**: bloccante per R1; lo standard esporta l'XML ma non trasmette né importa e l'e-documents per lo SdI non sarà pronto a gennaio; il setup di EX063 è a So Smart; il collegamento della conservazione in Premium è da rilevare.
- **Taglio fiscale**: dal 01/01/2027 tutti i documenti 2027 nascono nel nuovo BC; dal vecchio restano differite e autofatture di dicembre, liquidazione, acconto e bollo del quarto trimestre; fra 01/01 e 08/01 ci sono tre giorni lavorativi senza giacenze nel nuovo BC.
- **Open point proposti dalla revisione (10)**: chi installa le app EOS, GDAP del nuovo tenant, confine fra BlueAge e So Smart sulla configurazione non di produzione, utenze BlueAge, SMTP del BC di oggi (autenticazione di base disattivata a fine dicembre 2026), verniciatore del 2026, chiusura di inizio gennaio, etichette collo, postazioni e stampa in reparto, distinte bici a R4.
- **Contraddizioni con la SAL 01 per il cliente**: imballo nella distinta del sabbiato, scorta sui colori classici, amministratore interno, verniciatore, posizione di So Smart su Premium superata dai fatti del 07/10, date sulle righe delle distinte di assemblaggio (non esistono), CU fra le app in uso, funzioni presentate al cliente senza prova.
- **Aggiornamenti fino al 27/10**: dal 15/10 il foglio «Ambiente base» con la sequenza fino a «pronto per caricare», partendo subito da una sandbox BlueAge (opzione 3 confermata, [[velo-ce-stato-progetto-03-decisioni-aperte]]); le righe NBC passano da 185 a 189; il tenant di destinazione indicato come `veloe.eu` va letto `velo-ce.eu` (decisione del 20/10).

## Numeri

- 189 attività al 27/10 (185 al 07/10): per fase 21 R0-a, 72 R0-b, 72 R0-c, 17 R1, 3 R2-R4, 4 Dopo; tutte ancora «Da fare» nel foglio di riepilogo.
- Per esecutore (27/10): BlueAge 83, Cliente 77, So Smart 9, Commercialista 3, Fornitore del client 2, Partner licenze 1, Da decidere 14.
- Per tipo (27/10): 51 decisioni, 16 informazioni, 82 attività a sistema, 16 caricamenti dati, 17 test, 7 formazione.
- 32 righe sul percorso critico; la regola di codifica blocca circa 38 righe a cascata.
- Bollo virtuale 2,00 euro sulle fatture senza IVA sopra 77,47 euro; prova EOS di 20 giorni non sufficiente; aggiornamento principale di aprile 2027 = versione 30.0.

## Decisioni e azioni

- [ ] Cliente: amministratore globale interno di veloe.eu e titolare dell'MFA (NBC-001) 📅 2026-10-17
- [ ] Cliente: dove avviare subito le procedure d'acquisto (NBC-021) 📅 2026-10-17
- [ ] Cliente: canale delle licenze e acquisto della prima licenza Premium (NBC-003, NBC-006) 📅 2026-10-24
- [ ] Cliente: decisione scritta sull'autonomia di BlueAge nella configurazione (NBC-010) 📅 2026-10-24
- [ ] Cliente: scelta della strada e del partner per il nuovo ambiente (NBC-007) 📅 2026-10-30
- [ ] Cliente: regola di codifica, nomenclatura e descrizioni (NBC-064) 📅 2026-10-30
- [ ] BlueAge: creare la sandbox Premium di prova (NBC-014) 📅 2026-10-31
- [ ] Cliente: nome della società nel nuovo ambiente (NBC-019) 📅 2026-10-31
- [ ] BlueAge: società definitiva e passaggio in esperienza Premium (NBC-016, NBC-037, NBC-023) 📅 2026-11-07
- [ ] Commercialista: regola di taglio fiscale e metodo dei saldi d'apertura (NBC-089, NBC-090) 📅 2026-11-13
- [ ] So Smart: abbonamenti EOS sul Tenant ID di veloe.eu e installazione delle app (NBC-024, NBC-025) 📅 2026-11-14
- [ ] So Smart: setup della fattura elettronica EX063 nella nuova società (NBC-115) 📅 2026-11-27
- [ ] BlueAge: prova del ciclo della fattura elettronica senza invii reali (NBC-117) 📅 2026-12-04
- [ ] Prove end-to-end di R1 e UAT con gli utenti chiave (NBC-153, NBC-154) 📅 2026-12-11
- [ ] Prova generale e piano di cut-over con criteri di go/no-go (NBC-155, NBC-151, NBC-158) 📅 2026-12-18
- [ ] Decisione di go/no-go dell'avvio (NBC-178) 📅 2027-01-07
- [ ] Inventario e giacenze d'apertura, avvio R1 (NBC-169) 📅 2027-01-08
- [ ] Portare nel registro degli open point i 10 open point proposti dalla revisione

## Versioni

- Velo-CE - Piano attività nuovo ambiente - INTERNO - v001.xlsx · 2026-10-07 · prima versione ingerita; lettura parziale del foglio Attività (fino a NBC-172 di 185), letti per intero gli altri sei fogli
- Velo-CE - Piano attività nuovo ambiente - INTERNO - v001.xlsx · 2026-10-27 · registro aggiornato sul posto: foglio «Ambiente base» (15/10), 189 righe NBC (letti Leggimi e Riepilogo); nella cartella `Cristian/00 Progetto/`

