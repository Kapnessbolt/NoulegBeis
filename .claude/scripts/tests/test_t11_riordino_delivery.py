"""T11 dell'audit del 31/10 (`proposals/2026-10-31-audit-ingestion.md` §5, criterio dello step 17b di
SPEC 13.1) sul mini-vault di conftest.py, senza connettore: una cartella di prova in Delivery con 3
note viene spostata e rinominata (stessi folderId, stessi itemId dei file, percorsi nuovi). Il test
percorre la catena come la farebbero i task:

- `ingest-sharepoint` (SPEC 6.2 passo 7, `.claude/routines/ingest-sharepoint.md`): fotografia delle
  cartelle di Delivery con `stato.py set-cartelle` fino a `config.profondita("Delivery")`, prima e
  dopo il riordino → `riordino: true`, Delivery in `riconciliazione_dovuta`, riga d'esito nel digest;
- `digest` (`.claude/routines/digest.md`): `plancia.py --anomalie` e la riga del giro del mattino;
- `reconcile-ridotta` (SPEC 6.4 ridotta, `.claude/routines/reconcile-ridotta.md`): elenco della
  libreria con i `webUrl` nuovi → `riconcilia.py --piano` (3 `sposta`) → `--applica` → note nella
  cartella di `perimetro.py`, stato con i percorsi nuovi → `stato.py set-riconciliata` → riga
  d'esito nel digest, letta da `plancia.py` come `ok`; `controlla-vault.py` a 0 errori.

Il mini-vault di conftest.py non ha `fonti.rilevatore` né il task `reconcile-ridotta`: il fixture
`vault_t11` li aggiunge come nel `vault.yaml` reale (Delivery fotografata a 4 livelli, il task alle
09:10, la riga nella tabella di SPEC 7), così `plancia.py` confronta la riga del reconcile con
l'orario atteso.
"""

import datetime as dt
import json
import re
import sys
from urllib.parse import quote, unquote

import pytest
import yaml

from conftest import SCRIPTS, SPEC_MD, TENANT_SP, VAULT_YAML, esegui, git, leggi_stato, scrivi

sys.path.insert(0, str(SCRIPTS))
import config  # noqa: E402

SITO = f"{TENANT_SP}/sites/internal"
DRV = "b!delivery-t11"          # driveId della libreria Delivery
LM = "2026-10-12T08:30:00Z"     # lastModified dei file: il riordino non lo cambia
# doc-alfa di conftest.py sta nella radice di Delivery con la chiave `item-1`: l'elenco completo
# della libreria lo contiene, altrimenti il piano lo segnerebbe `in_attesa`
FILE_DOC_ALFA = {"chiave": "item-1", "webUrl": f"{SITO}/Delivery/Doc_Alfa_v2.pdf", "name": "Doc_Alfa_v2.pdf",
                 "lastModifiedDateTime": "2026-10-01T10:00:00Z"}

PROVA_PRIMA = "Customers/01 Velo-CE/Cartella di prova"
PROVA_DOPO = "Customers/99 Archivio/Prova T11 riordinata"
# Cartelle di Delivery fino a 4 livelli: la cartella di prova e la sua sottocartella cambiano
# percorso con lo stesso folderId (spostata sotto un'altra cartella e rinominata)
FOTO_A = {
    "fold-customers": "Customers",
    "fold-velo": "Customers/01 Velo-CE",
    "fold-archivio": "Customers/99 Archivio",
    "fold-prova": PROVA_PRIMA,
    "fold-verbali": f"{PROVA_PRIMA}/Verbali",
}
FOTO_B = {**FOTO_A, "fold-prova": PROVA_DOPO, "fold-verbali": f"{PROVA_DOPO}/Verbali"}
# I 3 file della cartella di prova: itemId → percorso relativo alla cartella di prova
FILE_PROVA = {
    "T11-PIANO": "Piano_Lavori_v1.docx",
    "T11-STIMA": "Stima_Costi.xlsx",
    "T11-VERBALE": "Verbali/Verbale_Kickoff.pdf",
}

RILEVATORE = """  rilevatore:
    profondita:
      SalesMarketing: 2
      Delivery: 4
      Shared Documents: 2
    soglia_id_nuovi: 5
"""
TASK_RIDOTTA = """  - nome: reconcile-ridotta
    orari: ["09:10"]
    giorni: ogni-giorno
    modello: sonnet
    connettori: [microsoft365]
"""
VAULT_YAML_T11 = (VAULT_YAML
                  .replace("  tipi_processati:", RILEVATORE + "  tipi_processati:", 1)
                  .replace("  - nome: curator\n", TASK_RIDOTTA + "  - nome: curator\n", 1))
