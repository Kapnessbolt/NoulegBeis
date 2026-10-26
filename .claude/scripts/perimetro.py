#!/usr/bin/env python3
"""Perimetro delle fonti (SPEC 5.1-5.2, agente ingestor §2 e §3.1): dice se il `webUrl` di un
documento di SharePoint o OneDrive è dentro il perimetro e in quale cartella va la sua nota.

Il confronto ignora maiuscole e minuscole e decodifica `%20` (e ogni altro `%xx`). Le
esclusioni valgono per le cartelle del percorso, non per il nome del file. Non si vede
dall'URL, e resta all'agente, la cartella di un progetto software (contiene `app.json`,
`package.json` o `.git`, es. `/Lab AL/`): se il documento sta lì, è fuori perimetro anche se
questo script dice `dentro`.

Uso:
  python3 .claude/scripts/perimetro.py <webUrl> [--json]
  python3 .claude/scripts/perimetro.py --verifica [--json]
      # golden test sul vault: per ogni nota sharepoint e onedrive, la cartella calcolata da
      # `current.web_url` contro la cartella reale della nota

Uscita: 0 se dentro, 1 se fuori, 2 se l'URL non è di SharePoint o OneDrive del tenant.
Con `--json` stampa:
  {"dentro": true|false, "motivo": "...", "fonte": "sharepoint"|"onedrive"|null,
   "libreria": "...", "cartella_nota": "sources/sharepoint/<libreria>/<percorso>"
                                       | "sources/onedrive/<percorso>" | null,
   "tipo_processato": true|false|null}
`cartella_nota` segue ingestor §3.1: segmenti in slug; per OneDrive il percorso parte da dentro
`BlueAge/`; per gli altri siti SharePoint (solo compito `file`) `sources/sharepoint/_<sito>/...`.
Per i file di OneDrive fuori da `BlueAge/` è null.

La variabile d'ambiente VAULT_ROOT, se presente, indica la radice del vault al posto della
cartella che contiene `.claude/` (serve ai test in `.claude/scripts/tests/`).
"""

import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from famiglia import slug  # noqa: E402

ROOT = Path(os.environ.get("VAULT_ROOT") or Path(__file__).resolve().parents[2]).resolve()

# --- Perimetro (SPEC 5.1-5.2) -----------------------------------------------------------
# Nello step 13 (SPEC 13.1) prefissi, esclusioni e tipi passano in `vault.yaml`.
SHAREPOINT = "https://blueagesrl.sharepoint.com/sites/"
ONEDRIVE = "https://blueagesrl-my.sharepoint.com/personal/"
SITO_INTERNO = "internal"
ONEDRIVE_UTENTE = "lorenzo_curione_blueage_it"
ONEDRIVE_LIBRERIA = "Documents"
ONEDRIVE_CARTELLA = "BlueAge"
PREFISSI_INCLUSI = (
    "https://blueagesrl.sharepoint.com/sites/internal/SalesMarketing/",
    "https://blueagesrl.sharepoint.com/sites/internal/Delivery/",
    "https://blueagesrl.sharepoint.com/sites/internal/Shared Documents/",
    "https://blueagesrl-my.sharepoint.com/personal/lorenzo_curione_blueage_it/Documents/BlueAge/",
)
# Cartelle escluse in qualunque punto del percorso (nome senza maiuscole)
CARTELLE_ESCLUSE = {"siteassets", "_originali", "_sorgenti", "dati"}
# Cartelle escluse per come finisce il nome (`05 Transcript`)
FINALI_ESCLUSI = ("transcript",)
# Cartelle escluse dentro un'altra: (finale del nome del genitore, nome della cartella)
DENTRO_ESCLUSE = (("evidenze", "export"),)
TIPI_PROCESSATI = {"pdf", "docx", "pptx", "xlsx", "md", "txt"}

ORDINE_RE = re.compile(r"^\d+[\s_.-]*")  # numero d'ordine davanti al nome: `01_Dati`, `06 Evidenze`


def nome_cartella(segmento):
    return ORDINE_RE.sub("", segmento.strip().lower())


def cartella_esclusa(cartelle):
    """Motivo dell'esclusione, o None. `cartelle`: segmenti del percorso senza il nome del file."""
    precedente = ""
    for seg in cartelle:
        basso, nome = seg.strip().lower(), nome_cartella(seg)
        if basso in CARTELLE_ESCLUSE or nome in CARTELLE_ESCLUSE:
            return f"cartella esclusa `{seg}`"
        if any(basso.endswith(f) for f in FINALI_ESCLUSI):
            return f"cartella esclusa `{seg}` (trascrizioni grezze)"
        for genitore, figlio in DENTRO_ESCLUSE:
            if precedente.strip().lower().endswith(genitore) and nome == figlio:
                return f"cartella esclusa `{seg}` dentro `{precedente}` (export grezzi)"
        precedente = seg
    return None


