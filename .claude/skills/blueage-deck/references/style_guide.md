# Style guide · Deck BlueAge

**Stato: v3, 09/10/2026.** Nasce dal template BlueAge di riferimento e dal logo ufficiale (SharePoint BlueAge, Sales & Marketing / Brand Assets), con un upgrade di design approvato da Lorenzo l'08/10/2026 (v2): testa e piede evidenti, sfondo bianco, motivi ricorrenti. La v3 aggiunge al catalogo i tipi DOMANDA, NUMERI, TIMELINE, IMMAGINE e NORMA, collaudati sul deck M1 del corso Meccanotecnica. Riferimento visivo: deck generato da `scripts/build_campione.js`.

Il codice che applica queste regole è in `scripts/blueage_lib.js` (tema, layout, componenti) e `scripts/build_deck.js` (un renderer per tipo di slide): ogni modifica qui va riportata lì.

## 1. Formato e griglia

- 16:9, 10 × 5,625 pollici. Margini laterali 0,5"; area utile 9".
- Layout PowerPoint veri (non caselle sparse): logo, piede e numero di pagina stanno nel layout.

| Zona | y | Contenuto |
|---|---|---|
| Testa | 0 – 0,40 | Banda navy a tutta larghezza: percorso a sinistra, tracker dei capitoli a destra |
| Titolo | 0,62 – 1,22 | Una riga, 26 pt bold navy (max ~50 caratteri) |
| Contenuto | 1,35 – 5,00 | Corpo della slide |
| Fonte | ~4,95 | 7,5-8 pt grigio, sopra la linea di piede |
| Piede | 5,20 – 5,625 | Linea sottile, numero pagina, nome del corso o del deck, logo BlueAge |

## 2. Palette

| Ruolo | Hex | Uso |
|---|---|---|
| Navy | `#0B2C4D` | Banda di testa, titoli, card scure, testo forte |
| Blu notte | `#050E2D` | Sfondo copertina, sezione, pausa, chiusura |
| Blu BlueAge | `#2F80ED` | Logo ("Age" e punto), capitolo corrente, numeri grandi, accento principale |
| Teal | `#1C9EB1` | Etichette, numeri delle domande, pannello "Tocca a voi", frasi di sintesi |
| Teal chiaro | `#7FD3DC` | Accenti su sfondo scuro |
| Testo | `#3A4750` | Corpo del testo |
| Grigio | `#6E7C87` | Piede, fonti, testo secondario |
| Linea | `#D5DEE5` | Linee sottili di separazione |
| Card | `#F2F5F8` | Riquadri su sfondo bianco |
| Tinta teal | `#E3F4F6` | Cerchi delle icone, box di suggerimento |
| Bianco | `#FFFFFF` | Sfondo delle slide di contenuto |
| Avviso | `#B04A2E` | Solo segnaposto `[DA VERIFICARE …]` e `[DA INSERIRE …]`: in un deck consegnato non deve restarne nessuno senza motivo |
| **Fuori palette** | `#E8452C` vermiglio · `#FFC629` giallo | **Solo RED TAG** (§6) |

## 3. Tipografia