SPEC_MD_T11 = SPEC_MD.replace(
    "| `cockpit` |",
    "| `reconcile-ridotta` | Ogni giorno alle 09:10 | Microsoft 365 | Sonnet | 6.4, ridotta |\n| `cockpit` |", 1)


# --- Aiuti ------------------------------------------------------------------------------

def url_di(percorso):
    """webUrl di un file di Delivery come lo restituisce il connettore (spazi in %20)."""
    return f"{SITO}/Delivery/{quote(percorso)}"


def istante_locale(giorno, hhmm):
    """Istante UTC (formato dello stato) di un'ora del giorno nel fuso del vault."""
    h, m = map(int, hhmm.split(":"))
    t = dt.datetime.combine(giorno, dt.time(h, m), tzinfo=config.fuso())
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ok(res):
    assert res.returncode == 0, res.stdout + res.stderr
    return res


def json_di(res):
    return json.loads(ok(res).stdout)


def perimetro(root, web_url):
    return json_di(esegui("perimetro.py", root, web_url, "--json"))


def fm(root, rel):
    return yaml.safe_load((root / rel).read_text(encoding="utf-8").split("---\n", 2)[1])


def fotografia(root, tmp_path, foto, istante):
    """Il passo «cartelle» del rilevatore: elenco nello scratchpad e `stato.py set-cartelle`."""
    p = tmp_path / "cartelle-delivery.json"
    p.write_text(json.dumps(foto, ensure_ascii=False), encoding="utf-8")
    return json_di(esegui("stato.py", root, "set-cartelle", "sharepoint", DRV, "--libreria", "Delivery",
                          "--profondita", config.profondita("Delivery"), "--istante", istante, "--elenco", p))


def elenco_libreria(cartella_prova):
    """L'elenco di Delivery che l'agente scrive dal `read_resource` ricorsivo (SPEC 6.4 passo 1)."""
    return [FILE_DOC_ALFA] + [
        {"id": item, "driveId": DRV, "webUrl": url_di(f"{cartella_prova}/{rel}"),
         "name": rel.rsplit("/", 1)[-1], "lastModifiedDateTime": LM}
        for item, rel in FILE_PROVA.items()]


def riconcilia(root, tmp_path, *args, codice=0):
    p = tmp_path / "elenco-delivery.json"
    p.write_text(json.dumps(elenco_libreria(PROVA_DOPO), ensure_ascii=False), encoding="utf-8")
    res = esegui("riconcilia.py", root, "--elenco", p, "--fonte", "sharepoint", "--libreria", "Delivery",
                 "--piano", tmp_path / "piano-delivery.json", *args, "--json")
    assert res.returncode == codice, res.stdout + res.stderr
    return json.loads(res.stdout)


def digest(giorno, decisioni, righe_esito):
    return (f"---\ntype: journal\ndate: {giorno}\n---\n\n# Digest {giorno}\n\n## Novità ingerite\n\n-\n\n"
            "## Attività in scadenza\n\n-\n\n## Decisioni\n\n" + "".join(f"{d}\n" for d in decisioni)
            + "\n## Scartate\n\n-\n\n## Controllo del vault\n\n-\n\n## Esito dei task\n\n"
            "| Task | Esito |\n|---|---|\n" + "".join(f"{r}\n" for r in righe_esito))


def aggiungi_esito(root, giorno, riga):
    """Riga nuova in coda alla tabella di `## Esito dei task` (l'ultima sezione del digest)."""
    p = root / "journal" / f"{giorno}.md"
    p.write_text(p.read_text(encoding="utf-8").rstrip("\n") + f"\n{riga}\n", encoding="utf-8")


def anomalie(root, giorno, ora):
    return json_di(esegui("plancia.py", root, "--anomalie", "--json", "--giorno", giorno, "--ora", ora))


def controllo_pulito(root):
    res = esegui("controlla-vault.py", root)
    assert res.returncode == 0, res.stdout + res.stderr
    assert " 0 errori " in res.stdout, res.stdout
    return res.stdout


def wikilink_rotti(root):
    """Wikilink delle note del vault che non puntano a nessuna nota (oltre al controllo del vault)."""
    note = [p for p in root.rglob("*.md")
            if not {".git", "_templates", ".claude"} & set(p.relative_to(root).parts)]
    slug = {p.stem for p in note}
    rotti = []
    for p in note:
        for link in re.findall(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]", p.read_text(encoding="utf-8")):
            if link.strip() not in slug:
                rotti.append((p.relative_to(root).as_posix(), link))
    return rotti


