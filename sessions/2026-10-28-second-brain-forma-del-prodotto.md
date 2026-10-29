---
type: session
date: 2026-10-28
surface: cloud
topics: ["[[second-brain]]"]
outcome: "Forma del prodotto Second Brain decisa: installazione fatta da BlueAge, tre gesti per il cliente (Leggi, Chiedi, Lavora), gestione mensile come prodotto, repo nell'organizzazione BlueAge; step 18 e 19 di SPEC §13 riscritti (SPEC 1.22), scheda del progetto e tema aggiornati, in PR"
---

# Second Brain: forma del prodotto per il cliente

## Obiettivo

Capire come il vault diventa un prodotto commerciale usabile da un manager non tecnico: facile da integrare, "self-installing", personalizzabile con un briefing facoltativo.

## Decisioni

- Non "self-installing per il cliente" ma installato da BlueAge in una giornata e gestito ogni mese. Nella prima settimana la fatica è stata operare (verifica dei giri, errori meccanici trovati solo a mano), non installare: un non tecnico non installa male, opera male, e il sistema degrada in silenzio. Il self-install (`/installa`) resta lo strumento interno con cui BlueAge installa in modo ripetibile. La "manutenzione al 15%" delle ipotesi di prezzo è il prodotto, non un accessorio (proposta della sessione, confermata dall'utente)
- Il cliente vede tre gesti: Leggi (Cockpit dal telefono), Chiedi (chat sul vault, risposte con le fonti dal librarian), Lavora (chat sul vault in cui fa le sue attività con Claude, deck compresi, e tutto resta nel vault). Git, PR, SPEC, permessi, verifica dei giri e curator non li vede mai (dall'utente: il terzo gesto è lavorare nel vault, non solo appuntare; la cattura via mail con oggetto `Appunto: …` resta una comodità dal telefono)
- Perché "Lavora" regga senza la disciplina del cliente, quattro cose passano dalla regola alla macchina: chiusura automatica (hook di fine turno che fa commit e push di ciò che è cambiato; task notturno che rilegge le sessioni del giorno e scrive diario, righe di log e attività, perché dai task schedulati si possono elencare le sessioni dell'account e leggerne gli eventi); consegna dei file prodotti (scheda scaricabile nella chat e nome del file nella nota del progetto finché il connettore non carica i binari; da chiudere prima di qualunque installazione esterna); integrità invisibile (la sessione corregge da sola gli errori del controllo e non li espone, il curator segnala a BlueAge il resto); skill del cliente (template pptx raccolto nel briefing e trasformato in skill durante l'installazione). Onestà sul "subito": i file sono salvati a ogni turno, la knowledge (decisioni, stato dei progetti) entra a fine sessione o la notte
- Il briefing è il wizard di `/installa`: elenca librerie e cartelle viste dal connettore e chiede sì/no, chiede nome, fuso, lingua, repository di progetto, e scrive `vault.yaml`. Con BlueAge presente è il briefing, senza è la stessa conversazione: così il briefing è facoltativo senza affidarsi a perimetri di default, che è la cosa che più cambia da un cliente all'altro. Lo step 13 progetta `vault.yaml` come output del wizard
- Quattro passi restano a mano perché sono azioni di account nelle interfacce di claude.ai e GitHub: piano Claude del cliente, repo creato dal template con l'app GitHub di Claude installata, ambiente cloud, autorizzazione del connettore Microsoft 365 (circa 15 minuti in condivisione schermo). Il resto lo fa `/installa` da una sessione: creazione dei task schedulati (da una sessione cloud esiste lo strumento per crearli con orario, modello e connettori), controllo dei tre nomi del connettore, permessi, giro di prova
- Repo del cliente: opzione A, repo privato nell'organizzazione GitHub di BlueAge, uno per cliente, con il cliente come collaboratore; l'opzione B (organizzazione del cliente) solo su richiesta di chi ha un IT. Motivi: la gestione è il prodotto e con il repo in casa BlueAge controlla upgrade, PR del curator, secret scanning e backup; il cliente non vede GitHub; markdown e git restano portabili, il repo si trasferisce alla sua organizzazione se lo chiede o se se ne va. Condizioni: accordo sul trattamento dei dati (nomina a responsabile) come documento contrattuale, non una riga della SPEC; accesso minimo di BlueAge (un team GitHub per cliente, un collaboratore per vault). Il cliente ha un account GitHub, anche gratuito, solo per collegare l'ambiente al repo (raccomandazione della sessione, confermata dall'utente)
- Vincoli da scrivere nei prerequisiti: sessioni e task girano sull'account Claude del cliente, quindi il consumo è suo e BlueAge non può lanciare sessioni al suo posto (gestione via repo e, per i guasti, intervento con il cliente collegato); il piano Claude necessario per sessioni cloud e task schedulati è da verificare, oggi il vault gira sul Max di Lorenzo
- I tier si distinguono per le skill, non per le ore di incontro: Start senza skill, Completo con la skill deck sul template del cliente, Executive con più skill
- Nessuno step nuovo: chiusura automatica, integrità invisibile, cattura via mail e `/installa` entrano nello step 18; la consegna dei file diventa prerequisito dello step 18; skill del cliente, upgrade del motore, repo nell'organizzazione BlueAge e accordo sui dati entrano nello step 19. La prova di "installabile" è la prima installazione interna, a Leonardo, con template e wizard: giornata cronometrata e ogni passo manuale annotato; quella lista è la guida di installazione e il perimetro del contratto di gestione

## File toccati

- `sessions/`: questo diario
- `projects/second-brain-prodotto/`: scheda (stato, attività degli step 18 e 19, decisioni, prossimi passi, fonti) e log
- `topics/second-brain.md`: tre gesti, installazione e gestione, tier e repo in `## Punti chiave`
- `SPEC.md`: 1.22, §13.1 step 18 e 19 riscritti, §13.2 forma del prodotto, §14 consegna dei file; sul branch della sessione, entra in `main` con una PR

## Aperti

- [x] Unire la PR di questa sessione (SPEC 1.22, scheda del progetto, tema) (chiuso: PR #36 unita)
- [ ] Prima di qualunque installazione esterna: chiudere la consegna dei file prodotti (scheda scaricabile e nome nella nota, o connettore che carica i binari)
- [ ] Verificare quale piano Claude serve al cliente per sessioni cloud e task schedulati
