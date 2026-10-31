"""Test di nuova-nota.py e aggiorna-nota.py (SPEC 4.2-4.3, ingestor §3.4-3.6).

Le note "reali" qui sotto sono copie del frontmatter di note del vault al 26/10/2026, con il
corpo accorciato: riscritte senza modifiche devono restare identiche byte per byte.
"""

import json
import sys

import yaml

from conftest import SCRIPTS, esegui, scrivi

sys.path.insert(0, str(SCRIPTS))
import nota  # noqa: E402

COMPANY_PROFILE = """---
type: source-doc
source: sharepoint
family: blueage-companyprofile
current:
  item_id: 01GEQYSS5CERFZRWVHNRGIGQNT5GBJMIF5
  uri: file:///b!A7b6m_TYN0WCnuUFi2d1SUF8cl0xQY1JqFaa3mGO8LaO54eDFnSESI_kxYrC6RpW/01GEQYSS5CERFZRWVHNRGIGQNT5GBJMIF5
  web_url: https://example.sharepoint.com/sites/partner/Partner/Condivisi/BlueAge_CompanyProfile.pdf
  name: BlueAge_CompanyProfile.pdf
  last_modified: 2026-10-19T16:12:01Z
versions:
  - { name: BlueAge_CompanyProfile.pdf, item_id: 01GEQYSS5CERFZRWVHNRGIGQNT5GBJMIF5, last_modified: 2026-10-19T16:12:01Z }
  - { name: BlueAge_CompanyProfile_v24.pdf, item_id: 01EFCYUZYLVH33U2NLBVGZ45BE6NPUJZD5, last_modified: 2026-10-01T17:20:46Z }
  - { name: BlueAge_CompanyProfile_v21.pdf, item_id: "", last_modified: 2026-09-07T12:11:59Z }
also_at:
  - { web_url: "https://example.sharepoint.com/sites/partner/Partner/Silvia Fumagalli/BlueAge_CompanyProfile.pdf", item_id: 01GEQYSSZ72VIUFCZWXJFIPDPVV5PYCYCF }
status: active
partial: false
ingested_at: 2026-10-22T15:05:00Z
projects: []
clients: []
topics: ["[[tema-uno]]"]
tags: [company-profile, posizionamento, sales]
---

# BlueAge · Company Profile

## Riassunto

Deck di presentazione aziendale.

## Versioni

- BlueAge_CompanyProfile.pdf · 2026-10-19 · nuovo claim di apertura
"""

ALLEGATO = """---
type: source-doc
source: attachment
family: ai-data-driven-management-indice-del-corso
current:
  item_id: "AAMkAGMyY2M5ZTczLTYwNDEtNGZiOC1iYjJjLTFhZjJhOGY1YjFiMQBGAAAAAADRF2aJ18MKT6wbnyNtwv9jBwCN="
  uri: "mail:///messages/AAMkAGMy%3D/attachments/AAMkAGMyY2M5%3D"
  web_url: ""
  name: "AI & Data-Driven Management – Indice del corso.pdf"
  last_modified: 2026-10-05T14:29:40Z
versions:
  - { name: "AI & Data-Driven Management – Indice del corso.pdf", item_id: "AAMkAGMyY2M5ZTczLTYwNDEtNGZiOC1iYjJjLTFhZjJhOGY1YjFiMQBGAAAAAADRF2aJ18MKT6wbnyNtwv9jBwCN=", last_modified: 2026-10-05T14:29:40Z }
also_at: []
status: active
partial: false
ingested_at: 2026-10-22T15:23:22Z
projects: ["[[alfa]]"]
clients: ["[[cliente-uno]]"]
topics: []
tags: [formazione, programma, filo-rosso, compass]
---

# AI & Data-Driven Management · indice del corso

## Riassunto

Indice ragionato del corso.
"""

