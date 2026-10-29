"""Test di config.py (SPEC 13.1, step 13) e dei controlli di configurazione di controlla-vault.py."""

import datetime as dt
import json
from zoneinfo import ZoneInfo

import pytest

from conftest import AGENTI, GUID_SERVER, SPEC_MD, TENANT_OD, agente, esegui

import config  # noqa: E402 (sys.path da conftest.py)


def cfg(root, *args):
    return esegui("config.py", root, *args)


def modifica(root, rel, vecchio, nuovo):
    p = root / rel
    testo = p.read_text(encoding="utf-8")
    assert vecchio in testo, f"{vecchio!r} non è in {rel}"
    p.write_text(testo.replace(vecchio, nuovo, 1), encoding="utf-8")


# --- Caricamento e validazione ------------------------------------------------------------

def test_carica_il_vault_yaml_di_prova(vault):
    c = config.carica(vault)
    assert c["vault"]["fuso"] == "Europe/Rome"
    assert config.sezione("relazione", c) == "Relazione con BlueAge"
    assert config.perimetro(c)["onedrive"] == f"{TENANT_OD}/personal/"


@pytest.mark.parametrize("vecchio, nuovo, messaggio", [
    ("fuso: Europe/Rome", "fuso: Europa/Roma", "`vault.fuso` non è un fuso orario IANA valido"),
    ('orari: ["06:50"]', 'orari: ["6:50"]', "`task.ingest-sharepoint.orari` orario non valido"),
    ("giorni: domenica", "giorni: festivi", "`task.reconcile.giorni` non valido"),
    ("connettori: [github]\n    digest", "connettori: [slack]\n    digest", "connettore `slack` non definito"),
    ("  da_fare: Da fare\n", "", "`sezioni.da_fare` deve essere un testo non vuoto"),
    ("tenant: https://example.sharepoint.com", "tenant: example.sharepoint.com", "`fonti.sharepoint.tenant` deve essere un indirizzo https://"),
    ("versione: 1", "versione: 2", "`versione` deve essere 1"),
    ("ingestor: [microsoft365.lettura, github.issue_read]", "ingestor: [microsoft365.scrittura]",
     "`scrittura` non è un gruppo né uno strumento"),
    ("nome_claude: [DailyBoard, DailyBoard2]", "nome_claude: [DailyBoard]", "1 nomi per 2 orari"),
])
def test_errori_di_schema(vault, vecchio, nuovo, messaggio):
    modifica(vault, "vault.yaml", vecchio, nuovo)
    with pytest.raises(config.ConfigErrata) as e:
        config.carica(vault)
    assert any(messaggio in m for m in e.value.errori), e.value.errori
    res = cfg(vault, "verifica")
    assert res.returncode == 1 and messaggio in res.stdout


def test_yaml_rotto_e_file_mancante(vault):
    (vault / "vault.yaml").write_text("vault: [\n", encoding="utf-8")
    res = cfg(vault, "oggi")
    assert res.returncode == 1 and "YAML non valido" in res.stderr
    (vault / "vault.yaml").unlink()
    res = cfg(vault, "oggi")
    assert res.returncode == 1 and "vault.yaml: manca" in res.stderr


@pytest.mark.parametrize("valore, attesi", [
    ("ogni-giorno", set(range(7))),
    ("domenica", {6}),
    ("lunedi", {0}),
    ("lun-ven", {0, 1, 2, 3, 4}),
    ("sab-lun", {5, 6, 0}),
    ("lun, mer", {0, 2}),
    (["martedì", "gio"], {1, 3}),
])
def test_giorni(valore, attesi):
    assert config.giorni(valore) == attesi


# --- Riga di comando ----------------------------------------------------------------------

@pytest.mark.parametrize("fuso", ["Pacific/Kiritimati", "Pacific/Pago_Pago"])
def test_oggi_e_ora_nel_fuso_del_vault(vault, fuso):
    # UTC+14 e UTC-11: la data è sempre diversa tra i due, quindi il fuso conta davvero
    modifica(vault, "vault.yaml", "fuso: Europe/Rome", f"fuso: {fuso}")
    prima = dt.datetime.now(ZoneInfo(fuso))
    oggi, ora = cfg(vault, "oggi"), cfg(vault, "ora")
    dopo = dt.datetime.now(ZoneInfo(fuso))
    assert oggi.returncode == 0 and ora.returncode == 0
    assert oggi.stdout.strip() in {prima.date().isoformat(), dopo.date().isoformat()}
    assert ora.stdout.strip() in {prima.strftime("%H:%M"), dopo.strftime("%H:%M")}


