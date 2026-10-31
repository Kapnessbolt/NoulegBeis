"""Test delle regole di anomalie.py (audit 2026-10-31, P4, P5, P6, P8, P11) su casi sintetici."""

import datetime as dt
import re

import pytest

import anomalie
from conftest import SCRIPTS, scrivi

ADESSO = dt.datetime(2026, 10, 31, 6, 0, tzinfo=dt.timezone.utc)


def prima(**kw):
    return (ADESSO - dt.timedelta(**kw)).strftime("%Y-%m-%dT%H:%M:%SZ")


# --- Riconciliazione dovuta (P4) ---------------------------------------------------------

def test_riconciliazione_dovuta_livelli_per_eta():
    stato = {"riconciliazione_dovuta": {"Delivery": prima(days=8), "SalesMarketing": prima(days=2),
                                        "Shared Documents": prima(hours=5)}}
    voci = {v["libreria"]: v for v in anomalie.riconciliazioni_dovute("sharepoint", stato, ADESSO)}
    assert [v for v in voci] == ["Delivery", "SalesMarketing", "Shared Documents"]  # in ordine di libreria
    assert (voci["Delivery"]["livello"], voci["Delivery"]["giorni"]) == ("errore", 8)
    assert (voci["SalesMarketing"]["livello"], voci["SalesMarketing"]["giorni"]) == ("avviso", 2)
    assert (voci["Shared Documents"]["livello"], voci["Shared Documents"]["giorni"]) == ("ok", 0)
    d = voci["SalesMarketing"]
    assert d["fonte"] == "sharepoint" and d["dal"] == prima(days=2) and not d["illeggibile"]
    assert d["comando"] == "/ingest riconcilia sharepoint:SalesMarketing"
    assert d["messaggio"] == (f"riconciliazione dovuta per SalesMarketing dal {prima(days=2)} (2 giorni): "
                              "/ingest riconcilia sharepoint:SalesMarketing, poi "
                              "`stato.py set-riconciliata sharepoint \"SalesMarketing\"`")


def test_riconciliazione_dovuta_onedrive_e_senza_segnale():
    (v,) = anomalie.riconciliazioni_dovute("onedrive", {"riconciliazione_dovuta": {"Lavoro": prima(days=3)}}, ADESSO)
    assert v["comando"] == "/ingest riconcilia onedrive" and v["livello"] == "avviso"
    assert anomalie.riconciliazioni_dovute("onedrive", {}, ADESSO) == []
    assert anomalie.riconciliazioni_dovute("onedrive", {"riconciliazione_dovuta": None}, ADESSO) == []


def test_riconciliazione_dovuta_illeggibile_e_errore():
    (v,) = anomalie.riconciliazioni_dovute("sharepoint", {"riconciliazione_dovuta": ["Delivery"]}, ADESSO)
    assert v["illeggibile"] and v["livello"] == "errore" and v["libreria"] is None
    assert v["messaggio"] == "`riconciliazione_dovuta` illeggibile: deve essere {libreria: istante}"
    (v,) = anomalie.riconciliazioni_dovute("sharepoint", {"riconciliazione_dovuta": {"Delivery": "ieri"}}, ADESSO)
    assert v["illeggibile"] and v["livello"] == "errore" and v["libreria"] == "Delivery"
    assert v["messaggio"] == "`riconciliazione_dovuta` di Delivery: istante `ieri` non valido"


def test_riconciliazione_dovuta_adesso_con_fuso():
    """`adesso` con il fuso del vault (plancia) dà gli stessi giorni dell'UTC."""
    roma = ADESSO.astimezone(dt.timezone(dt.timedelta(hours=1)))
    stato = {"riconciliazione_dovuta": {"Delivery": prima(days=2, hours=1)}}
    assert anomalie.riconciliazioni_dovute("sharepoint", stato, roma)[0]["giorni"] == 2


# --- Watermark fermo (P5) ----------------------------------------------------------------

GIRO = {"inizio": "2026-10-27T05:50:00Z", "fine": "2026-10-27T06:20:00Z", "risultati": 21,
        "piu_recente": "2026-10-26T18:00:00Z", "falliti": 0}


