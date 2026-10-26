# COMPASS · l'AI al lavoro — trascrizione

Metodo BlueAge per portare l'AI operativa in azienda. Trascrizione fedele del PDF `03_COMPASS_AI_al_lavoro.pdf` (BlueAge, 2 pagine, generato il 22/09/2026). Serve a leggere e citare il metodo senza aprire il PDF. In caso di dubbio fa fede il PDF.

COMPASS è una regola del metodo BlueAge: si usa solo questa definizione. Le modifiche al metodo si decidono con Leonardo e Lorenzo, e solo dopo entrano in questo file, con un commit nel vault che dice cosa cambia.

> Sette modi di usare l'AI, ognuno con un verbo. Per ciascuno: cosa fa, esempi in contesti diversi, a cosa stare attenti.

**La bussola:** C · O · M · P · A · S · S, disposte in cerchio.
*La bussola orienta. La direzione la sceglie chi guida.*

## I sette modi

### C · Codify — Mettere a sistema
**Trasforma l'esperienza delle persone in conoscenza consultabile.**
- Cosa fa il capoturno quando la macchina si comporta in un certo modo
- Un assistente che risponde sulle procedure interne
- Le non conformità risolte in un archivio interrogabile

**Attenzione:** il contenuto lo valida chi sa, e va tenuto aggiornato.

### O · Orchestrate — Automatizzare
**Toglie le operazioni ripetitive: flussi, integrazioni e AI lavorano insieme.**
- Ordini via mail o PDF caricati nel gestionale
- Certificati dei fornitori: valori estratti e registrati
- Bolle abbinate alle fatture, differenze evidenziate

**Attenzione:** prima si semplifica il processo, poi si automatizza.

### M · Monitor — Sorvegliare
**Segnala ciò che esce dalla norma, anche quando ogni valore da solo è nei limiti.**
- Un lotto con una combinazione di parametri mai vista
- Una fattura con importo anomalo rispetto allo storico
- Un ordine fuori dalle abitudini del cliente

**Attenzione:** soglie tarate bene, altrimenti gli allarmi non si guardano più.

### P · Predict — Prevedere
**Dallo storico stima cosa succederà prima che succeda.**
- La probabilità di scarto di un lotto
- La domanda del mese prossimo per articolo
- Il guasto di una macchina (manutenzione predittiva)

**Attenzione:** serve uno storico lungo, pulito e collegato all'esito.

### A · Analyze — Analizzare e interpretare
**Trova le relazioni nei dati. L'interpretazione resta a chi ha l'esperienza.**
- Scarti: quali prodotti, turni, macchine pesano di più
- Vendite: quali clienti stanno calando
- Consegne fornitori: chi sta peggiorando

**Attenzione:** due cose che si muovono insieme possono dipendere da una terza.

### S · Synthesize — Leggere e sintetizzare
**Legge in un minuto quello che richiede un pomeriggio.**
- Un capitolato di 80 pagine: requisiti e differenze dallo standard
- Un contratto fornitore: penali, scadenze, rinnovi
- Un anno di reclami: i temi che ritornano

**Attenzione:** numeri e clausole si verificano sull'originale.

### S · Spar — Ragionare in coppia
**Sparring partner: allarga le ipotesi, aiuta a scegliere, fa le domande giuste.**
- Le possibili cause di un difetto, poi le 3 da verificare
- Farsi intervistare per preparare una riunione difficile
- Scrivere requisiti o una procedura senza dimenticare pezzi

**Attenzione:** dare le aree da coprire, una domanda alla volta, riepilogo di cosa manca.

### DATA — La base di tutto
Dati completi, coerenti, collegati e sufficienti. Dati sporchi producono risposte sporche, dette con la stessa sicurezza di quelle giuste.

## Come si mette insieme

*L'AI rende quando lavora dentro un flusso e su dati solidi.*

### Orchestrate: più strumenti, un flusso
Nei casi reali il dato ordinato e quello disordinato arrivano insieme. Il risultato nasce dalla combinazione di tre strumenti:

**Integrazione** (i sistemi si passano i dati ordinati) **+ Orchestrazione** (n8n, Power Automate, Make mettono in fila le attività) **+ AI** (legge, estrae, decide dove il dato è disordinato)

**Esempio: l'ordine del cliente**
- Arriva una mail con un PDF allegato
- Il flusso la intercetta e la passa all'AI
- L'AI estrae cliente, codici, quantità, date
- Il flusso controlla anagrafiche e prezzi nel gestionale
- Se torna tutto crea l'ordine; se qualcosa non torna lo manda a una persona con il motivo

*Conta il risultato: per ogni passaggio lo strumento giusto.*

### DATA: la base
La qualità delle risposte dipende da quello che si dà all'AI.

**I quattro controlli**
- **Completi:** i campi che servono ci sono
- **Coerenti:** stesse unità, codici, definizioni
- **Collegati:** ogni evento risale alla sua origine (lotto, cliente, ordine)
- **Sufficienti:** abbastanza casi per imparare qualcosa

**L'architettura sotto:** Fonti (gestionale, macchine, Excel, documenti) → Base dati unica (pulita, collegata, storicizzata) → Uso (dashboard, analisi, AI)

*Il lavoro sui dati è la parte meno visibile e quella che decide se l'AI funziona.*
Per BlueAge è il fattore distintivo: la competenza su dati, analytics e architettura del dato viene prima dell'AI.

### Guardrail sempre validi
- Dati riservati e documenti dei clienti solo su strumenti autorizzati
- L'AI propone, la persona decide e firma
- Chiedere sempre "cosa non puoi concludere?"
- I numeri si ricontrollano alla fonte
- Le richieste che funzionano si salvano e si condividono

**La richiesta ben fatta:** Ruolo · dati · compito · limiti · formato

### Quale lettera per quale problema

| Problema | Lettera |
|---|---|
| Tutto sta in testa a poche persone | C · Codify |
| Ricopiamo a mano | O · Orchestrate |
| Ce ne accorgiamo tardi | M · Monitor |
| Vogliamo saperlo prima | P · Predict |
| Non sappiamo perché succede | A · Analyze + S · Spar |
| Troppi documenti da leggere | S · Synthesize |
| Dobbiamo preparare o decidere | S · Spar |

---

## Nota: cosa NON è nel PDF

Nei materiali del primo corso (indice Meccanotecnica, "COMPASS v2") compaiono elementi che **non sono in questo documento** e sono da validare con Leonardo (punto aperto G01 nel registro del metodo):
- i **tre livelli** Persona (Synthesize, Spar) · Dati (Analyze, Monitor, Predict) · Processo e conoscenza (Orchestrate, Codify);
- il **percorso di esecuzione in cinque passi**: Persona → DATA → Dati → Processo e conoscenza → Chi guida.

Finché non arriva una fonte BlueAge che li definisce, in slide vanno presentati come lettura del percorso formativo, non come parte della definizione originale del metodo, e non si usa la parola "livelli".
