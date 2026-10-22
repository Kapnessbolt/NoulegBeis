---
type: source-mail
conversation_id: "AAQkAGMyY2M5ZTczLTYwNDEtNGZiOC1iYjJjLTFhZjJhOGY1YjFiMQAQAOANjKoJuZ9OicSrWQyFIb0="
subject: "Twilio // Blueage follow up"
participants: ["[[cristian-schifone]]"]
first_message: 2026-10-11T20:36:01Z
last_message: 2026-10-12T12:24:04Z
messages: 5
attachments: []
projects: ["[[parts-radar-sviluppo]]"]
clients: []
topics: ["[[parts-radar]]"]
status: active
---

# Twilio // Blueage follow up

## Riassunto

Scambio con Twilio sul canale WhatsApp per [[parts-radar]]. L'interlocutore, "Isa Bell" (Digital Sales, Twilio), è un agente AI di vendita: lo dichiara la firma, e le mail hanno il link di disiscrizione marketing. Le sue indicazioni tecniche vanno quindi verificate.

Lorenzo, con [[cristian-schifone]] in copia, spiega l'esigenza: portare la linea WhatsApp Business dei clienti (i ricambisti) dentro un flusso automatico che inoltri i messaggi in ingresso al sistema BlueAge, senza personalizzazioni lato utente; vuole processare testo, audio e immagini.

Twilio indica la strada "build" con Programmable Messaging su WhatsApp. Ogni linea del cliente punta a un webhook HTTPS pubblico di BlueAge, che riceve ogni messaggio in ingresso con un HTTP POST. Il campo `To` dice quale numero cliente ha ricevuto il messaggio e serve al routing multi-tenant. Per i media contano `NumMedia`, `MediaUrl0` e `MediaContentType0`; `MessageSid` serve per tracciamento e deduplica. Se non serve rispondere all'utente, basta una risposta TwiML vuota. Altri consigli: validare la firma delle richieste con l'SDK Twilio e accettare parametri aggiuntivi senza errori. Formati WhatsApp supportati: immagini JPG/PNG/WEBP, audio OGG/AMR/3GP/AAC/MPEG. Resta aperta la domanda di Twilio sullo stack del webhook (Node, PHP o .NET).

## Decisioni e azioni

-

## Messaggi

### 2026-10-11 22:36 · Isa Bell (Twilio, agente AI)

Follow-up commerciale: chiede se BlueAge vuole partire con build (API), integrate (piattaforma esistente) o buy (soluzione di un partner).

### 2026-10-12 12:20 · Lorenzo Curione

Spiega che serve solo governare in automatico l'inbound WhatsApp Business dei clienti verso il servizio BlueAge, senza personalizzazioni.

### 2026-10-12 12:50 · Isa Bell (Twilio, agente AI)

Consiglia Programmable Messaging su WhatsApp con un webhook HTTPS che riceve l'inbound, il routing per cliente sul campo `To` e una risposta TwiML vuota; manda i link alla documentazione e chiede se gestire solo testo o anche media e posizione.

### 2026-10-12 13:55 · Lorenzo Curione

Vuole processare testo, audio e immagini.

### 2026-10-12 14:24 · Isa Bell (Twilio, agente AI)

Conferma che testo, audio e immagini passano nello stesso flusso inbound; elenca i campi del payload utili, i formati supportati e i consigli (validare la firma, parser tollerante); chiede lo stack del webhook.