def commit(root, messaggio):
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", messaggio)


@pytest.fixture
def vault_t11(vault, configurazione_di_prova):
    """Il mini-vault con il rilevatore e il task `reconcile-ridotta` del vault reale, e la cartella
    di prova in Delivery: 3 note fonte create con nuova-nota.py nella cartella di perimetro.py,
    registrate nello stato con `stato.py set-item`, una citata nel log del progetto alfa."""
    scrivi(vault, "vault.yaml", VAULT_YAML_T11)
    scrivi(vault, "SPEC.md", SPEC_MD_T11)
    config.imposta(config.da_testo(VAULT_YAML_T11))
    assert config.profondita("Delivery") == 4
    note = {}
    for item, rel in FILE_PROVA.items():
        web_url = url_di(f"{PROVA_PRIMA}/{rel}")
        cartella = perimetro(vault, web_url)["cartella_nota"]
        nome = rel.rsplit("/", 1)[-1]
        famiglia = json_di(esegui("famiglia.py", vault, nome, "--json"))["famiglia"]
        nota = f"{cartella}/{famiglia}.md"
        campi = [f"current.item_id={json.dumps(item)}", f"current.uri={json.dumps(f'file:///{DRV}/{item}')}",
                 f"current.web_url={json.dumps(web_url)}", f"current.name={json.dumps(nome)}",
                 f"current.last_modified={LM}", 'projects=["[[alfa]]"]']
        ok(esegui("nuova-nota.py", vault, "source-doc", nota, "--titolo", nome,
                  *[x for c in campi for x in ("--campo", c)]))
        ok(esegui("stato.py", vault, "set-item", "sharepoint", f"{DRV}/{item}", "--istante", LM, "--note", nota))
        note[item] = nota
    log = vault / "projects/alfa/alfa-log.md"
    slug_piano = note["T11-PIANO"].rsplit("/", 1)[-1][:-3]
    log.write_text(log.read_text(encoding="utf-8").replace(
        "# Log · Progetto Alfa\n\n", f"# Log · Progetto Alfa\n\n- 2026-10-12 · Piano dei lavori della cartella "
                                     f"di prova · [[{slug_piano}]]\n", 1), encoding="utf-8")
    controllo_pulito(vault)
    commit(vault, "ingest(sharepoint): 3 note nuove (cartella di prova)")
    return vault, note


# --- T11 · dal giro del mattino alla riconciliazione ridotta -----------------------------

