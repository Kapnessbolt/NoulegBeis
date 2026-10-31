"""Test di stato.py (SPEC 6.1, 11): migrazione, lettura, scrittura, merge driver."""

import json
import subprocess

from conftest import SCRIPTS, STATO, esegui, git, leggi_stato


def stato(root, *args):
    return esegui("stato.py", root, *args)


VECCHIO = ".state/stato-unico.json"  # il vecchio file unico, con una chiave per fonte


def test_migra_divide_e_cancella_il_file_unico(vault):
    for fonte in STATO:
        (vault / ".state" / f"{fonte}.json").unlink()
    vecchio = vault / VECCHIO
    vecchio.write_text(json.dumps(STATO, indent=2), encoding="utf-8")
    res = stato(vault, "migra", VECCHIO)
    assert res.returncode == 0, res.stderr
    assert not vecchio.exists()
    for fonte, contenuto in STATO.items():
        assert leggi_stato(vault, fonte) == contenuto
    # JSON ordinato con indentazione 2
    testo = (vault / ".state" / "sharepoint.json").read_text(encoding="utf-8")
    assert testo == json.dumps(STATO["sharepoint"], indent=2, sort_keys=True) + "\n"
    # una seconda volta non si fa
    assert stato(vault, "migra", VECCHIO).returncode != 0


def test_migra_non_sovrascrive_i_file_per_fonte(vault):
    (vault / VECCHIO).write_text(json.dumps(STATO), encoding="utf-8")
    res = stato(vault, "migra", VECCHIO)
    assert res.returncode != 0 and "esistono già" in res.stderr
    assert (vault / VECCHIO).exists()


def test_lettura(vault):
    res = stato(vault, "watermark", "sharepoint")
    assert res.returncode == 0 and res.stdout.strip() == "2026-10-02T06:50:00Z"
    res = stato(vault, "watermark", "onedrive")
    assert res.returncode == 1 and res.stdout.strip() == "null" and "primo caricamento" in res.stderr
    res = stato(vault, "item", "sharepoint", "item-1")
    assert res.returncode == 0
    assert json.loads(res.stdout)["note"] == "sources/sharepoint/delivery/doc-alfa.md"
    assert stato(vault, "item", "sharepoint", "manca").returncode == 1
    assert stato(vault, "repo", "owner/repo").returncode == 1
    assert json.loads(stato(vault, "elenco", "sharepoint").stdout) == STATO["sharepoint"]["items"]
    assert stato(vault, "watermark", "sconosciuta").returncode == 2


def test_set_item_documenti_posta_e_github(vault):
    res = stato(vault, "set-item", "sharepoint", "drive/item-2", "--last-modified", "2026-10-03T08:00:00Z",
                "--note", "sources/sharepoint/delivery/doc-beta.md")
    assert res.returncode == 0, res.stderr
    assert "non esiste ancora" in res.stderr  # avviso: la nota si scrive dopo
    assert leggi_stato(vault, "sharepoint")["items"]["drive/item-2"] == {
        "last_modified": "2026-10-03T08:00:00Z", "note": "sources/sharepoint/delivery/doc-beta.md"}
    # outlook: la chiave è il conversationId e il campo last_message, con --istante
    res = stato(vault, "set-item", "outlook", "AAQk=", "--istante", "2026-10-21T19:35:37Z",
                "--note", "sources/mail/2026-10/prova.md")
    assert res.returncode == 0, res.stderr
    assert leggi_stato(vault, "outlook")["threads"]["AAQk="]["last_message"] == "2026-10-21T19:35:37Z"
    # github con commit; poi solo commit e istante sulla voce esistente (la nota resta)
    chiave = "owner/repo:docs/a.md"
    assert stato(vault, "set-item", "github", chiave, "--istante", "2026-10-22T10:00:00Z",
                 "--note", "sources/github/repo/docs/repo-a.md", "--commit", "abc1234").returncode == 0
    assert stato(vault, "set-item", "github", chiave, "--istante", "2026-10-23T10:00:00Z",
                 "--commit", "def5678").returncode == 0
    voce = leggi_stato(vault, "github")["items"][chiave]
    assert voce == {"last_modified": "2026-10-23T10:00:00Z", "commit": "def5678",
                    "note": "sources/github/repo/docs/repo-a.md"}


