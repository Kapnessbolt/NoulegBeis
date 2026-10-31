"""Test di plancia.py sul mini-vault di conftest.py."""

import json
import re

import pytest

from conftest import aggiungi, esegui, git, leggi_stato, scrivi

FILE = ("progetti", "attivita", "log", "inbox", "task", "digest")


@pytest.fixture
def plancia(vault, tmp_path):
    out = tmp_path / "plancia"
    res = esegui("plancia.py", vault, out)
    assert res.returncode == 0, res.stderr
    return {nome: json.loads((out / f"{nome}.json").read_text(encoding="utf-8")) for nome in FILE}


def test_produce_i_sei_json(vault, tmp_path):
    out = tmp_path / "plancia"
    res = esegui("plancia.py", vault, out)
    assert res.returncode == 0, res.stderr
    assert sorted(p.name for p in out.iterdir()) == sorted(f"{n}.json" for n in FILE)
    for nome in FILE:
        assert isinstance(json.loads((out / f"{nome}.json").read_text(encoding="utf-8")), list)
    assert "2 progetti, 5 attività, 1 note in inbox" in res.stdout


def test_conta_progetti_e_attivita_aperte(plancia):
    progetti = {p["progetto"]: p for p in plancia["progetti"]}
    assert set(progetti) == {"alfa", "beta"}
    assert progetti["alfa"]["aperte"] == 2
    assert progetti["alfa"]["prossima"] == "2026-11-05"
    assert progetti["alfa"]["prossima_testo"] == "Inviare la proposta"
    assert progetti["alfa"]["clienti"] == "Cliente Uno"
    assert progetti["alfa"]["ultimo_log"] == "2026-10-20"
    assert progetti["beta"]["aperte"] == 0
    assert progetti["beta"]["stato"] == "in-pausa"


def test_attivita_aperte_e_chiuse(plancia):
    attivita = plancia["attivita"]
    assert len(attivita) == 5
    assert sum(1 for a in attivita if a["fatta"]) == 2
    assert sum(1 for a in attivita if not a["fatta"]) == 3
    per_origine = {o: [a for a in attivita if a["origine"] == o] for o in ("progetto", "inbox")}
    assert len(per_origine["progetto"]) == 4 and len(per_origine["inbox"]) == 1
    proposta = next(a for a in attivita if a["testo"] == "Inviare la proposta")
    assert proposta["scadenza"] == "2026-11-05" and proposta["fonte"] == "doc-alfa"


def test_inbox_e_log(plancia):
    assert plancia["inbox"] == [{"nota": "2026-10-20-idea", "titolo": "Idea da smistare",
                                 "creata": "2026-10-20", "aperte": 1, "prossima": "2026-11-01"}]
    assert [p["data"] for p in plancia["log"]] == ["2026-10-20", "2026-10-15"]
    assert plancia["log"][0]["testo"] == "Avvio del caso pilota"


def test_campi_della_pagina_cockpit(vault, tmp_path):
    """Campi aggiunti per cockpit.py: percorso, clienti_slug, prossimi_passi, scadute, prossima_fonte."""
    scheda = vault / "projects" / "alfa" / "alfa.md"
    testo = scheda.read_text(encoding="utf-8")
    testo = testo.replace("## Prossimi passi\n\n-\n",
                          "## Prossimi passi\n\n- Demo a [[mario-rossi]] ([[doc-alfa]])\n-\n- Poi il secondo reparto\n")
    testo = testo.replace("- [ ] Preparare la demo ([[doc-alfa]])",
                          "- [ ] Preparare la demo 📅 2020-01-10 ([[2026-10-20-prova]])")
    scheda.write_text(testo, encoding="utf-8")
    out = tmp_path / "plancia"
    res = esegui("plancia.py", vault, out)
    assert res.returncode == 0, res.stderr
    progetti = {p["progetto"]: p for p in json.loads((out / "progetti.json").read_text(encoding="utf-8"))}
    alfa, beta = progetti["alfa"], progetti["beta"]
    assert alfa["percorso"] == "projects/alfa/alfa.md"
    assert alfa["clienti_slug"] == ["cliente-uno"]
    assert alfa["prossimi_passi"] == ["Demo a Mario Rossi", "Poi il secondo reparto"]
    assert alfa["scadute"] == 1
    assert alfa["prossima"] == "2020-01-10" and alfa["prossima_fonte"] == "2026-10-20-prova"
    assert beta["percorso"] == "projects/beta/beta.md"
    assert beta["clienti_slug"] == [] and beta["prossimi_passi"] == []
    assert beta["scadute"] == 0 and beta["prossima_fonte"] == ""


