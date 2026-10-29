#!/bin/bash
# Setup dell'ambiente cloud del vault (SPEC 13.1, step 13): installa le dipendenze Python di
# script, test e skill. Idempotente (salta ciò che c'è già) e tollerante (un pacchetto che non
# si installa è un avviso, mai un errore: lo script esce sempre con 0).
#
# Come si usa:
# - nell'interfaccia di claude.ai, nelle impostazioni dell'ambiente, lo script di setup diventa
#   `bash .claude/setup/ambiente-cloud.sh` se a quel punto il repo è già clonato nella cartella
#   di lavoro; altrimenti si incolla lì il contenuto di questo file;
# - in locale o in una sessione già aperta: `bash .claude/setup/ambiente-cloud.sh`.
# L'hook di avvio `.claude/hooks/pull-inizio-sessione.sh` resta la rete di sicurezza per PyYAML.
#
# Dipendenze: pyyaml (script e pre-commit), pytest (test degli script), python-pptx (skill
# blueage-deck; porta con sé lxml), fonttools (`install_font.sh` della skill blueage-deck).
# Node, Playwright, Chromium e ffmpeg delle skill sono già nell'immagine cloud.

# modulo da importare : pacchetto pip
PACCHETTI=(
  "yaml:pyyaml"
  "pytest:pytest"
  "pptx:python-pptx"
  "fontTools:fonttools"
)

limite=""
command -v timeout >/dev/null && limite="timeout 120"
mancanti=()
for voce in "${PACCHETTI[@]}"; do
  modulo="${voce%%:*}"
  pacchetto="${voce#*:}"
  if python3 -c "import $modulo" >/dev/null 2>&1; then
    echo "ok · $pacchetto già presente"
  else
    mancanti+=("$pacchetto")
  fi
done

for pacchetto in "${mancanti[@]}"; do
  if $limite python3 -m pip install -q "$pacchetto" >/dev/null 2>&1 \
     || $limite python3 -m pip install -q --user "$pacchetto" >/dev/null 2>&1 \
     || $limite python3 -m pip install -q --user --break-system-packages "$pacchetto" >/dev/null 2>&1; then
    echo "ok · $pacchetto installato"
  else
    echo "avviso · $pacchetto non installato: python3 -m pip install $pacchetto"
  fi
done
exit 0
