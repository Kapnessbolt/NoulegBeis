---
description: Ingestion a richiesta da SharePoint, OneDrive e Outlook (SPEC 6.2–6.3)
argument-hint: "[sharepoint | onedrive | outlook | sharepoint:<Libreria> | riconcilia] [da AAAA-MM-GG]"
---

Esegui l'ingestion con l'agente `ingestor`.

Argomenti: `$ARGUMENTS`

1. Interpreta gli argomenti:
   - nessuna fonte → `tutte` (SharePoint, OneDrive, Outlook) dal watermark;
   - `sharepoint`, `onedrive`, `outlook` → solo quella fonte;
   - `sharepoint:<Libreria>` → solo quella libreria (usato nel primo caricamento, SPEC 6.5);
   - `riconcilia` → compito `riconcilia` (SPEC 6.4) al posto del delta;
   - una data (`AAAA-MM-GG` o `da AAAA-MM-GG`) → **da data**, al posto del watermark.
2. Se il watermark della fonte è `null` e non è stata data una data, non lanciare l'agente: spiega che serve il primo caricamento (SPEC 6.5) e proponi il comando per il prossimo lotto (es. `/ingest sharepoint:Knowledge da 2020-01-01`).
3. Lancia l'agente `ingestor` con: compito (`delta` o `riconcilia`), fonte, da data, modalità `interattiva`.
4. Riporta all'utente il resoconto dell'agente: note create e aggiornate, errori, collegamenti proposti, nuovo watermark. Per il primo caricamento, elenca 10 note a campione da controllare.