DIGEST = """---
type: journal
date: 2026-10-21
---

# Digest 2026-10-21

## Novità ingerite

- [[doc-alfa]] · nuova · documento del pilota
- [[tema-uno]] · nuova
- [[doc-alfa]] · nuova versione · D41 aggiunta
- [[doc-alfa]] · nuova versione · §9 riscritto
- [[cliente-uno]] · aggiornata · riletta
- [[mario-rossi]], [[alfa]] · aggiornate · nuova interazione

## Decisioni

- Da spuntare: inviare la proposta · [[alfa]]
- 2026-10-21 · [[alfa]] · Si parte da un solo reparto
  - dettaglio di secondo livello, non conta
- Nuove righe nei log (21/10): [[alfa]] 1
-
- Nessun progetto fermo: tutti i log hanno righe negli ultimi 14 giorni
- Nessuna proposta nuova dall'ingestor
- Progetti fermi: nessuno (tutti i log hanno righe negli ultimi 14 giorni)

## Esito dei task

| Task | Esito |
|---|---|
"""


def leggi_digest(vault, tmp_path):
    scrivi(vault, "journal/2026-10-21.md", DIGEST)
    out = tmp_path / "plancia"
    res = esegui("plancia.py", vault, out)
    assert res.returncode == 0, res.stderr
    return json.loads((out / "digest.json").read_text(encoding="utf-8"))[0]


def test_digest_nuova_versione_e_aggiornamento(vault, tmp_path):
    """Una "nuova versione" è un aggiornamento, non una nota nuova (digest del 27/10: 6 invece di 2)."""
    d = leggi_digest(vault, tmp_path)
    assert d["giorno"] == "2026-10-21"
    assert d["note_nuove"] == 2
    assert d["note_aggiornate"] == 4          # 2 nuove versioni, 1 aggiornata, 1 riga "aggiornate"


def test_digest_conta_le_decisioni_senza_data(vault, tmp_path):
    """Contano i punti di primo livello di `## Decisioni`, con o senza data; non "-" né i "nessun…"."""
    assert leggi_digest(vault, tmp_path)["decisioni"] == 3


def test_task_espone_l_ultimo_giro_per_fonte(vault, tmp_path):
    """P5 dell'audit 2026-10-31: `ultimo_giro` di ogni fonte nelle righe dei task di ingestion."""
    giro = {"inizio": "2026-10-31T05:50:00Z", "fine": "2026-10-31T06:20:00Z", "risultati": 21,
            "piu_recente": "2026-10-30T16:22:49Z", "falliti": 0}
    p = vault / ".state" / "sharepoint.json"
    stato = json.loads(p.read_text(encoding="utf-8"))
    stato["ultimo_giro"] = giro
    p.write_text(json.dumps(stato), encoding="utf-8")
    out = tmp_path / "plancia"
    res = esegui("plancia.py", vault, out)
    assert res.returncode == 0, res.stderr
    task = json.loads((out / "task.json").read_text(encoding="utf-8"))
    per_task = {t["task"]: t for t in task}
    assert per_task["ingest-sharepoint"]["ultimo_giro"] == {"sharepoint": giro, "onedrive": None}
    assert per_task["ingest-outlook"]["ultimo_giro"] == {"outlook": None}
    assert per_task["digest"]["ultimo_giro"] == {}


# --- --anomalie: verifica dei giri e hub da rileggere per il digest (audit 2026-10-31, P8 e P11)

# Il giorno prima del giorno controllato (21/10): tutti i giri del martedì tranne il cockpit
# delle 13:40, e l'ingest-outlook delle 13:15 in errore.
RIGHE_IERI = """| ingest-sharepoint 06:52 | OK · 1 nota nuova |
| ingest-outlook 07:06 | OK |
| ingest-github 07:21 | OK |
| cockpit 07:41 | OK · pagina ripubblicata |
| digest 07:46 | OK |
| ingest-outlook 13:16 | ERRORE · timeout del connettore |
"""


def digest_di(giorno, righe):
    return (f"---\ntype: journal\ndate: {giorno}\n---\n\n# Digest {giorno}\n\n## Novità ingerite\n\n-\n\n"
            "## Attività in scadenza\n\n-\n\n## Decisioni\n\n-\n\n## Scartate\n\n-\n\n"
            "## Controllo del vault\n\n-\n\n## Esito dei task\n\n| Task | Esito |\n|---|---|\n" + righe)


def cambia_stato(vault, fonte, **chiavi):
    data = leggi_stato(vault, fonte)
    data.update(chiavi)
    (vault / ".state" / f"{fonte}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")