Font unico **Plus Jakarta Sans** (da installare sui PC da cui si presenta: se manca, PowerPoint lo sostituisce e l'impaginazione salta).

| Elemento | Corpo | Stile |
|---|---|---|
| Titolo slide | 26 pt | bold, navy, una riga |
| Titolo copertina | 36 pt | bold, bianco |
| Titolo sezione | 28 pt | bold, bianco; numero 88 pt blu |
| Frase RED TAG | 42 pt (36 se lunga) | bold |
| Corpo | 13–14 pt (min 11,5) | regular, testo |
| Testo in card | 11–12,5 pt (min 9,5) | regular |
| Etichetta | 8,5 pt | bold maiuscolo, spaziatura +2 pt, teal |
| Testa (percorso, tracker) | 7–7,5 pt | bold maiuscolo |
| Piede, fonti | 7,5–8 pt | grigio |

## 4. Testa e piede (navigazione)

- **Testa:** `M1 · L'AI NEI CONTESTI INDUSTRIALI / 07 DAL PROMPT AL CONTESTO` a sinistra (modulo in bianco, capitolo in teal chiaro); a destra il tracker `01 … 10` con il capitolo corrente in un riquadro blu e quelli già fatti in teal chiaro. Su ogni slide di contenuto si vede dove si è nel modulo. Modulo, titolo del modulo e capitoli vengono dal file `deck.json`.
- **Piede:** linea sottile, numero di pagina in bold, nome del corso (campo `corso` di `deck.json`, es. "Meccanotecnica Umbra · AI & Data-Driven Management"), logo BlueAge ufficiale a destra.
- Copertina, sezione, pausa e chiusura non hanno la testa; RED TAG non ha né testa né piede.

## 5. Catalogo dei tipi di slide

| Tipo | Layout | Descrizione |
|---|---|---|
| `COPERTINA` | BA Copertina | Blu notte, logo ufficiale, motivo bussola (anelli + 7 punti) a destra, cliente · corso, titolo, modulo/sessione/data, docenti, payoff BlueAge |
| `AGENDA` | BA Contenuto | Una card per sessione: numero in cerchio, data, durata e modalità, titolo, argomenti |
| `SEZIONE` | BA Sezione | Blu notte, numero grande blu, titolo, sottotitolo; a destra l'elenco dei capitoli con il corrente evidenziato |
| `CONTENUTO` | BA Contenuto | Titolo-affermazione, testo da dispensa a sinistra, card "In pratica" e card scura "Attenzione" a destra |
| `QUATTRO_CARD` | BA Contenuto | Griglia 2×2, icona in cerchio tinto, titolo, testo; frase di sintesi teal |
| `AFFERMAZIONE_DOMANDA` | BA Contenuto | Numero grande blu, affermazione, spiegazione, box tinto con domanda in corsivo (solo nel deck campione) |
| `TABELLA` | BA Contenuto | Intestazione navy, righe alternate, nessun bordo; frase introduttiva facoltativa sopra |
| `DUE_CARD` | BA Contenuto | Confronto: card chiara + card navy, etichette maiuscole; card tinta "Caso reale" facoltativa |
| `ESERCIZIO` | BA Contenuto | Passi numerati collegati da una linea + card navy con risultato e regola |
| `COMPASS` | BA Contenuto | Bussola con le lettere del modulo in blu, elenco dei sette modi, banda DATA |
| `DOMANDA` | BA Contenuto | Titolo-domanda, invito in teal, 2-4 voci grandi con icona in cerchio (es. giro di tavolo). Non va confusa con "Tocca a voi": niente pannello teal |
| `NUMERI` | BA Contenuto | Statistiche: grafico nativo a barre facoltativo (modificabile in PowerPoint; la barra di confronto "UE/Europa/media" in navy), 2-4 numeri grandi blu (un numero negativo va in card scura), box tinto "Come è stato misurato", sintesi |
| `TIMELINE` | BA Contenuto | 3-5 tappe in orizzontale collegate da una linea, cerchi numerati (l'ultimo blu), card con periodo, nome e descrizione |
| `IMMAGINE` | BA Contenuto | Testo a sinistra con eventuale lettera COMPASS in pillola blu; immagine grande a destra, cliccabile se c'è un video (pulsante play, riga "Guarda il video"); didascalia. Senza file: riquadro rosso `[DA INSERIRE …]` |
| `NORMA` | BA Contenuto | Regola a sinistra; a destra card scura "Caso reale" e card chiara "In fabbrica" |
| `TOCCA_A_VOI` | BA Tocca a voi | Vedi §7 |
| `RED_TAG` | BA RED TAG vermiglio / giallo | Vedi §6 |
| `PAUSA` | BA Scura | Icona, "Pausa", durata |
| `CHIUSURA` | BA Scura | Sfida tra sessioni: etichetta, titolo, istruzioni, aggancio alla sessione successiva |
| `DOCENTI` | da fare | Da ricavare dalla slide 2 del template |

Un tipo nuovo si aggiunge prima qui, poi in `build_deck.js` come renderer `R.NOMETIPO`, poi in `references/storyboard_format.md`.

## 6. RED TAG

Scelta di Lorenzo (08/10/2026): il RED TAG è **quasi fuori palette**. Deve rompere la monotonia: ci si aspetta la prossima slide BlueAge e arriva una slide coerente ma dirompente.

- Colore pieno fuori palette, **due varianti attive**: **vermiglio** `#E8452C` (prima frase bianca, seconda quasi nera `#2A0A05`) e **giallo segnaletica** `#FFC629` (prima frase ocra `#7A5A00`, seconda blu notte). La variante si sceglie in `deck.json` (`red_tag_variante`) o nello storyboard (`RED TAG: variante giallo`, oppure campo `variante:` sulla singola slide). Dentro uno stesso deck si usa una sola variante, per non indebolire la riconoscibilità.
- **Nessuna testa e nessun piede**: è l'unica slide che rompe la cornice.
- Frase 42 pt bold, allineata a sinistra e in basso; seconda frase in un colore diverso per il contrasto. Nello storyboard le due parti sono separate da ` | `.
- In alto solo l'icona etichetta e `RED TAG · nn`.

## 7. Tocca a voi (scansione PAIN)

Nome interno: scansione PAIN. **Sulle slide non compare mai "PAIN" né lo scopo della scansione.** Chi ascolta deve riconoscere dall'estetica che è il suo momento di parlare. Il build si ferma se trova la parola nei testi visibili o nelle note.

- Pannello teal a sinistra (fisso nel layout) con icona conversazione, "TOCCA A VOI" e un invito breve (es. "Raccontateci come funziona da voi.").
- A destra: titolo neutro sul tema, 3–5 domande numerate `01…05` separate da linee sottili.
- In fondo un box tinto con un suggerimento che migliora la qualità delle risposte (esempio concreto, frequenza, conseguenze; processi, non persone).
- **Note del docente neutre**: "annotare processo, problema, esempio, conseguenze, gestione attuale". Nessun riferimento a vendita o soluzioni.

## 8. Motivi ricorrenti

- **Bussola**: anelli concentrici con sette punti (copertina), bussola completa nella slide COMPASS.
- **Punto blu** del logo: capitolo corrente nella sezione, numeri grandi.
- **Icone Lucide lineari** in cerchio tinto teal (su scuro: cerchio navy chiaro, icona teal chiaro). Nello storyboard si scelgono con `visual: icone Lucide: Nome1, Nome2, …`.
- Niente barre decorative o sottolineature dei titoli: la struttura la danno testa, piede e card.

## 9. Regole di contenuto sulla slide

- **Dispensa all'80%:** frasi complete, titoli che affermano il messaggio. 40–120 parole per slide di contenuto; oltre si divide o si sposta in una slide "solo dispensa".
- Titolo su una riga: se non ci sta, si riscrive (non si riduce il corpo).
- Fonti in basso, con data di consultazione per le informazioni che cambiano.
- Esempi con dati sintetici marcati "Esempio illustrativo".
- Immagini solo con licenza o fonte registrata; video come link online cliccabili, niente QR code.
- La dispensa ai partecipanti si distribuisce in **PDF senza note**.

## 10. Assets

- `assets/logo_blueage_chiaro.png` (Blue navy, Age e punto blu, su fondo bianco), `logo_blueage_scuro.png` (Blue bianco, su blu notte), `logo_blueage_bianco.png`: ricavati dal PNG bianco ufficiale su SharePoint. Se serve qualità vettoriale, usare `LogoBlueage.svg` da Brand Assets.
- `assets/icona_conversazione.png`: icona del pannello "Tocca a voi" (la rigenera `prepareAssets()`).
