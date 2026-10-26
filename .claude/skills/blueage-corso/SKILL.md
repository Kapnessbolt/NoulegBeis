---
name: blueage-corso
description: "Use when designing, building or updating a BlueAge training course on AI (any client): course folder setup, the 4-gate workflow (module sheet, storyboard, deck build, registers), COMPASS method, RED TAG and 'Tocca a voi' (PAIN scan) rules, teacher kits. Includes the AI & Data-Driven Management course for Meccanotecnica Umbra."
---

# Corso BlueAge · metodo e procedura

Come si progetta e si produce un corso di formazione BlueAge sull'AI, dal primo indice alle slide. Vale per ogni corso e ogni cliente. Per costruire le slide (gate 3) si usa anche la skill `blueage-deck`.

## File da caricare quando servono

| File | Quando |
|---|---|
| `references/principi.md` | Prima di scrivere una scheda o uno storyboard: slide come dispensa, COMPASS, "Tocca a voi", RED TAG, riservatezza e kit dei docenti, lingua |
| `references/linee_guida.md` | Regole complete e checklist (§6 scheda, §10 modulo, §11 corso). **Vincolanti per ogni modulo** |
| `references/compass.md` | Definizione originale del metodo COMPASS. Unica definizione ammessa |
| `references/modelli.md` | Modelli per aprire un corso nuovo: `CLAUDE.md` del corso, registri, scheda, storyboard, `Mx_deck.json` |
| `references/cartella.md` | Struttura della cartella del corso e convenzioni (versioni, date, codici, archivio, conflitti tra fonti) |

## Dove sta il materiale

| Dove | Cosa |
|---|---|
| Vault Second Brain, `.claude/skills/blueage-corso/` | Questa skill: fonte unica del metodo. Si modifica solo qui |
| Cartella sul PC `C:\Users\curione.l\Desktop\Formazione AI\` | Un corso per sottocartella: indice, registri, schede, storyboard, deck, kit, media |
| OneDrive BlueAge | Copia della cartella, sempre all'ultima versione (Lorenzo, a mano) |

Senza la cartella del corso non si lavora sui contenuti: dirlo a Lorenzo e chiedere di collegare il PC o di allegare i file. Un file del corso non si riscrive mai ricostruendolo da un output troncato: si modifica in place o si sovrascrive da una copia completa.

## Inizio di ogni sessione

1. Capire su quale corso si lavora (se non è chiaro, elencare le cartelle dei corsi e chiedere).
2. Leggere `CLAUDE.md` del corso e `02_Registri/Decisioni_e_punti_aperti.md`.

## Aprire un corso nuovo

1. Creare la cartella `<aaaa>_<Cliente>_<Corso>/` come in `references/cartella.md`, con i modelli di `references/modelli.md`.
2. Scrivere `00_KB/01_Indice_corso.md` dal programma depositato e dai vincoli del cliente: contesto, impostazione didattica, moduli con titoli e ore, calendario, punti aperti. Titoli e monte ore depositati non si cambiano (rendicontazione).
3. Riusare dal corso più vicino ciò che è generico (glossario dei termini COMPASS e dei fondamenti di AI, modelli di kit) e verificare di nuovo tutto ciò che cambia nel tempo.

## Workflow per modulo: 4 gate

Non si passa al gate successivo senza l'OK esplicito di Lorenzo.

1. **Scheda modulo** (`Mx_scheda.md`): gli 8 punti del §6 delle linee guida, più articolazione per sessione con minuti, fonti da verificare, punti aperti. Leggere prima `references/principi.md`.
2. **Storyboard** (`Mx_storyboard.md`): una voce per slide nel formato della skill `blueage-deck` (`references/storyboard_format.md`). Qui si scrive tutto il testo definitivo: il build non inventa contenuti. Insieme allo storyboard si prepara `Mx_deck.json`.
3. **Build e controllo**, con la skill `blueage-deck`: generare `Mx_vNN.pptx` dallo storyboard, controllare anteprime slide per slide, testi che sforano, style guide, checklist §10 delle linee guida, fonti verificate. Salvare .pptx e PDF di anteprima nella cartella del modulo. Le correzioni puntuali si fanno nello storyboard e si rigenera.
4. **Registri**: aggiornare RED TAG, domande "Tocca a voi", glossario, fonti e decisioni del corso.

## Quando cambia il metodo

Una regola nuova o diversa (linee guida, COMPASS, style guide, generatore) vale per tutti i corsi: si propone a Lorenzo e, con il suo OK, si modifica questa skill (o `blueage-deck`) nel vault, con un commit `vault: <cosa cambia>` che dice la regola nuova. Il vault è l'unica copia: niente versioni parallele in plugin o zip.
