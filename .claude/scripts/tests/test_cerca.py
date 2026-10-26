"""Test di cerca.py (SPEC 9.3, step 17 di 13.1) sul mini-vault di conftest.py."""

import json

import pytest

from conftest import esegui, scrivi


def cerca(root, *args):
    return esegui("cerca.py", root, *args)


def risultati(root, *args):
    res = cerca(root, *args, "--json")
    assert res.returncode == 0, res.stderr
    return json.loads(res.stdout)


def slugs(root, *args):
    return [r["slug"] for r in risultati(root, *args)]


def nota_semplice(root, rel, titolo, corpo="", tipo="topic", extra=""):
    return scrivi(root, rel, f"---\ntype: {tipo}\n{extra}---\n\n# {titolo}\n\n{corpo}\n")


# --- Termini ----------------------------------------------------------------------------

def test_ricerca_semplice(vault):
    assert set(slugs(vault, "pilota")) == {"alfa", "alfa-log", "cliente-uno", "mario-rossi",
                                           "doc-alfa", "2026-10-20"}


def test_piu_termini_in_and(vault):
    # `acquisti`: nel corpo di alfa e nel ruolo (frontmatter) di mario-rossi
    assert set(slugs(vault, "pilota", "acquisti")) == {"alfa", "mario-rossi"}


def test_frase_tra_virgolette(vault):
    assert set(slugs(vault, "caso pilota")) == {"alfa", "alfa-log"}
    assert slugs(vault, "pilota caso") == []
    # virgolette dentro un solo argomento, come le passa chi non usa la shell
    assert set(slugs(vault, 'acquisti "caso pilota"')) == {"alfa"}
    # la frase passa sopra trattini e maiuscole: `cliente uno` trova [[cliente-uno]]
    assert "cliente-uno" in slugs(vault, "cliente uno")


def test_apostrofo_e_virgolette_in_un_argomento(vault):
    nota_semplice(vault, "topics/cresce.md", "L'AI che cresce con l'azienda")
    nota_semplice(vault, "topics/cresce-due.md", "Cresce da sola", corpo="Un'azienda.")
    assert slugs(vault, "l'azienda") == ["cresce"]
    assert slugs(vault, 'cresce "con l\'azienda"') == ["cresce"]
    assert slugs(vault, 'cresce -"con l\'azienda"') == ["cresce-due"]


def test_esclusione(vault):
    assert set(slugs(vault, "pilota", "-acquisti")) == {"alfa-log", "cliente-uno", "doc-alfa",
                                                        "2026-10-20"}
    # frase esclusa
    assert "alfa" not in slugs(vault, "pilota", "-caso pilota")
    assert "alfa-log" not in slugs(vault, "pilota", "-caso pilota")
    # dopo `--` anche un termine che sembra un'opzione
    assert set(slugs(vault, "--tipo", "project", "--", "-alfa")) == {"beta"}


def test_solo_esclusioni(vault):
    assert set(slugs(vault, "--cartella", "projects", "-pilota")) == {"beta"}


def test_accenti_e_maiuscole(vault):
    base = set(slugs(vault, "attivita"))
    assert base >= {"alfa", "beta"}
    assert set(slugs(vault, "ATTIVITÀ")) == base
    assert set(slugs(vault, "Attività")) == base
    # accento nel testo e non nella query, e viceversa
    nota_semplice(vault, "topics/caffe.md", "Pausa caffè")
    assert slugs(vault, "caffe") == ["caffe"]
    assert slugs(vault, "CAFFÈ") == ["caffe"]


def test_inizio_parola(vault):
    # `ilota` è dentro `pilota`: non è un inizio di parola
    assert slugs(vault, "ilota") == []
    assert "alfa" in slugs(vault, "pilo")


# --- Filtri -----------------------------------------------------------------------------

def test_filtro_tipo(vault):
    assert slugs(vault, "pilota", "--tipo", "person") == ["mario-rossi"]
    assert set(slugs(vault, "pilota", "--tipo", "person", "--tipo", "client")) == {"mario-rossi",
                                                                                  "cliente-uno"}


