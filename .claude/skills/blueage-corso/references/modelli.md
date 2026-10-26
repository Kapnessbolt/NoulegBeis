# Modelli per un corso nuovo

Copiare questi modelli nella cartella del corso quando si apre un corso nuovo. Il corso Meccanotecnica (`2026_Meccanotecnica_AI-DDM/`) è l'esempio completo da guardare: scheda e storyboard di M1 sono i riferimenti per il livello di dettaglio.

## 1. `CLAUDE.md` del corso

```markdown
# <Corso> · <Cliente> — istruzioni del corso

Leggere all'inizio di ogni sessione di lavoro su questo corso, poi `02_Registri/Decisioni_e_punti_aperti.md`. Metodo, workflow e regole comuni stanno nelle skill `blueage-corso` e `blueage-deck`: qui solo ciò che è specifico del corso.

## 1. Il corso in breve
- **Corso:** titolo, ore, partecipanti (numero e ruolo), committente ed ente erogatore, finanziamento.
- **Date:** avvio, chiusura, vincoli di calendario.
- **Docenti:** chi presenta che cosa.
- **Deliverable:** deck per modulo (elenco), kit, dispensa PDF.
- **Piede dei deck:** testo esatto del campo `corso` in `Mx_deck.json`.
- **Priorità attuale:** modulo e gate in corso.

## 2. Fonti del corso
| File | Cosa decide |
|---|---|
| `00_KB/01_Indice_corso.md` | Contenuti, calendario, filo rosso, laboratori. Titoli e monte ore dei moduli depositati non si cambiano |
| `02_Registri/` | Decisioni, RED TAG, domande "Tocca a voi", glossario, fonti verificate |
| `Mx/` | Scheda, storyboard, `Mx_deck.json`, deck, media, kit del modulo |

## 3. Regole specifiche del corso
Solo ciò che si aggiunge o si discosta dal metodo (es. riservatezza dei dati del cliente, strumenti autorizzati, nomi da non citare).

## 4. Stato
Gate raggiunto per ogni modulo, con data.
```

## 2. `02_Registri/Decisioni_e_punti_aperti.md`

```markdown
# Decisioni e punti aperti

Da leggere all'inizio di ogni sessione, subito dopo `CLAUDE.md`. Le decisioni non si rimettono in discussione senza una nuova voce che le superi.

## 1. Decisioni
| # | Data | Decisione | Motivo |
|---|---|---|---|
| D01 | gg/mm/aaaa | … | … |

## 2. Lacune
| # | Lacuna | Impatto | Azione | Stato |
|---|---|---|---|---|

## 3. Punti aperti con il cliente
| # | Punto | Impatto sui deck | Stato |
|---|---|---|---|

## 4. Storico delle modifiche
| Data | Cosa | Dove |
|---|---|---|
```

Una decisione superata non si cancella: si scrive **Superata da Dnn** all'inizio della cella.

## 3. `02_Registri/RED_TAG_indice_inverso.md`

```markdown
# RED TAG · Indice inverso del corso

Stati: proposta · in scelta · approvata · in slide (con numero di slide). Stili delle proposte: A contrasto · B slogan · C metafora d'officina · D domanda diretta.

## 1. Registro
| ID | Frase in slide | Nucleo concettuale | Modulo | Contenuti collegati | Slide | Stato | Note |
|---|---|---|---|---|---|---|---|
| RT-M1-01 | «…» | … | M1 | Cap. … | … | proposta | Alternative: A «…» · B «…» · C «…» · D «…» |

## 2. Sequenza delle sole frasi
Per modulo, in ordine di proiezione.

## 3. Nuclei da coprire nei moduli successivi
| Modulo | Nuclei candidati |
|---|---|
```

## 4. `02_Registri/PAIN_domande.md`