def test_set_item_validazione(vault):
    base = ["set-item", "sharepoint", "x"]
    note = ["--note", "sources/sharepoint/x.md"]
    assert stato(vault, *base, "--istante", "2026-10-03T08:00:00.123Z", *note).returncode == 2
    assert stato(vault, *base, "--istante", "2026-10-03 08:00:00", *note).returncode == 2
    assert stato(vault, *base, "--istante", "2026-13-03T08:00:00Z", *note).returncode == 2
    assert stato(vault, *base, "--istante", "2026-10-03T08:00:00Z", "--note", "/tmp/x.md").returncode == 2
    assert stato(vault, *base, "--istante", "2026-10-03T08:00:00Z", "--note", "people/x.md").returncode == 2
    assert stato(vault, *base, "--istante", "2026-10-03T08:00:00Z", "--note", "sources/../x.md").returncode == 2
    assert stato(vault, *base, "--istante", "2026-10-03T08:00:00Z").returncode == 2  # voce nuova senza nota
    assert stato(vault, *base, "--istante", "2026-10-03T08:00:00Z", *note, "--commit", "abc1234").returncode == 2
    assert "x" not in leggi_stato(vault, "sharepoint")["items"]


def test_set_watermark_non_scende_mai(vault):
    res = stato(vault, "set-watermark", "sharepoint", "2026-10-01T00:00:00Z")
    assert res.returncode == 0 and "non abbassato" in res.stderr
    assert leggi_stato(vault, "sharepoint")["watermark"] == "2026-10-02T06:50:00Z"
    assert stato(vault, "set-watermark", "sharepoint", "2026-10-05T00:00:00Z").returncode == 0
    assert leggi_stato(vault, "sharepoint")["watermark"] == "2026-10-05T00:00:00Z"
    assert stato(vault, "set-watermark", "sharepoint", "2026-10-01T00:00:00Z", "--forza").returncode == 0
    assert leggi_stato(vault, "sharepoint")["watermark"] == "2026-10-01T00:00:00Z"
    # da null a un valore
    assert stato(vault, "set-watermark", "onedrive", "2026-10-01T00:00:00Z").returncode == 0
    assert stato(vault, "set-watermark", "onedrive", "ieri").returncode == 2


def test_set_repo_e_last_run(vault):
    res = stato(vault, "set-repo", "owner/repo", "--commit", "a" * 40, "--watermark", "2026-10-26T00:14:20Z")
    assert res.returncode == 0, res.stderr
    res = stato(vault, "set-repo", "owner/repo", "--commit", "b" * 40, "--watermark", "2026-10-20T00:00:00Z")
    assert res.returncode == 0 and "non aggiornato" in res.stderr
    assert json.loads(stato(vault, "repo", "owner/repo").stdout) == {
        "commit": "a" * 40, "watermark": "2026-10-26T00:14:20Z"}
    assert stato(vault, "set-repo", "senza-barra", "--commit", "a" * 7, "--watermark",
                 "2026-10-26T00:14:20Z").returncode == 2
    assert stato(vault, "set-last-run", "2026-10-25T07:47:56Z").returncode == 0
    assert stato(vault, "last-run").stdout.strip() == "2026-10-25T07:47:56Z"


def scrivi_json(p, data):
    p.write_text(json.dumps(data, indent=2), encoding="utf-8")