def test_filtro_cartella(vault):
    assert set(slugs(vault, "pilota", "--cartella", "projects")) == {"alfa", "alfa-log"}
    assert set(slugs(vault, "pilota", "--cartella", "projects/alfa/")) == {"alfa", "alfa-log"}
    assert slugs(vault, "pilota", "--cartella", "proj") == []  # cartelle intere, non prefissi di nome
    assert set(slugs(vault, "--cartella", "sources", "--cartella", "inbox")) == {"doc-alfa",
                                                                                "2026-10-20-idea"}


def test_filtro_progetto(vault):
    assert set(slugs(vault, "--progetto", "alfa")) == {"alfa-log", "cliente-uno", "mario-rossi",
                                                       "tema-uno", "doc-alfa"}


def test_filtro_cliente(vault):
    assert set(slugs(vault, "--cliente", "cliente-uno")) == {"alfa", "mario-rossi", "tema-uno",
                                                             "doc-alfa"}


def test_filtro_tema(vault):
    assert set(slugs(vault, "--tema", "tema-uno")) == {"doc-alfa", "2026-10-20-prova",
                                                       "2026-10-20-idea"}


def test_filtro_persona(vault):
    assert set(slugs(vault, "--persona", "mario-rossi")) == {"alfa", "cliente-uno", "doc-alfa"}
    # nel frontmatter (`participants`) di una mail
    scrivi(vault, "sources/mail/2026-10/saluti.md", """---
type: source-mail
participants: ["[[mario-rossi]]"]
last_message: 2026-10-21T08:00:00Z
clients: ["[[cliente-uno]]"]
---

# Saluti
""")
    assert "saluti" in slugs(vault, "--persona", "mario-rossi")


def test_filtri_combinati(vault):
    assert slugs(vault, "--persona", "mario-rossi", "--tipo", "project") == ["alfa"]
    assert slugs(vault, "pilota", "--cliente", "cliente-uno", "--tipo", "person") == ["mario-rossi"]


def test_filtro_date(vault):
    # doc-alfa: current.last_modified 2026-10-01; le altre note sono del 2026-10-20
    assert slugs(vault, "--cartella", "sources", "--a", "2026-10-10") == ["doc-alfa"]
    assert "doc-alfa" not in slugs(vault, "--da", "2026-10-02", "--limite", "0")
    # alfa-log non ha campi data: vale la riga di log più recente (2026-10-20)
    assert "alfa-log" in slugs(vault, "--da", "2026-10-20", "--limite", "0")
    assert "alfa-log" not in slugs(vault, "--da", "2026-10-21", "--limite", "0")
    assert "alfa-log" in slugs(vault, "--cartella", "projects")
    assert set(slugs(vault, "pilota", "--da", "2026-10-20", "--a", "2026-10-20")) == {
        "alfa", "alfa-log", "cliente-uno", "mario-rossi", "2026-10-20"}


def test_data_dal_nome_del_file(vault):
    scrivi(vault, "inbox/2026-09-01-vecchia.md", "---\ntype: inbox\n---\n\n# Vecchia idea\n")
    [r] = risultati(vault, "vecchia")
    assert r["data"] == "2026-09-01"
    assert slugs(vault, "--a", "2026-09-30") == ["2026-09-01-vecchia"]


def test_data_ordine_dei_campi(vault):
    # `date` vince su `updated`, `last_message` su `first_message`
    nota_semplice(vault, "topics/con-date.md", "Con date", extra="date: 2026-01-02\nupdated: 2026-05-05\n")
    scrivi(vault, "sources/mail/2026-02/filo.md", "---\ntype: source-mail\n"
           "first_message: 2026-02-01T10:00:00Z\nlast_message: 2026-02-03T23:30:00Z\n---\n\n# Filo\n")
    assert risultati(vault, "con date")[0]["data"] == "2026-01-02"
    assert risultati(vault, "filo")[0]["data"] == "2026-02-03"


