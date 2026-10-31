#!/usr/bin/env python3
"""Dati della plancia: progetti, attività, inbox, task e digest del vault in file JSON.

Uso:
  python3 .claude/scripts/plancia.py <cartella_output>
  python3 .claude/scripts/plancia.py --anomalie [--giorno AAAA-MM-GG] [--ora HH:MM] [--json]

Scrive in <cartella_output> progetti.json, attivita.json, log.json, inbox.json,
task.json e digest.json, i dati della pagina Cockpit. I file non vanno nel repo: la
cartella di output sta fuori dal vault. Richiede PyYAML.

La pagina la genera `cockpit.py` da questa cartella (più `calendario.json`, se il task
`cockpit` l'ha scritto): se cambi un campo qui, controlla che `cockpit.py` lo legga ancora.
In progetti.json, per ogni progetto, oltre ai contatori: `percorso` (la scheda, relativo
alla radice del vault), `clienti_slug`, `prossimi_passi` (i punti di `## Prossimi passi`,
senza la fonte in coda), `scadute` (attività aperte con 📅 prima di oggi) e
`prossima_fonte` (la fonte della prossima attività con data). In task.json ogni riga ha
`ultimo_giro`: per i task di ingestion delle fonti con watermark, `{"<fonte>": <ultimo_giro di
.state/<fonte>.json o null>}` (registro del giro, `stato.py set-giro`), per gli altri `{}`.

Con `--anomalie` (verifica dei giri automatica, audit 2026-10-31 P8 e P11) non scrive file:
stampa le righe markdown per il digest del task `digest` (SPEC 7), con le regole e le soglie di
`anomalie.py` (le stesse degli avvisi di `controlla-vault.py`):
- giri mancanti o in errore del giorno (regola di `esiti_del_giorno` all'ora `--ora`) e del giorno
  prima (alle 23:59, così il digest del mattino vede la giornata intera di ieri);
- watermark fermo di sharepoint, onedrive e outlook; riconciliazione dovuta da più di 1 giorno di
  sharepoint e onedrive; stato illeggibile (uno stato assente si salta);
- voci dello stato senza versione o copia nella nota, come conteggio (l'elenco è nel rapporto di
  `controlla-vault.py`);
- righe `- Da rileggere dopo [[<fonte>]] v<N> del AAAA-MM-GG` nelle hub (SPEC 4.3).
Uscita testo: il blocco sotto il titolo di `## Esito dei task` (una riga `- Anomalia · …` per
anomalia, o `Nessuna anomalia.`) e, se ci sono hub da rileggere, quello di `## Decisioni`
(`- Da rileggere: [[<hub>]] · dopo [[<fonte>]] v<N> del AAAA-MM-GG (<n> giorni)` per le righe
oltre 7 giorni, poi `- Da rileggere (entro 7 giorni): <n> hub` per le hub con righe più recenti).
Con `--json`: `{"giorno", "ora", "esito_task": [{"tipo", "riga", …campi della regola}],
"decisioni": [{"tipo": "hub_da_rileggere", "riga", …}], "conteggi": {…}}`; `tipo` è
`giro_mancante`, `giro_errore`, `stato_illeggibile`, `watermark_fermo`, `riconciliazione_dovuta`
o `voci_orfane`. In `conteggi` le hub sono contate una volta anche con più righe. Senza
`--giorno` vale oggi nel fuso del vault; senza `--ora` l'ora attuale per oggi, 23:59 per un
giorno passato, 00:00 per uno futuro. Uscita 0 anche con anomalie; 2 per argomenti o
configurazione non validi.

Fuso, nomi delle sezioni e task attesi (orari e giorni) vengono da `vault.yaml` (config.py).

La variabile d'ambiente VAULT_ROOT, se presente, indica la radice del vault al posto della
cartella che contiene `.claude/` (serve ai test in `.claude/scripts/tests/`).
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Manca PyYAML: pip install pyyaml")

sys.path.insert(0, str(Path(__file__).resolve().parent))
import anomalie  # noqa: E402
import config  # noqa: E402

ROOT = Path(os.environ.get("VAULT_ROOT") or Path(__file__).resolve().parents[2]).resolve()
SKIP_DIRS = {".git", ".github", ".claude", "_templates", ".obsidian", ".trash"}

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

# I task attesi nel giorno (SPEC 7) sono quelli di `vault.yaml` (`task`) che scrivono la riga
# d'esito nel digest, con i loro orari e giorni.
TOLLERANZA_MIN = 45   # dopo l'ora attesa, prima di dire "mancante"
FINESTRA_MIN = 180    # un'esecuzione oltre l'ora attesa + finestra non conta per quell'orario
# Fonti dello stato che ogni task di ingestion aggiorna (routine in .claude/routines/)
FONTI_DEL_TASK = {"ingest-sharepoint": ("sharepoint", "onedrive"), "ingest-outlook": ("outlook",)}


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
        for line in section(split_note(path)[1], config.sezione("esito_task")).splitlines():
            m = ESITO.match(line.strip())
            if m:
                eseguiti.append({"task": m.group(1), "ora": m.group(2), "esito": m.group(3)})
    attesi = [(task, ora_attesa) for ora_attesa, task in
              config.task_del_giorno(datetime.fromisoformat(giorno).date(), solo_digest=True)]
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


def ultimi_giri():
    """`ultimo_giro` di ogni fonte con watermark (null se non c'è o lo stato non si legge)."""
    out = {}
    for fonte in {f for fonti in FONTI_DEL_TASK.values() for f in fonti}:
        try:
            stato = json.loads((ROOT / ".state" / f"{fonte}.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            stato = {}
        giro = stato.get("ultimo_giro") if isinstance(stato, dict) else None
        out[fonte] = giro if isinstance(giro, dict) else None
    return out


def digest(giorno, ora):
    """Il digest più recente fino a `giorno`: note nuove e aggiornate, decisioni; e l'ora di questa lettura."""
    giornali = sorted(p for p in (ROOT / "journal").glob("????-??-??.md") if p.stem <= giorno)
    if not giornali:
        return []
    path = giornali[-1]
    body = split_note(path)[1]
    stati = [m.group(1) for m in map(NOVITA.match, section(body, config.sezione("novita")).splitlines()) if m]
    # Punti di primo livello, con o senza data (il digest scrive anche "Da spuntare: …"); "-" vuoto escluso.
    decisioni = [l for l in section(body, config.sezione("decisioni")).splitlines()
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


# --- Anomalie per il digest (P8, P11) -----------------------------------------------------

PREFISSO = "- Anomalia · "


def leggi_stato(fonte):
    """(stato, motivo): lo stato della fonte, oppure None e il motivo se non si legge; (None, None)
    se il file non c'è (fonte mai ingerita)."""
    try:
        stato = json.loads((ROOT / ".state" / f"{fonte}.json").read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, None
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
        return None, str(e)
    if not isinstance(stato, dict):
        return None, "non è un oggetto JSON"
    return stato, None


def frontmatter_fonti():
    """{percorso relativo: frontmatter} delle note di `sources/sharepoint` e `sources/onedrive`."""
    out = {}
    for fonte in anomalie.FONTI_DOVUTA:
        for p in sorted((ROOT / "sources" / fonte).rglob("*.md")):
            try:
                fm = split_note(p)[0]
            except (OSError, ValueError, yaml.YAMLError):
                continue
            if isinstance(fm, dict):
                out[p.relative_to(ROOT).as_posix()] = fm
    return out


def _giorni(n):
    return "1 giorno" if n == 1 else f"{n} giorni"


def anomalie_del_giorno(giorno, ora, adesso):
    """Il risultato di `--anomalie` (il dizionario dell'uscita JSON, più `hub_recenti`)."""
    ieri = (datetime.fromisoformat(giorno).date() - timedelta(days=1)).isoformat()
    esito = []
    for r in anomalie.giri_anomali(esiti_del_giorno(ieri, "23:59") + esiti_del_giorno(giorno, ora)):
        if r["stato"] == "mancante":
            riga = (f"giro mancante: {r['task']} atteso alle {r['atteso']} del {r['giorno']}, "
                    "nessuna riga nel digest")
            esito.append({"tipo": "giro_mancante", "riga": PREFISSO + riga, **r})
        else:
            riga = f"giro in errore: {r['task']} {r['eseguito']} del {r['giorno']} · {r['esito']}"
            esito.append({"tipo": "giro_errore", "riga": PREFISSO + riga, **r})
    voci = {}
    for fonte in anomalie.FONTI_WATERMARK:
        stato, motivo = leggi_stato(fonte)
        if motivo:
            esito.append({"tipo": "stato_illeggibile", "fonte": fonte, "motivo": motivo,
                          "riga": f"{PREFISSO}stato di {fonte} illeggibile: {motivo}"})
        if stato is None:
            continue
        fermo = anomalie.watermark_fermo(fonte, stato)
        if fermo:
            riga = (f"watermark fermo: {fonte} al {fermo['watermark']}, ultimo giro del {fermo['fine']} "
                    f"con {fermo['risultati']} risultati fino al {fermo['piu_recente']} ({fermo['causa']})")
            esito.append({"tipo": "watermark_fermo", "riga": PREFISSO + riga, **fermo})
        if fonte not in anomalie.FONTI_DOVUTA:
            continue
        items = stato.get("items")
        voci[fonte] = items if isinstance(items, dict) else {}
        for d in anomalie.riconciliazioni_dovute(fonte, stato, adesso):
            if d["illeggibile"]:
                esito.append({"tipo": "stato_illeggibile", "fonte": fonte, "motivo": d["messaggio"],
                              "riga": f"{PREFISSO}stato di {fonte} illeggibile: {d['messaggio']}"})
            elif d["livello"] in anomalie.LIVELLI_ANOMALI:
                riga = (f"riconciliazione dovuta: {d['libreria']} ({fonte}) dal {d['dal']} "
                        f"({_giorni(d['giorni'])}) · {d['comando']}")
                esito.append({"tipo": "riconciliazione_dovuta", "riga": PREFISSO + riga, **d})
    orfane = anomalie.voci_orfane(frontmatter_fonti(), voci) if voci else []
    if orfane:
        note, quante = len(orfane), sum(o["orfane"] for o in orfane)
        riga = (f"voci orfane: {note} note con {quante} voci dello stato senza versione o copia "
                "(controlla-vault.py)")
        esito.append({"tipo": "voci_orfane", "riga": PREFISSO + riga, "note": note, "voci": quante})
    hub = anomalie.hub_da_rileggere(ROOT, giorno)
    decisioni = [{"tipo": "hub_da_rileggere",
                  "riga": f"- Da rileggere: [[{h['hub']}]] · dopo [[{h['fonte']}]] {h['versione']} "
                          f"del {h['data']} ({_giorni(h['giorni'])})",
                  **{k: h[k] for k in ("hub", "nota", "fonte", "versione", "data", "giorni")}}
                 for h in hub if h["scaduta"]]

    def quanti(tipo):
        return sum(1 for e in esito if e["tipo"] == tipo)

    return {
        "giorno": giorno,
        "ora": ora,
        "esito_task": esito,
        "decisioni": decisioni,
        "hub_recenti": len({h["hub"] for h in hub if not h["scaduta"]}),
        "conteggi": {
            "giri_mancanti": quanti("giro_mancante"),
            "giri_in_errore": quanti("giro_errore"),
            "stati_illeggibili": quanti("stato_illeggibile"),
            "watermark_fermi": quanti("watermark_fermo"),
            "riconciliazioni_dovute": quanti("riconciliazione_dovuta"),
            "note_con_voci_orfane": len(orfane),
            "voci_orfane": sum(o["orfane"] for o in orfane),
            "hub_da_rileggere": len({h["hub"] for h in hub}),
            "hub_da_rileggere_scadute": len({h["hub"] for h in hub if h["scaduta"]}),
        },
    }


def testo_anomalie(r):
    """Le righe markdown dell'uscita testo di `--anomalie`."""
    righe = [f"## {config.sezione('esito_task')}", ""]
    righe += [e["riga"] for e in r["esito_task"]] or ["Nessuna anomalia."]
    decisioni = [d["riga"] for d in r["decisioni"]]
    if r["hub_recenti"]:
        decisioni.append(f"- Da rileggere (entro {anomalie.HUB_DA_RILEGGERE_GIORNI} giorni): "
                         f"{r['hub_recenti']} hub")
    if decisioni:
        righe += ["", f"## {config.sezione('decisioni')}", ""] + decisioni
    return "\n".join(righe)


def main_anomalie(argv):
    ap = argparse.ArgumentParser(prog="plancia.py",
                                 usage="%(prog)s --anomalie [--giorno AAAA-MM-GG] [--ora HH:MM] [--json]",
                                 description="Anomalie dei giri e hub da rileggere, per il digest (P8, P11).")
    ap.add_argument("--anomalie", action="store_true", required=True)
    ap.add_argument("--giorno", help="AAAA-MM-GG (predefinito: oggi nel fuso del vault)")
    ap.add_argument("--ora", help="HH:MM (predefinito: ora attuale per oggi, 23:59 per un giorno passato)")
    ap.add_argument("--json", action="store_true", help="uscita JSON")
    a = ap.parse_args(argv)
    try:
        config.carica()
    except config.ConfigErrata as e:
        print("Configurazione non valida:\n" + "\n".join(f"- {m}" for m in e.errori), file=sys.stderr)
        return 2
    ora_attuale = config.adesso()
    try:
        giorno = datetime.strptime(a.giorno, "%Y-%m-%d").date() if a.giorno else ora_attuale.date()
    except ValueError:
        ap.error(f"--giorno {a.giorno!r}: serve una data AAAA-MM-GG")
    if a.ora is not None:
        try:
            if not re.fullmatch(r"\d{2}:\d{2}", a.ora):
                raise ValueError
            ora = datetime.strptime(a.ora, "%H:%M").time()
        except ValueError:
            ap.error(f"--ora {a.ora!r}: serve un'ora HH:MM")
    elif giorno == ora_attuale.date():
        ora = ora_attuale.time().replace(second=0, microsecond=0)
    else:
        ora = datetime.strptime("23:59" if giorno < ora_attuale.date() else "00:00", "%H:%M").time()
    adesso = datetime.combine(giorno, ora, tzinfo=config.fuso())
    r = anomalie_del_giorno(giorno.isoformat(), ora.strftime("%H:%M"), adesso)
    if a.json:
        print(json.dumps({k: v for k, v in r.items() if k != "hub_recenti"}, ensure_ascii=False, indent=1))
    else:
        print(testo_anomalie(r))
    return 0


def main():
    if "--anomalie" in sys.argv[1:]:
        sys.exit(main_anomalie(sys.argv[1:]))
    try:
        config.carica()
    except config.ConfigErrata as e:
        sys.exit("Configurazione non valida:\n" + "\n".join(f"- {m}" for m in e.errori))
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    out_dir = Path(sys.argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)
    names = titles()
    plain = lambda s: LINK.sub(lambda m: names.get(m.group(1), m.group(1)), s)
    adesso = config.adesso()
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
        righe = list(checkbox(body, config.sezione("attivita"), plain))
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
            "prossimi_passi": punti(body, config.sezione("prossimi_passi"), plain),
            "scadute": sum(1 for r in aperte if r[1] and r[1] < oggi),
            "prossima_fonte": aperte[0][3] if aperte and aperte[0][1] else "",
        })

    inbox = []
    for path in sorted((ROOT / "inbox").glob("*.md")):
        fm, body = split_note(path)
        titolo = h1(body) or path.stem
        righe = list(checkbox(body, config.sezione("da_fare"), plain))
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
    giri = ultimi_giri()
    for t in task:
        t["ultimo_giro"] = {f: giri[f] for f in FONTI_DEL_TASK.get(t["task"], ())}
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