MAIL = """---
type: source-mail
conversation_id: "AAQkAGMyY2M5ZTczLTYwNDEtNGZiOC1iYjJjLTFhZjJhOGY1YjFiMQAQAEKlbkYHRUjangyjenWqM2w="
subject: "deepagent"
participants: ["[[mario-rossi]]"]
first_message: 2026-10-01T10:49:43Z
last_message: 2026-10-01T10:49:43Z
messages: 1
attachments: []
projects: []
clients: ["[[cliente-uno]]"]
topics: ["[[tema-uno]]"]
status: active
---

# deepagent

## Riassunto

Inoltro della presentazione di un possibile partner.

## Messaggi

### 2026-10-01 12:49 · [[mario-rossi]]

Inoltro con commento.
"""

CP = "sources/sharepoint/salesmarketing/deck/blueage-companyprofile.md"
AL = "sources/attachments/ai-data-driven-management-indice-del-corso.md"
ML = "sources/mail/2026-10/deepagent.md"


def nuova(root, *args):
    return esegui("nuova-nota.py", root, *args)


def aggiorna(root, *args):
    return esegui("aggiorna-nota.py", root, *args)


def fm(root, rel):
    testo = (root / rel).read_text(encoding="utf-8")
    return yaml.safe_load(testo[4:testo.find("\n---", 4)])


# --- nuova-nota.py ----------------------------------------------------------------------

CAMPI_DOC = ["--campo", "current.item_id=01ABC", "--campo", "current.uri=file:///b!drive/01ABC",
             "--campo", "current.web_url=https://example.sharepoint.com/sites/internal/Delivery/Doc_Gamma_v3.pdf",
             "--campo", "current.name=Doc_Gamma_v3.pdf", "--campo", "current.last_modified=2026-10-20T10:00:00Z",
             "--campo", "projects=[[alfa]]", "--campo", "tags=[prova, pilota]"]


def test_nuova_source_doc_completa_i_campi(vault):
    rel = "sources/sharepoint/delivery/doc-gamma.md"
    res = nuova(vault, "source-doc", rel, "--titolo", "Documento Gamma", *CAMPI_DOC, "--json")
    assert res.returncode == 0, res.stderr
    assert json.loads(res.stdout)["nota"] == rel
    d = fm(vault, rel)
    assert d["source"] == "sharepoint" and d["family"] == "doc-gamma"
    assert d["projects"] == ["[[alfa]]"] and d["tags"] == ["prova", "pilota"]
    assert d["versions"] == [{"name": "Doc_Gamma_v3.pdf", "item_id": "01ABC",
                              "last_modified": d["current"]["last_modified"]}]
    assert d["ingested_at"] is not None
    testo = (vault / rel).read_text(encoding="utf-8")
    assert '  - { name: Doc_Gamma_v3.pdf, item_id: 01ABC, last_modified: 2026-10-20T10:00:00Z }' in testo
    assert 'projects: ["[[alfa]]"]' in testo
    assert "# Documento Gamma\n\n## Riassunto" in testo and "## Versioni" in testo
    assert "{{" not in testo
    assert esegui("controlla-vault.py", vault).returncode == 0


def test_nuova_non_sovrascrive(vault):
    rel = "sources/sharepoint/delivery/doc-alfa.md"
    prima = (vault / rel).read_text(encoding="utf-8")
    res = nuova(vault, "source-doc", rel, "--titolo", "X", *CAMPI_DOC)
    assert res.returncode == 1 and "esiste già" in res.stderr
    assert (vault / rel).read_text(encoding="utf-8") == prima


def test_nuova_rifiuta_frontmatter_non_valido(vault):
    casi = [
        ("person", "people/anna-verdi.md", ["--campo", "stato=attivo"]),         # chiave sconosciuta
        ("client", "clients/nuovo-cliente.md", ["--campo", "status=amico"]),     # enum
        ("source-doc", "sources/sharepoint/x/doc-x.md", ["--campo", "current.name=x.pdf"]),  # senza collegamenti
        ("source-doc", "sources/sharepoint/x/doc-y.md", CAMPI_DOC + ["--campo", "current.last_modified=ieri"]),
        ("person", "clients/anna-verdi.md", []),                                 # cartella sbagliata
        ("person", "people/Anna Verdi.md", []),                                  # nome non in slug
        ("person", "people/mario-rossi-bis.md", ["--campo", "projects=[alfa]"]),  # non è un wikilink
        ("topic", "topics/tema-uno.md", []),                                     # esiste già
        ("inbox", "inbox/mario-rossi.md", []),                                   # slug già usato
    ]
    for tipo, rel, campi in casi:
        res = nuova(vault, tipo, rel, "--titolo", "Prova", *campi)
        assert res.returncode != 0, (rel, res.stdout)
    assert not (vault / "people/anna-verdi.md").exists()
    assert not (vault / "sources/sharepoint/x").exists()


