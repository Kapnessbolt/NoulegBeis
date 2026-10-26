# Componenti · libreria BA (video) e classi delle illustrazioni

Riferimento per scrivere un'animazione con `assets/template_animazione.html` e un'illustrazione con `assets/template_illustrazione.html`. Le firme qui sotto sono quelle del codice (`BA_ANIM_LIB v1`): se non trovi un componente, disegnalo nella scena con `BA.el` invece di modificare la libreria.

## 1. Com'è fatto il file di un'animazione

Copia del template, rinominata `animN_<tema>.html`. Tre blocchi, si scrive solo nel terzo:

| Blocco | Cosa | Si tocca? |
|---|---|---|
| `<svg id="s">` con i livelli `fondo`, `testa`, `trk`, `scena`, `hud`, `cnt`, `recap`, `foot`, `veil` | La tela 1920 × 1080 | No |
| `BA_ANIM_LIB v1` | Libreria: tempo, componenti, struttura fissa, anteprima | **Mai** |
| `ANIMAZIONE` | `CONFIG`, `prepara(A)`, `scena(t, A)`, `BA.avvia(...)` | Sì: si sostituisce l'esempio |

```js
var CONFIG = {
  nome: 'anim3_manutenzione',          // = nome del file
  durata: 18,                          // secondi (15-20)
  etichetta: 'MANUTENZIONE PREDITTIVA · SENSORI',
  titolo: 'Il guasto si annuncia prima di arrivare',
  passi: ['Misura le vibrazioni', 'Confronta con il normale', 'Segnala la deriva'],
  fasi: [[2.0,'attivo',1], [4.0,'attivo',2], [6.5,'attivo',3], [8.0,'reset'] /* … */],
  contatori: { voci: [ {nome:'MACCHINE', colore:'ok', valori:[[0,12]]},
                       {nome:'AVVISI', colore:'scarto', valori:[[0,0],[9.5,1]]} ] },
  riepilogo: { righe: ['Impara il comportamento normale', {testo:'Avvisa prima del fermo', icona:'attenzione'}], w: 760 },
  fotogrammi: [1, 3.5, 8, 10, 13.5, 17.5]   // per l'anteprima da approvare
};
var S = {};                          // oggetti della scena
function prepara(A) { /* costruisce una volta: S.x = BA.card(A.scena, {...}) */ }
function scena(t, A) { /* per ogni istante t: S.x.mostra(t, 3.0, 9.0) */ }
BA.avvia(CONFIG, prepara, scena);
```

### CONFIG

| Campo | Obbligatorio | Significato |
|---|---|---|
| `nome`, `durata`, `etichetta`, `titolo` | sì | `durata` default 18 |
| `passi` | sì (3-6) | Testi del tracker; `[]` = nessun tracker (solo se il concetto non ha passi) |
| `fasi` | sì | Stato del tracker nel tempo, vedi sotto |
| `tracker` | no | `{x, y, passo}` default `{96, 250, 95}` |
| `contatori` | no | `{x, y, larghezza, voci:[{nome, colore, valori:[[t, valore], …]}]}`; default in basso a sinistra (96, 900). Il numero cambia a ogni istante di `valori` con un piccolo impulso |
| `riepilogo` | sì | `{righe, w, x, y, da, attenua}`. `righe`: stringhe o `{testo, icona:'spunta'|'attenzione'|'croce'}`. Default: in basso a destra, `da` = durata − 2, `attenua` = 1 (0,3 se la card copre la scena) |
| `fotogrammi` | no | Istanti per l'anteprima; default 1 · 3,5 · 8 · 10 · 13,5 · durata − 0,5 |
| `poster`, `fps`, `disclaimer` | no | Default durata − 0,5 · 30 · "Illustrazione BlueAge · animazione didattica, non è un prodotto" |

**Fasi del tracker** (n parte da 1; fra uno stato e l'altro c'è una dissolvenza di 0,2 s):

| Fase | Effetto |
|---|---|
| `[t, 'attivo', n]` | Passo n blu, quelli prima teal con spunta, quelli dopo spenti |
| `[t, 'fatto', n]` | Passi fino a n teal con spunta, gli altri spenti |
| `[t, 'reset']` | Tutti spenti (arriva un nuovo pezzo, un nuovo documento) |
| `[t, 'tutti']` | Tutti teal con spunta. Se manca, la libreria la aggiunge a `riepilogo.da` + 0,35 s |

