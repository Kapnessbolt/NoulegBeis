"""Test di stato.py per l'identità dei documenti (SPEC 6.4, audit 31/10 P1 e P7): indice inverso,
`voci`, `trova`, `collega`, `set-assente`, `set-riconciliazione-dovuta` e merge per campo."""

import json

from conftest import SCRIPTS, esegui, git, leggi_stato, scrivi

DOC_ALFA = "sources/sharepoint/delivery/doc-alfa.md"
LM = "2026-10-01T10:00:00Z"


def stato(root, *args):
    return esegui("stato.py", root, *args)


def nota_fonte(root, rel, family, nome, item_id, drive="drv", versions=(), also_at=(), status="active",
               fonte="sharepoint", lm="2026-10-10T10:00:00Z"):
    """Nota source-doc minima più la sua voce nello stato `<drive>/<item_id>`."""
    righe = [f"  - {{ name: {json.dumps(n)}, item_id: {json.dumps(i)}, last_modified: {lm} }}" for n, i in versions]
    copie = [f"  - {{ web_url: {json.dumps(u)}, item_id: {json.dumps(i)} }}" for u, i in also_at]
    testo = "\n".join([
        "---", "type: source-doc", f"source: {fonte}", f"family: {family}", "current:",
        f"  item_id: {item_id}", f"  uri: file:///{drive}/{item_id}",
        f"  web_url: {json.dumps('https://example.sharepoint.com/sites/internal/x/' + nome)}",
        f"  name: {json.dumps(nome)}", f"  last_modified: {lm}",
        "versions:" + ("" if righe else " []"), *righe, "also_at:" + ("" if copie else " []"), *copie,
        f"status: {status}", "---", "", f"# {family}", ""])
    scrivi(root, rel, testo)
    res = stato(root, "set-item", fonte, f"{drive}/{item_id}", "--istante", lm, "--note", rel)
    assert res.returncode == 0, res.stderr
    return f"{drive}/{item_id}"


# --- Indice inverso e voci --------------------------------------------------------------

def test_indice_e_voci_della_nota(vault):
    assert stato(vault, "set-item", "sharepoint", "drv/vecchio", "--istante", "2026-09-01T00:00:00Z",
                 "--note", DOC_ALFA).returncode == 0
    res = stato(vault, "indice", "sharepoint")
    assert res.returncode == 0, res.stderr
    assert json.loads(res.stdout) == {DOC_ALFA: ["drv/vecchio", "item-1"]}
    res = stato(vault, "voci", "sharepoint", DOC_ALFA)
    assert res.returncode == 0, res.stderr
    assert json.loads(res.stdout) == {
        "drv/vecchio": {"last_modified": "2026-09-01T00:00:00Z", "note": DOC_ALFA},
        "item-1": {"last_modified": LM, "note": DOC_ALFA}}
    # anche con il percorso assoluto
    assert json.loads(stato(vault, "voci", "sharepoint", vault / DOC_ALFA).stdout) == json.loads(res.stdout)
    # nessuna voce: 1, JSON vuoto
    res = stato(vault, "voci", "sharepoint", "sources/sharepoint/delivery/manca.md")
    assert res.returncode == 1 and json.loads(res.stdout) == {} and "nessuna voce" in res.stderr
    assert json.loads(stato(vault, "indice", "outlook").stdout) == {}
    # errori d'uso
    assert stato(vault, "voci", "sconosciuta", DOC_ALFA).returncode == 2
    assert stato(vault, "voci", "sharepoint").returncode == 2
    assert stato(vault, "indice", "reconcile").returncode == 2


