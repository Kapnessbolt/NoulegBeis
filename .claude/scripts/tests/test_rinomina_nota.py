"""Test di rinomina-nota.py (SPEC 4.4) sul mini-vault di conftest.py."""

import json

from conftest import esegui


def rinomina(root, vecchio, nuovo):
    return esegui("rinomina-nota.py", root, vecchio, nuovo)


def test_rinomina_nota_aggiorna_wikilink(vault):
    res = rinomina(vault, "tema-uno", "tema-rinominato")
    assert res.returncode == 0, res.stderr
    assert not (vault / "topics/tema-uno.md").exists()
    assert (vault / "topics/tema-rinominato.md").exists()
    for rel in ("sources/sharepoint/delivery/doc-alfa.md", "sessions/2026-10-20-prova.md",
                "inbox/2026-10-20-idea.md"):
        testo = (vault / rel).read_text(encoding="utf-8")
        assert "[[tema-uno]]" not in testo
        assert "[[tema-rinominato]]" in testo
    assert esegui("controlla-vault.py", vault).returncode == 0


def test_rinomina_fonte_aggiorna_lo_stato(vault):
    res = rinomina(vault, "doc-alfa", "doc-alfa-pilota")
    assert res.returncode == 0, res.stderr
    stato = json.loads((vault / ".state/ingest.json").read_text(encoding="utf-8"))
    assert stato["sharepoint"]["items"]["item-1"]["note"] == "sources/sharepoint/delivery/doc-alfa-pilota.md"
    testo = (vault / "projects/alfa/alfa.md").read_text(encoding="utf-8")
    assert "[[doc-alfa]]" not in testo and testo.count("[[doc-alfa-pilota]]") == 6
    assert esegui("controlla-vault.py", vault).returncode == 0


def test_rinomina_progetto_sposta_cartella_scheda_e_log(vault):
    res = rinomina(vault, "alfa", "gamma")
    assert res.returncode == 0, res.stderr
    assert (vault / "projects/gamma/gamma.md").exists()
    assert (vault / "projects/gamma/gamma-log.md").exists()
    assert not (vault / "projects/alfa").exists()
    assert "[[gamma]]" in (vault / "projects/gamma/gamma-log.md").read_text(encoding="utf-8")
    assert "[[gamma]]" in (vault / "clients/cliente-uno.md").read_text(encoding="utf-8")
    assert esegui("controlla-vault.py", vault).returncode == 0


def test_rinomina_rifiuta_slug_esistente_o_non_valido(vault):
    assert rinomina(vault, "tema-uno", "mario-rossi").returncode != 0
    assert rinomina(vault, "tema-uno", "Tema Nuovo").returncode != 0
    assert (vault / "topics/tema-uno.md").exists()