def test_t11_riordino_rilevato_e_riconciliato(vault_t11, tmp_path):
    root, note = vault_t11
    oggi = config.oggi()
    ieri = oggi - dt.timedelta(days=1)
    giorno = oggi.isoformat()

    # 1. Giro di ieri: fotografia A (la prima non fa scattare niente)
    a = fotografia(root, tmp_path, FOTO_A, istante_locale(ieri, "06:52"))
    assert (a["prima"], a["riordino"], a["cartelle"]) == (True, False, 5)
    assert a["riconciliazione_dovuta"] is None
    assert leggi_stato(root, "sharepoint")["cartelle"][DRV]["profondita"] == 4

    # 2. Leonardo sposta e rinomina la cartella di prova; giro di oggi alle 06:52: fotografia B
    rilevato = istante_locale(oggi, "06:52")
    b = fotografia(root, tmp_path, FOTO_B, rilevato)
    assert (b["prima"], b["riordino"]) == (False, True)
    assert (b["nuove"], b["sparite"]) == ([], [])
    assert b["spostate"] == [{"da": PROVA_PRIMA, "a": PROVA_DOPO},
                             {"da": f"{PROVA_PRIMA}/Verbali", "a": f"{PROVA_DOPO}/Verbali"}]
    assert b["riconciliazione_dovuta"] == rilevato
    assert leggi_stato(root, "sharepoint")["riconciliazione_dovuta"] == {"Delivery": rilevato}
    res = esegui("stato.py", root, "riconciliazione-dovuta", "sharepoint")
    assert res.returncode == 0 and res.stdout.strip() == f"Riconciliazione dovuta: Delivery dal {giorno}"
    assert esegui("stato.py", root, "riconciliazione-dovuta", "onedrive").returncode == 1
    # il delta non vede il riordino: le note sono ancora nella cartella vecchia
    assert all((root / n).is_file() for n in note.values())

    # 3. Riga d'esito dell'ingestor e righe di `## Decisioni` (ingestor §4 passo 5)
    scrivi(root, f"journal/{giorno}.md", digest(
        giorno,
        ["- Riordino rilevato in Delivery: cartelle (2 spostate)",
         f"- Riconciliazione dovuta: Delivery dal {giorno}"],
        ["| ingest-sharepoint 06:52 | OK · riordino in Delivery, riconciliazione dovuta |"]))
    controllo_pulito(root)
    commit(root, "ingest(sharepoint): 0 note nuove, 0 aggiornate")

    # 4. Il digest delle 07:45 e la verifica delle 09:00: plancia non elenca una riconciliazione
    # dovuta da meno di DOVUTA_AVVISO_GIORNI (livello `ok` in anomalie.riconciliazioni_dovute):
    # il giorno del rilevamento la vede il digest dalle righe dell'ingestor (passo 3)
    for ora in ("07:45", "09:00"):
        r = anomalie(root, giorno, ora)
        assert r["conteggi"]["riconciliazioni_dovute"] == 0
        assert not [e for e in r["esito_task"] if e["tipo"] == "riconciliazione_dovuta"]
        assert not [e for e in r["esito_task"] if e.get("task") == "ingest-sharepoint"
                    and e.get("giorno") == giorno]
        assert r["conteggi"]["watermark_fermi"] == 0 and r["conteggi"]["stati_illeggibili"] == 0
        # solo la voce `item-1` di conftest.py: le note della cartella di prova non ne aggiungono
        assert r["conteggi"]["note_con_voci_orfane"] == 1

    # 5. reconcile-ridotta delle 09:10: elenco con i webUrl nuovi e piano
    piano = riconcilia(root, tmp_path)
    assert piano["riepilogo"] == {"sposta": 3, "ok": 1}, piano
    assert piano["ignorati"] == []
    assert not [v for v in piano["voci"] if v["tipo"] in ("rimuovi", "recupera", "in_attesa", "in_coda")]
    attese = {}
    for v in piano["voci"]:
        item = v["chiave"].split("/", 1)[1]
        web_url = url_di(f"{PROVA_DOPO}/{FILE_PROVA[item]}")
        cartella = perimetro(root, web_url)["cartella_nota"]
        assert (v["tipo"], v["nota"], v["web_url"]) == ("sposta", note[item], web_url)
        assert v["web_url_prima"] == url_di(f"{PROVA_PRIMA}/{FILE_PROVA[item]}")
        assert (v["cartella_nuova"], v["cambia_cartella"], v["cambia_famiglia"]) == (cartella, True, False)
        attese[item] = (web_url, f"{cartella}/{note[item].rsplit('/', 1)[-1]}")

    # 6. --applica con lo stesso --piano
    risultato = riconcilia(root, tmp_path, "--applica")
    assert risultato["applicato"] is True and risultato["ripreso"] is True
    assert risultato["esiti"] == {"fatto": 3}
    items = leggi_stato(root, "sharepoint")["items"]
    for item, (web_url, dopo) in attese.items():
        assert not (root / note[item]).exists() and (root / dopo).is_file()
        d = fm(root, dopo)
        assert d["current"]["web_url"] == web_url and d["current"]["item_id"] == item
        assert d["current"]["last_modified"] in (LM, dt.datetime(2026, 10, 12, 8, 30, tzinfo=dt.timezone.utc))
        assert d["status"] == "active"
        assert items[f"{DRV}/{item}"] == {"last_modified": LM, "note": dopo}
    assert not (root / "sources/sharepoint/delivery/customers/01-velo-ce").exists()
    assert wikilink_rotti(root) == []
    assert f"[[{attese['T11-PIANO'][1].rsplit('/', 1)[-1][:-3]}]]" in (
        root / "projects/alfa/alfa-log.md").read_text(encoding="utf-8")
    # --applica non chiude il segnale: lo chiude la routine a riconciliazione finita
    assert leggi_stato(root, "sharepoint")["riconciliazione_dovuta"] == {"Delivery": rilevato}
    # rifare il piano sullo stesso elenco non trova più niente
    assert riconcilia(root, tmp_path)["riepilogo"] == {"ok": 4}

    # 7. set-riconciliata e riga d'esito del reconcile-ridotta
    chiusa = json_di(esegui("stato.py", root, "set-riconciliata", "sharepoint", "Delivery", "--json"))
    assert (chiusa["cambiato"], chiusa["dovuta_dal"], chiusa["riconciliazione_dovuta"]) == (True, rilevato, {})
    assert "riconciliazione_dovuta" not in leggi_stato(root, "sharepoint")
    assert esegui("stato.py", root, "riconciliazione-dovuta", "sharepoint").returncode == 1
    n = risultato["riepilogo"]
    aggiungi_esito(root, giorno, f"| reconcile-ridotta 09:12 | OK · Delivery: {n.get('sposta', 0)} note spostate, "
                                 f"{n.get('rimuovi', 0)} rimosse, {n.get('recupera', 0)} recuperate, "
                                 f"{n.get('in_coda', 0)} in coda |")
    testo = (root / "journal" / f"{giorno}.md").read_text(encoding="utf-8")
    assert testo.endswith("| ingest-sharepoint 06:52 | OK · riordino in Delivery, riconciliazione dovuta |\n"
                          "| reconcile-ridotta 09:12 | OK · Delivery: 3 note spostate, 0 rimosse, "
                          "0 recuperate, 0 in coda |\n")

    # 8. controllo del vault, perimetro e famiglia sul mini-vault, commit
    controllo_pulito(root)
    ver = json_di(esegui("perimetro.py", root, "--verifica", "--json"))
    assert (ver["accordo"], ver["disaccordi"]) == (100.0, [])
    # famiglia: l'unico disaccordo è doc-alfa di conftest.py (`family: delivery/doc-alfa`), che
    # tiene il mini-vault sotto la soglia del 95%; le note spostate restano d'accordo
    fam = json.loads(esegui("famiglia.py", root, "--verifica", "--json").stdout)
    assert [d["nota"] for d in fam["disaccordi"]] == ["sources/sharepoint/delivery/doc-alfa.md"]
    assert fam["note"] == 4
    commit(root, "ingest(riconcilia): Delivery, 3 note spostate, 0 rimosse, 0 recuperate")

    # 9. plancia: la riga del reconcile-ridotta è `ok` all'orario atteso, e niente da riconciliare
    out = tmp_path / "plancia"
    ok(esegui("plancia.py", root, out))
    task = {(t["task"], t["atteso"]): t for t in json.loads((out / "task.json").read_text(encoding="utf-8"))
            if t["giorno"] == giorno}
    ridotta = task[("reconcile-ridotta", "09:10")]
    assert (ridotta["eseguito"], ridotta["stato"]) == ("09:12", "ok")
    assert ridotta["esito"] == "OK · Delivery: 3 note spostate, 0 rimosse, 0 recuperate, 0 in coda"
    giro = task[("ingest-sharepoint", "06:50")]
    assert (giro["eseguito"], giro["stato"]) == ("06:52", "ok")
    r = anomalie(root, giorno, "09:30")
    assert r["conteggi"]["riconciliazioni_dovute"] == 0
    assert not [e for e in r["esito_task"] if e.get("giorno") == giorno
                and e.get("task") in ("ingest-sharepoint", "reconcile-ridotta")]