def test_funzioni_importabili(vault, monkeypatch):
    """riconcilia.py e sposta-nota.py importano il modulo: le funzioni leggono lo stesso stato."""
    import importlib
    import sys
    monkeypatch.setenv("VAULT_ROOT", str(vault))
    sys.path.insert(0, str(SCRIPTS))
    sys.modules.pop("stato", None)
    modulo = importlib.import_module("stato")
    try:
        assert modulo.indice_note("sharepoint") == {DOC_ALFA: ["item-1"]}
        assert modulo.voci_della_nota("sharepoint", DOC_ALFA) == {"item-1": {"last_modified": LM, "note": DOC_ALFA}}
        r = modulo.trova("sharepoint", nome="doc_alfa_v2.pdf")
        assert r["famiglia"] == "doc-alfa" and [c["nota"] for c in r["candidati"]] == [DOC_ALFA]
    finally:
        sys.modules.pop("stato", None)


# --- trova ------------------------------------------------------------------------------

def test_trova_per_nome_senza_maiuscole_e_con_url_decodificato(vault):
    rel = "sources/sharepoint/salesmarketing/offerte/offerta-pilota.md"
    chiave = nota_fonte(vault, rel, "offerta-pilota", "Offerta Pilota_v3.pdf", "I1")
    res = stato(vault, "trova", "sharepoint", "--nome", "offerta%20pilota_V3.PDF", "--json",
                "--cartella", "sources/sharepoint/salesmarketing/offerte/")
    assert res.returncode == 0, res.stderr
    r = json.loads(res.stdout)
    assert r["famiglia"] == "offerta-pilota"
    assert r["candidati"] == [{"nota": rel, "family": "offerta-pilota", "status": "active",
                               "stessa_cartella": True, "stessa_libreria": True, "motivo": "nome, famiglia",
                               "chiavi": [chiave], "chiave_corrente": chiave}]
    # nome diverso, stessa famiglia (versione nuova): solo `famiglia`
    r = json.loads(stato(vault, "trova", "sharepoint", "--nome", "Offerta Pilota_v4.pdf", "--json").stdout)
    assert [(c["nota"], c["motivo"], c["stessa_cartella"]) for c in r["candidati"]] == [(rel, "famiglia", False)]
    # testo: una riga per candidato
    res = stato(vault, "trova", "sharepoint", "--nome", "Offerta Pilota_v3.pdf")
    assert res.returncode == 0 and res.stdout.strip().splitlines() == [
        f"{rel} · family offerta-pilota · active · nome, famiglia · 1 voci"]


def test_trova_nomi_di_versioni_e_copie_e_chiave_corrente(vault):
    rel = "sources/sharepoint/delivery/clienti/listino.md"
    chiave = nota_fonte(vault, rel, "listino", "Listino_2026.xlsx", "NUOVO",
                        versions=[("Listino_2026.xlsx", "NUOVO"), ("Listino prezzi base.xlsx", "VECCHIO")],
                        also_at=[("https://example.sharepoint.com/sites/partner/Docs/Listino%20Partner.xlsx", "COPIA")])
    # voce vecchia sulla stessa nota (ricaricamento): la corrente è quella dell'item_id di `current`
    assert stato(vault, "set-item", "sharepoint", "drv/VECCHIO", "--istante", "2026-09-01T00:00:00Z",
                 "--note", rel).returncode == 0
    for nome in ("listino prezzi base.xlsx", "Listino Partner.xlsx"):
        r = json.loads(stato(vault, "trova", "sharepoint", "--nome", nome, "--json").stdout)
        assert [c["nota"] for c in r["candidati"]] == [rel], nome
        assert "nome" in r["candidati"][0]["motivo"]
        assert r["candidati"][0]["chiavi"] == ["drv/NUOVO", "drv/VECCHIO"]
        assert r["candidati"][0]["chiave_corrente"] == chiave
    # famiglia passata: la famiglia calcolata da un nome di versione basta
    r = json.loads(stato(vault, "trova", "sharepoint", "--famiglia", "listino-prezzi-base", "--json").stdout)
    assert [(c["nota"], c["motivo"]) for c in r["candidati"]] == [(rel, "famiglia")]
    # chiave corrente non nello stato (mini-vault: `item-1` contro un item_id lungo): null
    r = json.loads(stato(vault, "trova", "sharepoint", "--nome", "Doc_Alfa_v2.pdf", "--json").stdout)
    assert r["candidati"][0]["chiave_corrente"] is None


