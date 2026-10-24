---
type: proposal
date: 2026-10-25
kind: hook
status: accettata
---

# Controllo che i nomi del connettore Microsoft 365 coincidano tra ingestor e permessi

## Motivazione

Il nome del server Microsoft 365 cambia con l'ambiente: `Microsoft_365` nelle sessioni cloud, `Microsoft-365` nei task, l'id del connettore in locale. In quattro diari un nome mancante ha rotto qualcosa ed è stato aggiunto a mano. SPEC §2 chiede che `tools` dell'ingestor e `permissions.allow` di `.claude/settings.json` li elenchino tutti, ma nessun controllo lo verifica, e oggi infatti non coincidono: `Microsoft-365` sta nei `tools` e manca nei permessi. Un nome dimenticato si scopre solo quando l'ingestor parte senza connettore o la modalità Auto blocca una lettura. Con il controllo nel controllo del vault l'errore esce al commit, dal workflow e da `/controlla`.

## Evidenze

- [[2026-10-22-step-2-ingestor]]: aperto "Verificare che il nome del server MCP (`Microsoft_365`) sia lo stesso nei task schedulati: se cambia, l'agente resta senza tool M365".
- [[2026-10-22-watermark-e-task-schedulati]]: in cloud il connettore ha un nome tecnico diverso da quello dichiarato dall'ingestor; i task eseguono l'ingestor nella sessione per aggirarlo.
- [[2026-10-23-verifica-primo-giro-task]]: `tools` riscritto con i nomi esatti di `Microsoft_365` e `Microsoft-365`; un nome `mcp__<uuid>__` resta scoperto.
- [[2026-10-24-cockpit-in-locale]]: in locale il nome è `6501b655-…`; la modalità Auto bloccava il calendario e l'ingestor sarebbe partito senza connettore; aggiunto a mano in `settings.json` e in `tools`.
- Stato del 25/10 (`.claude/settings.json`): mancano i 4 permessi `mcp__Microsoft-365__*`, presenti in `tools` dell'ingestor. Con il controllo qui sotto lo script dà oggi questo errore.

## Testo proposto

`.claude/scripts/controlla-vault.py`, nuove funzioni prima di `def main():`:

```python
# SPEC 2: strumenti in lettura del connettore Microsoft 365, da elencare per ogni nome di server
M365_LETTURA = {"sharepoint_search", "sharepoint_folder_search", "outlook_email_search", "read_resource"}


def server_m365(nomi):
    """{server: strumenti in lettura} dai nomi `mcp__<server>__<strumento>`."""
    out = defaultdict(set)
    for nome in nomi:
        parti = nome.strip().split("__")
        if len(parti) == 3 and parti[0] == "mcp" and parti[2] in M365_LETTURA:
            out[parti[1]].add(parti[2])
    return out


def controlla_connettore():
    """I nomi del server M365 nei `tools` dell'ingestor e nei permessi di settings.json coincidono."""
    agente, impost = ".claude/agents/ingestor.md", ".claude/settings.json"
    fm, _ = split_frontmatter((ROOT / agente).read_text(encoding="utf-8"))
    tools = server_m365(str((yaml.safe_load(fm) or {}).get("tools", "")).split(","))
    allow = json.loads((ROOT / impost).read_text(encoding="utf-8")).get("permissions", {}).get("allow", [])
    permessi = server_m365(allow)
    for nomi, dove, altri, altrove in ((tools, agente, permessi, impost), (permessi, impost, tools, agente)):
        for server, strumenti in nomi.items():
            mancano = sorted(M365_LETTURA - strumenti)
            if mancano:
                err(dove, f"server M365 `{server}`: mancano {', '.join(mancano)}")
            if server not in altri:
                err(altrove, f"server M365 `{server}` presente in `{dove}` ma non qui (SPEC 2)")
```

Stesso file, in `main()`, subito prima di `# Solo gli errori che dipendono dalle modifiche in corso (hook di commit)`:

```python
    # 7. Configurazione: nomi del connettore Microsoft 365 (SPEC 2)
    controlla_connettore()
```

`.claude/settings.json`, in `permissions.allow` dopo i permessi `mcp__Microsoft_365__*`. Va applicato insieme al controllo, altrimenti il workflow fallisce al primo push:

```json
      "mcp__Microsoft-365__sharepoint_search",
      "mcp__Microsoft-365__sharepoint_folder_search",
      "mcp__Microsoft-365__outlook_email_search",
      "mcp__Microsoft-365__read_resource",
```