def test_nuova_persona_e_inbox(vault):
    res = nuova(vault, "person", "people/anna-verdi.md", "--titolo", "Anna Verdi",
                "--campo", "email=anna.verdi@example.com", "--campo", "org=[[cliente-uno]]")
    assert res.returncode == 0, res.stderr
    testo = (vault / "people/anna-verdi.md").read_text(encoding="utf-8")
    assert 'org: "[[cliente-uno]]"' in testo and 'email: "anna.verdi@example.com"' in testo
    assert 'role: ""' in testo and "# Anna Verdi" in testo and "## Interazioni recenti" in testo
    res = nuova(vault, "inbox", "inbox/2026-10-26-prova.md", "--titolo", "Prova")
    assert res.returncode == 0, res.stderr
    assert fm(vault, "inbox/2026-10-26-prova.md")["type"] == "inbox"
    assert "# Prova" in (vault / "inbox/2026-10-26-prova.md").read_text(encoding="utf-8")


def test_nuova_wikilink_inesistente_e_un_avviso(vault):
    res = nuova(vault, "source-mail", "sources/mail/2026-10/prova.md", "--titolo", "Prova",
                "--campo", "subject=Prova", "--campo", "participants=[[[mario-rossi]], [[persona-nuova]]]",
                "--campo", "clients=[[cliente-uno]]", "--campo", "first_message=2026-10-20T10:00:00Z")
    assert res.returncode == 0, res.stderr
    assert "persona-nuova" in res.stderr
    assert fm(vault, "sources/mail/2026-10/prova.md")["participants"] == ["[[mario-rossi]]", "[[persona-nuova]]"]


# --- aggiorna-nota.py -------------------------------------------------------------------

def test_riscrittura_identica_di_note_reali(vault):
    for rel, testo in ((CP, COMPANY_PROFILE), (AL, ALLEGATO), (ML, MAIL)):
        scrivi(vault, rel, testo)
        res = aggiorna(vault, rel, "--campo", "status=active")
        assert res.returncode == 0, res.stderr
        assert "nessuna modifica" in res.stdout
        assert (vault / rel).read_text(encoding="utf-8") == testo
    # e il dumper, da solo, rifà identico il frontmatter della nota SharePoint
    fm_cp, _ = nota.dividi(COMPANY_PROFILE)
    dati = yaml.safe_load(fm_cp)
    assert nota.rendi_frontmatter(dati, list(dati)) == fm_cp


def test_campo_cambia_solo_la_riga_del_campo(vault):
    scrivi(vault, CP, COMPANY_PROFILE)
    res = aggiorna(vault, CP, "--campo", "partial=true", "--aggiungi", "tags=sales",
                   "--aggiungi", "tags=[deck, sales]", "--aggiungi", "projects=[[alfa]]")
    assert res.returncode == 0, res.stderr
    atteso = (COMPANY_PROFILE.replace("partial: false", "partial: true")
              .replace("tags: [company-profile, posizionamento, sales]",
                       "tags: [company-profile, posizionamento, sales, deck]")
              .replace("projects: []", 'projects: ["[[alfa]]"]'))
    assert (vault / CP).read_text(encoding="utf-8") == atteso


