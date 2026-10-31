---
type: proposal
date: 2026-10-31
kind: regola
status: proposta
---

# Audit: affidabilità dinamica di ingestion, riconciliazione e conoscenza

Audit sul repo (SPEC 1.26, `.claude/`, `vault.yaml`, `.state/`, note, digest, diari, git log), senza connettori. Script eseguiti sul vault reale (280 test verdi, `controlla-vault.py` 0 errori e 71 avvisi, `perimetro.py --verifica` 99,5%, `famiglia.py --verifica` 82,5% secco e 95,5% con i prefissi) e scenari sintetici di `stato.py` nello scratchpad (merge driver, fotografia delle cartelle, watermark).

## 1. Verdetto

Il flusso **non è ancora affidabile in modo dinamico**: regge finché qualcuno guarda il digest e interviene in sessione. In dieci giorni le fonti sono cambiate tre volte senza che un file fosse modificato (copia di Velo-CE il 28/10, ricaricamento il 29/10, riordino il 30/10) e ogni volta il recupero è stato manuale: 118 note riallineate il 29/10, 25 note spostate e 5 file recuperati il 31/10. La causa non è un bug ma un'architettura: l'identità di un documento è l'ID dell'item, che SharePoint non conserva in copie e ricaricamenti; la riconciliazione, che dovrebbe assorbire questi casi, è specificata in quattro righe e non ha mai girato per intero; e le regole che decidono se un giro ha visto tutto (watermark, spostamenti, versioni) stanno in prosa per l'LLM, non in uno script che le impone. La SPEC 1.26 (finestra di 48 ore, rilevatore di riordino, riconciliazione ridotta) chiude il caso del 31/10 solo in parte: rileva il riordino ma non lo risolve da sola, e il segnale si consuma anche se la riconciliazione fallisce. La meccanica di base (stato via script, watermark che non scende, merge driver, controllo a tre livelli, rinomina con i wikilink) è solida e va tenuta: il lavoro è spostare nel codice l'identità dei documenti, la riconciliazione e i controlli incrociati stato ↔ note.

## 2. Criticità

### Alta

