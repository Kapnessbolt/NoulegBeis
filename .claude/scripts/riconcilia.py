#!/usr/bin/env python3
"""Piano di riconciliazione (SPEC 6.4, audit del 31/10 P3): confronta l'elenco delle cartelle letto
dal connettore con lo stato (`.state/<fonte>.json`) e con le note, e stampa il piano in JSON; con
`--applica` ne esegue la parte meccanica con `sposta-nota.py`, `aggiorna-nota.py` e `stato.py`.
Il codice fa la meccanica e la regola dell'identità; all'agente restano la lettura dal connettore,
le voci `recupera` e i riassunti.

Uso:
  python3 .claude/scripts/riconcilia.py --elenco <file.json> --fonte <sharepoint | onedrive>
          [--libreria <nome>] [--piano <file.json>] [--applica [--solo <id,id,...>]] [--json]

--elenco   lista JSON dei file (l'agente la scrive dal `read_resource` ricorsivo delle cartelle del
           perimetro, saltando le escluse). Per ogni file: `id` (itemId), `driveId` (o
           `parentReference.driveId`), `webUrl`, `name`, `lastModifiedDateTime`; valgono anche
           `chiave` (`<driveId>/<itemId>`), `uri` (`file:///<driveId>/<itemId>`), `web_url`,
           `last_modified`. Anche `{"value": [...]}`. Le voci con `folder` (cartelle) si saltano.
           Istanti normalizzati a AAAA-MM-GGTHH:MM:SSZ (millisecondi tolti, fuso convertito in UTC).
--fonte    sharepoint o onedrive.
--libreria (solo sharepoint) una libreria del perimetro: si considerano solo i file di quella
           libreria e, per le assenze, solo le note la cui `current` sta in quella libreria.
           Senza, tutte le librerie del perimetro (o la cartella di OneDrive).
--piano    scrive il piano (o, con --applica, il risultato) anche in questo file. Con --applica, se
           il file c'è già e contiene il piano dello stesso elenco (stessa `impronta`: elenco,
           fonte, libreria e vault) scritto da meno di 24 ore, si riprende quel piano invece di
           ricalcolarlo: così ripetere un'applica interrotta non conta due volte la stessa assenza.
           Il file si scrive prima di applicare, poi con gli esiti.
--applica  esegue le voci nell'ordine sposta, copia, nuova_voce, in_attesa, rimuovi, azzera, in modo
           idempotente (prima di ogni passo guarda lo stato attuale: ciò che è fatto si salta con
           `già fatto`). Un errore su una voce non ferma le altre. Non tocca mai `watermark`,
           `riconciliazione_dovuta` (la chiude la routine con `stato.py set-riconciliata`) né
           `reconcile.last_run`.
--solo     con --applica, solo le voci con questi `id` (le altre restano senza esito).

Regola per ogni file dell'elenco (chiave `<driveId>/<itemId>`):
- URL non del tenant, di un'altra fonte, di un'altra libreria (con --libreria), fuori perimetro o
  di un tipo non processato: in `ignorati` con il motivo. Eccezione: un file di un altro sito del
  tenant (`sources/sharepoint/_<sito>/`, rango `sharepoint:*`), non in una cartella esclusa e di
  un tipo processato, conta come posizione di una nota che c'è già (copia, chiave nota) ma non si
  recupera mai: senza candidati resta in `ignorati` (si ingerisce a richiesta con /ingest-file).
- Chiave nota allo stato. Se l'ID è la `current` della nota (o la sola voce della nota, quando
  nessuna voce ha l'ID di `current`): `sposta` se `webUrl` o nome sono cambiati, se la nota non
  sta nella cartella che perimetro.py calcola dal file, o se la nota è `removed` (`ripristina`);
  in più `recupera` con `aggiorna: true` (o `in_coda`, se più recente del watermark) se il
  `lastModifiedDateTime` è più recente di quello registrato. Se l'ID è in `also_at` con un
  `webUrl` diverso: `copia` con `aggiorna: true`. ID in `versions` o in nessun campo della nota:
  niente (conta in `ok`).
- Chiave nuova: candidati con `stato.trova(fonte, nome=<name>, cartella=<cartella della nota>)`
  su tutta la fonte (stesso nome o stessa famiglia, SPEC 6.4). Scelta del candidato, prima tra
  quelli della stessa cartella e, se non ce ne sono, tra gli altri (già ordinati: stessa libreria,
  poi le altre): l'unico con lo stesso nome; se nessuno ha lo stesso nome, l'unico candidato. Più
  candidati con lo stesso nome, o più candidati per sola famiglia e nessuno con lo stesso nome: il
  piano non sceglie (nel vault reale due note diverse in cartelle diverse hanno la famiglia
  `00-leggimi`) e la voce è `recupera` o `in_coda` con `candidati_ambigui`: decide l'agente.
  - candidato nella stessa cartella → `nuova_voce` (ricaricamento o versione con un nome nuovo).
    Tra le voci nuove della stessa nota e la `current` (se il suo file è nell'elenco, o se la sua
    posizione non è coperta dall'elenco) diventa `current` quella con il `last_modified` più
    recente, a parità la `current` attuale, poi lo stesso nome: `diventa_current: true` (applica:
    `aggiorna-nota.py --nuova-versione`, `ingested_at` invariato se `rileggi` è false); le altre
    entrano in `versions` nell'ordine delle date. `rileggi: true` se `last_modified` o nome sono
    diversi dalla `current`: l'agente rigenera il riassunto.
  - candidato in un'altra cartella → `copia`. Con `config.rango_canonico` delle due posizioni (un
    altro sito vale `sharepoint:*`) la copia nuova `diventa_current` se ha rango più basso (vince),
    oppure se il file della `current` manca da un elenco che lo copriva (il documento si è
    spostato con un ID nuovo); a pari rango resta la `current`. Una sola copia per nota diventa
    `current` (la migliore per rango), e nessuna se la nota ha già una `nuova_voce` che diventa
    `current`. Applica: `sposta-nota.py` con `--item-id --uri --last-modified`, poi la vecchia
    `current` in `also_at` (`vecchia_current.dove: also_at`) o, se il suo file non c'è più, di
    nuovo in `versions` (`dove: versions`). Altrimenti `also_at` nuova + `stato.py collega`.
  - nessun candidato → `recupera` se `last_modified` ≤ watermark (o watermark null): file mai
    ingerito che il watermark ha superato, lo ingerisce l'agente come compito `file`;
    `in_coda` se più recente (lo prende il delta).
- Nota attiva (non `fuori-perimetro`, con la `current` in una posizione coperta dall'elenco)
  nessuna delle cui voci è nell'elenco e che nessuna `nuova_voce` o `copia` ritrova: `in_attesa`
  se `assente` della sua voce corrente è 0 (prima riconciliazione che non la trova,
  `assente_dopo: 1`), altrimenti `rimuovi` (`assente_dopo: n+1`, `status: removed`). Le note
  `removed` non producono nulla. Una nota ritrovata con `assente` su qualche voce: `azzera`.

Piano (JSON): {"fonte", "libreria", "watermark", "elenco": <n file>, "ignorati": [{"web_url",
"nome", "chiave", "motivo", ["nota"], ["candidati_ambigui"]}], "riepilogo": {<tipo>: n, "ok": n},
"impronta", "creato", "voci": [...]}. Ogni voce ha `id` (progressivo), `tipo` e:
  sposta      nota, chiave, web_url, web_url_prima, nome, cartella_nuova, cambia_cartella,
              cambia_famiglia, ripristina
  copia       nota, chiave, chiave_corrente, web_url, nome, last_modified, aggiorna, diventa_current,
              rango_nuovo, rango_corrente, cartella_nuova, rileggi, ripristina, motivo, uri,
              [web_url_prima con aggiorna], [vecchia_current {web_url, item_id, name,
              last_modified, dove} con diventa_current]
  nuova_voce  nota, chiave, chiave_corrente, web_url, nome, last_modified, uri, diventa_current,
              rileggi, ripristina, motivo
  recupera    nota (null per un file mai ingerito), chiave, web_url, nome, last_modified,
  in_coda     cartella_nota, aggiorna, [last_modified_stato], [candidati_ambigui]
  in_attesa   nota, chiave (la voce di cui si conta l'assenza), chiavi, assente_attuale,
  rimuovi     assente_dopo, motivo
  azzera      nota, chiavi (le voci con `assente` da togliere)
Ordine: sposta, copia, nuova_voce, in_attesa, rimuovi, azzera, recupera, in_coda, poi per nota.
Con --applica ogni voce eseguita ha `esito`: `fatto`, `già fatto`, `errore` (con `messaggio`) o
`all'agente` (recupera, in_coda; sposta e copia con `diventa_current` riportano `nota_dopo`); il
risultato ha anche `applicato: true`, `ripreso` (piano ripreso da --piano) ed `esiti`: {esito: n}.
`azzera` è una voce in più rispetto al contratto P3: rende visibile lo `stato.py set-assente
--azzera` delle note ritrovate.

Uscita: 0 piano stampato, o applicato senza errori; 1 almeno una voce in errore nell'applica; 2
errori d'uso, elenco illeggibile, fonte o libreria sconosciuta.

La variabile d'ambiente VAULT_ROOT, se presente, indica la radice del vault al posto della
cartella che contiene `.claude/` (serve ai test in `.claude/scripts/tests/`): gli script chiamati
la ereditano.
"""