def analizza(web_url):
    """Dizionario del risultato; `riconosciuto` False se l'URL non è del tenant."""
    url = unquote(urlsplit(str(web_url).strip())._replace(query="", fragment="").geturl())
    url = re.sub(r"/:[a-z]:/[rs]/", "/", url, flags=re.I)  # link di condivisione /:x:/r/
    basso = url.lower()
    out = {"dentro": False, "motivo": "", "fonte": None, "libreria": None,
           "cartella_nota": None, "tipo_processato": None, "riconosciuto": True}

    if basso.startswith(SHAREPOINT.lower()):
        parti = [p for p in url[len(SHAREPOINT):].split("/") if p]
        if len(parti) < 3:
            return {**out, "riconosciuto": False, "motivo": "URL di SharePoint senza libreria o file"}
        sito, libreria, resto = parti[0], parti[1], parti[2:]
        cartelle, nome_file = resto[:-1], resto[-1]
        out.update(fonte="sharepoint", libreria=libreria)
        base = ["sources", "sharepoint"] + ([] if sito.lower() == SITO_INTERNO else [f"_{slug(sito)}"])
        out["cartella_nota"] = "/".join(base + [slug(libreria)] + [slug(c) for c in cartelle])
    elif basso.startswith(ONEDRIVE.lower()):
        parti = [p for p in url[len(ONEDRIVE):].split("/") if p]
        if len(parti) < 3:
            return {**out, "riconosciuto": False, "motivo": "URL di OneDrive senza libreria o file"}
        utente, libreria, resto = parti[0], parti[1], parti[2:]
        cartelle, nome_file = resto[:-1], resto[-1]
        out.update(fonte="onedrive", libreria=libreria)
        dentro_cartella = (utente.lower() == ONEDRIVE_UTENTE and libreria.lower() == ONEDRIVE_LIBRERIA.lower()
                           and cartelle and cartelle[0].lower() == ONEDRIVE_CARTELLA.lower())
        if dentro_cartella:
            out["cartella_nota"] = "/".join(["sources", "onedrive"] + [slug(c) for c in cartelle[1:]])
    else:
        return {**out, "riconosciuto": False, "motivo": "URL non di SharePoint o OneDrive del tenant"}

    estensione = nome_file.rsplit(".", 1)[-1].lower() if "." in nome_file else None
    out["tipo_processato"] = None if estensione is None else estensione in TIPI_PROCESSATI

    prefisso = next((p for p in PREFISSI_INCLUSI if basso.startswith(p.lower())), None)
    if not prefisso:
        if out["fonte"] == "sharepoint":
            if parti[0].lower() != SITO_INTERNO:
                out["motivo"] = f"sito `{parti[0]}` fuori perimetro"
            else:
                out["motivo"] = f"libreria `{out['libreria']}` fuori perimetro"
        else:
            out["motivo"] = f"OneDrive fuori dalla cartella `{ONEDRIVE_CARTELLA}/`"
        return out
    escluso = cartella_esclusa(cartelle)
    if escluso:
        out["motivo"] = escluso
        return out
    if out["tipo_processato"] is False:
        out["motivo"] = f"tipo `.{estensione}` non processato"
        return out
    out["dentro"] = True
    out["motivo"] = f"prefisso `{prefisso}`"
    return out


def verifica():
    """Golden test: cartella calcolata da `current.web_url` contro la cartella reale della nota."""
    from famiglia import note_documento
    righe = []
    for rel, d in note_documento():
        if d.get("source") not in ("sharepoint", "onedrive"):
            continue
        web_url = (d.get("current") or {}).get("web_url") or ""
        r = analizza(web_url)
        reale = str(rel.parent)
        righe.append({"nota": str(rel), "web_url": web_url, "calcolata": r["cartella_nota"],
                      "reale": reale, "uguale": r["cartella_nota"] == reale})
    n = len(righe)
    uguali = sum(r["uguale"] for r in righe)
    return {"note": n, "uguali": uguali, "accordo": round(100 * uguali / n, 1) if n else 100.0,
            "disaccordi": [r for r in righe if not r["uguale"]]}


def main(argv):
    as_json = "--json" in argv
    args = [a for a in argv if a != "--json"]
    if len(args) != 1 or args[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    if args[0] == "--verifica":
        r = verifica()
        if as_json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        else:
            print(f"{r['note']} note · cartella uguale {r['uguali']} ({r['accordo']}%)")
            for d in r["disaccordi"]:
                print(f"- {d['nota']}: calcolata {d['calcolata']} ≠ reale {d['reale']} ({d['web_url']})")
        return 0 if r["accordo"] >= 90 else 1
    r = analizza(args[0])
    riconosciuto = r.pop("riconosciuto")
    if as_json:
        print(json.dumps(r, ensure_ascii=False))
    else:
        stato = "dentro" if r["dentro"] else "fuori"
        print(f"{stato} · {r['motivo']}" + (f" · {r['cartella_nota']}" if r["cartella_nota"] else ""))
    if not riconosciuto:
        sys.stderr.write(f"URL non riconosciuto: {r['motivo']}\n")
        return 2
    return 0 if r["dentro"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
