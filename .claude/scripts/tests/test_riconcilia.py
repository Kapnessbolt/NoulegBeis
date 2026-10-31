"""Test di riconcilia.py (SPEC 6.4, audit del 31/10 P3) sul mini-vault di conftest.py, con elenchi
delle cartelle sintetici al posto del connettore, e i test di collaudo T1–T10 della proposta
(`proposals/2026-10-31-audit-ingestion.md` §5)."""

import datetime as dt
import json
import sys
from urllib.parse import unquote

import yaml

from conftest import SCRIPTS, TENANT_OD, TENANT_SP, UTENTE_OD, aggiungi, esegui, git, leggi_stato

sys.path.insert(0, str(SCRIPTS))
import famiglia  # noqa: E402

SITO = f"{TENANT_SP}/sites/internal"
PARTNER = f"{TENANT_SP}/sites/partner"
ONEDRIVE = f"{TENANT_OD}/personal/{UTENTE_OD}/Documents/Lavoro"
DRV = "drv"
LM = "2026-10-05T09:00:00Z"
DOC_ALFA = "sources/sharepoint/delivery/doc-alfa.md"
FILE_DOC_ALFA = {"chiave": "item-1", "webUrl": f"{SITO}/Delivery/Doc_Alfa_v2.pdf", "name": "Doc_Alfa_v2.pdf",
                 "lastModifiedDateTime": "2026-10-01T10:00:00Z"}


# --- Aiuti ------------------------------------------------------------------------------

def adesso():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def file_(web_url, item, lm=LM, drive=DRV, nome=None):
    """Un file dell'elenco come lo scrive l'agente dal connettore."""
    return {"id": item, "driveId": drive, "webUrl": web_url,
            "name": nome or unquote(web_url.rsplit("/", 1)[-1]), "lastModifiedDateTime": lm}


def fonte(root, rel, web_url, item, lm=LM, drive=DRV, family=None, status=None):
    """Nota source-doc con nuova-nota.py, coerente con perimetro e famiglia, e la sua voce nello stato."""
    nome = unquote(web_url.rsplit("/", 1)[-1])
    campi = [f"current.item_id={json.dumps(item)}", f"current.uri={json.dumps(f'file:///{drive}/{item}')}",
             f"current.web_url={json.dumps(web_url)}", f"current.name={json.dumps(nome)}",
             f"current.last_modified={lm}", 'projects=["[[alfa]]"]']
    if family:
        campi.append(f"family={family}")
    if status:
        campi.append(f"status={status}")
    args = [x for c in campi for x in ("--campo", c)]
    res = esegui("nuova-nota.py", root, "source-doc", rel, "--titolo", nome, *args)
    assert res.returncode == 0, res.stderr
    fonte_stato = rel.split("/")[1]
    res = esegui("stato.py", root, "set-item", fonte_stato, f"{drive}/{item}", "--istante", lm, "--note", rel)
    assert res.returncode == 0, res.stderr
    return f"{drive}/{item}"


def rel_di(cartella, nome):
    return f"{cartella}/{famiglia.famiglia(nome)}.md"


def riconcilia(root, elenco, *args, codice=0):
    """Esegue riconcilia.py con l'elenco (scritto fuori dal vault) e restituisce il JSON."""
    p = root.parent / "elenco.json"
    p.write_text(json.dumps(elenco, ensure_ascii=False), encoding="utf-8")
    res = esegui("riconcilia.py", root, "--elenco", p, *args, "--json")
    assert res.returncode == codice, res.stdout + res.stderr
    return json.loads(res.stdout)


def voci(piano, tipo=None):
    return [v for v in piano["voci"] if tipo is None or v["tipo"] == tipo]


def fm(root, rel):
    return yaml.safe_load((root / rel).read_text(encoding="utf-8").split("---\n", 2)[1])


def fotografia(root):
    """Contenuto di tutti i file del vault, tranne .git: per confrontare prima e dopo."""
    return {str(p.relative_to(root)): p.read_bytes() for p in sorted(root.rglob("*"))
            if p.is_file() and ".git" not in p.relative_to(root).parts}


def controllo_pulito(root):
    res = esegui("controlla-vault.py", root)
    assert res.returncode == 0, res.stdout + res.stderr
    assert " 0 errori " in res.stdout
    return res.stdout


# --- Uso ed elenco ----------------------------------------------------------------------

def test_help_ed_errori_d_uso(vault, tmp_path):
    res = esegui("riconcilia.py", vault, "--help")
    assert res.returncode == 0 and "--elenco" in res.stdout and "candidati_ambigui" in res.stdout
    assert esegui("riconcilia.py", vault).returncode == 2
    p = tmp_path / "e.json"
    p.write_text(json.dumps([FILE_DOC_ALFA]), encoding="utf-8")
    casi = [
        ("--fonte", "sharepoint"),                                         # manca --elenco
        ("--elenco", p),                                                    # manca --fonte
        ("--elenco", p, "--fonte", "github"),                               # fonte sconosciuta
        ("--elenco", p, "--fonte", "sharepoint", "--libreria", "Knowledge"),  # libreria fuori perimetro
        ("--elenco", tmp_path / "manca.json", "--fonte", "sharepoint"),
        ("--elenco", p, "--fonte", "sharepoint", "--solo", "1"),            # --solo senza --applica
        ("--elenco", p, "--fonte", "sharepoint", "--applica", "--solo", "a"),
        ("--elenco", p, "--fonte", "sharepoint", "--boh"),
    ]
    for args in casi:
        assert esegui("riconcilia.py", vault, *args).returncode == 2, args
    for contenuto in ("non json", json.dumps({"a": 1}), json.dumps([1]),
                      json.dumps([{"id": "x", "driveId": "d", "lastModifiedDateTime": LM}]),          # senza webUrl
                      json.dumps([{"webUrl": f"{SITO}/Delivery/x.pdf", "lastModifiedDateTime": LM}]),  # senza id
                      json.dumps([file_(f"{SITO}/Delivery/x.pdf", "X", lm="2026-10-05")]),
                      json.dumps([file_(f"{SITO}/Delivery/x.pdf", "X"), file_(f"{SITO}/Delivery/y.pdf", "X")])):
        p.write_text(contenuto, encoding="utf-8")
        res = esegui("riconcilia.py", vault, "--elenco", p, "--fonte", "sharepoint")
        assert res.returncode == 2, contenuto
        assert res.stderr.startswith("errore:")


