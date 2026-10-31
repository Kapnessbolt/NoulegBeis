#!/usr/bin/env python3
"""Perimetro delle fonti (SPEC 5.1-5.2, agente ingestor §2 e §3.1): dice se il `webUrl` di un
documento di SharePoint o OneDrive è dentro il perimetro e in quale cartella va la sua nota.

Il perimetro è una lista ordinata di prefissi (`posizioni` di `config.perimetro()`, costruita da
`vault.yaml`): una voce per libreria di SharePoint del perimetro, una per la cartella di OneDrive,
poi i riconoscitori fuori perimetro (`<tenant>/sites/`: altro sito o libreria esclusa;
`<tenant>/personal/`: OneDrive fuori dalla cartella). Vince il primo prefisso che apre l'URL; poi
contano le cartelle, il nome del file, le esclusioni e il tipo. Una libreria o una cartella nuova
del perimetro è una voce in più nella lista, non un ramo nuovo nel codice; una fonte di tipo nuovo
aggiunge le sue voci (prefisso, radice, base) e, se ha un riconoscitore fuori perimetro, il suo
motivo in `motivo_fuori`.

Il confronto ignora maiuscole e minuscole e decodifica `%20` (e ogni altro `%xx`); i link di
condivisione `/:x:/r/` valgono come l'URL diretto. Le esclusioni valgono per le cartelle del
percorso, non per il nome del file. Non si vede dall'URL, e resta all'agente, la cartella di un
progetto software (contiene `app.json`, `package.json` o `.git`, es. `/Lab AL/`): se il documento
sta lì, è fuori perimetro anche se questo script dice `dentro`.

Uso:
  python3 .claude/scripts/perimetro.py <webUrl> [--json]
  python3 .claude/scripts/perimetro.py --verifica [--json]
      # golden test sul vault: per ogni nota sharepoint e onedrive, la cartella calcolata da
      # `current.web_url` contro la cartella reale della nota
  python3 .claude/scripts/perimetro.py --profondita <elenco.json> [--json]
      # profondità del rilevatore di riordino «fino alla prima cartella con file» (SPEC 6.2
      # passo 7, 13.1 step 18) per ogni libreria del perimetro e per `OneDrive`

Uscita: 0 se dentro, 1 se fuori, 2 se l'URL non è di SharePoint o OneDrive del tenant.
Con `--json` stampa:
  {"dentro": true|false, "motivo": "...", "fonte": "sharepoint"|"onedrive"|null,
   "libreria": "...", "cartella_nota": "sources/sharepoint/<libreria>/<percorso>"
                                       | "sources/onedrive/<percorso>" | null,
   "tipo_processato": true|false|null}
`cartella_nota` segue ingestor §3.1: segmenti in slug; per OneDrive il percorso parte da dentro
la cartella del vault (`fonti.onedrive.cartella`); per gli altri siti SharePoint (solo compito
`file`) `sources/sharepoint/_<sito>/...`. Per i file di OneDrive fuori da quella cartella è null.

--profondita legge un elenco di file nello stesso formato di `riconcilia.py --elenco` (lista JSON,
o `{"value": [...]}`, di voci con `webUrl` o `web_url`; le voci con `folder` si saltano; gli altri
campi non servono). Conta ogni file dentro un prefisso del perimetro, anche di un tipo non
processato (conta la struttura delle cartelle), tranne i file in cartelle escluse e quelli
direttamente nella radice della libreria o della cartella di OneDrive. La profondità di una
cartella è il numero di cartelle sotto la radice (SharePoint: dopo `<sito>/<libreria>/`;
OneDrive: dopo `<cartella>/`); una cartella è «prima cartella con file» se contiene un file e
nessuna sua antenata ne contiene. Profondità della libreria: la massima tra le sue prime cartelle
con file, da 1 a `PROFONDITA_MASSIMA`. Le librerie senza file nell'elenco restano fuori dal
risultato (in `senza_file`) e `config.py rilevatore` dà loro il default. Testo: una riga
`<libreria>: <n>` per libreria, poi lo snippet `profondita:` da mettere in `vault.yaml` sotto
`fonti.rilevatore`. JSON: {"profondita": {<libreria>: n}, "senza_file": [...], "file": <file
considerati>, "yaml": "<snippet>"}. Uscita 0; 2 se l'elenco non si legge.

Tenant, sito, librerie, cartella di OneDrive, esclusioni e tipi processati sono in `vault.yaml`
(`fonti`).

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
import config  # noqa: E402
import yaml  # noqa: E402  (config.py controlla che PyYAML ci sia)
from famiglia import slug  # noqa: E402

ROOT = Path(os.environ.get("VAULT_ROOT") or Path(__file__).resolve().parents[2]).resolve()

# Perimetro (SPEC 5.1-5.2): tenant, sito, librerie, cartella di OneDrive, esclusioni e tipi
# processati vengono da `vault.yaml` (`fonti`), letti con config.py.
ORDINE_RE = re.compile(r"^\d+[\s_.-]*")  # numero d'ordine davanti al nome: `01_Dati`, `06 Evidenze`
NOMI_FONTE = {"sharepoint": "SharePoint", "onedrive": "OneDrive"}
PROFONDITA_MASSIMA = 6  # tetto della profondità misurata da --profondita


def nome_cartella(segmento):
    return ORDINE_RE.sub("", segmento.strip().lower())


def cartella_esclusa(cartelle, p=None):
    """Motivo dell'esclusione, o None. `cartelle`: segmenti del percorso senza il nome del file."""
    p = p or config.perimetro()
    precedente = ""
    for seg in cartelle:
        basso, nome = seg.strip().lower(), nome_cartella(seg)
        if basso in p["cartelle_escluse"] or nome in p["cartelle_escluse"]:
            return f"cartella esclusa `{seg}`"
        if any(basso.endswith(f) for f in p["finali_esclusi"]):
            return f"cartella esclusa `{seg}` (trascrizioni grezze)"
        for genitore, figlio in p["dentro_escluse"]:
            if precedente.strip().lower().endswith(genitore) and nome == figlio:
                return f"cartella esclusa `{seg}` dentro `{precedente}` (export grezzi)"
        precedente = seg
    return None


