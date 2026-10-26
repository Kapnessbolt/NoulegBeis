---
name: blueage-deck
description: "Use when building or editing a BlueAge-branded PowerPoint deck (.pptx), in particular course decks generated from a storyboard (BlueAge training courses: M1–M5, PW): BlueAge style, RED TAG and 'Tocca a voi' slides, build from storyboard, QA."
---

# BlueAge deck

Stile e procedura per i deck PowerPoint BlueAge. Si usa **sopra** la skill pptx di Anthropic (pptxgenjs, `validate.py`, `apply_theme.js`, rendering): questa skill aggiunge le regole BlueAge, non sostituisce quella. È autosufficiente: codice, loghi e style guide sono inclusi. Per progettare i contenuti di un corso (scheda, storyboard, registri) si usa la skill `blueage-corso`; questa skill entra al gate 3, quando lo storyboard è approvato.

## Contenuto della skill

| File | Cosa contiene |
|---|---|
| `references/style_guide.md` | Design system v3: palette, tipografia, griglia, catalogo dei tipi di slide, RED TAG, "Tocca a voi". **Leggerlo prima di costruire.** |
| `references/storyboard_format.md` | Formato dello storyboard (campi per tipo, marcatura), di `deck.json` e di `media.json` |
| `scripts/blueage_lib.js` | Libreria: tema, 7 layout PowerPoint, componenti (`header` con tracker e `fatti`, `card`, `iconDot`, `label`, `fonte`, `compassRings`, `tag`), `save` con applicazione del tema |
| `scripts/build_deck.js` | Generatore generico: storyboard + `deck.json` (+ `media.json`) → .pptx. Un renderer per ogni tipo del catalogo |
| `scripts/build_campione.js` | Deck campione: una slide per tipo (v2). Prova della libreria ed esempio d'uso dei componenti |
| `scripts/install_font.sh` | Installa Plus Jakarta Sans nell'ambiente, per anteprime fedeli |
| `assets/logo_blueage_*.png`, `assets/icona_conversazione.png` | Logo BlueAge ufficiale (`chiaro` su bianco, `scuro` su blu notte, `bianco`) e icona del pannello "Tocca a voi" |

Logo originale: SharePoint BlueAge › Sales & Marketing › Brand Assets (`LogoBlueage.svg`, `blueage-logo-white.png`).

## Dove stanno i file di un corso

I contenuti di ogni corso stanno nella cartella sul PC di Lorenzo `Formazione AI/<anno>_<cliente>_<corso>/` (struttura nella skill `blueage-corso`). Per un modulo servono: `Mx/Mx_storyboard.md`, `Mx/Mx_deck.json`, `Mx/media/` (immagini e `media.json`). I deck e le anteprime si salvano nella stessa cartella `Mx/`.

## Preparazione (ogni nuova sessione)

1. Creare una cartella di lavoro nel cloud e copiarci `scripts/` e `assets/` della skill (la cartella della skill può essere in sola lettura).
2. Portare nella cartella di lavoro lo storyboard, `Mx_deck.json` e `media/` del modulo (dal PC collegato: `device_stage_files`, poi copia dalla cartella `uploads`).
3. `bash scripts/install_font.sh` (richiede npm e fontTools). Senza il font le anteprime usano un sostituto e il controllo dei testi che sforano non è affidabile.
4. `export PPTX_SKILL_DIR=<cartella della skill pptx di Anthropic>` (contiene `scripts/apply_theme.js`, serve ad applicare il tema) e `export NODE_PATH=$(npm root -g)`.
5. Prova: `node scripts/build_campione.js prova.pptx` deve stampare `ok`.

## Procedura di build (gate 3)

