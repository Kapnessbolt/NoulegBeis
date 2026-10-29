#!/usr/bin/env python3
"""Dati della plancia: progetti, attività, inbox, task e digest del vault in file JSON.

Uso:
  python3 .claude/scripts/plancia.py <cartella_output>

Scrive in <cartella_output> progetti.json, attivita.json, log.json, inbox.json,
task.json e digest.json, i dati della pagina Cockpit. I file non vanno nel repo: la
cartella di output sta fuori dal vault. Richiede PyYAML.

La pagina la genera `cockpit.py` da questa cartella (più `calendario.json`, se il task
`cockpit` l'ha scritto): se cambi un campo qui, controlla che `cockpit.py` lo legga ancora.
In progetti.json, per ogni progetto, oltre ai contatori: `percorso` (la scheda, relativo
alla radice del vault), `clienti_slug`, `prossimi_passi` (i punti di `## Prossimi passi`,
senza la fonte in coda), `scadute` (attività aperte con 📅 prima di oggi) e
`prossima_fonte` (la fonte della prossima attività con data).

La variabile d'ambiente VAULT_ROOT, se presente, indica la radice del vault al posto della
cartella che contiene `.claude/` (serve ai test in `.claude/scripts/tests/`).
"""

import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

try:
    import yaml
except ImportError:
    sys.exit("Manca PyYAML: pip install pyyaml")

ROOT = Path(os.environ.get("VAULT_ROOT") or Path(__file__).resolve().parents[2]).resolve()
SKIP_DIRS = {".git", ".github", ".claude", "_templates", ".obsidian", ".trash"}
ROMA = ZoneInfo("Europe/Rome")

LINK = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
TASK = re.compile(r"^- \[( |x|X)\] (.+)$")
DUE = re.compile(r"📅\s*(\d{4}-\d{2}-\d{2})")
SOURCE = re.compile(r"\s*\(((?:\[\[[^\]]+\]\](?:,\s*)?)+)\)\s*$")
LOG_LINE = re.compile(r"^- (\d{4}-\d{2}-\d{2}) ·", re.M)
LOG_ROW = re.compile(r"^- (\d{4}-\d{2}-\d{2}) · (.+?)(?: · (?:\[\[[^\]]+\]\](?:,\s*)?)+)?\s*$")
ULTIMI_PASSI = 5
ESITO = re.compile(r"^\|\s*([a-z][a-z0-9-]*)\s+(\d{2}:\d{2})\s*\|\s*(.*?)\s*\|\s*$")
# Riga di `## Novità ingerite`: `- [[slug]](, [[slug]])* · <stato> · <testo>`; lo stato è il primo
# campo dopo i link (nuova, nuova versione, aggiornata, aggiornate), il testo dopo non conta.
NOVITA = re.compile(r"^- \[\[[^\]]+\]\](?:,\s*\[\[[^\]]+\]\])* · ([^·]+?)\s*(?:·|$)")
# Punto di `## Decisioni` che dice solo che non c'è nulla ("Nessun progetto fermo…",
# "Progetti fermi: nessuno (…)"): non è una decisione e non si conta.
NIENTE = re.compile(r"^(?:nessun|[^:]*:\s*nessun)", re.I)

# Task schedulati attesi ogni giorno (SPEC 7). Se cambiano gli orari in SPEC, cambiali qui:
# altrimenti un task in orario risulta mancante.
ATTESI = [
    ("ingest-sharepoint", "06:50"),
    ("ingest-outlook", "07:05"),
    ("ingest-github", "07:20"),
    ("cockpit", "07:40"),
    ("digest", "07:45"),
    ("ingest-outlook", "13:15"),
    ("cockpit", "13:40"),
]
ATTESI_DOMENICA = [("reconcile", "08:45")]
TOLLERANZA_MIN = 45   # dopo l'ora attesa, prima di dire "mancante"
FINESTRA_MIN = 180    # un'esecuzione oltre l'ora attesa + finestra non conta per quell'orario