def test_filtro_tag(vault):
    nota_semplice(vault, "topics/tema-due.md", "Tema due", extra="tags: [da-verificare, Prova]\n")
    nota_semplice(vault, "topics/tema-tre.md", "Tema tre", extra="tags: [altro]\n")
    assert slugs(vault, "--tag", "da-verificare") == ["tema-due"]
    assert slugs(vault, "--tag", "prova") == ["tema-due"]
    assert set(slugs(vault, "tema", "--tag", "prova", "--tag", "altro")) == {"tema-due", "tema-tre"}


# --- Ordinamento ------------------------------------------------------------------------

def test_titolo_prima_del_frontmatter_prima_del_corpo(vault):
    nota_semplice(vault, "topics/nel-titolo.md", "Zafferano in testa")
    nota_semplice(vault, "topics/nel-frontmatter.md", "Altro", extra='kind: "zafferano"\n')
    nota_semplice(vault, "topics/nel-corpo.md", "Altro ancora", corpo="Si parla di zafferano.")
    res = risultati(vault, "zafferano")
    assert [r["slug"] for r in res] == ["nel-titolo", "nel-frontmatter", "nel-corpo"]
    assert [r["punteggio"] for r in res] == [10, 3, 1]


def test_slug_pesa_come_il_titolo(vault):
    nota_semplice(vault, "topics/zafferano-slug.md", "Titolo diverso")
    nota_semplice(vault, "topics/nel-corpo.md", "Altro ancora", corpo="Si parla di zafferano.")
    assert slugs(vault, "zafferano") == ["zafferano-slug", "nel-corpo"]


def test_a_parita_vince_chi_ha_piu_backlink(vault):
    nota_semplice(vault, "topics/zeta-poco.md", "Zeta")
    nota_semplice(vault, "topics/zeta-hub.md", "Zeta")
    for n in range(3):
        nota_semplice(vault, f"topics/rimando-{n}.md", f"Rimando {n}", corpo="Vedi [[zeta-hub]].")
    # anche dal frontmatter
    nota_semplice(vault, "topics/rimando-fm.md", "Rimando fm", extra='projects: ["[[zeta-poco]]"]\n')
    res = risultati(vault, "zeta", "--tipo", "topic")
    assert [r["slug"] for r in res][:2] == ["zeta-hub", "zeta-poco"]
    assert [r["backlink"] for r in res][:2] == [3, 1]


def test_a_parita_di_backlink_vince_la_piu_recente(vault):
    nota_semplice(vault, "topics/omega-vecchia.md", "Omega", extra="updated: 2026-01-01\n")
    nota_semplice(vault, "topics/omega-nuova.md", "Omega", extra="updated: 2026-06-01\n")
    nota_semplice(vault, "topics/omega-senza.md", "Omega")
    assert slugs(vault, "omega") == ["omega-nuova", "omega-vecchia", "omega-senza"]


def test_backlink_contati_una_volta_per_nota(vault):
    # doc-alfa è collegato da alfa, alfa-log, cliente-uno, mario-rossi, tema-uno e dal digest
    [r] = [r for r in risultati(vault, "documento alfa") if r["slug"] == "doc-alfa"]
    assert r["backlink"] == 6


def test_senza_termini_per_data(vault):
    # alfa e alfa-log sono del 2026-10-20 (alfa-log dalla riga di log), doc-alfa del 2026-10-01;
    # a parità di data vince chi ha più backlink
    assert slugs(vault, "--cartella", "sources", "--cartella", "projects/alfa") == [
        "alfa", "alfa-log", "doc-alfa"]


def test_limite(vault):
    assert len(slugs(vault, "pilota", "--limite", "2")) == 2
    assert len(slugs(vault, "pilota", "--limite", "0")) == 6
    res = cerca(vault, "pilota", "--limite", "2")
    assert "altri 4 risultati" in res.stdout


# --- Output -----------------------------------------------------------------------------