def test_nuova_versione(vault):
    scrivi(vault, CP, COMPANY_PROFILE)
    res = aggiorna(vault, CP, "--nuova-versione",
                   "--campo", "current.name=BlueAge_CompanyProfile_v25.pdf",
                   "--campo", "current.item_id=01NUOVO",
                   "--campo", "current.last_modified=2026-10-26T09:00:00Z",
                   "--campo", "current.uri=file:///b!drive/01NUOVO",
                   "--campo", "current.web_url=https://example.sharepoint.com/sites/internal/SalesMarketing/Deck/BlueAge_CompanyProfile_v25.pdf")
    assert res.returncode == 0, res.stderr
    d = fm(vault, CP)
    assert d["current"]["item_id"] == "01NUOVO"
    nomi = [v["name"] for v in d["versions"]]
    # la nuova in testa, la vecchia corrente non duplicata (c'era già come prima voce)
    assert nomi == ["BlueAge_CompanyProfile_v25.pdf", "BlueAge_CompanyProfile.pdf",
                    "BlueAge_CompanyProfile_v24.pdf", "BlueAge_CompanyProfile_v21.pdf"]
    testo = (vault / CP).read_text(encoding="utf-8")
    assert ("versions:\n  - { name: BlueAge_CompanyProfile_v25.pdf, item_id: 01NUOVO, "
            "last_modified: 2026-10-26T09:00:00Z }\n  - { name: BlueAge_CompanyProfile.pdf,") in testo
    assert d["ingested_at"] != yaml.safe_load("2026-10-22T15:05:00Z")
    assert testo.endswith(COMPANY_PROFILE.split("\n---\n", 1)[1])  # corpo intatto


def test_nuova_versione_porta_la_corrente_in_versions_se_manca(vault):
    rel = "sources/sharepoint/delivery/doc-alfa.md"  # versions: [] nel mini-vault
    res = aggiorna(vault, rel, "--nuova-versione", "--campo", "current.name=Doc_Alfa_v3.pdf",
                   "--campo", "current.item_id=item-3", "--campo", "current.last_modified=2026-10-10T10:00:00Z")
    assert res.returncode == 0, res.stderr
    assert "current.uri" in res.stderr  # avviso: uri della versione vecchia
    d = fm(vault, rel)
    assert [v["name"] for v in d["versions"]] == ["Doc_Alfa_v3.pdf", "Doc_Alfa_v2.pdf"]


def test_nuova_versione_github_porta_il_commit_nel_nome(vault):
    rel = "sources/github/repo/docs/repo-a.md"
    res = nuova(vault, "source-doc", rel, "--titolo", "Repo A",
                "--campo", "current.item_id=owner/repo:docs/a.md",
                "--campo", "current.uri=github://owner/repo/docs/a.md@61b833c0000000000000000000000000000000aa",
                "--campo", "current.web_url=https://github.com/owner/repo/blob/main/docs/a.md",
                "--campo", "current.name=docs/a.md", "--campo", "current.last_modified=2026-10-22T16:51:29Z",
                "--campo", "topics=[[tema-uno]]")
    assert res.returncode == 0, res.stderr
    assert fm(vault, rel)["versions"][0]["name"] == "docs/a.md@61b833c"
    res = aggiorna(vault, rel, "--nuova-versione", "--campo", "current.name=docs/a.md",
                   "--campo", "current.item_id=owner/repo:docs/a.md",
                   "--campo", "current.uri=github://owner/repo/docs/a.md@fe70fa4000000000000000000000000000000000",
                   "--campo", "current.last_modified=2026-10-25T23:55:16Z")
    assert res.returncode == 0, res.stderr
    assert [v["name"] for v in fm(vault, rel)["versions"]] == ["docs/a.md@fe70fa4", "docs/a.md@61b833c"]


def test_also_at_e_posta(vault):
    scrivi(vault, CP, COMPANY_PROFILE)
    url = "https://example.sharepoint.com/sites/internal/Delivery/Copie/BlueAge_CompanyProfile.pdf"
    assert aggiorna(vault, CP, "--also-at", f"web_url={url}", "item_id=01COPIA").returncode == 0
    assert aggiorna(vault, CP, "--also-at", f"web_url={url}", "item_id=01COPIA").returncode == 0  # già c'è
    d = fm(vault, CP)
    assert [x["item_id"] for x in d["also_at"]] == ["01GEQYSSZ72VIUFCZWXJFIPDPVV5PYCYCF", "01COPIA"]
    scrivi(vault, ML, MAIL)
    res = aggiorna(vault, ML, "--campo", "last_message=2026-10-02T08:00:00Z", "--campo", "messages=2",
                   "--aggiungi", "participants=[[mario-rossi]]", "--aggiungi", 'projects="[[alfa]]"')
    assert res.returncode == 0, res.stderr
    testo = (vault / ML).read_text(encoding="utf-8")
    assert "last_message: 2026-10-02T08:00:00Z\nmessages: 2\n" in testo
    assert 'participants: ["[[mario-rossi]]"]' in testo and 'projects: ["[[alfa]]"]' in testo
    assert 'subject: "deepagent"' in testo