import collections
import copy
import datetime as dt
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

QUI = Path(__file__).resolve().parent
sys.path.insert(0, str(QUI))
import config  # noqa: E402
import famiglia  # noqa: E402
import nota  # noqa: E402
import perimetro  # noqa: E402
import stato  # noqa: E402

ROOT = stato.ROOT
FONTI = ("sharepoint", "onedrive")
ORDINE_TIPI = ("sposta", "copia", "nuova_voce", "in_attesa", "rimuovi", "azzera", "recupera", "in_coda")
ALL_AGENTE = ("recupera", "in_coda")
VALIDITA_PIANO_ORE = 24
URI_RE = re.compile(r"^file:///([^/]+)/([^/]+)$")
ISTANTE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2}:\d{2})(?:[.,]\d+)?(Z|[+-]\d{2}:?\d{2})?$")


def _modulo(file, nome):
    spec = importlib.util.spec_from_file_location(nome, QUI / file)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


sposta_nota = _modulo("sposta-nota.py", "sposta_nota")  # nome_da_url, family_nuova, url_uguali


class Uscita(Exception):
    """Errore con il suo codice di uscita."""

    def __init__(self, codice, messaggio):
        super().__init__(messaggio)
        self.codice = codice


class Fallita(Exception):
    """Un passo dell'applica non riuscito: la voce va in errore, le altre continuano."""


# --- Lettura delle note -----------------------------------------------------------------

_LEGGI_FM = famiglia._frontmatter
_CACHE = {}


def _frontmatter_in_cache(p):
    """famiglia._frontmatter con una cache per file (inode, mtime, dimensione): il piano chiede
    a `stato.trova` gli stessi frontmatter una volta per file nuovo dell'elenco."""
    p = Path(p)
    try:
        st = p.stat()
    except OSError:
        return None
    k = (str(p), st.st_ino, st.st_mtime_ns, st.st_size)
    if k not in _CACHE:
        _CACHE[k] = _LEGGI_FM(p)
    return copy.deepcopy(_CACHE[k])


famiglia._frontmatter = _frontmatter_in_cache


def frontmatter(rel, fresco=False):
    p = ROOT / rel
    if not rel or not p.is_file():
        return None
    d = _LEGGI_FM(p) if fresco else _frontmatter_in_cache(p)
    return d if isinstance(d, dict) else None