def test_riga_di_testo(vault):
    res = cerca(vault, "progetto alfa")
    assert res.returncode == 0, res.stderr
    prima = res.stdout.splitlines()[0]
    assert prima == "10 · project · [[alfa]] · Progetto Alfa · 2026-10-20 · 5 backlink"


def test_contesto(vault):
    res = cerca(vault, "budget", "--contesto", "--tipo", "client")
    righe = res.stdout.splitlines()
    assert righe[0].startswith("1 · client · [[cliente-uno]]")
    assert righe[1] == "    > - Cliente dal 2026, budget di 3.000 € per il pilota ([[doc-alfa]])"
    assert cerca(vault, "budget", "--tipo", "client").stdout.count("    > ") == 0


def test_contesto_al_massimo_due_righe_tagliate(vault):
    lunga = "parola " * 10 + "girasole " + "riempitivo " * 30
    nota_semplice(vault, "topics/lunga.md", "Lunga",
                  corpo=f"- girasole uno\n- girasole due\n- {lunga}\n")
    [r] = risultati(vault, "girasole", "--contesto")
    assert len(r["contesto"]) == 2
    nota_semplice(vault, "topics/lunga.md", "Lunga", corpo=f"- {lunga}\n")
    [r] = risultati(vault, "girasole")
    [c] = r["contesto"]
    assert c.endswith("…") and "girasole" in c and len(c) <= 162


def test_json_con_tutti_i_campi(vault):
    [r] = risultati(vault, "riassunto", "--tipo", "source-doc")
    assert set(r) == {"slug", "percorso", "type", "titolo", "data", "backlink", "punteggio",
                      "contesto", "frontmatter"}
    assert r["slug"] == "doc-alfa"
    assert r["percorso"] == "sources/sharepoint/delivery/doc-alfa.md"
    assert r["type"] == "source-doc"
    assert r["titolo"] == "Documento Alfa"
    assert r["data"] == "2026-10-01"
    assert r["backlink"] == 6
    assert r["punteggio"] == 1
    assert r["contesto"] == ["## Riassunto"]
    assert r["frontmatter"]["current"]["last_modified"] == "2026-10-01T10:00:00Z"
    assert r["frontmatter"]["projects"] == ["[[alfa]]"]


def test_zero_risultati(vault):
    res = cerca(vault, "inesistentissimo")
    assert res.returncode == 0
    assert res.stdout.strip() == "nessun risultato"
    assert risultati(vault, "inesistentissimo") == []


# --- Collegamenti e scheda --------------------------------------------------------------

def test_collegamenti_testo(vault):
    res = cerca(vault, "--collegamenti", "alfa")
    assert res.returncode == 0, res.stderr
    out = res.stdout
    assert out.splitlines()[0] == "[[alfa]] · Progetto Alfa · project · collegata da 5 note"
    assert "project-log (1)" in out and "client (1)" in out and "person (1)" in out
    assert "- [[mario-rossi]] · Mario Rossi · 2026-10-20" in out
    assert out.index("project-log") < out.index("client (") < out.index("person (") < out.index("source-doc")


def test_collegamenti_json_per_data(vault):
    nota_semplice(vault, "topics/vecchio.md", "Vecchio", corpo="[[alfa]]", extra="updated: 2026-01-01\n")
    res = cerca(vault, "--collegamenti", "alfa", "--json")
    d = json.loads(res.stdout)
    assert d["slug"] == "alfa" and d["backlink"] == 6
    assert [n["slug"] for n in d["per_tipo"]["topic"]] == ["tema-uno", "vecchio"]
    assert set(d["per_tipo"]["topic"][0]) == {"slug", "percorso", "titolo", "data"}
    # con un filtro
    d = json.loads(cerca(vault, "--collegamenti", "alfa", "--tipo", "person", "--json").stdout)
    assert list(d["per_tipo"]) == ["person"]


def test_collegamenti_nota_inesistente(vault):
    res = cerca(vault, "--collegamenti", "alfa-x")
    assert res.returncode == 1
    assert "non trovata" in res.stderr and "alfa" in res.stderr


