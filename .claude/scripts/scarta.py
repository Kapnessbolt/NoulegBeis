#!/usr/bin/env python3
"""Filtri di scarto della posta (SPEC 5.3, 6.3 passo 2; agente ingestor §5): dice se una mail va
scartata in base agli elenchi di `vault.yaml` (`fonti.outlook`), dal mittente e dall'oggetto.

Applica solo gli elenchi. Il giudizio su notifiche di servizi, newsletter e marketing, thread
personali o estranei all'organizzazione resta all'agente (SPEC 5.3), sulle mail che questo script
tiene.

Uso:
  python3 .claude/scripts/scarta.py --mittente "<indirizzo o 'Nome <indirizzo>'>" [--oggetto "<oggetto>"] [--json]

Regole, nell'ordine (vince la prima che scatta; confronti senza maiuscole):
  1. `mittenti_scartati`, sulla parte locale dell'indirizzo (prima di `@`): scarta se è uguale a un
     termine, se inizia con un termine, o se il termine coincide con uno dei pezzi separati da
     `-` `.` `_` `+` (o con più pezzi di seguito, per i termini che hanno un separatore):
     `no-reply@`, `noreply123@`, `teams-notifications@`, `teams.no-reply@` → scarta; `lorenzo@` → tieni;
  2. `domini_scartati`: dominio uguale al termine o che finisce con `.<termine>` (sottodomini);
  3. `oggetti_scartati`: termine contenuto nell'oggetto.

Uscita: 0 = tieni (da ingerire, salvo il giudizio dell'agente), 1 = scarta, 2 = argomenti o
configurazione non validi (anche un mittente senza `@`).
Testo: `scarta · mittente `no-reply` (fonti.outlook.mittenti_scartati)` oppure `tieni`.
Con `--json`:
  {"scarta": true|false, "regola": "mittenti_scartati"|"domini_scartati"|"oggetti_scartati"|null,
   "termine": "..."|null, "motivo": "..."|null, "mittente": "<indirizzo>", "oggetto": "..."|null}
`mittente` è l'indirizzo senza il nome visualizzato, in minuscolo.

Come modulo: `valuta(mittente, oggetto=None, c=None)` restituisce lo stesso dizionario (ValueError
se il mittente non è un indirizzo). Gli elenchi si leggono con `config.py outlook`.

La variabile d'ambiente VAULT_ROOT, se presente, indica la radice del vault al posto della
cartella che contiene `.claude/` (serve ai test in `.claude/scripts/tests/`).
"""

import argparse
import json
import re
import sys
from email.utils import parseaddr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config  # noqa: E402

SEPARATORI_RE = re.compile(r"[-._+]")


def _pezzi(testo):
    return [x for x in SEPARATORI_RE.split(testo) if x]


def indirizzo(mittente):
    """Indirizzo in minuscolo da `indirizzo` o `Nome <indirizzo>`; ValueError se non lo è."""
    _, addr = parseaddr(str(mittente or "").strip())
    addr = addr.strip().lower()
    locale, chiocciola, dominio = addr.rpartition("@")
    if not chiocciola or not locale or not dominio or any(ch.isspace() for ch in addr):
        raise ValueError(f"mittente senza un indirizzo `nome@dominio`: {mittente!r}")
    return addr


def mittente_scartato(locale, termine):
    """True se la parte locale dell'indirizzo cade sotto il termine di `mittenti_scartati`."""
    if not termine:
        return False
    if locale == termine or locale.startswith(termine):
        return True
    pezzi, cercati = _pezzi(locale), _pezzi(termine)
    n = len(cercati)
    return n > 0 and any(pezzi[i:i + n] == cercati for i in range(len(pezzi) - n + 1))


def dominio_scartato(dominio, termine):
    return bool(termine) and (dominio == termine or dominio.endswith("." + termine))


def valuta(mittente, oggetto=None, c=None):
    """Esito dei filtri di `fonti.outlook` su mittente e oggetto (dizionario dell'uscita JSON)."""
    addr = indirizzo(mittente)
    locale, _, dominio = addr.rpartition("@")
    ol = config.outlook(c)
    oggetto_basso = (oggetto or "").casefold()
    regole = (
        ("mittenti_scartati", "mittente", lambda t: mittente_scartato(locale, t.strip().casefold())),
        ("domini_scartati", "dominio", lambda t: dominio_scartato(dominio, t.strip().casefold().lstrip("@."))),
        ("oggetti_scartati", "oggetto con", lambda t: bool(t.strip()) and t.strip().casefold() in oggetto_basso),
    )
    out = {"scarta": False, "regola": None, "termine": None, "motivo": None,
           "mittente": addr, "oggetto": oggetto}
    for regola, cosa, scatta in regole:
        termine = next((t for t in ol[regola] if scatta(t)), None)
        if termine is not None:
            return {**out, "scarta": True, "regola": regola, "termine": termine,
                    "motivo": f"{cosa} `{termine}` (fonti.outlook.{regola})"}
    return out


def main(argv):
    parser = argparse.ArgumentParser(prog="scarta.py", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--mittente", required=True)
    parser.add_argument("--oggetto")
    parser.add_argument("--json", action="store_true")
    try:
        args = parser.parse_args(argv)
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 2
    try:
        r = valuta(args.mittente, args.oggetto)
    except config.ConfigErrata as e:
        sys.stderr.write("Configurazione non valida:\n" + "\n".join(f"- {m}" for m in e.errori) + "\n")
        return 2
    except ValueError as e:
        sys.stderr.write(f"Errore: {e}\n")
        return 2
    if args.json:
        print(json.dumps(r, ensure_ascii=False))
    else:
        print(f"scarta · {r['motivo']}" if r["scarta"] else "tieni")
    return 1 if r["scarta"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
