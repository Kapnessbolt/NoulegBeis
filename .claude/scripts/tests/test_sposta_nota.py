"""Test di sposta-nota.py (SPEC 6.4, audit del 31/10 P2) sul mini-vault di conftest.py."""

import json

import yaml

from conftest import TENANT_SP, esegui, git, leggi_stato, scrivi

SITO = f"{TENANT_SP}/sites/internal"
DRIVE = "b!driveDiProva"


def sposta(root, *args):
    return esegui("sposta-nota.py", root, *args)


def frontmatter(root, rel):
    testo = (root / rel).read_text(encoding="utf-8")
    return yaml.safe_load(testo.split("---\n", 2)[1])


def fotografia(root):
    """Contenuto di tutti i file del vault, tranne .git: per confrontare prima e dopo."""
    return {str(p.relative_to(root)): p.read_bytes() for p in sorted(root.rglob("*"))
            if p.is_file() and ".git" not in p.relative_to(root).parts}


def nota_fonte(root, rel, nome, web_url, item, last_modified="2026-10-05T09:00:00Z", family=None,
               status="active", versioni=True):
    """Nota source-doc coerente con lo stato: `current.uri` file:///<DRIVE>/<item> e voce
    `<DRIVE>/<item>` nella fonte sharepoint; collegata da alfa, così si vedono i wikilink."""
    slug = rel.rsplit("/", 1)[-1][:-3]
    righe_versioni = (f"\n  - {{ name: {nome}, item_id: {item}, last_modified: {last_modified} }}"
                      if versioni else " []")
    scrivi(root, rel, f"""---
type: source-doc
source: sharepoint
family: {family or slug}
current:
  item_id: {item}
  uri: file:///{DRIVE}/{item}
  web_url: {web_url}
  name: {nome}
  last_modified: {last_modified}
versions:{righe_versioni}
also_at: []
status: {status}
partial: false
ingested_at: 2026-10-06T08:00:00Z
projects: ["[[alfa]]"]
clients: []
topics: ["[[tema-uno]]"]
tags: [offerta]
---

# {nome}

## Riassunto

Documento di prova per [[alfa]].

## Versioni

- {nome} · {last_modified[:10]}
""")
    p = root / "projects/alfa/alfa.md"
    p.write_text(p.read_text(encoding="utf-8") + f"- [[{slug}]]\n", encoding="utf-8")
    stato = leggi_stato(root, "sharepoint")
    stato["items"][f"{DRIVE}/{item}"] = {"last_modified": last_modified, "note": rel}
    (root / ".state/sharepoint.json").write_text(json.dumps(stato, indent=2), encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", f"nota {slug}")
    return rel


def offerta(root, **kw):
    return nota_fonte(root, "sources/sharepoint/delivery/offerta-pilota.md", "Offerta_Pilota_v1.docx",
                      f"{SITO}/Delivery/Offerta_Pilota_v1.docx", "ITEMOFFERTA1", **kw)


def controllo_pulito(root):
    res = esegui("controlla-vault.py", root)
    assert res.returncode == 0, res.stdout + res.stderr


def test_help(vault):
    res = sposta(vault, "--help")
    assert res.returncode == 0 and "--web-url" in res.stdout
    assert sposta(vault).returncode == 2
    assert sposta(vault, "doc-alfa").returncode == 2  # manca --web-url
    assert sposta(vault, "doc-alfa", "--web-url", f"{SITO}/Delivery/x.pdf", "--boh").returncode == 2


def test_stesso_url_niente_da_fare(vault):
    prima = fotografia(vault)
    res = sposta(vault, "sources/sharepoint/delivery/doc-alfa.md", "--web-url",
                 f"{SITO}/Delivery/Doc_Alfa_v2.pdf", "--json")
    assert res.returncode == 0, res.stderr
    esito = json.loads(res.stdout)
    assert esito["cambiato"] is False and esito["campi_cambiati"] == [] and esito["chiavi_stato"] == []
    # anche per slug e con l'URL codificato: stesso documento, nessuna riscrittura
    res = sposta(vault, "doc-alfa", "--web-url", f"{SITO}/Delivery/Doc%5FAlfa%5Fv2.pdf")
    assert res.returncode == 0 and "nessuna modifica" in res.stdout
    assert fotografia(vault) == prima


def test_stessa_cartella_nome_nuovo_stessa_famiglia(vault):
    rel = offerta(vault)
    res = sposta(vault, rel, "--web-url", f"{SITO}/Delivery/Offerta_Pilota_v2.docx", "--json")
    assert res.returncode == 0, res.stderr
    esito = json.loads(res.stdout)
    assert esito["nota_dopo"] == rel and not esito["cartella_cambiata"] and not esito["slug_cambiato"]
    assert esito["family_dopo"] == "offerta-pilota"
    assert sorted(esito["campi_cambiati"]) == ["current.name", "current.web_url", "versions"]
    fm = frontmatter(vault, rel)
    assert fm["current"]["name"] == "Offerta_Pilota_v2.docx"
    assert fm["versions"][0]["name"] == "Offerta_Pilota_v2.docx" and len(fm["versions"]) == 1
    controllo_pulito(vault)


def test_cartella_nuova(vault):
    vecchio = (vault / "sources/sharepoint/delivery/doc-alfa.md").read_text(encoding="utf-8")
    url = f"{SITO}/Delivery/Pilota Alfa/Doc_Alfa_v2.pdf"
    res = sposta(vault, "sources/sharepoint/delivery/doc-alfa.md", "--web-url", url, "--json")
    assert res.returncode == 0, res.stderr
    esito = json.loads(res.stdout)
    dopo = "sources/sharepoint/delivery/pilota-alfa/doc-alfa.md"
    assert esito["nota_dopo"] == dopo and esito["cartella_cambiata"] and not esito["slug_cambiato"]
    assert esito["chiavi_stato"] == ["item-1"] and esito["campi_cambiati"] == ["current.web_url"]
    assert not (vault / "sources/sharepoint/delivery/doc-alfa.md").exists()
    assert leggi_stato(vault, "sharepoint")["items"]["item-1"]["note"] == dopo
    nuovo = (vault / dopo).read_text(encoding="utf-8")
    # cambia solo la riga di web_url (le virgolette dell'originale restano)
    diff = [(a, b) for a, b in zip(vecchio.splitlines(), nuovo.splitlines()) if a != b]
    assert diff == [(f'  web_url: "{SITO}/Delivery/Doc_Alfa_v2.pdf"', f'  web_url: "{url}"')]
    righe = git(vault, "status", "--porcelain").stdout.splitlines()
    assert any(r.startswith("R") and r.endswith(dopo) for r in righe), righe  # git vede lo spostamento
    controllo_pulito(vault)


def test_cartella_nuova_in_un_altra_libreria(vault):
    rel = offerta(vault)
    res = sposta(vault, "offerta-pilota", "--web-url", f"{SITO}/SalesMarketing/Offerte/Offerta_Pilota_v1.docx")
    assert res.returncode == 0, res.stderr
    dopo = "sources/sharepoint/salesmarketing/offerte/offerta-pilota.md"
    assert (vault / dopo).exists() and not (vault / rel).exists()
    assert leggi_stato(vault, "sharepoint")["items"][f"{DRIVE}/ITEMOFFERTA1"]["note"] == dopo
    controllo_pulito(vault)


def test_rinomina_con_famiglia_nuova(vault):
    rel = offerta(vault)
    url = f"{SITO}/Delivery/Contratti/Contratto_Pilota_v3.docx"
    res = sposta(vault, rel, "--web-url", url, "--json")
    assert res.returncode == 0, res.stderr
    esito = json.loads(res.stdout)
    dopo = "sources/sharepoint/delivery/contratti/contratto-pilota.md"
    assert esito["nota_dopo"] == dopo and esito["cartella_cambiata"] and esito["slug_cambiato"]
    assert (esito["family_prima"], esito["family_dopo"]) == ("offerta-pilota", "contratto-pilota")
    assert esito["chiavi_stato"] == [f"{DRIVE}/ITEMOFFERTA1"]
    # una sola nota, con wikilink, family, current, versions e stato aggiornati
    assert not (vault / rel).exists()
    assert list(vault.joinpath("sources").rglob("*pilota*.md")) == [vault / dopo]
    fm = frontmatter(vault, dopo)
    assert fm["family"] == "contratto-pilota" and fm["current"]["name"] == "Contratto_Pilota_v3.docx"
    assert fm["current"]["web_url"] == url and fm["current"]["item_id"] == "ITEMOFFERTA1"
    assert [v["name"] for v in fm["versions"]] == ["Contratto_Pilota_v3.docx"]
    alfa = (vault / "projects/alfa/alfa.md").read_text(encoding="utf-8")
    assert "[[offerta-pilota]]" not in alfa and "[[contratto-pilota]]" in alfa
    assert leggi_stato(vault, "sharepoint")["items"][f"{DRIVE}/ITEMOFFERTA1"]["note"] == dopo
    controllo_pulito(vault)


def test_slug_diverso_dalla_family_resta(vault):
    # doc-alfa ha family `delivery/doc-alfa`: la family cambia, lo slug no
    res = sposta(vault, "doc-alfa", "--web-url", f"{SITO}/Delivery/Relazione_Pilota_v1.pdf", "--json")
    assert res.returncode == 0, res.stderr
    esito = json.loads(res.stdout)
    assert esito["nota_dopo"] == "sources/sharepoint/delivery/doc-alfa.md" and not esito["slug_cambiato"]
    assert (esito["family_prima"], esito["family_dopo"]) == ("delivery/doc-alfa", "relazione-pilota")
    assert frontmatter(vault, esito["nota_dopo"])["family"] == "relazione-pilota"
    controllo_pulito(vault)


def test_slug_scelto_e_slug_occupato(vault):
    rel = offerta(vault)
    prima = fotografia(vault)
    url = f"{SITO}/Delivery/Tema_Uno_v1.docx"  # famiglia `tema-uno`: è già lo slug di un tema
    res = sposta(vault, rel, "--web-url", url)
    assert res.returncode == 1 and "--slug" in res.stderr
    assert fotografia(vault) == prima
    assert sposta(vault, rel, "--web-url", url, "--slug", "Tema Uno").returncode == 2
    res = sposta(vault, rel, "--web-url", url, "--slug", "tema-uno-documento", "--json")
    assert res.returncode == 0, res.stderr
    esito = json.loads(res.stdout)
    assert esito["nota_dopo"] == "sources/sharepoint/delivery/tema-uno-documento.md"
    assert esito["family_dopo"] == "tema-uno"
    controllo_pulito(vault)


def test_item_id_nuovo_voce_nuova_e_vecchia_conservata(vault):
    rel = offerta(vault)
    res = sposta(vault, rel, "--web-url", f"{SITO}/SalesMarketing/Offerta_Pilota_v1.docx",
                 "--item-id", "ITEMOFFERTA2", "--last-modified", "2026-10-20T12:00:00Z", "--json")
    assert res.returncode == 0, res.stderr
    esito = json.loads(res.stdout)
    dopo = "sources/sharepoint/salesmarketing/offerta-pilota.md"
    assert esito["chiavi_stato"] == [f"{DRIVE}/ITEMOFFERTA1", f"{DRIVE}/ITEMOFFERTA2"]
    items = leggi_stato(vault, "sharepoint")["items"]
    assert items[f"{DRIVE}/ITEMOFFERTA1"] == {"last_modified": "2026-10-05T09:00:00Z", "note": dopo}
    assert items[f"{DRIVE}/ITEMOFFERTA2"] == {"last_modified": "2026-10-20T12:00:00Z", "note": dopo}
    fm = frontmatter(vault, dopo)
    assert fm["current"]["item_id"] == "ITEMOFFERTA2"
    assert fm["current"]["uri"] == f"file:///{DRIVE}/ITEMOFFERTA2"
    assert [v["item_id"] for v in fm["versions"]] == ["ITEMOFFERTA2"]
    controllo_pulito(vault)


def test_uri_nuovo_da_l_item_id(vault):
    rel = offerta(vault)
    res = sposta(vault, rel, "--web-url", f"{SITO}/Delivery/Offerta_Pilota_v1.docx",
                 "--uri", "file:///b!altroDrive/ITEMOFFERTA9", "--json")
    assert res.returncode == 0, res.stderr
    assert json.loads(res.stdout)["chiavi_stato"] == ["b!altroDrive/ITEMOFFERTA9"]
    assert frontmatter(vault, rel)["current"]["item_id"] == "ITEMOFFERTA9"
    voce = leggi_stato(vault, "sharepoint")["items"]["b!altroDrive/ITEMOFFERTA9"]
    assert voce == {"last_modified": "2026-10-05T09:00:00Z", "note": rel}
    assert sposta(vault, rel, "--web-url", f"{SITO}/Delivery/Offerta_Pilota_v1.docx",
                  "--uri", "https://non-un-uri").returncode == 2


def test_chiave_di_un_altra_nota(vault):
    rel = offerta(vault)
    res = sposta(vault, rel, "--web-url", f"{SITO}/Delivery/Offerta_Pilota_v1.docx", "--uri", "file:///x/y")
    assert res.returncode == 0, res.stderr
    prima = fotografia(vault)
    res = sposta(vault, "doc-alfa", "--web-url", f"{SITO}/Delivery/Doc_Alfa_v2.pdf", "--uri", "file:///x/y")
    assert res.returncode == 1 and "offerta-pilota" in res.stderr
    assert fotografia(vault) == prima


def test_fuori_perimetro_non_tocca_nulla(vault):
    prima = fotografia(vault)
    for url in (f"{SITO}/Delivery/Dati/Doc_Alfa_v2.pdf",       # cartella esclusa
                f"{SITO}/Knowledge/Doc_Alfa_v2.pdf",           # libreria fuori perimetro
                f"{SITO}/Delivery/Doc_Alfa_v2.zip"):           # tipo non processato
        res = sposta(vault, "doc-alfa", "--web-url", url)
        assert res.returncode == 1, (url, res.stderr)
        assert "fuori perimetro" in res.stderr
    res = sposta(vault, "doc-alfa", "--web-url", "https://altro.example.org/Doc_Alfa_v2.pdf")
    assert res.returncode == 2
    assert fotografia(vault) == prima


def test_nota_non_fonte_o_inesistente(vault):
    url = f"{SITO}/Delivery/Doc_Alfa_v2.pdf"
    assert sposta(vault, "tema-uno", "--web-url", url).returncode == 2
    assert sposta(vault, "non-esiste", "--web-url", url).returncode == 2
    assert sposta(vault, "doc-alfa", "--web-url", url, "--last-modified", "2026-10-20").returncode == 2


def test_idempotenza(vault):
    rel = offerta(vault)
    args = ("--web-url", f"{SITO}/SalesMarketing/Contratti 2026/Contratto_Pilota_v3.docx",
            "--item-id", "ITEMOFFERTA2", "--last-modified", "2026-10-20T12:00:00Z")
    res = sposta(vault, rel, *args)
    assert res.returncode == 0, res.stderr
    prima = fotografia(vault)
    # stessi argomenti, compreso il percorso vecchio che non esiste più
    res = sposta(vault, rel, *args, "--json")
    assert res.returncode == 0, res.stderr
    esito = json.loads(res.stdout)
    assert esito["cambiato"] is False and esito["chiavi_stato"] == [] and esito["campi_cambiati"] == []
    assert esito["nota_dopo"] == "sources/sharepoint/salesmarketing/contratti-2026/contratto-pilota.md"
    res = sposta(vault, rel, *args)
    assert res.returncode == 0 and "nessuna modifica" in res.stdout
    assert fotografia(vault) == prima
    controllo_pulito(vault)


def test_prefisso_di_disambiguazione_conservato(vault):
    rel = nota_fonte(vault, "sources/sharepoint/delivery/velo-ce-offerta-pilota.md", "Offerta_Pilota_v1.docx",
                     f"{SITO}/Delivery/Offerta_Pilota_v1.docx", "ITEMVELO1")
    res = sposta(vault, rel, "--web-url", f"{SITO}/Delivery/Contratto_Pilota.docx", "--json")
    assert res.returncode == 0, res.stderr
    esito = json.loads(res.stdout)
    assert esito["family_dopo"] == "velo-ce-contratto-pilota"
    assert esito["nota_dopo"] == "sources/sharepoint/delivery/velo-ce-contratto-pilota.md"
    assert frontmatter(vault, esito["nota_dopo"])["family"] == "velo-ce-contratto-pilota"
    assert "[[velo-ce-contratto-pilota]]" in (vault / "projects/alfa/alfa.md").read_text(encoding="utf-8")
    controllo_pulito(vault)


def test_nota_rimossa_torna_attiva(vault):
    rel = offerta(vault, status="removed")
    res = sposta(vault, rel, "--web-url", f"{SITO}/Delivery/Archivio/Offerta_Pilota_v1.docx", "--json")
    assert res.returncode == 0, res.stderr
    esito = json.loads(res.stdout)
    assert "status" in esito["campi_cambiati"]
    assert frontmatter(vault, esito["nota_dopo"])["status"] == "active"
    controllo_pulito(vault)