Con più casi in sequenza (pezzi, documenti) ogni caso riparte da `reset`, e un passo che vale solo per alcuni casi (es. "04 Devia lo scarto") si accende solo per quelli. Le fasi di anim1:
```js
fasi: [[2.0,'attivo',1],[2.9,'attivo',2],[4.1,'attivo',3],[4.7,'reset'],              // pezzo buono: 01-03
       [5.4,'attivo',1],[6.4,'attivo',2],[9.4,'attivo',3],[12.0,'attivo',4],[14.8,'reset'], // pezzo difettoso: 01-04
       [15.0,'attivo',1],[15.4,'attivo',2],[15.7,'attivo',3],[16.0,'tutti']]             // ciclo di richiamo veloce, poi riepilogo
```

### Le tre regole del codice
1. **Solo funzioni di t.** `scena(t)` imposta tutto lo stato a partire da t: posizione, opacità, testo. Niente variabili che si accumulano da un fotogramma all'altro, niente `setTimeout`, `Date`, `Math.random` (c'è `BA.casuale(seme)`), niente animazioni CSS.
2. **Costruisci in `prepara`, aggiorna in `scena`.** In `scena` non si creano elementi.
3. **Non toccare l'opacità di `A.scena` e `A.hud`** (la usa il riepilogo: con `attenua` si attenua **tutto** ciò che sta nei due livelli) né il `transform` di `pezzo.dentro` (lo usa `mostra`): per spostare un pezzo si usa `pezzo.sposta(x, y)`.
4. **Nel riepilogo non resta nulla "in corso"**: mirini, deviatori, frecce, pillole di un ciclo e card di dettaglio spariscono prima di `riepilogo.da` (parametro `off` di `mostra`). Il controllo automatico non lo vede: guardare il poster.

`A` contiene: `A.scena` (livello degli oggetti), `A.hud` (sopra la scena: card, pillole, testi di esito), `A.defs`, `A.C` (colori), `A.durata`.

## 2. Tempo

| Funzione | Restituisce |
|---|---|
| `BA.pr(t, a, b)` | Avanzamento lineare 0→1 fra a e b (0 prima, 1 dopo) |
| `BA.ep(t, a, b)` | Come `pr` ma con easing morbido. **La più usata** |
| `BA.finestra(t, on, off, din=0.4, dout=0.3)` | 0→1 da `on`, poi 1→0 da `off` (`off` null = resta). Per le opacità |
| `BA.bump(t, a, b)` | 0→1→0 fra a e b (lampi, impulsi) |
| `BA.chiavi(t, [[t0,v0],[t1,v1,'eout'],…])` | Valore interpolato fra fotogrammi chiave; v numero o `[x,y]`; terzo elemento facoltativo `'eio'` (default), `'eout'`, `'ein'`, `'lin'`. Per fermare un oggetto si ripete il valore: `[[2,0],[4.5,0],[5.3,330]]` |
| `BA.scalino(t, [[t0,v0],[t1,v1]])` | Ultimo valore con tempo ≤ t (testi o numeri che cambiano di colpo) |
| `BA.lerp(a, b, u)`, `BA.clamp(x)`, `BA.mix(colore1, colore2, u)` | Interpolazione di numeri e di colori `#RRGGBB` |

## 3. Componenti del video

Tutti prendono come primo argomento il livello genitore (`A.scena`, `A.hud`, o il `.corpo` di una card). Molti restituiscono un **Pezzo**:

| Pezzo | |
|---|---|
| `p.sposta(x, y, scala, rotazione)` | Posizione del gruppo |
| `p.mostra(t, on, off, {dy:14, dx:0, scala, entrata:0.4, uscita:0.3, max:1})` | Compare a `on` scorrendo di `dy` (o scalando da `scala`), sparisce a `off` (null = resta). Restituisce l'opacità |
| `p.opacita(v)` | Opacità diretta |
| `p.g`, `p.dentro` | Gruppo esterno (posizione) e interno (comparsa): per aggiungere elementi si usa `p.dentro` |