def test_versione_aggiunge_un_id_superato_in_ordine(vault):
    scrivi(vault, CP, COMPANY_PROFILE)
    res = aggiorna(vault, CP, "--versione", "name=BlueAge_CompanyProfile.pdf", "item_id=01RICARICATO",
                   "last_modified=2026-10-10T08:00:00Z", "--json")
    assert res.returncode == 0, res.stderr
    assert json.loads(res.stdout)["cambiati"] == ["versions"]
    nuova_riga = ("  - { name: BlueAge_CompanyProfile.pdf, item_id: 01RICARICATO, "
                  "last_modified: 2026-10-10T08:00:00Z }\n")
    prima_v24 = "  - { name: BlueAge_CompanyProfile_v24.pdf,"
    # la corrente resta prima, la nuova voce va tra la v24 (01/10) e la corrente, il resto è intatto
    atteso = COMPANY_PROFILE.replace(prima_v24, nuova_riga + prima_v24)
    assert (vault / CP).read_text(encoding="utf-8") == atteso
    # una voce più recente della seconda va subito dopo la corrente, una più vecchia in fondo
    assert aggiorna(vault, CP, "--versione", "name=BlueAge_CompanyProfile.pdf", "item_id=01COPIA2810",
                    "last_modified=2026-10-28T08:06:21Z").returncode == 0
    assert aggiorna(vault, CP, "--versione", "name=BlueAge_CompanyProfile_v20.pdf", "item_id=01V20",
                    "last_modified=2026-08-01T09:00:00Z").returncode == 0
    d = fm(vault, CP)
    assert [v["item_id"] for v in d["versions"]] == [
        "01GEQYSS5CERFZRWVHNRGIGQNT5GBJMIF5", "01COPIA2810", "01RICARICATO",
        "01EFCYUZYLVH33U2NLBVGZ45BE6NPUJZD5", "", "01V20"]
    assert d["current"]["item_id"] == "01GEQYSS5CERFZRWVHNRGIGQNT5GBJMIF5"
    assert nota.normale(d["ingested_at"]) == "2026-10-22T15:05:00Z"


def test_versione_idempotente_con_lo_stesso_item_id(vault):
    scrivi(vault, CP, COMPANY_PROFILE)
    args = ["--versione", "name=BlueAge_CompanyProfile.pdf", "item_id=01RICARICATO",
            "last_modified=2026-10-10T08:00:00Z"]
    assert aggiorna(vault, CP, *args).returncode == 0
    dopo = (vault / CP).read_text(encoding="utf-8")
    for altro in (args, ["--versione", "name=Altro.pdf", "item_id=01RICARICATO",
                         "last_modified=2026-10-12T08:00:00Z"],
                  ["--versione", "name=BlueAge_CompanyProfile_v24.pdf",
                   "item_id=01EFCYUZYLVH33U2NLBVGZ45BE6NPUJZD5", "last_modified=2026-10-01T17:20:46Z"]):
        res = aggiorna(vault, CP, *altro)
        assert res.returncode == 0, res.stderr
        assert "nessuna modifica" in res.stdout
        assert (vault / CP).read_text(encoding="utf-8") == dopo


def test_versione_con_versions_vuoto_mette_prima_la_corrente(vault):
    rel = "sources/sharepoint/delivery/doc-alfa.md"  # versions: [] nel mini-vault
    res = aggiorna(vault, rel, "--versione", "name=Doc_Alfa_v2.pdf", "item_id=item-0",
                   "last_modified=2026-09-28T10:00:00Z")
    assert res.returncode == 0, res.stderr
    d = fm(vault, rel)
    assert [v["item_id"] for v in d["versions"]] == [d["current"]["item_id"], "item-0"]
    assert nota.normale(d["versions"][0]["last_modified"]) == "2026-10-01T10:00:00Z"


