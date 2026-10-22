---
type: session
date: 2026-10-22
surface: cloud
topics: ["[[fatturazione-elettronica-sdi]]", "[[percorso-supply-chain-magazzino]]"]
outcome: "Due temi nuovi, ruoli nei progetti, progetto corso-ai-manini, verifica dell'hook di pre-commit"
---

# Temi, ruoli nei progetti e verifica dell'hook

## Obiettivo

Chiudere le decisioni sul lotto Delivery e verificare in una sessione nuova l'hook che blocca i commit con errori.

## Decisioni

- Nuovi temi approvati dall'utente: `fatturazione-elettronica-sdi` (collegato a 13 fonti Velo-CE) e `percorso-supply-chain-magazzino` (10 fonti Manini).
- Ruoli dichiarati dall'utente: Velo-CE non lo segue (lo seguono Cristian Schifone e Leonardo Pinsone); nel percorso supply chain di Manini non è coinvolto.
- L'utente segue la formazione AI di Manini insieme a Leonardo Pinsone, in aula come docente ma nel ruolo di AI consultant: creato il progetto `corso-ai-manini`.
- Hook di pre-commit: in una sessione nuova blocca correttamente un commit con un link rotto. Limite trovato: se lo stesso comando crea il file e fa il commit, il controllo gira prima che il file esista e lo lascia passare.

## File toccati

- `topics/fatturazione-elettronica-sdi.md`, `topics/percorso-supply-chain-magazzino.md`
- `projects/corso-ai-manini/`, ruoli in `projects/velo-ce-progetto-dynamics/` e `projects/manini-supply-chain-magazzino/`
- campo `topics` di 23 fonti, `clients/manini.md`, `people/leonardo-pinsone.md`

## Aperti

- [x] Limite dell'hook chiuso con il pre-commit di git (SPEC 1.8, PR #8 mergiata)
- [ ] Prossimo lotto: Shared Documents
