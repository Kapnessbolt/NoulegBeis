---
type: source-doc
source: onedrive
family: manini-ddt-essenziale
current:
  item_id: 013UYHJHEWRFNHJGQO4JG37XUVRX6UUVDG
  uri: file:///b!2fHSoBOOE0aRvS_GntS6s6RJcyNKjAJMiRtoiZ6n5xzp8hWMRRoMQKOVYgftTbzT/013UYHJHEWRFNHJGQO4JG37XUVRX6UUVDG
  web_url: https://blueagesrl-my.sharepoint.com/personal/lorenzo_curione_blueage_it/Documents/BlueAge/01_Materiale clienti/Manini/Progetto Automazione/Library/essenziale.md
  name: essenziale.md
  last_modified: 2026-10-25T22:18:22Z
versions:
  - { name: essenziale.md, item_id: 013UYHJHEWRFNHJGQO4JG37XUVRX6UUVDG, last_modified: 2026-10-25T22:18:22Z }
  - { name: manini_ddt_essenziale.md, item_id: 013UYHJHCY44X6NSPPYNF24EAWAYK64P35, last_modified: 2026-10-23T12:51:23Z }
  - { name: manini_ddt_essenziale.md, item_id: 013UYHJHCY44X6NSPPYNF24EAWAYK64P35, last_modified: 2026-10-23T12:04:17Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-26T05:53:02Z
projects: ["[[manini-automazione-ddt]]"]
clients: ["[[manini]]"]
topics: ["[[ai-nei-processi]]"]
tags: [entrata-merci, ddt, sintesi]
---

# Manini · caso DDT / entrata merci, l'essenziale

## Riassunto

Sintesi in una pagina del progetto [[manini-automazione-ddt]], aggiornata al 25/10/2026. Il master è `report/essenziale.md` nel repo GitHub `manini-automazione-ddt`; la copia condivisa è nella Library di `Progetto Automazione`. Fino al 23/10 la copia stava nella cartella Manini come `manini_ddt_essenziale.md`, cancellata il 26/10 perché superata. Rispetto ad allora aggiunge il ritest del prompt v1.1 ([[04-benchmark]]) e il matching sull'estrazione reale ([[05-matching]]). Distingue ciò che ha detto [[manini]], ciò che viene dal deck di [[leonardo-pinsone]] e ciò che è analisi BlueAge non ancora validata; copre persone, vincoli del [[corso-ai-manini]], dati del campione, benchmark, matching, posizioni prese, business case, piano aula, stato degli step, domande aperte e lezioni riusabili.

## Punti chiave

- La lettura è risolta con un modello generativo capace: il prompt v1.1, ritestato il 25/10, porta il modello standard a 15/15 DDT pronti e 14/15 perfetti; il veloce sale ma resta sotto e legge male la quantità dello scontrino termico
- Sull'estrazione reale il matching regge: con il modello standard nessun DDT cambia stato e 0 abbinamenti automatici errati (H29 chiusa); due correzioni al motore prima del pilota (H33, H34)
- Gli errori che arrivano a un DDT pronto sono tutti in `campi_incerti`: regola di flusso "campo critico incerto → verifica" (H30)
- Il limite resta il processo: tetto di 10 DDT pronti su 15 anche con matching perfetto
- Scrittura su AS400 con staging e programma RPG di import; Power Automate come spina dorsale, Copilot Studio solo per le eccezioni; pilota in tre fasi
- Audience: il magazzino non è in nessun gruppo del corso; per i gruppi B e C serve un caso preventivi
- Lezioni operative nuove: benchmark con subagenti (standard = Sonnet, veloce = Haiku) ed estrazione alla cieca; controllare le attività pianificate create per errore dai subagenti
- Dal 23/10 il master di report e kit è nel repo GitHub `manini-automazione-ddt`; i dati reali restano su OneDrive in `Dati/`

## Numeri

- Circa 12.100 DDT/anno (11.160 sugli stabilimenti); campione di 15 DDT, 14 fornitori, 0 PDF nativi
- Benchmark v1.1, campi critici: standard 100%, veloce 98%; DDT pronti 15/15 e 11/15; v1.0: 100% e 88%, OCR classico 27%
- Matching simulato: 5–7 DDT pronti su 15 all'avviamento con politica automatica, 6–7 a regime; risparmio sul campione circa 630–740 ore/anno (22–26 k€) contro 949 ore (33 k€) del prudente del deck
- Corso utenti: 3 gruppi da 12, date 12/11, 13/11, 26/11, 27/11, 11/12; IT: 9 persone, 40 ore (8 BlueAge, 32 Raffaele Brilli)

## Decisioni e azioni

- [x] Ritestare il prompt v1.1 (25/10, [[04-benchmark]])
- [x] Matching sull'estrazione reale (25/10, [[05-matching]])
- [ ] Correggere il motore (H33, H34) e ripetere il matching con le righe d'ordine vere
- [ ] Ritestare i candidati v1.2 del prompt prima dell'uso
- [ ] Prova delle demo con Angelo Santilli una settimana prima del 12/11
- [ ] Domande aperte a Manini: "Mov." sull'etichetta, DDT della pesa di Bastia, import su AS400 e gateway, ambiente Power Platform e crediti, estratti di dati, conferme dei formati

## Versioni

- essenziale.md (Library) · 2026-10-25 · ritest del prompt v1.1, matching sull'estrazione (§5b), stato degli step e lezioni operative; la copia passa dalla cartella Manini alla Library
- manini_ddt_essenziale.md (cartella Manini) · 2026-10-23 12:51 · aggiunti la sezione 5b sul matching simulato, lo step 4 fatto e i file del matching
- manini_ddt_essenziale.md (cartella Manini) · 2026-10-23 · prima versione completa (21–22/10); corretti in sessione i nomi di Angelo Santilli e Cristian Schifone (Trif), sezione 12 sui file aggiornata al repo
