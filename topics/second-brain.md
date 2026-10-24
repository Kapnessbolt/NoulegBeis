---
type: topic
kind: offerta
projects: []
clients: []
tags: [ai, pacchetto]
updated: 2026-10-25
---

# Second Brain

## Cos'è

Pacchetto da vendere che costruisce per un manager o un reparto una memoria di lavoro gestita dall'AI: raccoglie mail, chat, trascrizioni e documenti, li organizza in note collegate e ogni giorno propone priorità e cose da fare ([[ieri-sera-e-oggi-idee-su-cui-ragionare]]).

## Punti chiave

- Funzionamento: input da mail, chat di Claude, trascrizioni, SharePoint e OneDrive; memoria in Markdown collegato su GitHub o SharePoint/OneDrive; ingestion periodica delle novità e un passaggio che integra e pulisce la memoria; ogni giorno una chat con priorità e mail da rispondere ([[ieri-sera-e-oggi-idee-su-cui-ragionare]])
- Prezzi ipotizzati nelle idee per crescere: tre incontri da 2 ore; Start 2.000 €, Completo 3.000 €, Executive 4.500 €, manutenzione 15% al mese ([[blueage-le-idee-per-crescere]]); nella mail del 15–16/10 circa 2.000 € (2 + 2 ore) e circa 3.000 € con 2 ore di messa a punto ([[ieri-sera-e-oggi-idee-su-cui-ragionare]])
- Vincoli: WhatsApp non si collega alle routine di Claude, niente connettori non ufficiali per i clienti, costi AI da stimare; si parte da Claude con Copilot in parallelo, prima si vende e poi si costruisce ([[ieri-sera-e-oggi-idee-su-cui-ragionare]])
- Consegna: se Silvia lo vende, la fa Lorenzo, poi Cristian; Leonardo e/o Silvia seguono raccolta delle esigenze e criteri di importanza ([[call-di-oggi-prossimi-passi-architettura-copilot-manini-meccanotecnica-second-brain]])
- Primo passo: standardizzare la versione interna e provarla su tutto il team, a partire da Leonardo ([[blueage-le-idee-per-crescere]], [[ieri-sera-e-oggi-idee-su-cui-ragionare]])

## Dove è usato

- Questo vault è la versione personale di Lorenzo ([[2026-10-22-primo-caricamento-shared-documents-onedrive]])
- Interfaccia della versione personale, due viste che convivono con livelli di dettaglio diversi: la dashboard Cockpit su claude.ai è il briefing, leggibile anche dal telefono e dalle sessioni cloud, alimentata dalle routine `DailyBoard`; la mod `cockpit` dell'app desktop è la postazione operativa al PC (consumo del piano Max, esito dei task, prossime cose, avvio degli agenti) ([[2026-10-24-restyling-cockpit]], [[2026-10-24-restyling-cockpit-implementazione]], [[2026-10-25-cockpit-v05-smistamento]])
- Le mod (pannelli accanto alla chat) compaiono solo dove un'app si collega alla sessione come superficie: sul desktop sì, sul telefono no, nemmeno seguendo una sessione locale; lì resta la dashboard ([[2026-10-24-interfaccia-personalizzata]], [[2026-10-25-cockpit-v05-smistamento]])
- Scartate per l'interfaccia: un frontend locale che pilota Claude Code con il login Max (uso personale tollerato ma non esplicitamente permesso, credito Agent SDK separato dal 15/06/2026) e un'interfaccia su API key (a consumo, connettori e task da rifare). Le API delle mod sono in early access e possono cambiare ([[2026-10-24-interfaccia-personalizzata]])

## Fonti

- [[ieri-sera-e-oggi-idee-su-cui-ragionare]]
- [[call-di-oggi-prossimi-passi-architettura-copilot-manini-meccanotecnica-second-brain]]
- [[blueage-le-idee-per-crescere]]
- [[blueage-le-idee-per-crescere-spunti-per-la-prossima-general]]
- [[general-di-lunedi-19-10-ordine-del-giorno-provvisorio]]