def test_versione_lascia_com_erano_le_righe_delle_voci_invariate(vault):
    rel = "sources/sharepoint/delivery/doc-alfa.md"
    testo = (vault / rel).read_text(encoding="utf-8")
    vecchie = ("versions:\n"
               "  - { name: Doc Alfa v2.pdf, item_id: item-1, last_modified: 2026-10-01T10:00:00Z }\n"
               "  - { name: Doc Alfa v1.docx, item_id: item-0, last_modified: 2026-09-01T10:00:00Z }\n")
    scrivi(vault, rel, testo.replace("versions: []\n", vecchie))
    res = aggiorna(vault, rel, "--versione", "name=Doc Alfa v2.pdf", "item_id=item-copia",
                   "last_modified=2026-10-28T08:06:21Z")
    assert res.returncode == 0, res.stderr
    # le righe senza virgolette restano tali e la voce nuova segue lo stesso stile
    nuova_riga = "  - { name: Doc Alfa v2.pdf, item_id: item-copia, last_modified: 2026-10-28T08:06:21Z }\n"
    attesa = vecchie.replace("  - { name: Doc Alfa v1.docx", nuova_riga + "  - { name: Doc Alfa v1.docx")
    assert (vault / rel).read_text(encoding="utf-8") == testo.replace("versions: []\n", attesa)
    # con i nomi tra virgolette, la voce nuova va tra virgolette
    scrivi(vault, rel, testo.replace("versions: []\n", vecchie.replace("Doc Alfa v2.pdf", '"Doc Alfa v2.pdf"')
                                     .replace("Doc Alfa v1.docx", '"Doc Alfa v1.docx"')))
    assert aggiorna(vault, rel, "--versione", "name=Doc Alfa v2.pdf", "item_id=item-copia",
                    "last_modified=2026-10-28T08:06:21Z").returncode == 0
    assert ('  - { name: "Doc Alfa v2.pdf", item_id: item-copia, last_modified: 2026-10-28T08:06:21Z }\n'
            '  - { name: "Doc Alfa v1.docx",') in (vault / rel).read_text(encoding="utf-8")


def test_versione_rifiuta_argomenti_mancanti_o_non_validi(vault):
    scrivi(vault, CP, COMPANY_PROFILE)
    scrivi(vault, ML, MAIL)
    casi = [
        (CP, ["--versione"]),
        (CP, ["--versione", "name=x.pdf", "item_id=01X"]),
        (CP, ["--versione", "item_id=01X", "last_modified=2026-10-10T08:00:00Z"]),
        (CP, ["--versione", "name=x.pdf", "item_id=", "last_modified=2026-10-10T08:00:00Z"]),
        (CP, ["--versione", "name=x.pdf", "item_id=01X", "last_modified=2026-10-10"]),
        (CP, ["--versione", "name=x.pdf", "item_id=01GEQYSS5CERFZRWVHNRGIGQNT5GBJMIF5",
              "last_modified=2026-10-10T08:00:00Z"]),  # è la current
        (ML, ["--versione", "name=x.pdf", "item_id=01X", "last_modified=2026-10-10T08:00:00Z"]),
    ]
    for rel, args in casi:
        res = aggiorna(vault, rel, *args)
        assert res.returncode == 2, (args, res.stdout, res.stderr)
    assert (vault / CP).read_text(encoding="utf-8") == COMPANY_PROFILE
    assert (vault / ML).read_text(encoding="utf-8") == MAIL


def test_aggiorna_rifiuta_e_lascia_la_nota_com_era(vault):
    scrivi(vault, CP, COMPANY_PROFILE)
    for args in (["--campo", "status=archiviato"], ["--campo", "sconosciuto=1"],
                 ["--campo", "current.last_modified=2026-10-26 09:00"], ["--aggiungi", "status=x"],
                 ["--nuova-versione", "--campo", "current.name=x.pdf"]):
        res = aggiorna(vault, CP, *args)
        assert res.returncode == 2, (args, res.stdout)
    assert (vault / CP).read_text(encoding="utf-8") == COMPANY_PROFILE
    assert aggiorna(vault, "sources/non-esiste.md", "--campo", "status=active").returncode == 2