def test_elenco_normalizzato_e_testo(vault, tmp_path):
    # millisecondi, fuso, parentReference, uri, cartelle e {"value": [...]}: tutto lo stesso doc-alfa
    for voce in ({**FILE_DOC_ALFA, "lastModifiedDateTime": "2026-10-01T10:00:00.123Z"},
                 {**FILE_DOC_ALFA, "lastModifiedDateTime": "2026-10-01T12:00:00+02:00"},
                 {"chiave": "item-1", "web_url": FILE_DOC_ALFA["webUrl"], "last_modified": "2026-10-01T10:00:00Z"}):
        piano = riconcilia(vault, {"value": [voce, {"name": "Cartella", "folder": {"childCount": 3},
                                                    "webUrl": f"{SITO}/Delivery/Cartella"}]},
                           "--fonte", "sharepoint")
        assert piano["voci"] == [] and piano["riepilogo"] == {"ok": 1}, piano
        assert piano["elenco"] == 1 and piano["cartelle_saltate"] == 1
    nuovo = riconcilia(vault, [FILE_DOC_ALFA, {"id": "N1", "parentReference": {"driveId": "b!d"},
                                              "webUrl": f"{SITO}/Delivery/Nota_Nuova.pdf",
                                              "lastModifiedDateTime": "2026-09-01T08:00:00.5Z"},
                               {"uri": "file:///b!e/N2", "web_url": f"{SITO}/Delivery/Altra_Nota.pdf",
                                "last_modified": "2026-10-20T08:00:00Z"}], "--fonte", "sharepoint")
    assert [(v["tipo"], v["chiave"], v["last_modified"]) for v in nuovo["voci"]] == [
        ("recupera", "b!d/N1", "2026-09-01T08:00:00Z"), ("in_coda", "b!e/N2", "2026-10-20T08:00:00Z")]
    assert [v["id"] for v in nuovo["voci"]] == [1, 2]
    assert nuovo["voci"][0]["nome"] == "Nota_Nuova.pdf" and nuovo["voci"][0]["cartella_nota"] == "sources/sharepoint/delivery"
    # testo senza --json: una riga per voce e il riepilogo
    p = tmp_path / "e.json"
    p.write_text(json.dumps([FILE_DOC_ALFA]), encoding="utf-8")
    res = esegui("riconcilia.py", vault, "--elenco", p, "--fonte", "sharepoint", "--libreria", "delivery")
    assert res.returncode == 0, res.stderr
    assert res.stdout.startswith("Riconciliazione sharepoint · Delivery: 1 file") and "Riepilogo: ok 1" in res.stdout


def test_ignorati(vault):
    elenco = [FILE_DOC_ALFA,
              file_(f"{SITO}/Knowledge/Corso.pdf", "K1"),                       # libreria fuori perimetro
              file_(f"{SITO}/Delivery/Archivio.zip", "Z1"),                     # tipo non processato
              file_(f"{SITO}/Delivery/Cliente/Dati/Export.xlsx", "D1"),         # cartella esclusa
              file_(f"{ONEDRIVE}/Appunti.docx", "O1"),                          # altra fonte
              file_("https://altro.example.org/x.pdf", "U1"),                   # URL non del tenant
              file_(f"{PARTNER}/Partner/Condivisi/Listino.pdf", "P1"),          # altro sito, nessuna nota
              file_(f"{SITO}/SalesMarketing/Offerta.pdf", "S1")]
    piano = riconcilia(vault, elenco, "--fonte", "sharepoint", "--libreria", "Delivery")
    motivi = {i["chiave"]: i["motivo"] for i in piano["ignorati"]}
    assert set(motivi) == {"drv/K1", "drv/Z1", "drv/D1", "drv/O1", "drv/U1", "drv/P1", "drv/S1"}
    assert "fuori da --libreria Delivery" in motivi["drv/S1"] and "fuori da --libreria" in motivi["drv/K1"]
    assert "non processato" in motivi["drv/Z1"] and "esclusa" in motivi["drv/D1"]
    assert "onedrive" in motivi["drv/O1"]
    assert piano["voci"] == [] and piano["riepilogo"] == {"ok": 1}
    # senza --libreria: Knowledge fuori perimetro, SalesMarketing entra (in coda), il partner resta fuori
    piano = riconcilia(vault, elenco, "--fonte", "sharepoint")
    motivi = {i["chiave"]: i["motivo"] for i in piano["ignorati"]}
    assert "fuori perimetro" in motivi["drv/K1"] and "/ingest-file" in motivi["drv/P1"]
    assert [(v["tipo"], v["chiave"]) for v in piano["voci"]] == [("in_coda", "drv/S1")]


# --- T1 · Riordino sintetico ------------------------------------------------------------

def test_t1_riordino_sintetico(vault, tmp_path):
    """Rinomina di 2 cartelle, 10 file spostati con gli stessi ID: 10 note spostate nella cartella
    di perimetro.py, 0 rimosse; il segnale resta (lo toglie la routine con set-riconciliata)."""
    vecchie = {"Clienti A": "Cliente Alfa", "Clienti B": "Cliente Beta"}
    note = []
    for n, (prima, dopo) in enumerate(vecchie.items()):
        for i in range(5):
            nome = f"Verbale_{'AB'[n]}{i}_v1.pdf"
            rel = rel_di(f"sources/sharepoint/delivery/{famiglia.slug(prima)}", nome)
            item = f"T1{n}{i}"
            fonte(vault, rel, f"{SITO}/Delivery/{prima}/{nome}", item)
            note.append((rel, item, f"{SITO}/Delivery/{dopo}/{nome}", f"sources/sharepoint/delivery/{famiglia.slug(dopo)}"))
    controllo_pulito(vault)
    ist = adesso()
    for foto in ({"f1": "Clienti A", "f2": "Clienti B"}, {"f1": "Cliente Alfa", "f2": "Cliente Beta"}):
        (tmp_path / "foto.json").write_text(json.dumps(foto), encoding="utf-8")
        res = esegui("stato.py", vault, "set-cartelle", "sharepoint", DRV, "--libreria", "Delivery",
                     "--profondita", "2", "--istante", ist, "--elenco", tmp_path / "foto.json")
        assert res.returncode == 0, res.stderr
    assert json.loads(res.stdout)["riordino"] is True
    assert leggi_stato(vault, "sharepoint")["riconciliazione_dovuta"] == {"Delivery": ist}

    elenco = [FILE_DOC_ALFA] + [file_(url, item) for _, item, url, _ in note]
    piano = riconcilia(vault, elenco, "--fonte", "sharepoint", "--libreria", "Delivery")
    assert piano["riepilogo"] == {"sposta": 10, "ok": 1}
    assert all(v["cambia_cartella"] and not v["cambia_famiglia"] for v in voci(piano))
    risultato = riconcilia(vault, elenco, "--fonte", "sharepoint", "--libreria", "Delivery", "--applica")
    assert risultato["esiti"] == {"fatto": 10}
    items = leggi_stato(vault, "sharepoint")["items"]
    for rel, item, url, cartella in note:
        dopo = f"{cartella}/{rel.rsplit('/', 1)[-1]}"
        assert not (vault / rel).exists() and (vault / dopo).is_file()
        d = fm(vault, dopo)
        assert d["current"]["web_url"] == url and d["status"] == "active"
        assert items[f"{DRV}/{item}"]["note"] == dopo
    assert leggi_stato(vault, "sharepoint")["riconciliazione_dovuta"] == {"Delivery": ist}
    assert not any(fm(vault, p.relative_to(vault))["status"] == "removed" for p in (vault / "sources").rglob("*.md"))
    controllo_pulito(vault)
    # il piano sullo stesso elenco ora è vuoto
    assert riconcilia(vault, elenco, "--fonte", "sharepoint", "--libreria", "Delivery")["riepilogo"] == {"ok": 11}


