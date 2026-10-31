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
    # il motivo nomina il prefisso trovato, non la configurazione intera
    assert r["motivo"].startswith("prefisso `https://") and "{" not in r["motivo"], r["motivo"]


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


# --- Lista di prefissi (P13) --------------------------------------------------------------

def test_vince_il_primo_prefisso_della_lista(vault):
    """Una libreria in più è una voce in più di `posizioni`: lo stesso URL passa da «libreria
    fuori perimetro» (riconoscitore `<tenant>/sites/`) a dentro, con la sua cartella di nota."""
    url = SP + "Archivio/2025/Verbale.pdf"
    res = esegui("perimetro.py", vault, url, "--json")
    assert res.returncode == 1 and json.loads(res.stdout)["motivo"] == "libreria `Archivio` fuori perimetro"
    p = vault / "vault.yaml"
    p.write_text(p.read_text(encoding="utf-8").replace(
        "librerie: [SalesMarketing, Delivery, Shared Documents]",
        "librerie: [SalesMarketing, Delivery, Shared Documents, Archivio]"), encoding="utf-8")
    res = esegui("perimetro.py", vault, url, "--json")
    out = json.loads(res.stdout)
    assert res.returncode == 0 and out["motivo"] == f"prefisso `{SP}Archivio/`"
    assert out["cartella_nota"] == "sources/sharepoint/archivio/2025"


@pytest.mark.parametrize("url, motivo", [
    (f"{TENANT_SP}/sites/internal", "URL di SharePoint senza libreria o file"),
    (SP + "Delivery/", "URL di SharePoint senza libreria o file"),
    (f"{TENANT_OD}/personal/{UTENTE_OD}/Documents", "URL di OneDrive senza libreria o file"),
    ("https://altro.sharepoint.com/sites/internal/Delivery/X.pdf", "URL non di SharePoint o OneDrive del tenant"),
])
def test_url_non_riconosciuti(url, motivo):
    r = analizza(url)
    assert r["riconosciuto"] is False and r["motivo"] == motivo and r["fonte"] is None


def test_link_di_condivisione_e_query_come_l_url_diretto():
    diretto = analizza(SP + "Delivery/Velo/Stato.xlsx")
    condiviso = analizza(f"{TENANT_SP}/:x:/r/sites/internal/Delivery/Velo/Stato.xlsx?d=w1&csf=1&web=1")
    assert condiviso == diretto and diretto["cartella_nota"] == "sources/sharepoint/delivery/velo"


def test_onedrive_con_doppia_barra_come_oggi():
    """La cartella di nota si confronta per segmenti, il prefisso come testo: una doppia barra
    lascia il file fuori ma con la sua cartella, come prima della lista di prefissi."""
    r = analizza(f"{TENANT_OD}/personal/{UTENTE_OD}//Documents/{CARTELLA_OD}/Manini/a.pdf")
    assert r["dentro"] is False and r["motivo"] == f"OneDrive fuori dalla cartella `{CARTELLA_OD}/`"
    assert r["cartella_nota"] == "sources/onedrive/manini"


# --- Profondità del rilevatore (--profondita, SPEC 6.2 passo 7, 13.1 step 18) -------------

ESEMPIO_PROFONDITA = [
    SP + "SalesMarketing/Deck/a.pdf",
    SP + "SalesMarketing/Casi/Velo/b.pptx",
    SP + "SalesMarketing/radice.pdf",                                   # nella radice: ignorato
    SP + "Delivery/Customers/01 Velo-CE/Progetto Dynamics/00 Progetto/Stato.md",
    SP + "Delivery/99 - old versions/x.pdf",                            # cartella esclusa: ignorato
    SP + "Delivery/Customers/_originali/A/B/C/D/E/F/vecchio.pdf",       # cartella esclusa: ignorato
    OD + "01_Materiale clienti/Manini/Gruppi.xlsx",
    OD + "Nota.md",                                                     # nella radice: ignorato
    SP + "Knowledge/Corso/Modulo/Lezione/M1.pdf",                       # fuori perimetro: ignorato
    f"{TENANT_SP}/sites/partner/Partner/A/B/C/x.pdf",                   # altro sito: ignorato
    f"{TENANT_OD}/personal/{UTENTE_OD}/Documents/Altro/A/B/C/x.pdf",    # fuori dalla cartella: ignorato
]


def elenco(root, urls, forma="lista"):
    voci = [{"id": f"id-{i}", "name": u.rsplit("/", 1)[-1], "webUrl": u} for i, u in enumerate(urls)]
    voci.append({"id": "cartella", "name": "Customers", "webUrl": SP + "Delivery/Customers", "folder": {}})
    return scrivi(root, "elenco.json", json.dumps({"value": voci} if forma == "value" else voci))


