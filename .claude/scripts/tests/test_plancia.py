"""Test di plancia.py sul mini-vault di conftest.py."""

import json

import pytest

from conftest import esegui, scrivi

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
