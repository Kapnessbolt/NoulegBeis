"""Test di perimetro.py (SPEC 5.1-5.2, ingestor §2 e §3.1)."""

import json
import sys

import pytest

from conftest import CARTELLA_OD, SCRIPTS, TENANT_OD, TENANT_SP, UTENTE_OD, esegui, scrivi

sys.path.insert(0, str(SCRIPTS))
from perimetro import analizza  # noqa: E402

# Tenant e cartella di OneDrive finti, da `vault.yaml` del mini-vault (conftest.py)
SP = f"{TENANT_SP}/sites/internal/"
OD = f"{TENANT_OD}/personal/{UTENTE_OD}/Documents/{CARTELLA_OD}/"
PARTNER = f"{TENANT_SP}/sites/partner/Partner/Condivisi/Company_Profile.pdf"
OD_ALTRO = f"{TENANT_OD}/personal/{UTENTE_OD}/Documents/Altro/x.pdf"


@pytest.mark.parametrize("url, cartella", [
    (SP + "SalesMarketing/Deck/Company_Profile_v24.pdf", "sources/sharepoint/salesmarketing/deck"),
    (SP + "SalesMarketing/Offerte 2026/Offerta.docx", "sources/sharepoint/salesmarketing/offerte-2026"),
    (SP + "Shared%20Documents/Varie/Nota.md", "sources/sharepoint/shared-documents/varie"),
    (SP + "Delivery/Customers/01 Velo-CE/Progetto Dynamics/00 Progetto/Stato.md",
     "sources/sharepoint/delivery/customers/01-velo-ce/progetto-dynamics/00-progetto"),
    (OD + "01_Materiale clienti/Manini/Gruppi.xlsx", "sources/onedrive/01-materiale-clienti/manini"),
    (OD + "Nota.md", "sources/onedrive"),
    # maiuscole e %20 nel prefisso
    ("https://Example.SharePoint.com/sites/Internal/salesmarketing/Deck/X.pdf",
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
    (PARTNER, "sito `partner`"),
    (OD_ALTRO, f"cartella `{CARTELLA_OD}/`"),
])
def test_fuori(url, motivo):
    r = analizza(url)
    assert r["dentro"] is False, r
    assert motivo in r["motivo"]


def test_file_che_si_chiama_dati_non_e_una_cartella_esclusa():
    assert analizza(OD + "Manini/Dati.xlsx")["dentro"] is True


def test_altri_siti_e_onedrive_fuori_cartella():
    r = analizza(PARTNER)
    assert r["fonte"] == "sharepoint" and r["cartella_nota"] == "sources/sharepoint/_partner/partner/condivisi"
    r = analizza(OD_ALTRO)
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
    res = esegui("perimetro.py", vault, "--verifica", "--json")
    out = json.loads(res.stdout)
    assert res.returncode == 0 and out["note"] == 1 and out["uguali"] == 1
    # Un URL di un altro tenant: la cartella non si calcola e l'accordo scende sotto il 90%
    scrivi(vault, "sources/sharepoint/delivery/doc-alfa.md",
           (vault / "sources/sharepoint/delivery/doc-alfa.md").read_text(encoding="utf-8").replace(
               TENANT_SP, "https://altro.sharepoint.com"))
    res = esegui("perimetro.py", vault, "--verifica", "--json")
    out = json.loads(res.stdout)
    assert res.returncode == 1 and out["uguali"] == 0 and out["disaccordi"][0]["calcolata"] is None


def test_perimetro_da_vault_yaml(vault):
    """Tenant e librerie vengono da vault.yaml: con un altro tenant lo stesso URL è fuori."""
    p = vault / "vault.yaml"
    p.write_text(p.read_text(encoding="utf-8").replace(TENANT_SP, "https://altro.sharepoint.com")
                 .replace("librerie: [SalesMarketing, Delivery, Shared Documents]", "librerie: [Delivery]"),
                 encoding="utf-8")
    assert esegui("perimetro.py", vault, SP + "Delivery/X.pdf").returncode == 2
    assert esegui("perimetro.py", vault, "https://altro.sharepoint.com/sites/internal/Delivery/X.pdf").returncode == 0
    res = esegui("perimetro.py", vault, "https://altro.sharepoint.com/sites/internal/SalesMarketing/X.pdf")
    assert res.returncode == 1 and "libreria `SalesMarketing` fuori perimetro" in res.stdout
