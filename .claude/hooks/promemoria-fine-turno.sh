#!/bin/bash
# Hook Stop (CLAUDE.md §7-8): nelle sessioni locali, a fine risposta, se nel vault restano modifiche
# non committate o commit non spinti su origin, rimanda Claude a chiuderli (exit 2), come fa l'hook
# dell'ambiente cloud. In cloud non fa nulla: lì c'è già quello dell'ambiente.
[ "$CLAUDE_CODE_REMOTE" = "true" ] && exit 0
input=$(cat)
attivo=$(printf '%s' "$input" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("stop_hook_active", False))' 2>/dev/null)
[ "$attivo" = "True" ] && exit 0
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
git rev-parse --git-dir >/dev/null 2>&1 || exit 0
if [ -n "$(git status --porcelain)" ]; then
  echo "Nel vault ci sono modifiche non committate: controlla-vault.py, commit, git pull --rebase origin main e push su main (CLAUDE.md §7)." >&2
  exit 2
fi
remoto=$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || echo origin/main)
if [ "$(git rev-list --count "$remoto..HEAD" 2>/dev/null || echo 0)" -gt 0 ]; then
  echo "Nel vault ci sono commit non spinti su $remoto: git pull --rebase origin main e push su main (CLAUDE.md §7)." >&2
  exit 2
fi
exit 0
