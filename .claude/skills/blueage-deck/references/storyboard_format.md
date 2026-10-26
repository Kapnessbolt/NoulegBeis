# Formato dello storyboard, di deck.json e di media.json

`scripts/build_deck.js` legge tre file e non inventa nulla: tutto il testo viene dallo storyboard.

```
node build_deck.js <Mx_storyboard.md> <Mx_deck.json> <Mx_vNN.pptx> [media.json]
```

Se `media.json` non è indicato, il build lo cerca in `media/media.json` accanto allo storyboard.

## 1. Storyboard (`Mx_storyboard.md`)

### Struttura

- `# CAP. 05 · TITOLO · minuti` apre un capitolo: il numero dopo `CAP.` accende il capitolo nel tracker della testa. Un `#` senza `CAP.` (es. `# APERTURA`, `# PAUSA`, `# CHIUSURA`) azzera il capitolo.
- `## 07 · TIPO` apre una slide: numero a due cifre, tipo dal catalogo della style guide (§5).
- Campi su una riga: `campo: testo`. Campi su più righe: `campo: |` e poi righe rientrate di due spazi.
- `---` chiude la slide corrente.
- Il testo prima della prima slide (intestazione, impostazioni, note) è ignorato dal build: si usa per le note di lavoro. Unica eccezione: una riga che contiene `RED TAG: variante giallo` (o `vermiglio`) imposta la variante dei RED TAG per tutto il deck.

### Campi comuni

```
## 07 · CONTENUTO
occhiello: FONDAMENTI DELL'AI
titolo: Il modello genera la risposta parola per parola, non la recupera
corpo: |
  testo completo della slide (frasi intere; elenchi con "- ", numerati con "1. ")
visual: descrizione dell'eventuale schema o immagine; per le card: "icone Lucide: Nome1, Nome2, …"
fonte: Autore – Titolo (data consultazione)
rif: COMPASS S·Synthesize · RT-M1-05 · PAIN-M1-3
note: |
  - punto da sottolineare
  - domanda da porre all'aula
min: 3
```

- `rif:`, `visual:` e `min:` non vanno in slide. `note:` e `min:` vanno nelle note del docente ("Tempo: 3 min").
- `min: 0 · solo dispensa`: la slide sta nel deck e nel PDF ai partecipanti, in aula si salta.

### Campi per tipo

