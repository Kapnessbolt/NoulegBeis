#!/usr/bin/env python3
"""Stato dell'ingestion (SPEC 6.1): un file per fonte in `.state/`, letto e scritto solo da qui.

File e contenuto:
  .state/sharepoint.json  {"watermark": ..., "items": {"<driveId>/<itemId>": {"last_modified", "note"}}}
  .state/onedrive.json    come sharepoint
  .state/outlook.json     {"watermark": ..., "threads": {"<conversationId>": {"last_message", "note"}}}
  .state/github.json      {"repos": {"<owner>/<repo>": {"commit", "watermark"}},
                           "items": {"<owner>/<repo>:<percorso>": {"last_modified", "commit", "note"},
                                     "<owner>/<repo>#<numero>": {"last_modified", "note"}}}
  .state/reconcile.json   {"last_run": ...}

Uso (fonte: sharepoint | onedrive | outlook | github | reconcile):
  stato.py migra <file>                           divide il vecchio file unico dello stato (SPEC
                                                  fino alla 1.18, una chiave per fonte) nei file
                                                  per fonte e lo cancella; una volta sola
  stato.py watermark <fonte>                      stampa il watermark; esce con 1 se è null
  stato.py last-run                               stampa reconcile.last_run; 1 se è null
  stato.py item <fonte> <chiave>                  JSON della voce; esce con 1 se manca
  stato.py repo <owner/repo>                      JSON del repo in github.repos; 1 se manca
  stato.py elenco <fonte>                         JSON di tutte le voci (items o threads)
  stato.py set-item <fonte> <chiave> --istante <ISO UTC> [--note sources/...] [--commit <sha>]
      --istante vale anche come --last-modified o --last-message: lo script scrive il campo
      giusto per la fonte (last_message per outlook, last_modified per le altre). --note serve
      solo per una voce nuova; --commit solo per github
  stato.py set-watermark <fonte> <ISO UTC> [--forza]
      non abbassa mai il watermark: se il nuovo è più vecchio esce con 0 e un avviso, a meno
      di --forza
  stato.py set-repo <owner/repo> --commit <sha> --watermark <ISO UTC> [--forza]
      stessa regola: un watermark più vecchio non sostituisce quello registrato
  stato.py set-last-run <ISO UTC>                 reconcile.last_run
  stato.py merge-driver <base> <nostro> <loro>    merge driver di git per .state/*.json
                                                  (.gitattributes: `merge=stato`)
  stato.py risolvi [<file> ...]                   risolve a mano un conflitto rimasto su
                                                  .state/*.json (dagli stadi dell'indice), poi
                                                  `git add`; senza file, tutti quelli in conflitto

Opzione comune: --json per le risposte dei comandi di scrittura.

Regole: istanti nel formato AAAA-MM-GGTHH:MM:SSZ (errore altrimenti); --note è un percorso
relativo dentro sources/ (avviso se il file non esiste ancora: l'agente può scrivere la nota
dopo). Scrittura atomica (file temporaneo e rename), JSON con indentazione 2 e chiavi ordinate.
Le voci non si cancellano mai (SPEC 6.4): una nota rimossa ha `status: removed`, la voce resta.

Merge driver: il watermark (e last_run) più avanzato vince; items, threads e repos si uniscono
e per la stessa chiave vince l'istante più recente (per i repo il watermark); a parità vince il
lato che ha cambiato la voce rispetto alla base. Scrive il risultato in <nostro> ed esce con 0;
con un file illeggibile esce con 1 e git lascia il conflitto.

La variabile d'ambiente VAULT_ROOT, se presente, indica la radice del vault al posto della
cartella che contiene `.claude/` (serve ai test in `.claude/scripts/tests/`).
"""

import datetime as dt
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(os.environ.get("VAULT_ROOT") or Path(__file__).resolve().parents[2]).resolve()
STATE = ROOT / ".state"