def test_valore(vault):
    assert cfg(vault, "valore", "vault.fuso").stdout == "Europe/Rome\n"
    assert cfg(vault, "valore", "fonti.sharepoint.librerie").stdout == "SalesMarketing\nDelivery\nShared Documents\n"
    assert cfg(vault, "valore", "task.0.nome").stdout == "ingest-sharepoint\n"
    assert json.loads(cfg(vault, "valore", "fonti.github.repository").stdout)[0]["progetto"] == "alfa"
    res = cfg(vault, "valore", "vault.inesistente")
    assert res.returncode == 1 and "Chiave non trovata" in res.stderr


def test_task_di_un_giorno_feriale(vault):
    res = cfg(vault, "task", "2026-10-29")  # giovedì
    assert res.returncode == 0
    assert res.stdout.splitlines() == [
        "06:50 ingest-sharepoint", "07:05 ingest-outlook", "07:20 ingest-github", "07:40 cockpit",
        "07:45 digest", "13:15 ingest-outlook", "13:40 cockpit"]


def test_task_della_domenica(vault):
    righe = cfg(vault, "task", "2026-11-01").stdout.splitlines()
    assert "08:45 reconcile" in righe and righe[-1] == "21:10 curator" and len(righe) == 9
    # --digest: il curator non scrive la riga d'esito nel digest
    solo = json.loads(cfg(vault, "task", "2026-11-01", "--digest", "--json").stdout)
    assert {"ora": "08:45", "task": "reconcile"} in solo and all(t["task"] != "curator" for t in solo)


def test_argomenti_non_validi(vault):
    assert cfg(vault, "task", "29/10/2026").returncode == 2
    assert cfg(vault, "boh").returncode == 2
    assert cfg(vault).returncode == 2
    res = cfg(vault, "--help")
    assert res.returncode == 0 and "verifica" in res.stdout and "applica" in res.stdout


def test_verifica_sul_vault_valido(vault):
    res = cfg(vault, "verifica")
    assert res.returncode == 0, res.stdout


# --- applica ------------------------------------------------------------------------------

def test_applica_riscrive_permessi_e_tools_ed_e_idempotente(vault):
    settings = vault / ".claude/settings.json"
    ingestor = vault / ".claude/agents/ingestor.md"
    # Permessi disallineati: un server in più, uno strumento che manca, un agente senza github
    dati = json.loads(settings.read_text(encoding="utf-8"))
    dati["permissions"]["allow"] = [n for n in dati["permissions"]["allow"] if n != "mcp__github__get_file_contents"]
    dati["permissions"]["allow"].append("mcp__Vecchio-365__read_resource")
    settings.write_text(json.dumps(dati, indent=2) + "\n", encoding="utf-8")
    ingestor.write_text(agente("ingestor", ["Read", "Write", "Bash", "mcp__Vecchio-365__read_resource"]),
                        encoding="utf-8")
    assert cfg(vault, "verifica").returncode == 1

    res = cfg(vault, "applica")
    assert res.returncode == 0 and "settings.json" in res.stdout and "ingestor.md" in res.stdout
    assert cfg(vault, "verifica").returncode == 0
    allow = json.loads(settings.read_text(encoding="utf-8"))["permissions"]["allow"]
    assert "mcp__github__get_file_contents" in allow and "mcp__Vecchio-365__read_resource" not in allow
    assert allow[-1] == "Bash(git pull:*)"  # le voci non mcp restano dove sono
    testo = ingestor.read_text(encoding="utf-8")
    assert "tools: Read, Write, Bash, mcp__Microsoft_365__sharepoint_search," in testo
    assert f"mcp__{GUID_SERVER}__read_resource, mcp__github__issue_read\n" in testo
    assert "outlook_calendar_search" not in testo and "\n\nAgente di prova.\n" in testo

    fotografia = {p: p.read_text(encoding="utf-8") for p in (settings, *vault.glob(".claude/agents/*.md"))}
    res = cfg(vault, "applica")
    assert res.returncode == 0 and "Niente da cambiare" in res.stdout
    assert {p: p.read_text(encoding="utf-8") for p in fotografia} == fotografia


def test_applica_sul_mini_vault_allineato_cambia_solo_l_ordine(vault):
    res = cfg(vault, "applica")
    assert res.returncode == 0
    # Il librarian ha gli strumenti di github in un altro ordine rispetto a vault.yaml
    assert res.stdout.strip() == "Aggiornati: .claude/agents/librarian.md"
    testo = (vault / ".claude/agents/librarian.md").read_text(encoding="utf-8")
    tools = next(r for r in testo.splitlines() if r.startswith("tools:"))
    assert sorted(tools[7:].split(", ")) == sorted(AGENTI["librarian"])


# --- SPEC 7 ↔ vault.yaml in controlla-vault.py --------------------------------------------

def controlla(root):
    return esegui("controlla-vault.py", root)


def test_spec_e_vault_yaml_uguali_nessun_errore(vault):
    res = controlla(vault)
    assert res.returncode == 0, res.stdout
    assert config.problemi_spec(vault, config.carica(vault)) == []


