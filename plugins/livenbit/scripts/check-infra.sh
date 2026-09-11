#!/bin/bash
# Verifica dove sono ospitati i dati di un progetto, leggendo i fatti
# registrati da /livenbit:nuovo-progetto in .claude/infra.json.
#
# Esiste per una ragione sola: un DPA non deve mai dichiarare "dati in UE"
# se nessuno l'ha accertato. Meglio "da verificare" che una dichiarazione
# falsa firmata da entrambe le parti.
#
# Uso:  check-infra.sh [directory-progetto]
# Esce 0 solo se tutto risulta UE e il rilevamento non e' scaduto.

cd "${1:-.}" || exit 1
F=".claude/infra.json"
SCADENZA_GIORNI=180

if [ ! -f "$F" ]; then
  echo "NON VERIFICABILE: manca $F"
  echo "  Il DPA non puo' dichiarare la localizzazione dei dati."
  echo "  Rimedio: lancia /livenbit:nuovo-progetto, oppure scrivi il file a mano."
  exit 1
fi

command -v jq >/dev/null || { echo "NON VERIFICABILE: manca jq"; exit 1; }

RILEVATO=$(jq -r '.rilevato_il // empty' "$F")
if [ -z "$RILEVATO" ]; then
  echo "NON VERIFICABILE: $F non riporta la data del rilevamento"
  exit 1
fi

GIORNI=$(( ( $(date +%s) - $(date -d "$RILEVATO" +%s 2>/dev/null || echo 0) ) / 86400 ))
if [ "$GIORNI" -gt "$SCADENZA_GIORNI" ]; then
  echo "SCADUTO: rilevamento del $RILEVATO, $GIORNI giorni fa (limite $SCADENZA_GIORNI)."
  echo "  Le region cambiano. Riverifica prima di dichiararle in un contratto."
  exit 1
fi

# Una region e' europea se comincia per eu- o europe-, o e' fra le sigle note.
eu() {
  case "$1" in
    eu-*|europe-*|fra1|cdg1|dub1|arn1|zrh1|lhr1|mad1|par1|ams*) return 0 ;;
    *) return 1 ;;
  esac
}

ESITO=0
echo "Rilevamento del $RILEVATO ($GIORNI giorni fa)"
echo
while IFS=$'\t' read -r ruolo servizio region; do
  [ -z "$servizio" ] && continue
  if [ -z "$region" ] || [ "$region" = "null" ]; then
    printf '  %-10s %-12s region NON DICHIARATA\n' "$ruolo" "$servizio"; ESITO=1
  elif eu "$region"; then
    printf '  %-10s %-12s %s  UE\n' "$ruolo" "$servizio" "$region"
  else
    printf '  %-10s %-12s %s  FUORI UE\n' "$ruolo" "$servizio" "$region"; ESITO=1
  fi
done < <(jq -r '
  [ {r:"database", s:.database.servizio,  g:.database.region},
    {r:"hosting",  s:.hosting.servizio,   g:.hosting.region_funzioni} ]
  | .[] | [.r, .s, (.g // "null")] | @tsv' "$F")

echo
echo "Societa' terze con cui transitano dati personali (sede legale):"
jq -r '.servizi_terzi[]? | "  - \(.nome) — \(.sede) — \(.finalita)"' "$F"

echo
if [ "$ESITO" -eq 0 ]; then
  echo "ESITO: hosting in UE, verificato. Il DPA puo' dichiararlo."
else
  echo "ESITO: NON dichiarare hosting UE. Scrivi cosa risulta davvero."
fi
exit "$ESITO"
