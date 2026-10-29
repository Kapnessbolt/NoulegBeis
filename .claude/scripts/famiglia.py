#!/usr/bin/env python3
"""Chiave di famiglia e slug (SPEC 4.3, agente ingestor §3.1, §3.2 e §3.6).

Dal nome di un file toglie, nell'ordine: estensione; date (anche con l'ora che le segue);
suffissi di versione, di stato e di copia; poi applica lo slug. Esempio obbligatorio:
`BlueAge_CompanyProfile_v24.pdf` → `blueage-companyprofile`.

- Date: `2026-10-01`, `2026_10_01`, `20261001`, `01.10.2026`, `01-10-2026`, `2026-10`,
  `260918` (AAMMGG) e l'ora che segue una data (`260929-1744`), `ott26`, `ottobre 2026`,
  `del 6 ottobre`, un anno isolato (`_2026`).
- Suffissi in coda, anche ripetuti: versione (`_v24`, ` v2`, `- v001`, `_v1.2`, `_rev3`,
  `version 1`, una lettera maiuscola isolata dopo `_` come `PULSE_Sintesi_C`), stato
  (`_final`, `_def`, `_definitivo`, `_signed`, `_firmato`, `_sent`, `_inviato`, `_bozza`,
  `_draft`), copia (`(1)`, `- Copia`, `copy`), firma dell'autore (`fonti.firme_in_coda` in
  `vault.yaml`, es. `_<Firma>`).
- Slug: minuscolo, senza accenti, apostrofi tolti (`d'acquisto` → `dacquisto`), ogni altro
  carattere che non è lettera o cifra diventa `-`, trattini doppi ridotti, niente trattini ai bordi.

Uso:
  python3 .claude/scripts/famiglia.py <nome file> [--json]   # chiave di famiglia
  python3 .claude/scripts/famiglia.py --slug "<testo>"        # solo lo slug (segmenti, titoli)
  python3 .claude/scripts/famiglia.py --oggetto "<oggetto>"   # slug dell'oggetto di una mail,
                                                              # senza RE:, R:, FW:, FWD:, I:
  python3 .claude/scripts/famiglia.py --cerca <nome file> [--cartella sources/...] [--json]
      # note source-doc del vault della stessa famiglia: per `family`, per nome del file, o
      # perché la famiglia calcolata da `current.name` o da una voce di `versions` coincide.
      # Esce con 1 se non ne trova. Decidere se è una nuova versione, una copia (`also_at`)
      # o un'altra famiglia resta all'agente (ingestor §3.2).
  python3 .claude/scripts/famiglia.py --verifica [--json]
      # golden test sul vault: famiglia calcolata da `current.name` contro `family` per le
      # note sharepoint, onedrive e attachment; esce con 1 se l'accordo è sotto il 90%.

La variabile d'ambiente VAULT_ROOT, se presente, indica la radice del vault al posto della
cartella che contiene `.claude/` (serve ai test in `.claude/scripts/tests/`).
"""

import json
import os
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config  # noqa: E402

ROOT = Path(os.environ.get("VAULT_ROOT") or Path(__file__).resolve().parents[2]).resolve()

# Separatori tra le parti di un nome di file
SEP = r"[\s_.\-–—·()\[\],]"
INIZIO = rf"(?:^|(?<={SEP}))"
FINE = rf"(?=$|{SEP})"

MESI_IT = ("gennaio febbraio marzo aprile maggio giugno luglio agosto settembre ottobre "
           "novembre dicembre").split()
MESI_EN = ("january february march april may june july august september october november "
           "december").split()
ABBR = ("gen feb mar apr mag giu lug ago set sett ott nov dic "
        "jan may jun jul aug sep sept oct dec").split()
MESI = "|".join(sorted(set(MESI_IT + MESI_EN + ABBR), key=len, reverse=True))

GG = r"(?:0?[1-9]|[12]\d|3[01])"
MM = r"(?:0?[1-9]|1[0-2])"
ANNO = r"(?:19|20)\d{2}"
ORA = r"(?:[01]\d|2[0-3])[.:h]?[0-5]\d"

