#!/bin/bash
# Blocca la scrittura di credenziali in chiaro e la modifica di file sensibili.
# Uscita 2 = azione bloccata, stderr torna a Claude come feedback.

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
BODY=$(echo "$INPUT" | jq -r '.tool_input.content // .tool_input.new_string // empty')

# Normalizza i separatori di percorso in stile Windows
FILE="${FILE//\\//}"

case "$FILE" in
  *.env.example|*.env.sample|*.env.template) ;;
  *.env|*.env.*|*/.git/*|*/id_rsa|*/id_ed25519|*.pem|*.p12)
    echo "Blocked: $FILE non si modifica da qui. Le credenziali stanno in variabili d'ambiente, mai nel repo." >&2
    exit 2
    ;;
esac

PATTERNS='sk_live_[A-Za-z0-9]'
PATTERNS="$PATTERNS|sk_test_[A-Za-z0-9]"
PATTERNS="$PATTERNS|rk_live_[A-Za-z0-9]"
PATTERNS="$PATTERNS|whsec_[A-Za-z0-9]"
PATTERNS="$PATTERNS|eyJhbGciOi"
PATTERNS="$PATTERNS|-----BEGIN [A-Z ]*PRIVATE KEY-----"
PATTERNS="$PATTERNS|ghp_[A-Za-z0-9]{20}"
PATTERNS="$PATTERNS|github_pat_[A-Za-z0-9]"
PATTERNS="$PATTERNS|AKIA[0-9A-Z]{16}"
PATTERNS="$PATTERNS|sk-ant-[A-Za-z0-9_-]{10}"
PATTERNS="$PATTERNS|sk-proj-[A-Za-z0-9_-]{10}"
PATTERNS="$PATTERNS|AIza[0-9A-Za-z_-]{20}"
PATTERNS="$PATTERNS|xox[baprs]-[0-9A-Za-z-]{10}"

if echo "$BODY" | grep -qE "$PATTERNS"; then
  echo "Blocked: credenziale in chiaro rilevata in $FILE. Se è reale ruotala subito, poi leggila da process.env." >&2
  exit 2
fi

exit 0
