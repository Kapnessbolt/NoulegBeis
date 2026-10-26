#!/usr/bin/env python3
"""Aggiorna il frontmatter di una nota esistente senza toccare il corpo (SPEC 4.2-4.3,
agente ingestor §3.4-3.6).

Uso:
  python3 .claude/scripts/aggiorna-nota.py <percorso> [--campo chiave=valore ...]
          [--aggiungi lista=valore ...] [--also-at web_url=... item_id=...]
          [--nuova-versione --campo current.name=... --campo current.item_id=...
           --campo current.last_modified=... [--campo current.uri=... --campo current.web_url=...]]
          [--json]

- `--campo chiave=valore`: imposta un campo (anche `current.<sotto>`), valore in YAML come in
  `nuova-nota.py` (es. `--campo last_message=2026-10-21T19:35:37Z --campo messages=3`).
- `--aggiungi lista=valore`: aggiunge a una lista se manca (`participants`, `projects`,
  `clients`, `topics`, `attachments`, `tags`...); il valore può essere `[[slug]]`, `"[[slug]]"`
  o una lista `[a, b]`.
- `--also-at web_url=... item_id=...`: aggiunge una posizione in `also_at` se nessuna voce ha
  già lo stesso `item_id` o lo stesso `web_url`.
- `--nuova-versione` (source-doc, ingestor §3.5 passo 1): la `current` attuale entra in testa a
  `versions` se non c'è già una voce con lo stesso `item_id` e `last_modified`, poi i `--campo
  current.*` passati diventano la nuova `current` (quelli non passati restano), che entra a sua
  volta in testa a `versions` (lo schema 4.2 tiene la corrente come prima voce). `ingested_at`
  diventa l'istante attuale UTC, se non lo passi. Per GitHub il nome in `versions` porta il
  commit abbreviato preso da `current.uri`.

Le righe dei campi che non cambiano restano identiche; i campi cambiati si scrivono nello stile
delle note reali (liste inline, `versions` come mappe inline). Il risultato si valida contro il
template come in `nuova-nota.py`: se non è valido esce con 2 e la nota resta com'era. Senza
modifiche effettive la nota non si riscrive.

La variabile d'ambiente VAULT_ROOT, se presente, indica la radice del vault al posto della
cartella che contiene `.claude/` (serve ai test in `.claude/scripts/tests/`).
"""

import copy
import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import nota  # noqa: E402


def voce_versione(data):
    cur = data.get("current") or {}
    nome = cur.get("name") or ""
    if data.get("source") == "github":
        m = re.search(r"@([0-9a-f]{7,40})$", str(cur.get("uri") or ""))
        if m and "@" not in nome:
            nome = f"{nome}@{m.group(1)[:7]}"
    return {"name": nome, "item_id": cur.get("item_id") or "", "last_modified": cur.get("last_modified")}


def stessa_versione(a, b):
    return (str(a.get("item_id") or "") == str(b.get("item_id") or "")
            and nota.normale(a.get("last_modified")) == nota.normale(b.get("last_modified")))