def test_trova_prefisso_di_disambiguazione_e_non_il_solo_suffisso(vault):
    con_prefisso = "sources/sharepoint/delivery/velo/handoff/velo-ce-handoff-afc.md"
    nota_fonte(vault, con_prefisso, "velo-ce-handoff-afc", "Handoff AFC - v002.xlsx", "H1")
    altra = "sources/sharepoint/delivery/velo/verbali/velo-ce-verbale-codifica-handoff-afc.md"
    nota_fonte(vault, altra, "velo-ce-verbale-codifica-handoff-afc", "Verbale codifica handoff AFC.docx", "H2")
    r = json.loads(stato(vault, "trova", "sharepoint", "--famiglia", "handoff-afc", "--json").stdout)
    assert [c["nota"] for c in r["candidati"]] == [con_prefisso]
    r = json.loads(stato(vault, "trova", "sharepoint", "--nome", "Handoff AFC - v003.xlsx", "--json").stdout)
    assert [c["nota"] for c in r["candidati"]] == [con_prefisso]
    # la family registrata con il prefisso, passata così com'è
    r = json.loads(stato(vault, "trova", "sharepoint", "--famiglia", "velo-ce-handoff-afc", "--json").stdout)
    assert [c["nota"] for c in r["candidati"]] == [con_prefisso]


def test_trova_ordine_libreria_e_stato_rimosso(vault):
    stessa = "sources/sharepoint/delivery/progetti/report.md"
    libreria = "sources/sharepoint/delivery/archivio/report-2.md"
    altra_lib = "sources/sharepoint/salesmarketing/report-3.md"
    partner = "sources/sharepoint/_partner/docs/report-4.md"
    nota_fonte(vault, altra_lib, "report", "Report.pdf", "R3")
    nota_fonte(vault, partner, "report", "Report.pdf", "R4")
    nota_fonte(vault, libreria, "report", "Report_v1.pdf", "R2", status="removed")
    nota_fonte(vault, stessa, "report", "Report_v2.pdf", "R1")
    res = stato(vault, "trova", "sharepoint", "--famiglia", "report", "--cartella",
                "sources/sharepoint/delivery/progetti", "--json")
    r = json.loads(res.stdout)
    assert [(c["nota"], c["stessa_cartella"], c["stessa_libreria"]) for c in r["candidati"]] == [
        (stessa, True, True), (libreria, False, True), (partner, False, False), (altra_lib, False, False)]
    assert [c["status"] for c in r["candidati"]][:2] == ["active", "removed"]
    # --libreria restringe alle note della libreria (slug del nome)
    r = json.loads(stato(vault, "trova", "sharepoint", "--nome", "report.pdf", "--libreria", "SalesMarketing",
                         "--json").stdout)
    assert [(c["nota"], c["stessa_libreria"], c["motivo"]) for c in r["candidati"]] == [
        (altra_lib, True, "nome, famiglia")]
    # la cartella di un altro sito: la libreria è il segmento dopo `_<sito>`
    r = json.loads(stato(vault, "trova", "sharepoint", "--famiglia", "report", "--cartella",
                         "sources/sharepoint/_partner/docs/sotto", "--json").stdout)
    assert [c["nota"] for c in r["candidati"] if c["stessa_libreria"]] == [partner]
    # testo: la stessa cartella e la stessa libreria si leggono nella riga
    righe = stato(vault, "trova", "sharepoint", "--famiglia", "report", "--cartella",
                  "sources/sharepoint/delivery/progetti").stdout.splitlines()
    assert righe[0].endswith("stessa cartella · 1 voci") and "stessa libreria" in righe[1]