def test_watermark_fermo_senza_falliti():
    w = anomalie.watermark_fermo("sharepoint", {"watermark": "2026-10-19T16:22:49Z", "ultimo_giro": GIRO})
    assert {k: w[k] for k in ("fonte", "watermark", "piu_recente", "fine", "risultati", "falliti")} == {
        "fonte": "sharepoint", "watermark": "2026-10-19T16:22:49Z", "piu_recente": "2026-10-26T18:00:00Z",
        "fine": "2026-10-27T06:20:00Z", "risultati": 21, "falliti": 0}
    assert w["causa"] == "nessun fallito: `stato.py set-watermark sharepoint --da-giro`"
    assert w["messaggio"] == (
        "watermark di sharepoint fermo al 2026-10-19T16:22:49Z: l'ultimo giro (2026-10-27T06:20:00Z) ha "
        "21 risultati fino al 2026-10-26T18:00:00Z, più di 2 giorni dopo "
        "(nessun fallito: `stato.py set-watermark sharepoint --da-giro`)")


def test_watermark_fermo_con_falliti():
    w = anomalie.watermark_fermo("outlook", {"watermark": "2026-10-19T16:22:49Z", "ultimo_giro": {**GIRO, "falliti": 3}})
    assert w["falliti"] == 3 and w["causa"] == "3 falliti lo tengono fermo: riprova quei file"


@pytest.mark.parametrize("stato", [
    {"watermark": "2026-10-19T16:22:49Z"},                                       # nessun giro
    {"watermark": "2026-10-19T16:22:49Z", "ultimo_giro": {**GIRO, "risultati": 0}},  # giro vuoto
    {"watermark": "2026-10-25T00:00:00Z", "ultimo_giro": GIRO},                  # meno di 2 giorni
    {"watermark": "2026-10-26T18:00:00Z", "ultimo_giro": GIRO},                  # al passo
    {"watermark": None, "ultimo_giro": GIRO},                                    # mai impostato
    {"watermark": "2026-10-19T16:22:49Z", "ultimo_giro": "rotto"},
])
def test_watermark_non_fermo(stato):
    assert anomalie.watermark_fermo("sharepoint", stato) is None


# --- Voci orfane (P6) --------------------------------------------------------------------

def fm(item_id, versions=(), also_at=(), **altro):
    return {"type": "source-doc", "source": "sharepoint", "tags": [],
            "current": {"item_id": item_id}, "versions": list(versions), "also_at": list(also_at), **altro}


def test_voci_orfane_una_riga_per_nota():
    note = {
        "sources/sharepoint/delivery/a.md": fm("A2", versions=[{"item_id": "A1"}]),
        "sources/sharepoint/delivery/b.md": fm("B1"),
        "sources/sharepoint/delivery/c.md": fm("C1"),
    }
    voci = {"sharepoint": {
        "drv/A2": {"note": "sources/sharepoint/delivery/a.md"},
        "drv/A1": {"note": "sources/sharepoint/delivery/a.md"},
        "drv/A0": {"note": "sources/sharepoint/delivery/a.md"},
        "drv/X": {"note": "sources/sharepoint/delivery/b.md"},
        "drv/Y": {"note": "sources/sharepoint/delivery/b.md"},
        "drv/C1": {"note": "sources/sharepoint/delivery/c.md"},
    }}
    out = anomalie.voci_orfane(note, voci)
    assert [(o["nota"], o["orfane"], o["voci"], o["fonte"]) for o in out] == [
        ("sources/sharepoint/delivery/a.md", 1, 3, "sharepoint"),
        ("sources/sharepoint/delivery/b.md", 2, 2, "sharepoint")]
    assert out[0]["messaggio"] == ("1 voce dello stato (su 3) senza versione o copia nella nota: l'ID non è né in "
                                   "`current`, né in `versions`, né in `also_at` (`stato.py voci sharepoint <nota>`)")
    assert out[1]["messaggio"].startswith("2 voci dello stato (su 2)")


def test_voci_orfane_copia_in_also_at_e_note_escluse():
    voci = {"sharepoint": {"drv/K": {"note": "sources/sharepoint/a.md"},
                           "drv/Z": {"note": "sources/sharepoint/fuori.md"},
                           "drv/W": {"note": "sources/onedrive/w.md"},
                           "drv/T": {"note": "topics/t.md"}}}
    note = {
        "sources/sharepoint/a.md": fm("A", also_at=[{"item_id": "K"}]),           # copia: non orfana
        "sources/sharepoint/fuori.md": fm("A", tags=["fuori-perimetro"]),         # fuori perimetro
        "sources/onedrive/w.md": fm("A", source="onedrive"),                      # fonte senza stato letto
        "topics/t.md": fm("A"),                                                   # non in sources/
    }
    assert anomalie.voci_orfane(note, voci) == []


