"""Regole delle anomalie dell'ingestion (SPEC 4.3, 4.4, 6.1, 6.2 passo 7, 7; audit 2026-10-31
P4, P5, P6, P8, P11). Modulo condiviso da `controlla-vault.py` (che ne fa avvisi ed errori del
rapporto) e da `plancia.py --anomalie` (che ne fa le righe del digest): non è un comando.

Le soglie stanno solo qui. Le funzioni sono pure: non stampano e non scrivono, restituiscono
dizionari con i campi della regola e il `messaggio` che `controlla-vault.py` mette nel rapporto.

- `riconciliazioni_dovute(fonte, state, adesso)`: una voce per libreria di
  `riconciliazione_dovuta` (6.1), con `livello` `errore` oltre `DOVUTA_ERRORE_GIORNI`, `avviso`
  oltre `DOVUTA_AVVISO_GIORNI`, `ok` sotto; un campo illeggibile (non un oggetto, o un istante
  non valido) è una voce con `illeggibile: true` e `livello: "errore"`.
- `watermark_fermo(fonte, state)`: il watermark più di `WATERMARK_FERMO_GIORNI` giorni dietro il
  risultato più recente dell'ultimo giro con risultati (`ultimo_giro`, 6.2 passo 6), con la causa.
- `voci_orfane(note_frontmatter, voci)`: per nota, le voci dello stato il cui itemId (la parte
  della chiave dopo l'ultima `/`) non è né in `current.item_id`, né in `versions`, né in
  `also_at` (4.4). Le note considerate sono quelle di `incrociabile`.
- `hub_da_rileggere(root, oggi, giorni)`: le righe `- Da rileggere dopo [[<fonte>]] v<N> del
  AAAA-MM-GG` (4.3) nelle note di `topics/`, `clients/`, `projects/`; `scaduta` oltre
  `HUB_DA_RILEGGERE_GIORNI` giorni.
- `giri_anomali(righe_esiti)`: dalle righe di `plancia.esiti_del_giorno` quelle `mancante` o
  `errore` (la regola dell'orario atteso resta in plancia).
"""

import datetime as dt
import re
from collections import defaultdict
from pathlib import Path

# Giorni oltre i quali una riconciliazione dovuta è un avviso e poi un errore (P4), distacco
# massimo tra il watermark e il risultato più recente dell'ultimo giro (P5), età oltre la quale
# una riga «Da rileggere» va nel digest (P8)
DOVUTA_AVVISO_GIORNI = 1
DOVUTA_ERRORE_GIORNI = 7
WATERMARK_FERMO_GIORNI = 2
HUB_DA_RILEGGERE_GIORNI = 7

# Fonti dello stato con `riconciliazione_dovuta` (6.1) e con watermark e `ultimo_giro`
FONTI_DOVUTA = ("sharepoint", "onedrive")
FONTI_WATERMARK = ("sharepoint", "onedrive", "outlook")
# Cartelle delle note hub che citano le fonti (4.3)
CARTELLE_HUB = ("topics", "clients", "projects")
DA_RILEGGERE = re.compile(
    r"^[ \t]*- Da rileggere dopo \[\[([^\]|#]+)(?:[|#][^\]]*)?\]\] v(\d+) del (\d{4}-\d{2}-\d{2})", re.M)
LIVELLI_ANOMALI = ("avviso", "errore")


