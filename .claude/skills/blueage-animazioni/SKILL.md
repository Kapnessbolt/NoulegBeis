---
name: blueage-animazioni
description: "Use when creating a BlueAge didactic animation (15-20 s MP4 rendered from HTML, dark style) or a static illustration (HTML to PNG, light style) to explain a concept or process in a BlueAge course deck: scene planning, templates, render, poster, embedding the video in PowerPoint."
---

# Animazioni e illustrazioni BlueAge

Schemi animati e illustrazioni che spiegano **come funziona** una tecnologia o un processo, per le slide dei corsi BlueAge. Dato un concetto, la skill produce in modo ripetibile:

1. un **video didattico** 15-20 s (HTML → MP4 1920 × 1080, 30 fps, senza audio), stile scuro;
2. oppure un'**illustrazione statica** (HTML → PNG a 2x), stile chiaro;
3. il **poster** del video, il fotogramma che si legge da solo nella dispensa PDF;
4. l'incorporazione del video nel deck PowerPoint.

Entra al gate 3 del corso (skill `blueage-corso`), quando lo storyboard prevede un'animazione o un'illustrazione; le slide si fanno con la skill `blueage-deck`.

## Contenuto della skill

| File | Cosa contiene |
|---|---|
| `references/stile.md` | Palette scura e chiara, corpi minimi, composizione, movimento, struttura nel tempo, poster. **Leggerlo prima di progettare** |
| `references/scene.md` | Video, illustrazione o niente; modello del file delle scene al secondo; esempio approvato |
| `references/componenti.md` | Struttura del file, `CONFIG`, funzioni di tempo, componenti della libreria BA, schemi ricorrenti, classi delle illustrazioni. **Leggerlo prima di scrivere codice** |
| `references/powerpoint.md` | Come il video va in slide: posizione, poster, didascalia, fonte, link facoltativo al prodotto reale, `add_video.py` |
| `assets/template_animazione.html` | Scheletro del video: libreria `BA_ANIM_LIB v1` (non si modifica) + esempio da sostituire |
| `assets/template_illustrazione.html` | Scheletro dell'illustrazione: stile `BA_ILL_STILE v1` (non si modifica), icone, esempio da sostituire |
| `assets/esempio_anim1_visione.html` | L'animazione "visione artificiale" del 14/10/2026 rifatta con il template: esempio completo di scena con cicli, nastro, card, barra con soglia, contatori |
| `assets/font/` | Plus Jakarta Sans (licenza OFL) che `render.js` incorpora nell'HTML |
| `scripts/render.js` | `check` · `fotogrammi` · `video` · `png` · `font` |
| `scripts/add_video.py` | Incorpora l'MP4 in un .pptx esistente (avvio automatico, loop, poster, link facoltativo) |

## Preparazione (ogni sessione)

1. Cartella di lavoro nel cloud; copiarci `scripts/` e `assets/` della skill (la cartella della skill può essere in sola lettura).
2. `export NODE_PATH=$(npm root -g)`. Chromium, Playwright e ffmpeg sono preinstallati: **non** lanciare `playwright install`. Il font non va installato: `render.js` lo incorpora nell'HTML.
3. Prova su una copia: `cp assets/template_animazione.html prova.html && node scripts/render.js check prova.html` deve dire `OK: nessun errore`. `render.js` incorpora il font e **riscrive** l'HTML: mai lanciarlo sui file della skill.

I file del corso stanno sul PC di Lorenzo: `Mx/media/animazioni/` (video) e `Mx/media/illustrazioni/` (illustrazioni). Si portano nel cloud con `device_stage_files` e si riportano con `device_commit_files`.

## Procedura a gate

Non si passa al gate successivo senza l'OK esplicito di Lorenzo.

