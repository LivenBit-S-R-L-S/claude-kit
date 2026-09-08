#!/bin/bash
# Dopo ogni modifica a un file TypeScript, esegue il typecheck del progetto.
# Se fallisce, restituisce gli errori a Claude che li corregge nello stesso turno.

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
FILE="${FILE//\\//}"

case "$FILE" in
  *.ts|*.tsx) ;;
  *) exit 0 ;;
esac

cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
[ -f tsconfig.json ] || exit 0
[ -x node_modules/.bin/tsc ] || exit 0

OUT=$(npx --no-install tsc --noEmit 2>&1)
if [ $? -ne 0 ]; then
  echo "$OUT" | head -20 >&2
  exit 2
fi

exit 0