def test_incrociabile():
    assert anomalie.incrociabile("sources/sharepoint/a.md", fm("A"), {"sharepoint": {}})
    assert not anomalie.incrociabile("sources/sharepoint/a.md", fm("A", type="source-mail"), {"sharepoint": {}})
    assert not anomalie.incrociabile("sources/sharepoint/a.md", fm("A"), ("onedrive",))
    assert not anomalie.incrociabile("sources/sharepoint/a.md", None, ("sharepoint",))


# --- Hub da rileggere (P8) ---------------------------------------------------------------

def test_hub_da_rileggere_righe_eta_e_ordine(tmp_path):
    scrivi(tmp_path, "topics/tema-uno.md", "---\ntype: topic\n---\n\n## Punti chiave\n\n- Punto ([[doc-a]])\n"
           "- Da rileggere dopo [[doc-a]] v3 del 2026-10-29\n\n## Fonti\n\n- [[doc-a]]\n"
           "- Da rileggere dopo [[doc-b|Documento B]] v12 del 2026-10-21 · punti 2 e 3\n")
    scrivi(tmp_path, "clients/cliente-uno.md", "## Fonti\n\n  - Da rileggere dopo [[doc-c]] v2 del 2026-10-24\n")
    scrivi(tmp_path, "projects/alfa/alfa.md", "## Fonti\n\n- Da rileggere dopo [[doc-d]] v1 del 2026-10-23\n")
    # fuori dalle hub, o non nel formato: non contano
    scrivi(tmp_path, "sources/sharepoint/x.md", "- Da rileggere dopo [[doc-a]] v3 del 2026-10-01\n")
    scrivi(tmp_path, "journal/2026-10-30.md", "- Da rileggere dopo [[doc-a]] v3 del 2026-10-01\n")
    scrivi(tmp_path, "topics/tema-due.md", "- Da rileggere: [[doc-a]] v3 del 2026-10-01\n"
           "Testo che cita - Da rileggere dopo [[doc-a]] v3 del 2026-10-01\n")
    out = anomalie.hub_da_rileggere(tmp_path, dt.date(2026, 10, 31))
    assert [(h["hub"], h["fonte"], h["versione"], h["data"], h["giorni"], h["scaduta"]) for h in out] == [
        ("tema-uno", "doc-b", "v12", "2026-10-21", 10, True),
        ("alfa", "doc-d", "v1", "2026-10-23", 8, True),
        ("cliente-uno", "doc-c", "v2", "2026-10-24", 7, False),   # 7 giorni: non ancora «più di 7»
        ("tema-uno", "doc-a", "v3", "2026-10-29", 2, False)]
    assert out[1]["nota"] == "projects/alfa/alfa.md"
    # soglia diversa e oggi come testo
    out = anomalie.hub_da_rileggere(tmp_path, "2026-10-31", giorni=1)
    assert [h["scaduta"] for h in out] == [True, True, True, True]


def test_hub_da_rileggere_senza_cartelle(tmp_path):
    assert anomalie.hub_da_rileggere(tmp_path, dt.date(2026, 10, 31)) == []


# --- Giri anomali (P11) ------------------------------------------------------------------

def test_giri_anomali_tiene_mancanti_ed_errori():
    righe = [{"task": "a", "stato": "ok"}, {"task": "b", "stato": "mancante"},
             {"task": "c", "stato": "atteso"}, {"task": "d", "stato": "errore"}]
    assert [r["task"] for r in anomalie.giri_anomali(righe)] == ["b", "d"]


def test_soglie_solo_in_anomalie():
    """Ogni regola vive in un posto solo: le soglie non sono ridefinite negli altri script."""
    soglie = ("DOVUTA_AVVISO_GIORNI", "DOVUTA_ERRORE_GIORNI", "WATERMARK_FERMO_GIORNI", "HUB_DA_RILEGGERE_GIORNI")
    for p in SCRIPTS.glob("*.py"):
        if p.name == "anomalie.py":
            continue
        testo = p.read_text(encoding="utf-8")
        assert not any(re.search(rf"^{s}\s*=", testo, re.M) for s in soglie), p.name
