---
type: source-doc
source: onedrive
family: 02-aula-e-architettura
current:
  item_id: 013UYHJHAIDQ6JE4FJW5AYHZDQNOMLUFKI
  uri: file:///b!2fHSoBOOE0aRvS_GntS6s6RJcyNKjAJMiRtoiZ6n5xzp8hWMRRoMQKOVYgftTbzT/013UYHJHAIDQ6JE4FJW5AYHZDQNOMLUFKI
  web_url: https://blueagesrl-my.sharepoint.com/personal/lorenzo_curione_blueage_it/Documents/BlueAge/01_Materiale clienti/Manini/Progetto Automazione/Library/02_aula_e_architettura.md
  name: 02_aula_e_architettura.md
  last_modified: 2026-10-23T11:33:34Z
versions:
  - { name: 02_aula_e_architettura.md, item_id: 013UYHJHAIDQ6JE4FJW5AYHZDQNOMLUFKI, last_modified: 2026-10-23T11:33:34Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-23T12:05:00Z
projects: ["[[manini-automazione-ddt]]"]
clients: ["[[manini]]"]
topics: ["[[ai-nei-processi]]"]
tags: [entrata-merci, ddt, architettura, microsoft]
---

# Manini · caso DDT, 02 cosa portare in aula e come si implementa in Microsoft

## Riassunto

Report del 22/10/2026 per [[manini-automazione-ddt]]. Rilegge il deck entrata merci v3 di [[leonardo-pinsone]] ([[blueage-automation-entrata-merci]]) alla luce delle risposte di [[luca-zamponi]] e dell'inventario. Mappa le opzioni Microsoft strato per strato (lettura, abbinamento, persone, scrittura AS400, orchestrazione, costi) e propone un'architettura per il pilota. Definisce il laboratorio per il corso utenti, le 8 ore per i Sistemi Informativi ([[corso-ai-manini]]) e un pilota in tre fasi.

## Punti chiave

- Il deck regge come racconto, ma quattro punti vanno sistemati: niente modello AI Builder addestrato per layout; niente scrittura diretta su DB2; il 60% prudente regge solo usando le righe aperte dell'ordine come candidati; la casella "ddt@" oggi non esiste, la carta arriva col camion
- Lettura: prompt AI Builder per il pilota, nodo Extract di Copilot Studio da mostrare, Azure Content Understanding solo se serve la confidenza per campo
- Abbinamento secondo la linea di [[cristian-schifone]]: logica deterministica dove si può, AI solo dove serve giudizio; la proposta dell'AI confermata da una persona popola la tabella codici
- Scrittura AS400 raccomandata: staging su DB2 più programma RPG di import scritto dai Sistemi Informativi; RPA sul 5250 solo come ponte; lettura degli ordini aperti via gateway in sola lettura
- Laboratorio utenti di circa 2 ore nel tenant Manini con tre DDT (facile, 45 righe, illeggibile): lettura in Copilot Chat, confronto in Excel, agente Agent Builder, PAIN scan
- Sessione IT di 8 ore: costruzione live del flusso Power Automate, variante Extract, AS400, tabella codici, governance e costi, piano del pilota
- Pilota: Fase 0 dati, Fase 1 in ombra solo su Aprilia con confronto via "Mov.", Fase 2 scrittura in staging; i numeri della Fase 1 sostituiscono il 60/80% del deck
- Ipotesi H7–H12 (pesa di Bastia, staging accettata, righe aperte sufficienti, crediti, nodo Extract in EU, Agent Builder con le licenze Manini)

## Numeri

- 11.160 DDT/anno sugli stabilimenti, circa 1,7 pagine a DDT
- 35–50 Copilot Credits a DDT: 390.000–560.000 crediti/anno, circa 4.000–5.600 $ (1 credito ≈ 0,01 $, da verificare)
- I crediti AI Builder passano ai Copilot Credits dal 1/11/2026
- Slide 5 del deck verificata: 1.860 ore oggi, 911 prudente, 521 spinto

## Decisioni e azioni

- [ ] Preparare file ordini simulato e bozza della tabella codici per le demo
- [ ] Chiedere a Manini un ambiente Power Platform di sviluppo con Copilot Credits e l'eventuale gateway dati locale
- [ ] Provare le demo con la licenza Copilot di [[angelo-santilli]] 📅 2026-11-05
- [ ] Domande per Manini: "Mov." (H1), volumi e registrazione della pesa di Bastia (H7), web service o import su AS400, gateway esistente

## Versioni

- 02_aula_e_architettura.md · 2026-10-23 · prima versione (analisi del 22/10)
