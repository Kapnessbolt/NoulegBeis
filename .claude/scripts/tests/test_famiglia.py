"""Test di famiglia.py (SPEC 4.3, ingestor §3.2): regole, coppie reali del vault, ricerca."""

import json
import sys

import pytest

from conftest import SCRIPTS, esegui, scrivi

sys.path.insert(0, str(SCRIPTS))
from famiglia import famiglia, slug, slug_oggetto  # noqa: E402

# Coppie reali (current.name → family) su cui lo script è d'accordo con il vault al 26/10/2026.
# Dataset fisso: i test non leggono il vault reale.
COPPIE_REALI = [
    ("BlueAge_CompanyProfile_v24.pdf", "blueage-companyprofile"),
    ("BlueAge_CompanyProfile.pdf", "blueage-companyprofile"),
    ("BlueAge_AI_che_cresce_onepage_v2.pdf", "blueage-ai-che-cresce-onepage"),
    ("Policy_AI_MTU_signed.pdf", "policy-ai-mtu"),
    ("260918 Velo-CE - Il giro del telaio in Essential e in Premium - v001.docx",
     "velo-ce-il-giro-del-telaio-in-essential-e-in-premium"),
    ("AI & Data-Driven Management – Indice del corso.pdf", "ai-data-driven-management-indice-del-corso"),
    ("Manini · Percorso AI per i Sistemi Informativi (16 ore).docx",
     "manini-percorso-ai-per-i-sistemi-informativi-16-ore"),
    ("00_istruzioni_progetto.md", "00-istruzioni-progetto"),
    ("BlueAge_Sintesi_sent.pptx", "blueage-sintesi"),
    ("PULSE_I_EN.pptx", "pulse-i-en"),
    ("PULSE_DemoDeck_G.pdf", "pulse-demodeck"),
    ("Velo-CE - Open point - INTERNO - v002.xlsx", "velo-ce-open-point-interno"),
    ("Velo-CE - SAL 01 del 6 ottobre - CLIENTE - v002.pptx", "velo-ce-sal-01-cliente"),
    ("Velo-CE - Criticità di configurazione per macroarea - v004.xlsx",
     "velo-ce-criticita-di-configurazione-per-macroarea"),
    ("Velo-CE - Domande per l'intervista con Claudia - INTERNO - v001.xlsx",
     "velo-ce-domande-per-lintervista-con-claudia-interno"),
    ("Velo-CE - App So Smart, che cosa serve - CLIENTE - v002.pdf", "velo-ce-app-so-smart-che-cosa-serve-cliente"),
    ("velo-ce-app-eos-documentazione-ufficiale-2026-09-29.md", "velo-ce-app-eos-documentazione-ufficiale"),
    ("velo-ce-verbale-260929-1744-allineamento-serale.md", "velo-ce-verbale-allineamento-serale"),
    ("velo-ce-verbale-261005-1103-app-fiscali-piano-b.md", "velo-ce-verbale-app-fiscali-piano-b"),
    ("Velo-CE - Layout etichetta articolo standard report 6625 - INTERNO - v001.docx",
     "velo-ce-layout-etichetta-articolo-standard-report-6625-interno"),
    ("Manini_G1_M1P1_Strategia_portafoglio_acquisti_BlueAge.pptx", "manini-g1-m1p1-strategia-portafoglio-acquisti"),
    ("Manini_Relazione_processi_gestione_materiali_slides_v2.pdf",
     "manini-relazione-processi-gestione-materiali-slides"),
    ("Velo-CE - Pilota BC Lungo Bosch - Modello dati 5 fogli - v008.xlsx",
     "velo-ce-pilota-bc-lungo-bosch-modello-dati-5-fogli"),
    ("Meccanotecnica Umbra Spa - programma didattico azienda.docx",
     "meccanotecnica-umbra-spa-programma-didattico-azienda"),
    ("Template - Scheda decisionale.pptx", "template-scheda-decisionale"),
    ("Velo-CE - Guida ciclo d'acquisto ordine ricevimento fattura - CLIENTE - v001.pdf",
     "velo-ce-guida-ciclo-dacquisto-ordine-ricevimento-fattura-cliente"),
    ("Velo-CE - Flusso operativo telaio a scorta, acquisto-sabbiato - INTERNO - v001.xlsx",
     "velo-ce-flusso-operativo-telaio-a-scorta-acquisto-sabbiato-interno"),
]


@pytest.mark.parametrize("nome, attesa", COPPIE_REALI)
def test_coppie_reali_del_vault(nome, attesa):
    assert famiglia(nome) == attesa