# Struttura vuota di ogni fonte
FONTI = {
    "sharepoint": {"watermark": None, "items": {}},
    "onedrive": {"watermark": None, "items": {}},
    "outlook": {"watermark": None, "threads": {}},
    "github": {"repos": {}, "items": {}},
    "reconcile": {"last_run": None},
}
COLLEZIONE = {"sharepoint": "items", "onedrive": "items", "outlook": "threads", "github": "items"}
CAMPO_ISTANTE = {"sharepoint": "last_modified", "onedrive": "last_modified",
                 "outlook": "last_message", "github": "last_modified"}
ISTANTE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
COMMIT_RE = re.compile(r"^[0-9a-f]{7,40}$")
REPO_RE = re.compile(r"^[\w.-]+/[\w.-]+$")


class Errore(Exception):
    pass


def avviso(msg):
    sys.stderr.write(f"avviso: {msg}\n")


# --- Lettura e scrittura ----------------------------------------------------------------

def percorso(fonte):
    return STATE / f"{fonte}.json"


def controlla_fonte(fonte, ammesse=FONTI):
    if fonte not in ammesse:
        raise Errore(f"fonte sconosciuta `{fonte}` (ammesse: {', '.join(ammesse)})")


def leggi(fonte):
    """Contenuto del file della fonte; la struttura vuota se il file non c'è ancora."""
    controlla_fonte(fonte)
    p = percorso(fonte)
    if not p.exists():
        return json.loads(json.dumps(FONTI[fonte]))
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise Errore(f"{p.relative_to(ROOT)} illeggibile: {e}")
    for k, v in FONTI[fonte].items():
        data.setdefault(k, json.loads(json.dumps(v)))
    return data


def serializza(data):
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _umask():
    attuale = os.umask(0)
    os.umask(attuale)
    return attuale


def scrivi_atomico(p, testo):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{p.name}.", suffix=".tmp", dir=p.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(testo)
        os.chmod(tmp, p.stat().st_mode & 0o777 if p.exists() else 0o666 & ~_umask())
        os.replace(tmp, p)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def scrivi(fonte, data):
    scrivi_atomico(percorso(fonte), serializza(data))


# --- Validazione ------------------------------------------------------------------------

