---
description: Ingestion a richiesta da SharePoint, OneDrive, Outlook e GitHub (SPEC 6.2–6.3, 6.6)
argument-hint: "[sharepoint | onedrive | outlook | github | sharepoint:<Libreria> | riconcilia [sharepoint:<Libreria> | onedrive]] [da AAAA-MM-GG]"
---

Esegui l'ingestion con l'agente `ingestor`.

Argomenti: `$ARGUMENTS`

1. Interpreta gli argomenti:
   - nessuna fonte → `tutte` (SharePoint, OneDrive, Outlook) dal watermark;
   - `sharepoint`, `onedrive`, `outlook`, `github` → solo quella fonte (`github`: i repo di SPEC 5.4, che devono essere collegati alla sessione);
   - `sharepoint:<Libreria>` → solo quella libreria (usato nel primo caricamento, SPEC 6.5);
   - `riconcilia` → compito `riconcilia` (SPEC 6.4) al posto del delta, fonte `tutte`; `riconcilia sharepoint:<Libreria>` o `riconcilia onedrive` → riconciliazione ridotta a quella libreria o alla cartella di OneDrive (dopo un riordino annunciato nel digest o in una mail);
   - una data (`AAAA-MM-GG` o `da AAAA-MM-GG`) → **da data**, al posto del watermark.
2. Se il watermark della fonte è `null` e non è stata data una data, non lanciare l'agente: spiega che serve il primo caricamento (SPEC 6.5) e proponi il comando per il prossimo lotto (es. `/ingest sharepoint:SalesMarketing da 2020-01-01`).
3. Lancia l'agente `ingestor` con: compito (`delta` o `riconcilia`), fonte, da data, modalità `interattiva`.
4. Riporta all'utente il resoconto dell'agente: note create e aggiornate, errori, collegamenti proposti, nuovo watermark. Per il primo caricamento, elenca 10 note a campione da controllare.