def test_trova_onedrive_ignora_la_libreria(vault):
    rel = "sources/onedrive/corsi/programma.md"
    nota_fonte(vault, rel, "programma", "Programma.docx", "O1", fonte="onedrive")
    r = json.loads(stato(vault, "trova", "onedrive", "--nome", "Programma.docx", "--libreria", "Documents",
                         "--cartella", "sources/onedrive/altro", "--json").stdout)
    assert [(c["nota"], c["stessa_cartella"], c["stessa_libreria"]) for c in r["candidati"]] == [(rel, False, True)]
    # le note di sharepoint non sono candidate per onedrive
    assert stato(vault, "trova", "onedrive", "--nome", "Doc_Alfa_v2.pdf").returncode == 1


def test_trova_nessun_candidato_ed_errori(vault):
    res = stato(vault, "trova", "sharepoint", "--nome", "Inesistente.pdf", "--json")
    assert res.returncode == 1 and json.loads(res.stdout) == {"famiglia": "inesistente", "candidati": []}
    res = stato(vault, "trova", "sharepoint", "--famiglia", "inesistente")
    assert res.returncode == 1 and res.stdout == "" and "nessun candidato" in res.stderr
    # una voce verso una nota che non c'è più non rompe la ricerca
    assert stato(vault, "set-item", "sharepoint", "drv/orfana", "--istante", LM,
                 "--note", "sources/sharepoint/delivery/sparita.md").returncode == 0
    assert stato(vault, "trova", "sharepoint", "--nome", "Doc_Alfa_v2.pdf").returncode == 0
    assert stato(vault, "trova", "sharepoint").returncode == 2                       # né nome né famiglia
    assert stato(vault, "trova", "sharepoint", "--famiglia", " ").returncode == 2
    assert stato(vault, "trova", "outlook", "--nome", "x.pdf").returncode == 2        # fonte senza documenti
    assert stato(vault, "trova", "github", "--nome", "x.pdf").returncode == 2
    assert stato(vault, "trova", "sharepoint", "--nome").returncode == 2              # opzione senza valore
    assert stato(vault, "trova", "sharepoint", "--tipo", "x").returncode == 2         # opzione sconosciuta


# --- collega ----------------------------------------------------------------------------

def test_collega_voce_nuova_sulla_stessa_nota_idempotente(vault):
    p = vault / ".state" / "sharepoint.json"
    res = stato(vault, "collega", "sharepoint", "drv/nuovo", "--stessa-nota-di", "item-1",
                "--istante", "2026-10-29T16:00:00Z", "--json")
    assert res.returncode == 0, res.stderr
    assert json.loads(res.stdout) == {"fonte": "sharepoint", "chiave": "drv/nuovo", "stessa_nota_di": "item-1",
                                      "cambiato": True, "last_modified": "2026-10-29T16:00:00Z", "note": DOC_ALFA}
    items = leggi_stato(vault, "sharepoint")["items"]
    assert items["drv/nuovo"] == {"last_modified": "2026-10-29T16:00:00Z", "note": DOC_ALFA}
    assert items["item-1"] == {"last_modified": LM, "note": DOC_ALFA}  # la vecchia resta
    # seconda volta: niente da scrivere, lo dice, file identico
    prima = p.read_bytes()
    res = stato(vault, "collega", "sharepoint", "drv/nuovo", "--stessa-nota-di", "item-1",
                "--istante", "2026-10-29T16:00:00Z")
    assert res.returncode == 0 and "già collegata" in res.stdout
    assert p.read_bytes() == prima
    # un istante più vecchio sulla voce già collegata non la abbassa
    res = stato(vault, "collega", "sharepoint", "drv/nuovo", "--stessa-nota-di", "item-1",
                "--istante", "2026-10-20T00:00:00Z", "--json")
    assert json.loads(res.stdout)["cambiato"] is False and p.read_bytes() == prima


