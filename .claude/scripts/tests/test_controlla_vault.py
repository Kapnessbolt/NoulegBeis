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


def test_stato_per_fonte_voce_verso_nota_inesistente_e_errore(vault):
    res = esegui("stato.py", vault, "set-item", "outlook", "conv-1", "--istante", "2026-10-20T10:00:00Z",
                 "--note", "sources/mail/2026-10/non-esiste.md")
    assert res.returncode == 0, res.stderr
    res = controlla(vault)
    assert res.returncode == 1
    assert "`.state/outlook.json` · outlook `conv-1` punta a una nota inesistente" in res.stdout


def test_stato_illeggibile_e_errore_e_documento_non_registrato_e_avviso(vault):
    (vault / ".state" / "onedrive.json").write_text("{ non json", encoding="utf-8")
    scrivi(vault, ".state/sharepoint.json", '{"watermark": null, "items": {}}')
    res = controlla(vault)
    assert res.returncode == 1
    assert "`.state/onedrive.json` · illeggibile" in res.stdout
    assert "documento non registrato nello stato (.state/sharepoint.json)" in res.stdout


def test_regola_a_percorso_valida_nessun_errore(vault):
    scrivi(vault, ".claude/rules/fonti.md", '---\npaths:\n  - "sources/**"\n---\n\n# Fonti\n\nRegola di prova.\n')
    scrivi(vault, ".claude/rules/sempre.md", "# Sempre\n\nRegola senza paths, caricata sempre.\n")
    res = controlla(vault)
    assert res.returncode == 0, res.stdout
    assert errori(res) == 0


def test_regola_con_frontmatter_rotto_e_errore(vault):
    scrivi(vault, ".claude/rules/rotta.md", "---\npaths: [sources/**\n---\n\n# Rotta\n")
    res = controlla(vault)
    assert res.returncode == 1
    assert "rotta.md" in res.stdout and "caricata in ogni sessione" in res.stdout


def test_regola_con_paths_non_lista_e_errore(vault):
    scrivi(vault, ".claude/rules/mappa.md", "---\npaths:\n  sources: true\n---\n\n# Mappa\n")
    res = controlla(vault)
    assert res.returncode == 1
    assert "`paths` deve essere una lista" in res.stdout


def test_regola_su_cartella_inesistente_e_avviso(vault):
    scrivi(vault, ".claude/rules/altrove.md", '---\npaths: ["cartella-che-non-esiste/**"]\n---\n\n# Altrove\n')
    res = controlla(vault)
    assert res.returncode == 0, res.stdout
    assert "non esiste nel vault" in res.stdout


# --- Stato dell'ingestion: riconciliazione dovuta e watermark fermo (audit 2026-10-31, P4 e P5)

import datetime as dt  # noqa: E402
import json  # noqa: E402


def fa(**kw):
    """Istante UTC di `kw` fa (giorni=, ore=), nel formato dello stato."""
    t = dt.datetime.now(dt.timezone.utc) - dt.timedelta(**kw)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def modifica_stato(vault, fonte, **chiavi):
    p = vault / ".state" / f"{fonte}.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data.update(chiavi)
    p.write_text(json.dumps(data, indent=2), encoding="utf-8")


def test_riconciliazione_dovuta_avviso_dopo_un_giorno_errore_dopo_sette(vault):
    modifica_stato(vault, "sharepoint", riconciliazione_dovuta={"SalesMarketing": fa(hours=5)})
    res = controlla(vault)
    assert res.returncode == 0 and "riconciliazione dovuta" not in res.stdout
    modifica_stato(vault, "sharepoint", riconciliazione_dovuta={"SalesMarketing": fa(days=2)})
    res = controlla(vault)
    assert res.returncode == 0, res.stdout
    assert "riconciliazione dovuta per SalesMarketing" in res.stdout.split("## Avvisi")[1]
    modifica_stato(vault, "onedrive", riconciliazione_dovuta={"Lavoro": fa(days=8)})
    res = controlla(vault)
    assert res.returncode == 1
    errori_txt = res.stdout.split("## Errori")[1].split("## Avvisi")[0]
    assert "riconciliazione dovuta per Lavoro" in errori_txt and "/ingest riconcilia onedrive" in errori_txt


def test_riconciliazione_dovuta_non_blocca_il_commit_dell_ingestion(vault):
    """L'errore resta nel rapporto e in CI, ma il pre-commit non ferma il giro che scrive lo stato:
    bloccarlo perderebbe le note del giro e allargherebbe il ritardo."""
    modifica_stato(vault, "sharepoint", riconciliazione_dovuta={"Delivery": fa(days=9)})
    res = controlla(vault, "--modificati")
    assert res.returncode == 0, res.stdout
    assert controlla(vault).returncode == 1


def test_riconciliazione_dovuta_illeggibile_e_errore(vault):
    modifica_stato(vault, "sharepoint", riconciliazione_dovuta={"Delivery": "ieri"})
    res = controlla(vault)
    assert res.returncode == 1 and "riconciliazione_dovuta" in res.stdout


def test_watermark_fermo_con_risultati_nel_giro_e_avviso(vault):
    """27/10 (A2): 21 risultati fino al 26/10, watermark fermo al 19/10."""
    giro = {"inizio": fa(hours=2), "fine": fa(hours=1), "risultati": 21,
            "piu_recente": "2026-10-26T18:00:00Z", "falliti": 0}
    modifica_stato(vault, "sharepoint", watermark="2026-10-19T16:22:49Z", ultimo_giro=giro)
    res = controlla(vault)
    assert res.returncode == 0
    avvisi = res.stdout.split("## Avvisi")[1]
    assert "watermark di sharepoint fermo al 2026-10-19T16:22:49Z" in avvisi and "21 risultati" in avvisi


def test_watermark_al_passo_o_giro_vuoto_nessun_avviso(vault):
    giro = {"inizio": fa(hours=2), "fine": fa(hours=1), "risultati": 21,
            "piu_recente": "2026-10-26T18:00:00Z", "falliti": 0}
    # weekend senza modifiche: i risultati sono quelli già visti, il watermark è il più recente
    modifica_stato(vault, "sharepoint", watermark="2026-10-26T18:00:00Z", ultimo_giro=giro)
    # giro senza risultati con watermark vecchio
    modifica_stato(vault, "outlook", watermark="2026-10-01T00:00:00Z",
                   ultimo_giro={**giro, "risultati": 0, "piu_recente": None})
    # meno di 2 giorni di distacco
    modifica_stato(vault, "onedrive", watermark="2026-10-25T00:00:00Z", ultimo_giro=giro)
    res = controlla(vault)
    assert res.returncode == 0 and "fermo al" not in res.stdout