# --- T2 · Spostato e rinominato con famiglia nuova --------------------------------------

def test_t2_spostato_e_rinominato(vault):
    rel = "sources/sharepoint/delivery/offerta-pilota.md"
    fonte(vault, rel, f"{SITO}/Delivery/Offerta_Pilota_v1.docx", "OFF1")
    aggiungi(vault, "projects/alfa/alfa.md", "- [[offerta-pilota]]")
    url = f"{SITO}/Delivery/Contratti/Contratto_Pilota_v3.docx"
    elenco = [FILE_DOC_ALFA, file_(url, "OFF1")]
    piano = riconcilia(vault, elenco, "--fonte", "sharepoint")
    (v,) = voci(piano)
    assert (v["tipo"], v["cambia_cartella"], v["cambia_famiglia"], v["cartella_nuova"]) == (
        "sposta", True, True, "sources/sharepoint/delivery/contratti")
    risultato = riconcilia(vault, elenco, "--fonte", "sharepoint", "--applica")
    dopo = "sources/sharepoint/delivery/contratti/contratto-pilota.md"
    assert risultato["voci"][0]["esito"] == "fatto" and risultato["voci"][0]["nota_dopo"] == dopo
    assert not (vault / rel).exists() and list((vault / "sources").rglob("*pilota*.md")) == [vault / dopo]
    d = fm(vault, dopo)
    assert d["family"] == "contratto-pilota" and d["current"]["web_url"] == url
    alfa = (vault / "projects/alfa/alfa.md").read_text(encoding="utf-8")
    assert "[[offerta-pilota]]" not in alfa and "[[contratto-pilota]]" in alfa
    assert leggi_stato(vault, "sharepoint")["items"][f"{DRV}/OFF1"]["note"] == dopo
    controllo_pulito(vault)


# --- T3 · Cartella ricaricata -----------------------------------------------------------

def test_t3_cartella_ricaricata(vault, tmp_path):
    """ID nuovi, stessi percorsi e nomi: voci nuove sulla stessa nota, versione nuova in testa,
    0 note nuove, 0 rimosse; il rilevatore delle cartelle vede «nuove» e «sparite» uguali."""
    cartella = "sources/sharepoint/delivery/pilota"
    file_vecchi = {}
    for i, nome in enumerate(("Report_Uno_v1.pdf", "Report_Due_v1.pdf")):
        url = f"{SITO}/Delivery/Pilota/{nome}"
        fonte(vault, rel_di(cartella, nome), url, f"OLD{i}")
        file_vecchi[rel_di(cartella, nome)] = (url, f"OLD{i}", f"NEW{i}")
    ingested = {rel: fm(vault, rel)["ingested_at"] for rel in file_vecchi}
    note_prima = sorted((vault / "sources").rglob("*.md"))
    # il rilevatore: stessa cartella con un ID nuovo
    for foto in ({"fold-old": "Pilota"}, {"fold-new": "Pilota"}):
        (tmp_path / "foto.json").write_text(json.dumps(foto), encoding="utf-8")
        res = esegui("stato.py", vault, "set-cartelle", "sharepoint", DRV, "--libreria", "Delivery",
                     "--profondita", "2", "--istante", adesso(), "--elenco", tmp_path / "foto.json")
    confronto = json.loads(res.stdout)
    assert confronto["riordino"] and confronto["nuove"] == confronto["sparite"] == ["Pilota"]

    elenco = [FILE_DOC_ALFA] + [file_(url, new) for url, _, new in file_vecchi.values()]
    piano = riconcilia(vault, elenco, "--fonte", "sharepoint", "--libreria", "Delivery")
    assert piano["riepilogo"] == {"nuova_voce": 2, "ok": 1}
    for v in voci(piano):
        assert v["diventa_current"] and not v["rileggi"] and v["chiave_corrente"] == f"{DRV}/{file_vecchi[v['nota']][1]}"
    risultato = riconcilia(vault, elenco, "--fonte", "sharepoint", "--libreria", "Delivery", "--applica")
    assert risultato["esiti"] == {"fatto": 2}
    items = leggi_stato(vault, "sharepoint")["items"]
    for rel, (url, old, new) in file_vecchi.items():
        d = fm(vault, rel)
        assert d["current"]["item_id"] == new and d["current"]["uri"] == f"file:///{DRV}/{new}"
        assert [x["item_id"] for x in d["versions"]] == [new, old]
        assert d["ingested_at"] == ingested[rel]  # niente da rileggere: ingested_at invariato
        assert items[f"{DRV}/{old}"]["note"] == items[f"{DRV}/{new}"]["note"] == rel
    assert sorted((vault / "sources").rglob("*.md")) == note_prima
    assert not any(v.get("assente") for v in items.values())
    controllo_pulito(vault)
    assert riconcilia(vault, elenco, "--fonte", "sharepoint", "--libreria", "Delivery")["riepilogo"] == {"ok": 3}


