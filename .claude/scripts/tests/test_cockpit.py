"""Test di cockpit.py: la pagina Cockpit generata dai JSON di plancia.py sul mini-vault di conftest.py."""

import json
import re
from html.parser import HTMLParser

import pytest

from conftest import esegui, scrivi

OGGI, ORA = "2026-10-27", "07:40"
REPO = "https://github.com/esempio/vault"

PROGETTI = {
    # Scaduto: un'attività del 20/10, una per oggi, una per venerdì; testo con caratteri da escapare
    "projects/gamma/gamma.md": """---
type: project
status: attivo
role: "consulente"
clients: ["[[cliente-uno]]"]
people: []
updated: 2026-10-26
---

# Progetto Gamma

## Attività

- [ ] Rispondere a <script>alert(1)</script> & co 📅 2026-10-20 ([[doc-alfa]])
- [ ] Chiamare il fornitore 📅 2026-10-27 ([[doc-alfa]])
- [ ] Mandare il verbale 📅 2026-10-30 ([[doc-alfa]])

## Prossimi passi

- Chiudere il <b>contratto</b> & partire ([[doc-alfa]])
""",
    "projects/gamma/gamma-log.md": """---
type: project-log
project: "[[gamma]]"
---

# Log · Progetto Gamma

- 2026-10-26 · Riunione di avvio · [[doc-alfa]]
""",
    # Fermo: ultimo log del 1/9
    "projects/delta/delta.md": """---
type: project
status: attivo
role: "consulente"
clients: []
people: []
updated: 2026-09-01
---

# Progetto Delta

## Attività

- [ ] Riprendere i contatti ([[doc-alfa]])

## Prossimi passi

-
""",
    "projects/delta/delta-log.md": """---
type: project-log
project: "[[delta]]"
---

# Log · Progetto Delta

- 2026-09-01 · Ultima riunione · [[doc-alfa]]
""",
    # Osservato, anche se ha una scaduta: va in coda
    "projects/epsilon/epsilon.md": """---
type: project
status: attivo
role: "Non coinvolto: lo segue un collega"
clients: []
people: []
updated: 2026-10-26
---

# Progetto Epsilon

## Attività

- [ ] Rilascio del collega 📅 2026-10-25 ([[doc-alfa]])
""",
}

CALENDARIO = [
    {"inizio": "2026-10-27T14:00:00+01:00", "fine": "2026-10-27T15:00:00+01:00", "tutto_il_giorno": False,
     "titolo": "Riunione pomeriggio", "luogo": "Sala 2", "online": False, "organizzatore": "Mario Rossi",
     "risposta": "accettato"},
    {"inizio": "2026-10-27T09:00:00Z", "fine": "2026-10-27T09:30:00Z", "titolo": "Call mattina",
     "online": True, "risposta": "provvisorio"},
    {"inizio": "2026-10-27T11:00:00+01:00", "fine": "2026-10-27T12:00:00+01:00", "titolo": "Evento rifiutato",
     "risposta": "rifiutato"},
    {"inizio": "2026-10-28", "fine": "2026-10-30", "tutto_il_giorno": True, "titolo": "Fiera di Bologna"},
    {"inizio": "2026-10-29T08:30:00+01:00", "fine": "2026-10-29T09:00:00+01:00", "titolo": "Colazione"},
    {"inizio": "2026-11-20T08:30:00+01:00", "titolo": "Fuori finestra"},
]

TASK = [
    {"task": "ingest-sharepoint", "atteso": "06:50", "eseguito": "06:51", "stato": "ok", "esito": "OK"},
    {"task": "ingest-outlook", "atteso": "07:05", "eseguito": "07:06", "stato": "errore",
     "esito": "connettore assente"},
    {"task": "ingest-github", "atteso": "07:20", "eseguito": "07:21", "stato": "ok", "esito": "OK"},
    {"task": "digest", "atteso": "07:45", "eseguito": "", "stato": "atteso", "esito": ""},
]

VUOTI = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Struttura(HTMLParser):
    """Controlla che ogni tag si chiuda nell'ordine giusto e conta tag e attributi."""

    def __init__(self):
        super().__init__()
        self.pila, self.errori, self.conta, self.href = [], [], {}, []

    def handle_starttag(self, tag, attrs):
        self.conta[tag] = self.conta.get(tag, 0) + 1
        self.href += [v for k, v in attrs if k in ("href", "src") and v]
        if tag not in VUOTI:
            self.pila.append(tag)

    def handle_endtag(self, tag):
        if not self.pila or self.pila[-1] != tag:
            self.errori.append(f"</{tag}> inatteso, aperti: {self.pila[-3:]}")
            return
        self.pila.pop()


def analizza(html):
    p = Struttura()
    p.feed(html)
    p.close()
    return p


