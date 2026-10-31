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


def test_messaggi_dello_stato_vengono_da_anomalie(vault):
    """Le regole stanno in anomalie.py (P8, P11): il rapporto ne stampa i messaggi così come sono,
    gli stessi che `plancia.py --anomalie` usa per le righe del digest."""
    import anomalie
    giro = {"inizio": fa(hours=2), "fine": fa(hours=1), "risultati": 4,
            "piu_recente": "2026-10-26T18:00:00Z", "falliti": 1}
    modifica_stato(vault, "outlook", watermark="2026-10-19T16:22:49Z", ultimo_giro=giro)
    modifica_stato(vault, "sharepoint", riconciliazione_dovuta={"Delivery": fa(days=3)})
    res = controlla(vault)
    assert res.returncode == 0, res.stdout
    avvisi = res.stdout.split("## Avvisi")[1]
    fermo = anomalie.watermark_fermo("outlook", leggi_stato(vault, "outlook"))
    (dovuta,) = anomalie.riconciliazioni_dovute("sharepoint", leggi_stato(vault, "sharepoint"))
    (orfana,) = anomalie.voci_orfane({DOC_ALFA: {"type": "source-doc", "source": "sharepoint", "current": {}}},
                                     {"sharepoint": leggi_stato(vault, "sharepoint")["items"]})
    assert f"- `.state/outlook.json` · {fermo['messaggio']}" in avvisi
    assert f"- `.state/sharepoint.json` · {dovuta['messaggio']}" in avvisi
    assert f"- `{DOC_ALFA}` · {orfana['messaggio']}" in avvisi


# --- Stato ↔ note ↔ fonti: cartella, ID, famiglia, stesso nome (audit 2026-10-31, P6)

from conftest import leggi_stato  # noqa: E402

DOC_ALFA = "sources/sharepoint/delivery/doc-alfa.md"
ITEM_ALFA = "01EFCYUZYLVH33U2NLBVGZ45BE6NPUJZD5aGVsbG8gd29ybGQgdGhpcyBpcyBhIHNlY3JldA"
URL_SP = "https://example.sharepoint.com/sites/internal"
MESSAGGI_P6 = ("non ha seguito il file", "senza versione o copia nella nota", "`family`", "stesso nome di file")


def scrivi_voci(vault, fonte, items):
    data = leggi_stato(vault, fonte)
    data["items"] = items
    (vault / ".state" / f"{fonte}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")


def sostituisci(vault, rel, vecchio, nuovo):
    p = vault / rel
    testo = p.read_text(encoding="utf-8")
    assert vecchio in testo, vecchio
    p.write_text(testo.replace(vecchio, nuovo, 1), encoding="utf-8")


@pytest.fixture
def coerente(vault):
    """Il mini-vault con stato e nota allineati: la chiave della voce finisce con
    `current.item_id` e `family` è quella calcolata da `current.name` (conftest usa ancora la
    forma vecchia `delivery/doc-alfa` e la chiave `item-1`)."""
    sostituisci(vault, DOC_ALFA, 'family: "delivery/doc-alfa"', "family: doc-alfa")
    scrivi_voci(vault, "sharepoint", {f"drive-1/{ITEM_ALFA}": {
        "last_modified": "2026-10-01T10:00:00Z", "note": DOC_ALFA}})
    git(vault, "commit", "-q", "-am", "stato allineato")
    return vault


def test_stato_e_note_coerenti_nessun_errore_ne_avviso(coerente):
    res = controlla(coerente)
    assert res.returncode == 0, res.stdout
    assert errori(res) == 0
    assert not any(m in res.stdout for m in MESSAGGI_P6), res.stdout


def test_mini_vault_di_conftest_ha_family_e_id_non_allineati(vault):
    res = controlla(vault)
    assert res.returncode == 0, res.stdout
    avvisi = res.stdout.split("## Avvisi")[1]
    assert "`family` `delivery/doc-alfa` diversa da `doc-alfa`" in avvisi
    assert "1 voce dello stato (su 1) senza versione o copia nella nota" in avvisi


def test_nota_che_non_ha_seguito_il_file_e_errore_che_non_blocca_il_commit(coerente):
    nuovo = f"{URL_SP}/SalesMarketing/Offerte/Doc_Alfa_v2.pdf"
    sostituisci(coerente, DOC_ALFA, f"{URL_SP}/Delivery/Doc_Alfa_v2.pdf", nuovo)
    res = controlla(coerente)
    assert res.returncode == 1
    errori_txt = res.stdout.split("## Errori")[1].split("## Avvisi")[0]
    assert "la nota non ha seguito il file (cartella attesa `sources/sharepoint/salesmarketing/offerte`)" in errori_txt
    assert f'sposta-nota.py {DOC_ALFA} --web-url "{nuovo}"' in errori_txt
    assert errori(res) == 1
    # il pre-commit non ferma il giro (o la sessione) che tocca la nota
    res = controlla(coerente, "--modificati")
    assert res.returncode == 0, res.stdout