def test_collega_toglie_assente_e_corregge_la_nota(vault):
    altra = "sources/sharepoint/delivery/altra.md"
    assert stato(vault, "set-item", "sharepoint", "drv/x", "--istante", LM, "--note", altra).returncode == 0
    assert stato(vault, "set-assente", "sharepoint", "drv/x").returncode == 0
    res = stato(vault, "collega", "sharepoint", "drv/x", "--stessa-nota-di", "item-1", "--istante", LM)
    assert res.returncode == 0 and "puntava a" in res.stderr
    assert leggi_stato(vault, "sharepoint")["items"]["drv/x"] == {"last_modified": LM, "note": DOC_ALFA}
    # stessa nota ma con `assente`: lo toglie (la voce cambia)
    assert stato(vault, "set-assente", "sharepoint", "drv/x").returncode == 0
    r = json.loads(stato(vault, "collega", "sharepoint", "drv/x", "--stessa-nota-di", "item-1",
                         "--istante", LM, "--json").stdout)
    assert r["cambiato"] is True and "assente" not in leggi_stato(vault, "sharepoint")["items"]["drv/x"]


def test_collega_errori(vault):
    prima = leggi_stato(vault, "sharepoint")
    base = ["collega", "sharepoint", "drv/nuovo"]
    assert stato(vault, *base, "--stessa-nota-di", "manca", "--istante", LM).returncode == 2
    assert stato(vault, *base, "--stessa-nota-di", "item-1").returncode == 2              # senza istante
    assert stato(vault, *base, "--istante", LM).returncode == 2                           # senza vecchia
    assert stato(vault, *base, "--stessa-nota-di", "item-1", "--istante", "ieri").returncode == 2
    assert stato(vault, "collega", "github", "o/r:x", "--stessa-nota-di", "o/r:y", "--istante", LM).returncode == 2
    assert stato(vault, "collega", "outlook", "t", "--stessa-nota-di", "u", "--istante", LM).returncode == 2
    assert stato(vault, "collega", "sharepoint", "--stessa-nota-di", "item-1", "--istante", LM).returncode == 2
    assert leggi_stato(vault, "sharepoint") == prima


# --- set-assente ------------------------------------------------------------------------

def test_set_assente_conta_e_azzera(vault):
    p = vault / ".state" / "sharepoint.json"
    for n in (1, 2):
        res = stato(vault, "set-assente", "sharepoint", "item-1", "--json")
        assert res.returncode == 0, res.stderr
        assert json.loads(res.stdout) == {"fonte": "sharepoint", "chiave": "item-1", "assente": n, "cambiato": True}
    assert leggi_stato(vault, "sharepoint")["items"]["item-1"]["assente"] == 2
    res = stato(vault, "set-assente", "sharepoint", "item-1", "--azzera")
    assert res.returncode == 0 and "azzerato" in res.stdout
    assert leggi_stato(vault, "sharepoint")["items"]["item-1"] == {"last_modified": LM, "note": DOC_ALFA}
    prima = p.read_bytes()
    res = stato(vault, "set-assente", "sharepoint", "item-1", "--azzera", "--json")
    assert res.returncode == 0 and json.loads(res.stdout)["cambiato"] is False and p.read_bytes() == prima
    # testo
    assert stato(vault, "set-assente", "sharepoint", "item-1").stdout.strip() == "sharepoint `item-1`: assente 1"


def test_set_item_toglie_assente(vault):
    assert stato(vault, "set-assente", "sharepoint", "item-1").returncode == 0
    assert stato(vault, "set-item", "sharepoint", "item-1", "--istante", "2026-10-05T00:00:00Z").returncode == 0
    assert leggi_stato(vault, "sharepoint")["items"]["item-1"] == {"last_modified": "2026-10-05T00:00:00Z",
                                                                    "note": DOC_ALFA}


def test_set_assente_errori(vault):
    prima = leggi_stato(vault, "sharepoint")
    assert stato(vault, "set-assente", "sharepoint", "manca").returncode == 2
    assert stato(vault, "set-assente", "outlook", "t").returncode == 2
    assert stato(vault, "set-assente", "github", "o/r:x").returncode == 2
    assert stato(vault, "set-assente", "sharepoint").returncode == 2
    assert stato(vault, "set-assente", "sharepoint", "item-1", "--azzera", "--tutto").returncode == 2
    assert leggi_stato(vault, "sharepoint") == prima