# --- aggiorna-nota.py --versioni-in-ordine ----------------------------------------------

RIGA_CUR = ("  - { name: BlueAge_CompanyProfile.pdf, item_id: 01GEQYSS5CERFZRWVHNRGIGQNT5GBJMIF5, "
            "last_modified: 2026-10-19T16:12:01Z }\n")
RIGA_V24 = ("  - { name: BlueAge_CompanyProfile_v24.pdf, item_id: 01EFCYUZYLVH33U2NLBVGZ45BE6NPUJZD5, "
            "last_modified: 2026-10-01T17:20:46Z }\n")
RIGA_V21 = '  - { name: BlueAge_CompanyProfile_v21.pdf, item_id: "", last_modified: 2026-09-07T12:11:59Z }\n'
RIGA_RIC = "  - { name: BlueAge_CompanyProfile.pdf, item_id: 01RICARICATO, last_modified: 2026-10-28T08:06:21Z }\n"


def con_versioni(*righe):
    """COMPANY_PROFILE con queste righe in `versions` al posto delle sue."""
    vecchie = RIGA_CUR + RIGA_V24 + RIGA_V21
    assert vecchie in COMPANY_PROFILE
    return COMPANY_PROFILE.replace(vecchie, "".join(righe))


def in_ordine(root, rel):
    return aggiorna(root, rel, "--versioni-in-ordine", "--json")


def test_versioni_in_ordine_inserisce_la_current_mancante_in_testa(vault):
    # come le note Velo-CE del 29/10: la current non è in versions, la prima voce è un ID superato
    scrivi(vault, CP, con_versioni(RIGA_V24, RIGA_RIC, RIGA_V21))
    res = in_ordine(vault, CP)
    assert res.returncode == 0, res.stderr
    out = json.loads(res.stdout)
    assert out["cambiati"] == ["versions"]
    assert out["versioni_in_ordine"] == {"creata": True, "aggiornata": False, "spostata": False,
                                         "doppioni_tolti": 0, "riordinate": True}
    # in testa la current, poi le altre per data; le righe delle voci che c'erano restano identiche,
    # current, also_at, ingested_at e corpo pure
    assert (vault / CP).read_text(encoding="utf-8") == con_versioni(RIGA_CUR, RIGA_RIC, RIGA_V24, RIGA_V21)


def test_versioni_in_ordine_sposta_in_testa_la_current_e_la_allinea(vault):
    scrivi(vault, CP, con_versioni(RIGA_V24, RIGA_CUR, RIGA_V21))
    res = in_ordine(vault, CP)
    assert res.returncode == 0, res.stderr
    esito = json.loads(res.stdout)["versioni_in_ordine"]
    assert esito["spostata"] and not esito["creata"] and not esito["aggiornata"]
    assert (vault / CP).read_text(encoding="utf-8") == COMPANY_PROFILE
    # la voce della current con name e last_modified diversi prende quelli di current
    vecchia = RIGA_CUR.replace("BlueAge_CompanyProfile.pdf", "BlueAge_CP.pdf").replace("16:12:01", "09:00:00")
    scrivi(vault, CP, con_versioni(RIGA_V24, vecchia, RIGA_V21))
    res = in_ordine(vault, CP)
    assert res.returncode == 0, res.stderr
    esito = json.loads(res.stdout)["versioni_in_ordine"]
    assert esito["spostata"] and esito["aggiornata"] and not esito["creata"]
    assert (vault / CP).read_text(encoding="utf-8") == COMPANY_PROFILE


