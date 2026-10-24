---
type: source-doc
source: onedrive
family: manini-ddt-essenziale
current:
  item_id: 013UYHJHCY44X6NSPPYNF24EAWAYK64P35
  uri: file:///b!2fHSoBOOE0aRvS_GntS6s6RJcyNKjAJMiRtoiZ6n5xzp8hWMRRoMQKOVYgftTbzT/013UYHJHCY44X6NSPPYNF24EAWAYK64P35
  web_url: https://blueagesrl-my.sharepoint.com/personal/lorenzo_curione_blueage_it/Documents/BlueAge/01_Materiale clienti/Manini/manini_ddt_essenziale.md
  name: manini_ddt_essenziale.md
  last_modified: 2026-10-23T12:51:23Z
versions:
  - { name: manini_ddt_essenziale.md, item_id: 013UYHJHCY44X6NSPPYNF24EAWAYK64P35, last_modified: 2026-10-23T12:51:23Z }
  - { name: manini_ddt_essenziale.md, item_id: 013UYHJHCY44X6NSPPYNF24EAWAYK64P35, last_modified: 2026-10-23T12:04:17Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-24T04:52:15Z
projects: ["[[manini-automazione-ddt]]"]
clients: ["[[manini]]"]
topics: ["[[ai-nei-processi]]"]
tags: [entrata-merci, ddt, sintesi]
---

# Manini · caso DDT / entrata merci, l'essenziale

## Riassunto

Sintesi in una pagina del progetto [[manini-automazione-ddt]], aggiornata al 23/10/2026: raccoglie le due sessioni di lavoro su claude.ai (21 e 22/10) e i report 01–04. Distingue ciò che ha detto [[manini]], ciò che viene dal deck di [[leonardo-pinsone]] e ciò che è analisi BlueAge non ancora validata. Copre persone, vincoli del corso ([[corso-ai-manini]]), dati del campione, benchmark, matching simulato ([[05-matching]]), posizioni prese, business case, piano aula, stato degli step, domande aperte e lezioni riusabili. Il master è nel repo GitHub `manini-automazione-ddt`; questa è la copia condivisa.

## Punti chiave

- Il collo di bottiglia è l'abbinamento con ordini e codici, non la lettura: un modello generativo capace legge tutti i 15 DDT del campione
- In simulazione, con l'ordine sul DDT l'abbinamento si automatizza senza errori; il limite diventa il processo, con un tetto di 10 DDT pronti su 15 anche con matching perfetto
- Scrittura su AS400 con tabella di staging e programma RPG di import, mai INSERT diretto; Power Automate come spina dorsale, agente Copilot Studio solo per le eccezioni
- Pilota in tre fasi: dati (2 settimane), in ombra solo Aprilia (4–6 settimane), scrittura in staging
- Audience: il magazzino, che registra i DDT, non è in nessun gruppo del corso; il caso DDT funziona per il gruppo A e per l'IT, per B e C serve un caso preventivi
- Lezioni riusabili: prima i dati e poi il deck; "trascrivi, non dedurre" con possibilità di rifiutare il documento; scegliere il modello capace; controlli deterministici per gli errori strutturali; benchmark onesti

## Numeri

- Circa 12.100 DDT/anno (11.160 sugli stabilimenti): Bastia 530/mese, Aprilia 400/mese, cantiere circa 80/mese
- Campione: 15 DDT, 14 fornitori, 0 PDF nativi; ordine Manini in 10 su 15; codice Manini esplicito in 2 su 15
- Benchmark sui campi critici: modello standard 100%, modello veloce 88%, OCR classico 27%
- Business case deck v3: 1.860 ore oggi, 911 (prudente) o 521 (spinto); risparmio 33–47 k€/anno
- Costo AI stimato: 35–50 Copilot Credits a DDT, circa 4–5,6 k$/anno
- Matching simulato: 5–7 DDT pronti su 15 all'avviamento con politica automatica, 6–7 a regime; risparmio sul campione 22–26 k€/anno

## Decisioni e azioni

- [x] Step 4: matching contro un CSV ordini simulato, con distrattori e due scenari di tabella codici ([[05-matching]])
- [ ] Ritestare il prompt v1.1
- [ ] Prova delle demo con Angelo Santilli 📅 2026-11-05
- [ ] Domande aperte a Manini: significato del "Mov." sull'etichetta, DDT della pesa di Bastia, web service o import su AS400, gateway dati, ambiente Power Platform, estratti di dati

## Versioni

- manini_ddt_essenziale.md · 2026-10-23 12:51 · aggiunti la sezione 5b sul matching simulato, lo step 4 fatto e i file del matching
- manini_ddt_essenziale.md · 2026-10-23 · prima versione completa (21–22/10); corretti in sessione i nomi di Angelo Santilli e Cristian Schifone (Trif), sezione 12 sui file aggiornata al repo
