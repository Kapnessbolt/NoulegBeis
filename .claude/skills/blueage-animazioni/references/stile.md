# Stile delle animazioni e delle illustrazioni BlueAge

**Stato: v1, 14/10/2026.** Ricavato dalle due animazioni e dalle illustrazioni del deck M1 del corso Meccanotecnica, approvate da Lorenzo il 14/10/2026. Riferimenti visivi: `assets/esempio_anim1_visione.html` (video) e `assets/template_illustrazione.html` (illustrazione). I colori e i corpi sono già dentro i template: questa pagina dice **perché** e **quando**, il codice li applica.

Due stili, un solo font (**Plus Jakarta Sans**, incorporato nell'HTML da `render.js`):

| | Video didattico | Illustrazione |
|---|---|---|
| Fondo | Scuro (blu notte con griglia) | Bianco |
| Uso | Un processo che si svolge nel tempo, in slide al posto di un'immagine | Una struttura o un confronto che si legge in un colpo d'occhio |
| Formato | 1920 × 1080, 30 fps, 15-20 s, MP4 senza audio | PNG a 2x; larghezza = larghezza in slide (pollici) × 200 px |
| Template | `assets/template_animazione.html` | `assets/template_illustrazione.html` |

## 1. Palette

### Video (fondo scuro)

| Ruolo | Colore | Nella libreria |
|---|---|---|
| Fondo | gradiente radiale `#0E3358` → `#081A3A` → `#050E2D`, griglia teal al 5% | automatico |
| Card, superfici | `#0B2C4D` al 92%, bordo `#7FD3DC` al 30-50% | `BA.card` |
| Oggetti di scena (macchine, nastri) | `#13385E`, `#123A61`, bordi `#7FD3DC` | `BA.C.superficie`, `BA.C.nastro` |
| Accento, passo attivo | `#2F80ED` | `BA.C.blu` |
| Testo e linee, esito OK, passo fatto | `#7FD3DC` (teal chiaro), testo `#FFFFFF` | `BA.C.teal`, `BA.C.bianco` |
| Anomalia, scarto, caso da verificare | `#FF7A59` (corallo) | `BA.C.corallo` |
| Documenti di carta | `#F4F7FA`, testo `#0B2C4D` e `#5B6B78` | `BA.documento` |

### Illustrazione (fondo bianco)

| Ruolo | Colore | Classe o variabile |
|---|---|---|
| Titoli, testo forte, card scura | `#0B2C4D` | `.titolo`, `.forte`, `.card.scura` |
| Testo | `#3A4750` | `.testo` |
| Testo secondario, note | `#6E7C87` | `.nota` |
| Etichette, numeri, esito OK | `#1C9EB1` | `.etichetta`, `.numero`, `.ok` |
| Accento | `#2F80ED` | `.badge` |
| Card, linee | `#F2F5F8`, `#D5DEE5`; tinta teal `#E3F4F6` | `.card`, `.card.bianca` |
| Anomalia | `#FF7A59` per bordi e campiture, `#C2492C` per il testo (leggibile su bianco), tinta `#FFEDE7` | `.ko`, `.card.anomalia`, `.evidenza` |
| Chip (token, parole) | `#DCEBFD`, `#D7F0F3`, `#FFE3D9`, `#E8EDF2` | `.k0`…`.k3` |

**Mai il vermiglio `#E8452C`**: è il colore dei RED TAG. `render.js check` si ferma se lo trova.

## 2. Tipografia e corpi minimi

In slide il video occupa circa metà larghezza: un testo di 28 px su 1920 diventa piccolo. Pochi testi, grandi.

| Elemento (video, su 1920 px) | Corpo | Peso |
|---|---|---|
| Etichetta di testa (maiuscolo, spaziatura 5) | 22 px | bold, teal |
| Titolo | 44 px | bold, bianco |
| Passi del tracker | numero `01` 20 px, testo 28 px | bold |
| Testi essenziali (card, esiti, riepilogo) | ≥ 28 px | bold |
| Etichette (maiuscolo, spaziatura 3-4) | ≥ 20 px | bold, teal |
| Numeri dei contatori | 48 px | bold |
| Dati dimostrativi (campi di un documento, maschere) | 22-24 px | |
| Disclaimer | 18 px, bianco al 45% | regular |

| Elemento (illustrazione, scala 200 px per pollice) | Corpo |
|---|---|
| Titoli delle card, voci principali | 30 px |
| Testo | 26 px |
| Note | 22 px |
| Etichette | 20 px |

Minimo assoluto controllato da `render.js`: **20 px** (disclaimer 16). Un testo che fa solo da texture (le righe di un documento finto) si sostituisce con linee grigie (`doc.linee`) o si marca `data-ba="decoro"`.

## 3. Composizione del video

| Zona | Dove (px su 1920 × 1080) | Contenuto |
|---|---|---|
| Testa | x 96, y 80-170 | Etichetta e titolo: il titolo afferma il messaggio e sta in 1100 px (circa 50 caratteri a 44 px) |
| Tracker dei passi | x 96, da y 250, un passo ogni 95 px, 3-6 passi | Cosa sta succedendo adesso |
| Scena | x 730-1824, y 220-820 (può usare tutta la larghezza, come il nastro di anim1) | Gli oggetti che si muovono |
| Fascia bassa | y 840-1000 | Contatori a sinistra, riepilogo a destra (o sotto il tracker) |
| Disclaimer | in basso a destra, y 1042 | "Illustrazione BlueAge · animazione didattica, non è un prodotto" |

Margine di sicurezza: 96 px ai lati; nessun testo a meno di 20 px dal bordo.

## 4. Movimento

- **Easing morbido** (`easeInOutCubic`, in libreria `BA.ep`). Niente rimbalzi, rotazioni gratuite, zoom, effetti da videogioco.
- **Una cosa nuova alla volta**: l'occhio deve sapere dove guardare. Fra due novità in punti diversi dello schermo almeno 0,3 s.
- **Il tracker guida**: il passo attivo si accende in blu, quelli fatti diventano teal con la spunta. Ogni cambio di scena corrisponde a un passo.
- **Tempo di lettura**: un testo nuovo resta fermo almeno 1 s + 0,25 s per parola.
- **Entrate** in 0,3-0,6 s con un leggero scorrimento (14 px); **uscite** in dissolvenza 0,3 s.
- Ogni passo dura almeno 2 s, salvo il **ciclo di richiamo** veloce prima del riepilogo (un caso già visto che ripassa tutti i passi in circa 1 s). L'anomalia (il caso interessante) ha più tempo dei casi normali.
- **L'anomalia si vede ma non si evidenzia** finché il passo che la scopre non la mette in luce (bagliore, riquadro): disegnata piccola e discreta sul pezzo o sul documento.

## 5. Struttura nel tempo

| Momento | Durata | Cosa succede |
|---|---|---|
| Apertura | 0-1,5 s | Dissolvenza dal nero, testa e tracker, contatori. La scena è già "in funzione" |
| Caso normale | 2-4 s | Un giro rapido di tutti i passi: si capisce il meccanismo |
| Caso interessante | 5-8 s | L'anomalia, l'eccezione, la decisione: più lento, con la spiegazione (card, motivo) |
| Chiusura del caso | 2-3 s | Esito: scarto deviato, caso passato a una persona, ordine registrato |
| Riepilogo | ultimi 2 s, fermo | Tutti i passi teal; card con 2-3 righe che dicono il messaggio |

Il loop è pulito: dissolvenza dal nero nei primi 0,35 s e verso il nero negli ultimi 0,3 s (automatica).

## 6. Il poster

Nel PDF della dispensa il video è un'immagine ferma: il **poster** (fotogramma a durata − 0,5 s, dentro il riepilogo) deve raccontare da solo tutto il processo. Tracker completo, riepilogo leggibile; se la card del riepilogo copre elementi chiave della scena, la scena si attenua (`riepilogo.attenua: 0.3`) o la card va in un'area libera.

## 7. Contenuti

- Spiega **come funziona**, passo per passo. Non è pubblicità e non è realistica: è uno schema animato.
- **Dati fittizi**, coerenti con il testo della slide e con le altre illustrazioni del deck, e dichiarati (disclaimer nel video; "esempio inventato" nell'illustrazione o nella didascalia).
- **Nessun marchio** né interfaccia riconoscibile di terzi: casella di posta generica, "Gestionale" con l'icona di un database, nessun logo.
- Italiano, termini del glossario del corso.