def test_versioni_in_ordine_ordina_le_altre_per_data_e_toglie_i_doppioni(vault):
    senza_data = "  - { name: BlueAge_CompanyProfile_v1.pdf, item_id: 01V1, last_modified: null }\n"
    doppia_ric = RIGA_RIC.replace("BlueAge_CompanyProfile.pdf", "Altro_nome.pdf")
    doppia_cur = RIGA_CUR.replace("16:12:01", "08:00:00")
    scrivi(vault, CP, con_versioni(senza_data, RIGA_V21, RIGA_CUR, RIGA_V24, RIGA_RIC, doppia_ric,
                                   doppia_cur, RIGA_V21))
    res = in_ordine(vault, CP)
    assert res.returncode == 0, res.stderr
    esito = json.loads(res.stdout)["versioni_in_ordine"]
    assert esito["doppioni_tolti"] == 3 and esito["riordinate"] and esito["spostata"]
    # dei doppioni resta il primo; le voci senza data vanno in fondo
    assert (vault / CP).read_text(encoding="utf-8") == con_versioni(RIGA_CUR, RIGA_RIC, RIGA_V24, RIGA_V21,
                                                                    senza_data)


def test_versioni_in_ordine_idempotente(vault):
    scrivi(vault, CP, COMPANY_PROFILE)
    res = aggiorna(vault, CP, "--versioni-in-ordine")
    assert res.returncode == 0, res.stderr
    assert "nessuna modifica" in res.stdout
    assert (vault / CP).read_text(encoding="utf-8") == COMPANY_PROFILE
    assert json.loads(in_ordine(vault, CP).stdout)["versioni_in_ordine"] == {
        "creata": False, "aggiornata": False, "spostata": False, "doppioni_tolti": 0, "riordinate": False}
    # dopo un riordino, il secondo giro non cambia niente
    scrivi(vault, CP, con_versioni(RIGA_V21, RIGA_V24))
    assert aggiorna(vault, CP, "--versioni-in-ordine").returncode == 0
    dopo = (vault / CP).read_text(encoding="utf-8")
    assert dopo == COMPANY_PROFILE
    res = aggiorna(vault, CP, "--versioni-in-ordine")
    assert "nessuna modifica" in res.stdout and (vault / CP).read_text(encoding="utf-8") == dopo


def test_versioni_in_ordine_con_versions_vuoto_e_su_github(vault):
    rel = "sources/sharepoint/delivery/doc-alfa.md"  # versions: [] nel mini-vault
    assert in_ordine(vault, rel).returncode == 0
    d = fm(vault, rel)
    assert [v["item_id"] for v in d["versions"]] == [d["current"]["item_id"]]
    # GitHub: l'item_id è lo stesso per tutte le versioni, lo storico resta
    gh = "sources/github/repo/docs/repo-a.md"
    assert nuova(vault, "source-doc", gh, "--titolo", "Repo A",
                 "--campo", "current.item_id=owner/repo:docs/a.md",
                 "--campo", "current.uri=github://owner/repo/docs/a.md@fe70fa4000000000000000000000000000000000",
                 "--campo", "current.web_url=https://github.com/owner/repo/blob/main/docs/a.md",
                 "--campo", "current.name=docs/a.md", "--campo", "current.last_modified=2026-10-25T23:55:16Z",
                 "--campo", "topics=[[tema-uno]]").returncode == 0
    testo = (vault / gh).read_text(encoding="utf-8")
    vecchia = "  - { name: docs/a.md@61b833c, item_id: owner/repo:docs/a.md, last_modified: 2026-10-22T16:51:29Z }\n"
    scrivi(vault, gh, testo.replace("versions:\n", "versions:\n" + vecchia, 1))
    res = in_ordine(vault, gh)
    assert res.returncode == 0, res.stderr
    assert json.loads(res.stdout)["versioni_in_ordine"]["spostata"]
    assert [v["name"] for v in fm(vault, gh)["versions"]] == ["docs/a.md@fe70fa4", "docs/a.md@61b833c"]


def test_versioni_in_ordine_solo_per_source_doc(vault):
    scrivi(vault, ML, MAIL)
    res = aggiorna(vault, ML, "--versioni-in-ordine")
    assert res.returncode == 2
    assert "solo per le note source-doc" in res.stderr
    assert (vault / ML).read_text(encoding="utf-8") == MAIL