1. **Progetto.** Leggere il testo della slide, `references/stile.md` e `references/scene.md`. Decidere tra video e illustrazione. Per un video scrivere `animN_<tema>_scene.md` (testo della slide, messaggio chiave, elementi fissi, dati fittizi, scene al secondo, riepilogo, fotogrammi chiave) e mandarlo a Lorenzo. Per un'illustrazione basta un brief breve (messaggio, larghezza in slide, elementi).
2. **Fotogrammi chiave.** Copiare il template, scrivere `CONFIG`, `prepara`, `scena` seguendo `references/componenti.md` (esempio completo: `assets/esempio_anim1_visione.html`). Poi `node scripts/render.js fotogrammi animN_<tema>.html`: si ferma se il controllo trova errori. Guardare la tavola `animN_<tema>_anteprime.png` e mandarla a Lorenzo con il file HTML (si apre nel browser: spazio = pausa, frecce = ±0,5 s, `#t=8` nell'indirizzo = fermo a 8 s). Se la scena introduce oggetti mai disegnati prima (una macchina, un'interfaccia), far approvare prima un solo fotogramma di stile. Per un'illustrazione: `node scripts/render.js png ill_<tema>.html` e si manda il PNG.
3. **Render e controllo.** `node scripts/render.js video animN_<tema>.html` → `animN_<tema>.mp4` e `animN_<tema>_poster.png`; lo script verifica dimensioni, durata e peso (< 10 MB) ed estrae tre fotogrammi dall'MP4 (`anteprime_<nome>/<nome>_dal_video_*.png`). Guardarli insieme al poster: nel poster non deve restare nulla "in corso" (mirini, deviatori, pillole). Controllare a mano: testi in italiano senza refusi, coerenza con il testo della slide, dati fittizi uguali al resto del deck, loop pulito. Compilare le note di consegna nel file delle scene.
4. **Consegna e deck.** HTML, MP4, poster, anteprime e file delle scene nella cartella `media/animazioni/` del modulo e in chat. Poi in slide secondo `references/powerpoint.md`: dallo storyboard con `blueage-deck` oppure con `add_video.py` sul .pptx; fonte "animazione BlueAge (gg/mm/aaaa)" nel registro delle fonti del corso.

## Regole che non si negoziano

1. **Spiega come funziona**, passo per passo, fedele al testo della slide. Non è pubblicità e non è realistica.
2. **Dati fittizi** coerenti con il deck e dichiarati; **nessun marchio** né interfaccia riconoscibile di terzi; disclaimer "Illustrazione BlueAge · animazione didattica, non è un prodotto" nel video.
3. **Anomalie in corallo `#FF7A59`, mai il vermiglio `#E8452C`** dei RED TAG.
4. **Leggibile a mezza slide**: titolo 44 px, testi essenziali ≥ 28 px, etichette ≥ 20 px su 1920; una cosa nuova alla volta; tracker dei passi a sinistra; riepilogo fermo negli ultimi 2 s.
5. **Un file HTML autosufficiente**: niente librerie esterne né CDN, font incorporato. **Deterministico**: tutto lo stato da `window.renderAt(t)`, niente `setTimeout`, orologio, casuale o animazioni CSS.
6. **Il blocco `BA_ANIM_LIB` (e `BA_ILL_STILE`) non si modifica** nel singolo file: ciò che manca si disegna nella scena; una correzione alla libreria è una modifica di metodo, da fare in questa skill nel vault.
7. Il **link al video del prodotto reale è facoltativo**: si mette quando serve dimostrare che la tecnologia è in commercio.
8. Nessun render finale con errori del controllo (`--forza` solo per anteprime di lavoro).

## Errori già incontrati

- `page.screenshot` di Playwright è lento (0,4 s per fotogramma): `render.js` usa la cattura CDP veloce e passa i fotogrammi a ffmpeg senza file intermedi. Un video di 18 s richiede circa 70 s: lanciarlo con un timeout di almeno 5 minuti.
- Il font installato nel sistema del cloud aveva solo i pesi 400 e 700: per questo il font è incorporato nell'HTML (400, 500, 700).
- Documenti in volo o che si ingrandiscono: durante la transizione i testi sono piccoli. Il controllo lo segnala come avviso; diventa errore se il testo resta piccolo da fermo.
- Pillole e card sopra la scena: allargarle o spostarle prima di ridurre il testo (in anim1 la pillola SCARTO toccava gli angoli del mirino).
- La card del riepilogo copriva la scena: in anim1 la scena si attenua al 30% (`attenua: 0.3`), in anim2 la card va sotto il tracker.
- LibreOffice non riproduce i video: avvio automatico e loop si verificano in PowerPoint.
- Collaudo della skill (14/10/2026, anim1 rifatta da un modello più piccolo partendo solo dalla skill): il confronto byte per byte degli screenshot dava falsi errori di determinismo (rumore di rasterizzazione), ora si confronta il DOM; l'impulso dei contatori dava falsi "testi sovrapposti", ora il controllo esclude l'interlinea; nel poster restavano mirino e deviatore, da qui la regola "nel riepilogo non resta nulla in corso"; senza un modello per il nastro con più pezzi la coreografia andava inventata, da qui `BA.nastro` e lo schema in `componenti.md` §4.