@pytest.fixture
def con_anomalie(vault):
    scrivi(vault, "journal/2026-10-20.md", digest_di("2026-10-20", RIGHE_IERI))
    cambia_stato(vault, "sharepoint", watermark="2026-10-10T00:00:00Z",
                 ultimo_giro={"inizio": "2026-10-20T04:50:00Z", "fine": "2026-10-20T05:10:00Z", "risultati": 5,
                              "piu_recente": "2026-10-19T10:00:00Z", "falliti": 2},
                 riconciliazione_dovuta={"Delivery": "2026-10-18T05:00:00Z"})
    # dovuta da meno di un giorno: non è ancora un'anomalia
    cambia_stato(vault, "onedrive", riconciliazione_dovuta={"Lavoro": "2026-10-21T01:00:00Z"})
    tema = vault / "topics" / "tema-uno.md"
    tema.write_text(tema.read_text(encoding="utf-8").replace(
        "## Fonti\n\n- [[doc-alfa]]\n",
        "## Fonti\n\n- [[doc-alfa]]\n- Da rileggere dopo [[doc-alfa]] v2 del 2026-10-11\n"
        "- Da rileggere dopo [[doc-alfa|Documento Alfa]] v3 del 2026-10-19 · solo i numeri\n"), encoding="utf-8")
    return vault


def anomalie_json(vault, *args):
    res = esegui("plancia.py", vault, "--anomalie", *args, "--json")
    assert res.returncode == 0, res.stderr
    return json.loads(res.stdout)


def test_anomalie_json(con_anomalie):
    r = anomalie_json(con_anomalie, "--giorno", "2026-10-21", "--ora", "07:00")
    assert (r["giorno"], r["ora"]) == ("2026-10-21", "07:00")
    righe = [e["riga"] for e in r["esito_task"]]
    assert righe == [
        "- Anomalia · giro in errore: ingest-outlook 13:16 del 2026-10-20 · ERRORE · timeout del connettore",
        "- Anomalia · giro mancante: cockpit atteso alle 13:40 del 2026-10-20, nessuna riga nel digest",
        "- Anomalia · watermark fermo: sharepoint al 2026-10-10T00:00:00Z, ultimo giro del 2026-10-20T05:10:00Z "
        "con 5 risultati fino al 2026-10-19T10:00:00Z (2 falliti lo tengono fermo: riprova quei file)",
        "- Anomalia · riconciliazione dovuta: Delivery (sharepoint) dal 2026-10-18T05:00:00Z (3 giorni) · "
        "/ingest riconcilia sharepoint:Delivery",
        # conftest: la voce `item-1` non è l'item_id della nota
        "- Anomalia · voci orfane: 1 note con 1 voci dello stato senza versione o copia (controlla-vault.py)",
    ], righe
    per_tipo = {e["tipo"]: e for e in r["esito_task"]}
    assert per_tipo["giro_mancante"]["task"] == "cockpit" and per_tipo["giro_mancante"]["giorno"] == "2026-10-20"
    assert per_tipo["riconciliazione_dovuta"]["libreria"] == "Delivery"
    assert per_tipo["riconciliazione_dovuta"]["livello"] == "avviso"
    assert per_tipo["watermark_fermo"]["falliti"] == 2
    assert (per_tipo["voci_orfane"]["note"], per_tipo["voci_orfane"]["voci"]) == (1, 1)
    assert r["decisioni"] == [{
        "tipo": "hub_da_rileggere",
        "riga": "- Da rileggere: [[tema-uno]] · dopo [[doc-alfa]] v2 del 2026-10-11 (10 giorni)",
        "hub": "tema-uno", "nota": "topics/tema-uno.md", "fonte": "doc-alfa", "versione": "v2",
        "data": "2026-10-11", "giorni": 10}]
    assert r["conteggi"] == {
        "giri_mancanti": 1, "giri_in_errore": 1, "stati_illeggibili": 0, "watermark_fermi": 1,
        "riconciliazioni_dovute": 1, "note_con_voci_orfane": 1, "voci_orfane": 1,
        "hub_da_rileggere": 1, "hub_da_rileggere_scadute": 1}


def test_anomalie_testo(con_anomalie):
    res = esegui("plancia.py", con_anomalie, "--anomalie", "--giorno", "2026-10-21", "--ora", "07:00")
    assert res.returncode == 0, res.stderr
    esito, decisioni = res.stdout.split("## Decisioni")
    assert esito.startswith("## Esito dei task\n\n- Anomalia · giro in errore: ingest-outlook 13:16")
    punti = [r for r in esito.splitlines() if r.startswith("- ")]
    assert len(punti) == 5 and all(r.startswith("- Anomalia · ") for r in punti)
    assert decisioni.strip().splitlines() == [
        "- Da rileggere: [[tema-uno]] · dopo [[doc-alfa]] v2 del 2026-10-11 (10 giorni)",
        "- Da rileggere (entro 7 giorni): 1 hub"]


