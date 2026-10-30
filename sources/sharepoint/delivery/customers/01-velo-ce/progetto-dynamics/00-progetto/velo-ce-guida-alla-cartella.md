---
type: source-doc
source: sharepoint
family: velo-ce-guida-alla-cartella
current:
  item_id: 01EFCYUZZCKLPA4PNT7VEIATDIJCQOMYL4
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZZCKLPA4PNT7VEIATDIJCQOMYL4
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/00 Progetto/Velo-CE - Guida alla cartella.md
  name: Velo-CE - Guida alla cartella.md
  last_modified: 2026-10-29T16:14:29Z
versions:
  - { name: "Velo-CE - Guida alla cartella.md", item_id: 01EFCYUZZCKLPA4PNT7VEIATDIJCQOMYL4, last_modified: 2026-10-29T16:14:29Z }
  - { name: "Velo-CE - Guida alla cartella.md", item_id: 01EFCYUZ5GPH3MGVJAXVFIK3TX3MNNYILU, last_modified: 2026-10-28T08:04:52Z }
  - { name: "Velo-CE - Guida alla cartella.md", item_id: 01EFCYUZ6MFKTCPQS6OZEICA65NE5QYARE, last_modified: 2026-10-08T10:43:47Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-30T05:58:45Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: []
tags: [guida, cartella, struttura, regole, interno]
---

# Velo-CE · Guida alla cartella

## Riassunto

Guida interna BlueAge alla cartella del progetto Velo-CE, nella struttura nata con l'avvio del progetto il 02/10/2026; sostituisce il vecchio indice dei file di progetto. Descrive cosa contiene ogni cartella, da `00 Progetto` a `99 Project Claude (copia)` e `_superato`, e fissa quattro regole su versioni, nomi, spostamenti e collocazione dei file. Precisa che la fonte di verità sul progetto resta lo stato progetto nel Claude Project: la guida dice solo dove stanno i file.

## Punti chiave

- **00 Progetto**: piano di progetto (da costruire), indice dei codici, handoff, mappa della riorganizzazione; dal 07/10 il piano della ripresa dati al 01/01/2027 ([[velo-ce-piano-ripresa-dati-interno]]) e il piano attività del nuovo ambiente ([[velo-ce-piano-attivita-nuovo-ambiente-interno]]); in `_fonti piano/` i piani del 18-21/09 da assorbire nel nuovo piano.
- **01 Deck cliente**: deck per tema (Licenze e Premium, App So Smart, Sistemi e integrazioni, Telaio e produzione, Metodo e governo, Acquisti e magazzino, con il capitolato di etichettatura dei colli dal 07/10); in `SAL/` dal 06/10 i deck del SAL mensile numerati.
- **02 Configurazione**: logica (Word di Leo) e tabelle Excel per Telaio e produzione (pilota Lungo, guide sulla sandbox), Anagrafica e codifica, Materiali, pianificazione e costi.
- **03 Mappa sistemi**: mappa dei sistemi per il cliente (file unico dal 02/10) e flussi SdI della fattura elettronica.
- **04 Partner e ambienti**: So Smart, App EOS (analisi interne sulle 54 app), Governance e accessi, Ambienti e rilasci, Lab AL.
- **05 Transcript / 06 Evidenze**: un integrale per sessione; schermate E (tenant del cliente) e T (tenant BlueAge) con indice.
- **07 Aree** (dal 06/10): area AFC con il Piano AFC e le mappe di processo (ciclo passivo oggi e domani dal 07/10).
- **08 Guide** (dal 07/10): guide operative su Business Central; prima guida la stampa dell'etichetta articolo con codice a barre (report 6625, layout Code 39), dall'08/10 la guida per il cliente del ciclo d'acquisto ordine, carico, fattura.
- **98 Share Team** (dall'08/10): materiali per il team BlueAge, primo la sintesi dell'area AFC per Leonardo.
- **Regole**: la versione sostituita va in `_superato/<stesso percorso>`; nome `Velo-CE - <Titolo> - <DESTINATARIO> - vNNN` con destinatario CLIENTE, SO SMART, INTERNO o niente; nessuna cancellazione, solo spostamenti; cartella giusta al primo colpo.
- **Aggiornamenti dal 08/10 al 20/10**: in `01 Deck cliente/SAL/` i deck portano in testa la data della riunione (`AAMMGG`, decisione di Cristian del 16/10), con il deck «Le fondamenta» del 21/09, il SAL 01 del 06/10 e i quattro deck del 14/10; `03 Mappa sistemi` contiene solo mappe (decisione del 20/10): mappa dei sistemi CLIENTE v004 con i tre tenant della posta e Zucchetti, pagina sui tenant Microsoft e la posta, flussi SdI; in `07 Aree/AFC` il piano operativo del passaggio della fattura elettronica fra vecchio e nuovo BC (dal 12/10); in `08 Guide` la guida all'etichetta collo, la guida e i link ufficiali sulla migrazione della posta al tenant unico (20/10); nuova cartella `98 Share Team` per le sintesi al team BlueAge (08/10).
- Nuova regola: se un file da aggiornare è aperto, Claude crea la versione successiva e non tocca quello aperto.
- Dal 28-29/10: in `07 Aree/AFC/` e `07 Aree/AFC/Mappe/` le sottocartelle `Oda` del ciclo d'acquisto; in `08 Guide/` le sottocartelle `Schede operative` e `Setup tecnici` (un file per tema con i setup del nuovo BC da allineare con So Smart) ([[velo-ce-stato-progetto-99-log-revisioni]]).

## Numeri

- Riorganizzazione della cartella: 02/10/2026; struttura fino al 01/10 in `_superato/2026-10-01 struttura pre-avvio/`.
- App EOS analizzate: 54.
- Data obiettivo della ripresa dati: 01/01/2027.

## Decisioni e azioni

- Decisione (02/10/2026): nuova alberatura della cartella e regole su nomi e versioni.
- Il piano di progetto Excel è ancora da costruire, assorbendo i piani del 18-21/09 ([[velo-ce-piano-di-progetto-per-cantieri]], [[velo-ce-mappa-cantieri-dynamics]]).

## Versioni

- Velo-CE - Guida alla cartella.md · 2026-10-08 · prima versione ingerita (data della riorganizzazione della cartella)
- Velo-CE - Guida alla cartella.md · 2026-10-28 · aggiornata fino al 20/10: SAL con data della riunione, 03 solo mappe, guide nuove, 98 Share Team; nella cartella `Cristian/00 Progetto/`
- Velo-CE - Guida alla cartella.md · 2026-10-29 · riga `08 Guide` con le sottocartelle `Schede operative` e `Setup tecnici` (025.116) e riga `07 Aree` con le sottocartelle `Oda` (025.112); aggiornata dal log revisioni, file non riletto
