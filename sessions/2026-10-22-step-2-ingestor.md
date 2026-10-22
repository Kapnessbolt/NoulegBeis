---
type: session
date: 2026-10-22
surface: cloud
topics: ["[[blueage]]", "[[pulse]]"]
outcome: Step 2 completato: agente ingestor, comandi /ingest e /ingest-file, prima nota ingerita (Company Profile v24)
---

# Step 2 · agente ingestor e comandi di ingestion

## Obiettivo

Implementare lo step 2 della SPEC: agente `ingestor` e comandi `/ingest`, `/ingest-file`, con criterio di accettazione `/ingest-file` su `BlueAge_CompanyProfile_v24.pdf`.

## Decisioni

- L'agente ha due modalità: `schedulata` rispetta alla lettera i permessi di scrittura della SPEC 3; `interattiva` può anche creare note nuove in `people/`, `clients/`, `topics/` e `inbox/`. Risolve il conflitto tra "l'ingestor scrive solo in sources/journal/.state" e "crea la nota di destinazione dal template".
- In modalità schedulata i collegamenti mancanti (persone, clienti, temi, progetti) finiscono nel digest come proposte.
- Campo `topics: []` aggiunto a `source-doc` e `source-mail` (SPEC 4.2, template, agente): i collegamenti ai temi stanno nel frontmatter.
- I documenti fuori perimetro ingeriti con `/ingest-file` vanno in `sources/sharepoint/_<sito>/...`, con tag `fuori-perimetro`, e non entrano in `.state/ingest.json` (la riconciliazione li segnerebbe come rimossi).
- L'agente usa solo i tool M365 in lettura (lista esplicita nel frontmatter); `settings.json` li pre-autorizza insieme ai comandi git.
- `sharepoint_search` con `query: "*"` restituisce anche altri siti e il resto di OneDrive: il filtro sul `webUrl` è indispensabile.

## File toccati

- `.claude/agents/ingestor.md`
- `.claude/commands/ingest.md`, `.claude/commands/ingest-file.md`
- `.claude/settings.json`
- `sources/sharepoint/salesmarketing/deck/blueage-companyprofile.md`
- `topics/pulse.md`, `topics/blueage.md`
- `.state/ingest.json` (item del Company Profile, watermark invariati)
- `README.md`
- `SPEC.md` (1.2), `CLAUDE.md`, `_templates/source-doc.md`, `_templates/source-mail.md`

## Aperti

- [x] PR dedicata sulla SPEC: campo `topics: []` in `source-doc` e `source-mail`; eccezione "creazione note nuove in modalità interattiva" nella sezione 3 (SPEC 1.2, PR aperta in questa sessione)
- [ ] Sul sito `sites/partner` c'è `BlueAge_CompanyProfile.pdf` modificato il 2026-10-19, con un testo diverso dalla v24: verificare se è una versione più recente da portare in `SalesMarketing/Deck`
- [ ] Verificare che il nome del server MCP (`Microsoft_365`) sia lo stesso nei task schedulati: se cambia, l'agente resta senza tool M365