@pytest.fixture
def dati(vault, tmp_path):
    """Cartella dati di plancia.py sul mini-vault con i progetti di prova, più calendario e task fissati."""
    for rel, testo in PROGETTI.items():
        scrivi(vault, rel, testo)
    out = tmp_path / "dati"
    res = esegui("plancia.py", vault, out)
    assert res.returncode == 0, res.stderr
    (out / "calendario.json").write_text(json.dumps(CALENDARIO, ensure_ascii=False), encoding="utf-8")
    (out / "task.json").write_text(json.dumps(TASK), encoding="utf-8")
    return out


def genera(vault, dati, tmp_path, *extra):
    pagina = tmp_path / "pagina" / "cockpit.html"
    res = esegui("cockpit.py", vault, dati, pagina, "--oggi", OGGI, "--ora", ORA, *extra)
    return res, (pagina.read_text(encoding="utf-8") if pagina.exists() else "")


def blocco(html, id_):
    """Il contenuto della sezione con quell'id."""
    m = re.search(rf'<section class="blocco" id="{id_}"[^>]*>(.*?)</section>', html, re.S)
    assert m, f"manca la sezione {id_}"
    return m.group(1)


def giorno_settimana(html, titolo):
    m = re.search(rf'<div class="gruppo"><h3>{re.escape(titolo)}.*?</div>(?=<div class="gruppo">|</div>$)',
                  blocco(html, "settimana"), re.S)
    assert m, f"manca il giorno {titolo}"
    return m.group(0)


def test_pagina_ben_formata(vault, dati, tmp_path):
    res, html = genera(vault, dati, tmp_path)
    assert res.returncode == 0, res.stderr
    p = analizza(html)
    assert p.errori == [] and p.pila == []
    assert "<title>Cockpit BlueAge</title>" in html[:8192]
    assert "{{" not in html and "}}" not in html
    # Una scheda per progetto attivo, una riga apribile per attività in Oggi e Settimana, le senza data
    assert p.conta["details"] == 4 + 3 + 2 + 1
    assert "martedì 27 ottobre 2026" in html and "aggiornato alle 07:40" in html


def test_contatori_della_testata(vault, dati, tmp_path):
    _, html = genera(vault, dati, tmp_path)
    contatori = dict((e, int(n)) for n, e in re.findall(
        r'<span class="n">(\d+)</span><span class="etichetta">([^<]+)</span>', html))
    # scadute: gamma 20/10 ed epsilon 25/10; oggi: due eventi e un'attività;
    # settimana: fiera (28 e 29), colazione, verbale di gamma (30), attività dell'inbox (1/11)
    assert contatori == {"scadute": 2, "oggi": 3, "in settimana": 5}
    assert 'href="#scadute"' in html and 'href="#settimana"' in html


def test_scaduta_nel_blocco_oggi(vault, dati, tmp_path):
    _, html = genera(vault, dati, tmp_path)
    oggi = blocco(html, "oggi")
    assert 'id="scadute"' in oggi
    riga = re.search(r'<li class="scaduta">.*?</li>', oggi, re.S).group(0)
    assert "Rispondere a" in riga and "da 7 giorni" in riga and "Progetto Gamma" in riga
    assert "da 2 giorni" in oggi                         # epsilon, scaduta il 25/10
    assert "Chiamare il fornitore" in oggi and "scade oggi" in oggi
    assert "Mandare il verbale" not in oggi


def test_attivita_nel_giorno_giusto_della_settimana(vault, dati, tmp_path):
    _, html = genera(vault, dati, tmp_path)
    assert "Mandare il verbale" in giorno_settimana(html, "ven 30 ott")
    assert "Valutare Tema Uno per un altro cliente" in giorno_settimana(html, "dom 1 nov")
    assert "domani" in giorno_settimana(html, "mer 28 ott")
    settimana = blocco(html, "settimana")
    assert "sab 31 ott" not in settimana                 # giorno vuoto: niente sottotitolo
    assert "Inviare la proposta" not in settimana        # 5/11, fuori dai 7 giorni
    assert "Preparare la demo" not in settimana          # senza data


def test_eventi_del_calendario(vault, dati, tmp_path):
    _, html = genera(vault, dati, tmp_path)
    oggi = blocco(html, "oggi")
    assert oggi.index("Call mattina") < oggi.index("Riunione pomeriggio")
    assert ">10:00<" in oggi                             # 09:00Z = 10:00 a Roma
    assert "da confermare" in oggi and "Sala 2 · Mario Rossi" in oggi
    assert "Evento rifiutato" not in html and "Fuori finestra" not in html
    for titolo in ("mer 28 ott", "gio 29 ott"):
        giorno = giorno_settimana(html, titolo)
        assert "Fiera di Bologna" in giorno and "tutto il giorno" in giorno
    assert "Fiera di Bologna" not in giorno_settimana(html, "ven 30 ott")    # fine esclusa
    gio = giorno_settimana(html, "gio 29 ott")
    assert gio.index("Fiera di Bologna") < gio.index("Colazione")


