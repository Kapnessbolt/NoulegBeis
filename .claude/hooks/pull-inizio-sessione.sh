#!/bin/bash
# Hook SessionStart (CLAUDE.md §1): allinea il vault con origin/main all'apertura della sessione,
# in cloud e in locale. Non blocca mai l'avvio: quello che stampa arriva a Claude, che se il pull
# è saltato o fallito lo rifà a mano.
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
git rev-parse --git-dir >/dev/null 2>&1 || exit 0
if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
  echo "git pull saltato: ci sono modifiche non committate. Committale, poi git pull --rebase origin main."
  exit 0
fi
limite=""
command -v timeout >/dev/null && limite="timeout 30"
if out=$(GIT_TERMINAL_PROMPT=0 $limite git pull --rebase -q origin main 2>&1); then
  echo "Vault allineato con origin/main: $(git log -1 --format='%h %s')"
else
  git rebase --abort >/dev/null 2>&1
  echo "git pull non riuscito (${out%%$'\n'*}): rifallo a mano con git pull --rebase origin main."
fi
# PyYAML serve a controlla-vault.py e plancia.py (e quindi al pre-commit): l'immagine cloud oggi
# lo ha, ma non è garantito. Se manca prova a installarlo, altrimenti lo dice.
if ! python3 -c "import yaml" >/dev/null 2>&1; then
  if $limite python3 -m pip install -q --user pyyaml >/dev/null 2>&1; then
    echo "PyYAML mancava: installato."
  else
    echo "PyYAML manca e non si installa da solo: pip install pyyaml, o il pre-commit si blocca."
  fi
fi
exit 0
