"""Test di perimetro.py (SPEC 5.1-5.2, ingestor §2 e §3.1)."""

import json
import sys

import pytest

from conftest import SCRIPTS, esegui, scrivi

sys.path.insert(0, str(SCRIPTS))
from perimetro import analizza  # noqa: E402

SP = "https://blueagesrl.sharepoint.com/sites/internal/"
OD = "https://blueagesrl-my.sharepoint.com/personal/lorenzo_curione_blueage_it/Documents/BlueAge/"


@pytest.mark.parametrize("url, cartella", [
    (SP + "SalesMarketing/Deck/BlueAge_CompanyProfile_v24.pdf", "sources/sharepoint/salesmarketing/deck"),
    (SP + "SalesMarketing/Offerte 2026/Offerta.docx", "sources/sharepoint/salesmarketing/offerte-2026"),
    (SP + "Shared%20Documents/Varie/Nota.md", "sources/sharepoint/shared-documents/varie"),
    (SP + "Delivery/Customers/01 Velo-CE/Progetto Dynamics/00 Progetto/Stato.md",
     "sources/sharepoint/delivery/customers/01-velo-ce/progetto-dynamics/00-progetto"),
    (OD + "01_Materiale clienti/Manini/Gruppi.xlsx", "sources/onedrive/01-materiale-clienti/manini"),
    (OD + "Nota.md", "sources/onedrive"),
    # maiuscole e %20 nel prefisso
    ("https://BlueAgeSrl.sharepoint.com/sites/Internal/salesmarketing/Deck/X.pdf",
     "sources/sharepoint/salesmarketing/deck"),
    (OD.replace(" ", "%20") + "06 Evidenze/Sintesi.pdf", "sources/onedrive/06-evidenze"),
])
def test_dentro(url, cartella):
    r = analizza(url)
    assert r["dentro"] is True, r
    assert r["cartella_nota"] == cartella


@pytest.mark.parametrize("url, motivo", [
    (SP + "SiteAssets/Blocco/Note.md", "libreria `SiteAssets`"),
    (SP + "Knowledge/Corso/M1.pdf", "libreria `Knowledge`"),
    (SP + "SalesMarketing/Deck/_originali/Deck.pptx", "_originali"),
    (SP + "Delivery/X/_sorgenti/a.md", "_sorgenti"),
    (SP + "Delivery/Velo-CE/05 Transcript/riunione.md", "Transcript"),
    (SP + "Delivery/Velo-CE/06 Evidenze/Export/tabella.xlsx", "Export"),
    (OD + "01_Materiale clienti/Manini/Progetto Automazione/Dati/ddt.pdf", "Dati"),
    (OD + "01_Materiale%20clienti/Manini/Progetto%20Automazione/dati/ddt.pdf", "dati"),
    (SP + "SalesMarketing/Deck/foto.png", "tipo `.png`"),
    ("https://blueagesrl.sharepoint.com/sites/partner/Partner/Condivisi/BlueAge_CompanyProfile.pdf", "sito `partner`"),
    ("https://blueagesrl-my.sharepoint.com/personal/lorenzo_curione_blueage_it/Documents/Altro/x.pdf", "BlueAge"),
])
def test_fuori(url, motivo):
    r = analizza(url)
    assert r["dentro"] is False, r
    assert motivo in r["motivo"]


def test_file_che_si_chiama_dati_non_e_una_cartella_esclusa():
    assert analizza(OD + "Manini/Dati.xlsx")["dentro"] is True


def test_altri_siti_e_onedrive_fuori_cartella():
    r = analizza("https://blueagesrl.sharepoint.com/sites/partner/Partner/Condivisi/BlueAge_CompanyProfile.pdf")
    assert r["fonte"] == "sharepoint" and r["cartella_nota"] == "sources/sharepoint/_partner/partner/condivisi"
    r = analizza("https://blueagesrl-my.sharepoint.com/personal/lorenzo_curione_blueage_it/Documents/Altro/x.pdf")
    assert r["fonte"] == "onedrive" and r["cartella_nota"] is None


def test_riga_di_comando_e_codici_di_uscita(vault):
    res = esegui("perimetro.py", vault, SP + "SalesMarketing/Deck/X_v2.pdf", "--json")
    assert res.returncode == 0
    out = json.loads(res.stdout)
    assert set(out) == {"dentro", "motivo", "fonte", "libreria", "cartella_nota", "tipo_processato"}
    assert out["fonte"] == "sharepoint" and out["libreria"] == "SalesMarketing"
    assert esegui("perimetro.py", vault, OD + "Clienti/Dati/x.pdf").returncode == 1
    res = esegui("perimetro.py", vault, "https://example.com/x.pdf", "--json")
    assert res.returncode == 2 and json.loads(res.stdout)["fonte"] is None


def test_verifica_sul_mini_vault(vault):
    scrivi(vault, "sources/sharepoint/delivery/doc-alfa.md",
           (vault / "sources/sharepoint/delivery/doc-alfa.md").read_text(encoding="utf-8").replace(
               "https://example.sharepoint.com/sites/internal/Delivery/Doc_Alfa_v2.pdf",
               SP + "Delivery/Doc_Alfa_v2.pdf"))
    res = esegui("perimetro.py", vault, "--verifica", "--json")
    out = json.loads(res.stdout)
    assert res.returncode == 0 and out["note"] == 1 and out["uguali"] == 1