# --- T4 · Copia su un altro sito e nella libreria interna -------------------------------

def test_t4_copia_partner_dopo_la_interna(vault):
    rel = "sources/sharepoint/salesmarketing/listini/listino-partner.md"
    interna = f"{SITO}/SalesMarketing/Listini/Listino_Partner_v2.pdf"
    partner = f"{PARTNER}/Partner/Condivisi/Listino_Partner_v2.pdf"
    fonte(vault, rel, interna, "SM1")
    elenco = [FILE_DOC_ALFA, file_(interna, "SM1"), file_(partner, "P1", drive="drvP")]
    piano = riconcilia(vault, elenco, "--fonte", "sharepoint")
    (v,) = voci(piano)
    assert (v["tipo"], v["nota"], v["diventa_current"], v["rango_nuovo"], v["rango_corrente"]) == (
        "copia", rel, False, 4, 0)
    assert v["motivo"].startswith("nome")
    riconcilia(vault, elenco, "--fonte", "sharepoint", "--applica")
    d = fm(vault, rel)
    assert d["current"]["web_url"] == interna
    assert d["also_at"] == [{"web_url": partner, "item_id": "P1"}]
    assert leggi_stato(vault, "sharepoint")["items"]["drvP/P1"]["note"] == rel
    assert len(list((vault / "sources").rglob("*listino*.md"))) == 1
    controllo_pulito(vault)
    assert riconcilia(vault, elenco, "--fonte", "sharepoint")["riepilogo"] == {"ok": 3}


def test_t4_copia_interna_dopo_la_partner(vault):
    """Prima la copia sul sito partner, poi quella interna: la interna vince (rango 0) e diventa
    `current`, la nota la segue e la partner va in `also_at`."""
    prima = "sources/sharepoint/_partner/partner/condivisi/listino-partner.md"
    interna = f"{SITO}/SalesMarketing/Listini/Listino_Partner_v2.pdf"
    partner = f"{PARTNER}/Partner/Condivisi/Listino_Partner_v2.pdf"
    fonte(vault, prima, partner, "P1", drive="drvP", lm="2026-10-04T08:00:00Z")
    controllo_pulito(vault)
    elenco = [file_(interna, "SM1")]
    piano = riconcilia(vault, elenco, "--fonte", "sharepoint", "--libreria", "SalesMarketing")
    (v,) = voci(piano)
    assert (v["tipo"], v["diventa_current"], v["rango_nuovo"], v["rango_corrente"]) == ("copia", True, 0, 4)
    assert v["vecchia_current"]["dove"] == "also_at" and v["cartella_nuova"] == "sources/sharepoint/salesmarketing/listini"
    assert v["rileggi"] is True  # last_modified diverso dalla current
    risultato = riconcilia(vault, elenco, "--fonte", "sharepoint", "--libreria", "SalesMarketing", "--applica")
    dopo = "sources/sharepoint/salesmarketing/listini/listino-partner.md"
    assert risultato["voci"][0]["esito"] == "fatto" and risultato["voci"][0]["nota_dopo"] == dopo
    assert not (vault / prima).exists()
    d = fm(vault, dopo)
    assert d["current"]["web_url"] == interna and d["current"]["item_id"] == "SM1"
    assert d["current"]["uri"] == f"file:///{DRV}/SM1"
    assert d["also_at"] == [{"web_url": partner, "item_id": "P1"}]
    items = leggi_stato(vault, "sharepoint")["items"]
    assert items[f"{DRV}/SM1"]["note"] == items["drvP/P1"]["note"] == dopo
    controllo_pulito(vault)
    # riconciliazione completa dopo: entrambe le posizioni sono invariate
    tutto = [FILE_DOC_ALFA, file_(interna, "SM1"), file_(partner, "P1", drive="drvP", lm="2026-10-04T08:00:00Z")]
    assert riconcilia(vault, tutto, "--fonte", "sharepoint")["riepilogo"] == {"ok": 3}


# --- T5 · Watermark e finestra ----------------------------------------------------------

def test_t5_recupera_e_in_coda_senza_toccare_il_watermark(vault):
    """Un file mai ingerito più vecchio del watermark (l'indice in ritardo lo ha fatto saltare) si
    recupera come compito `file`; uno più recente lo prende il delta. Il watermark non cambia."""
    assert leggi_stato(vault, "sharepoint")["watermark"] == "2026-10-02T06:50:00Z"
    elenco = [FILE_DOC_ALFA,
              file_(f"{SITO}/Delivery/Archivio/Verbale_Kickoff.pdf", "X1", lm="2026-10-01T15:00:00Z"),
              file_(f"{SITO}/Delivery/Verbale_Avanzamento.pdf", "X2", lm="2026-10-20T15:00:00Z")]
    stato_prima = (vault / ".state/sharepoint.json").read_bytes()
    risultato = riconcilia(vault, elenco, "--fonte", "sharepoint", "--applica")
    assert [(v["tipo"], v["chiave"], v["nota"], v["aggiorna"], v["esito"]) for v in risultato["voci"]] == [
        ("recupera", "drv/X1", None, False, "all'agente"), ("in_coda", "drv/X2", None, False, "all'agente")]
    assert risultato["voci"][0]["cartella_nota"] == "sources/sharepoint/delivery/archivio"
    assert risultato["watermark"] == "2026-10-02T06:50:00Z"
    assert (vault / ".state/sharepoint.json").read_bytes() == stato_prima
    controllo_pulito(vault)


def test_versione_sfuggita_al_delta(vault):
    """Chiave nota con un lastModified più recente di quello registrato: recupera con `aggiorna`
    se il watermark l'ha superata, in coda altrimenti."""
    for lm, tipo in (("2026-10-01T20:00:00Z", "recupera"), ("2026-10-25T20:00:00Z", "in_coda")):
        piano = riconcilia(vault, [{**FILE_DOC_ALFA, "lastModifiedDateTime": lm}], "--fonte", "sharepoint")
        (v,) = voci(piano)
        assert (v["tipo"], v["nota"], v["aggiorna"], v["last_modified_stato"]) == (
            tipo, DOC_ALFA, True, "2026-10-01T10:00:00Z")
        assert piano["riepilogo"] == {tipo: 1, "ok": 0}


# --- T6 · Idempotenza -------------------------------------------------------------------

