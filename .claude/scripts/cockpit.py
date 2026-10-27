#!/usr/bin/env python3
"""Pagina Cockpit: una pagina HTML statica e autosufficiente generata dai dati del vault.

Uso:
  python3 .claude/scripts/cockpit.py <cartella_dati> <file_html> [--oggi AAAA-MM-GG]
      [--ora HH:MM] [--repo-url URL] [--titolo TITOLO]

<cartella_dati> è la cartella scritta da `plancia.py` (progetti.json, attivita.json, log.json,
inbox.json, task.json, digest.json: obbligatori) più, se c'è, calendario.json, scritto dal
task `cockpit` con il connettore Microsoft 365. La pagina riempie lo scheletro
`.claude/templates/cockpit.html`: testata con tre contatori (scadute, oggi, settimana),
blocco Oggi, blocco Settimana (i 7 giorni dopo oggi), schede dei progetti attivi, e in fondo
inbox, ultimo digest, task del giorno e attività senza data. Sola lettura, senza risorse
esterne: funziona anche salvata come file.

Schema di calendario.json (una lista di eventi; campi mancanti tollerati):
  [{"inizio": "2026-10-27T09:00:00+01:00", "fine": "2026-10-27T10:00:00+01:00",
    "tutto_il_giorno": false, "titolo": "Call Manini", "luogo": "Teams", "online": true,
    "organizzatore": "Leonardo Pinsone", "risposta": "accettato"}]
  - `inizio` e `fine`: istanti ISO 8601 con offset (senza offset valgono in Europe/Rome);
    con `tutto_il_giorno: true` sono date AAAA-MM-GG e `fine` è esclusa, come in Outlook (un
    evento del solo 27 ha inizio 2026-10-27 e fine 2026-10-28; senza `fine` dura un giorno).
  - `risposta`: accettato, provvisorio, non risposto, organizzatore o rifiutato. Gli eventi
    rifiutati non compaiono; quelli senza `inizio` leggibile si scartano con un avviso.
Se calendario.json manca, il blocco dice "Calendario non disponibile in questo giro".

Semafori dei progetti: rosso "scaduto" se ha attività aperte con 📅 prima di oggi; giallo
"fermo da N giorni" se l'ultima riga del log (o, senza log, `updated`) ha più di 14 giorni;
verde "in ordine" altrimenti. Ordine: prima i progetti seguiti, poi quelli che si osservano
(`coinvolto: false`); in ciascun gruppo scaduti (più scadute prima), fermi (fermi da più
tempo prima), poi gli altri per `aggiornato` decrescente.

I link alle note puntano a `<repo-url>/blob/main/<percorso>` (GitHub rende il markdown anche
sul telefono). Senza `--repo-url` la base si ricava da `git remote get-url origin` nella
radice del vault; `--repo-url ""` toglie i link. Stampa su stdout la riga di riepilogo per il
digest. Esce con 1 se un JSON obbligatorio manca o non si legge, con 2 se gli argomenti non
sono validi. Solo libreria standard.

La variabile d'ambiente VAULT_ROOT, se presente, indica la radice del vault al posto della
cartella che contiene `.claude/` (serve ai test in `.claude/scripts/tests/`).
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime, timedelta
from html import escape
from pathlib import Path
from urllib.parse import quote
from zoneinfo import ZoneInfo

ROOT = Path(os.environ.get("VAULT_ROOT") or Path(__file__).resolve().parents[2]).resolve()
TEMPLATE = Path(__file__).resolve().parents[1] / "templates" / "cockpit.html"
SKIP_DIRS = {".git", ".github", ".claude", "_templates", ".obsidian", ".trash"}
ROMA = ZoneInfo("Europe/Rome")

OBBLIGATORI = ("progetti", "attivita", "log", "inbox", "task", "digest")
GIORNI_SETTIMANA = 7
FERMO_GIORNI = 14
ULTIMI_LOG = 3
RIFIUTATO = {"rifiutato", "declined"}
PROVVISORIO = {"provvisorio", "tentative", "non risposto", "notresponded", "none"}

GIORNI = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]
GIORNI_BREVI = ["lun", "mar", "mer", "gio", "ven", "sab", "dom"]
MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto",
        "settembre", "ottobre", "novembre", "dicembre"]
MESI_BREVI = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]

SEGNAPOSTO = re.compile(r"\{\{([a-z_]+)\}\}")
H1 = re.compile(r"^# (.+)$", re.M)


class DatiMancanti(Exception):
    pass


# ---------------------------------------------------------------- date in italiano

def data_lunga(g):
    return f"{GIORNI[g.weekday()]} {g.day} {MESI[g.month - 1]} {g.year}"


def data_media(g):
    return f"{GIORNI[g.weekday()]} {g.day} {MESI[g.month - 1]}"


def data_breve(g):
    return f"{g.day} {MESI_BREVI[g.month - 1]}"


def giorno_breve(g):
    return f"{GIORNI_BREVI[g.weekday()]} {g.day} {MESI_BREVI[g.month - 1]}"


def giorno(valore):
    try:
        return date.fromisoformat(str(valore)[:10])
    except (TypeError, ValueError):
        return None


CODICE = re.compile(r"`([^`]+)`")
GRASSETTO = re.compile(r"\*\*(.+?)\*\*")


def testo(s):
    """Testo di una nota in HTML: tutto escapato, poi `codice` e **grassetto** del markdown."""
    s = escape(str(s or ""))
    s = CODICE.sub(lambda m: f"<code>{m.group(1)}</code>", s)
    return GRASSETTO.sub(lambda m: f"<strong>{m.group(1)}</strong>", s)


def plurale(n, uno, molti):
    return f"{n} {uno if n == 1 else molti}"


# ---------------------------------------------------------------- lettura dei dati

def leggi_json(cartella, nome):
    path = cartella / f"{nome}.json"
    if not path.exists():
        raise DatiMancanti(f"manca {path}")
    try:
        dati = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
        raise DatiMancanti(f"{path} non è leggibile: {e}")
    if not isinstance(dati, list):
        raise DatiMancanti(f"{path} non contiene una lista")
    return [r for r in dati if isinstance(r, dict)]


def istante(valore):
    """Un istante ISO 8601 in Europe/Rome; senza offset vale già in Europe/Rome."""
    try:
        t = datetime.fromisoformat(str(valore).strip().replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    return t.replace(tzinfo=ROMA) if t.tzinfo is None else t.astimezone(ROMA)


def leggi_calendario(cartella, primo, ultimo):
    """Eventi tra `primo` e `ultimo` (date incluse), per giorno. None se il file manca.

    Ogni evento: giorno, inizio e fine (HH:MM o ""), tutto_il_giorno, titolo, luogo, online,
    organizzatore, provvisorio, chiave (per contare una volta gli eventi di più giorni).
    """
    path = cartella / "calendario.json"
    if not path.exists():
        return None, ""
    try:
        dati = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
        return None, f"calendario.json non leggibile: {e}"
    if isinstance(dati, dict):
        dati = dati.get("eventi", [])
    if not isinstance(dati, list):
        return None, "calendario.json non contiene una lista di eventi"
    eventi, scartati = [], 0
    for n, e in enumerate(dati):
        if not isinstance(e, dict):
            scartati += 1
            continue
        if str(e.get("risposta") or "").strip().lower() in RIFIUTATO:
            continue
        base = {
            "titolo": str(e.get("titolo") or "").strip() or "(senza titolo)",
            "luogo": str(e.get("luogo") or "").strip(),
            "online": bool(e.get("online")),
            "organizzatore": str(e.get("organizzatore") or "").strip(),
            "provvisorio": str(e.get("risposta") or "").strip().lower() in PROVVISORIO,
            "chiave": n,
        }
        if e.get("tutto_il_giorno"):
            da = giorno(e.get("inizio"))
            if not da:
                scartati += 1
                continue
            a = giorno(e.get("fine"))
            a = a - timedelta(days=1) if a and a > da else da
            g = max(da, primo)
            while g <= min(a, ultimo):
                eventi.append({**base, "giorno": g, "inizio": "", "fine": "", "tutto_il_giorno": True})
                g += timedelta(days=1)
            continue
        inizio = istante(e.get("inizio"))
        if not inizio:
            scartati += 1
            continue
        fine = istante(e.get("fine")) if e.get("fine") else None
        g = inizio.date()
        if primo <= g <= ultimo:
            eventi.append({**base, "giorno": g, "inizio": inizio.strftime("%H:%M"),
                           "fine": fine.strftime("%H:%M") if fine and fine.date() == g else "",
                           "fine_altro_giorno": fine.date() if fine and fine.date() != g else None,
                           "tutto_il_giorno": False})
    eventi.sort(key=lambda e: (e["giorno"], not e["tutto_il_giorno"], e["inizio"], e["titolo"].lower()))
    avviso = f"{plurale(scartati, 'evento scartato', 'eventi scartati')} da calendario.json (inizio illeggibile)" if scartati else ""
    return eventi, avviso


def indice_note():
    """slug → (percorso relativo, titolo H1) di ogni nota del vault, per i link alle fonti."""
    out = {}
    for p in ROOT.rglob("*.md"):
        rel = p.relative_to(ROOT)
        if SKIP_DIRS & set(rel.parts):
            continue
        try:
            contenuto = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        corpo = contenuto.split("---", 2)[2] if contenuto.startswith("---") and contenuto.count("---") >= 2 else contenuto
        m = H1.search(corpo)
        out[p.stem] = (rel.as_posix(), m.group(1).strip() if m else p.stem.replace("-", " "))
    return out


def repo_da_git():
    """`https://github.com/<owner>/<repo>` dal remote `origin` del vault, o "" se non si ricava."""
    try:
        url = subprocess.run(["git", "-C", str(ROOT), "remote", "get-url", "origin"],
                             capture_output=True, text=True, timeout=10).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""
    return repo_web(url)


def repo_web(url):
    url = (url or "").strip()
    if not url:
        return ""
    m = re.match(r"^[\w.-]+@[\w.-]+:(.+)$", url)          # git@github.com:owner/repo.git
    percorso = m.group(1) if m else re.sub(r"^[a-z+]+://[^/]+/?", "", url)
    parti = [p for p in re.sub(r"\.git$", "", percorso.strip("/")).split("/") if p]
    if len(parti) < 2:
        return ""
    return f"https://github.com/{parti[-2]}/{parti[-1]}"


# ---------------------------------------------------------------- costruzione della pagina

class Pagina:
    def __init__(self, dati, eventi, avviso_calendario, oggi, ora, repo, titolo, indice):
        self.oggi, self.ora, self.repo, self.titolo, self.indice = oggi, ora, repo.rstrip("/"), titolo, indice
        self.ultimo = oggi + timedelta(days=GIORNI_SETTIMANA)
        self.eventi = eventi
        self.avviso_calendario = avviso_calendario
        self.progetti = dati["progetti"]
        self.per_slug = {p.get("progetto"): p for p in self.progetti}
        self.log = dati["log"]
        self.inbox = dati["inbox"]
        self.task = dati["task"]
        self.digest = dati["digest"]
        self.aperte = []
        for a in dati["attivita"]:
            if a.get("fatta"):
                continue
            a = dict(a)
            a["giorno"] = giorno(a.get("scadenza")) if a.get("scadenza") else None
            self.aperte.append(a)
        datate = sorted((a for a in self.aperte if a["giorno"]), key=lambda a: (a["giorno"], a.get("nome_progetto") or ""))
        self.scadute = [a for a in datate if a["giorno"] < oggi]
        self.di_oggi = [a for a in datate if a["giorno"] == oggi]
        self.della_settimana = [a for a in datate if oggi < a["giorno"] <= self.ultimo]
        if eventi is None:
            self.eventi_oggi, self.eventi_settimana = [], []
        else:
            self.eventi_oggi = [e for e in eventi if e["giorno"] == oggi]
            self.eventi_settimana = [e for e in eventi if oggi < e["giorno"] <= self.ultimo]

    # -- collegamenti

    def url(self, percorso):
        return f"{self.repo}/blob/main/{quote(percorso)}" if self.repo and percorso else ""

    def link(self, percorso, etichetta, classe=""):
        url = self.url(percorso)
        cls = f' class="{classe}"' if classe else ""
        if not url:
            return f"<span{cls}>{escape(etichetta)}</span>"
        return f'<a{cls} href="{escape(url)}" target="_blank" rel="noopener">{escape(etichetta)}</a>'

    def link_nota(self, slug):
        """Titolo della nota con il link su GitHub, e lo slug; solo lo slug se la nota non si trova."""
        if not slug:
            return ""
        percorso, titolo = self.indice.get(slug, ("", ""))
        if not percorso:
            return f'<span class="slug">[[{escape(slug)}]]</span>'
        return f'{self.link(percorso, titolo)} <span class="slug">[[{escape(slug)}]]</span>'

    def percorso_progetto(self, a):
        if a.get("origine") == "inbox":
            m = re.match(r"^inbox-(.+)-\d+$", str(a.get("id") or ""))
            return self.indice.get(m.group(1), ("", ""))[0] if m else ""
        p = self.per_slug.get(a.get("progetto"))
        if p and p.get("percorso"):
            return p["percorso"]
        return self.indice.get(a.get("progetto"), ("", ""))[0]

    # -- righe

    def riga_evento(self, e):
        adesso = self.ora
        passato = e["giorno"] < self.oggi or (e["giorno"] == self.oggi and e["fine"] and e["fine"] <= adesso)
        in_corso = (e["giorno"] == self.oggi and not e["tutto_il_giorno"] and e["inizio"] <= adesso
                    and (e["fine"] > adesso if e["fine"] else False))
        if e["tutto_il_giorno"]:
            quando = '<span class="quando"><small>tutto il giorno</small></span>'
        else:
            fine = e["fine"] or (f"fino al {data_breve(e['fine_altro_giorno'])}" if e.get("fine_altro_giorno") else "")
            quando = f'<span class="quando">{escape(e["inizio"])}<small>{escape(fine)}</small></span>'
        meta = []
        if e["luogo"]:
            meta.append(escape(e["luogo"]))
        if e["online"] and "teams" not in e["luogo"].lower() and "online" not in e["luogo"].lower():
            meta.append("online")
        if e["organizzatore"]:
            meta.append(escape(e["organizzatore"]))
        etichette = ""
        if in_corso:
            etichette += '<span class="etichetta-evento in-corso">in corso</span>'
        if e["provvisorio"]:
            etichette += '<span class="etichetta-evento provvisorio">da confermare</span>'
        classe = "voce evento" + (" passato" if passato and not in_corso else "")
        meta_html = f'<span class="meta">{" · ".join(meta)}</span>' if meta else ""
        return (f'<li class="{classe}">{quando}<span class="cosa"><span class="testo">'
                f'{testo(e["titolo"])}{etichette}</span>{meta_html}</span><span></span></li>')

    def riga_attivita(self, a, mostra_ritardo=True):
        g = a["giorno"]
        classe, ritardo = "", ""
        if g and g < self.oggi:
            classe = "scaduta"
            ritardo = f'da {plurale((self.oggi - g).days, "giorno", "giorni")}'
        elif g == self.oggi:
            classe = "in-oggi"
            ritardo = "scade oggi"
        meta = [escape(a.get("nome_progetto") or a.get("progetto") or "")]
        if a.get("coinvolto") is False:
            meta.append("osservi")
        if ritardo and mostra_ritardo:
            meta.append(f'<span class="ritardo">{ritardo}</span>')
        dettaglio = []
        if g:
            dettaglio.append(f"Scadenza: {escape(data_lunga(g))}")
        if a.get("fonte"):
            dettaglio.append(f"Fonte: {self.link_nota(a['fonte'])}")
        percorso = self.percorso_progetto(a)
        if percorso and self.repo:
            dettaglio.append(self.link(percorso, "Apri la scheda su GitHub ↗"))
        if not dettaglio:
            dettaglio.append("Nessuna fonte indicata")
        corpo = "".join(f"<span>{d}</span>" for d in dettaglio)
        return (f'<li class="{classe}"><details><summary class="voce"><span class="casella" aria-hidden="true"></span>'
                f'<span class="cosa"><span class="testo">{testo(a.get("testo"))}</span>'
                f'<span class="meta">{" · ".join(m for m in meta if m)}</span></span>'
                f'<span class="freccia" aria-hidden="true"></span></summary>'
                f'<div class="dettaglio">{corpo}</div></details></li>')

    def gruppo(self, titolo, righe, id_="", relativo=""):
        if not righe:
            return ""
        idattr = f' id="{id_}"' if id_ else ""
        rel = f' <span class="relativo">{escape(relativo)}</span>' if relativo else ""
        return (f'<div class="gruppo"{idattr}><h3>{escape(titolo)}{rel}</h3>'
                f'<ul class="righe">{"".join(righe)}</ul></div>')

    # -- contatori

    def n_oggi(self):
        return len(self.eventi_oggi) + len(self.di_oggi)

    def n_settimana(self):
        return len(self.eventi_settimana) + len(self.della_settimana)

    def contatori(self):
        voci = [
            ("#scadute" if self.scadute else "#oggi", len(self.scadute), "scadute", "allarme"),
            ("#oggi", self.n_oggi(), "oggi", "attenzione"),
            ("#settimana", self.n_settimana(), "in settimana", ""),
        ]
        out = []
        for href, n, etichetta, tono in voci:
            classe = "contatore " + ((tono or "") if n else "zero")
            out.append(f'<a class="{classe.strip()}" href="{href}"><span class="n">{n}</span>'
                       f'<span class="etichetta">{etichetta}</span></a>')
        return "".join(out)

    # -- blocchi

    def avviso_eventi(self):
        if self.eventi is not None:
            return ""
        messaggio = "Calendario non disponibile in questo giro"
        if self.avviso_calendario:
            messaggio += f" ({self.avviso_calendario})"
        return f'<p class="vuoto calendario-assente">{escape(messaggio)}</p>'

    def blocco_oggi(self):
        parti = [self.avviso_eventi()]
        parti.append(self.gruppo("Agenda", [self.riga_evento(e) for e in self.eventi_oggi]))
        parti.append(self.gruppo("Scadute", [self.riga_attivita(a) for a in self.scadute], "scadute"))
        parti.append(self.gruppo("In scadenza oggi", [self.riga_attivita(a) for a in self.di_oggi]))
        if not (self.eventi_oggi or self.scadute or self.di_oggi):
            parti.append('<p class="vuoto">Niente in scadenza oggi</p>')
        n = self.n_oggi() + len(self.scadute)
        return (f'<h2>Oggi <span class="conta">{n}</span></h2>'
                f'<div class="pannello">{"".join(parti)}</div>')

    def blocco_settimana(self):
        giorni = []
        for i in range(1, GIORNI_SETTIMANA + 1):
            g = self.oggi + timedelta(days=i)
            righe = [self.riga_evento(e) for e in self.eventi_settimana if e["giorno"] == g]
            righe += [self.riga_attivita(a) for a in self.della_settimana if a["giorno"] == g]
            relativo = "domani" if i == 1 else ""
            giorni.append(self.gruppo(giorno_breve(g), righe, relativo=relativo))
        corpo = "".join(giorni)
        if not corpo:
            corpo = '<p class="vuoto">Niente nei prossimi 7 giorni</p>'
        avviso = self.avviso_eventi()
        return (f'<h2>Prossimi 7 giorni <span class="conta">{self.n_settimana()}</span></h2>'
                f'<div class="pannello">{avviso}{corpo}</div>')

    def stato_progetto(self, p):
        """(categoria, scadute, giorni da fermo): 0 scaduto, 1 fermo, 2 in ordine."""
        slug = p.get("progetto")
        scadute = sum(1 for a in self.scadute if a.get("progetto") == slug)
        rif = giorno(p.get("ultimo_log")) or giorno(p.get("aggiornato"))
        fermo = (self.oggi - rif).days if rif else None
        if scadute:
            return 0, scadute, fermo
        if fermo is None or fermo > FERMO_GIORNI:
            return 1, scadute, fermo
        return 2, scadute, fermo

    def ordina_progetti(self, progetti):
        progetti = sorted(progetti, key=lambda p: str(p.get("aggiornato") or ""), reverse=True)
        def chiave(p):
            cat, scadute, fermo = self.stato_progetto(p)
            return (p.get("coinvolto") is False, cat, -scadute, -(fermo or 10**6) if cat == 1 else 0)
        return sorted(progetti, key=chiave)

    def carta(self, p):
        slug = p.get("progetto")
        cat, scadute, fermo = self.stato_progetto(p)
        tono, parola = [("allarme", "scaduto"),
                        ("attenzione", f"fermo da {plurale(fermo, 'giorno', 'giorni')}" if fermo is not None else "fermo"),
                        ("ok", "in ordine")][cat]
        osservi = p.get("coinvolto") is False
        aperte = sorted((a for a in self.aperte if a.get("progetto") == slug),
                        key=lambda a: a["giorno"] or date.max)
        datate = [a for a in aperte if a["giorno"]]
        senza = len(aperte) - len(datate)
        numeri = plurale(len(aperte), "aperta", "aperte")
        if scadute:
            numeri += f' · <b>{plurale(scadute, "scaduta", "scadute")}</b>'
        passi = [str(x) for x in (p.get("prossimi_passi") or []) if str(x).strip()]
        if passi:
            passo = f'<span class="passo">{testo(passi[0])}</span>'
        elif datate:
            passo = (f'<span class="passo"><span class="data">{escape(data_breve(datate[0]["giorno"]))} ·</span> '
                     f'{testo(datate[0].get("testo"))}</span>')
        elif p.get("prossima_testo"):
            g = giorno(p.get("prossima"))
            data = f'<span class="data">{escape(data_breve(g))} ·</span> ' if g else ""
            passo = f'<span class="passo">{data}{testo(p["prossima_testo"])}</span>'
        elif aperte:
            passo = f'<span class="passo">{testo(aperte[0].get("testo"))}</span>'
        else:
            passo = '<span class="passo manca">Nessun prossimo passo nella scheda</span>'
        chip = '<span class="chip">osservi</span>' if osservi else ""
        cliente = f'<span class="cliente">{escape(p.get("clienti") or "")}</span>' if p.get("clienti") else ""
        testa = (f'<span class="carta-testa"><span class="semaforo"><i></i>{escape(parola)}</span>{chip}'
                 f'<span class="numeri">{numeri}</span><span class="freccia" aria-hidden="true"></span></span>')
        corpo = []
        if passi:
            corpo.append('<div><h4>Prossimi passi</h4><ul class="passi">'
                         + "".join(f"<li>{testo(x)}</li>" for x in passi) + "</ul></div>")
        if datate or senza:
            righe = "".join(
                f'<li class="{"scaduta" if a["giorno"] < self.oggi else ""}"><span class="data">'
                f'{escape(data_breve(a["giorno"]))}</span><span>{testo(a.get("testo"))}</span></li>'
                for a in datate)
            elenco = f'<ul class="elenco">{righe}</ul>' if righe else ""
            extra = (f'<p class="nota-piccola">{plurale(senza, "attività senza data", "attività senza data")}</p>'
                     if senza else "")
            corpo.append(f"<div><h4>Attività aperte</h4>{elenco}{extra}</div>")
        log = sorted((r for r in self.log if r.get("progetto") == slug),
                     key=lambda r: str(r.get("data") or ""), reverse=True)[:ULTIMI_LOG]
        if log:
            righe = "".join(
                f'<li><span class="data">{escape(data_breve(giorno(r.get("data"))) if giorno(r.get("data")) else "")}'
                f'</span><span>{testo(r.get("testo"))}</span></li>' for r in log)
            corpo.append(f'<div><h4>Ultimi passi</h4><ul class="elenco">{righe}</ul></div>')
        percorso = p.get("percorso") or self.indice.get(slug, ("", ""))[0]
        if percorso and self.repo:
            corpo.append(f"<p>{self.link(percorso, 'Apri la scheda su GitHub ↗', 'vai')}</p>")
        if not corpo:
            corpo.append('<p class="nota-piccola">Niente di aperto in questo progetto</p>')
        classi = f"carta stato-{tono}" + (" osservi" if osservi else "")
        return (f'<details class="{classi}" data-progetto="{escape(slug or "")}"><summary>{testa}'
                f'<h3>{escape(p.get("nome") or slug or "")}</h3>{cliente}{passo}</summary>'
                f'<div class="carta-corpo">{"".join(corpo)}</div></details>')

    def attivi(self):
        return [p for p in self.progetti if str(p.get("stato") or "").lower() == "attivo"]

    def blocco_progetti(self):
        attivi = self.ordina_progetti(self.attivi())
        seguiti = [p for p in attivi if p.get("coinvolto") is not False]
        osservati = [p for p in attivi if p.get("coinvolto") is False]
        pulsante = '<button type="button" class="interruttore spinta" id="apri-tutte" hidden>apri tutte</button>'
        out = [f'<h2>Progetti <span class="conta">{len(attivi)}</span>{pulsante}</h2>']
        if not attivi:
            out.append('<div class="pannello"><p class="vuoto">Nessun progetto attivo</p></div>')
        if seguiti:
            out.append('<div class="carte">' + "".join(self.carta(p) for p in seguiti) + "</div>")
        if osservati:
            out.append(f'<p class="titoletto osservi-titolo">Progetti che osservi <span class="conta">{len(osservati)}</span></p>')
            out.append('<div class="carte">' + "".join(self.carta(p) for p in osservati) + "</div>")
        altri = [p for p in self.progetti if str(p.get("stato") or "").lower() != "attivo"]
        if altri:
            voci = " · ".join(f'{escape(p.get("nome") or p.get("progetto") or "")} '
                              f'({escape(str(p.get("stato") or "senza stato"))})' for p in altri)
            out.append(f'<p class="nota-piccola">Non attivi: {voci}</p>')
        return "".join(out)

    def conteggio_task(self):
        conta = {}
        for t in self.task:
            conta[t.get("stato")] = conta.get(t.get("stato"), 0) + 1
        return conta

    def blocco_fondo(self):
        riquadri = []
        if self.inbox:
            n = len(self.inbox)
            riquadri.append(f'<div class="riquadro"><p class="titoletto">Inbox</p>'
                            f'<p class="grande">{n}</p><p>{"nota" if n == 1 else "note"} da smistare</p></div>')
        if self.digest:
            d = self.digest[0]
            g = giorno(d.get("giorno"))
            nome = f"Digest del {data_breve(g)}" if g else "Ultimo digest"
            percorso = self.indice.get(str(d.get("giorno")), ("", ""))[0]
            titolo = self.link(percorso, nome) if percorso else escape(nome)
            voci = [plurale(int(d.get("note_nuove") or 0), "nota nuova", "note nuove"),
                    plurale(int(d.get("note_aggiornate") or 0), "aggiornata", "aggiornate"),
                    plurale(int(d.get("decisioni") or 0), "decisione", "decisioni")]
            riquadri.append(f'<div class="riquadro"><p class="titoletto">Novità</p><p>{titolo}</p>'
                            f'<ul>{"".join(f"<li>{v}</li>" for v in voci)}</ul></div>')
        conta = self.conteggio_task()
        if self.task:
            parti = [f"{conta.get('ok', 0)} OK"] if conta.get("ok") else []
            for stato, uno, molti in (("errore", "errore", "errori"), ("mancante", "mancante", "mancanti"),
                                      ("atteso", "atteso", "attesi")):
                if conta.get(stato):
                    parti.append(plurale(conta[stato], uno, molti))
            non_ok, attesi = [], []
            for t in self.task:
                ora = t.get("eseguito") or t.get("atteso") or ""
                nome = f'{escape(t.get("task") or "")} {escape(ora)}'
                if t.get("stato") == "atteso":
                    attesi.append(nome)
                elif t.get("stato") != "ok":
                    riga = f'{nome} · {escape(t.get("stato") or "")}'
                    if t.get("stato") == "errore" and t.get("esito"):
                        riga += f': {escape(t["esito"])}'
                    non_ok.append(f'<li class="ko">{riga}</li>')
            if attesi:
                non_ok.append(f'<li>Da eseguire: {", ".join(attesi)}</li>')
            elenco = f'<ul>{"".join(non_ok)}</ul>' if non_ok else ""
            riquadri.append(f'<div class="riquadro"><p class="titoletto">Task di oggi</p>'
                            f'<p>{" · ".join(parti)}</p>{elenco}</div>')
        else:
            riquadri.append('<div class="riquadro"><p class="titoletto">Task di oggi</p>'
                            '<p>Nessun task registrato</p></div>')
        out = ['<h2>Il resto</h2>', f'<div class="fondo">{"".join(riquadri)}</div>']
        senza = {}
        for a in self.aperte:
            if not a["giorno"]:
                nome = a.get("nome_progetto") or a.get("progetto") or ""
                senza[nome] = senza.get(nome, 0) + 1
        if senza:
            totale = sum(senza.values())
            righe = "".join(f"<li><span>{escape(nome)}</span><b>{n}</b></li>"
                            for nome, n in sorted(senza.items(), key=lambda kv: (-kv[1], kv[0])))
            out.append(f'<details class="senza-data"><summary>Attività senza data '
                       f'<span class="conta">{totale}</span><span class="freccia" aria-hidden="true"></span>'
                       f"</summary><ul>{righe}</ul></details>")
        return "".join(out)

    def piede(self):
        return f"Generato da cockpit.py dal vault · {escape(data_breve(self.oggi))} {self.oggi.year}, {escape(self.ora)}"

    # -- tutto

    def html(self, template):
        valori = {
            "titolo": escape(self.titolo),
            "ora": escape(self.ora),
            "data_lunga": escape(data_lunga(self.oggi)),
            "contatori": self.contatori(),
            "blocco_oggi": self.blocco_oggi(),
            "blocco_settimana": self.blocco_settimana(),
            "blocco_progetti": self.blocco_progetti(),
            "blocco_fondo": self.blocco_fondo(),
            "piede": self.piede(),
        }
        mancanti = set(SEGNAPOSTO.findall(template)) - set(valori)
        if mancanti:
            raise DatiMancanti(f"segnaposto sconosciuti nel template: {', '.join(sorted(mancanti))}")
        # Una sola passata: il testo delle note, anche se contiene graffe, non viene riletto.
        return SEGNAPOSTO.sub(lambda m: valori[m.group(1)], template)

    def riepilogo(self):
        in_scadenza = len(self.di_oggi) + len(self.della_settimana)
        if self.eventi is None:
            eventi = "calendario non disponibile"
        else:
            n = len({e["chiave"] for e in self.eventi if self.oggi <= e["giorno"] <= self.ultimo})
            eventi = plurale(n, "evento", "eventi")
        conta = self.conteggio_task()
        dovuti = sum(n for s, n in conta.items() if s != "atteso")
        return (f"{len(self.attivi())} progetti attivi, {plurale(len(self.scadute), 'attività scaduta', 'attività scadute')}, "
                f"{in_scadenza} in scadenza entro 7 giorni, {eventi}, {conta.get('ok', 0)} task OK su {dovuti}")


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(2, f"{self.prog}: errore: {message}\n")


class Formato(argparse.RawDescriptionHelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        return super().add_usage(usage, actions, groups, "uso: ")


def argomenti(argv):
    parser = Parser(
        prog="cockpit.py", add_help=False, formatter_class=Formato,
        description="Genera la pagina Cockpit (HTML statico e autosufficiente) dai JSON di plancia.py\n"
                    "e, se c'è, da calendario.json. Lo schema del calendario è nel docstring dello script.",
        epilog="Esce con 1 se un JSON obbligatorio manca o non si legge, con 2 se gli argomenti non sono validi.")
    parser._positionals.title = "argomenti"
    parser._optionals.title = "opzioni"
    parser.add_argument("-h", "--help", action="help", help="mostra questo aiuto ed esce")
    parser.add_argument("cartella_dati", type=Path, help="cartella scritta da plancia.py (più calendario.json, facoltativo)")
    parser.add_argument("file_html", type=Path, help="file HTML da scrivere")
    parser.add_argument("--oggi", help="giorno di riferimento AAAA-MM-GG (predefinito: oggi in Europe/Rome)")
    parser.add_argument("--ora", help="ora dell'aggiornamento HH:MM (predefinito: adesso in Europe/Rome)")
    parser.add_argument("--repo-url", help="base dei link alle note, per esempio https://github.com/<owner>/<repo> "
                                           "(predefinito: dal remote origin del vault; \"\" toglie i link)")
    parser.add_argument("--titolo", default="Cockpit BlueAge", help="titolo della pagina (predefinito: %(default)s)")
    args = parser.parse_args(argv)
    adesso = datetime.now(ROMA)
    if args.oggi is None:
        args.oggi = adesso.date()
    else:
        try:
            args.oggi = date.fromisoformat(args.oggi)
        except ValueError:
            parser.error(f"--oggi non valido: {args.oggi} (serve AAAA-MM-GG)")
    if args.ora is None:
        args.ora = adesso.strftime("%H:%M")
    elif not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", args.ora):
        parser.error(f"--ora non valida: {args.ora} (serve HH:MM)")
    if not args.titolo.strip():
        parser.error("--titolo vuoto")
    return args


def main(argv=None):
    args = argomenti(sys.argv[1:] if argv is None else argv)
    try:
        dati = {nome: leggi_json(args.cartella_dati, nome) for nome in OBBLIGATORI}
        template = TEMPLATE.read_text(encoding="utf-8")
    except DatiMancanti as e:
        print(f"Errore: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"Errore: template non leggibile: {e}", file=sys.stderr)
        return 1
    eventi, avviso = leggi_calendario(args.cartella_dati, args.oggi, args.oggi + timedelta(days=GIORNI_SETTIMANA))
    if avviso:
        print(f"Avviso: {avviso}", file=sys.stderr)
    repo = repo_da_git() if args.repo_url is None else re.sub(r"\.git$", "", args.repo_url.strip().rstrip("/"))
    pagina = Pagina(dati, eventi, avviso if eventi is None else "", args.oggi, args.ora, repo,
                    args.titolo.strip(), indice_note())
    try:
        html = pagina.html(template)
    except DatiMancanti as e:
        print(f"Errore: {e}", file=sys.stderr)
        return 1
    args.file_html.parent.mkdir(parents=True, exist_ok=True)
    args.file_html.write_text(html, encoding="utf-8")
    print(pagina.riepilogo())
    return 0


if __name__ == "__main__":
    sys.exit(main())
