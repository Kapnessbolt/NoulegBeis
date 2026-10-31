---
type: source-doc
source: sharepoint
family: velo-ce-richieste-accessi-e-licensing
current:
  item_id: 01EFCYUZ4BI65UZAKTBFHKM3BFK2DVQYBT
  uri: file:///b!qVc_gEAkd0SrxYHP_MxTuzWhDnaUNaZKpoIpo9e_gKV-y7RZZQefRaYsG3tmobah/01EFCYUZ4BI65UZAKTBFHKM3BFK2DVQYBT
  web_url: https://blueagesrl.sharepoint.com/sites/internal/Delivery/Customers/01 - Velo-CE/Progetto Dynamics/04 Partner e ambienti/Governance e accessi/Velo-CE - Richieste accessi e licensing - v002.xlsx
  name: Velo-CE - Richieste accessi e licensing - v002.xlsx
  last_modified: 2026-09-27T18:32:52Z
versions:
  - { name: Velo-CE - Richieste accessi e licensing - v002.xlsx, item_id: 01EFCYUZ4BI65UZAKTBFHKM3BFK2DVQYBT, last_modified: 2026-09-27T18:32:52Z }
  - { name: Velo-CE - Richieste accessi e licensing - v002.xlsx, item_id: 01EFCYUZ5PEKY5GPQEOVGKAH32YUIYUG6W, last_modified: 2026-09-27T18:32:52Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T13:31:42Z
projects: ["[[velo-ce-progetto-dynamics]]"]
clients: ["[[velo-ce]]"]
topics: ["[[business-central-ai]]"]
tags: [velo-ce, business-central, accessi, licenze, power-bi, premium]
---

# Velo-CE · Richieste di accesso e licensing

## Riassunto

Elenco preparato da BlueAge il 21/09/2026 e aggiornato il 27/09 delle concessioni da chiedere a Velo-CE: cosa abilita ciascuna e come la attiva il titolare. Distingue due strati: i ruoli Microsoft Entra governano i portali di amministrazione, i set di autorizzazioni governano l'applicativo Business Central. Copre cinque blocchi: tenant Business Central, tenant Microsoft 365 della posta (gestito da un fornitore esterno), Power BI, sistemi esterni (Veloce-CRM, portali B2B, Fatture in Cloud) e attività che restano a Velo-CE. Al 27/09 non ci sono richieste oltre agli accessi già attivi. Un secondo foglio elenca 13 punti da confermare in riunione.

## Punti chiave

- **Attivi dal 21/09**: utenza generica BlueAge senza licenza sul tenant BC, con ruolo Entra di amministratore Business Central (che consente anche copia, ripristino ed eliminazione degli ambienti) e Lettore globale. Se l'utenza la usano più persone, le azioni non sono attribuibili.
- **Non richiesti (27/09)**: set di autorizzazioni dentro BC (SUPER non si chiede); utenza e Lettore globale sul tenant della posta; ruolo di lettura su Azure; licenze Power BI Pro per Leonardo e Cristian e accesso ai file .pbix; accessi in lettura a Veloce-CRM, portali B2B Veloe e Van Nicholas e Fatture in Cloud (tramite Stefano, We Make Code o il marketing Van Nicholas).
- **Licenza Premium di prova**: la chiede Stefano a EOS, fuori dalla call; due strade (prova di 30 giorni dal rivenditore EOS Online o licenza mensile comprata da Microsoft); il passaggio di esperienza si fa solo in sandbox.
- **Restano a Velo-CE**: acquisto e assegnazione delle licenze (anche le 2 Team Members acquistate e mai assegnate), cambio di esperienza a Premium (solo un utente con licenza Premium), aggiornamento utenti e registro modifiche (utente licenziato con SUPER), lettura della delega GDAP del partner, installazione di app da AppSource in produzione.
- **Utenza condivisa dell'amministrazione** (licenza nominale di Claudia Crippa): da sostituire con un'utenza nominale, perché ogni modifica risulta a nome di Claudia.
- **Punti risolti**: tre licenze BC assegnate a Stefano, Claudia e Anton, nessuna utenza tecnica; account di fatturazione MCA con sottoscrizioni mensili. **Aperti**: dominio del tenant della posta, esistenza di una sottoscrizione Azure, chi ha SUPER, uso delle sandbox, chi detiene i .pbix, contratto scritto con So Smart, chi fattura le licenze (EOS o Microsoft), licenza Power BI di Anton su un account personale, uso degli account amministrativi di So Smart.

## Numeri

- 4 ambienti: 1 Production + 3 sandbox (Educational, Educational2906, TestTemp1509); nessuno slot libero con la quota standard.
- 3 licenze Business Central; 2 licenze Team Members acquistate e mai assegnate.
- 13 punti da confermare in riunione.

## Decisioni e azioni

- Decisione (27/09): nessuna richiesta di accesso oltre a quelli già attivi; SUPER non si chiede.
- [ ] Stefano chiede a EOS la licenza Premium di prova
- [ ] Sostituire l'utenza condivisa dell'amministrazione con un'utenza nominale
- [ ] Confermare in riunione i punti aperti del foglio «Da confermare»

## Versioni

- Velo-CE - Richieste accessi e licensing - v002.xlsx · 2026-09-27 · prima versione ingerita (contenuto del 21/09, aggiornato il 27/09)