| Tipo | Campi |
|---|---|
| COPERTINA | `occhiello`, `titolo`, `sottotitolo`, `docenti` |
| DOMANDA | `occhiello`, `titolo`, `corpo` (prima riga invito, poi 2-4 voci "- ") |
| AGENDA | `occhiello`, `titolo`, `corpo` (righe sessione `Sessione 1 · data · durata · modalità · titolo`, sotto le voci "- "), `sintesi` |
| CONTENUTO | `corpo`, `esempi` (card "In pratica"), `attenzione` (card scura) |
| QUATTRO_CARD | `corpo` (riga introduttiva facoltativa; 4 voci `- Titolo · descrizione` oppure `- Titolo · ETICHETTA · descrizione` oppure `- Titolo · valore · descrizione`), `sintesi`, `visual: icone Lucide: …` |
| TABELLA | `intro` (facoltativo), `righe` (prima riga intestazione; celle separate da ` \| `), `sintesi` |
| DUE_CARD | `card_sx`, `card_dx` (prima riga `ETICHETTA` o `ETICHETTA · NUMERO GRANDE`, poi righe di testo; una riga che inizia con « è una citazione), `caso`, `sintesi` |
| ESERCIZIO | `passi` (righe `1 · testo`), `output`, `regola`. Se l'occhiello contiene ESPERIMENTO o LABORATORIO cambia l'icona |
| COMPASS | `corpo` (7 righe `- C · Codify · Mettere a sistema: descrizione` e una riga `DATA · …`). Le lettere da evidenziare stanno in `deck.json` |
| NUMERI | `corpo` (breve, facoltativo), `grafico` (righe `tipo: barre`, `titolo: …`, poi `etichetta \| valore`), `numeri` (2-4 righe `valore \| testo`), `criterio`, `sintesi` |
| TIMELINE | `passi` (3-5 righe `quando \| nome \| descrizione`; `nome · sottotitolo` facoltativo; se `quando` è un numero non compare l'etichetta), `sintesi` |
| IMMAGINE | `corpo`, `lettera` (es. `M · Monitor`), `immagine` (che cosa mostrare e da dove), `video` (descrizione e link), `esempi` (box tinto sotto il testo), `didascalia`. File e link reali stanno in `media.json` |
| NORMA | `corpo`, `caso` (card scura "Caso reale"), `scenario` (card chiara "In fabbrica") |
| SEZIONE | `numero`, `titolo`, `sottotitolo` |
| RED_TAG | `etichetta` (`RED TAG · 01`), `frase` (`prima parte \| seconda parte`), `alternative` (righe `A · … \| …`, vanno nelle note), `variante` (facoltativo) |
| TOCCA_A_VOI | `invito`, `titolo`, `domande` (righe `01 testo`), `suggerimento` |
| PAUSA | `titolo`, `durata` |
| CHIUSURA | `etichetta`, `titolo`, `sottotitolo`, `corpo`, `aggancio` |

### Marcatura del testo

- `**testo**` grassetto · `_testo_` corsivo · `<br>` a capo dentro una cella di tabella.
- `[DA VERIFICARE · …]` resta in rosso sulla slide finché non viene sostituito.

## 2. Impostazioni del deck (`Mx_deck.json`)

```json
{
  "modulo": "M1",
  "titolo_modulo": "L'AI nei contesti industriali",
  "capitoli": ["COMPASS", "Stato dell'arte", "…"],
  "titolo_deck": "M1 · L'intelligenza artificiale nei contesti industriali · Sessione 1",
  "corso": "Meccanotecnica Umbra  ·  AI & Data-Driven Management",
  "compass_evidenza": [6, 7],
  "red_tag_variante": "vermiglio",
  "parole_vietate": ["PAIN"]
}
```

| Campo | Uso |
|---|---|
| `modulo`, `titolo_modulo` | Percorso nella testa delle slide |
| `capitoli` | Tracker della testa e indice delle slide SEZIONE (l'ordine è quello dei numeri `CAP.`) |
| `titolo_deck` | Titolo del file PowerPoint (proprietà del documento) |
| `corso` | Testo del piede |
| `compass_evidenza` | Posizioni 1-7 delle lettere da evidenziare in blu nella slide COMPASS (C=1, O=2, M=3, P=4, A=5, S Synthesize=6, S Spar=7) |
| `red_tag_variante` | `vermiglio` o `giallo` |
| `parole_vietate` | Parole che fermano il build se compaiono nei testi visibili o nelle note (default `PAIN`) |

## 3. Immagini e video (`media/media.json`)

Una voce per numero di slide IMMAGINE. I file stanno nella stessa cartella `media/`.

```json
{
  "27": { "file": "inspekto.png", "video": "https://…", "video_titolo": "Inspekto Product Video · Siemens · 1:30" },
  "28": { "file": "estrazione.png", "video": "https://…", "video_titolo": "…", "play": false },
  "64": { "file": "harness.png", "schema": ["Istruzioni", "Documenti", "Strumenti", "Memoria", "Permessi"], "schema_centro": "MODELLO" }
}
```

- `video`: l'immagine, il pulsante play e la riga "Guarda il video" diventano link.
- `"play": false` toglie il pulsante (per le illustrazioni che non sono fotogrammi).
- `schema`: etichette disposte attorno al centro dell'immagine, con `schema_centro` (default "MODELLO") al centro.
- Se il file manca, la slide mostra un riquadro rosso `[DA INSERIRE …]` e il build va avanti.