# --- set-riconciliazione-dovuta ---------------------------------------------------------

def test_set_riconciliazione_dovuta_tiene_l_istante_vecchio(vault):
    res = stato(vault, "set-riconciliazione-dovuta", "sharepoint", "Delivery", "--istante",
                "2026-10-29T06:50:00Z", "--motivo", "68 ID nuovi con famiglie note", "--json")
    assert res.returncode == 0, res.stderr
    assert json.loads(res.stdout) == {"fonte": "sharepoint", "libreria": "Delivery", "cambiato": True,
                                      "dovuta_dal": "2026-10-29T06:50:00Z",
                                      "riconciliazione_dovuta": {"Delivery": "2026-10-29T06:50:00Z"}}
    # un secondo segnale non sposta l'istante; il motivo va solo nel testo
    res = stato(vault, "set-riconciliazione-dovuta", "sharepoint", "Delivery", "--istante",
                "2026-10-30T06:50:00Z", "--motivo", "ID nuovi")
    assert res.returncode == 0 and "già dovuta dal 2026-10-29" in res.stdout and "(ID nuovi)" in res.stdout
    assert leggi_stato(vault, "sharepoint")["riconciliazione_dovuta"] == {"Delivery": "2026-10-29T06:50:00Z"}
    res = stato(vault, "set-riconciliazione-dovuta", "sharepoint", "SalesMarketing", "--istante",
                "2026-10-30T06:50:00Z", "--motivo", "7 ID nuovi")
    assert res.returncode == 0 and res.stdout.strip() == (
        "sharepoint: riconciliazione di SalesMarketing dovuta dal 2026-10-30 (7 ID nuovi)")
    assert stato(vault, "riconciliazione-dovuta", "sharepoint").stdout.splitlines() == [
        "Riconciliazione dovuta: Delivery dal 2026-10-29", "Riconciliazione dovuta: SalesMarketing dal 2026-10-30"]
    # la toglie solo set-riconciliata
    assert stato(vault, "set-riconciliata", "sharepoint", "Delivery").returncode == 0
    assert leggi_stato(vault, "sharepoint")["riconciliazione_dovuta"] == {"SalesMarketing": "2026-10-30T06:50:00Z"}


def test_set_riconciliazione_dovuta_errori(vault):
    prima = leggi_stato(vault, "sharepoint")
    assert stato(vault, "set-riconciliazione-dovuta", "sharepoint", "Delivery").returncode == 2
    assert stato(vault, "set-riconciliazione-dovuta", "sharepoint", "--istante", LM).returncode == 2
    assert stato(vault, "set-riconciliazione-dovuta", "sharepoint", " ", "--istante", LM).returncode == 2
    assert stato(vault, "set-riconciliazione-dovuta", "sharepoint", "Delivery", "--istante", "oggi").returncode == 2
    assert stato(vault, "set-riconciliazione-dovuta", "outlook", "Posta", "--istante", LM).returncode == 2
    assert leggi_stato(vault, "sharepoint") == prima


# --- P7 · merge per campo ---------------------------------------------------------------

def merge(vault, tmp_path, base, nostro, loro):
    pb, pn, pl = tmp_path / "base", tmp_path / "nostro", tmp_path / "loro"
    for p, d in ((pb, base), (pn, nostro), (pl, loro)):
        p.write_text(json.dumps(d, indent=2), encoding="utf-8")
    res = stato(vault, "merge-driver", pb, pn, pl)
    assert res.returncode == 0, res.stderr
    return json.loads(pn.read_text(encoding="utf-8"))


VECCHIA = "sources/sharepoint/a/x.md"
NUOVA = "sources/sharepoint/b/x.md"