def test_orario_diverso_tra_spec_e_vault_yaml_e_errore(vault):
    modifica(vault, "SPEC.md", "Ogni giorno alle 07:05 e alle 13:15", "Ogni giorno alle 07:05 e alle 13:25")
    res = controlla(vault)
    assert res.returncode == 1
    assert "task `ingest-outlook`: orari diversi (SPEC 7 07:05, 13:25, vault.yaml 07:05, 13:15)" in res.stdout


def test_giorni_diversi_e_task_mancante_sono_errori(vault):
    modifica(vault, "SPEC.md", "| `reconcile` | Domenica alle 08:45", "| `reconcile` | Ogni giorno alle 08:45")
    modifica(vault, "SPEC.md", "| `curator` |", "| `curatore` |")
    res = controlla(vault)
    assert res.returncode == 1
    assert "task `reconcile`: giorni diversi (SPEC 7 ogni giorno, vault.yaml domenica)" in res.stdout
    assert "task `curatore` in SPEC 7 ma non in vault.yaml" in res.stdout
    assert "task `curator` in vault.yaml ma non in SPEC 7" in res.stdout


def test_vault_yaml_non_valido_e_errore(vault):
    modifica(vault, "vault.yaml", "fuso: Europe/Rome", "fuso: Roma")
    res = controlla(vault)
    assert res.returncode == 1
    assert "`vault.yaml` · vault.yaml: `vault.fuso` non è un fuso orario IANA valido" in res.stdout


def test_tabella_della_spec(vault):
    spec = config.task_della_spec(SPEC_MD)
    assert spec["ingest-outlook"] == (frozenset(range(7)), ("07:05", "13:15"))
    assert spec["reconcile"] == (frozenset({6}), ("08:45",))
    assert "/oggi" not in spec and "`/oggi`" not in spec  # la tabella della sezione 8 non conta


# --- Connettori: vault.yaml ↔ settings.json e tools degli agenti --------------------------

def test_permessi_coerenti_nessun_errore(vault):
    assert config.problemi_permessi(vault, config.carica(vault)) == []


def test_server_m365_mancante_nei_permessi_e_errore(vault):
    settings = vault / ".claude/settings.json"
    dati = json.loads(settings.read_text(encoding="utf-8"))
    dati["permissions"]["allow"] = [n for n in dati["permissions"]["allow"] if GUID_SERVER not in n]
    settings.write_text(json.dumps(dati, indent=2), encoding="utf-8")
    res = controlla(vault)
    assert res.returncode == 1
    assert f"`.claude/settings.json` · manca `mcp__{GUID_SERVER}__sharepoint_search`" in res.stdout


def test_strumento_in_lettura_mancante_nei_tools_e_errore(vault):
    modifica(vault, ".claude/agents/ingestor.md", "mcp__Microsoft_365__read_resource, ", "")
    res = controlla(vault)
    assert res.returncode == 1
    assert "`.claude/agents/ingestor.md` · manca `mcp__Microsoft_365__read_resource`" in res.stdout


def test_server_in_piu_e_errore(vault):
    modifica(vault, ".claude/agents/librarian.md", "tools: Read, ", "tools: Read, mcp__Microsoft-365__read_resource, ")
    res = controlla(vault)
    assert res.returncode == 1
    assert "`mcp__Microsoft-365__read_resource`: server non previsto in vault.yaml" in res.stdout


def test_server_nuovo_in_vault_yaml_manca_ovunque(vault):
    modifica(vault, "vault.yaml", f"server: [Microsoft_365, {GUID_SERVER}]",
             f"server: [Microsoft_365, {GUID_SERVER}, Microsoft-365]")
    res = controlla(vault)
    assert res.returncode == 1
    for dove in (".claude/settings.json", ".claude/agents/ingestor.md", ".claude/agents/librarian.md"):
        assert f"`{dove}` · manca `mcp__Microsoft-365__sharepoint_search`" in res.stdout
    assert "curator.md` · manca" not in res.stdout  # il curator non usa connettori
    assert cfg(vault, "applica").returncode == 0
    assert controlla(vault).returncode == 0


def test_strumento_di_scrittura_non_previsto_e_errore(vault):
    modifica(vault, ".claude/agents/curator.md", "tools: Read, ", "tools: Read, mcp__github__create_pull_request, ")
    res = controlla(vault)
    assert res.returncode == 1
    assert "`mcp__github__create_pull_request`: strumento non previsto in vault.yaml" in res.stdout


def test_modificati_vede_gli_errori_di_configurazione(vault):
    modifica(vault, "SPEC.md", "Domenica alle 21:10", "Domenica alle 21:40")
    res = esegui("controlla-vault.py", vault, "--modificati")
    assert res.returncode == 1 and "task `curator`: orari diversi" in res.stdout