def test_t6_applica_due_volte_sullo_stesso_elenco(vault, tmp_path):
    da_spostare = "sources/sharepoint/delivery/relazione-q3.md"
    fonte(vault, da_spostare, f"{SITO}/Delivery/Relazione_Q3.pdf", "R1")
    ricaricata = "sources/sharepoint/delivery/clienti/contratto-quadro.md"
    fonte(vault, ricaricata, f"{SITO}/Delivery/Clienti/Contratto_Quadro.docx", "C1")
    copiata = "sources/sharepoint/salesmarketing/listino-partner.md"
    fonte(vault, copiata, f"{SITO}/SalesMarketing/Listino_Partner_v2.pdf", "L1")
    sparita = "sources/sharepoint/delivery/verbale-chiuso.md"
    fonte(vault, sparita, f"{SITO}/Delivery/Verbale_Chiuso.pdf", "V1")
    elenco = [FILE_DOC_ALFA,
              file_(f"{SITO}/Delivery/Archivio/Relazione_Q3.pdf", "R1"),
              file_(f"{SITO}/Delivery/Clienti/Contratto_Quadro.docx", "C2"),
              file_(f"{SITO}/SalesMarketing/Listino_Partner_v2.pdf", "L1"),
              file_(f"{SITO}/Delivery/Listini/Listino_Partner_v2.pdf", "L2")]
    piano_file = tmp_path / "piano.json"
    primo = riconcilia(vault, elenco, "--fonte", "sharepoint", "--applica", "--piano", piano_file)
    assert primo["riepilogo"] == {"sposta": 1, "copia": 1, "nuova_voce": 1, "in_attesa": 1, "ok": 2}
    assert primo["esiti"] == {"fatto": 4} and not primo.get("ripreso")
    assert json.loads(piano_file.read_text(encoding="utf-8"))["esiti"] == {"fatto": 4}
    assert leggi_stato(vault, "sharepoint")["items"][f"{DRV}/V1"]["assente"] == 1
    dopo = fotografia(vault)
    secondo = riconcilia(vault, elenco, "--fonte", "sharepoint", "--applica", "--piano", piano_file)
    assert secondo["ripreso"] is True and secondo["esiti"] == {"già fatto": 4}
    assert [v["id"] for v in secondo["voci"]] == [v["id"] for v in primo["voci"]]
    assert fotografia(vault) == dopo  # stato e note identici byte per byte
    controllo_pulito(vault)
    # un --piano di un altro elenco non si riprende: il piano si ricalcola
    altro = riconcilia(vault, elenco[:-1], "--fonte", "sharepoint", "--piano", piano_file)
    assert not altro.get("ripreso") and altro["impronta"] != primo["impronta"]


# --- T7 · Giri sovrapposti --------------------------------------------------------------

