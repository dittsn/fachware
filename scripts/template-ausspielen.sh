#!/usr/bin/env bash
# Spielt den Template-Ordner dieses Repos in die Arbeitskopie des Template-Repos aus.
# Das Template-Repo wird nie direkt bearbeitet; Quelle ist immer skills/fachware/assets/template/.
# Aufruf: scripts/template-ausspielen.sh [PFAD_ZUR_TEMPLATE_ARBEITSKOPIE]   (Standard: ../fachware-template)
set -euo pipefail
QUELLE="$(cd "$(dirname "$0")/.." && pwd)/skills/fachware/assets/template"
ZIEL="${1:-$(cd "$(dirname "$0")/.." && pwd)/../fachware-template}"
[ -d "$ZIEL/.git" ] || { echo "Template-Arbeitskopie nicht gefunden: $ZIEL" >&2; exit 1; }
# Alles außer .git und der Template-eigenen README-Ergänzung überschreiben
rsync -a --delete --exclude '.git' --exclude 'README-template.md' "$QUELLE/" "$ZIEL/"
cd "$ZIEL"
if git status --porcelain | grep -q .; then
  VERSION="$(git -C "$QUELLE" describe --tags --always 2>/dev/null || echo unbekannt)"
  git add -A
  git commit -q -m "Ausspielung aus fachware ($VERSION)"
  echo "Ausgespielt und committet ($VERSION). Jetzt: git -C $ZIEL push"
else
  echo "Keine Änderungen – Template-Repo ist auf Stand."
fi