def tags(d):
    t = d.get("tags")
    return t if isinstance(t, list) else ([t] if t else [])


def corrente(d):
    return d.get("current") if isinstance(d.get("current"), dict) else {}


def mappe(d, campo):
    return [x for x in d.get(campo) or [] if isinstance(x, dict)]


def testo(v):
    return "" if v is None else str(v)


def ist(v):
    """Istante di un valore del frontmatter (datetime o stringa) come stringa ISO UTC, o None."""
    v = nota.normale(v)
    return v if isinstance(v, str) and stato.ISTANTE_RE.match(v) else None


# --- Elenco -----------------------------------------------------------------------------

def normalizza_istante(v, dove):
    m = ISTANTE_RE.match(str(v or "").strip())
    if not m:
        raise Uscita(2, f"{dove}: istante `{v}` non valido (serve AAAA-MM-GGTHH:MM:SSZ)")
    giorno, ora, zona = m.groups()
    try:
        t = dt.datetime.strptime(f"{giorno}T{ora}", "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        raise Uscita(2, f"{dove}: istante `{v}` non è una data valida")
    if zona and zona != "Z":
        segno = 1 if zona[0] == "+" else -1
        cifre = zona[1:].replace(":", "")
        t -= segno * dt.timedelta(hours=int(cifre[:2]), minutes=int(cifre[2:]))
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def leggi_elenco(percorso):
    """(file, cartelle saltate): file = [{chiave, item_id, drive, uri, web_url, nome, last_modified}]."""
    try:
        dati = json.loads(Path(percorso).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
        raise Uscita(2, f"--elenco `{percorso}` illeggibile: {e}")
    if isinstance(dati, dict) and isinstance(dati.get("value"), list):
        dati = dati["value"]
    if not isinstance(dati, list):
        raise Uscita(2, f"--elenco `{percorso}`: serve una lista JSON di file (o {{\"value\": [...]}})")
    files, cartelle, viste = [], 0, {}
    for i, x in enumerate(dati, 1):
        dove = f"--elenco, voce {i}"
        if not isinstance(x, dict):
            raise Uscita(2, f"{dove}: non è un oggetto JSON")
        if "folder" in x:
            cartelle += 1
            continue
        web_url = str(x.get("webUrl") or x.get("web_url") or "").strip()
        if not web_url:
            raise Uscita(2, f"{dove}: manca `webUrl`")
        drive = x.get("driveId") or (x.get("parentReference") or {}).get("driveId")
        item_id, uri, chiave = x.get("id"), x.get("uri"), x.get("chiave")
        m = URI_RE.match(str(uri or ""))
        if uri and not m:
            raise Uscita(2, f"{dove}: `uri` `{uri}` non è file:///<driveId>/<itemId>")
        if m:
            drive, item_id = drive or m.group(1), item_id or m.group(2)
        if chiave:
            chiave = str(chiave).strip()
            if "/" in chiave:
                d, i_ = chiave.rsplit("/", 1)
                drive, item_id = drive or d, item_id or i_
            else:
                item_id = item_id or chiave
        elif drive and item_id:
            chiave = f"{drive}/{item_id}"
        else:
            raise Uscita(2, f"{dove}: servono `id` e `driveId` (o `chiave`, o `uri`)")
        if not uri and drive and item_id:
            uri = f"file:///{drive}/{item_id}"
        lm = normalizza_istante(x.get("lastModifiedDateTime") or x.get("last_modified"), dove)
        if chiave in viste:
            raise Uscita(2, f"{dove}: chiave `{chiave}` ripetuta (voce {viste[chiave]})")
        viste[chiave] = i
        files.append({"chiave": chiave, "item_id": str(item_id), "drive": drive, "uri": uri,
                      "web_url": web_url, "nome": str(x.get("name") or sposta_nota.nome_da_url(web_url)),
                      "last_modified": lm})
    return files, cartelle


def impronta(fonte, libreria, files):
    testo_ = json.dumps({"vault": str(ROOT), "fonte": fonte, "libreria": libreria,
                         "elenco": sorted(files, key=lambda f: f["chiave"])}, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(testo_.encode("utf-8")).hexdigest()


# --- Posizioni --------------------------------------------------------------------------

class Contesto:
    def __init__(self, fonte, libreria):
        self.fonte = fonte
        self.conf = config.carica()
        self.per = config.perimetro()
        self.librerie = list(self.conf["fonti"]["sharepoint"]["librerie"])
        self.libreria = None
        if fonte == "sharepoint" and libreria:
            uguali = [x for x in self.librerie if x.lower() == str(libreria).strip().lower()]
            if not uguali:
                raise Uscita(2, f"libreria sconosciuta `{libreria}` (perimetro: {', '.join(self.librerie)})")
            self.libreria = uguali[0]
        self._pos = {}

    def libreria_canonica(self, nome):
        return next((x for x in self.librerie if x.lower() == str(nome or "").lower()), nome)

    def posizione(self, web_url):
        """Fonte, libreria, cartella della nota, altro sito e rango canonico di un webUrl."""
        if web_url in self._pos:
            return self._pos[web_url]
        an = perimetro.analizza(web_url)
        cartella = an.get("cartella_nota")
        altro_sito = bool(an.get("fonte") == "sharepoint" and cartella and cartella.startswith("sources/sharepoint/_"))
        libreria = self.libreria_canonica(an.get("libreria"))
        rango = None
        if an.get("riconosciuto") and an.get("fonte"):
            rango = config.rango_canonico(an["fonte"], None if altro_sito else libreria)
        pos = {"an": an, "fonte": an.get("fonte"), "libreria": libreria, "cartella": cartella,
               "altro_sito": altro_sito, "rango": rango}
        self._pos[web_url] = pos
        return pos

    def coperta(self, pos):
        """True se un file in quella posizione, se esiste, deve essere nell'elenco."""
        if not pos["an"].get("riconosciuto") or pos["fonte"] != self.fonte or not pos["cartella"]:
            return False
        if self.fonte == "onedrive":
            return True
        if pos["altro_sito"]:
            return False
        return pos["libreria"] == self.libreria if self.libreria else pos["libreria"] in self.librerie

    def esclusa_altro_sito(self, web_url):
        url = unquote(urlsplit(web_url.strip())._replace(query="", fragment="").geturl())
        parti = [x for x in url[len(self.per["sharepoint"]):].split("/") if x]
        return perimetro.cartella_esclusa(parti[2:-1], self.per)


# --- Piano ------------------------------------------------------------------------------

def _scegli(candidati):
    """(candidato, ambigui): l'unico con lo stesso nome, se no l'unico candidato; altrimenti nessuno."""
    per_nome = [c for c in candidati if "nome" in c["motivo"].split(", ")]
    if len(per_nome) == 1:
        return per_nome[0], []
    if per_nome:
        return None, per_nome
    if len(candidati) == 1:
        return candidati[0], []
    return None, candidati


def calcola_piano(fonte, libreria, files, cartelle_saltate=0):
    ctx = Contesto(fonte, libreria)
    dati = stato.leggi(fonte)
    items = dati["items"]
    watermark = dati.get("watermark")
    indice = stato.indice_note(fonte)
    voci, ignorati = [], []
    ok = 0
    presenti = {}        # chiave → file dell'elenco accettato
    ritrovate = set()    # note con una voce nell'elenco, o ritrovate da nuova_voce / copia
    ignorati_noti = {}   # chiave nota allo stato → motivo dell'esclusione
    nuove = collections.defaultdict(list)   # nota → voci nuova_voce provvisorie
    copie = collections.defaultdict(list)   # nota → voci copia provvisorie
    info = {}

    def nota_info(rel):
        if rel not in info:
            d = frontmatter(rel)
            if d is None:
                info[rel] = None
            else:
                cur = corrente(d)
                chiavi = indice.get(rel, [])
                cid = testo(cur.get("item_id"))
                kc = next((k for k in chiavi if cid and k.rsplit("/", 1)[-1] == cid), None)
                if kc is None and len(chiavi) == 1:
                    kc = chiavi[0]  # la sola voce della nota fa da corrente
                info[rel] = {"d": d, "cur": cur, "chiavi": chiavi, "chiave_corrente": kc}
        return info[rel]

    def ignora(f, motivo, **extra):
        ignorati.append({"web_url": f["web_url"], "nome": f["nome"], "chiave": f["chiave"], "motivo": motivo, **extra})
        if f["chiave"] in items:
            ignorati_noti[f["chiave"]] = motivo

    def da_recuperare(f, pos, **extra):
        tipo = "recupera" if watermark is None or not stato.piu_recente(f["last_modified"], watermark) else "in_coda"
        voci.append({"tipo": tipo, "nota": extra.pop("nota", None), "chiave": f["chiave"], "web_url": f["web_url"],
                     "nome": f["nome"], "last_modified": f["last_modified"], "cartella_nota": pos["cartella"],
                     "aggiorna": False, **extra})

    # 1. File dell'elenco
    for f in files:
        pos = ctx.posizione(f["web_url"])
        an = pos["an"]
        if not an.get("riconosciuto"):
            ignora(f, an.get("motivo") or "URL non riconosciuto")
            continue
        if pos["fonte"] != fonte:
            ignora(f, f"file di {pos['fonte']}, non di {fonte}")
            continue
        if ctx.libreria and (pos["altro_sito"] or pos["libreria"] != ctx.libreria):
            ignora(f, f"libreria `{an.get('libreria')}` fuori da --libreria {ctx.libreria}")
            continue
        if not an["dentro"]:
            if not (pos["altro_sito"] and an.get("tipo_processato") is not False
                    and not ctx.esclusa_altro_sito(f["web_url"])):
                ignora(f, an.get("motivo") or "fuori perimetro")
                continue
        voce = items.get(f["chiave"])
        if voce is not None:
            rel = voce.get("note")
            ni = nota_info(rel) if rel else None
            if ni is None:
                ignora(f, "la voce dello stato punta a una nota inesistente o illeggibile", nota=rel)
                continue
            d, cur = ni["d"], ni["cur"]
            if "fuori-perimetro" in tags(d):
                ignora(f, "nota con il tag fuori-perimetro", nota=rel)
                continue
            presenti[f["chiave"]] = f
            ritrovate.add(rel)
            iid = f["item_id"]
            copia = next((a for a in mappe(d, "also_at") if testo(a.get("item_id")) == iid), None)
            e_corrente = f["chiave"] == ni["chiave_corrente"]
            if e_corrente:
                prodotte = False
                cambia_url = not sposta_nota.url_uguali(f["web_url"], cur.get("web_url"))
                cambia_nome = f["nome"] != testo(cur.get("name"))
                fuori_posto = pos["cartella"] != str(Path(rel).parent)
                ripristina = d.get("status") == "removed"
                if cambia_url or cambia_nome or fuori_posto or ripristina:
                    if pos["altro_sito"]:
                        ignora(f, "la current è cambiata su un altro sito del tenant: sposta-nota.py non sposta "
                                  "fuori perimetro, decide l'agente", nota=rel)
                    else:
                        family = d.get("family")
                        nuova = sposta_nota.family_nuova(family, cur.get("name"), sposta_nota.nome_da_url(f["web_url"]))
                        voci.append({"tipo": "sposta", "nota": rel, "chiave": f["chiave"], "web_url": f["web_url"],
                                     "web_url_prima": cur.get("web_url"), "nome": f["nome"],
                                     "cartella_nuova": pos["cartella"], "cambia_cartella": fuori_posto,
                                     "cambia_famiglia": nuova != family, "ripristina": ripristina})
                    prodotte = True
                if stato.piu_recente(f["last_modified"], voce.get("last_modified")):
                    da_recuperare(f, pos, nota=rel, aggiorna=True, last_modified_stato=voce.get("last_modified"))
                    prodotte = True
                ok += not prodotte
            elif copia is not None and not sposta_nota.url_uguali(f["web_url"], copia.get("web_url")):
                voci.append({"tipo": "copia", "nota": rel, "chiave": f["chiave"], "chiave_corrente": ni["chiave_corrente"],
                             "web_url": f["web_url"], "web_url_prima": copia.get("web_url"), "nome": f["nome"],
                             "last_modified": f["last_modified"], "uri": f["uri"], "aggiorna": True,
                             "diventa_current": False, "rango_nuovo": pos["rango"],
                             "rango_corrente": ctx.posizione(testo(cur.get("web_url")))["rango"],
                             "cartella_nuova": pos["cartella"], "rileggi": False, "ripristina": False,
                             "motivo": "item_id in also_at"})
            else:
                ok += 1  # versione vecchia ancora presente, copia invariata o voce senza posizione nella nota
            continue

        # Chiave nuova: regola dell'identità (SPEC 6.4)
        candidati = [c for c in stato.trova(fonte, nome=f["nome"], cartella=pos["cartella"])["candidati"]
                     if nota_info(c["nota"]) is not None and "fuori-perimetro" not in tags(nota_info(c["nota"])["d"])]
        stessa = [c for c in candidati if c["stessa_cartella"]]
        scelto, ambigui = _scegli(stessa or candidati)
        if scelto is None:
            elenco_ambigui = [c["nota"] for c in ambigui]
            if pos["altro_sito"]:
                ignora(f, "altro sito del tenant: nessuna nota" + (" sola" if ambigui else "") + " a cui legarlo "
                          "(si ingerisce a richiesta con /ingest-file)",
                       **({"candidati_ambigui": elenco_ambigui} if ambigui else {}))
            else:
                da_recuperare(f, pos, **({"candidati_ambigui": elenco_ambigui} if ambigui else {}))
            continue
        rel = scelto["nota"]
        ni = nota_info(rel)
        base = {"nota": rel, "chiave": f["chiave"], "chiave_corrente": ni["chiave_corrente"] or ni["chiavi"][0],
                "web_url": f["web_url"], "nome": f["nome"], "last_modified": f["last_modified"], "uri": f["uri"],
                "ripristina": ni["d"].get("status") == "removed", "motivo": scelto["motivo"]}
        if scelto["stessa_cartella"]:
            nuove[rel].append(base)
        else:
            copie[rel].append({**base, "pos": pos})

    # 2. Voci nuove della stessa nota: quale diventa current
    for rel, lista in nuove.items():
        ni = nota_info(rel)
        cur = ni["cur"]
        nome_cur, lm_cur = testo(cur.get("name")), ist(cur.get("last_modified"))
        kc = ni["chiave_corrente"]
        contendenti = []
        if kc in presenti:
            contendenti.append({"corrente": True, "last_modified": presenti[kc]["last_modified"], "nome": nome_cur})
        elif not ctx.coperta(ctx.posizione(testo(cur.get("web_url")))):
            contendenti.append({"corrente": True, "last_modified": lm_cur or "", "nome": nome_cur})
        contendenti += sorted(lista, key=lambda v: v["chiave"])
        contendenti.sort(key=lambda c: (c["last_modified"] or "", bool(c.get("corrente")), c["nome"] == nome_cur),
                         reverse=True)
        vince = contendenti[0]
        for v in lista:
            diventa = v is vince
            voci.append({"tipo": "nuova_voce", **v, "diventa_current": diventa,
                         "rileggi": diventa and (v["last_modified"] != lm_cur or v["nome"] != nome_cur)})
        ritrovate.add(rel)
    con_nuova_current = {v["nota"] for v in voci if v["tipo"] == "nuova_voce" and v["diventa_current"]}

    # 3. Copie: current sulla posizione canonica
    for rel, lista in copie.items():
        ni = nota_info(rel)
        cur = ni["cur"]
        pos_cur = ctx.posizione(testo(cur.get("web_url")))
        kc = ni["chiave_corrente"]
        cur_presente = kc in presenti or not ctx.coperta(pos_cur)
        rango_cur = pos_cur["rango"] if pos_cur["rango"] is not None else len(config.canoniche())
        migliore = min(lista, key=lambda c: (c["pos"]["rango"], c["chiave"]))
        diventa = None
        if rel not in con_nuova_current and not migliore["pos"]["altro_sito"]:
            if not cur_presente or migliore["pos"]["rango"] < rango_cur:
                diventa = migliore
        nome_cur, lm_cur = testo(cur.get("name")), ist(cur.get("last_modified"))
        for c in lista:
            pos = c.pop("pos")
            v = {"tipo": "copia", **c, "aggiorna": False, "diventa_current": c is diventa,
                 "rango_nuovo": pos["rango"], "rango_corrente": pos_cur["rango"], "cartella_nuova": pos["cartella"],
                 "rileggi": c is diventa and (c["last_modified"] != lm_cur or c["nome"] != nome_cur)}
            if c is diventa:
                v["vecchia_current"] = {"web_url": cur.get("web_url"), "item_id": testo(cur.get("item_id")),
                                        "name": nome_cur, "last_modified": lm_cur,
                                        "dove": "also_at" if cur_presente else "versions"}
            voci.append(v)
        ritrovate.add(rel)

    # 4. Assenze
    for rel, chiavi in indice.items():
        if rel in ritrovate:
            con_assente = [k for k in chiavi if "assente" in items.get(k, {})]
            if con_assente:
                voci.append({"tipo": "azzera", "nota": rel, "chiavi": con_assente})
            continue
        ni = nota_info(rel)
        if ni is None or "fuori-perimetro" in tags(ni["d"]) or ni["d"].get("status") == "removed":
            continue
        if not ctx.coperta(ctx.posizione(testo(ni["cur"].get("web_url")))):
            continue
        k = ni["chiave_corrente"] or max(chiavi, key=lambda x: (items[x].get("last_modified") or "", x))
        attuale = stato.numero(items[k].get("assente", 0), "assente")
        noti = [ignorati_noti[c] for c in chiavi if c in ignorati_noti]
        motivo = ("il file è nell'elenco ma è stato ignorato: " + noti[0] if noti
                  else "nessuna voce della nota nell'elenco e nessun candidato")
        voci.append({"tipo": "in_attesa" if attuale < 1 else "rimuovi", "nota": rel, "chiave": k, "chiavi": chiavi,
                     "assente_attuale": attuale, "assente_dopo": attuale + 1, "motivo": motivo})

    voci.sort(key=lambda v: (ORDINE_TIPI.index(v["tipo"]), v.get("nota") or "", not v.get("diventa_current", False),
                             v.get("chiave") or ""))
    for i, v in enumerate(voci, 1):
        v["id"] = i
    riepilogo = dict(collections.Counter(v["tipo"] for v in voci))
    riepilogo["ok"] = ok
    return {"fonte": fonte, "libreria": ctx.libreria, "watermark": watermark,
            "elenco": len(files), "cartelle_saltate": cartelle_saltate, "ignorati": ignorati,
            "riepilogo": {t: riepilogo[t] for t in (*ORDINE_TIPI, "ok") if t in riepilogo},
            "voci": [{"id": v.pop("id"), **v} for v in voci]}


# --- Applica ----------------------------------------------------------------------------

def esegui(script, *args):
    res = subprocess.run([sys.executable, str(QUI / script), *map(str, args)], cwd=ROOT,
                         capture_output=True, text=True)
    if res.returncode != 0:
        raise Fallita(f"{script} uscito con {res.returncode}: {(res.stderr or res.stdout).strip()}")
    return res.stdout


def esegui_json(script, *args):
    out = esegui(script, *args, "--json")
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        raise Fallita(f"{script}: risposta non JSON: {out.strip()[:200]}")


def nota_attuale(fonte, chiavi, ripiego):
    """Percorso attuale della nota: segue lo stato (sposta-nota.py aggiorna `note`)."""
    items = stato.leggi(fonte)["items"]
    for k in chiavi:
        rel = (items.get(k) or {}).get("note")
        if k and rel and (ROOT / rel).is_file():
            return rel
    if ripiego and (ROOT / ripiego).is_file():
        return ripiego
    raise Fallita(f"nota non trovata (voci {', '.join(c for c in chiavi if c)}, nota del piano `{ripiego}`)")


def flusso(lista):
    """Lista di mappe in YAML inline per `aggiorna-nota.py --campo versions=...|also_at=...`."""
    parti = []
    for x in lista:
        coppie = []
        for k, v in x.items():
            if k == "last_modified":
                s = ist(v) or "null"
            else:
                s = json.dumps(testo(v), ensure_ascii=False)
            coppie.append(f"{k}: {s}")
        parti.append("{" + ", ".join(coppie) + "}")
    return "[" + ", ".join(parti) + "]"


def con_versione(versioni, voce):
    """versions con la voce inserita in ordine di data (dopo la prima, che è la corrente)."""
    out = list(versioni)
    i = 1 if out else 0
    while i < len(out) and (ist(out[i].get("last_modified")) or "") >= (voce["last_modified"] or ""):
        i += 1
    out.insert(i, voce)
    return out


def assicura_also_at(rel, web_url, item_id):
    """La posizione in also_at (aggiunta con --also-at, o corretta se c'è con un altro URL o ID)."""
    d = frontmatter(rel, fresco=True) or {}
    lista = mappe(d, "also_at")
    per_id = next((a for a in lista if item_id and testo(a.get("item_id")) == item_id), None)
    per_url = next((a for a in lista if sposta_nota.url_uguali(a.get("web_url"), web_url)), None)
    if per_id is not None:
        if sposta_nota.url_uguali(per_id.get("web_url"), web_url):
            return False
        per_id["web_url"] = web_url
    elif per_url is not None:
        per_url["item_id"] = item_id
    else:
        esegui("aggiorna-nota.py", rel, "--also-at", f"web_url={web_url}", f"item_id={item_id}")
        return True
    esegui("aggiorna-nota.py", rel, "--campo", f"also_at={flusso(lista)}")
    return True


def assicura_versione(rel, nome, item_id, last_modified, ripristina=False):
    d = frontmatter(rel, fresco=True) or {}
    versioni = mappe(d, "versions")
    args = []
    if not any(testo(v.get("item_id")) == item_id for v in versioni):
        nuove = con_versione(versioni, {"name": nome, "item_id": item_id, "last_modified": last_modified})
        args += ["--campo", f"versions={flusso(nuove)}"]
    if ripristina and d.get("status") == "removed":
        args += ["--campo", "status=active"]
    if args:
        esegui("aggiorna-nota.py", rel, *args)
    return bool(args)


def assicura_collegata(fonte, chiave, vecchia, istante, rel):
    voce = stato.leggi(fonte)["items"].get(chiave) or {}
    if voce.get("note") == rel and "assente" not in voce:
        return False
    if not vecchia:
        raise Fallita(f"nessuna voce della nota da cui collegare `{chiave}`")
    esegui_json("stato.py", "collega", fonte, chiave, "--stessa-nota-di", vecchia, "--istante", istante)
    return True


def applica_sposta(fonte, v):
    rel = nota_attuale(fonte, [v["chiave"]], v["nota"])
    out = esegui_json("sposta-nota.py", rel, "--web-url", v["web_url"])
    v["nota_dopo"] = out.get("nota_dopo")
    return out.get("cambiato")


def applica_copia(fonte, v):
    rel = nota_attuale(fonte, [v.get("chiave_corrente"), v["chiave"]], v["nota"])
    if v.get("aggiorna"):
        return assicura_also_at(rel, v["web_url"], testo(v["chiave"]).rsplit("/", 1)[-1])
    item_id = v["chiave"].rsplit("/", 1)[-1]
    fatto = False
    if v.get("diventa_current"):
        args = [rel, "--web-url", v["web_url"], "--item-id", item_id, "--last-modified", v["last_modified"]]
        if v.get("uri"):
            args += ["--uri", v["uri"]]
        out = esegui_json("sposta-nota.py", *args)
        fatto = bool(out.get("cambiato"))
        rel = out.get("nota_dopo") or rel
        v["nota_dopo"] = rel
        vc = v["vecchia_current"]
        if vc["dove"] == "also_at":
            fatto |= assicura_also_at(rel, vc["web_url"], vc["item_id"])
        else:
            fatto |= assicura_versione(rel, vc["name"], vc["item_id"], vc["last_modified"])
        fatto |= assicura_collegata(fonte, v["chiave"], v.get("chiave_corrente"), v["last_modified"], rel)
        return fatto
    fatto |= assicura_also_at(rel, v["web_url"], item_id)
    if v.get("ripristina"):
        d = frontmatter(rel, fresco=True) or {}
        if d.get("status") == "removed":
            esegui("aggiorna-nota.py", rel, "--campo", "status=active")
            fatto = True
    fatto |= assicura_collegata(fonte, v["chiave"], v.get("chiave_corrente"), v["last_modified"], rel)
    return fatto


def applica_nuova_voce(fonte, v):
    rel = nota_attuale(fonte, [v.get("chiave_corrente"), v["chiave"]], v["nota"])
    item_id = v["chiave"].rsplit("/", 1)[-1]
    fatto = False
    if v.get("diventa_current"):
        d = frontmatter(rel, fresco=True) or {}
        cur = corrente(d)
        if testo(cur.get("item_id")) != item_id:
            args = [rel, "--nuova-versione",
                    "--campo", f"current.name={json.dumps(v['nome'], ensure_ascii=False)}",
                    "--campo", f"current.item_id={json.dumps(item_id)}",
                    "--campo", f"current.last_modified={v['last_modified']}",
                    "--campo", f"current.web_url={json.dumps(v['web_url'], ensure_ascii=False)}"]
            if v.get("uri"):
                args += ["--campo", f"current.uri={json.dumps(v['uri'])}"]
            if v.get("ripristina") and d.get("status") == "removed":
                args += ["--campo", "status=active"]
            if not v.get("rileggi") and ist(d.get("ingested_at")):
                args += ["--campo", f"ingested_at={ist(d.get('ingested_at'))}"]  # niente da rileggere
            esegui("aggiorna-nota.py", *args)
            fatto = True
        elif v.get("ripristina") and d.get("status") == "removed":
            esegui("aggiorna-nota.py", rel, "--campo", "status=active")
            fatto = True
    else:
        fatto |= assicura_versione(rel, v["nome"], item_id, v["last_modified"], v.get("ripristina"))
    fatto |= assicura_collegata(fonte, v["chiave"], v.get("chiave_corrente"), v["last_modified"], rel)
    return fatto


def applica_assenza(fonte, v):
    voce = stato.leggi(fonte)["items"].get(v["chiave"])
    if voce is None:
        raise Fallita(f"nessuna voce `{v['chiave']}` nello stato")
    attuale = stato.numero(voce.get("assente", 0), "assente")
    fatto = False
    if attuale == v["assente_attuale"]:
        esegui_json("stato.py", "set-assente", fonte, v["chiave"])
        fatto = True
    elif attuale != v["assente_dopo"]:
        raise Fallita(f"`assente` di `{v['chiave']}` è {attuale}, il piano l'aveva letto {v['assente_attuale']}: "
                      "qualcosa è cambiato, rifai il piano")
    if v["tipo"] == "rimuovi":
        rel = nota_attuale(fonte, [v["chiave"]], v["nota"])
        d = frontmatter(rel, fresco=True) or {}
        if d.get("status") != "removed":
            esegui("aggiorna-nota.py", rel, "--campo", "status=removed")
            fatto = True
    return fatto


def applica_azzera(fonte, v):
    items = stato.leggi(fonte)["items"]
    fatto = False
    for k in v["chiavi"]:
        if "assente" in (items.get(k) or {}):
            esegui_json("stato.py", "set-assente", fonte, k, "--azzera")
            fatto = True
    return fatto


AZIONI = {"sposta": applica_sposta, "copia": applica_copia, "nuova_voce": applica_nuova_voce,
          "in_attesa": applica_assenza, "rimuovi": applica_assenza, "azzera": applica_azzera}


def applica(piano, solo=None):
    fonte = piano["fonte"]
    for v in sorted(piano["voci"], key=lambda x: (ORDINE_TIPI.index(x["tipo"]), x["id"])):
        if solo is not None and v["id"] not in solo:
            continue
        v.pop("messaggio", None)
        if v["tipo"] in ALL_AGENTE:
            v["esito"] = "all'agente"
            continue
        try:
            v["esito"] = "fatto" if AZIONI[v["tipo"]](fonte, v) else "già fatto"
        except (Fallita, stato.Errore, nota.Errore) as e:
            v["esito"] = "errore"
            v["messaggio"] = str(e)
    piano["applicato"] = True
    piano["esiti"] = dict(collections.Counter(v["esito"] for v in piano["voci"] if "esito" in v))
    return piano


# --- Riga di comando --------------------------------------------------------------------

def adesso():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def piano_ripreso(percorso, impr):
    """Il piano salvato in --piano, se è dello stesso elenco e recente; altrimenti None."""
    p = Path(percorso)
    if not p.is_file():
        return None
    try:
        salvato = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        sys.stderr.write(f"avviso: --piano `{percorso}` illeggibile: ricalcolo il piano\n")
        return None
    if not isinstance(salvato, dict) or salvato.get("impronta") != impr or not isinstance(salvato.get("voci"), list):
        sys.stderr.write(f"avviso: --piano `{percorso}` è di un altro elenco: ricalcolo il piano\n")
        return None
    try:
        creato = dt.datetime.strptime(salvato.get("creato", ""), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    except ValueError:
        return None
    if dt.datetime.now(dt.timezone.utc) - creato > dt.timedelta(hours=VALIDITA_PIANO_ORE):
        sys.stderr.write(f"avviso: --piano `{percorso}` ha più di {VALIDITA_PIANO_ORE} ore: ricalcolo il piano\n")
        return None
    return salvato


def scrivi_piano(percorso, piano):
    if percorso:
        stato.scrivi_atomico(Path(percorso), json.dumps(piano, ensure_ascii=False, indent=2) + "\n")


def riga(v):
    cosa = v.get("nota") or v.get("web_url")
    dettagli = []
    if v["tipo"] == "sposta":
        dettagli.append(f"→ {v['cartella_nuova']}" + (" (cartella nuova)" if v["cambia_cartella"] else "")
                        + (" (famiglia nuova)" if v["cambia_famiglia"] else "") + (" (ripristina)" if v["ripristina"] else ""))
    elif v["tipo"] in ("copia", "nuova_voce"):
        dettagli.append(v["web_url"])
        if v.get("diventa_current"):
            dettagli.append("diventa current")
        if v.get("rileggi"):
            dettagli.append("da rileggere")
        if v.get("aggiorna"):
            dettagli.append("posizione aggiornata")
    elif v["tipo"] in ("in_attesa", "rimuovi"):
        dettagli.append(f"assente {v['assente_attuale']} → {v['assente_dopo']}")
    elif v["tipo"] in ALL_AGENTE:
        dettagli.append(v["last_modified"] + (" · versione nuova" if v.get("aggiorna") else ""))
        if v.get("candidati_ambigui"):
            dettagli.append("candidati ambigui: " + ", ".join(v["candidati_ambigui"]))
    esito = f" · {v['esito']}" if "esito" in v else ""
    if v.get("messaggio"):
        esito += f": {v['messaggio']}"
    return f"- #{v['id']} {v['tipo']} · {cosa} · " + " · ".join(dettagli) + esito


def testo_piano(p):
    dove = f"{p['fonte']}" + (f" · {p['libreria']}" if p.get("libreria") else "")
    righe = [f"Riconciliazione {dove}: {p['elenco']} file nell'elenco, {len(p['ignorati'])} ignorati, "
             f"watermark {p['watermark'] or 'null'}" + (" (piano ripreso)" if p.get("ripreso") else "")]
    righe += [riga(v) for v in p["voci"]]
    righe += [f"- ignorato · {i['web_url']} · {i['motivo']}" for i in p["ignorati"]]
    righe.append("Riepilogo: " + ", ".join(f"{t} {n}" for t, n in p["riepilogo"].items()))
    if p.get("applicato"):
        righe.append("Esiti: " + (", ".join(f"{e} {n}" for e, n in p["esiti"].items()) or "nessuna voce"))
    return "\n".join(righe)


def main(argv):
    if not argv or any(a in ("-h", "--help") for a in argv):
        print(__doc__)
        return 0 if argv else 2
    opt, flag = {}, set()
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--applica", "--json"):
            flag.add(a)
        elif a in ("--elenco", "--fonte", "--libreria", "--piano", "--solo"):
            if i + 1 >= len(argv) or not argv[i + 1].strip():
                raise Uscita(2, f"{a} vuole un valore")
            opt[a] = argv[i + 1].strip()
            i += 1
        else:
            raise Uscita(2, f"argomento non riconosciuto: {a} (riconcilia.py --help)")
        i += 1
    for obbligatoria in ("--elenco", "--fonte"):
        if obbligatoria not in opt:
            raise Uscita(2, f"{obbligatoria} è obbligatorio (riconcilia.py --help)")
    fonte = opt["--fonte"]
    if fonte not in FONTI:
        raise Uscita(2, f"fonte sconosciuta `{fonte}` (ammesse: {', '.join(FONTI)})")
    solo = None
    if "--solo" in opt:
        if "--applica" not in flag:
            raise Uscita(2, "--solo vale solo con --applica")
        try:
            solo = {int(x) for x in opt["--solo"].split(",") if x.strip()}
        except ValueError:
            raise Uscita(2, f"--solo `{opt['--solo']}`: servono id numerici separati da virgole")
    libreria = opt.get("--libreria") if fonte == "sharepoint" else None
    try:
        files, cartelle = leggi_elenco(opt["--elenco"])
        ctx = Contesto(fonte, libreria)  # valida la libreria prima di tutto
        impr = impronta(fonte, ctx.libreria, files)
        piano = piano_ripreso(opt["--piano"], impr) if "--applica" in flag and "--piano" in opt else None
        if piano is not None:
            piano["ripreso"] = True
        else:
            piano = calcola_piano(fonte, ctx.libreria, files, cartelle)
            piano = {**{k: piano[k] for k in piano if k != "voci"}, "impronta": impr, "creato": adesso(),
                     "voci": piano["voci"]}
    except config.ConfigErrata as e:
        raise Uscita(2, "configurazione non valida: " + "; ".join(e.errori))
    except stato.Errore as e:
        raise Uscita(2, str(e))
    if "--applica" in flag:
        scrivi_piano(opt.get("--piano"), piano)  # un'interruzione lascia il piano da riprendere
        applica(piano, solo)
    scrivi_piano(opt.get("--piano"), piano)
    print(json.dumps(piano, ensure_ascii=False, indent=2) if "--json" in flag else testo_piano(piano))
    return 1 if piano.get("esiti", {}).get("errore") else 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Uscita as e:
        sys.stderr.write(f"errore: {e}\n")
        sys.exit(e.codice)
