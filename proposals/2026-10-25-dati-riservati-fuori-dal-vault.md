---
type: proposal
date: 2026-10-25
kind: regola
status: accettata
---

# Regola scritta sui dati riservati che non entrano nel vault

## Motivazione

Cosa non scrivere nelle note è stato deciso caso per caso in tre lotti e in un task schedulato: GUID e IBAN nel lotto Delivery, credenziali, compensi, codici Teams e CV nel lotto Outlook, dati reali di Manini nel caso DDT. La SPEC dice solo "nessun materiale sensibile" (§1), e il perimetro di OneDrive (§5.2) include tutte le sottocartelle, compresa `Dati/`, dove ci sono i DDT reali. Il 24/10 l'ingest-sharepoint li ha saltati di sua iniziativa; un altro giro potrebbe farne una nota e portarla su GitHub, contro la policy AI di Manini. Con la regola la scelta è la stessa in ogni sessione e in ogni task.

## Evidenze

- [[2026-10-22-primo-caricamento-delivery]]: "Nessun dato sensibile riportato (GUID, tenant ID, IBAN, account personali)", deciso nel lotto.
- [[2026-10-22-primo-caricamento-outlook]]: 10 thread esclusi a mano (personali, contratto, compensi, credenziali); omessi credenziali Solera, codici Teams, compensi, indirizzi e telefoni; CV non ingeriti.
- [[2026-10-23-manini-automazione-ddt]]: dati reali solo su OneDrive in `Dati/`, perché la policy AI di Manini li ammette solo nel tenant o anonimizzati.
- [[2026-10-24]]: 3 PDF in `Progetto Automazione/Dati/` non ingeriti; il digest propone di escludere la cartella dal perimetro con una PR.

## Testo proposto

`CLAUDE.md` §5, in coda all'elenco:

```markdown
- Dati riservati, nemmeno riassunti: credenziali, token, codici di accesso e di riunione; IBAN e coordinate bancarie; GUID, tenant ID e account dei sistemi dei clienti; compensi e contratti personali; indirizzi e telefoni personali; CV. La nota dice che il documento li contiene ("credenziali del web service demo, omesse"), non il valore.
- Dati reali dei clienti riga per riga (DDT, ordini, anagrafiche, export di tabelle): restano su OneDrive nelle cartelle `Dati/` e non generano note. La nota del progetto cita solo la cartella e i numeri aggregati. Se la policy AI del cliente limita l'uso dei dati, scrivilo nella nota del cliente.
- Thread personali o estranei a BlueAge: non si ingeriscono. Nel dubbio, in sessione chiedi; nei task schedulati scarta e scrivi solo mittente e oggetto in `## Scartate` del digest.
```

`SPEC.md` §5.2, dopo "Tutte le sottocartelle di `BlueAge/` sono incluse…" (PR dedicata):

```markdown
Esclusioni in qualunque punto del percorso: cartelle `Dati` (dati reali dei clienti, es. `01_Materiale clienti/Manini/Progetto Automazione/Dati/`), che restano su OneDrive e non generano note (`CLAUDE.md` §5).
```