def test_merge_driver_tre_file(vault, tmp_path):
    base = {"watermark": "2026-10-01T00:00:00Z", "items": {
        "a": {"last_modified": "2026-09-01T00:00:00Z", "note": "sources/a.md"},
        "r": {"last_modified": "2026-09-01T00:00:00Z", "note": "sources/vecchio.md"}}}
    nostro = {"watermark": "2026-10-05T00:00:00Z", "items": {
        "a": {"last_modified": "2026-10-04T00:00:00Z", "note": "sources/a.md"},
        "b": {"last_modified": "2026-10-04T00:00:00Z", "note": "sources/b.md"},
        "r": {"last_modified": "2026-09-01T00:00:00Z", "note": "sources/vecchio.md"}}}
    loro = {"watermark": "2026-10-03T00:00:00Z", "items": {
        "a": {"last_modified": "2026-10-02T00:00:00Z", "note": "sources/a.md"},
        "c": {"last_modified": "2026-10-02T00:00:00Z", "note": "sources/c.md"},
        # stessa data, nota rinominata da loro: vince chi ha cambiato rispetto alla base
        "r": {"last_modified": "2026-09-01T00:00:00Z", "note": "sources/nuovo.md"}}}
    pb, pn, pl = tmp_path / "base", tmp_path / "nostro", tmp_path / "loro"
    for p, d in ((pb, base), (pn, nostro), (pl, loro)):
        scrivi_json(p, d)
    res = stato(vault, "merge-driver", pb, pn, pl)
    assert res.returncode == 0, res.stderr
    out = json.loads(pn.read_text(encoding="utf-8"))
    assert out["watermark"] == "2026-10-05T00:00:00Z"
    assert out["items"]["a"]["last_modified"] == "2026-10-04T00:00:00Z"
    assert set(out["items"]) == {"a", "b", "c", "r"}
    assert out["items"]["r"]["note"] == "sources/nuovo.md"


def test_merge_driver_posta_github_e_base_vuota(vault, tmp_path):
    pb, pn, pl = tmp_path / "base", tmp_path / "nostro", tmp_path / "loro"
    pb.write_text("", encoding="utf-8")  # nessun antenato comune
    scrivi_json(pn, {"watermark": "2026-10-26T11:07:13Z", "threads": {
        "t1": {"last_message": "2026-10-26T11:07:13Z", "note": "sources/mail/x.md"}}})
    scrivi_json(pl, {"watermark": "2026-10-26T12:00:00Z", "threads": {
        "t1": {"last_message": "2026-10-20T00:00:00Z", "note": "sources/mail/x.md"},
        "t2": {"last_message": "2026-10-26T12:00:00Z", "note": "sources/mail/y.md"}}})
    assert stato(vault, "merge-driver", pb, pn, pl).returncode == 0
    out = json.loads(pn.read_text(encoding="utf-8"))
    assert out["watermark"] == "2026-10-26T12:00:00Z"
    assert out["threads"]["t1"]["last_message"] == "2026-10-26T11:07:13Z"
    assert "t2" in out["threads"]
    # github: per i repo vince il watermark più recente
    scrivi_json(pb, {"repos": {}, "items": {}})
    scrivi_json(pn, {"repos": {"o/r": {"commit": "a" * 40, "watermark": "2026-10-20T00:00:00Z"}}, "items": {}})
    scrivi_json(pl, {"repos": {"o/r": {"commit": "b" * 40, "watermark": "2026-10-26T00:00:00Z"}}, "items": {}})
    assert stato(vault, "merge-driver", pb, pn, pl).returncode == 0
    assert json.loads(pn.read_text(encoding="utf-8"))["repos"]["o/r"]["commit"] == "b" * 40


def test_merge_driver_file_illeggibile_lascia_il_conflitto(vault, tmp_path):
    pb, pn, pl = tmp_path / "base", tmp_path / "nostro", tmp_path / "loro"
    scrivi_json(pb, {})
    pn.write_text("<<<<<<< HEAD\n{}\n", encoding="utf-8")
    scrivi_json(pl, {})
    assert stato(vault, "merge-driver", pb, pn, pl).returncode != 0