def split_note(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    _, fm, body = text.split("---", 2)
    return yaml.safe_load(fm) or {}, body


def h1(body):
    m = re.search(r"^# (.+)$", body, re.M)
    return m.group(1).strip() if m else None


def titles():
    """slug → titolo H1 di ogni nota del vault, per rendere leggibili i wikilink."""
    out = {}
    for p in ROOT.rglob("*.md"):
        if SKIP_DIRS & set(p.relative_to(ROOT).parts):
            continue
        try:
            out[p.stem] = h1(split_note(p)[1]) or p.stem.replace("-", " ")
        except Exception:
            out[p.stem] = p.stem.replace("-", " ")
    return out


def section(body, name):
    m = re.search(rf"^## {re.escape(name)}\s*$(.*?)(?=^## |\Z)", body, re.M | re.S)
    return m.group(1) if m else ""


def slugs(value):
    return [LINK.search(v).group(1) for v in (value or []) if LINK.search(str(v))]


def checkbox(body, sezione, plain):
    """Le checkbox di una sezione: (testo, scadenza, fatta, fonte)."""
    for line in section(body, sezione).splitlines():
        m = TASK.match(line.strip())
        if not m:
            continue
        testo = m.group(2)
        fonte = SOURCE.search(testo)
        testo = SOURCE.sub("", testo)
        due = DUE.search(testo)
        testo = DUE.sub("", testo).strip()
        yield (plain(testo), due.group(1) if due else "", m.group(1).lower() == "x",
               LINK.findall(fonte.group(1))[0] if fonte else "")


def punti(body, sezione, plain):
    """I punti di una sezione (righe `- testo`), senza trattino, senza fonte in coda, vuoti esclusi."""
    out = []
    for line in section(body, sezione).splitlines():
        line = line.strip()
        if not line.startswith("- ") or TASK.match(line):
            continue
        testo = plain(SOURCE.sub("", line[2:])).strip()
        if testo:
            out.append(testo)
    return out


def minuti(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def esiti_del_giorno(giorno, ora):
    """Righe di `## Esito dei task` del digest del giorno, confrontate con i task attesi."""
    path = ROOT / "journal" / f"{giorno}.md"
    eseguiti = []
    if path.exists():
        for line in section(split_note(path)[1], "Esito dei task").splitlines():
            m = ESITO.match(line.strip())
            if m:
                eseguiti.append({"task": m.group(1), "ora": m.group(2), "esito": m.group(3)})
    attesi = list(ATTESI)
    if datetime.fromisoformat(giorno).weekday() == 6:
        attesi += ATTESI_DOMENICA
    attesi.sort(key=lambda t: t[1])
    adesso = minuti(ora)
    usati, righe = set(), []
    for task, atteso in attesi:
        trovato = next((i for i, e in enumerate(eseguiti) if i not in usati and e["task"] == task
                        and minuti(atteso) - 10 <= minuti(e["ora"]) <= minuti(atteso) + FINESTRA_MIN), None)
        if trovato is not None:
            usati.add(trovato)
            e = eseguiti[trovato]
            ok = e["esito"].upper().startswith("OK")
            righe.append({"task": task, "atteso": atteso, "eseguito": e["ora"],
                          "stato": "ok" if ok else "errore", "esito": e["esito"]})
        elif adesso > minuti(atteso) + TOLLERANZA_MIN:
            righe.append({"task": task, "atteso": atteso, "eseguito": "",
                          "stato": "mancante", "esito": "nessuna riga nel digest"})
        else:
            righe.append({"task": task, "atteso": atteso, "eseguito": "",
                          "stato": "atteso", "esito": ""})
    for i, e in enumerate(eseguiti):
        if i not in usati:
            ok = e["esito"].upper().startswith("OK")
            righe.append({"task": e["task"], "atteso": "", "eseguito": e["ora"],
                          "stato": "ok" if ok else "errore", "esito": e["esito"]})
    for n, r in enumerate(righe, 1):
        r["id"] = f"{r['task']}-{r['atteso'] or r['eseguito']}-{n}"
        r["giorno"] = giorno
    return righe


def digest(giorno, ora):
    """Il digest più recente fino a `giorno`: note nuove e aggiornate, decisioni; e l'ora di questa lettura."""
    giornali = sorted(p for p in (ROOT / "journal").glob("????-??-??.md") if p.stem <= giorno)
    if not giornali:
        return []
    path = giornali[-1]
    body = split_note(path)[1]
    stati = [m.group(1) for m in map(NOVITA.match, section(body, "Novità ingerite").splitlines()) if m]
    # Punti di primo livello, con o senza data (il digest scrive anche "Da spuntare: …"); "-" vuoto escluso.
    decisioni = [l for l in section(body, "Decisioni").splitlines()
                 if l.startswith("- ") and l[2:].strip() and not NIENTE.match(l[2:].strip())]
    return [{
        "giorno": path.stem,
        # Una riga per stato: "nuova versione" è un aggiornamento della nota, non una nota nuova.
        "note_nuove": sum(1 for s in stati if s == "nuova"),
        "note_aggiornate": sum(1 for s in stati if s in ("nuova versione", "aggiornata", "aggiornate")),
        "decisioni": len(decisioni),
        "vault_del": giorno,
        "vault_alle": ora,
    }]


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    out_dir = Path(sys.argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)
    names = titles()
    plain = lambda s: LINK.sub(lambda m: names.get(m.group(1), m.group(1)), s)
    adesso = datetime.now(ROMA)
    oggi, ora = adesso.date().isoformat(), adesso.strftime("%H:%M")

    progetti, attivita, passi = [], [], []
    for path in sorted((ROOT / "projects").glob("*/*.md")):
        slug = path.stem
        if slug != path.parent.name:
            continue
        fm, body = split_note(path)
        nome = h1(body) or slug
        ruolo = fm.get("role") or ""
        coinvolto = not ruolo.lower().startswith("non coinvolto")
        righe = list(checkbox(body, "Attività", plain))
        for n, (testo, scadenza, fatta, fonte) in enumerate(righe, 1):
            attivita.append({
                "id": f"{slug}-{n}",
                "progetto": slug,
                "nome_progetto": nome,
                "testo": testo,
                "scadenza": scadenza,
                "fatta": fatta,
                "fonte": fonte,
                "coinvolto": coinvolto,
                "origine": "progetto",
            })
        aperte = sorted((r for r in righe if not r[2]), key=lambda r: r[1] or "9999")
        log = path.with_name(f"{slug}-log.md")
        testo_log = log.read_text(encoding="utf-8") if log.exists() else ""
        date_log = LOG_LINE.findall(testo_log)
        # Il log è dalla riga più recente: le prime righe sono gli ultimi passi.
        righe_log = [m for m in map(LOG_ROW.match, testo_log.splitlines()) if m]
        for n, m in enumerate(sorted(righe_log, key=lambda m: m.group(1), reverse=True)[:ULTIMI_PASSI], 1):
            passi.append({"id": f"{slug}-{n}", "progetto": slug, "data": m.group(1), "testo": plain(m.group(2))})
        clienti = slugs(fm.get("clients"))
        progetti.append({
            "progetto": slug,
            "nome": nome,
            "clienti": ", ".join(names.get(s, s) for s in clienti),
            "ruolo": ruolo,
            "coinvolto": coinvolto,
            "stato": fm.get("status") or "",
            "aggiornato": str(fm.get("updated") or ""),
            "aperte": len(aperte),
            "prossima": aperte[0][1] if aperte and aperte[0][1] else "",
            "prossima_testo": aperte[0][0] if aperte and aperte[0][1] else "",
            "ultimo_log": max(date_log) if date_log else "",
            "percorso": path.relative_to(ROOT).as_posix(),
            "clienti_slug": clienti,
            "prossimi_passi": punti(body, "Prossimi passi", plain),
            "scadute": sum(1 for r in aperte if r[1] and r[1] < oggi),
            "prossima_fonte": aperte[0][3] if aperte and aperte[0][1] else "",
        })

    inbox = []
    for path in sorted((ROOT / "inbox").glob("*.md")):
        fm, body = split_note(path)
        titolo = h1(body) or path.stem
        righe = list(checkbox(body, "Da fare", plain))
        for n, (testo, scadenza, fatta, fonte) in enumerate(righe, 1):
            attivita.append({
                "id": f"inbox-{path.stem}-{n}",
                "progetto": "inbox",
                "nome_progetto": f"Inbox · {titolo}",
                "testo": testo,
                "scadenza": scadenza,
                "fatta": fatta,
                "fonte": fonte,
                "coinvolto": True,
                "origine": "inbox",
            })
        aperte = sorted(r[1] for r in righe if not r[2] and r[1])
        inbox.append({
            "nota": path.stem,
            "titolo": titolo,
            "creata": str(fm.get("created") or ""),
            "aperte": sum(1 for r in righe if not r[2]),
            "prossima": aperte[0] if aperte else "",
        })

    task = esiti_del_giorno(oggi, ora)
    files = (("progetti", progetti), ("attivita", attivita), ("log", passi), ("inbox", inbox),
             ("task", task), ("digest", digest(oggi, ora)))
    for name, rows in files:
        (out_dir / f"{name}.json").write_text(
            json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    dovuti = [t for t in task if t["stato"] != "atteso"]
    print(f"{len(progetti)} progetti, {len(attivita)} attività, {len(inbox)} note in inbox, "
          f"{sum(1 for t in dovuti if t['stato'] == 'ok')} task OK su {len(dovuti)} → {out_dir}")


if __name__ == "__main__":
    main()
