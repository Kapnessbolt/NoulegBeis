# Dal video alla slide

Come si porta un'animazione nel deck PowerPoint, in accordo con la skill `blueage-deck`. Provato il 14/10/2026 sul deck M1 v06 di Meccanotecnica (slide 31 e 32).

## 1. Come si presenta in slide

| Aspetto | Regola |
|---|---|
| Posizione | Al posto dell'immagine di una slide IMMAGINE: mezza slide a destra, `x 5,05" · y 1,4" · larghezza 4,45"` (altezza 16:9 = 2,5"). A tutta larghezza solo se la slide è dedicata al video (`x 0,5" · larghezza 9"`) |
| Avvio | Automatico all'ingresso della slide, in loop, senza audio, poster visibile da fermo |
| Poster | `animN_<tema>_poster.png` (riepilogo finale): è anche ciò che si vede nel PDF della dispensa |
| Didascalia | "Animazione BlueAge: come funziona, passo per passo." |
| Fonte (in piccolo, in fondo alla slide) | "animazione BlueAge (gg/mm/aaaa)"; dati fittizi dichiarati se compaiono nomi o numeri |
| Note del docente | "L'animazione parte da sola e va in loop (N s): commentarla seguendo il tracker a sinistra" |
| Link al prodotto reale | **Facoltativo.** Se nel deck serve anche la prova che la tecnologia è in commercio, una riga "▶  Il prodotto reale" con il link al video ufficiale (regola M10: link cliccabile, niente QR, fonte registrata). Altrimenti l'animazione basta |

## 2. Due strade

| Situazione | Strumento |
|---|---|
| Il deck si genera dallo storyboard con `build_deck.js` | Voce della slide IMMAGINE in `media/media.json` (skill `blueage-deck`, `references/storyboard_format.md` §3, regola M13 del metodo): `"file"` (il poster, anche come immagine di riserva), `"video_file": "animazioni/animN_<tema>.mp4"`, `"poster": "animazioni/animN_<tema>_poster.png"`; facoltativi `"video"` e `"video_titolo"` per il link al prodotto reale. Dopo il build: `python3 scripts/post_build.py Mx_vNN.pptx Mx/media/media.json` (skill `blueage-deck`) incorpora il video |
| Il deck esiste già ed è stato modificato a mano | `scripts/add_video.py` sul .pptx, salvando una nuova versione |

```bash
python3 scripts/add_video.py M1_v06.pptx M1_v07.pptx --slide 31 \
  --video media/animazioni/anim1_visione.mp4 --poster media/animazioni/anim1_visione_poster.png \
  --x 5.05 --y 1.4 --w 4.45 --togli immagine \
  [--link https://… --testo-link "▶  Il prodotto reale"]
```

- `--togli`: nomi delle forme da eliminare (l'immagine che il video sostituisce, un vecchio pulsante play). Se un nome non esiste, lo script elenca le forme presenti.
- La durata del timing si legge dal file MP4.
- OUT diverso da IN: una versione consegnata non si sovrascrive (convenzione `Mx_vNN`).
- Didascalia, fonte e note si aggiornano nello storyboard (deck generato) o a mano sul .pptx (deck modificato a mano).

Esempio di voce in `media.json`:
```json
"31": { "file": "animazioni/anim1_visione_poster.png", "video_file": "animazioni/anim1_visione.mp4",
        "poster": "animazioni/anim1_visione_poster.png" }
```
Con il link al prodotto reale si aggiungono `"video": "https://…"` e `"video_titolo": "…"`.

## 3. Controllo

- LibreOffice **non** riproduce i video e le sue anteprime mostrano solo il poster: va bene per controllare l'impaginazione, non l'avvio.
- L'avvio automatico e il loop si verificano in PowerPoint: chiedere a Lorenzo di aprire la slide in presentazione prima della consegna.
- Peso: ogni video aggiunge 1-3 MB al .pptx.