# --- Posizione di un URL ----------------------------------------------------------------

def normalizza(web_url):
    """URL senza query e frammento, `%xx` decodificati, link di condivisione `/:x:/r/` tolti."""
    url = unquote(urlsplit(str(web_url).strip())._replace(query="", fragment="").geturl())
    return re.sub(r"/:[a-z]:/[rs]/", "/", url, flags=re.I)


def segmenti(percorso):
    return [x for x in percorso.split("/") if x]


def testa(pos):
    """Segmenti del prefisso sotto la radice (`<sito>/<libreria>`, `<utente>/<libreria>/<cartella>`)."""
    return segmenti(pos["prefisso"][len(pos["radice"]):])


def posizione(url, p):
    """(posizione, parti): la prima posizione il cui prefisso apre l'URL normalizzato (senza
    maiuscole) e i segmenti del percorso sotto la sua radice; (None, []) se nessuna."""
    basso = url.lower()
    pos = next((x for x in p["posizioni"] if basso.startswith(x["prefisso"].lower())), None)
    return pos, ([] if pos is None else segmenti(url[len(pos["radice"]):]))


def cartella_nota(pos, parti, p):
    """Cartella della nota: la base della posizione del perimetro i cui segmenti aprono le
    cartelle dell'URL, più le cartelle sotto, in slug. Per un riconoscitore fuori perimetro con
    `base` (altri siti, librerie escluse) la base più `_<sito>/` se il sito non è quello del
    perimetro, la libreria e le cartelle; senza `base` (OneDrive fuori dalla cartella) null."""
    cartelle = parti[:-1]
    candidate = [pos] if pos["dentro"] else [x for x in p["posizioni"] if x["dentro"] and x["fonte"] == pos["fonte"]]
    for d in candidate:
        t = [s.lower() for s in testa(d)]
        # confronto per segmenti: prende anche gli URL con una doppia barra che il prefisso non apre
        if [s.lower() for s in cartelle[:len(t)]] == t:
            return "/".join([d["base"]] + [slug(c) for c in cartelle[len(t):]])
    if pos["dentro"] or pos["base"] is None:
        return None
    sito, libreria = parti[0], parti[1]
    altro_sito = [] if sito.lower() == p["sito"].lower() else [f"_{slug(sito)}"]
    return "/".join([pos["base"]] + altro_sito + [slug(libreria)] + [slug(c) for c in parti[2:-1]])


def motivo_fuori(pos, parti, p):
    if pos["fonte"] == "sharepoint":
        if parti[0].lower() != p["sito"].lower():
            return f"sito `{parti[0]}` fuori perimetro"
        return f"libreria `{parti[1]}` fuori perimetro"
    return f"OneDrive fuori dalla cartella `{p['onedrive_cartella']}/`"