def test_ordine_dei_progetti(vault, dati, tmp_path):
    _, html = genera(vault, dati, tmp_path)
    ordine = re.findall(r'<details class="carta stato-(\w+)( osservi)?" data-progetto="([^"]+)"', html)
    assert [(slug, stato, bool(oss)) for stato, oss, slug in ordine] == [
        ("gamma", "allarme", False), ("delta", "attenzione", False), ("alfa", "ok", False),
        ("epsilon", "allarme", True)]
    progetti = blocco(html, "progetti")
    assert "scaduto" in progetti and "fermo da 56 giorni" in progetti and "in ordine" in progetti
    assert "Progetti che osservi" in progetti
    assert "Progetto Beta (in-pausa)" in progetti        # non attivo: solo citato
    # Prossimo passo: dalla sezione, altrimenti la prossima attività
    assert "Chiudere il &lt;b&gt;contratto&lt;/b&gt; &amp; partire" in progetti
    assert "Inviare la proposta" in progetti


def test_escaping_del_testo_delle_note(vault, dati, tmp_path):
    _, html = genera(vault, dati, tmp_path)
    assert "<script>alert" not in html and "<b>contratto" not in html
    assert "Rispondere a &lt;script&gt;alert(1)&lt;/script&gt; &amp; co" in html
    assert html.count("<script>") == 1                   # solo quello facoltativo del template


def test_senza_calendario(vault, dati, tmp_path):
    (dati / "calendario.json").unlink()
    res, html = genera(vault, dati, tmp_path)
    assert res.returncode == 0, res.stderr
    assert "Calendario non disponibile in questo giro" in blocco(html, "oggi")
    assert "Call mattina" not in html
    assert "calendario non disponibile" in res.stdout
    assert analizza(html).errori == []


def test_calendario_illeggibile(vault, dati, tmp_path):
    (dati / "calendario.json").write_text("{non json", encoding="utf-8")
    res, html = genera(vault, dati, tmp_path)
    assert res.returncode == 0
    assert "Calendario non disponibile in questo giro" in html and "Avviso" in res.stderr


def test_json_mancante(vault, dati, tmp_path):
    (dati / "attivita.json").unlink()
    res, html = genera(vault, dati, tmp_path)
    assert res.returncode == 1 and "attivita.json" in res.stderr and html == ""


def test_json_illeggibile(vault, dati, tmp_path):
    (dati / "progetti.json").write_text("[{", encoding="utf-8")
    res, _ = genera(vault, dati, tmp_path)
    assert res.returncode == 1


def test_argomenti_non_validi(vault, dati, tmp_path):
    assert genera(vault, dati, tmp_path, "--oggi", "27/10/2026")[0].returncode == 2
    assert esegui("cockpit.py", vault, dati, tmp_path / "x.html", "--ora", "25:00").returncode == 2
    assert esegui("cockpit.py", vault).returncode == 2
    aiuto = esegui("cockpit.py", vault, "--help")
    assert aiuto.returncode == 0 and "uso:" in aiuto.stdout and "calendario.json" in aiuto.stdout


def test_link_con_repo_url(vault, dati, tmp_path):
    _, html = genera(vault, dati, tmp_path, "--repo-url", REPO + "/")
    assert f'href="{REPO}/blob/main/projects/alfa/alfa.md"' in html
    assert f'href="{REPO}/blob/main/sources/sharepoint/delivery/doc-alfa.md"' in html    # fonte di un'attività
    assert f'href="{REPO}/blob/main/journal/2026-10-20.md"' in html                     # ultimo digest
    esterni = [h for h in analizza(html).href if h.startswith(("http://", "https://"))]
    assert esterni and all(h.startswith(REPO + "/blob/main/") for h in esterni)
    assert set(re.findall(r"https?://[^\s\"'<>)]+", html)) == set(esterni)


def test_nessuna_risorsa_esterna_senza_repo(vault, dati, tmp_path):
    # Il mini-vault non ha remote: niente link
    _, html = genera(vault, dati, tmp_path)
    assert not re.search(r"https?://", html)
    assert "[[doc-alfa]]" in html                        # la fonte resta come slug
    _, html = genera(vault, dati, tmp_path, "--repo-url", "")
    assert not re.search(r"https?://", html)


def test_riga_di_riepilogo(vault, dati, tmp_path):
    res, _ = genera(vault, dati, tmp_path)
    assert res.stdout.strip() == ("4 progetti attivi, 2 attività scadute, 3 in scadenza entro 7 giorni, "
                                  "4 eventi, 2 task OK su 3")


def test_fondo_della_pagina(vault, dati, tmp_path):
    _, html = genera(vault, dati, tmp_path)
    altro = blocco(html, "altro")
    assert "2 OK · 1 errore · 1 atteso" in altro
    assert "ingest-outlook 07:06 · errore: connettore assente" in altro
    assert "Da eseguire: digest 07:45" in altro
    assert "Digest del 20 ott" in altro and "1 nota nuova" in altro
    assert "1</p><p>nota da smistare" in altro
    assert re.search(r"Attività senza data <span class=\"conta\">2</span>", altro)
    assert "Generato da cockpit.py dal vault · 27 ott 2026, 07:40" in html
