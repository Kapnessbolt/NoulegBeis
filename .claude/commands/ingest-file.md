---
description: Ingerisce un singolo documento di SharePoint o OneDrive, anche fuori dal perimetro
argument-hint: "<url, file:/// o nome del file>"
---

Ingerisci un singolo documento con l'agente `ingestor`.

Documento: `$ARGUMENTS`

1. Se l'argomento è vuoto, chiedi all'utente l'URL o il nome del file.
2. Lancia l'agente `ingestor` con: compito `file`, documento `$ARGUMENTS`, modalità `interattiva`.
3. Se l'agente restituisce più candidati, mostrali all'utente, fai scegliere e rilancia l'agente con l'URI scelto.
4. Riporta all'utente: percorso della nota, famiglia, versione corrente, collegamenti creati o proposti, esito del push.