1. Leggere `references/style_guide.md`, `references/storyboard_format.md` e lo storyboard approvato.
2. Se manca, scrivere `Mx_deck.json` (modulo, capitoli, piede, lettere COMPASS da evidenziare).
3. Generare con versione numerata: `node scripts/build_deck.js Mx/Mx_storyboard.md Mx/Mx_deck.json Mx_vNN.pptx`. Mai sovrascrivere una versione già consegnata: si incrementa il numero.
4. Se lo storyboard usa un tipo che il build non conosce, il build si ferma: aggiungere il tipo alla style guide, poi il renderer `R.TIPO` in `build_deck.js`, poi la riga in `storyboard_format.md`. Le modifiche alla skill si annotano nel registro del metodo del Project "Formazione AI".
5. QA obbligatorio: `validate.py` della skill pptx; testo estratto (`markitdown` o python-pptx) per refusi, testi mancanti e segnaposto `[DA VERIFICARE …]` / `[DA INSERIRE …]` rimasti; conversione in PDF con LibreOffice e immagini con `pdftoppm`; controllo visivo di ogni slide (testi che sforano, sovrapposizioni, titoli su due righe, contrasto, allineamenti, tracker corretto). Correggere nello storyboard o nel generatore e rigenerare.
6. Consegna: il .pptx e il PDF di anteprima (`Mx_vNN_anteprima.pdf`) vanno nella cartella del modulo sul PC (`device_commit_files`) e si mandano anche in chat. Poi si aggiornano i registri del corso (gate 4, skill `blueage-corso`).

## Immagini e video

- L'ambiente cloud non scarica dai siti di immagini e video. Si usa il browser integrato dell'app desktop: si apre l'immagine o il fotogramma a tutto schermo e si cattura con lo zoom (800 px di larghezza bastano per mezza slide). Il file va in `Mx/media/` e la voce in `media.json`.
- Ogni immagine ha licenza o fonte registrata nel registro delle fonti del corso. I video sono link online cliccabili, niente QR code.
- Illustrazioni BlueAge (es. un documento fittizio con i campi estratti): HTML convertito in PNG con Playwright (Chromium preinstallato nell'ambiente cloud); il sorgente HTML si conserva nella cartella del corso.

## Regole che non si negoziano

1. **RED TAG**: colore pieno fuori palette, nessuna testa né piede, frase 42 pt bold in basso a sinistra, seconda frase in colore diverso, in alto solo icona etichetta + `RED TAG · nn`. Due varianti attive (vermiglio `E8452C`, giallo `FFC629`): una sola per deck.
2. **Tocca a voi** (nome interno: scansione PAIN): pannello teal a sinistra con icona conversazione e "TOCCA A VOI"; domande numerate 01…05 a destra; box suggerimento in fondo. La parola PAIN e lo scopo della scansione **non compaiono mai** né sulle slide né nelle note del docente: il build si ferma se la trova.
3. **Testa e piede** su ogni slide di contenuto: banda navy con percorso (modulo / capitolo) e tracker dei capitoli; piede con linea, numero pagina, nome del corso, logo. Copertina, sezione, pausa e chiusura senza testa; RED TAG senza testa né piede.
4. **Dispensa all'80%**: frasi complete, titoli su una riga che affermano il messaggio, 40–120 parole per slide di contenuto. Note del docente sintetiche (3-4 punti). La dispensa ai partecipanti si distribuisce in PDF senza note.
5. **COMPASS**: solo la definizione originale BlueAge (nella skill `blueage-corso`, `references/compass.md`). Lettere del modulo evidenziate in blu.
6. Il build non inventa contenuti: il testo viene dallo storyboard approvato. Dati che cambiano solo se verificati, con fonte in slide.

## Errori già incontrati

- I layout pptxgenjs non accettano testo a più colori né ellissi: logo come immagine, bussola disegnata per slide.
- Margini delle celle di tabella in pollici (non punti): valori in punti rompono la tabella. Le tabelle scelgono da sole il corpo (da 12 a 9 pt) per stare nello spazio.
- `charSpacing`, non `letterSpacing`. Colori senza `#`.
- Titoli lunghi vanno su due righe e urtano il contenuto: riscriverli, non ridurre il corpo.
- La cartella della skill installata può essere in sola lettura: le icone generate vanno in una cartella temporanea (già gestito da `prepareAssets()`).
- Quando l'ordine di proiezione dei capitoli non è numerico, il tracker usa `fatti` (capitoli già svolti): `build_deck.js` lo calcola da solo seguendo l'ordine delle slide.
- I grafici di NUMERI sono grafici nativi (modificabili in PowerPoint): la barra con "UE", "Europa" o "media" nell'etichetta prende il colore di confronto.