def con_old_versions(root):
    """Il mini-vault non esclude `old versions`: lo aggiunge come nel vault reale."""
    p = root / "vault.yaml"
    p.write_text(p.read_text(encoding="utf-8").replace(
        "cartelle: [siteassets, _originali, _sorgenti, dati]",
        "cartelle: [siteassets, _originali, _sorgenti, dati, old versions]"), encoding="utf-8")


def test_profondita_json(vault):
    con_old_versions(vault)
    res = esegui("perimetro.py", vault, "--profondita", elenco(vault, ESEMPIO_PROFONDITA, forma="value"), "--json")
    assert res.returncode == 0, res.stderr
    out = json.loads(res.stdout)
    assert out["profondita"] == {"SalesMarketing": 2, "Delivery": 4, "OneDrive": 2}
    assert list(out["profondita"]) == ["SalesMarketing", "Delivery", "OneDrive"]  # ordine del perimetro
    assert out["senza_file"] == ["Shared Documents"]
    assert out["file"] == 4
    assert out["yaml"] == "profondita:\n  SalesMarketing: 2\n  Delivery: 4\n  OneDrive: 2\n"


def test_profondita_si_ferma_alla_prima_cartella_con_file(vault):
    """Un file in `Customers` rende `Customers` la prima cartella con file del ramo: 1."""
    urls = [SP + "Delivery/Customers/leggimi.md",
            SP + "Delivery/Customers/01 Velo-CE/Progetto Dynamics/00 Progetto/Stato.md"]
    out = json.loads(esegui("perimetro.py", vault, "--profondita", elenco(vault, urls), "--json").stdout)
    assert out["profondita"] == {"Delivery": 1}
    assert out["senza_file"] == ["SalesMarketing", "Shared Documents", "OneDrive"]


def test_profondita_anche_tipi_non_processati_e_al_massimo_sei(vault):
    # web_url al posto di webUrl, come accetta riconcilia.py --elenco
    scrivi(vault, "elenco.json", json.dumps([
        {"web_url": SP + "Shared Documents/A/B/C/D/E/F/G/H/foto.png", "name": "foto.png"},
        {"web_url": OD + "A/video.mp4", "name": "video.mp4"},
    ]))
    out = json.loads(esegui("perimetro.py", vault, "--profondita", vault / "elenco.json", "--json").stdout)
    assert out["profondita"] == {"Shared Documents": 6, "OneDrive": 1} and out["file"] == 2


def test_profondita_testo(vault):
    con_old_versions(vault)
    res = esegui("perimetro.py", vault, "--profondita", elenco(vault, ESEMPIO_PROFONDITA))
    assert res.returncode == 0, res.stderr
    righe = res.stdout.splitlines()
    assert righe[:3] == ["SalesMarketing: 2", "Delivery: 4", "OneDrive: 2"]
    assert "Shared Documents" in righe[3] and righe[4] == "4 file considerati"
    assert res.stdout.endswith("profondita:\n  SalesMarketing: 2\n  Delivery: 4\n  OneDrive: 2\n")


def test_profondita_snippet_valido_per_vault_yaml(vault):
    """Lo snippet, messo sotto `fonti.rilevatore`, passa la validazione di config.py."""
    con_old_versions(vault)
    out = json.loads(esegui("perimetro.py", vault, "--profondita", elenco(vault, ESEMPIO_PROFONDITA),
                            "--json").stdout)
    blocco = "".join(f"    {r}\n" for r in out["yaml"].splitlines())
    p = vault / "vault.yaml"
    p.write_text(p.read_text(encoding="utf-8").replace(
        "  tipi_processati: [pdf, docx, pptx, xlsx, md, txt]\n",
        "  tipi_processati: [pdf, docx, pptx, xlsx, md, txt]\n  rilevatore:\n" + blocco), encoding="utf-8")
    res = esegui("config.py", vault, "rilevatore")
    assert res.returncode == 0, res.stderr
    assert json.loads(res.stdout)["profondita"] == {"SalesMarketing": 2, "Delivery": 4,
                                                    "Shared Documents": 2, "OneDrive": 2}


@pytest.mark.parametrize("contenuto", [None, "non è json", '{"value": 3}', "[1, 2]", '[{"name": "a.pdf"}]'])
def test_profondita_elenco_illeggibile(vault, contenuto):
    if contenuto is not None:
        scrivi(vault, "elenco.json", contenuto)
    res = esegui("perimetro.py", vault, "--profondita", vault / "elenco.json")
    assert res.returncode == 2 and "--profondita: elenco" in res.stderr and res.stdout == ""


def test_profondita_senza_file_da_leggere(vault):
    assert esegui("perimetro.py", vault, "--profondita").returncode == 2
