"""Test di scarta.py (SPEC 5.3, 6.3 passo 2): filtri di scarto della posta da `vault.yaml`."""

import json

import pytest

from conftest import VAULT_YAML, esegui

import config  # noqa: E402 (sys.path da conftest.py)
from scarta import valuta  # noqa: E402

# Il blocco `fonti.outlook` del mini-vault ha solo `mittenti_scartati: [no-reply, noreply]`:
# i test con gli elenchi pieni sostituiscono il blocco con questo
OUTLOOK_MINI = "  outlook:\n    mittenti_scartati: [no-reply, noreply]\n"
OUTLOOK_PIENO = """  outlook:
    finestra_ore: 3
    mittenti_scartati: [no-reply, noreply, donotreply, notifications, notification, mailer-daemon]
    domini_scartati: [fornitore.it, "@marketing.example"]
    oggetti_scartati: [newsletter, "webinar gratuito"]
"""


def yaml_pieno():
    assert OUTLOOK_MINI in VAULT_YAML
    return VAULT_YAML.replace(OUTLOOK_MINI, OUTLOOK_PIENO)


@pytest.fixture
def pieno():
    return config.da_testo(yaml_pieno())


@pytest.mark.parametrize("mittente, oggetto, regola, termine", [
    ("no-reply@x.it", None, "mittenti_scartati", "no-reply"),
    ("noreply123@x.it", None, "mittenti_scartati", "noreply"),
    ("teams-notifications@x.it", None, "mittenti_scartati", "notifications"),
    ("azure_notification@x.it", None, "mittenti_scartati", "notification"),
    ("MAILER-DAEMON@x.it", None, "mittenti_scartati", "mailer-daemon"),
    ("teams.no-reply@x.it", None, "mittenti_scartati", "no-reply"),      # termine con separatore, a metà
    ("DoNotReply@x.it", None, "mittenti_scartati", "donotreply"),
    ("mario@fornitore.it", None, "domini_scartati", "fornitore.it"),
    ("mario@news.fornitore.it", None, "domini_scartati", "fornitore.it"),  # sottodominio
    ("eventi@marketing.example", None, "domini_scartati", "@marketing.example"),
    ("mario@x.it", "Newsletter di ottobre", "oggetti_scartati", "newsletter"),
    ("mario@x.it", "Iscriviti al WEBINAR GRATUITO", "oggetti_scartati", "webinar gratuito"),
    # vince la prima regola: il mittente prima del dominio e dell'oggetto
    ("no-reply@fornitore.it", "newsletter", "mittenti_scartati", "no-reply"),
    ("mario@fornitore.it", "newsletter", "domini_scartati", "fornitore.it"),
])
def test_scarta(pieno, mittente, oggetto, regola, termine):
    r = valuta(mittente, oggetto, pieno)
    assert r["scarta"] is True, r
    assert (r["regola"], r["termine"]) == (regola, termine)
    assert r["motivo"].endswith(f"`{termine}` (fonti.outlook.{regola})")


@pytest.mark.parametrize("mittente, oggetto", [
    ("lorenzo@x.it", None),
    ("lorenzo@x.it", "Offerta per il progetto"),
    ("reply@x.it", None),                    # `reply` da solo non è `no-reply`
    ("notifiche@x.it", None),                # non inizia con `notification`
    ("anno@x.it", "Re: preventivo"),         # `no` dentro una parola non conta
    ("mario@altrofornitore.it", None),       # dominio che finisce con il termine ma non è un sottodominio
    ("mario@fornitore.it.example", None),
    ("mario@x.it", "News di ottobre"),
])
def test_tieni(pieno, mittente, oggetto):
    r = valuta(mittente, oggetto, pieno)
    assert r == {"scarta": False, "regola": None, "termine": None, "motivo": None,
                 "mittente": mittente.lower(), "oggetto": oggetto}