DATE = [
    # 2026-10-01, 2026_10_01, 2026.10.01, 20261001
    rf"{ANNO}[-_.]{MM}[-_.]{GG}",
    rf"{ANNO}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])",
    # 01.10.2026, 01-10-2026, 01_10_2026
    rf"{GG}[-_.]{MM}[-_.]{ANNO}",
    # 260918 (AAMMGG)
    r"\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])",
    # 2026-10 (anno e mese)
    rf"{ANNO}[-_.](?:0[1-9]|1[0-2])",
    # ott26, ott-26, ottobre 2026, oct_2026
    rf"(?:{MESI})[\s_\-.]?(?:{ANNO}|[23]\d)",
    # del 6 ottobre, 6 ottobre 2026
    rf"(?:(?:del|dal|al|il)\s+)?{GG}\s+(?:{MESI})(?:\s+{ANNO})?",
    # anno isolato: _2026
    ANNO,
]
DATA_RE = re.compile(rf"{INIZIO}(?:{'|'.join(DATE)})(?:[\s_\-]{ORA})?{FINE}", re.I)

# Suffissi in coda: versione, stato, copia (si tolgono ripetutamente)
VERSIONE = r"(?:v|ver|rev|version|versione)[\s_.]?\d+(?:[._]\d+)*"
STATO = r"(?:final|finale|def|definitivo|definitiva|signed|firmato|firmata|sent|inviato|inviata|bozza|draft)"
COPIA = r"(?:copia|copy)"
CODA_RE = re.compile(rf"(?:(?:{SEP}+|^)(?:{VERSIONE}|{STATO}|{COPIA})|\s*\(\d+\))\s*$", re.I)
# Firma dell'autore in coda (`Manini_G1_Strategia_<Firma>.pptx`): non distingue il documento.
# Le firme sono in `vault.yaml` (`fonti.firme_in_coda`).
_FIRMA = {}


def firma_re():
    firme = config.firme_in_coda()
    if firme not in _FIRMA:
        _FIRMA[firme] = re.compile(rf"{SEP}+(?:{'|'.join(map(re.escape, firme))})\s*$", re.I) if firme else None
    return _FIRMA[firme]

LETTERA_RE = re.compile(r"_[A-Z]$")  # PULSE_Sintesi_C: lettera di versione (maiuscola, dopo `_`)
ESTENSIONE_RE = re.compile(r"\.[A-Za-z0-9]{1,5}$")
SPAZZATURA_RE = re.compile(rf"{SEP}+$")

PREFISSI_OGGETTO_RE = re.compile(r"^\s*(?:re|r|fw|fwd|i|inoltro)\s*:\s*", re.I)


