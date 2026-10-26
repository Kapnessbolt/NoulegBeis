"""Test di controlla-vault.py (SPEC 4.4) sul mini-vault di conftest.py."""

import re

import pytest

from conftest import aggiungi, esegui, git, scrivi

IBAN_FINTO = "IT60 X054 2811 1010 0000 0123 456"


def controlla(root, *args):
    return esegui("controlla-vault.py", root, *args)


def errori(res):
    m = re.search(r"(\d+) errori", res.stdout)
    assert m, res.stdout + res.stderr
    return int(m.group(1))


def test_vault_valido_nessun_errore(vault):
    res = controlla(vault)
    assert res.returncode == 0, res.stdout
    assert errori(res) == 0


def test_wikilink_rotto_e_errore(vault):
    aggiungi(vault, "topics/tema-uno.md", "Vedi anche [[nota-che-non-esiste]].")
    res = controlla(vault)
    assert res.returncode == 1
    assert "collegamento rotto: [[nota-che-non-esiste]]" in res.stdout


def test_campo_del_template_mancante_e_errore(vault):
    p = vault / "projects/alfa/alfa.md"
    p.write_text(p.read_text(encoding="utf-8").replace('role: "consulente AI"\n', ""), encoding="utf-8")
    res = controlla(vault)
    assert res.returncode == 1
    assert "campi mancanti: role" in res.stdout


def test_slug_duplicato_e_errore(vault):
    scrivi(vault, "inbox/mario-rossi.md", "---\ntype: inbox\ncreated: 2026-10-21\n---\n\nDoppione.\n")
    res = controlla(vault)
    assert res.returncode == 1
    assert "slug `mario-rossi` duplicato" in res.stdout


def test_iban_nel_corpo_e_errore_senza_stampare_il_valore(vault):
    aggiungi(vault, "inbox/2026-10-20-idea.md", f"Bonifico su {IBAN_FINTO} entro venerdì.")
    res = controlla(vault)
    assert res.returncode == 1
    assert "possibile dato riservato: IBAN" in res.stdout
    assert "`IT60…`" in res.stdout
    assert "X054" not in res.stdout and "0123" not in res.stdout


@pytest.mark.parametrize("testo, categoria", [
    ("Cellulare di Mario: 345 123 4567.", "telefono"),
    ("Telefono +39 02 1234 5678 in ufficio.", "telefono"),
    ("Chiave sk-ant-api03-AbCdEf1234567890XyZw nel file.", "chiave o token"),
    ("Token ghp_abcdefghijklmnopqrstuvwxyz0123456789 di GitHub.", "chiave o token"),
    ("Chiave AKIAIOSFODNN7EXAMPLE di AWS.", "chiave o token"),
    ("Sessione eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIi firmata.", "chiave o token"),
    ("Hash 3f786850e387550fdab836ed7e6dc881de23001b del file.", "stringa esadecimale lunga"),
    ("Segreto aGVsbG8gd29ybGQgdGhpcyBpcyBhIHNlY3JldCBrZXkgMTIz nel testo.", "stringa base64 lunga"),
    ("Tenant del cliente 72f988bf-86f1-41af-91ab-2d7cd011db47.", "GUID"),
    ("ID riunione: 362 245 789 123", "ID di riunione"),
    ("Meeting ID: 812 3456 7890", "ID di riunione"),
    ("Passcode: aB3xYz", "codice di accesso"),
    ("password: Segreta123!", "password in chiaro"),
    ("pwd=abc123", "password in chiaro"),
])
def test_dati_riservati_nel_corpo_sono_errore(vault, testo, categoria):
    aggiungi(vault, "topics/tema-uno.md", testo)
    res = controlla(vault)
    assert res.returncode == 1, res.stdout
    assert f"possibile dato riservato: {categoria}" in res.stdout


@pytest.mark.parametrize("testo", [
    "Il documento è protetto da password.",
    "La password la reinserisce l'amministratore.",
    "Budget di 3.000 € per il pilota.",
    "Il carico è di 1.860 ore all'anno.",
    "Risparmio di 330.000.000 € e quota del 345 123 456%.",
    "Un totale di 1.330.000.000 pezzi, 320 ore di aula.",
    "Password: omessa. Codice di accesso del web service demo, omesso.",
    "password: `[omessa]`",
    "Riunione del 2026-10-12, norma UE 2016/679, ISO 9001.",
    "Server MCP `6501b655-9b79-4832-8016-17eddb19e4b6` già in settings.json.",
    "Link https://claude.ai/artifact/KN8Wp48Ja6vGbShXeTpRgR e file BlueAge_OnePage_BusinessCentral_AI_v2.pdf",
])
def test_testo_lecito_nessun_errore(vault, testo):
    aggiungi(vault, "topics/tema-uno.md", testo)
    res = controlla(vault)
    assert res.returncode == 0, res.stdout
    assert errori(res) == 0


def test_frontmatter_non_controllato(vault):
    """`item_id` e `uri` lunghi (come quelli del vault) stanno nel frontmatter: niente errore."""
    p = vault / "sources/sharepoint/delivery/doc-alfa.md"
    testo = p.read_text(encoding="utf-8").replace(
        'family: "delivery/doc-alfa"',
        'family: "delivery/doc-alfa"\nconversation_id: "72f988bf-86f1-41af-91ab-2d7cd011db47"', 1)
    p.write_text(testo, encoding="utf-8")
    res = controlla(vault)
    assert "possibile dato riservato" not in res.stdout


def test_modificati_solo_i_file_modificati(vault):
    # Un errore già committato in una nota che non tocchiamo
    aggiungi(vault, "topics/tema-uno.md", "Vedi [[nota-che-non-esiste]].")
    git(vault, "commit", "-q", "-am", "errore già nel repo")
    # Modifica lecita a un'altra nota: l'errore vecchio non blocca
    aggiungi(vault, "clients/cliente-uno.md", "Nota aggiunta senza problemi.")
    res = controlla(vault, "--modificati")
    assert res.returncode == 0, res.stdout
    assert controlla(vault).returncode == 1  # il rapporto completo lo vede ancora
    # Un dato riservato nella nota modificata invece blocca, e si vede solo quello
    aggiungi(vault, "clients/cliente-uno.md", f"IBAN {IBAN_FINTO}.")
    res = controlla(vault, "--modificati")
    assert res.returncode == 1
    assert "clients/cliente-uno.md" in res.stdout and "IBAN" in res.stdout
    assert "tema-uno" not in res.stdout


def test_modificati_vede_i_link_rotti_da_una_nota_cancellata(vault):
    (vault / "people/mario-rossi.md").unlink()
    res = controlla(vault, "--modificati")
    assert res.returncode == 1
    assert "collegamento rotto: [[mario-rossi]]" in res.stdout
