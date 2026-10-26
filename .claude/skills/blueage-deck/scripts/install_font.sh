#!/usr/bin/env bash
# Installa Plus Jakarta Sans (Regular, Bold, Italic, Bold Italic) per anteprime fedeli.
set -e
T=$(mktemp -d); cd "$T"
npm pack @fontsource/plus-jakarta-sans >/dev/null 2>&1
tar xzf fontsource-plus-jakarta-sans-*.tgz
mkdir -p ~/.fonts
python3 - <<'PY'
from fontTools.ttLib import TTFont
import os
m={("400","normal"):"Regular",("700","normal"):"Bold",("400","italic"):"Italic",("700","italic"):"Bold Italic"}
for (w,s),sub in m.items():
    f=TTFont(f"package/files/plus-jakarta-sans-latin-{w}-{s}.woff"); f.flavor=None
    n=f["name"]
    for r in list(n.names):
        if r.nameID in (1,16): n.setName("Plus Jakarta Sans",r.nameID,r.platformID,r.platEncID,r.langID)
        if r.nameID in (2,17): n.setName(sub,r.nameID,r.platformID,r.platEncID,r.langID)
        if r.nameID==4: n.setName("Plus Jakarta Sans "+sub,4,r.platformID,r.platEncID,r.langID)
    b=w=="700"; i=s=="italic"
    f["OS/2"].usWeightClass=int(w)
    f["OS/2"].fsSelection=(0x20 if b else 0)|(0x01 if i else 0)|(0x40 if not(b or i) else 0)
    f["head"].macStyle=(1 if b else 0)|(2 if i else 0)
    f.save(os.path.expanduser(f"~/.fonts/PlusJakartaSans-{sub.replace(' ','')}.ttf"))
PY
fc-cache -f >/dev/null
fc-list | grep -c "Plus Jakarta Sans" | xargs echo "Stili installati:"