def istante(valore, nome="istante"):
    if not isinstance(valore, str) or not ISTANTE_RE.match(valore):
        raise Errore(f"{nome} `{valore}` non è nel formato AAAA-MM-GGTHH:MM:SSZ (UTC, senza millisecondi)")
    try:
        dt.datetime.strptime(valore, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        raise Errore(f"{nome} `{valore}` non è una data valida")
    return valore


def nota(valore):
    v = str(valore)
    p = Path(v)
    if p.is_absolute() or ".." in p.parts or not p.parts or p.parts[0] != "sources" or p.suffix != ".md":
        raise Errore(f"--note `{v}` deve essere un percorso relativo dentro sources/ che finisce con .md")
    if not (ROOT / p).is_file():
        avviso(f"la nota `{v}` non esiste ancora: scrivila prima del commit")
    return v


def commit(valore):
    if not COMMIT_RE.match(str(valore)):
        raise Errore(f"commit `{valore}` non valido (sha esadecimale minuscolo, da 7 a 40 caratteri)")
    return str(valore)


def repo_valido(valore):
    if not REPO_RE.match(str(valore)):
        raise Errore(f"repo `{valore}` non è nella forma owner/repo")
    return str(valore)


def piu_recente(a, b):
    """True se l'istante a è più avanzato di b (None è il più vecchio)."""
    if a is None or a == "":
        return False
    if b is None or b == "":
        return True
    return a > b  # stesso formato ISO UTC: l'ordine delle stringhe è quello del tempo


# --- Comandi ----------------------------------------------------------------------------

def migra(file_vecchio):
    vecchio_p = Path(file_vecchio)
    if not vecchio_p.is_absolute():
        vecchio_p = ROOT / vecchio_p
    if not vecchio_p.is_file():
        raise Errore(f"`{file_vecchio}` non c'è: migrazione già fatta?")
    esistenti = [f for f in FONTI if percorso(f).exists()]
    if esistenti:
        raise Errore("esistono già " + ", ".join(f".state/{f}.json" for f in esistenti))
    vecchio = json.loads(vecchio_p.read_text(encoding="utf-8"))
    sconosciute = set(vecchio) - set(FONTI)
    if sconosciute:
        raise Errore(f"chiavi sconosciute in `{file_vecchio}`: {', '.join(sorted(sconosciute))}")
    for fonte, vuoto in FONTI.items():
        data = vecchio.get(fonte) or json.loads(json.dumps(vuoto))
        for k, v in vuoto.items():
            data.setdefault(k, v)
        scrivi(fonte, data)
    vecchio_p.unlink()
    return {f: str(percorso(f).relative_to(ROOT)) for f in FONTI}


def cmd_watermark(fonte):
    controlla_fonte(fonte, ("sharepoint", "onedrive", "outlook"))
    return leggi(fonte).get("watermark")


def cmd_item(fonte, chiave):
    controlla_fonte(fonte, COLLEZIONE)
    return leggi(fonte)[COLLEZIONE[fonte]].get(chiave)


def cmd_set_item(fonte, chiave, ist, note=None, sha=None):
    controlla_fonte(fonte, COLLEZIONE)
    istante(ist)
    if sha is not None:
        if fonte != "github":
            raise Errore("--commit vale solo per la fonte github")
        commit(sha)
    data = leggi(fonte)
    coll = data[COLLEZIONE[fonte]]
    voce = dict(coll.get(chiave) or {})
    if note is None and "note" not in voce:
        raise Errore(f"voce nuova `{chiave}`: serve --note")
    campo = CAMPO_ISTANTE[fonte]
    if piu_recente(voce.get(campo), ist):
        avviso(f"`{chiave}`: {campo} {ist} è più vecchio di quello registrato ({voce.get(campo)})")
    voce[campo] = ist
    if note is not None:
        voce["note"] = nota(note)
    if sha is not None:
        voce["commit"] = sha
    coll[chiave] = voce
    scrivi(fonte, data)
    return voce


def cmd_set_watermark(fonte, ist, forza=False):
    controlla_fonte(fonte, ("sharepoint", "onedrive", "outlook"))
    istante(ist)
    data = leggi(fonte)
    attuale = data.get("watermark")
    if piu_recente(attuale, ist) and not forza:
        avviso(f"watermark di {fonte} non abbassato: {ist} è più vecchio di {attuale} (--forza per abbassarlo)")
        return {"fonte": fonte, "watermark": attuale, "cambiato": False}
    cambiato = attuale != ist
    if cambiato:
        data["watermark"] = ist
        scrivi(fonte, data)
    return {"fonte": fonte, "watermark": ist, "cambiato": cambiato}


def cmd_set_repo(repo, sha, wm, forza=False):
    repo_valido(repo)
    commit(sha)
    istante(wm, "watermark")
    data = leggi("github")
    attuale = data["repos"].get(repo) or {}
    if piu_recente(attuale.get("watermark"), wm) and not forza:
        avviso(f"repo {repo} non aggiornato: {wm} è più vecchio di {attuale.get('watermark')} (--forza)")
        return {"repo": repo, **attuale, "cambiato": False}
    nuovo = {"commit": sha, "watermark": wm}
    cambiato = nuovo != attuale
    if cambiato:
        data["repos"][repo] = nuovo
        scrivi("github", data)
    return {"repo": repo, **nuovo, "cambiato": cambiato}


def cmd_set_last_run(ist):
    istante(ist)
    data = leggi("reconcile")
    data["last_run"] = ist
    scrivi("reconcile", data)
    return data


# --- Merge driver -----------------------------------------------------------------------

def _istante_voce(voce, campi=("last_modified", "last_message", "watermark")):
    if not isinstance(voce, dict):
        return None
    for c in campi:
        if voce.get(c):
            return voce[c]
    return None


def _scegli(base, nostro, loro, chiave_istante):
    """Voce da tenere tra due versioni della stessa chiave."""
    if nostro == loro:
        return nostro
    a, b = chiave_istante(nostro), chiave_istante(loro)
    if piu_recente(a, b):
        return nostro
    if piu_recente(b, a):
        return loro
    # Stesso istante: vince il lato che ha cambiato la voce rispetto alla base
    if nostro == base:
        return loro
    return nostro


def unisci(base, nostro, loro):
    """Unione a tre vie del contenuto di un file di stato."""
    base = base if isinstance(base, dict) else {}
    out = {}
    for k in sorted(set(nostro) | set(loro)):
        if k not in loro:
            out[k] = nostro[k]
        elif k not in nostro:
            out[k] = loro[k]
        elif k in ("watermark", "last_run"):
            out[k] = nostro[k] if not piu_recente(loro[k], nostro[k]) else loro[k]
        elif k in ("items", "threads", "repos") and isinstance(nostro[k], dict) and isinstance(loro[k], dict):
            b = base.get(k) if isinstance(base.get(k), dict) else {}
            campi = ("watermark",) if k == "repos" else ("last_modified", "last_message")
            coll = {}
            for chiave in sorted(set(nostro[k]) | set(loro[k])):
                if chiave not in loro[k]:
                    coll[chiave] = nostro[k][chiave]
                elif chiave not in nostro[k]:
                    coll[chiave] = loro[k][chiave]
                else:
                    coll[chiave] = _scegli(b.get(chiave), nostro[k][chiave], loro[k][chiave],
                                           lambda v: _istante_voce(v, campi))
            out[k] = coll
        else:
            out[k] = _scegli(base.get(k), nostro[k], loro[k], lambda v: None)
    return out


def _carica(p):
    testo = Path(p).read_text(encoding="utf-8")
    return json.loads(testo) if testo.strip() else {}


def merge_driver(base, nostro, loro):
    try:
        b, n, l = _carica(base), _carica(nostro), _carica(loro)
    except (OSError, json.JSONDecodeError) as e:
        raise Errore(f"merge-driver: file di stato illeggibile ({e}): conflitto lasciato a git")
    scrivi_atomico(nostro, serializza(unisci(b, n, l)))


def git_out(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=False)


def risolvi(files):
    if not files:
        out = git_out("diff", "--name-only", "--diff-filter=U").stdout.split()
        files = [f for f in out if f.startswith(".state/") and f.endswith(".json")]
    if not files:
        raise Errore("nessun conflitto su .state/*.json")
    risolti = []
    for f in files:
        stadi = []
        for n in (1, 2, 3):
            r = git_out("show", f":{n}:{f}")
            stadi.append(r.stdout if r.returncode == 0 else "")
        with tempfile.TemporaryDirectory() as tmp:
            nomi = [Path(tmp) / x for x in ("base", "nostro", "loro")]
            for p, testo in zip(nomi, stadi):
                p.write_text(testo, encoding="utf-8")
            merge_driver(*nomi)
            scrivi_atomico(ROOT / f, nomi[1].read_text(encoding="utf-8"))
        git_out("add", "--", f)
        risolti.append(f)
    return risolti


# --- Riga di comando --------------------------------------------------------------------

def opzioni(args, nomi_valore, flag=()):
    """Separa le opzioni `--nome valore` e i flag dagli argomenti posizionali."""
    pos, opt = [], {}
    i = 0
    while i < len(args):
        a = args[i]
        if a in flag:
            opt[a] = True
        elif a in nomi_valore:
            if i + 1 >= len(args):
                raise Errore(f"{a} vuole un valore")
            opt[a] = args[i + 1]
            i += 1
        elif a.startswith("--"):
            raise Errore(f"opzione sconosciuta: {a}")
        else:
            pos.append(a)
        i += 1
    return pos, opt


def stampa(valore, as_json=True):
    print(json.dumps(valore, ensure_ascii=False, indent=2, sort_keys=True) if as_json else valore)


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if argv else 2
    cmd, args = argv[0], argv[1:]
    as_json = "--json" in args
    args = [a for a in args if a != "--json"]

    def posizionali(pos, n, uso):
        if len(pos) != n:
            raise Errore(f"uso: stato.py {uso}")
        return pos

    if cmd == "migra":
        (file_vecchio,) = posizionali(args, 1, "migra <file del vecchio stato>")
        stampa(migra(file_vecchio))
        return 0
    if cmd == "watermark":
        (fonte,) = posizionali(args, 1, "watermark <fonte>")
        wm = cmd_watermark(fonte)
        stampa({"fonte": fonte, "watermark": wm} if as_json else (wm or "null"), as_json)
        if not wm:
            sys.stderr.write(f"watermark di {fonte} null: serve il primo caricamento (SPEC 6.5)\n")
            return 1
        return 0
    if cmd == "last-run":
        posizionali(args, 0, "last-run")
        lr = leggi("reconcile").get("last_run")
        stampa({"last_run": lr} if as_json else (lr or "null"), as_json)
        return 0 if lr else 1
    if cmd == "item":
        fonte, chiave = posizionali(args, 2, "item <fonte> <chiave>")
        voce = cmd_item(fonte, chiave)
        if voce is None:
            sys.stderr.write(f"nessuna voce `{chiave}` in .state/{fonte}.json\n")
            return 1
        stampa(voce)
        return 0
    if cmd == "repo":
        (repo,) = posizionali(args, 1, "repo <owner/repo>")
        voce = leggi("github")["repos"].get(repo)
        if voce is None:
            sys.stderr.write(f"nessun repo `{repo}` in .state/github.json: serve il primo caricamento\n")
            return 1
        stampa(voce)
        return 0
    if cmd == "elenco":
        (fonte,) = posizionali(args, 1, "elenco <fonte>")
        controlla_fonte(fonte, COLLEZIONE)
        stampa(leggi(fonte)[COLLEZIONE[fonte]])
        return 0
    if cmd == "set-item":
        nomi = ("--istante", "--last-modified", "--last-message", "--note", "--commit")
        pos, opt = opzioni(args, nomi)
        fonte, chiave = posizionali(pos, 2, "set-item <fonte> <chiave> --istante <ISO> [--note ...] [--commit ...]")
        istanti = [opt[n] for n in ("--istante", "--last-modified", "--last-message") if n in opt]
        if len(istanti) != 1:
            raise Errore("serve uno e uno solo tra --istante, --last-modified, --last-message")
        voce = cmd_set_item(fonte, chiave, istanti[0], opt.get("--note"), opt.get("--commit"))
        stampa({"fonte": fonte, "chiave": chiave, **voce} if as_json else f"{fonte} `{chiave}` aggiornata", as_json)
        return 0
    if cmd == "set-watermark":
        pos, opt = opzioni(args, (), ("--forza",))
        fonte, ist = posizionali(pos, 2, "set-watermark <fonte> <ISO UTC> [--forza]")
        r = cmd_set_watermark(fonte, ist, "--forza" in opt)
        stampa(r if as_json else f"watermark {fonte}: {r['watermark']}", as_json)
        return 0
    if cmd == "set-repo":
        pos, opt = opzioni(args, ("--commit", "--watermark"), ("--forza",))
        (repo,) = posizionali(pos, 1, "set-repo <owner/repo> --commit <sha> --watermark <ISO UTC>")
        if "--commit" not in opt or "--watermark" not in opt:
            raise Errore("set-repo vuole --commit e --watermark")
        r = cmd_set_repo(repo, opt["--commit"], opt["--watermark"], "--forza" in opt)
        stampa(r if as_json else f"repo {repo}: {r.get('commit')} {r.get('watermark')}", as_json)
        return 0
    if cmd == "set-last-run":
        (ist,) = posizionali(args, 1, "set-last-run <ISO UTC>")
        r = cmd_set_last_run(ist)
        stampa(r if as_json else f"reconcile.last_run: {ist}", as_json)
        return 0
    if cmd == "merge-driver":
        base, nostro, loro = posizionali(args, 3, "merge-driver <base> <nostro> <loro>")
        merge_driver(base, nostro, loro)
        return 0
    if cmd == "risolvi":
        risolti = risolvi(args)
        stampa(risolti if as_json else "risolti: " + ", ".join(risolti), as_json)
        return 0
    raise Errore(f"comando sconosciuto `{cmd}` (stato.py --help)")


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Errore as e:
        sys.stderr.write(f"errore: {e}\n")
        sys.exit(2)
