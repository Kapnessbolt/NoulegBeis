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
exit 0
