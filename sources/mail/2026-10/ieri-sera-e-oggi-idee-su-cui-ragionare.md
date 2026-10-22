---
type: source-mail
conversation_id: "AAQkAGMyY2M5ZTczLTYwNDEtNGZiOC1iYjJjLTFhZjJhOGY1YjFiMQAQAJqLSDAR-wxFoUCpV3hJUPQ="
subject: "Ieri sera e oggi · idee su cui ragionare"
participants: ["[[leonardo-pinsone]]", "[[cristian-schifone]]"]
first_message: 2026-10-15T18:34:26Z
last_message: 2026-10-16T11:55:23Z
messages: 2
attachments: []
projects: ["[[corso-ai-mtu]]", "[[corso-ai-manini]]"]
clients: ["[[meccanotecnica-umbra]]", "[[velo-ce]]", "[[manini]]"]
topics: ["[[blueage]]", "[[second-brain]]", "[[business-central-ai]]", "[[pulse]]", "[[parts-radar]]"]
status: active
---

# Ieri sera e oggi · idee su cui ragionare

## Riassunto

Dopo il viaggio e la giornata del 15 ottobre da [[meccanotecnica-umbra]], [[leonardo-pinsone]] scrive a Lorenzo (con Cristian, "Trif", in copia per una lettura) le idee emerse, divise tra cose dette e punti da ragionare. Quattro filoni: Microsoft come canale di vendita, con tre o quattro automazioni funzionanti da mostrare; "sartoriale davanti, fabbrica dietro" (soluzione percepita su misura, blocchi riusabili dietro, anche per [[pulse]]); Meccanotecnica oltre il corso (richiesta di supporto sul make or buy); il [[second-brain]] di produttività personale come pacchetto in vendita, con funzionamento, offerta, prezzi indicativi e vincoli.

[[cristian-schifone]] risponde il 16 ottobre precisando il confronto tra Business Central e InforLN e la sua lettura del make or buy.

## Decisioni e azioni

- Microsoft come canale: BlueAge studia per conto suo l'ecosistema Microsoft intorno a [[business-central-ai]] (Power Automate, Copilot Studio, Power Apps, Power Pages, Dataverse), disegna cosa serve all'azienda e lo porta al partner già costruito; il passo successivo all'Excel delle automazioni di Lorenzo è costruirne tre o quattro funzionanti, con il prima e il dopo. [[parts-radar]] è citato come esempio che si capisce subito.
- L'automazione per [[velo-ce]] va avanti senza aspettare Pulse: qualche giornata, test, materiale per un deck.
- Nel corso [[manini]] ([[corso-ai-manini]]) manca la parte di governance (gruppi e team, permessi, visibilità SharePoint, modelli per utente, crediti di tenant condivisi): Leo la aggiungerebbe.
- Linea sui flussi complessi (di Lorenzo): flussi deterministici per i processi, agenti con skill solo quando il percorso non si può scomporre.
- Second Brain: partire da Claude, tenendo Copilot in parallelo; vendere prima e costruire dopo (approccio di Cristian); prova prima su Leo, poi su Lorenzo e Silvia.
- [ ] Cristian Schifone: abilitare l'ambiente Copilot in cui costruire le automazioni dimostrative
- [ ] Lorenzo: integrare il documento dei requisiti del Second Brain che aveva già scritto con quanto emerso il 15 ottobre
- [ ] Lorenzo: rispondere a Leo sui ragionamenti e sulla domanda di dove BlueAge porta valore ai clienti

## Messaggi

### 2026-10-15 20:34 · [[leonardo-pinsone]]

**Microsoft come canale**: i partner Microsoft incontrati coprono la tecnologia ma faticano sul business, BlueAge può tenere insieme business, dati e AI. Da ragionare: quali automazioni (ricezione DDT e ordini via mail, scadenze e solleciti, entrate merci), dove costruirle, come confezionarle (demo, deck, prezzo). **Fabbrica dietro**: inventario dei blocchi esistenti e mancanti (connettori, dashboard, skill, automazioni, moduli dei corsi) e una regola per decidere quando un pezzo fatto per un cliente diventa riusabile.

**Meccanotecnica oltre il corso** ([[corso-ai-mtu]]): Fausto chiede supporto sul make or buy; oggi i reparti sviluppano piccoli tool su cicli e tempi e metodi; l'azienda è su InforLN e usa Qdrant come base vettoriale. Dall'aula: la qualità è coinvolta, la policy AI esiste sulla carta ma ognuno usa ciò che trova, in plenaria è difficile arrivare ai processi e BlueAge viene percepita un po' come IT. Idee: qualche giornata di assessment make or buy partendo dalla qualità, eventuale RAG ibrido sulla base dell'esperienza di Lorenzo sul chatbot delle non conformità, rotazione dei gruppi per raccogliere casi concreti.

**Second Brain come pacchetto** (nome di lavoro "PASINI"): input da mail, chat di Claude, trascrizioni, WhatsApp, SharePoint e OneDrive; memoria in Markdown collegato (metodo LLM Wiki) su GitHub o SharePoint/OneDrive, con Qdrant come passo successivo per un company brain; ingestion periodica delle sole novità con integrazione e pulizia della memoria; ogni giorno una chat con priorità, prossimi giorni e mail da rispondere, più un riepilogo in Markdown. Componenti: skill di catalogazione personalizzata, due attività programmate (ingestion e feedback), chat. Offerta: 2 ore di raccolta più 2 di installazione (circa 2.000 €), più 2 di messa a punto (circa 3.000 €), con manutenzione ricorrente; profili standard per reparto e un configuratore sul sito. Vincoli: WhatsApp non si collega alle routine di Claude, niente connettori non ufficiali per i clienti, ingestion in cloud, costi AI da stimare.

### 2026-10-16 13:55 · [[cristian-schifone]]

Precisa che Business Central è pensato per le PMI, mentre InforLN è un ERP enterprise: l'equivalente Microsoft è Dynamics 365 F&O. BC non regge bene multisito, vendita su commessa o configurazione di prodotto spinta; per processi più semplici InforLN è sovradimensionato. Sul make or buy legge la tendenza a sviluppare fuori dall'ERP ciò che il gestionale fa male e costa troppo, con il limite della mancata lettura in tempo reale, oggi affrontato con data hub tipo MuleSoft e architetture a microservizi.