def test_t11_segnale_non_chiuso_resta_e_diventa_anomalia(vault_t11, tmp_path):
    """Senza riconciliazione il segnale resta (una seconda fotografia identica non lo consuma) e il
    digest del giorno dopo lo riceve da plancia come anomalia: oltre 1 giorno è un avviso."""
    root, _ = vault_t11
    oggi = config.oggi()
    domani = (oggi + dt.timedelta(days=1)).isoformat()
    fotografia(root, tmp_path, FOTO_A, istante_locale(oggi - dt.timedelta(days=1), "06:52"))
    rilevato = istante_locale(oggi, "06:52")
    assert fotografia(root, tmp_path, FOTO_B, rilevato)["riordino"] is True
    # il giro di domani rifotografa le stesse cartelle: niente di nuovo, il segnale resta com'era
    c = fotografia(root, tmp_path, FOTO_B, istante_locale(oggi + dt.timedelta(days=1), "06:52"))
    assert (c["riordino"], c["riconciliazione_dovuta"]) == (False, rilevato)
    r = anomalie(root, domani, "07:45")
    (dovuta,) = [e for e in r["esito_task"] if e["tipo"] == "riconciliazione_dovuta"]
    assert (dovuta["libreria"], dovuta["fonte"], dovuta["dal"], dovuta["livello"]) == (
        "Delivery", "sharepoint", rilevato, "avviso")
    assert dovuta["riga"] == (f"- Anomalia · riconciliazione dovuta: Delivery (sharepoint) dal {rilevato} "
                              "(1 giorno) · /ingest riconcilia sharepoint:Delivery")
    assert r["conteggi"]["riconciliazioni_dovute"] == 1