```markdown
# Scansione PAIN · Registro delle domande

Documento interno: in slide la scansione si chiama "Tocca a voi" e non dichiara il proprio scopo.

## 1. Progressione di riferimento
(linee guida §3.3)

## 2. Scansioni per modulo
### M1 · Focus: …
**PAIN-M1-1 · Titolo** (dopo cap. …, sessione …)
- domanda 1
- …
Raccolta: …

## 3. Struttura della mappa PAIN cumulativa
ID · Processo/area · Attività · Descrizione · Esempi ed evidenze · Conseguenze · Gestione attuale · Informazioni e sistemi · Vincoli · Aspetti da chiarire · Possibile contributo (lettera COMPASS) · Criteri di verifica · Modulo di origine e aggiornamenti · Stato (confermata · ipotesi · aperta)

## 4. Regole per scrivere nuove domande
(linee guida §3.4) + controllare che la domanda non sia già nel registro.
```

## 5. `02_Registri/Glossario.md`

```markdown
# Glossario del corso

Termini da usare in modo identico in tutti i moduli. Fonte: KB = indice o linee guida · COMPASS = metodo · Proposta = definizione scritta per il corso.

| Termine | Definizione | Fonte |
|---|---|---|
```

Partire dal glossario del corso Meccanotecnica per i termini COMPASS e i fondamenti di AI: sono già scritti per chi parte da zero.

## 6. `02_Registri/Fonti_verificate.md`

```markdown
# Fonti · Registro delle verifiche

Stati: da verificare · verificata (con data) · superata (indicare cosa è cambiato) · scartata.

| # | Fonte | Uso previsto | Modulo / cap. | Stato | Data verifica | Note |
|---|---|---|---|---|---|---|
| F01 | [Titolo](url) | … | M1 cap. … | verificata | gg/mm/aaaa | che cosa dice esattamente, date, numeri |
```

Anche le immagini e i video in slide hanno una riga (autore, licenza, file in `Mx/media/`).

## 7. `Mx/Mx_scheda.md` (gate 1)

```markdown
# Mx · Titolo — Scheda modulo (gate 1)

vNN · gg/mm/aaaa · stato del gate. Fonte dei contenuti: `00_KB/01_Indice_corso.md`.

Marcatori: [da verificare · Pxx] · [solo dispensa] · [proposta] · [Fxx]

## 1. Obiettivo formativo e contributo al percorso (con 2-3 risultati osservabili)
## 2. Collegamento con COMPASS (tabella elemento → dove → uso)
## 3. Nuclei concettuali e progressione (tabella N1… con capitoli, RED TAG, sessione)
## 4. Capitoli approfonditi (per ognuno: concetti da trasmettere, esempi, demo o esercizio, verifica, solo dispensa)
## 5. RED TAG e indice inverso del modulo
## 6. "Tocca a voi": domande e conduzione
## 7. Esempi, dimostrazioni ed esercitazioni (tabella; materiali da preparare; sfide tra sessioni)
## 8. Output per il dossier
## 9. Raccordo con il modulo precedente e il successivo
## 10. Articolazione delle sessioni (minuti per blocco)
## 11. Fonti da verificare
## 12. Punti aperti e dipendenze
## 13. Esito del gate 1 (tabella proposta → esito → decisione)
```

## 8. `Mx/Mx_storyboard.md` (gate 2)

```markdown
# Mx · Storyboard — Sessione n · data · orario · modalità

vNN · gg/mm/aaaa · stato del gate. Fonte: `Mx/Mx_scheda.md`.

**Impostazioni del deck**
- Tracker dei capitoli: 01 … · 02 … (devono coincidere con `Mx_deck.json`)
- RED TAG: variante vermiglio

**Minuti per blocco:** … = totale

---

# APERTURA · n minuti

## 01 · COPERTINA
occhiello: CLIENTE · CORSO
titolo: …
sottotitolo: Modulo n · Sessione n · data
docenti: …
rif: —
note: |
  - …
min: 1

---

# CAP. 01 · TITOLO · n minuti
…
```

Formato completo dei campi per tipo di slide: skill `blueage-deck`, `references/storyboard_format.md`.

## 9. `Mx/Mx_deck.json`

```json
{
  "modulo": "M1",
  "titolo_modulo": "…",
  "capitoli": ["…", "…"],
  "titolo_deck": "M1 · … · Sessione 1",
  "corso": "Cliente  ·  Titolo del corso",
  "compass_evidenza": [6, 7],
  "red_tag_variante": "vermiglio",
  "parole_vietate": ["PAIN"]
}
```
