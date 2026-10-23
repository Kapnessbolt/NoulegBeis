---
type: source-doc
source: onedrive
family: 00-istruzioni-progetto
current:
  item_id: 013UYHJHGHI3Y257QCM5E2EQC7JZDJFYPH
  uri: file:///b!2fHSoBOOE0aRvS_GntS6s6RJcyNKjAJMiRtoiZ6n5xzp8hWMRRoMQKOVYgftTbzT/013UYHJHGHI3Y257QCM5E2EQC7JZDJFYPH
  web_url: https://blueagesrl-my.sharepoint.com/personal/lorenzo_curione_blueage_it/Documents/BlueAge/01_Materiale clienti/Manini/Progetto Automazione/00_istruzioni_progetto.md
  name: 00_istruzioni_progetto.md
  last_modified: 2026-10-23T11:35:24Z
versions:
  - { name: 00_istruzioni_progetto.md, item_id: 013UYHJHGHI3Y257QCM5E2EQC7JZDJFYPH, last_modified: 2026-10-23T11:35:24Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-23T12:05:00Z
projects: ["[[manini-automazione-ddt]]"]
clients: ["[[manini]]"]
topics: ["[[ai-nei-processi]]"]
tags: [entrata-merci, ddt, brief]
---

# Manini · automazione DDT, istruzioni del progetto

## Riassunto

Brief del Project claude.ai "Automazione DDT Manini", da cui nasce [[manini-automazione-ddt]]. Fissa contesto, obiettivi in ordine e regole di lavoro del caso studio entrata merci per [[manini]], e riporta i link alle due conversazioni (21/10 "Manini case study overview", 22/10 "Automazione in ambiente Microsoft"). Dal 23/10 il contenuto è anche nel `CLAUDE.md` del repo GitHub del progetto.

## Punti chiave

- Input: ZIP di DDT reali dei fornitori; dati riservati, da non portare fuori dal sandbox
- Contesto: gestionale AS400; la tabella codice fornitore → codice Manini non esiste; l'abbinamento fattura-DDT-ordine lo propone già l'AS400; il test Sanmarco si è fermato all'integrazione
- Obiettivi: inventario, schema JSON, benchmark di estrazione, matching contro ordini simulati, output per aula, sessione IT e business case di [[leonardo-pinsone]]
- Regole: italiano, sintesi, ogni ipotesi dichiarata, report in Markdown

## Numeri

- Circa 12.100 DDT/anno: Bastia 530/mese, Aprilia 400/mese, cantiere circa 80/mese

## Decisioni e azioni

- Il collo di bottiglia dichiarato in partenza è l'abbinamento con ordini e codici, non l'OCR

## Versioni

- 00_istruzioni_progetto.md · 2026-10-23 · prima versione