def test_scheda_nota(vault):
    res = cerca(vault, "--nota", "alfa", "--json")
    assert res.returncode == 0, res.stderr
    d = json.loads(res.stdout)
    assert d["percorso"] == "projects/alfa/alfa.md"
    assert d["type"] == "project" and d["titolo"] == "Progetto Alfa" and d["data"] == "2026-10-20"
    assert d["frontmatter"]["status"] == "attivo"
    assert [s["titolo"] for s in d["sezioni"]] == ["Stato", "Attività", "Decisioni", "Prossimi passi", "Fonti"]
    assert d["sezioni"][1]["righe"] == 3
    assert d["backlink"] == 5
    assert set(d["collega"]) == {"cliente-uno", "mario-rossi", "doc-alfa"}
    testo = cerca(vault, "--nota", "alfa").stdout
    assert "percorso: projects/alfa/alfa.md" in testo
    assert "  status: attivo" in testo and "  - Attività (3 righe)" in testo


def test_scheda_nota_inesistente(vault):
    res = cerca(vault, "--nota", "gamma")
    assert res.returncode == 1
    assert "non trovata" in res.stderr


# --- Codici di uscita e note saltate ----------------------------------------------------

@pytest.mark.parametrize("args", [
    [],
    ["pilota", "--da", "2026-13-01"],
    ["pilota", "--a", "ieri"],
    ["pilota", "--limite", "-1"],
    ["pilota", "--limite", "molti"],
    ["--nota", "alfa", "pilota"],
    ["--nota", "alfa", "--tipo", "project"],
    ["--nota", "alfa", "--collegamenti", "alfa"],
    ["pilota", "--da", "2026-10-20", "--a", "2026-10-01"],
    ["pilota", "--opzione-che-non-esiste"],
    ["!!!"],
])
def test_argomenti_non_validi(vault, args):
    res = cerca(vault, *args)
    assert res.returncode == 2
    assert "errore" in res.stderr


def test_slug_del_filtro_inesistente(vault):
    res = cerca(vault, "pilota", "--progetto", "gamma")
    assert res.returncode == 1
    assert "gamma" in res.stderr


def test_aiuto(vault):
    res = cerca(vault, "--help")
    assert res.returncode == 0
    assert res.stdout.startswith("Uso: cerca.py")
    assert "--collegamenti" in res.stdout and "Punteggio" in res.stdout


def test_frontmatter_rotto_saltato_con_avviso(vault):
    scrivi(vault, "people/rotta.md", "---\ntype: [person\n---\n\n# Rotta pilota\n\n[[beta]]\n")
    scrivi(vault, "topics/senza-frontmatter.md", "# Senza frontmatter pilota\n")
    res = cerca(vault, "pilota", "--json")
    assert res.returncode == 0
    assert "people/rotta.md" in res.stderr and "frontmatter non leggibile" in res.stderr
    assert "topics/senza-frontmatter.md" in res.stderr
    trovati = {r["slug"] for r in json.loads(res.stdout)}
    assert "rotta" not in trovati and "senza-frontmatter" not in trovati
    assert len(trovati) == 6
    # la nota saltata non conta nemmeno nei backlink: beta resta collegata solo dal diario
    assert json.loads(cerca(vault, "--nota", "beta", "--json").stdout)["collegata_da"] == ["2026-10-20-prova"]


def test_file_esclusi(vault):
    for rel in ("CLAUDE.md", "README.md", "SPEC.md", "home.md", "_templates/extra.md",
                ".claude/agents/extra.md", "sessions/_raw/estratto.md", ".obsidian/extra.md"):
        nota_semplice(vault, rel, "Unicorno escluso")
    nota_semplice(vault, "topics/unicorno.md", "Unicorno vero")
    res = cerca(vault, "unicorno", "--json")
    assert res.returncode == 0
    assert [r["slug"] for r in json.loads(res.stdout)] == ["unicorno"]
    assert res.stderr == ""