def test_merge_m1_spostamento_e_versione_nuova(vault, tmp_path):
    """Scenario 1 dell'audit (M1): un lato sposta la nota con l'istante vecchio, l'altro registra
    una versione nuova con la nota vecchia: escono la nota nuova e l'istante nuovo, in entrambi i versi."""
    base = {"items": {"k": {"last_modified": "2026-10-01T00:00:00Z", "note": VECCHIA}}}
    sposta = {"items": {"k": {"last_modified": "2026-10-01T00:00:00Z", "note": NUOVA}}}
    versione = {"items": {"k": {"last_modified": "2026-10-30T00:00:00Z", "note": VECCHIA}}}
    atteso = {"last_modified": "2026-10-30T00:00:00Z", "note": NUOVA}
    assert merge(vault, tmp_path, base, sposta, versione)["items"]["k"] == atteso
    assert merge(vault, tmp_path, base, versione, sposta)["items"]["k"] == atteso
    # posta: stessa regola con last_message
    base = {"threads": {"t": {"last_message": "2026-10-01T00:00:00Z", "note": "sources/mail/a.md"}}}
    nostro = {"threads": {"t": {"last_message": "2026-10-01T00:00:00Z", "note": "sources/mail/b.md"}}}
    loro = {"threads": {"t": {"last_message": "2026-10-02T00:00:00Z", "note": "sources/mail/a.md"}}}
    assert merge(vault, tmp_path, base, nostro, loro)["threads"]["t"] == {
        "last_message": "2026-10-02T00:00:00Z", "note": "sources/mail/b.md"}


def test_merge_note_cambiata_da_entrambi_e_commit_con_il_suo_istante(vault, tmp_path):
    base = {"items": {"k": {"last_modified": "2026-10-01T00:00:00Z", "note": VECCHIA}}}
    nostro = {"items": {"k": {"last_modified": "2026-10-02T00:00:00Z", "note": NUOVA}}}
    loro = {"items": {"k": {"last_modified": "2026-10-03T00:00:00Z", "note": "sources/sharepoint/c/x.md"}}}
    assert merge(vault, tmp_path, base, nostro, loro)["items"]["k"]["note"] == "sources/sharepoint/c/x.md"
    # stesso istante, nota cambiata da entrambi: la nostra
    loro["items"]["k"]["last_modified"] = "2026-10-02T00:00:00Z"
    assert merge(vault, tmp_path, base, nostro, loro)["items"]["k"]["note"] == NUOVA
    # github: il commit va con il suo istante, la nota con chi l'ha spostata
    gb = {"repos": {}, "items": {"o/r:a.md": {"last_modified": "2026-10-01T00:00:00Z", "commit": "a" * 7,
                                              "note": "sources/github/r/r-a.md"}}}
    gn = {"repos": {}, "items": {"o/r:a.md": {"last_modified": "2026-10-01T00:00:00Z", "commit": "a" * 7,
                                              "note": "sources/github/r/docs/r-a.md"}}}
    gl = {"repos": {}, "items": {"o/r:a.md": {"last_modified": "2026-10-05T00:00:00Z", "commit": "b" * 7,
                                              "note": "sources/github/r/r-a.md"}}}
    assert merge(vault, tmp_path, gb, gn, gl)["items"]["o/r:a.md"] == {
        "last_modified": "2026-10-05T00:00:00Z", "commit": "b" * 7, "note": "sources/github/r/docs/r-a.md"}


def test_merge_assente(vault, tmp_path):
    voce = {"last_modified": "2026-10-01T00:00:00Z", "note": VECCHIA}
    # un lato conta un'assenza, l'altro non tocca la voce: l'assenza resta
    out = merge(vault, tmp_path, {"items": {"k": voce}}, {"items": {"k": {**voce, "assente": 1}}}, {"items": {"k": voce}})
    assert out["items"]["k"] == {**voce, "assente": 1}
    # un lato la toglie (nota ritrovata, versione nuova), l'altro la incrementa: vince chi l'ha tolta
    base = {"items": {"k": {**voce, "assente": 1}}}
    ritrovata = {"items": {"k": {"last_modified": "2026-10-01T00:00:00Z", "note": VECCHIA}}}
    seconda = {"items": {"k": {**voce, "assente": 2}}}
    assert merge(vault, tmp_path, base, seconda, ritrovata)["items"]["k"] == voce
    assert merge(vault, tmp_path, base, ritrovata, seconda)["items"]["k"] == voce
    # la versione nuova di un lato non cancella il conteggio dell'altro se nessuno l'ha tolto
    nuova = {"items": {"k": {**voce, "last_modified": "2026-10-09T00:00:00Z", "assente": 1}}}
    assert merge(vault, tmp_path, base, seconda, nuova)["items"]["k"] == {
        "last_modified": "2026-10-09T00:00:00Z", "note": VECCHIA, "assente": 2}


