---
type: source-doc
source: sharepoint
family: velo-ce-indice-evidenze
current:
  item_id: 01EFCYUZ7EZBAXN7HLLRCYZHLGVDQKDC3O
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ7EZBAXN7HLLRCYZHLGVDQKDC3O
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/06 Evidenze/00 Indice evidenze Velo-CE.md
  name: 00 Indice evidenze Velo-CE.md
  last_modified: 2026-10-29T16:14:45Z
versions:
  - { name: "00 Indice evidenze Velo-CE.md", item_id: 01EFCYUZ7EZBAXN7HLLRCYZHLGVDQKDC3O, last_modified: 2026-10-29T16:14:45Z }
  - { name: "00 Indice evidenze Velo-CE.md", item_id: 01EFCYUZ5R6F2FB6XZEFDYWFHHPPEFF36F, last_modified: 2026-10-28T08:04:54Z }
  - { name: "00 Indice evidenze Velo-CE.md", item_id: 01EFCYUZ6MMJXJUHRGHRHZ3N3NZITV3FTI, last_modified: 2026-10-08T10:43:55Z }
also_at: []
status: active
partial: true
ingested_at: 2026-10-30T05:58:45Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, business-central, evidenze, indice, interno]
---

# Velo-CE · Indice delle evidenze

## Riassunto

Indice interno BlueAge, non mostrabile al cliente, di tutte le schermate ed export salvati nella cartella delle evidenze del progetto Velo-CE: una riga per evidenza con file, pagina di Business Central, cosa mostra, esito e documento di rilevazione collegato. La serie E riguarda il tenant del cliente (Production ed Educational, Admin Center, Entra), sempre in sola lettura; la serie T il tenant BlueAge (sandbox Essentials e Premium, società dimostrativa CRONUS IT), usato per stabilire cosa fa lo standard. È la base documentale di tutti i giudizi «VERIFICATO» degli altri file di progetto. Ultimo aggiornamento interno del 27/10/2026. Il connettore restituisce circa 200.000 caratteri: nota parziale.

## Punti chiave

- **Convenzione**: codice in testa al nome del file (decisione del 18/09), data AAMMGG, sistema e pagina; dal 02/10 la cartella è «06 Evidenze» con gli export in una sottocartella.
- **Sezioni lette (serie E, 17/09-07/10)**: assemblaggio, giro dell'ordine e pianificazione; distinte e calcolo del piano su Educational; licenze, ruoli e fatturazione nell'Admin Center M365; gestione estensioni, servizi web e coda processi; catalogo oggetti per app; log di accesso Entra e registrazione dell'app «CRM»; un ordine del canale automatico; i sei job So Smart; operazioni sugli ambienti; dettaglio di Production e app installate; elenco ambienti; tabelle EOS che crescono; modulo IVC; assemblaggio su ordine Van Nicholas; strumento PDA; fattura elettronica in uscita e conto lavoro; Accruals; Advanced Document Reporting; valore del magazzino e bilancio; scarico componenti; ubicazioni.
- **Sezioni lette (serie T, 17/09-24/09)**: prove Essentials contro Premium sul tenant BlueAge in dieci round (conto lavoro, costo dell'assemblato, varianti, ruoli Entra e accesso senza licenza, cascata del piano su più livelli in Essentials, make-to-order in Premium, riattivazione di una voce di coda da un'altra utenza).
- **Esiti ricorrenti**: 1 Production + 3 sandbox senza slot libero; AMFR entra con rettifiche positive da giugno 2026; conto lavoro su assemblaggio non standard («C\Lavoro» a zero); 144 tabelle EOS con righe, 36 cresciute in 5 giorni; 10 ubicazioni con campo principale non standard; la pagina di pianificazione si apre in Essentials.
- L'aggiornamento più recente (T155-T172, 08/10) riguarda il confronto fra ciclo d'acquisto standard ordine-carico-fattura e carico da Registrazioni magazzino: non compreso nella parte letta.
- **Aggiornamenti dal 08/10 al 27/10** (dalle note di aggiornamento in testa al file): T273-T290 (24/10) costi accessori d'acquisto con gli addebiti TRASP e DAZI in VC-NBC PROVA; E223-E224 (26/10) fatture di tubi registrate su conto con quantità 1 e senza unità di misura (OP-46); T291-T295 (26/10) import del master v005 e conti delle nuove categorie in VC-IMPORT PROVA; E227-E230 (26/10) errore IVA sul flusso MMI segnalato da We Make Code dopo gli aggiornamenti notturni delle app del 23/10 in Production; T296-T299 (27/10) unità di stockkeeping e pianificazione per colore; E231 (27/10) XML della fattura mensile DHL con sei spedizioni; E232-E236 (27/10) transitorio dogana fra bolla e fattura della bolla e conto anticipi a fornitori.
- Dal 28 al 29/10: E237-E252 (tenant della posta e di BC), E253-E255 (flusso MMI, altra sessione), E256-E264 (conti del ciclo d'acquisto in Production), T300-T334 (prove per scenario e anticipi in VC-IMPORT PROVA) ([[velo-ce-stato-progetto-99-log-revisioni]]).

## Numeri

- Evidenze E fino a E159 nella parte letta; T fino a T172 (ultimo aggiornamento).
- Assemblaggio: 1.263 righe di distinta, 571 ordini registrati, 10 ordini aperti; AMFR 705 pezzi da 6 output di assemblaggio (05/2025-03/2026).
- Flusso MMI: da 25.515 a 25.747 movimenti fra il 24 e il 29/09.
- Al 27/10: serie E fino a E236, serie T fino a T299.

## Decisioni e azioni

- Decisione del 18/09: codice dell'evidenza in testa al nome del file.
- Nessuna azione esplicita nella parte letta.

## Versioni

- 00 Indice evidenze Velo-CE.md · 2026-10-08 · prima versione ingerita; data di modifica della riorganizzazione della cartella; letta solo la prima pagina (partial)
- 00 Indice evidenze Velo-CE.md · 2026-10-28 · aggiornato al 27/10 (E fino a E236, T fino a T299); lette le note di aggiornamento in testa, contenuto oltre i 200.000 caratteri non letto; nella cartella `Cristian/06 Evidenze/`
- 00 Indice evidenze Velo-CE.md · 2026-10-29 · evidenze fino a E264 e T334 (prossimi E265 e T335): inventario della posta E237-E252, conti del ciclo d'acquisto E256-E264, prove per scenario e anticipi T300-T334; aggiornato dal log revisioni, file non riletto