| Componente | Firma | Note |
|---|---|---|
| Gruppo vuoto | `BA.gruppo(parent, x, y)` → Pezzo | Per gli oggetti propri della scena |
| Card | `BA.card(parent, {x, y, w, h, etichetta, titolo, icona, colore:'ok'|'scarto'|'info'|hex, bordo})` → Pezzo con `.corpo` (gruppo sotto l'intestazione), `.fondo`, `.etichetta`, `.titolo` | Etichetta 20 px, titolo 28 px. Il colore vale per bordo ed etichetta |
| Righe etichetta-valore | `BA.righe(parent, {x, y, w, passo:64, righe:[['CLIENTE','Rossi S.r.l.'], …], icone:true})` → array di Pezzi con `.eti`, `.val`, `.sfondo`, `.icona(nome, colore)` | Il pannello "Campi estratti" e il "Gestionale" di anim2. `.sfondo` è il riquadro corallo di errore (opacità 0); `.icona` mette spunta o croce a destra e restituisce l'elemento (opacità con `BA.op`) |
| Pillola | `BA.pillola(parent, 'OK', 'ok'|'scarto'|'info'|'neutra', {x, y})` → Pezzo | Larghezza automatica. Per comparire: `p.mostra(t, on, off, {dy:0, scala:0.8})` |
| Barra con soglia | `BA.barraSoglia(parent, {x, y, w, soglia:0.5, nota})` → `{imposta(u)}` | Teal sotto soglia, corallo sopra; la tacca della soglia si accende quando la supera |
| Mirino | `BA.mirino(parent, {x, y, lato:184})` → `{ciclo(t, t0, tFine)}` | Angoli che si chiudono (t0 → t0+0,6), lampo, linea di scansione (t0+0,25 → t0+0,95), uscita a tFine (se null: all'inizio del riepilogo). Restituisce l'intensità del lampo (per far brillare una telecamera). Un ciclo alla volta: con più casi vedi §4 |
| Nastro | `BA.nastro(parent, {y:640, h:170, freccia:true})` → `{scorri(d), y, centro}` | Nastro trasportatore a tutta larghezza con tacche e freccia di direzione; `scorri(d)` muove le tacche con lo stesso spostamento dei pezzi |
| Scansione | `BA.scansione(parent, {x, y, w, h})` → `{passa(t, a, b)}` | Linea luminosa che scende da y a y+h fra a e b (su un documento) |
| Connettore | `BA.connettore(parent, {da:[x,y], a:[x,y], curva:true, colore})` → `{disegna(u)}` | La linea si disegna con u da 0 a 1 (`c.disegna(BA.ep(t, 5, 5.6))`); punto all'arrivo |
| Testo che si scrive | `BA.digita(elementoTesto, 'Rossi S.r.l.', u)` | Mostra i primi u × n caratteri |
| Documento di carta | `BA.documento(parent, {x, y, w, h, titolo})` → Pezzo con `.riga(y, 'Cliente:', 'Rossi S.r.l.')` → `{box, eti, val}` e `.linee(y, n, passo)` | `.box` è l'evidenziazione blu (opacità 0); `.linee` disegna righe grigie al posto del testo che non va letto |
| Lista con icone | `BA.lista(parent, righe, {x, y, passo:48, corpo:28})` → array di Pezzi | Come il riepilogo; righe stringa o `{testo, icona}` |
| Icone | `BA.icona(parent, nome, x, y, r=22, colore)` | `spunta`, `croce`, `attenzione` (cerchio pieno); `gestionale`, `persona`, `mail`, `documento` (a linea) |
| Testi | `BA.testo(parent, 'testo', {x, y, 'font-size':28, fill, 'text-anchor'})`, `BA.etichetta(parent, 'MAIUSCOLO', {x, y})` | Default: bianco 28 px bold; etichetta teal 20 px spaziata |
| Elementi SVG | `BA.el('rect', {…}, parent)`, `BA.set(el, {…})`, `BA.op(el, v)`, `BA.tr(x, y, s, r)`, `BA.larghezza(testo)` | Per tutto ciò che non è un componente |

Filtri e gradienti già pronti in `defs`: `url(#ba-glow)` (bagliore), `url(#ba-ombra)` (ombra), `url(#ba-lampo)` (lampo), `url(#ba-caldo)` (bagliore corallo della mappa delle differenze).

## 4. Schemi ricorrenti

**Un oggetto che entra, si ferma e riparte** (documento che vola):
```js
var x = BA.chiavi(t, [[0,-330,'eout'],[2,0],[4.5,0],[5.3,330],[12,330],[12.9,660]]);
S.pezzo.sposta(x + 1040, 725);
```

**Un nastro con più pezzi**: un solo spostamento `D(t)` per tutti; ogni pezzo ha la sua posizione di partenza `x0`, distanziata di quanto il nastro avanza a ogni passo, così che a ogni fermata un pezzo diverso sia sotto la stazione. Nessun pezzo passa la stazione senza essere controllato: fra un caso e l'altro il nastro avanza di un passo intero.
```js
function D(t){ return BA.chiavi(t, [[0,-330],[2.0,0,'eout'],[4.6,0],[5.4,360],[12.0,360],[12.9,720]]); }
// prepara: S.pezzi = [1040, 680, 320].map(function(x0){ var p = BA.gruppo(A.scena, x0, 725); p.x0 = x0; /* disegno */ return p; });
// scena:   var d = D(t); S.nastro.scorri(d); S.pezzi.forEach(function(p){ p.sposta(p.x0 + d, 725); });
```
Il pezzo che esce dal nastro (deviato, prelevato) segue la sua traiettoria da quando lo tocca il deviatore: vedi `assets/esempio_anim1_visione.html`.

**Un ciclo di controllo ripetuto** (pezzi diversi, stessa sequenza): descrivi i cicli come dati e trova quello in corso. L'esempio completo, con card diverse per caso conforme e caso difettoso, è `assets/esempio_anim1_visione.html`.
```js
var CICLI = [ {t0:2.0, fine:4.5, ok:true}, {t0:5.3, fine:12.0, ok:false} ];
function inCorso(t){ for (var c of CICLI) if (t >= c.t0 && t < c.fine + 0.3) return c; return null; }
// in scena(t): var c = inCorso(t); if (c) S.mirino.ciclo(t, c.t0, c.fine);
```

**Una riga che diventa errore**:
```js
BA.op(S.righe[4].sfondo, BA.finestra(t, 11.2));
BA.op(S.croce, BA.finestra(t, 11.2));
BA.op(S.motivo, BA.finestra(t, 11.6));     // testo corallo con il motivo
```

**Un testo che cambia con lo stato**: `S.esito.textContent = c.ok ? 'Entro soglia' : 'Fuori soglia: graffio sul bordo';`

## 5. Errori tipici (li trova `render.js check`)

| Sintomo | Causa | Rimedio |
|---|---|---|
| "renderAt non deterministica" | Una variabile accumulata fra fotogrammi, un `Math.random` | Calcolare tutto da t |
| "corpo … < 20 px" | Testo piccolo o dentro un gruppo scalato | Ingrandire; testo decorativo → `doc.linee` o `data-ba="decoro"` |
| "testo tagliato dal bordo" | Testo che esce dalla tela mentre è visibile | Spostare o farlo comparire dopo |
| "testi sovrapposti" (avviso) | Card sopra una scena con testo | Spostare, oppure `riepilogo.attenua` |
| Mirino, deviatore o pillole ancora visibili nel poster | Elemento senza `off` | Farlo uscire prima di `riepilogo.da` |
| Elemento che non compare | Opacità mai portata a 1, o creato in `scena` | `mostra`/`finestra`; creare in `prepara` |

## 6. Comandi di `render.js`

| Comando | Cosa fa |
|---|---|
| `node scripts/render.js check file.html` | Solo controlli |
| `node scripts/render.js fotogrammi file.html [1,3.5,8]` | Controlli, poi i fotogrammi (default `CONFIG.fotogrammi`) in `anteprime_<nome>/` e la tavola `<nome>_anteprime.png`; i fotogrammi vecchi dello stesso file vengono sostituiti |
| `node scripts/render.js video file.html` | Controlli, MP4, poster, verifica con ffprobe e tre fotogrammi estratti dall'MP4 in `anteprime_<nome>/<nome>_dal_video_*.png` |
| `node scripts/render.js png file.html` | Controlli e PNG a 2x (illustrazioni) |
| Opzioni | `--out <cartella>` (default: quella dell'HTML) · `--forza` (prosegue con errori: solo anteprime di lavoro) |

Ogni comando **incorpora il font nell'HTML e lo riscrive**: si lancia sulle copie di lavoro, mai sui file della skill.

## 7. Illustrazioni: classi del template chiaro

Si scrive HTML con queste classi sotto il commento `ILLUSTRAZIONE`; dimensioni con `body{--w:…px; --h:…px;}` (larghezza = pollici in slide × 200; l'altezza si stringe al contenuto, `render.js` avvisa se avanza spazio).

| Classe | Uso |
|---|---|
| `.riga`, `.colonna`, `.centro` (+ `style="--spazio:20px"`) | Impaginazione flex |
| `.titolo` (30 px navy), `.testo` (26 px), `.nota` (22 px grigio), `.etichetta` (20 px teal maiuscolo), `.forte`, `.ok`, `.ko` | Testi |
| `.card`, `.card.bianca` (bordo e ombra), `.card.scura` (navy, per l'elemento conclusivo), `.card.anomalia`, `.piede` (fondo della card con linea) | Riquadri |
| `.numero` / `.numero.pieno`, `.badge` (`.teal`, `.navy`), `.pill` (`.teal`, `.chiara`, `.anomalia`) | Marcatori |
| `.chips` con `<span class="k0">…</span>` (k0-k3), `.evidenza` | Token, parole, elementi da notare |
| `.tratteggio`, `<svg class="freccia"><use href="#i-freccia"/></svg>` | Collegamenti |
| `<svg class="icona"><use href="#i-mail"/></svg>` (`i-documento`, `i-gestionale`, `i-persona`, `i-spunta`, `i-croce`, `i-attenzione`, `i-ingranaggio`) | Icone; colore con `style="color:var(--teal)"`, dimensione con `--i:36px` |

Per grafici e schemi con coordinate (curve, anelli) si può disegnare un `<svg>` dentro la pagina, con gli stessi colori (`var(--…)` non vale negli attributi SVG: usare gli esadecimali di `stile.md`).
