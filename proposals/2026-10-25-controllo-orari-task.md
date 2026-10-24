---
type: proposal
date: 2026-10-25
kind: hook
status: rifiutata
---

# Controllo che gli orari dei task in plancia.py siano quelli di SPEC 7

## Motivazione

Gli orari dei task schedulati sono scritti in tre posti: SPEC §7, la tabella `ATTESI` di `.claude/scripts/plancia.py` e la mod `cockpit`, che sta fuori dal repo. Si sono già disallineati una volta: i task creati il 22/10 avevano orari diversi dalla SPEC, e ci è voluta una PR per allinearla. Oggi l'unica difesa è un commento in `plancia.py`. Se cambia un orario e la tabella resta indietro, il Cockpit segna "mancante" un task che gira regolarmente: un falso allarme proprio sul controllo che si fa più spesso. Con il controllo, una PR sulla SPEC che cambia un orario non passa il pre-commit né il workflow finché `plancia.py` non è allineato, e il messaggio ricorda la mod.

## Evidenze

- [[2026-10-22-watermark-e-task-schedulati]]: "Orari diversi da SPEC §7, da allineare con la PR sulla SPEC".
- [[2026-10-23-verifica-primo-giro-task]]: PR #10 per portare in SPEC §7 gli orari reali dei task.
- [[2026-10-24-restyling-cockpit-implementazione]]: "gli orari attesi di SPEC 7 stanno in una tabella dentro `plancia.py` e dentro la mod… Se cambiano gli orari in SPEC vanno cambiati in tutti e due"; resta aperta una PR su SPEC §7 per la riga `cockpit`.

## Testo proposto

`.claude/scripts/controlla-vault.py`, import in testa: `import importlib.util` e `from collections import Counter, defaultdict` al posto di `from collections import defaultdict`. Nuove funzioni prima di `def main():`:

```python
def orari_spec():
    """Task con orario fisso dalla tabella di SPEC 7: (giornalieri, domenicali) come Counter."""
    testo = (ROOT / "SPEC.md").read_text(encoding="utf-8")
    sezione = testo.split("\n## 7.", 1)[1].split("\n## ", 1)[0]
    giorno, domenica = Counter(), Counter()
    for riga in sezione.splitlines():
        m = re.match(r"^\|\s*`([a-z-]+)`\s*\|([^|]*)\|", riga)
        if not m or "da creare" in m.group(2):
            continue
        quando = m.group(2).strip().lower()
        meta = giorno if quando.startswith("ogni giorno") else domenica if quando.startswith("domenica") else None
        for ora in re.findall(r"\b\d{2}:\d{2}\b", quando) if meta is not None else ():
            meta[(m.group(1), ora)] += 1
    return giorno, domenica


def controlla_orari():
    """Gli orari attesi di plancia.py (ATTESI, ATTESI_DOMENICA) sono quelli di SPEC 7."""
    script = ".claude/scripts/plancia.py"
    spec = importlib.util.spec_from_file_location("plancia", ROOT / script)
    plancia = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True   # niente __pycache__ in .claude/scripts/
    spec.loader.exec_module(plancia)
    for atteso, trovato, quando in zip(orari_spec(), (Counter(plancia.ATTESI), Counter(plancia.ATTESI_DOMENICA)),
                                       ("ogni giorno", "la domenica")):
        for task, ora in sorted((atteso - trovato) + (trovato - atteso)):
            dove = "manca in" if (task, ora) in atteso - trovato else "non è in SPEC 7, ma è in"
            err(["SPEC.md", script], f"orari dei task: `{task}` {ora} {quando} {dove} `{script}` "
                "(aggiorna anche la tabella della mod cockpit)")
```

Stesso file, in `main()`, subito prima di `# Solo gli errori che dipendono dalle modifiche in corso (hook di commit)`:

```python
    # 8. Configurazione: orari dei task tra SPEC 7 e plancia.py
    controlla_orari()
```

Provato sul vault del 25/10: nessun errore; con l'orario `13:40` del cockpit cambiato in `13:50` nella SPEC dà due errori, uno per orario.
