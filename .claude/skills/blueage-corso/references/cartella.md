# Cartella del corso e convenzioni

Da leggere quando si apre un corso nuovo o si salvano file nella cartella di un corso.

## Struttura della cartella

```
Formazione AI/
├── README.md                          come è organizzata la cartella
├── _archivio/                         materiale superato, non si usa come fonte
└── <aaaa>_<Cliente>_<Corso>/          un corso
    ├── CLAUDE.md                      dati, regole specifiche e stato del corso
    ├── 00_KB/
    │   ├── 01_Indice_corso.md         fonte unica dei contenuti del corso
    │   └── _archivio/
    ├── 02_Registri/
    │   ├── Decisioni_e_punti_aperti.md
    │   ├── RED_TAG_indice_inverso.md
    │   ├── PAIN_domande.md
    │   ├── Glossario.md
    │   └── Fonti_verificate.md
    └── M1/ … M5/ PW/                  un modulo per cartella
        ├── Mx_scheda.md               gate 1
        ├── Mx_storyboard.md           gate 2
        ├── Mx_deck.json               impostazioni del deck
        ├── Mx_vNN.pptx                gate 3, con Mx_vNN_anteprima.pdf
        ├── media/                     immagini e media.json
        └── kit_docenti/               materiali d'aula (sorgenti in kit_docenti/sorgenti/)
```

## Convenzioni

- Deck: `Mx_v01.pptx`, `Mx_v02.pptx`… Non si sovrascrive mai una versione consegnata: si incrementa il numero.
- Schede e storyboard si aggiornano in place; ogni modifica sostanziale va annotata in `Decisioni_e_punti_aperti.md` con la data.
- Date in formato gg/mm/aaaa nei testi, aaaa-mm-gg nei nomi file quando servono.
- I documenti superati non si cancellano: si spostano in `_archivio/` del modulo o della KB.
- Codici: RED TAG `RT-Mx-nn`, scansioni `PAIN-Mx-n`, decisioni `Dnn`, lacune `Gnn`, punti aperti con il cliente `Pnn`, fonti `Fnn`.
- In caso di conflitto tra fonti: non scegliere da soli. Segnalarlo a Lorenzo e registrarlo nelle decisioni del corso.