def test_merge_driver_in_un_rebase_vero(vault, tmp_path):
    """Due cloni scrivono lo stesso file di stato: il rebase passa senza conflitti."""
    driver = f"python3 {SCRIPTS / 'stato.py'} merge-driver %O %A %B"
    (vault / ".gitattributes").write_text(".state/*.json merge=stato\n", encoding="utf-8")
    git(vault, "add", ".gitattributes")
    git(vault, "commit", "-q", "-m", "attributi")
    remoto = tmp_path / "remoto.git"
    git(tmp_path, "clone", "-q", "--bare", str(vault), str(remoto))
    altro = tmp_path / "altro"
    git(tmp_path, "clone", "-q", str(remoto), str(altro))
    # l'altro clone avanza il watermark e aggiunge una voce, e fa push
    assert stato(altro, "set-item", "sharepoint", "item-9", "--istante", "2026-10-09T00:00:00Z",
                 "--note", "sources/sharepoint/delivery/doc-alfa.md").returncode == 0
    assert stato(altro, "set-watermark", "sharepoint", "2026-10-09T00:00:00Z").returncode == 0
    git(altro, "commit", "-q", "-am", "ingest altro")
    git(altro, "push", "-q", "origin", "HEAD")
    # questo clone fa lo stesso con valori diversi, poi pull --rebase
    git(vault, "remote", "add", "origin", str(remoto))
    git(vault, "config", "merge.stato.driver", driver)
    assert stato(vault, "set-item", "sharepoint", "item-5", "--istante", "2026-10-05T00:00:00Z",
                 "--note", "sources/sharepoint/delivery/doc-alfa.md").returncode == 0
    assert stato(vault, "set-watermark", "sharepoint", "2026-10-05T00:00:00Z").returncode == 0
    git(vault, "commit", "-q", "-am", "ingest questo")
    ramo = git(vault, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    git(vault, "pull", "-q", "--rebase", "origin", ramo)
    out = leggi_stato(vault, "sharepoint")
    assert out["watermark"] == "2026-10-09T00:00:00Z"
    assert {"item-1", "item-5", "item-9"} <= set(out["items"])
    assert "<<<<<<<" not in (vault / ".state" / "sharepoint.json").read_text(encoding="utf-8")


def test_risolvi_a_mano_un_conflitto_rimasto(vault, tmp_path):
    """Senza merge driver configurato il rebase si ferma: `risolvi` chiude il conflitto."""
    ramo = git(vault, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    git(vault, "checkout", "-q", "-b", "altro")
    assert stato(vault, "set-watermark", "sharepoint", "2026-10-09T00:00:00Z").returncode == 0
    git(vault, "commit", "-q", "-am", "altro")
    git(vault, "checkout", "-q", ramo)
    assert stato(vault, "set-watermark", "sharepoint", "2026-10-05T00:00:00Z").returncode == 0
    git(vault, "commit", "-q", "-am", "questo")
    res = subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.com",
                          "-c", "core.hooksPath=/dev/null", "merge", "altro"],
                         cwd=vault, capture_output=True, text=True)
    assert res.returncode != 0  # conflitto
    res = stato(vault, "risolvi")
    assert res.returncode == 0, res.stderr
    assert leggi_stato(vault, "sharepoint")["watermark"] == "2026-10-09T00:00:00Z"
    assert git(vault, "diff", "--name-only", "--diff-filter=U").stdout.strip() == ""