@pytest.mark.parametrize("nome, attesa", [
    # date
    ("Offerta_2026-10-01.pdf", "offerta"),
    ("Offerta 20261001.pdf", "offerta"),
    ("Offerta 01.10.2026.pdf", "offerta"),
    ("Offerta_ott26.pdf", "offerta"),
    ("Budget_2026.xlsx", "budget"),
    ("Verbale 2026-10-08 1430.docx", "verbale"),
    # versioni, stati e copie
    ("Deck_v24.pptx", "deck"),
    ("Deck v2.pptx", "deck"),
    ("Deck - v001.pptx", "deck"),
    ("Deck_v1.2.pptx", "deck"),
    ("Deck_rev3.pptx", "deck"),
    ("Deck_final.pptx", "deck"),
    ("Deck_def.pptx", "deck"),
    ("Deck (1).pptx", "deck"),
    ("Deck(2).pptx", "deck"),
    ("Deck - Copia.pptx", "deck"),
    ("Deck_v3_final (1).pptx", "deck"),
    ("Articoli version 1.xlsx", "articoli"),
    # niente da togliere o il nome resterebbe vuoto
    ("Report 6625.docx", "report-6625"),
    ("v2.pdf", "v2"),
    ("Piano_B.docx", "piano"),
    ("piano-b.md", "piano-b"),
])
def test_regole(nome, attesa):
    assert famiglia(nome) == attesa


def test_url_e_percorso_danno_il_nome_del_file():
    url = "https://blueagesrl.sharepoint.com/sites/internal/SalesMarketing/Deck/BlueAge_CompanyProfile_v24.pdf"
    assert famiglia(url) == "blueage-companyprofile"
    assert famiglia("BlueAge%20Company%20Profile%20v2.pdf") == "blueage-company-profile"


@pytest.mark.parametrize("testo, attesa", [
    ("SalesMarketing", "salesmarketing"),
    ("Offerte 2026", "offerte-2026"),
    ("01_Materiale clienti", "01-materiale-clienti"),
    ("Città  --  Perù_", "citta-peru"),
    ("Info trasferta 14–15 ottobre | MTU", "info-trasferta-14-15-ottobre-mtu"),
    ("L'offerta d'autunno", "lofferta-dautunno"),
])
def test_slug(testo, attesa):
    assert slug(testo) == attesa


@pytest.mark.parametrize("oggetto, attesa", [
    ("RE: Automazione Entrata Merci - Caso Manini", "automazione-entrata-merci-caso-manini"),
    ("R: RE: FW: Bozza CP BlueAge", "bozza-cp-blueage"),
    ("Fwd: I: re: Proposta", "proposta"),
    ("Riunione di avvio", "riunione-di-avvio"),
])
def test_slug_oggetto(oggetto, attesa):
    assert slug_oggetto(oggetto) == attesa


def test_riga_di_comando(vault):
    res = esegui("famiglia.py", vault, "BlueAge_CompanyProfile_v24.pdf")
    assert res.returncode == 0 and res.stdout.strip() == "blueage-companyprofile"
    res = esegui("famiglia.py", vault, "BlueAge_CompanyProfile_v24.pdf", "--json")
    assert json.loads(res.stdout)["famiglia"] == "blueage-companyprofile"
    res = esegui("famiglia.py", vault, "--oggetto", "RE: FW: Prova")
    assert res.stdout.strip() == "prova"
    res = esegui("famiglia.py", vault, "--slug", "Offerte 2026")
    assert res.stdout.strip() == "offerte-2026"
    assert esegui("famiglia.py", vault, "--sconosciuta", "x").returncode == 2


def test_cerca_trova_la_famiglia_per_family_e_per_nome_di_versione(vault):
    # doc-alfa: family "delivery/doc-alfa", current.name Doc_Alfa_v2.pdf → famiglia doc-alfa
    res = esegui("famiglia.py", vault, "--cerca", "Doc_Alfa_v3.pdf", "--cartella",
                 "sources/sharepoint/delivery", "--json")
    assert res.returncode == 0, res.stderr
    out = json.loads(res.stdout)
    assert out["famiglia"] == "doc-alfa"
    assert [n["nota"] for n in out["note"]] == ["sources/sharepoint/delivery/doc-alfa.md"]
    assert out["note"][0]["stessa_cartella"] is True
    # una famiglia che nel vault non c'è
    assert esegui("famiglia.py", vault, "--cerca", "Altro_documento.pdf").returncode == 1


def test_cerca_vede_una_copia_in_altra_cartella(vault):
    scrivi(vault, "sources/onedrive/copie/doc-alfa-copia.md",
           (vault / "sources/sharepoint/delivery/doc-alfa.md").read_text(encoding="utf-8")
           .replace('family: "delivery/doc-alfa"', "family: doc-alfa-copia"))
    out = json.loads(esegui("famiglia.py", vault, "--cerca", "Doc_Alfa_v3.pdf", "--cartella",
                            "sources/sharepoint/delivery", "--json").stdout)
    assert [n["nota"] for n in out["note"]] == ["sources/sharepoint/delivery/doc-alfa.md",
                                                "sources/onedrive/copie/doc-alfa-copia.md"]
    assert [n["stessa_cartella"] for n in out["note"]] == [True, False]


def test_verifica_sul_mini_vault(vault):
    res = esegui("famiglia.py", vault, "--verifica", "--json")
    out = json.loads(res.stdout)
    # family "delivery/doc-alfa" non è nella forma attuale: un disaccordo su una nota
    assert out["note"] == 1 and out["uguali"] == 0
    assert out["disaccordi"][0]["calcolata"] == "doc-alfa"
    assert res.returncode == 1
