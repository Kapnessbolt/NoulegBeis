"""Test di plancia.py sul mini-vault di conftest.py."""

import json

import pytest

from conftest import esegui

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