def test_anomalie_giri_di_oggi_secondo_l_ora(con_anomalie):
    """Alle 08:00 del 21/10 senza digest i giri delle 06:50 e delle 07:05 sono mancanti, gli altri attesi."""
    r = anomalie_json(con_anomalie, "--giorno", "2026-10-21", "--ora", "08:00")
    mancanti = [(e["task"], e["atteso"], e["giorno"]) for e in r["esito_task"] if e["tipo"] == "giro_mancante"]
    assert mancanti == [("cockpit", "13:40", "2026-10-20"), ("ingest-sharepoint", "06:50", "2026-10-21"),
                        ("ingest-outlook", "07:05", "2026-10-21")]


def test_anomalie_giorno_passato_senza_ora_vale_23_59(con_anomalie):
    r = anomalie_json(con_anomalie, "--giorno", "2026-10-20")
    assert r["ora"] == "23:59"
    assert ("cockpit", "13:40") in [(e["task"], e["atteso"]) for e in r["esito_task"] if e["tipo"] == "giro_mancante"]


def test_anomalie_nessuna(vault):
    """Stato e nota allineati, tutti i giri di ieri nel digest, nessuna hub da rileggere."""
    nota = vault / "sources/sharepoint/delivery/doc-alfa.md"
    item = re.search(r'item_id: "([^"]+)"', nota.read_text(encoding="utf-8")).group(1)
    cambia_stato(vault, "sharepoint", items={f"drive-1/{item}": {
        "last_modified": "2026-10-01T10:00:00Z", "note": "sources/sharepoint/delivery/doc-alfa.md"}})
    scrivi(vault, "journal/2026-10-20.md", digest_di("2026-10-20", RIGHE_IERI.replace(
        "ERRORE · timeout del connettore", "OK") + "| cockpit 13:41 | OK |\n"))
    res = esegui("plancia.py", vault, "--anomalie", "--giorno", "2026-10-21", "--ora", "07:00")
    assert res.returncode == 0, res.stderr
    assert res.stdout == "## Esito dei task\n\nNessuna anomalia.\n"
    r = anomalie_json(vault, "--giorno", "2026-10-21", "--ora", "07:00")
    assert r["esito_task"] == [] and r["decisioni"] == []
    assert set(r["conteggi"].values()) == {0}
    # una sola riga «Da rileggere» recente: il blocco decisioni ha solo il conteggio
    aggiungi(vault, "topics/tema-uno.md", "- Da rileggere dopo [[doc-alfa]] v3 del 2026-10-20")
    res = esegui("plancia.py", vault, "--anomalie", "--giorno", "2026-10-21", "--ora", "07:00")
    assert res.stdout == ("## Esito dei task\n\nNessuna anomalia.\n\n## Decisioni\n\n"
                          "- Da rileggere (entro 7 giorni): 1 hub\n")


def test_anomalie_stato_illeggibile_o_mancante(con_anomalie):
    scrivi(con_anomalie, ".state/outlook.json", "{rotto")
    (con_anomalie / ".state" / "onedrive.json").unlink()
    cambia_stato(con_anomalie, "sharepoint", riconciliazione_dovuta={"Delivery": "ieri"})
    r = anomalie_json(con_anomalie, "--giorno", "2026-10-21", "--ora", "07:00")
    illeggibili = [e for e in r["esito_task"] if e["tipo"] == "stato_illeggibile"]
    assert [e["fonte"] for e in illeggibili] == ["sharepoint", "outlook"]
    assert illeggibili[0]["riga"] == ("- Anomalia · stato di sharepoint illeggibile: "
                                      "`riconciliazione_dovuta` di Delivery: istante `ieri` non valido")
    assert illeggibili[1]["riga"].startswith("- Anomalia · stato di outlook illeggibile: ")
    assert r["conteggi"]["stati_illeggibili"] == 2 and r["conteggi"]["riconciliazioni_dovute"] == 0
    assert not any(e.get("fonte") == "onedrive" for e in r["esito_task"])


@pytest.mark.parametrize("args", [
    ("--giorno", "2026-13-01"), ("--giorno", "ieri"), ("--ora", "25:00"), ("--ora", "7:00"), ("--boh",),
])
def test_anomalie_argomenti_non_validi(vault, args):
    res = esegui("plancia.py", vault, "--anomalie", *args)
    assert res.returncode == 2, res.stdout


def test_anomalie_configurazione_non_valida(vault):
    scrivi(vault, "vault.yaml", "versione: 1\n")
    res = esegui("plancia.py", vault, "--anomalie")
    assert res.returncode == 2 and "Configurazione non valida" in res.stderr


def test_anomalie_non_scrive_file(con_anomalie):
    git(con_anomalie, "add", "-A")
    git(con_anomalie, "commit", "-q", "-m", "anomalie")
    assert esegui("plancia.py", con_anomalie, "--anomalie").returncode == 0
    assert git(con_anomalie, "status", "--porcelain").stdout == ""
