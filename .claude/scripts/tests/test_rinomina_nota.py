"""Test di rinomina-nota.py (SPEC 4.4) sul mini-vault di conftest.py."""

from conftest import esegui, leggi_stato, scrivi

DOC_ALFA = "sources/sharepoint/delivery/doc-alfa.md"


def rinomina(root, vecchio, nuovo, *altri):
    return esegui("rinomina-nota.py", root, vecchio, nuovo, *altri)


def righe_diverse(prima, dopo):
    return [(a, b) for a, b in zip(prima.splitlines(), dopo.splitlines()) if a != b]


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
    stato = leggi_stato(vault, "sharepoint")
    assert stato["items"]["item-1"]["note"] == "sources/sharepoint/delivery/doc-alfa-pilota.md"
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


def test_help_e_errori_d_uso(vault):
    res = rinomina(vault, "--help", "x")
    assert res.returncode == 0 and "--family" in res.stdout
    assert esegui("rinomina-nota.py", vault, "solo-uno").returncode == 2
    assert rinomina(vault, "tema-uno", "tema-due", "--boh").returncode == 2
    assert rinomina(vault, "tema-uno", "tema-due", "--family").returncode == 2


def test_family_uguale_allo_slug_segue_lo_slug(vault):
    testo = (vault / DOC_ALFA).read_text(encoding="utf-8").replace('family: "delivery/doc-alfa"', 'family: "doc-alfa"')
    scrivi(vault, DOC_ALFA, testo)
    res = rinomina(vault, "doc-alfa", "doc-alfa-pilota")
    assert res.returncode == 0, res.stderr
    dopo = (vault / "sources/sharepoint/delivery/doc-alfa-pilota.md").read_text(encoding="utf-8")
    # solo la riga di family (lo stile resta: virgolette comprese)
    assert righe_diverse(testo, dopo) == [('family: "doc-alfa"', 'family: "doc-alfa-pilota"')]
    assert esegui("controlla-vault.py", vault).returncode == 0


def test_family_diversa_dallo_slug_resta(vault):
    testo = (vault / DOC_ALFA).read_text(encoding="utf-8")
    assert rinomina(vault, "doc-alfa", "doc-alfa-pilota").returncode == 0
    assert (vault / "sources/sharepoint/delivery/doc-alfa-pilota.md").read_text(encoding="utf-8") == testo


def test_family_passata(vault):
    testo = (vault / DOC_ALFA).read_text(encoding="utf-8")
    res = rinomina(vault, "doc-alfa", "relazione-pilota", "--family", "relazione-pilota")
    assert res.returncode == 0, res.stderr
    dopo = (vault / "sources/sharepoint/delivery/relazione-pilota.md").read_text(encoding="utf-8")
    assert righe_diverse(testo, dopo) == [('family: "delivery/doc-alfa"', 'family: "relazione-pilota"')]
    assert leggi_stato(vault, "sharepoint")["items"]["item-1"]["note"] == "sources/sharepoint/delivery/relazione-pilota.md"
    assert esegui("controlla-vault.py", vault).returncode == 0


def test_family_solo_per_le_note_fonte(vault):
    res = rinomina(vault, "tema-uno", "tema-due", "--family", "tema-due")
    assert res.returncode == 2
    assert (vault / "topics/tema-uno.md").exists() and not (vault / "topics/tema-due.md").exists()
