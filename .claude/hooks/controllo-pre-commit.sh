#!/bin/bash
# Hook PreToolUse (SPEC 4.4): prima di un `git commit` lancia il controllo del vault
# sui file modificati. Se trova errori blocca il commit (exit 2) e li passa a Claude.
input=$(cat)
command=$(printf '%s' "$input" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null)
case "$command" in
  *"git commit"*) ;;
  *) exit 0 ;;
esac
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
report=$(python3 .claude/scripts/controlla-vault.py --modificati 2>&1)
if [ $? -ne 0 ]; then
  printf '%s\n' "$report" >&2
  exit 2
fi
exit 0