def analizza(web_url):
    """Dizionario del risultato; `riconosciuto` False se l'URL non è del tenant."""
    p = config.perimetro()
    out = {"dentro": False, "motivo": "", "fonte": None, "libreria": None,
           "cartella_nota": None, "tipo_processato": None, "riconosciuto": True}
    pos, parti = posizione(normalizza(web_url), p)
    if pos is None:
        return {**out, "riconosciuto": False, "motivo": "URL non di SharePoint o OneDrive del tenant"}
    if len(parti) < 3:
        return {**out, "riconosciuto": False,
                "motivo": f"URL di {NOMI_FONTE[pos['fonte']]} senza libreria o file"}
    # parti: <sito>/<libreria>/… per SharePoint, <utente>/<libreria>/… per OneDrive
    cartelle, nome_file = parti[2:-1], parti[-1]
    out.update(fonte=pos["fonte"], libreria=parti[1], cartella_nota=cartella_nota(pos, parti, p))
    estensione = nome_file.rsplit(".", 1)[-1].lower() if "." in nome_file else None
    out["tipo_processato"] = None if estensione is None else estensione in p["tipi"]

    if not pos["dentro"]:
        out["motivo"] = motivo_fuori(pos, parti, p)
        return out
    escluso = cartella_esclusa(cartelle, p)
    if escluso:
        out["motivo"] = escluso
        return out
    if out["tipo_processato"] is False:
        out["motivo"] = f"tipo `.{estensione}` non processato"
        return out
    out["dentro"] = True
    out["motivo"] = f"prefisso `{pos['prefisso']}`"
    return out


# --- Golden test ------------------------------------------------------------------------

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


# --- Profondità del rilevatore ----------------------------------------------------------

class ElencoIlleggibile(Exception):
    pass


def leggi_elenco(percorso):
    """`webUrl` dei file di un elenco nel formato di `riconcilia.py --elenco` (solo la lettura:
    gli altri campi, obbligatori per la riconciliazione, qui non servono)."""
    try:
        dati = json.loads(Path(percorso).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
        raise ElencoIlleggibile(f"`{percorso}` illeggibile: {e}")
    if isinstance(dati, dict) and isinstance(dati.get("value"), list):
        dati = dati["value"]
    if not isinstance(dati, list):
        raise ElencoIlleggibile(f"`{percorso}`: serve una lista JSON di file (o {{\"value\": [...]}})")
    urls = []
    for i, x in enumerate(dati, 1):
        if not isinstance(x, dict):
            raise ElencoIlleggibile(f"`{percorso}`, voce {i}: non è un oggetto JSON")
        if "folder" in x:
            continue
        web_url = str(x.get("webUrl") or x.get("web_url") or "").strip()
        if not web_url:
            raise ElencoIlleggibile(f"`{percorso}`, voce {i}: manca `webUrl`")
        urls.append(web_url)
    return urls


def chiave_rilevatore(pos):
    """Chiave di `fonti.rilevatore.profondita`: la libreria di SharePoint, o `OneDrive`."""
    return pos["libreria"] if pos["fonte"] == "sharepoint" else config.ONEDRIVE_PROFONDITA


def profondita(urls, p=None):
    """Profondità «fino alla prima cartella con file» per libreria (vedi la docstring)."""
    p = p or config.perimetro()
    con_file = {chiave_rilevatore(x): set() for x in p["posizioni"] if x["dentro"]}
    considerati = 0
    for u in urls:
        pos, parti = posizione(normalizza(u), p)
        if pos is None or not pos["dentro"] or len(parti) < 3 or cartella_esclusa(parti[2:-1], p):
            continue
        sotto = parti[len(testa(pos)):-1]
        if not sotto:  # file nella radice della libreria o della cartella di OneDrive
            continue
        considerati += 1
        con_file[chiave_rilevatore(pos)].add(tuple(s.lower() for s in sotto))
    risultato, senza_file = {}, []
    for lib, cartelle in con_file.items():
        prime = [c for c in cartelle if not any(c[:n] in cartelle for n in range(1, len(c)))]
        if not prime:
            senza_file.append(lib)
            continue
        risultato[lib] = max(1, min(PROFONDITA_MASSIMA, max(len(c) for c in prime)))
    snippet = yaml.safe_dump({"profondita": risultato}, sort_keys=False, allow_unicode=True,
                             default_flow_style=False)
    return {"profondita": risultato, "senza_file": senza_file, "file": considerati, "yaml": snippet}


# --- Riga di comando --------------------------------------------------------------------

def main(argv):
    try:
        return comando(argv)
    except config.ConfigErrata as e:
        sys.stderr.write("Configurazione non valida:\n" + "\n".join(f"- {m}" for m in e.errori) + "\n")
        return 2


def comando(argv):
    as_json = "--json" in argv
    args = [a for a in argv if a != "--json"]
    if args and args[0] == "--profondita":
        if len(args) != 2:
            print(__doc__)
            return 2
        try:
            r = profondita(leggi_elenco(args[1]))
        except ElencoIlleggibile as e:
            sys.stderr.write(f"--profondita: elenco {e}\n")
            return 2
        if as_json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        else:
            for lib, n in r["profondita"].items():
                print(f"{lib}: {n}")
            if r["senza_file"]:
                print(f"senza file nell'elenco (default di `config.py rilevatore`): {', '.join(r['senza_file'])}")
            print(f"{r['file']} file considerati")
            print("\n# vault.yaml, sotto `fonti.rilevatore`:")
            print(r["yaml"], end="")
        return 0
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
