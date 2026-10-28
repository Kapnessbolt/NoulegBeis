---
type: topic
kind: offerta
projects: ["[[second-brain-prodotto]]"]
clients: []
tags: [ai, pacchetto]
updated: 2026-10-28
---

# Second Brain

## Cos'è

Pacchetto da vendere che costruisce per un manager o un reparto una memoria di lavoro gestita dall'AI: raccoglie mail, chat, trascrizioni e documenti, li organizza in note collegate e ogni giorno propone priorità e cose da fare ([[ieri-sera-e-oggi-idee-su-cui-ragionare]]).

## Punti chiave

- Funzionamento: input da mail, chat di Claude, trascrizioni, SharePoint e OneDrive; memoria in Markdown collegato su GitHub o SharePoint/OneDrive; ingestion periodica delle novità e un passaggio che integra e pulisce la memoria; ogni giorno una chat con priorità e mail da rispondere ([[ieri-sera-e-oggi-idee-su-cui-ragionare]])
- Prezzi ipotizzati nelle idee per crescere: tre incontri da 2 ore; Start 2.000 €, Completo 3.000 €, Executive 4.500 €, manutenzione 15% al mese ([[blueage-le-idee-per-crescere]]); nella mail del 15–16/10 circa 2.000 € (2 + 2 ore) e circa 3.000 € con 2 ore di messa a punto ([[ieri-sera-e-oggi-idee-su-cui-ragionare]])
- Vincoli: WhatsApp non si collega alle routine di Claude, niente connettori non ufficiali per i clienti, costi AI da stimare; si parte da Claude con Copilot in parallelo, prima si vende e poi si costruisce ([[ieri-sera-e-oggi-idee-su-cui-ragionare]])
- Consegna: se Silvia lo vende, la fa Lorenzo, poi Cristian; Leonardo e/o Silvia seguono raccolta delle esigenze e criteri di importanza ([[call-di-oggi-prossimi-passi-architettura-copilot-manini-meccanotecnica-second-brain]])
- Forma del prodotto (28/10): BlueAge installa in una giornata e gestisce ogni mese, la gestione è il prodotto; il cliente fa tre gesti: Leggi (Cockpit dal telefono), Chiedi (chat sul vault con risposte e fonti), Lavora (chat sul vault in cui fa le sue attività con Claude, deck compresi, e tutto resta nel vault); git, PR, verifica dei giri e curator restano a BlueAge ([[2026-10-28-second-brain-forma-del-prodotto]])
- Tier per skill, non per ore: Start senza skill, Completo con la skill deck sul template del cliente, Executive con più skill; il briefing è il wizard di `/installa` che scrive la configurazione, con o senza BlueAge presente ([[2026-10-28-second-brain-forma-del-prodotto]])
- Repo del cliente privato nell'organizzazione GitHub di BlueAge con accordo sul trattamento dei dati; prerequisiti: piano Claude del cliente (quale, da verificare), account GitHub anche gratuito, connettore Microsoft 365; sessioni e task girano sull'account del cliente, quindi il consumo è suo ([[2026-10-28-second-brain-forma-del-prodotto]])
- Primo passo: standardizzare la versione interna e provarla su tutto il team, a partire da Leonardo ([[blueage-le-idee-per-crescere]], [[ieri-sera-e-oggi-idee-su-cui-ragionare]])

## Dove è usato

- Questo vault è la versione personale di Lorenzo e il banco di prova del prodotto: quello che funziona e i limiti trovati qui orientano l'offerta (sezione sotto) ([[2026-10-22-primo-caricamento-shared-documents-onedrive]], [[2026-10-25-cockpit-v05-smistamento]])
- Materiali di presentazione del 26/10: one pager commerciale A4 (problema, soluzione, 4 passi, contatto Silvia; niente prezzi), PDF in OneDrive `BlueAge/02_Second Brain/`; one pager tecnico navigabile per il team (architettura, strumenti, struttura del repo, giornata tipo) come artifact su claude.ai: https://claude.ai/artifact/FeqbkutspXZcAds7v8iZcL ([[2026-10-26-one-pager-second-brain]])

## Versione personale e banco di prova

- Piano per passare dal vault personale al prodotto: progetto [[second-brain-prodotto]], step 11–20 di SPEC §13 (affidabilità, uso, prodotto), principio "il codice fa la meccanica, il modello fa il giudizio" ([[2026-10-26-piano-prodotto-second-brain]])
- Interfaccia, due viste che convivono con livelli di dettaglio diversi: la dashboard Cockpit su claude.ai è il briefing, leggibile anche dal telefono e dalle sessioni cloud, alimentata dalle routine `DailyBoard`; la mod `cockpit` dell'app desktop è la postazione operativa al PC (consumo del piano Max, esito dei task, prossime cose, avvio degli agenti) ([[2026-10-24-restyling-cockpit]], [[2026-10-24-restyling-cockpit-implementazione]], [[2026-10-25-cockpit-v05-smistamento]])
- Le mod (pannelli accanto alla chat) compaiono solo dove un'app si collega alla sessione come superficie: sul desktop sì, sul telefono no, nemmeno seguendo una sessione locale; lì resta la dashboard ([[2026-10-24-interfaccia-personalizzata]], [[2026-10-25-cockpit-v05-smistamento]])
- Scartate per l'interfaccia: un frontend locale che pilota Claude Code con il login Max (uso personale tollerato ma non esplicitamente permesso, credito Agent SDK separato dal 15/06/2026) e un'interfaccia su API key (a consumo, connettori e task da rifare). Le API delle mod sono in early access e possono cambiare ([[2026-10-24-interfaccia-personalizzata]])
- Il connettore Microsoft 365 ha un nome di server diverso in sessione cloud, task schedulati e sessione locale: permessi e agenti vanno scritti per tutti e tre, e un nome nuovo blocca le letture finché non si aggiunge ([[2026-10-24-cockpit-in-locale]])
- Controllare i task schedulati è stata la procedura più ripetuta della prima settimana, e gli errori veri (ordine dei comandi git, ore in UTC, finestra del digest) sono usciti solo dalla verifica a mano: un cliente avrà bisogno di un controllo dei giri pronto, non solo di OK/errore ([[2026-10-25-comando-verifica-task]])

## Fonti

- [[ieri-sera-e-oggi-idee-su-cui-ragionare]]
- [[call-di-oggi-prossimi-passi-architettura-copilot-manini-meccanotecnica-second-brain]]
- [[blueage-le-idee-per-crescere]]
- [[blueage-le-idee-per-crescere-spunti-per-la-prossima-general]]
- [[general-di-lunedi-19-10-ordine-del-giorno-provvisorio]]