**A1 · L'identità del documento è l'ID dell'item, che le fonti non conservano.**
- Problema: lo stato è `{driveId}/{itemId} → nota` (SPEC 6.1, `SPEC.md:393-418`). Una copia, un ricaricamento o un'esportazione cambiano l'ID; la riconciliazione (SPEC 6.4, `SPEC.md:461`) legge «ID non più presenti → `status: removed`». Il caso «ID nuovo ma famiglia già nota nella stessa cartella» è un passo in prosa dell'agente (`ingestor.md:38`), non della riconciliazione né di uno script.
- Scenario: Leonardo copia `Progetto Dynamics/` in un'altra cartella e cancella l'originale. Il delta crea note nuove o versioni (giudizio dell'agente); la riconciliazione della domenica segna rimosse le note vecchie. Nel vault la stessa conoscenza esiste due volte, una marcata `removed`.
- Evidenza: [[2026-10-29-cockpit-conteggi-e-step-13]] («64 note puntavano ancora agli ID dei file originali… la riconciliazione, che ragiona per ID, le avrebbe segnate come rimosse»), commit `14060ab` (118 note a mano); [[2026-10-30]] (ricaricamento del 29/10: «ID nuovi su 68 note»); oggi `.state/sharepoint.json` ha 117 note con più voci e 36 voci il cui ID non compare né in `current`, né in `versions`, né in `also_at` della nota: la mappa ID → nota è già a strati e nessun controllo la legge.
- Impatto: conoscenza sbagliata (note doppie, rimosse a torto) e lavoro manuale a ogni copia. Nel prodotto (SPEC 13.2) i clienti copiano e ricaricano cartelle più di quanto le modifichino.
- SPEC 1.26: coperta a metà. Il segnale «ID nuovi» (`SPEC.md:432`) rileva il ricaricamento; la risoluzione (stessa nota, voce nuova, `removed` solo senza candidati) non è scritta in 6.4 e non ha uno script.

**A2 · Il watermark può superare file che l'indice non ha ancora restituito, e nessuno se ne accorge.**
- Problema: il delta si fida della ricerca; il watermark sale al risultato più recente (`SPEC.md:429`, `ingestor.md:72`). La finestra di 48 ore (1.26) riduce la finestra di esposizione, non la chiude: un file che l'indice restituisce dopo 48 ore, o che resta fuori dai primi 1000 risultati (`ingestor.md:70`), è perso finché una riconciliazione non lo trova. La regola del watermark è prosa e l'agente la applica in modo incoerente.
- Scenario: riordino il pomeriggio, giro alle 06:50, indice aggiornato alle 10:00: i file spostati e modificati nel riordino non entrano, il watermark è oltre, il digest dice «OK».
- Evidenza: [[2026-10-31]] (5 file del 30/10 non restituiti, «watermark già oltre», recuperati a mano, visibile solo perché una mail annunciava il riordino); [[2026-10-27]] (21 risultati, «sharepoint invariato 2026-10-19T16:22:49Z»: la regola «il più recente di tutti i risultati» non è stata applicata e il 29/10 la ricerca è ripartita dal 19/10 con 298 risultati, commit `7c20370`).
- Impatto: perdita di versioni, silenziosa: il digest, il cockpit e `/verifica-task` non hanno un segnale per «il giro non ha visto tutto».
- SPEC 1.26: coperta in parte (finestra).

**A3 · Il rilevatore di riordino consuma il segnale prima che la riconciliazione sia finita, e ha buchi noti.**
- Problema: `stato.py set-cartelle` salva la fotografia nello stesso comando che la confronta (`stato.py:315-345`): scatta una volta sola. Non esiste una voce di stato «riconciliazione dovuta» (`reconcile.json` ha solo `last_run` della completa, `SPEC.md:465`). Falsi negativi: file spostato tra cartelle esistenti, file rinominato, cartelle sotto il livello 2 (gli handoff di Velo-CE stanno al livello 4 di Delivery), riordino sotto i 10 ID nuovi. Non è ancora collaudato: `cartelle` è vuoto nello stato.
- Scenario: la fotografia rileva il riordino alle 06:50, la riconciliazione ridotta si ferma a metà (connettore, limite della sessione, push fallito). Il giorno dopo la fotografia coincide con quella salvata: niente riordino, note con il percorso vecchio per sempre, salvo la domenica.
- Evidenza: scenario sintetico 5 nello scratchpad (seconda fotografia identica dopo il riordino → `riordino: false`); `ingestor.md:76` («un errore del connettore sul rilevatore va nel digest e non ferma il resto del giro»: il resto del giro include il `set-cartelle`); [[2026-10-31-riordino-sharepoint]] («non ancora collaudato su un riordino reale»).
- Impatto: lavoro manuale e `current.web_url` stale, con il librarian che apre link morti.
- SPEC 1.26: è la risposta stessa; i buchi sono residui.

**A4 · La riconciliazione è sottospecificata, mai eseguita per intero, e fa tutto l'LLM.**
- Problema: SPEC 6.4 è quattro righe (`SPEC.md:455-465`); la sequenza di uno spostamento (cartella da `perimetro.py`, `git mv`, `current.web_url` e `uri`, `set-item --note`, `rinomina-nota.py` se cambia la famiglia, `family` a mano perché `rinomina-nota.py` non lo aggiorna, `rinomina-nota.py:87`) è a carico dell'agente, con Sonnet la domenica. Non c'è uno script che prende l'elenco delle cartelle e produce il piano (spostare, rimuovere, recuperare, versione).
- Scenario: la domenica dopo un riordino la riconciliazione deve fare in un giro ciò che il 31/10 ha richiesto una sessione con Opus e l'utente che decideva caso per caso (copia interna vs sito partner, quale è `current`).
- Evidenza: unico giro `reconcile` del 25/10 in [[2026-10-25]]: «confronto con ricerca SharePoint/OneDrive (indice instabile, totali variabili tra le pagine) e con gli elenchi delle cartelle SalesMarketing, Pulse, one-pager, TradeSpending, Velo-CE `00 Progetto` e `Handoff`»: un campione, non il perimetro, e nessun commit `ingest(riconcilia)` nel git log; [[2026-10-29-famiglie-allineate]] (`family` corretto a mano dopo la rinomina); [[2026-10-31-riordino-sharepoint]] (25 note spostate a mano «con `current.web_url` e il percorso nello stato aggiornati»).
- Impatto: la rete di sicurezza del flusso è la parte meno specificata e meno collaudata.
- SPEC 1.26: no (aggiunge solo la variante ridotta).

### Media

**M1 · Il merge driver dello stato perde lo spostamento di una nota se l'altro lato ha un istante più recente.**
- Problema: `_scegli` prende l'intera voce dal lato con `last_modified` più recente (`stato.py:360-373`): il campo `note` segue l'istante, non chi l'ha cambiato.
- Scenario: `/ingest riconcilia` in sessione sposta la nota (`--note` nuovo) mentre il task delta registra una versione nuova dello stesso ID: dopo il rebase lo stato punta al percorso vecchio, che non esiste più. Verificato nello scratchpad (scenario 1): risultato `note: sources/sharepoint/a/x.md` con `last_modified` nuovo.
- Impatto: errore del controllo («punta a una nota inesistente») e CI rossa; recupero a mano.
- SPEC 1.26: no.

**M2 · Stato e note non si controllano a vicenda.**
- Problema: `controlla-vault.py` verifica solo che `note` esista e che i documenti siano registrati (`controlla-vault.py:528-550`). Non verifica: l'ID della voce dentro la nota (36 voci orfane oggi), la cartella della nota contro `perimetro.py` da `current.web_url` (oggi 1 disaccordo: [[velo-ce-progetto-dynamics-e-power-bi-la-strada-verso-premium]], nota in Delivery con `current` in SalesMarketing), `family` contro `famiglia.py` (12 «diversa»), `current.web_url` stale. I golden test `--verifica` non sono in CI né nel pre-commit.
- Scenario: dopo un riordino assorbito a metà, il vault ha 0 errori e il librarian apre un link morto.
- Impatto: la frase «0 errori» non copre il disallineamento tra stato, note e fonti.
- SPEC 1.26: no.

**M3 · Una nuova versione non si propaga alle note hub.**
- Problema: l'avviso «aggiornata dopo questa nota: da rileggere» (`controlla-vault.py:487`) è l'unico meccanismo; nessun task lo smaltisce, `/controlla` è manuale. Oggi 63 avvisi di questo tipo.
- Scenario: [[blueage-ai-che-cresce-onepage]] è alla v4, [[ai-che-cresce-con-lazienda]] descrive la v2 (aperto in [[2026-10-31-riordino-sharepoint]]); il librarian risponde con i punti chiave vecchi, citando la fonte giusta.
- Impatto: conoscenza sbagliata con fonte apparentemente valida.
- SPEC 1.26: no.

**M4 · La chiave di famiglia decide quando la nota è una sola, ma lascia i casi limite al giudizio.**
- Problema: `_MEETING`, `- INVIATO`, `_OLD`, `vecchia`, lettere di versione senza `_` (`PULSE_K`), versione a metà nome (`… v006 - Guida … - v001`) escono dalla famiglia o la spezzano; «contenuto equivalente → copia, diverso → `<cartella>-<famiglia>`» (`ingestor.md:38`) è un giudizio senza traccia. Due giri con due agenti diversi possono decidere in modo diverso sullo stesso file.
- Evidenza: `famiglia.py --verifica`: 12 «diversa», tra cui `BlueAge_Possibilita_v3_MEETING.pdf → blueage-possibilita-v3-meeting` (attribuita a mano a [[blueage-possibilita]]); [[2026-10-31]] «v006 in un'altra cartella… trattata come nuova versione della stessa famiglia» (decisione del giro, non regola).
- Impatto: note doppie o versioni perse, non rilevate (il controllo vede solo `family` identico).
- SPEC 1.26: no.

**M5 · Regole duplicate o solo in prosa che possono divergere.**
- Watermark: SPEC 6.2 passo 6 e `ingestor.md:72`, applicata dall'LLM (A2).
- Mittenti scartati: SPEC 5.3, `vault.yaml` (`fonti.outlook.mittenti_scartati`) e `ingestor.md:82` con l'elenco copiato; nessuno script li applica (`config.py` li valida e basta).
- Finestra della posta: «2 ore» in SPEC 6.3 e nell'agente, mentre quella dei documenti è in `vault.yaml`.
- Riconciliazione in tre testi (SPEC 6.4, `ingestor.md` §7, `routines/reconcile.md`); perimetro in SPEC 5 e `vault.yaml` (dichiarato, step 14).
- Cartelle di progetto software: esclusione «resta all'agente» (`ingestor.md:30`, `perimetro.py`).
- `ingestor.md` è a 1.802 parole contro il criterio di 1.500 dello step 12 (`SPEC.md:634`).
- Impatto: ogni divergenza è un comportamento diverso tra un giro e l'altro.

**M6 · Osservabilità e recupero.**
- Cosa si vede: giri mancanti e righe non OK (`plancia.py`, cockpit, `/oggi`), errori del controllo, note `da-verificare`.
- Cosa resta silenzioso: watermark fermo per giorni (27–28/10), file saltati dall'indice, note con percorso vecchio, riconciliazione non fatta o parziale, `current.web_url` morto, hub superate.
- Recupero: le procedure del 29/10 e del 31/10 esistono solo nei diari; `/verifica-task` è manuale e in dieci giorni ha prodotto cinque diari di verifica. Per il prodotto (13.2, «integrità invisibile») questo lavoro oggi lo fa Lorenzo.

### Bassa

**B1 · Riconciliazione ridotta dentro il giro di `ingest-sharepoint`.** Un riordino grande (Delivery intera) allunga il giro oltre il limite della sessione senza un punto di ripresa; nessun limite né ordine di priorità.

**B2 · Watermark unico per SharePoint e OneDrive da una sola ricerca.** Un file OneDrive fallito ferma solo `onedrive`, ma la regola è prosa (`ingestor.md:72`); le note `fuori-perimetro` (4 oggi) restano fuori dallo stato per scelta e la riconciliazione le ignora: coerente, ma non scritto in 6.4.

**B3 · Tenuta per il prodotto.** Profondità 2 e soglia 10 sono tarate su questo tenant (librerie a tre cartelle di primo livello); un cliente con una libreria unica e cartelle profonde rende cieco il segnale «cartelle», e il segnale «ID nuovi» dipende dall'affidabilità della famiglia (M4). Più utenti sullo stesso SharePoint moltiplicano copie personali (`also_at`, quale è `current`). `perimetro.py` ha un ramo per sito e uno per OneDrive, non una lista di prefissi generica (SPEC 14 lo ammette). Il wizard `/installa` (step 18) non misura nulla delle fonti prima di scegliere i parametri.

## 3. Cosa funziona bene (non toccare)

- `stato.py`: scrittura atomica, validazione degli istanti e dei percorsi, watermark che non scende, voci mai cancellate, merge driver provato in un rebase vero (`test_merge_driver_in_un_rebase_vero`), `risolvi` per i conflitti residui.
- Il principio «il codice fa la meccanica, il modello il giudizio» e gli script che già lo applicano: `perimetro.py` (99,5% sul vault), `nuova-nota.py` e `aggiorna-nota.py` (`--nuova-versione`, `--also-at` idempotenti), `rinomina-nota.py` per i wikilink e lo stato.
- Controllo a tre livelli (hook, pre-commit, CI) con 280 test su un mini-vault; CI che esegue i test prima del controllo.
- Digest con la tabella degli esiti letta da `plancia.py` (giri mancanti visibili nel cockpit), diari di sessione completi: senza di loro questo audit non avrebbe evidenze.
- `vault.yaml` come configurazione separata: i parametri del rilevatore sono già fuori dal motore.

## 4. Piano di interventi

| # | Intervento | Dove | Priorità | Effort | Chiude |
|---|---|---|---|---|---|
| P1 | **Identità per famiglia e cartella accanto all'ID.** `stato.py` tiene l'indice inverso nota → voci e offre `trova --famiglia <f> --cartella <c>` e `collega <chiave nuova> --stessa-nota-di <chiave vecchia>`; SPEC 6.4 passo 2 diventa: ID sparito → cerca lo stesso nome o famiglia nella stessa cartella, poi nella libreria; trovato → voce nuova sulla stessa nota (versione o `also_at`); `removed` solo senza candidati e dopo due giri consecutivi | SPEC 6.1, 6.4; `stato.py`; controllo | Alta | M | A1, parte di M2 |
| P2 | **`sposta-nota.py <nota> --web-url <nuovo> [--item-id --uri]`**: cartella da `perimetro.py`, `git mv`, `current.*`, `family` e slug se cambiano (chiama `rinomina-nota.py`, che da solo aggiorna anche `family`), `set-item --note`; unico modo per spostare una nota fonte, usato da riconciliazione, rilevatore e sessione | script nuovo; `rinomina-nota.py`; `fonti.md`; SPEC 6.4 | Alta | M | A4, M2, parte di A3 |
| P3 | **`riconcilia.py --elenco <json dal connettore> --fonte <f> [--libreria <l>]`**: confronta l'elenco ricorsivo (ID, webUrl, nome, lastModified) con lo stato e le note e stampa il piano in JSON (sposta, rinomina, nuova voce, rimuovi, recupera, in coda); `--applica` esegue la parte meccanica con P2; l'agente fa solo lettura dal connettore e riassunti. Testato su elenchi sintetici | script nuovo; SPEC 6.4; `ingestor.md` §7; `reconcile.md` | Alta | L | A4, A1, A3 |
| P4 | **Segnale di riordino persistente.** `set-cartelle` scrive `riconciliazione_dovuta: {libreria: istante}` nello stato della fonte; la toglie solo `stato.py set-riconciliata <fonte> <libreria>` a fine riconciliazione; il controllo del vault avvisa se dovuta da più di 1 giorno, errore oltre 7; il digest la ripete ogni giorno | `stato.py`; `controlla-vault.py`; SPEC 6.2 passo 7 | Alta | S | A3 |
| P5 | **Registro del giro.** `stato.py set-giro <fonte> --inizio --fine --risultati <n> --piu-recente <istante> --falliti <n>` scrive `ultimo_giro` nella fonte; `set-watermark` accetta `--da-giro` e calcola da sé la regola di SPEC 6.2 passo 6; il controllo avvisa se il watermark è fermo da più di 2 giorni con risultati nel giro o se un giro atteso manca; `plancia.py` lo mostra | `stato.py`; `controlla-vault.py`; `plancia.py`; `ingestor.md` §4 | Alta | S | A2, M5, M6 |
| P6 | **Controlli incrociati stato ↔ note** in `controlla-vault.py`: voce il cui ID non è nella nota (avviso), cartella della nota diversa da `perimetro.py` su `current.web_url` (errore), `family` diversa da `famiglia.py` salvo prefisso (avviso), nota con più voci senza `versions`/`also_at` corrispondenti (avviso); `perimetro.py --verifica` e `famiglia.py --verifica` nella CI | `controlla-vault.py`; workflow | Media | S | M2, M4 |
| P7 | **Merge per campo** nel driver: `note` dal lato che l'ha cambiata rispetto alla base, `last_modified` il più recente, `commit` con l'istante; test con lo scenario 1 | `stato.py` | Media | S | M1 |
| P8 | **Propagazione delle versioni.** A ogni `--nuova-versione` l'ingestor scrive nel hub (`## Fonti` o riga in coda a `## Punti chiave`) `- Da rileggere: [[fonte]] vN del AAAA-MM-GG`; il task `digest` elenca le hub da rileggere da più di 7 giorni; il curator le conta nelle metriche. In alternativa, un task settimanale Sonnet che rigenera i punti chiave e lascia la decisione a Lorenzo in una PR | `ingestor.md` §3.4; `digest.md`; SPEC 4.3 | Media | M | M3 |
| P9 | **`famiglia.py`**: suffissi `_MEETING`, `_OLD`, `vecchia`, `- INVIATO`, `- INVIATA`; lettera di versione anche senza `_` quando è una sola maiuscola finale; versione a metà nome (`v006 -`) tolta solo se seguita da un segmento; golden test aggiornato e soglia al 95% | `famiglia.py`; test | Media | S | M4 |
| P10 | **Fonte unica.** Mittenti scartati applicati da uno script (`scarta.py --mittente --oggetto` da `vault.yaml`) e tolti da SPEC 5.3 e dall'agente; finestra della posta in `vault.yaml`; riconciliazione descritta una volta (SPEC) con agente e routine che rimandano; agente sotto le 1.500 parole | `vault.yaml`; `config.py`; SPEC 5.3, 6.3; `ingestor.md` | Media | S | M5 |
| P11 | **Verifica dei giri automatica**: il task `digest` esegue `plancia.py` e scrive in `## Esito dei task` le anomalie (giro mancante, watermark fermo, riconciliazione dovuta, voci orfane); `/verifica-task` resta per l'indagine | `digest.md`; `plancia.py` | Bassa | S | M6 |
| P12 | **Riconciliazione ridotta come task separato** lanciato dal rilevatore (riga nel digest + `riconciliazione_dovuta`) ed eseguito dal giro successivo o da un task `reconcile-ridotta` alle 09:00, con Sonnet e un limite per libreria | SPEC 6.2, 7; `vault.yaml` | Bassa | S | B1 |
| P13 | **Prodotto.** Parametri del rilevatore per libreria; profondità «fino alla prima cartella con file» misurata da `/installa`; `perimetro.py` con una lista di prefissi e cartelle di nota invece dei due rami; regola scritta su quale copia è `current` (cartella canonica in `vault.yaml`, non l'ultima modificata) | `vault.yaml`; `perimetro.py`; SPEC 5, 13.1 step 18 | Bassa | M | B3 |

Ordine consigliato: P4 e P5 subito (piccoli, chiudono i silenzi), poi P1 + P2 + P3 insieme (sono lo stesso cambiamento: identità e riconciliazione nel codice), poi P6 e P7, infine P8–P13.

## 5. Test di collaudo

Tutti su un mini-vault nello scratchpad (come i test esistenti), con elenchi delle cartelle sintetici al posto del connettore. Criterio comune: `controlla-vault.py` 0 errori, `perimetro.py --verifica` e `famiglia.py --verifica` al 100% sul mini-vault, nessun wikilink rotto, diff dello stato leggibile.

| Scenario | Come | Successo |
|---|---|---|
| T1 · Riordino sintetico (rinomina di 2 cartelle, 10 file spostati con gli stessi ID) | Fotografia A poi B con `set-cartelle`; elenco con i webUrl nuovi a `riconcilia.py` | `riordino: true`; 10 note spostate nella cartella di `perimetro.py`, `current.web_url` nuovo, 0 `removed`, `riconciliazione_dovuta` tolta solo dopo l'esecuzione |
| T2 · File spostato e rinominato (famiglia diversa) | Elenco con webUrl e nome nuovi, stesso ID | Nota rinominata con `rinomina-nota.py`, `family` aggiornata, wikilink e stato aggiornati, una sola nota |
| T3 · Cartella ricaricata (ID nuovi, stessi percorsi e nomi) | Elenco con ID nuovi | 0 note nuove, 0 `removed`, voci nuove sulla stessa nota, `versions` con la voce nuova in testa; il rilevatore scatta («nuove» e «sparite» uguali) |
| T4 · Copia in due cartelle (sito partner e interna) | Due voci con nomi uguali in cartelle diverse | Una nota, `also_at` con la copia, `current` sulla cartella canonica |
| T5 · Indice in ritardo | Giro 1 senza i file X (modificati prima del watermark finale); giro 2 con X | X ingeriti nel giro 2 dalla finestra; se X più vecchi della finestra, la riconciliazione li recupera come «mai ingeriti» senza toccare il watermark |
| T6 · Giro rieseguito (idempotenza) | Stesso elenco due volte | Secondo giro: nessuna nota riscritta, stato identico (diff vuoto), nessuna riga doppia nei log dei progetti |
| T7 · Giri sovrapposti | Branch A: riconciliazione sposta una nota; branch B: delta registra una versione dello stesso ID; rebase | Stato con `note` nuovo e `last_modified` nuovo, nessuna voce verso note inesistenti (P7) |
| T8 · Riconciliazione interrotta | `riconcilia.py --applica` fermato dopo metà del piano | `riconciliazione_dovuta` ancora presente; la ripetizione completa il resto senza rifare ciò che è fatto |
| T9 · Watermark fermo | Due giri con risultati tutti già registrati | Watermark salito al più recente dei risultati (regola in `set-watermark --da-giro`), nessun avviso |
| T10 · Nuova versione e hub | `--nuova-versione` su una fonte citata da un tema | Riga «Da rileggere» nel tema, riga nel log del progetto, avviso del controllo; dopo la rilettura l'avviso sparisce |
| T11 · Riordino reale (dopo P1–P5) | Chiedere a Leonardo di spostare e rinominare una cartella di prova in Delivery | Il giro del mattino rileva, riconcilia e il digest dice quante note ha spostato; nessun intervento in sessione |

## 6. Domande aperte per Lorenzo

1. **Identità**: accetti che un ID sparito con un file «uguale» (stesso nome e famiglia nella stessa libreria) sia la stessa nota per regola, senza passare dal giudizio dell'agente? E `removed` solo dopo due riconciliazioni consecutive senza candidati?
2. **Copie**: quale copia è `current` quando lo stesso documento sta sul sito partner e in SalesMarketing: l'ultima modificata o la cartella canonica dichiarata in `vault.yaml`? Il 31/10 hai scelto la copia interna caso per caso.
3. **Riconciliazione**: dentro `ingest-sharepoint` con Opus (SPEC 1.26) o task separato con Sonnet dopo che lo script fa il piano (P12)? Dipende da quanto giudizio vuoi lasciare al giro del mattino.
4. **Hub superate**: chi rilegge i punti chiave quando una fonte cambia versione: tu in sessione con una lista, o un task che propone la riscrittura in PR?
5. **Soglie**: profondità 2 e 10 ID nuovi restano finché non c'è un riordino reale, o le tari subito (profondità 4 per Delivery, soglia 5) accettando qualche riconciliazione ridotta in più?
6. **Step 13**: il criterio «3 giri senza errori» è soddisfatto con il giro anomalo del 31/10, oppure lo step si chiude dopo T11?
7. **Prodotto**: il primo cliente riceve il rilevatore attivo su tutte le fonti e la riconciliazione automatica, o solo la settimanale con BlueAge che interviene? Cambia il contratto di gestione (13.2).
