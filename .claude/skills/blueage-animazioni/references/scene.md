# Scene al secondo · come progettare un'animazione o un'illustrazione

Il progetto si scrive **prima** del codice e si approva con Lorenzo (gate 1 della skill). Un buon file delle scene basta a chi implementa: non deve inventare nulla.

## 1. Video, illustrazione o niente

| Il concetto è… | Scelta |
|---|---|
| Un processo in passi successivi, una causa che produce un effetto, qualcosa che si muove o si trasforma (un pezzo in linea, un documento che diventa dati, una richiesta che passa da un sistema all'altro) | **Video** (15-20 s, 3-6 passi) |
| Una struttura, un confronto, una mappa, un andamento: si capisce in un colpo d'occhio e non ha un "prima e dopo" | **Illustrazione** |
| Bastano un elenco o una tabella in slide | Nessuna delle due |
| Serve dimostrare che la tecnologia esiste ed è in commercio | Immagine o video reale (regola M10 del metodo), eventualmente accanto all'animazione |

Un video è più costoso (progetto, fotogrammi, render) e in PDF diventa un'immagine ferma: se il concetto non perde nulla da fermo, meglio un'illustrazione.

## 2. Il file delle scene

Uno per animazione, accanto all'HTML: `Mx/media/animazioni/animN_<tema>_scene.md`. Modello:

```markdown
# animN_<tema> · <titolo breve>

Corso <cartella> · modulo Mx · slide nn · progetto del gg/mm/aaaa · stato: da approvare | approvato il gg/mm/aaaa

## Testo della slide (riferimento: l'animazione non se ne discosta)
"<testo della slide, copiato>"

## Messaggio chiave
<una frase: che cosa deve restare a chi guarda. Es.: il modello impara dai pezzi buoni, non da un catalogo dei difetti>

## Elementi fissi
- Etichetta: <MAIUSCOLO · MAIUSCOLO>
- Titolo: <una riga, afferma il messaggio, max ~45 caratteri>
- Passi del tracker: 01 <verbo + oggetto> · 02 … (3-6 passi, max ~28 caratteri ciascuno)
- Contatori (se servono): <NOME: valore iniziale → valori>
- Riepilogo (2-3 righe, ≤ 45 caratteri ciascuna): <riga> · <riga> · <riga>

## Dati fittizi
<tutti i nomi, codici, numeri che compaiono; coerenti con le altre illustrazioni del deck>

## Scene
| Tempo | Passo | Scena |
|---|---|---|
| 0,0-2,0 | — | … |
| 2,0-5,0 | 01-03 | … |
| … | | |
| 16,0-18,0 | tutti | Riepilogo, fermo |

## Fotogrammi chiave da approvare
t = 1 · 3,5 · 8 · 10 · 13,5 · 17,5 s (uno per ogni momento importante)

## Video del prodotto reale (facoltativo)
<URL e fonte, se nel deck si vuole anche il link; altrimenti "nessuno">

## Note di consegna (si compila alla fine)
File, durata, peso, scelte rispetto al progetto, cosa resta da migliorare.
```

## 3. Regole per scrivere le scene

1. **Parti dal testo della slide**: ogni affermazione della slide che descrive il funzionamento deve avere la sua scena; nulla che la slide non dica.
2. **Il messaggio chiave si vede**, non solo si legge: in anim1 il profilo "pezzo conforme" si sovrappone al pezzo prima della mappa delle differenze.
3. **Prima un caso normale veloce, poi il caso interessante lento.** Il caso normale mostra il meccanismo; l'anomalia mostra perché serve (e chi decide).
4. **Ogni scena dice quale passo è attivo.** Il tracker cambia a ogni scena.
5. **Tempi realistici per leggere**: 1 s + 0,25 s per parola per ogni testo nuovo; ogni passo ≥ 2 s (salvo il ciclo di richiamo veloce); riepilogo fermo 2 s.
6. **Dì dove stanno le cose che si muovono**: posizione della stazione, del deviatore, da dove entra e dove esce ogni oggetto, quale caso arriva dopo. Chi implementa non deve inventare la coreografia.
7. **Testi brevi e grandi**: titolo una riga, passi ≤ 28 caratteri, righe del riepilogo ≤ 45.
8. **Dati inventati ma plausibili** e uguali in tutto il deck (stesso ordine, stesso cliente, stessi prezzi). Mai dati reali del cliente.
9. **Niente marchi**: nessun prodotto, logo o interfaccia riconoscibile.

## 4. Esempio (estratto da anim1, approvato il 14/10/2026)

| Tempo | Passo | Scena |
|---|---|---|
| 0,0-2,0 | — | Il nastro scorre, i pezzi entrano da sinistra. Titolo ed etichetta in dissolvenza. Contatori 145 / 143 / 2 |
| 2,0-5,0 | 01-03 | **Pezzo buono.** Si ferma sotto la telecamera. 01: lampo, linea di scansione, angoli del riquadro che si chiudono. 02: profilo di riferimento "pezzo conforme" in trasparenza che si allinea; barra di scostamento bassa, in teal. 03: pillola "OK". Contatori 146 / 144 / 2. Il pezzo riparte |
| 5,0-12,0 | 01-03 | **Pezzo con difetto** (intaccatura sul bordo). 01 come sopra. 02, più lento: profilo di riferimento, poi mappa delle differenze (bagliore corallo) e riquadro tratteggiato corallo. Card "PEZZO 0147 · Scostamento dai pezzi conformi": la barra supera la soglia ("soglia decisa da chi conosce il prodotto"). "Fuori soglia: graffio sul bordo". 03: pillola "SCARTO" |
| 12,0-15,0 | 04 | Un deviatore spinge il pezzo su uno scivolo verso la vaschetta "SCARTI". Scarti 3, Controllati 147 |
| 15,0-16,0 | 01-03 | Un altro pezzo buono, ciclo rapido fino all'OK |
| 16,0-18,0 | tutti | Riepilogo fermo: "Impara dai pezzi conformi" · "Segnala ciò che se ne discosta" · "La soglia la decide chi conosce il prodotto" |

## 5. Illustrazioni

Per un'illustrazione basta un brief breve nella sezione media dello storyboard o in chat: messaggio, larghezza in slide (mezza slide 4,45" → 890 px; area utile intera 9" → 1800 px), elementi e testi, dati fittizi. File: `Mx/media/illustrazioni/ill_<tema>.html` → `ill_<tema>.png`.