def test_cartelle_prima_fotografia_e_riordino(vault, tmp_path):
    el = tmp_path / "elenco.json"
    scrivi_json(el, {"f1": "Deck", "f2": "Product Portfolio", "f3": "Product Portfolio/Pulse"})
    args = ("--libreria", "SalesMarketing", "--profondita", "2", "--elenco", el)
    res = stato(vault, "set-cartelle", "sharepoint", "drv", "--istante", "2026-10-29T05:00:00Z", *args)
    assert res.returncode == 0, res.stderr
    out = json.loads(res.stdout)
    assert out["prima"] is True and out["riordino"] is False and out["cartelle"] == 3
    # stessa struttura il giorno dopo: niente riordino
    out = json.loads(stato(vault, "set-cartelle", "sharepoint", "drv", "--istante", "2026-10-30T05:00:00Z", *args).stdout)
    assert out["prima"] is False and out["riordino"] is False
    # riordino del 30/10: una cartella rinominata, una nuova, una sparita
    scrivi_json(el, {"f2": "02 - Offerte", "f3": "02 - Offerte/Pulse", "f4": "01 - Materiali istituzionali"})
    out = json.loads(stato(vault, "set-cartelle", "sharepoint", "drv", "--istante", "2026-10-31T05:00:00Z", *args).stdout)
    assert out["riordino"] is True
    assert out["nuove"] == ["01 - Materiali istituzionali"] and out["sparite"] == ["Deck"]
    assert out["spostate"] == [{"a": "02 - Offerte", "da": "Product Portfolio"},
                               {"a": "02 - Offerte/Pulse", "da": "Product Portfolio/Pulse"}]
    voce = json.loads(stato(vault, "cartelle", "sharepoint", "drv").stdout)
    assert voce["istante"] == "2026-10-31T05:00:00Z" and voce["libreria"] == "SalesMarketing"
    assert stato(vault, "cartelle", "sharepoint", "altro").returncode == 1
    # gli items restano dove sono
    assert leggi_stato(vault, "sharepoint")["items"] == STATO["sharepoint"]["items"]


def test_set_cartelle_validazione(vault, tmp_path):
    el = tmp_path / "elenco.json"
    scrivi_json(el, {"f1": "A/B/C"})
    base = ("set-cartelle", "sharepoint", "drv", "--libreria", "X", "--istante", "2026-10-31T05:00:00Z")
    res = stato(vault, *base, "--profondita", "2", "--elenco", el)
    assert res.returncode != 0 and "oltre la profondità" in res.stderr
    assert stato(vault, *base, "--profondita", "0", "--elenco", el).returncode != 0
    assert stato(vault, *base[:-2], "--istante", "ieri", "--profondita", "3", "--elenco", el).returncode != 0
    assert stato(vault, "set-cartelle", "outlook", "drv", "--libreria", "X", "--istante",
                 "2026-10-31T05:00:00Z", "--profondita", "3", "--elenco", el).returncode != 0
    assert stato(vault, *base, "--profondita", "3").returncode != 0  # manca --elenco
    # una fotografia più vecchia non sostituisce quella registrata
    assert stato(vault, *base, "--profondita", "3", "--elenco", el).returncode == 0
    res = stato(vault, *base[:-2], "--istante", "2026-10-30T05:00:00Z", "--profondita", "3", "--elenco", el)
    assert res.returncode != 0 and "più vecchia" in res.stderr
    # cambiare profondità riparte da una prima fotografia
    scrivi_json(el, {"f1": "A"})
    out = json.loads(stato(vault, *base[:-2], "--istante", "2026-11-01T05:00:00Z", "--profondita", "1",
                           "--elenco", el).stdout)
    assert out["prima"] is True and out["riordino"] is False


def test_merge_driver_cartelle_vince_la_fotografia_piu_recente(vault, tmp_path):
    pb, pn, pl = tmp_path / "base", tmp_path / "nostro", tmp_path / "loro"
    vecchia = {"libreria": "D", "profondita": 2, "istante": "2026-10-30T05:00:00Z", "elenco": {"f": "A"}}
    nuova = {"libreria": "D", "profondita": 2, "istante": "2026-10-31T05:00:00Z", "elenco": {"f": "B"}}
    scrivi_json(pb, {"watermark": None, "items": {}})
    scrivi_json(pn, {"watermark": None, "items": {}, "cartelle": {"d1": nuova, "d2": vecchia}})
    scrivi_json(pl, {"watermark": None, "items": {}, "cartelle": {"d1": vecchia, "d3": vecchia}})
    assert stato(vault, "merge-driver", pb, pn, pl).returncode == 0
    out = json.loads(pn.read_text(encoding="utf-8"))["cartelle"]
    assert out["d1"]["elenco"] == {"f": "B"} and set(out) == {"d1", "d2", "d3"}