def test_nome_visualizzato_e_maiuscole(pieno):
    r = valuta("Mario Rossi <Mario.Rossi@Fornitore.IT>", "Offerta", pieno)
    assert r["mittente"] == "mario.rossi@fornitore.it" and r["regola"] == "domini_scartati"
    r = valuta('"Microsoft Teams" <no-reply@teams.mail.microsoft>', None, pieno)
    assert r["mittente"] == "no-reply@teams.mail.microsoft" and r["termine"] == "no-reply"
    assert r["motivo"] == "mittente `no-reply` (fonti.outlook.mittenti_scartati)"


def test_elenchi_dalla_configurazione_del_vault():
    """Senza `c` vale la configurazione del vault (qui il mini-vault: solo no-reply e noreply)."""
    assert valuta("noreply@x.it")["scarta"] is True
    assert valuta("notifications@x.it")["scarta"] is False
    assert valuta("mario@fornitore.it", "newsletter")["scarta"] is False   # liste vuote di default


@pytest.mark.parametrize("mittente", ["mario", "", "Mario Rossi", "@x.it", "mario@", "Mario <mario>"])
def test_mittente_non_valido(mittente):
    with pytest.raises(ValueError):
        valuta(mittente)


# --- Riga di comando ----------------------------------------------------------------------

def scarta(root, *args):
    return esegui("scarta.py", root, *args)


def test_riga_di_comando_testo_e_codici(vault):
    res = scarta(vault, "--mittente", "no-reply@x.it")
    assert res.returncode == 1
    assert res.stdout == "scarta · mittente `no-reply` (fonti.outlook.mittenti_scartati)\n"
    res = scarta(vault, "--mittente", "Mario Rossi <mario@x.it>", "--oggetto", "Offerta")
    assert res.returncode == 0 and res.stdout == "tieni\n"


def test_riga_di_comando_json(vault):
    res = scarta(vault, "--mittente", "Mario Rossi <mario@x.it>", "--oggetto", "Offerta", "--json")
    assert res.returncode == 0
    assert json.loads(res.stdout) == {"scarta": False, "regola": None, "termine": None, "motivo": None,
                                      "mittente": "mario@x.it", "oggetto": "Offerta"}
    res = scarta(vault, "--mittente", "noreply@x.it", "--json")
    assert res.returncode == 1
    out = json.loads(res.stdout)
    assert out["scarta"] is True and out["regola"] == "mittenti_scartati" and out["termine"] == "noreply"
    assert out["oggetto"] is None


def test_riga_di_comando_con_gli_elenchi_pieni(vault):
    (vault / "vault.yaml").write_text(yaml_pieno(), encoding="utf-8")
    res = scarta(vault, "--mittente", "info@news.fornitore.it", "--json")
    assert res.returncode == 1 and json.loads(res.stdout)["regola"] == "domini_scartati"
    res = scarta(vault, "--mittente", "mario@x.it", "--oggetto", "La NEWSLETTER")
    assert res.returncode == 1 and res.stdout == "scarta · oggetto con `newsletter` (fonti.outlook.oggetti_scartati)\n"
    assert scarta(vault, "--mittente", "teams-notifications@x.it").returncode == 1
    assert scarta(vault, "--mittente", "lorenzo@x.it", "--oggetto", "Offerta").returncode == 0


@pytest.mark.parametrize("args", [
    ("--mittente", "mario"),            # senza @
    ("--mittente", "Mario Rossi"),
    (),                                 # --mittente obbligatorio
    ("--oggetto", "Offerta"),
    ("--mittente", "a@x.it", "--boh"),
])
def test_argomenti_non_validi(vault, args):
    res = scarta(vault, *args)
    assert res.returncode == 2 and res.stdout == ""


def test_configurazione_non_valida(vault):
    p = vault / "vault.yaml"
    p.write_text(p.read_text(encoding="utf-8").replace(OUTLOOK_MINI, OUTLOOK_MINI + "    finestra_ore: 0\n"),
                 encoding="utf-8")
    res = scarta(vault, "--mittente", "mario@x.it")
    assert res.returncode == 2 and "`fonti.outlook.finestra_ore` deve essere un intero positivo" in res.stderr


def test_help(vault):
    res = scarta(vault, "--help")
    assert res.returncode == 0 and "mittenti_scartati" in res.stdout and "domini_scartati" in res.stdout