@pytest.mark.parametrize("web_url", [
    "https://altro.example.org/documenti/Doc_Alfa_v2.pdf",  # URL non del tenant
    "https://example-my.sharepoint.com/personal/utente_prova_example_com/Documents/Altro/Doc_Alfa_v2.pdf",
])
def test_url_non_riconosciuto_o_senza_cartella_non_e_errore_di_cartella(coerente, web_url):
    sostituisci(coerente, DOC_ALFA, f"{URL_SP}/Delivery/Doc_Alfa_v2.pdf", web_url)
    res = controlla(coerente)
    assert res.returncode == 0, res.stdout
    assert "non ha seguito il file" not in res.stdout


def test_nota_fuori_perimetro_si_salta(coerente):
    sostituisci(coerente, DOC_ALFA, f"{URL_SP}/Delivery/Doc_Alfa_v2.pdf", f"{URL_SP}/Knowledge/Doc_Alfa_v2.pdf")
    sostituisci(coerente, DOC_ALFA, "tags: []", "tags: [fuori-perimetro]")
    res = controlla(coerente)
    assert res.returncode == 0, res.stdout
    assert "non ha seguito il file" not in res.stdout


def test_voce_dello_stato_senza_versione_nella_nota_e_avviso(coerente):
    voci = leggi_stato(coerente, "sharepoint")["items"]
    voci["drive-1/item-vecchio"] = {"last_modified": "2026-09-01T10:00:00Z", "note": DOC_ALFA}
    voci["drive-2/item-copia"] = {"last_modified": "2026-09-02T10:00:00Z", "note": DOC_ALFA}
    scrivi_voci(coerente, "sharepoint", voci)
    res = controlla(coerente)
    assert res.returncode == 0, res.stdout
    righe = [r for r in res.stdout.splitlines() if "senza versione o copia nella nota" in r]
    assert len(righe) == 1 and "2 voci dello stato (su 3)" in righe[0], righe  # una riga per nota
    assert "`stato.py voci sharepoint <nota>`" in righe[0]
    # la versione vecchia in `versions` e la copia in `also_at`: l'avviso sparisce
    sostituisci(coerente, DOC_ALFA, "versions: []",
                'versions: [{name: "Doc_Alfa_v1.pdf", item_id: "item-vecchio", last_modified: 2026-09-01T10:00:00Z}]')
    sostituisci(coerente, DOC_ALFA, "also_at: []",
                f'also_at: [{{web_url: "{URL_SP}/SalesMarketing/Doc_Alfa_v2.pdf", item_id: "item-copia"}}]')
    res = controlla(coerente)
    assert res.returncode == 0, res.stdout
    assert "senza versione o copia nella nota" not in res.stdout


def test_family_diversa_da_famiglia_py_e_avviso_salvo_il_prefisso(coerente):
    sostituisci(coerente, DOC_ALFA, "family: doc-alfa", "family: documento-alfa")
    res = controlla(coerente)
    assert res.returncode == 0, res.stdout
    assert "`family` `documento-alfa` diversa da `doc-alfa`" in res.stdout.split("## Avvisi")[1]
    sostituisci(coerente, DOC_ALFA, "family: documento-alfa", "family: cliente-uno-doc-alfa")
    res = controlla(coerente)
    assert res.returncode == 0, res.stdout
    assert "`family`" not in res.stdout


def test_stesso_nome_in_cartelle_diverse_su_note_diverse_e_avviso(coerente):
    copia = "sources/sharepoint/salesmarketing/doc-alfa-copia.md"
    testo = (coerente / DOC_ALFA).read_text(encoding="utf-8")
    scrivi(coerente, copia, testo.replace("family: doc-alfa", "family: salesmarketing-doc-alfa")
           .replace(ITEM_ALFA, "item-copia").replace(f"{URL_SP}/Delivery/", f"{URL_SP}/SalesMarketing/"))
    voci = leggi_stato(coerente, "sharepoint")["items"]
    voci["drive-2/item-copia"] = {"last_modified": "2026-10-01T10:00:00Z", "note": copia}
    scrivi_voci(coerente, "sharepoint", voci)
    res = controlla(coerente)
    assert res.returncode == 0, res.stdout
    righe = [r for r in res.stdout.splitlines() if "stesso nome di file `doc_alfa_v2.pdf`" in r]
    assert len(righe) == 1 and copia in righe[0], res.stdout
    # una nota non registrata nello stato non conta (ha già il suo avviso)
    scrivi_voci(coerente, "sharepoint", {k: v for k, v in voci.items() if v["note"] != copia})
    assert "stesso nome di file" not in controlla(coerente).stdout