def aggiorna(rel, campi, aggiunte, also_at, nuova_versione):
    p = nota.ROOT / rel
    if not p.is_file():
        raise nota.Errore(f"la nota `{rel}` non esiste: usa nuova-nota.py")
    testo = p.read_text(encoding="utf-8")
    fm, resto = nota.dividi(testo)
    try:
        vecchio = yaml.safe_load(fm) or {}
    except yaml.YAMLError as e:
        raise nota.Errore(f"frontmatter non valido ({str(e).splitlines()[0]})")
    sch = nota.schema(vecchio.get("type"))
    nuovo = copy.deepcopy(vecchio)
    gia_extra = set(vecchio) - set(sch["default"])

    if nuova_versione:
        if sch["tipo"] != "source-doc":
            raise nota.Errore("--nuova-versione vale solo per le note source-doc")
        chiavi = {nota.campo(c)[0] for c in campi}
        manca = [k for k in ("current.name", "current.item_id", "current.last_modified") if k not in chiavi]
        if manca:
            raise nota.Errore(f"--nuova-versione vuole anche --campo {', --campo '.join(manca)}")
        versioni = list(nuovo.get("versions") or [])
        vecchia = voce_versione(nuovo)
        if not any(stessa_versione(v, vecchia) for v in versioni if isinstance(v, dict)):
            versioni.insert(0, vecchia)
        nuovo["versions"] = versioni

    for arg in campi:
        k, v = nota.campo(arg)
        nota.imposta(nuovo, sch, k, v)

    if nuova_versione:
        recente = voce_versione(nuovo)
        versioni = [v for v in nuovo["versions"] if not (isinstance(v, dict) and stessa_versione(v, recente))]
        nuovo["versions"] = [recente] + versioni
        if "ingested_at" not in {nota.campo(c)[0] for c in campi}:
            nuovo["ingested_at"] = nota.adesso()

    for arg in aggiunte:
        k, v = nota.campo(arg)
        if not isinstance(sch["default"].get(k), list) or k in nota.LISTE_DI_MAPPE:
            raise nota.Errore(f"--aggiungi vale per i campi lista del template, non per `{k}`")
        lista = list(nuovo.get(k) or [])
        for x in nota.interpreta(v, k, []):
            if x not in lista:
                lista.append(x)
        nuovo[k] = lista

    if also_at:
        if "also_at" not in sch["default"]:
            raise nota.Errore("--also-at vale solo per le note source-doc")
        voce = {"web_url": also_at.get("web_url", ""), "item_id": also_at.get("item_id", "")}
        lista = list(nuovo.get("also_at") or [])
        doppia = any(isinstance(x, dict) and ((voce["item_id"] and str(x.get("item_id")) == voce["item_id"])
                                              or x.get("web_url") == voce["web_url"]) for x in lista)
        if not doppia:
            lista.append(voce)
        nuovo["also_at"] = lista

    errori, avvisi = nota.valida(nuovo, sch, extra_ammesse=gia_extra)
    if nuova_versione:
        prima, dopo = vecchio.get("current") or {}, nuovo.get("current") or {}
        for k in ("uri", "web_url"):
            if prima.get("item_id") != dopo.get("item_id") and prima.get(k) == dopo.get(k) and dopo.get(k):
                avvisi.append(f"current.{k} è rimasto quello della versione precedente: passalo con --campo")
    if errori:
        raise nota.Errore("frontmatter non valido: " + "; ".join(errori))
    cambiati = [k for k in nuovo if nota.normale(nuovo.get(k)) != nota.normale(vecchio.get(k))]
    if cambiati:
        nota.scrivi_atomico(p, nota.unisci(nota.riscrivi_frontmatter(fm, vecchio, nuovo), resto))
    return cambiati, avvisi


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if argv else 2
    rel = argv[0]
    campi, aggiunte, also_at = [], [], {}
    nuova_versione = as_json = False
    i = 1
    while i < len(argv):
        a = argv[i]
        if a == "--json":
            as_json = True
        elif a == "--nuova-versione":
            nuova_versione = True
        elif a in ("--campo", "--aggiungi"):
            if i + 1 >= len(argv):
                raise nota.Errore(f"{a} vuole chiave=valore")
            (campi if a == "--campo" else aggiunte).append(argv[i + 1])
            i += 1
        elif a == "--also-at":
            while i + 1 < len(argv) and re.match(r"^(web_url|item_id)=", argv[i + 1]):
                k, v = nota.campo(argv[i + 1])
                also_at[k] = v
                i += 1
            if "web_url" not in also_at:
                raise nota.Errore("--also-at vuole almeno web_url=...")
        else:
            raise nota.Errore(f"argomento non riconosciuto: {a}")
        i += 1
    if not (campi or aggiunte or also_at or nuova_versione):
        raise nota.Errore("niente da fare: passa --campo, --aggiungi, --also-at o --nuova-versione")
    cambiati, avvisi = aggiorna(rel, campi, aggiunte, also_at, nuova_versione)
    for a in avvisi:
        sys.stderr.write(f"avviso: {a}\n")
    if as_json:
        print(json.dumps({"nota": rel, "cambiati": cambiati, "avvisi": avvisi}, ensure_ascii=False))
    else:
        print(f"{rel}: " + (", ".join(cambiati) if cambiati else "nessuna modifica"))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except nota.Errore as e:
        sys.stderr.write(f"errore: {e}\n")
        sys.exit(2)