def test_t7_riconciliazione_e_delta_su_due_rami(vault, tmp_path):
    """Ramo A: riconcilia.py sposta la nota; ramo B: il delta registra una versione nuova dello
    stesso ID; rebase con il merge driver: `note` nuovo e `last_modified` nuovo (P7)."""
    driver = f"{sys.executable} {SCRIPTS / 'stato.py'} merge-driver %O %A %B"
    (vault / ".gitattributes").write_text(".state/*.json merge=stato\n", encoding="utf-8")
    git(vault, "add", ".gitattributes")
    git(vault, "commit", "-q", "-m", "attributi")
    remoto = tmp_path / "remoto.git"
    git(tmp_path, "clone", "-q", "--bare", str(vault), str(remoto))
    altro = tmp_path / "altro"
    git(tmp_path, "clone", "-q", str(remoto), str(altro))
    nuova = "sources/sharepoint/delivery/clienti/doc-alfa.md"
    # ramo A (riconciliazione)
    risultato = riconcilia(altro, [{**FILE_DOC_ALFA, "webUrl": f"{SITO}/Delivery/Clienti/Doc_Alfa_v2.pdf"}],
                           "--fonte", "sharepoint", "--applica")
    assert risultato["voci"][0]["tipo"] == "sposta" and risultato["voci"][0]["esito"] == "fatto"
    git(altro, "add", "-A")
    git(altro, "commit", "-q", "-m", "ingest(riconcilia): Delivery, 1 nota spostata")
    git(altro, "push", "-q", "origin", "HEAD")
    # ramo B (delta): versione nuova dello stesso ID, nota vecchia
    git(vault, "remote", "add", "origin", str(remoto))
    git(vault, "config", "merge.stato.driver", driver)
    assert esegui("stato.py", vault, "set-item", "sharepoint", "item-1", "--istante", "2026-10-30T09:00:00Z").returncode == 0
    git(vault, "commit", "-q", "-am", "ingest(sharepoint): versione nuova")
    ramo = git(vault, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    git(vault, "pull", "-q", "--rebase", "origin", ramo)
    assert leggi_stato(vault, "sharepoint")["items"]["item-1"] == {"last_modified": "2026-10-30T09:00:00Z", "note": nuova}
    assert (vault / nuova).is_file() and not (vault / DOC_ALFA).exists()
    controllo_pulito(vault)


# --- T8 · Riconciliazione interrotta ----------------------------------------------------

def test_t8_applica_interrotta_e_ripresa(vault, tmp_path):
    for nome, item in (("Relazione_Q3.pdf", "R1"), ("Contratto_Quadro.docx", "C1")):
        fonte(vault, rel_di("sources/sharepoint/delivery", nome), f"{SITO}/Delivery/{nome}", item)
    assert esegui("stato.py", vault, "set-riconciliazione-dovuta", "sharepoint", "Delivery",
                  "--istante", adesso()).returncode == 0
    elenco = [FILE_DOC_ALFA, file_(f"{SITO}/Delivery/Archivio/Relazione_Q3.pdf", "R1"),
              file_(f"{SITO}/Delivery/Archivio/Contratto_Quadro.docx", "C1")]
    piano_file = tmp_path / "piano.json"
    piano = riconcilia(vault, elenco, "--fonte", "sharepoint", "--libreria", "Delivery", "--piano", piano_file)
    assert [v["tipo"] for v in piano["voci"]] == ["sposta", "sposta"]
    primo, secondo = piano["voci"]
    # interruzione dopo la prima voce
    parziale = riconcilia(vault, elenco, "--fonte", "sharepoint", "--libreria", "Delivery", "--applica",
                          "--piano", piano_file, "--solo", str(primo["id"]))
    assert parziale["ripreso"] and parziale["voci"][0]["esito"] == "fatto" and "esito" not in parziale["voci"][1]
    assert (vault / "sources/sharepoint/delivery/archivio" / primo["nota"].rsplit("/", 1)[-1]).is_file()
    assert (vault / secondo["nota"]).is_file()
    dovuta = leggi_stato(vault, "sharepoint")["riconciliazione_dovuta"]
    assert "Delivery" in dovuta
    # la ripetizione completa il resto senza rifare la prima
    completo = riconcilia(vault, elenco, "--fonte", "sharepoint", "--libreria", "Delivery", "--applica",
                          "--piano", piano_file)
    assert [v["esito"] for v in completo["voci"]] == ["già fatto", "fatto"]
    assert not (vault / secondo["nota"]).exists()
    assert leggi_stato(vault, "sharepoint")["riconciliazione_dovuta"] == dovuta
    controllo_pulito(vault)


def test_errore_su_una_voce_non_ferma_le_altre(vault):
    fonte(vault, "sources/sharepoint/delivery/relazione-q3.md", f"{SITO}/Delivery/Relazione_Q3.pdf", "R1")
    fonte(vault, "sources/sharepoint/delivery/offerta-pilota.md", f"{SITO}/Delivery/Offerta_Pilota_v1.docx", "O1")
    # la seconda si rinomina in `tema-uno`, lo slug di un tema: sposta-nota.py rifiuta (slug occupato)
    elenco = [FILE_DOC_ALFA, file_(f"{SITO}/Delivery/Archivio/Relazione_Q3.pdf", "R1"),
              file_(f"{SITO}/Delivery/Tema_Uno.docx", "O1")]
    risultato = riconcilia(vault, elenco, "--fonte", "sharepoint", "--applica", codice=1)
    esiti = {v["nota"]: v for v in risultato["voci"]}
    assert esiti["sources/sharepoint/delivery/relazione-q3.md"]["esito"] == "fatto"
    errata = esiti["sources/sharepoint/delivery/offerta-pilota.md"]
    assert errata["esito"] == "errore" and "--slug" in errata["messaggio"]
    assert risultato["esiti"] == {"fatto": 1, "errore": 1}
    controllo_pulito(vault)


# --- T9 · Watermark dal giro ------------------------------------------------------------

def test_t9_due_giri_con_risultati_gia_registrati(vault):
    """Riconcilia non tocca il watermark; due giri con risultati tutti già registrati lo fanno
    salire con set-watermark --da-giro, e il controllo non vede un watermark fermo."""
    fonte(vault, "sources/sharepoint/delivery/relazione-q3.md", f"{SITO}/Delivery/Relazione_Q3.pdf", "R1",
          lm="2026-10-20T10:00:00Z")
    elenco = [FILE_DOC_ALFA, file_(f"{SITO}/Delivery/Relazione_Q3.pdf", "R1", lm="2026-10-20T10:00:00Z")]
    risultato = riconcilia(vault, elenco, "--fonte", "sharepoint", "--applica")
    assert risultato["voci"] == [] and risultato["riepilogo"] == {"ok": 2}
    assert leggi_stato(vault, "sharepoint")["watermark"] == "2026-10-02T06:50:00Z"
    for giorno, piu_recente in (("2026-10-21", "2026-10-20T10:00:00Z"), ("2026-10-22", "2026-10-21T18:30:00Z")):
        assert esegui("stato.py", vault, "set-giro", "sharepoint", "--inizio", f"{giorno}T04:50:00Z",
                      "--fine", f"{giorno}T05:10:00Z", "--risultati", "2", "--piu-recente", piu_recente,
                      "--falliti", "0").returncode == 0
        if giorno == "2026-10-21":
            assert "watermark di sharepoint fermo" in esegui("controlla-vault.py", vault).stdout
        res = esegui("stato.py", vault, "set-watermark", "sharepoint", "--da-giro", "--json")
        assert res.returncode == 0, res.stderr
        assert json.loads(res.stdout)["watermark"] == piu_recente
        assert leggi_stato(vault, "sharepoint")["watermark"] == piu_recente
        assert "fermo" not in controllo_pulito(vault)


# --- T10 · Nuova versione e hub ---------------------------------------------------------

def test_t10_nuova_versione_e_tema_da_rileggere(vault):
    """Una versione nuova di doc-alfa (ID nuovo, stessa cartella, data più recente): la nota la
    prende come current, l'avviso «da rileggere» compare sul tema che la cita e sparisce quando
    il tema viene aggiornato (la riga «Da rileggere» nel tema la scrive l'agente)."""
    assert "da rileggere" not in controllo_pulito(vault)
    url = f"{SITO}/Delivery/Doc_Alfa_v3.pdf"
    elenco = [FILE_DOC_ALFA, file_(url, "item-2", lm="2026-10-25T12:00:00Z")]
    piano = riconcilia(vault, elenco, "--fonte", "sharepoint", "--libreria", "Delivery")
    (v,) = voci(piano)
    assert (v["tipo"], v["nota"], v["diventa_current"], v["rileggi"], v["chiave_corrente"]) == (
        "nuova_voce", DOC_ALFA, True, True, "item-1")
    riconcilia(vault, elenco, "--fonte", "sharepoint", "--libreria", "Delivery", "--applica")
    d = fm(vault, DOC_ALFA)
    assert d["current"]["name"] == "Doc_Alfa_v3.pdf" and d["current"]["web_url"] == url
    assert [x["name"] for x in d["versions"]] == ["Doc_Alfa_v3.pdf", "Doc_Alfa_v2.pdf"]
    assert leggi_stato(vault, "sharepoint")["items"]["drv/item-2"]["note"] == DOC_ALFA
    rapporto = controllo_pulito(vault)
    assert any("tema-uno" in r and "[[doc-alfa]]" in r and "da rileggere" in r for r in rapporto.splitlines())
    oggi = d["ingested_at"].date().isoformat()
    assert esegui("aggiorna-nota.py", vault, "topics/tema-uno.md", "--campo", f"updated={oggi}").returncode == 0
    assert not any("tema-uno" in r and "da rileggere" in r for r in controllo_pulito(vault).splitlines())


# --- Regola dell'identità: casi delicati ------------------------------------------------

def test_candidati_ambigui_non_si_sceglie(vault):
    """Due note diverse con la stessa famiglia calcolata (`00-leggimi`) in cartelle diverse: un
    file nuovo con quella famiglia in una terza cartella non si lega a nessuna delle due."""
    fonte(vault, "sources/sharepoint/delivery/cliente-a/cliente-a-00-leggimi.md",
          f"{SITO}/Delivery/Cliente A/00_Leggimi.md", "LA", family="cliente-a-00-leggimi")
    fonte(vault, "sources/sharepoint/delivery/cliente-b/cliente-b-00-leggimi.md",
          f"{SITO}/Delivery/Cliente B/00 Leggimi.md", "LB", family="cliente-b-00-leggimi")
    presenti = [FILE_DOC_ALFA, file_(f"{SITO}/Delivery/Cliente A/00_Leggimi.md", "LA"),
                file_(f"{SITO}/Delivery/Cliente B/00 Leggimi.md", "LB")]
    piano = riconcilia(vault, presenti + [file_(f"{SITO}/Delivery/Cliente C/00-Leggimi.md", "LC",
                                                lm="2026-09-01T00:00:00Z")], "--fonte", "sharepoint")
    (v,) = voci(piano)
    assert v["tipo"] == "recupera" and v["nota"] is None
    assert v["candidati_ambigui"] == ["sources/sharepoint/delivery/cliente-a/cliente-a-00-leggimi.md",
                                      "sources/sharepoint/delivery/cliente-b/cliente-b-00-leggimi.md"]
    # lo stesso nome di una sola delle due: è quella (copia)
    piano = riconcilia(vault, presenti + [file_(f"{SITO}/Delivery/Cliente C/00_Leggimi.md", "LC")],
                       "--fonte", "sharepoint")
    (v,) = voci(piano)
    assert (v["tipo"], v["nota"], v["diventa_current"]) == (
        "copia", "sources/sharepoint/delivery/cliente-a/cliente-a-00-leggimi.md", False)
    # un solo candidato, per sola famiglia, in un'altra cartella: è quello
    piano_lavori = "sources/sharepoint/delivery/cliente-a/piano-lavori.md"
    fonte(vault, piano_lavori, f"{SITO}/Delivery/Cliente A/Piano_Lavori_v1.docx", "PA")
    piano = riconcilia(vault, presenti + [file_(f"{SITO}/Delivery/Cliente A/Piano_Lavori_v1.docx", "PA"),
                                          file_(f"{SITO}/Delivery/Cliente C/Piano Lavori v2.docx", "PC")],
                       "--fonte", "sharepoint")
    (v,) = voci(piano)
    assert (v["tipo"], v["nota"], v["motivo"]) == ("copia", piano_lavori, "famiglia")


def test_assente_per_due_riconciliazioni_poi_rimossa_e_ripristinata(vault, tmp_path):
    rel = "sources/sharepoint/delivery/verbale-chiuso.md"
    url = f"{SITO}/Delivery/Verbale_Chiuso.pdf"
    fonte(vault, rel, url, "V1")
    elenco = [FILE_DOC_ALFA]
    # prima riconciliazione: in attesa
    primo = riconcilia(vault, elenco, "--fonte", "sharepoint", "--libreria", "Delivery", "--applica")
    (v,) = voci(primo)
    assert (v["tipo"], v["chiave"], v["assente_attuale"], v["assente_dopo"], v["esito"]) == (
        "in_attesa", f"{DRV}/V1", 0, 1, "fatto")
    assert fm(vault, rel)["status"] == "active"
    # seconda: rimossa (un elenco incompleto non rimuove alla prima)
    secondo = riconcilia(vault, elenco, "--fonte", "sharepoint", "--libreria", "Delivery", "--applica")
    (v,) = voci(secondo)
    assert (v["tipo"], v["assente_attuale"], v["assente_dopo"], v["esito"]) == ("rimuovi", 1, 2, "fatto")
    assert fm(vault, rel)["status"] == "removed"
    assert leggi_stato(vault, "sharepoint")["items"][f"{DRV}/V1"] == {"assente": 2, "last_modified": LM, "note": rel}
    controllo_pulito(vault)
    # terza: una nota rimossa che resta assente non produce nulla
    assert voci(riconcilia(vault, elenco, "--fonte", "sharepoint", "--libreria", "Delivery")) == []
    # il file ricompare: la nota torna attiva e il conteggio si azzera
    di_nuovo = riconcilia(vault, elenco + [file_(url, "V1")], "--fonte", "sharepoint", "--applica")
    assert [(v["tipo"], v.get("ripristina"), v["esito"]) for v in di_nuovo["voci"]] == [
        ("sposta", True, "fatto"), ("azzera", None, "fatto")]
    assert fm(vault, rel)["status"] == "active"
    assert "assente" not in leggi_stato(vault, "sharepoint")["items"][f"{DRV}/V1"]
    controllo_pulito(vault)


def test_assente_cambiato_da_un_altro_giro_e_errore(vault, tmp_path):
    rel = "sources/sharepoint/delivery/verbale-chiuso.md"
    fonte(vault, rel, f"{SITO}/Delivery/Verbale_Chiuso.pdf", "V1")
    piano_file = tmp_path / "piano.json"
    riconcilia(vault, [FILE_DOC_ALFA], "--fonte", "sharepoint", "--piano", piano_file)
    # un altro giro conta l'assenza due volte nel frattempo
    for _ in range(2):
        assert esegui("stato.py", vault, "set-assente", "sharepoint", f"{DRV}/V1").returncode == 0
    risultato = riconcilia(vault, [FILE_DOC_ALFA], "--fonte", "sharepoint", "--applica", "--piano", piano_file,
                           codice=1)
    assert risultato["voci"][0]["esito"] == "errore" and "rifai il piano" in risultato["voci"][0]["messaggio"]
    assert fm(vault, rel)["status"] == "active"


def test_versione_vecchia_e_versione_nuova_nella_stessa_cartella(vault):
    rel = "sources/sharepoint/delivery/offerta-pilota.md"
    fonte(vault, rel, f"{SITO}/Delivery/Offerta_Pilota_v2.docx", "O2", lm="2026-10-10T10:00:00Z")
    v2 = file_(f"{SITO}/Delivery/Offerta_Pilota_v2.docx", "O2", lm="2026-10-10T10:00:00Z")
    v1 = file_(f"{SITO}/Delivery/Offerta_Pilota_v1.docx", "O1", lm="2026-10-01T10:00:00Z")
    v3 = file_(f"{SITO}/Delivery/Offerta_Pilota_v3.docx", "O3", lm="2026-10-20T10:00:00Z")
    piano = riconcilia(vault, [FILE_DOC_ALFA, v1, v2, v3], "--fonte", "sharepoint")
    assert [(v["chiave"], v["diventa_current"], v["rileggi"]) for v in voci(piano)] == [
        (f"{DRV}/O3", True, True), (f"{DRV}/O1", False, False)]
    riconcilia(vault, [FILE_DOC_ALFA, v1, v2, v3], "--fonte", "sharepoint", "--applica")
    d = fm(vault, rel)
    assert d["current"]["item_id"] == "O3" and d["current"]["name"] == "Offerta_Pilota_v3.docx"
    assert [x["item_id"] for x in d["versions"]] == ["O3", "O2", "O1"]
    items = leggi_stato(vault, "sharepoint")["items"]
    assert {items[f"{DRV}/{i}"]["note"] for i in ("O1", "O2", "O3")} == {rel}
    rapporto = controllo_pulito(vault)
    assert not any("offerta-pilota" in r and "senza versione o copia" in r for r in rapporto.splitlines())
    assert riconcilia(vault, [FILE_DOC_ALFA, v1, v2, v3], "--fonte", "sharepoint")["riepilogo"] == {"ok": 4}


def test_spostata_con_id_nuovo_in_un_altra_cartella(vault):
    """Copiata altrove e cancellata (la current manca dall'elenco che la copriva): la nota segue
    il file nuovo e la vecchia current torna in `versions`; nessuna assenza."""
    rel = "sources/sharepoint/delivery/relazione-q3.md"
    fonte(vault, rel, f"{SITO}/Delivery/Relazione_Q3.pdf", "R1")
    elenco = [FILE_DOC_ALFA, file_(f"{SITO}/Delivery/Archivio/Relazione_Q3.pdf", "R2")]
    piano = riconcilia(vault, elenco, "--fonte", "sharepoint", "--libreria", "Delivery")
    (v,) = voci(piano)
    assert (v["tipo"], v["diventa_current"], v["vecchia_current"]["dove"]) == ("copia", True, "versions")
    riconcilia(vault, elenco, "--fonte", "sharepoint", "--libreria", "Delivery", "--applica")
    dopo = "sources/sharepoint/delivery/archivio/relazione-q3.md"
    d = fm(vault, dopo)
    assert d["current"]["item_id"] == "R2" and d["also_at"] == []
    assert [x["item_id"] for x in d["versions"]] == ["R2", "R1"]
    items = leggi_stato(vault, "sharepoint")["items"]
    assert items[f"{DRV}/R1"]["note"] == items[f"{DRV}/R2"]["note"] == dopo
    rapporto = controllo_pulito(vault)
    assert not any("relazione-q3" in r and "senza versione o copia" in r for r in rapporto.splitlines())
    assert riconcilia(vault, elenco, "--fonte", "sharepoint", "--libreria", "Delivery")["riepilogo"] == {"ok": 2}


def test_copia_spostata_aggiorna_also_at(vault):
    rel = "sources/sharepoint/salesmarketing/listino-partner.md"
    interna = f"{SITO}/SalesMarketing/Listino_Partner_v2.pdf"
    fonte(vault, rel, interna, "L1")
    assert esegui("aggiorna-nota.py", vault, rel, "--also-at", f"web_url={SITO}/Delivery/Listino_Partner_v2.pdf",
                  "item_id=L2").returncode == 0
    assert esegui("stato.py", vault, "collega", "sharepoint", f"{DRV}/L2", "--stessa-nota-di", f"{DRV}/L1",
                  "--istante", LM).returncode == 0
    nuova = f"{SITO}/Delivery/Listini/Listino_Partner_v2.pdf"
    elenco = [FILE_DOC_ALFA, file_(interna, "L1"), file_(nuova, "L2")]
    (v,) = voci(riconcilia(vault, elenco, "--fonte", "sharepoint"))
    assert (v["tipo"], v["aggiorna"], v["web_url_prima"]) == ("copia", True, f"{SITO}/Delivery/Listino_Partner_v2.pdf")
    riconcilia(vault, elenco, "--fonte", "sharepoint", "--applica")
    assert fm(vault, rel)["also_at"] == [{"web_url": nuova, "item_id": "L2"}]
    controllo_pulito(vault)
    assert riconcilia(vault, elenco, "--fonte", "sharepoint")["riepilogo"] == {"ok": 3}


def test_versione_vecchia_ancora_presente_non_produce_nulla(vault):
    rel = "sources/sharepoint/delivery/offerta-pilota.md"
    fonte(vault, rel, f"{SITO}/Delivery/Offerta_Pilota_v1.docx", "O1", lm="2026-10-01T10:00:00Z")
    nuova = file_(f"{SITO}/Delivery/Offerta_Pilota_v2.docx", "O2", lm="2026-10-10T10:00:00Z")
    elenco = [FILE_DOC_ALFA, file_(f"{SITO}/Delivery/Offerta_Pilota_v1.docx", "O1", lm="2026-10-01T10:00:00Z"), nuova]
    riconcilia(vault, elenco, "--fonte", "sharepoint", "--applica")
    assert fm(vault, rel)["current"]["item_id"] == "O2"
    assert riconcilia(vault, elenco, "--fonte", "sharepoint")["riepilogo"] == {"ok": 3}


def test_onedrive(vault):
    rel = "sources/onedrive/clienti/appunti-riunione.md"
    fonte(vault, rel, f"{ONEDRIVE}/Clienti/Appunti_Riunione.docx", "OD1", drive="drvO")
    nuovo = f"{ONEDRIVE}/Clienti/Archivio/Appunti_Riunione.docx"
    elenco = [file_(nuovo, "OD1", drive="drvO")]
    piano = riconcilia(vault, elenco, "--fonte", "onedrive", "--libreria", "ignorata")
    assert piano["libreria"] is None
    (v,) = voci(piano)
    assert (v["tipo"], v["cartella_nuova"]) == ("sposta", "sources/onedrive/clienti/archivio")
    riconcilia(vault, elenco, "--fonte", "onedrive", "--applica")
    assert leggi_stato(vault, "onedrive")["items"]["drvO/OD1"]["note"] == "sources/onedrive/clienti/archivio/appunti-riunione.md"
    controllo_pulito(vault)