def test_merge_m1_in_un_rebase_vero(vault, tmp_path):
    """T7 dell'audit: il ramo A sposta la nota (istante vecchio) e fa push, il ramo B registra una
    versione nuova dello stesso ID e fa pull --rebase: lo stato ha la nota nuova e l'istante nuovo."""
    driver = f"python3 {SCRIPTS / 'stato.py'} merge-driver %O %A %B"
    (vault / ".gitattributes").write_text(".state/*.json merge=stato\n", encoding="utf-8")
    git(vault, "add", ".gitattributes")
    git(vault, "commit", "-q", "-m", "attributi")
    remoto = tmp_path / "remoto.git"
    git(tmp_path, "clone", "-q", "--bare", str(vault), str(remoto))
    altro = tmp_path / "altro"
    git(tmp_path, "clone", "-q", str(remoto), str(altro))
    nuova = "sources/sharepoint/delivery/clienti/doc-alfa.md"
    # ramo A (riconciliazione): sposta la nota e aggiorna `note` con l'istante registrato
    (altro / nuova).parent.mkdir(parents=True)
    git(altro, "mv", DOC_ALFA, nuova)
    assert stato(altro, "set-item", "sharepoint", "item-1", "--istante", LM, "--note", nuova).returncode == 0
    git(altro, "commit", "-q", "-am", "riconcilia: sposta doc-alfa")
    git(altro, "push", "-q", "origin", "HEAD")
    # ramo B (delta): versione nuova dello stesso ID, nota vecchia
    git(vault, "remote", "add", "origin", str(remoto))
    git(vault, "config", "merge.stato.driver", driver)
    assert stato(vault, "set-item", "sharepoint", "item-1", "--istante", "2026-10-30T09:00:00Z").returncode == 0
    git(vault, "commit", "-q", "-am", "ingest: versione nuova")
    ramo = git(vault, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    git(vault, "pull", "-q", "--rebase", "origin", ramo)
    voce = leggi_stato(vault, "sharepoint")["items"]["item-1"]
    assert voce == {"last_modified": "2026-10-30T09:00:00Z", "note": nuova}
    assert (vault / nuova).is_file() and not (vault / DOC_ALFA).exists()
    assert "<<<<<<<" not in (vault / ".state" / "sharepoint.json").read_text(encoding="utf-8")


# --- Uso --------------------------------------------------------------------------------

def test_help_dei_comandi_dell_identita(vault):
    for cmd in ("voci", "indice", "trova", "collega", "set-assente", "set-riconciliazione-dovuta"):
        res = stato(vault, cmd, "--help")
        assert res.returncode == 0, res.stderr
        assert res.stdout.lstrip().startswith(f"stato.py {cmd} "), res.stdout
    assert "--stessa-nota-di" in stato(vault, "collega", "--help").stdout
    assert "--azzera" in stato(vault, "set-assente", "--help").stdout
    assert "prefisso di disambiguazione" in stato(vault, "trova", "--help").stdout
    assert "assente" in stato(vault, "set-item", "--help").stdout
    # l'uso di set-riconciliata non si mescola con quello del comando nuovo
    assert "--istante" not in stato(vault, "set-riconciliata", "--help").stdout
    generale = stato(vault, "--help").stdout
    assert "campo per campo" in generale and '["assente"]' in generale