def istante_utc(v):
    """Istante `AAAA-MM-GGTHH:MM:SSZ` dello stato come datetime UTC; None se non è valido."""
    try:
        return dt.datetime.strptime(str(v), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    except ValueError:
        return None


def _lista(v):
    if v is None or v == "":
        return []
    return v if isinstance(v, list) else [v]


def comando_riconciliazione(fonte, libreria):
    """Il comando che chiude una riconciliazione dovuta (6.4)."""
    return "/ingest riconcilia onedrive" if fonte == "onedrive" else f"/ingest riconcilia sharepoint:{libreria}"


def riconciliazioni_dovute(fonte, state, adesso=None):
    """Una voce per libreria di `riconciliazione_dovuta` di `state` (dizionario dello stato della
    fonte), in ordine di libreria: `{"fonte", "libreria", "dal", "giorni", "livello", "comando",
    "messaggio", "illeggibile"}`. `adesso`: datetime con fuso (predefinito: ora, UTC)."""
    adesso = adesso or dt.datetime.now(dt.timezone.utc)
    dovute = state.get("riconciliazione_dovuta") or {}
    if not isinstance(dovute, dict):
        return [{"fonte": fonte, "libreria": None, "dal": None, "giorni": None, "livello": "errore",
                 "comando": None, "illeggibile": True,
                 "messaggio": "`riconciliazione_dovuta` illeggibile: deve essere {libreria: istante}"}]
    out = []
    for libreria, ist in sorted(dovute.items()):
        t = istante_utc(ist)
        if t is None:
            out.append({"fonte": fonte, "libreria": libreria, "dal": ist, "giorni": None,
                        "livello": "errore", "comando": None, "illeggibile": True,
                        "messaggio": f"`riconciliazione_dovuta` di {libreria}: istante `{ist}` non valido"})
            continue
        giorni = (adesso - t).total_seconds() / 86400
        comando = comando_riconciliazione(fonte, libreria)
        livello = ("errore" if giorni > DOVUTA_ERRORE_GIORNI else
                   "avviso" if giorni > DOVUTA_AVVISO_GIORNI else "ok")
        out.append({"fonte": fonte, "libreria": libreria, "dal": ist, "giorni": int(giorni),
                    "livello": livello, "comando": comando, "illeggibile": False,
                    "messaggio": f"riconciliazione dovuta per {libreria} dal {ist} ({int(giorni)} giorni): "
                                 f"{comando}, poi `stato.py set-riconciliata {fonte} \"{libreria}\"`"})
    return out


def watermark_fermo(fonte, state):
    """None, oppure `{"fonte", "watermark", "piu_recente", "fine", "risultati", "falliti",
    "causa", "messaggio"}` se l'ultimo giro ha risultati e il più recente è più di
    `WATERMARK_FERMO_GIORNI` giorni dopo il watermark."""
    giro = state.get("ultimo_giro")
    if not isinstance(giro, dict) or not giro.get("risultati"):
        return None
    wm, piu_rec = istante_utc(state.get("watermark")), istante_utc(giro.get("piu_recente"))
    if not (wm and piu_rec and (piu_rec - wm).total_seconds() > WATERMARK_FERMO_GIORNI * 86400):
        return None
    falliti = giro.get("falliti") or 0
    causa = (f"{falliti} falliti lo tengono fermo: riprova quei file" if falliti
             else "nessun fallito: `stato.py set-watermark " + fonte + " --da-giro`")
    return {
        "fonte": fonte,
        "watermark": state.get("watermark"),
        "piu_recente": giro.get("piu_recente"),
        "fine": giro.get("fine"),
        "risultati": giro.get("risultati"),
        "falliti": falliti,
        "causa": causa,
        "messaggio": f"watermark di {fonte} fermo al {state.get('watermark')}: l'ultimo giro "
                     f"({giro.get('fine')}) ha {giro.get('risultati')} risultati fino al "
                     f"{giro.get('piu_recente')}, più di {WATERMARK_FERMO_GIORNI} giorni dopo ({causa})",
    }


def incrociabile(rel, fm, fonti):
    """Vero se la nota (`rel` relativo alla radice, `fm` il suo frontmatter) entra nei controlli
    incrociati con lo stato: `source-doc` in `sources/` con `source` tra `fonti`, senza il tag
    `fuori-perimetro`."""
    return (Path(rel).parts[:1] == ("sources",) and isinstance(fm, dict) and fm.get("type") == "source-doc"
            and fm.get("source") in fonti and "fuori-perimetro" not in _lista(fm.get("tags")))


def voci_per_nota(voci):
    """{nota: [(fonte, chiave)]} dalle voci `{fonte: {chiave: voce}}` che hanno `note`."""
    per_nota = defaultdict(list)
    for fonte, items in voci.items():
        for chiave, v in items.items():
            if isinstance(v, dict) and v.get("note"):
                per_nota[v["note"]].append((fonte, chiave))
    return per_nota


def voci_orfane(note_frontmatter, voci):
    """Note con voci dello stato senza versione o copia, in ordine di percorso: `{"nota",
    "orfane", "voci", "fonte", "messaggio"}`. `note_frontmatter`: {percorso relativo: frontmatter}
    (le note fuori da `incrociabile` si saltano); `voci`: {fonte: {chiave: voce}} delle fonti di
    documenti (sharepoint, onedrive) di cui lo stato si è letto."""
    per_nota = voci_per_nota(voci)
    out = []
    for rel, fm in sorted(note_frontmatter.items(), key=lambda x: str(x[0])):
        if not incrociabile(rel, fm, voci):
            continue
        cur = fm.get("current") if isinstance(fm.get("current"), dict) else {}
        ids = {str(cur.get("item_id") or "")}
        for k in ("versions", "also_at"):
            ids |= {str(x.get("item_id") or "") for x in _lista(fm.get(k)) if isinstance(x, dict)}
        chiavi = per_nota.get(str(rel), [])
        orfane = [c for _, c in chiavi if c.rsplit("/", 1)[-1] not in ids]
        if not orfane:
            continue
        fonte = fm.get("source")
        quante = "1 voce" if len(orfane) == 1 else f"{len(orfane)} voci"
        out.append({"nota": str(rel), "orfane": len(orfane), "voci": len(chiavi), "fonte": fonte,
                    "messaggio": f"{quante} dello stato (su {len(chiavi)}) senza versione o copia nella nota: "
                                 f"l'ID non è né in `current`, né in `versions`, né in `also_at` "
                                 f"(`stato.py voci {fonte} <nota>`)"})
    return out


def hub_da_rileggere(root, oggi, giorni=HUB_DA_RILEGGERE_GIORNI):
    """Righe «Da rileggere» delle note hub sotto `root` (Path), in ordine di data crescente:
    `{"hub", "nota", "fonte", "versione", "data", "giorni", "scaduta"}`. `oggi`: date o
    `AAAA-MM-GG`; `scaduta` se la riga ha più di `giorni` giorni."""
    root = Path(root)
    oggi = oggi if isinstance(oggi, dt.date) else dt.date.fromisoformat(str(oggi))
    out = []
    for cartella in CARTELLE_HUB:
        for p in sorted((root / cartella).rglob("*.md")):
            try:
                testo = p.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for m in DA_RILEGGERE.finditer(testo):
                try:
                    data = dt.date.fromisoformat(m.group(3))
                except ValueError:
                    continue
                eta = (oggi - data).days
                out.append({"hub": p.stem, "nota": p.relative_to(root).as_posix(), "fonte": m.group(1).strip(),
                            "versione": f"v{m.group(2)}", "data": m.group(3), "giorni": eta,
                            "scaduta": eta > giorni})
    return sorted(out, key=lambda h: (h["data"], h["hub"], h["fonte"]))


def giri_anomali(righe_esiti):
    """Le righe di `plancia.esiti_del_giorno` con stato `mancante` o `errore`, nello stesso ordine."""
    return [r for r in righe_esiti if r.get("stato") in ("mancante", "errore")]