def slug(testo):
    """Slug di vault: minuscolo, senza accenti, apostrofi tolti, il resto in trattini."""
    s = unicodedata.normalize("NFKD", str(testo))
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()  # accenti via, `–` resta
    s = re.sub(r"['’`´]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def togli_coda(s):
    """Toglie un suffisso di versione, stato o copia in coda. Restituisce (testo, tolto?)."""
    m = CODA_RE.search(s)
    if m and m.start() > 0:
        return s[:m.start()], True
    for regola in (firma_re(), LETTERA_RE):
        m = regola.search(s) if regola else None
        if m and m.start() > 0:
            return s[:m.start()], True
    return s, False


def famiglia(nome):
    """Chiave di famiglia da un nome di file (anche con percorso o URL)."""
    base = unquote(str(nome)).replace("\\", "/").rstrip("/").rsplit("/", 1)[-1].strip()
    stem = ESTENSIONE_RE.sub("", base) if "." in base else base
    s = DATA_RE.sub(" ", stem)
    while True:
        s, tolto = togli_coda(s.rstrip())
        if not tolto:
            pulito = SPAZZATURA_RE.sub("", s)
            if pulito == s:
                break
            s = pulito
    return slug(s) or slug(stem)


def slug_oggetto(oggetto):
    """Slug dell'oggetto di una mail senza prefissi di risposta e inoltro, anche ripetuti."""
    s = str(oggetto)
    while True:
        nuovo = PREFISSI_OGGETTO_RE.sub("", s)
        if nuovo == s:
            break
        s = nuovo
    return slug(s)


# --- Ricerca nel vault ------------------------------------------------------------------

def _frontmatter(p):
    import yaml  # solo qui: il calcolo della famiglia non richiede PyYAML
    testo = p.read_text(encoding="utf-8")
    if not testo.startswith("---\n"):
        return None
    fine = testo.find("\n---", 4)
    if fine == -1:
        return None
    try:
        return yaml.safe_load(testo[4:fine]) or {}
    except yaml.YAMLError:
        return None


def note_documento():
    """(percorso relativo, frontmatter) di ogni nota source-doc in sources/."""
    for p in sorted((ROOT / "sources").rglob("*.md")):
        d = _frontmatter(p)
        if isinstance(d, dict) and d.get("type") == "source-doc":
            yield p.relative_to(ROOT), d


def cerca(nome, cartella=None):
    chiave = famiglia(nome)
    trovate = []
    for rel, d in note_documento():
        motivi = []
        if d.get("family") == chiave:
            motivi.append("family")
        if rel.stem == chiave:
            motivi.append("nome della nota")
        nomi = [(d.get("current") or {}).get("name")] + [v.get("name") for v in d.get("versions") or []
                                                          if isinstance(v, dict)]
        if any(n and famiglia(n.split("@")[0]) == chiave for n in nomi):
            motivi.append("nome di una versione")
        if motivi:
            trovate.append({
                "nota": str(rel),
                "family": d.get("family"),
                "source": d.get("source"),
                "stessa_cartella": bool(cartella) and str(rel.parent) == str(cartella).rstrip("/"),
                "motivo": ", ".join(motivi),
            })
    trovate.sort(key=lambda t: (not t["stessa_cartella"], t["nota"]))
    return chiave, trovate


def verifica():
    """Golden test: famiglia calcolata da `current.name` contro `family` registrata."""
    righe = []
    for rel, d in note_documento():
        if d.get("source") not in ("sharepoint", "onedrive", "attachment"):
            continue
        nome = (d.get("current") or {}).get("name") or ""
        calcolata = famiglia(nome)
        registrata = d.get("family")
        if calcolata == registrata:
            esito = "uguale"
        elif str(registrata).endswith("-" + calcolata):
            esito = "prefisso"  # prefisso di disambiguazione scelto dall'agente (ingestor §3.2)
        else:
            esito = "diversa"
        righe.append({"nota": str(rel), "nome": nome, "calcolata": calcolata,
                      "registrata": registrata, "esito": esito})
    n = len(righe)
    uguali = sum(r["esito"] == "uguale" for r in righe)
    con_prefisso = sum(r["esito"] == "prefisso" for r in righe)
    return {"note": n, "uguali": uguali, "con_prefisso": con_prefisso,
            "accordo": round(100 * uguali / n, 1) if n else 100.0,
            "accordo_con_prefisso": round(100 * (uguali + con_prefisso) / n, 1) if n else 100.0,
            "disaccordi": [r for r in righe if r["esito"] != "uguale"]}


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if argv else 2
    as_json = "--json" in argv
    args = [a for a in argv if a != "--json"]
    op = args[0]
    if op in ("--slug", "--oggetto"):
        if len(args) != 2:
            sys.stderr.write(f"{op} vuole un solo testo tra virgolette\n")
            return 2
        risultato = slug(args[1]) if op == "--slug" else slug_oggetto(args[1])
        if not risultato:
            sys.stderr.write(f"slug vuoto per {args[1]!r}\n")
            return 1
        print(json.dumps({"slug": risultato}) if as_json else risultato)
        return 0
    if op == "--cerca":
        cartella = None
        if "--cartella" in args:
            i = args.index("--cartella")
            if i + 1 >= len(args):
                sys.stderr.write("--cartella vuole un percorso\n")
                return 2
            cartella = args[i + 1]
            args = args[:i] + args[i + 2:]
        if len(args) != 2:
            sys.stderr.write("--cerca vuole un nome di file\n")
            return 2
        chiave, trovate = cerca(args[1], cartella)
        if as_json:
            print(json.dumps({"famiglia": chiave, "note": trovate}, ensure_ascii=False, indent=2))
        else:
            print(f"famiglia: {chiave}")
            for t in trovate:
                dove = " (stessa cartella)" if t["stessa_cartella"] else ""
                print(f"- {t['nota']}{dove} · family {t['family']} · {t['motivo']}")
            if not trovate:
                print("nessuna nota della stessa famiglia")
        return 0 if trovate else 1
    if op == "--verifica":
        r = verifica()
        if as_json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        else:
            print(f"{r['note']} note · uguali {r['uguali']} ({r['accordo']}%) · "
                  f"con prefisso di disambiguazione {r['con_prefisso']} "
                  f"(accordo complessivo {r['accordo_con_prefisso']}%)")
            for d in r["disaccordi"]:
                print(f"- [{d['esito']}] {d['nome']} → {d['calcolata']} ≠ {d['registrata']}")
        return 0 if r["accordo_con_prefisso"] >= 90 else 1
    if op.startswith("--"):
        sys.stderr.write(f"opzione sconosciuta: {op}\n")
        return 2
    if len(args) != 1:
        sys.stderr.write("un solo nome di file (tra virgolette se contiene spazi)\n")
        return 2
    chiave = famiglia(args[0])
    if not chiave:
        sys.stderr.write(f"famiglia vuota per {args[0]!r}\n")
        return 1
    print(json.dumps({"nome": args[0], "famiglia": chiave}, ensure_ascii=False) if as_json else chiave)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
