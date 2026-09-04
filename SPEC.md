# SPEC — LivenBit Claude Kit

Questo file è la specifica completa. Crea ogni file esattamente come indicato,
con il percorso indicato. Non aggiungere file, campi o componenti non elencati
qui. Non modificare i contenuti: se qualcosa ti sembra sbagliato, fermati e
chiedi conferma invece di correggere in autonomia.

Tutti i file di testo devono avere terminatori di riga LF, mai CRLF.

## Struttura da creare

claude-kit/
  .gitattributes
  .gitignore
  README.md
  SPEC.md                          (esiste già, non toccarlo)
  .claude-plugin/
    marketplace.json
  plugins/
    livenbit/
      .claude-plugin/
        plugin.json
      hooks/
        hooks.json
      scripts/
        no-secrets.sh              (eseguibile)
        typecheck.sh               (eseguibile)
      agents/
        security-review.md
      skills/
        preventivo/
          SKILL.md
        nuovo-progetto/
          SKILL.md
      bin/
        livenbit-new               (eseguibile)


=== FILE: .gitattributes ===
* text=auto eol=lf
*.sh text eol=lf
bin/* text eol=lf
*.png binary
*.jpg binary
*.jpeg binary
*.ico binary
=== END FILE ===


=== FILE: .gitignore ===
node_modules/
.DS_Store
Thumbs.db
*.log
.env
.env.local
=== END FILE ===


=== FILE: README.md ===
# LivenBit Claude Kit

Standard di sviluppo LivenBit distribuiti come plugin Claude Code.

Contiene:
- blocco delle credenziali in chiaro e typecheck automatico (hook)
- agent di review sicurezza da invocare prima di ogni PR
- skill per preventivi e per la personalizzazione di un progetto nuovo
- comando `livenbit-new` per creare un progetto cliente da repo template

## Installazione

    claude plugin marketplace add livenbit/claude-kit
    claude plugin install livenbit@livenbit-kit

Installare sempre a scope utente (il default). Mai `--scope project`: il
riferimento a questo marketplace privato finirebbe committato nel repo del
cliente.

Proprietà di LivenBit SRLS. Uso interno.
=== END FILE ===


=== FILE: .claude-plugin/marketplace.json ===
{
  "name": "livenbit-kit",
  "owner": {
    "name": "LivenBit SRLS"
  },
  "metadata": {
    "description": "Standard di sviluppo e workflow commerciali LivenBit",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "livenbit",
      "description": "Hook di sicurezza, skill commerciali e review agent per progetti LivenBit",
      "source": "./plugins/livenbit",
      "category": "development"
    }
  ]
}
=== END FILE ===


=== FILE: plugins/livenbit/.claude-plugin/plugin.json ===
{
  "name": "livenbit",
  "displayName": "LivenBit Standards",
  "description": "Standard tecnici e commerciali LivenBit: blocco credenziali, review sicurezza, preventivi, scaffold progetti.",
  "author": { "name": "LivenBit SRLS" },
  "license": "UNLICENSED"
}

NOTA: il campo "version" è assente di proposito. Senza di esso la versione
viene derivata dal commit SHA e ogni push arriva agli aggiornamenti. Non
aggiungerlo.

Conseguenza: `claude plugin validate --strict` esce 1 con il warning
"version: No version specified". È atteso. Se un giorno il kit verrà
distribuito fuori da LivenBit, si aggiunge `version` e si passa a --strict.
=== END FILE ===


=== FILE: plugins/livenbit/hooks/hooks.json ===
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/no-secrets.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/typecheck.sh"
          }
        ]
      }
    ]
  }
}
=== END FILE ===


=== FILE: plugins/livenbit/scripts/no-secrets.sh ===
#!/bin/bash
# Blocca la scrittura di credenziali in chiaro e la modifica di file sensibili.
# Uscita 2 = azione bloccata, stderr torna a Claude come feedback.

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
BODY=$(echo "$INPUT" | jq -r '.tool_input.content // .tool_input.new_string // empty')

# Normalizza i separatori di percorso in stile Windows
FILE="${FILE//\\//}"

case "$FILE" in
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

if echo "$BODY" | grep -qE "$PATTERNS"; then
  echo "Blocked: credenziale in chiaro rilevata in $FILE. Se è reale ruotala subito, poi leggila da process.env." >&2
  exit 2
fi

exit 0
=== END FILE ===


=== FILE: plugins/livenbit/scripts/typecheck.sh ===
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

OUT=$(npx --no-install tsc --noEmit 2>&1)
if [ $? -ne 0 ]; then
  echo "$OUT" | head -20 >&2
  exit 2
fi

exit 0
=== END FILE ===


=== FILE: plugins/livenbit/agents/security-review.md ===
---
name: security-review
description: Rivede un diff prima del commit cercando violazioni degli standard LivenBit. Invocalo prima di ogni PR o quando l'utente chiede una review di sicurezza.
model: opus
tools: Read, Grep, Glob, Bash
maxTurns: 25
---

Sei un revisore senior. Esamini solo il diff, non riscrivi codice.

Cerca, in quest'ordine di gravità:

1. Credenziali, chiavi, token o URL con secret nel codice, nei commenti, nei log o nei file di test. Se ne trovi uno, la prima parola della tua risposta è "ruotala".
2. Tabelle Supabase con dati utente senza policy RLS attiva, o query client su dati sensibili senza policy corrispondente.
3. Endpoint di pagamento senza verifica della firma webhook, senza chiave di idempotenza, o senza riconciliazione.
4. Chiamate di rete o di pagamento senza gestione errori esplicita, e componenti senza stato di loading ed errore.
5. `any` non giustificato, `@ts-ignore`, `!` non necessari.
6. Modifiche allo schema DB fuori da una migrazione versionata.
7. Dati personali raccolti senza base giuridica o minimizzazione evidente.

Formato: solo ciò che è rotto, insicuro o caro da mantenere, ordinato per gravità, con file e riga. Salta lo stile. Se una categoria è pulita, non scriverla.

Segnala se una finding riguarda codice che potrebbe diventare modulo riutilizzabile su altri clienti.
=== END FILE ===


=== FILE: plugins/livenbit/skills/preventivo/SKILL.md ===
---
name: preventivo
description: Produce un preventivo LivenBit completo di scope, esclusioni, ore per fase, prezzo, ricorrente e rischi. Usalo quando serve quotare un lavoro nuovo o una variazione.
disable-model-invocation: true
---

Prepara un preventivo per: $ARGUMENTS

Se mancano dati che cambiano il prezzo, fai UNA domanda sola. Altrimenti assumi e dichiara l'assunzione in una riga.

Struttura obbligatoria:

**Scope** — cosa è incluso, in punti verificabili. Niente aggettivi.

**Esclusioni esplicite** — cosa non è incluso. Almeno cinque voci. Contenuti e testi, migrazione dati da sistemi esistenti, integrazioni con software terzi non nominati, formazione, SEO, grafica originale se non citata.

**Ore per fase** — analisi, setup, sviluppo, test, deploy, consegna. Ore realistiche, non ottimistiche.

**Prezzo** — ore per tariffa. Acconto all'ordine e milestone di pagamento, sempre.

**Canone ricorrente mensile** — hosting, manutenzione, assistenza. Se non c'è, scrivi la ragione esplicita per cui non c'è.

**Costi infrastruttura mensili** — Supabase, Vercel o Netlify, Stripe, dominio, email. Cifre stimate con margine d'errore.

**Rischi che fanno esplodere le ore** — dipendenze dal cliente, API terze non documentate, contenuti in ritardo, cambi di scope.

Chiudi con: verifica margine. Ore per costo orario interno contro il prezzo. Se il margine è sotto soglia, dillo nella prima riga del blocco.

Clausole da riportare in ogni bozza contrattuale:
- Il codice prodotto resta di proprietà di LivenBit. Al cliente è concessa licenza d'uso. La cessione della proprietà intellettuale è possibile solo a pagamento separato e a prezzo pieno.
- Ogni richiesta fuori dallo scope elencato genera un nuovo preventivo, anche per interventi di due ore.
- Il GDPR è una voce di costo del progetto: informativa, base giuridica, minimizzazione, registro trattamenti.
=== END FILE ===


=== FILE: plugins/livenbit/skills/nuovo-progetto/SKILL.md ===
---
name: nuovo-progetto
description: Personalizza un progetto appena creato con livenbit-new sul dominio del cliente. Genera schema DB, policy RLS, rotte e CLAUDE.md di progetto. Usalo subito dopo lo scaffold, mai su un progetto già avviato.
disable-model-invocation: true
---

Il progetto è già in piedi: stack, dipendenze, layout e config esistono. Non rigenerarli, non ricreare file che ci sono già.

Il tuo compito è solo la parte che dipende dal cliente.

## 1. Intervista
Usa AskUserQuestion. Non fare domande la cui risposta è già nel repo. Copri solo:
- entità del dominio e loro relazioni;
- chi accede a cosa: ruoli, e per ciascuno quali righe deve vedere;
- se servono pagamenti, e se sono incassi diretti o split fra più soggetti;
- quali dati personali vengono raccolti e per quale finalità.

Fermati quando hai abbastanza per scrivere lo schema. Non oltre.

## 2. Scrivi lo schema
Una migrazione versionata in `supabase/migrations/`, mai modifiche a mano.
Per ogni tabella con dati utente: abilita la Row Level Security e scrivi le policy select, insert, update e delete che corrispondono ai ruoli emersi dall'intervista. Una tabella con dati utente e senza policy è un errore, non un TODO.
Genera i tipi TypeScript dallo schema.

## 3. Aggiorna le regole di progetto
Scrivi `.claude/rules/dominio.md` nel repo con: entità, ruoli, chi vede cosa. Sotto le 60 righe.
Aggiorna il `CLAUDE.md` del repo con il nome del cliente, le entità e i comandi specifici. Non ripetere ciò che è già scritto nelle regole.

## 4. Chiudi
Elenca: cosa hai creato, cosa resta da fare a mano, quali variabili d'ambiente vanno compilate.
Segnala esplicitamente ogni funzione che può diventare modulo riutilizzabile su altri clienti, prima che venga scritta su misura.

Non aggiungere funzionalità non richieste. Non installare dipendenze non necessarie allo schema.
=== END FILE ===


=== FILE: plugins/livenbit/bin/livenbit-new ===
#!/usr/bin/env bash
# Crea un progetto cliente da un repo template GitHub e sostituisce i placeholder.
set -euo pipefail

OWNER="livenbit"
TEMPLATE="livenbit/template-saas"
CLIENT=""
SLUG=""
VISIBILITY="--private"

usage() {
  cat <<'EOF'
livenbit-new <slug> --client "Nome Cliente" [--template <repo>] [--public]

  <slug>       nome repo/progetto, kebab-case (es. rossi-gestionale)
  --client     ragione sociale del cliente, usata in README e CLAUDE.md
  --template   repo template da usare (default: livenbit/template-saas)
  --public     crea il repo pubblico (default: privato)

Crea il repo da template, clona, sostituisce i placeholder, primo commit.
Non scrive nessuna credenziale: genera .env.local con i soli nomi delle variabili.
EOF
}

[ $# -ge 1 ] || { usage; exit 1; }
SLUG="$1"; shift

while [ $# -gt 0 ]; do
  case "$1" in
    --client)   CLIENT="${2:-}"; shift 2 ;;
    --template) TEMPLATE="${2:-}"; shift 2 ;;
    --public)   VISIBILITY="--public"; shift ;;
    -h|--help)  usage; exit 0 ;;
    *) echo "Argomento sconosciuto: $1" >&2; usage; exit 1 ;;
  esac
done

[ -n "$CLIENT" ] || { echo "Manca --client" >&2; exit 1; }

if ! echo "$SLUG" | grep -qE '^[a-z][a-z0-9]*(-[a-z0-9]+)*$'; then
  echo "Slug non valido: '$SLUG'. Usa kebab-case minuscolo." >&2
  exit 1
fi

for cmd in gh git perl; do
  command -v "$cmd" >/dev/null || { echo "Manca $cmd nel PATH" >&2; exit 1; }
done

gh auth status >/dev/null 2>&1 || { echo "gh non autenticato. Esegui: gh auth login" >&2; exit 1; }

DEST="${LIVENBIT_PROJECTS_DIR:-$HOME/dev}/$SLUG"
[ -e "$DEST" ] && { echo "Esiste già: $DEST" >&2; exit 1; }

echo "-> creo $OWNER/$SLUG da $TEMPLATE"
gh repo create "$OWNER/$SLUG" --template "$TEMPLATE" $VISIBILITY >/dev/null

echo "-> clono in $DEST"
for attempt in 1 2 3 4 5; do
  if gh repo clone "$OWNER/$SLUG" "$DEST" >/dev/null 2>&1; then break; fi
  sleep 3
done
[ -d "$DEST/.git" ] || { echo "Clone fallito. Il repo è stato creato: clonalo a mano." >&2; exit 1; }

cd "$DEST"

TITLE=$(echo "$SLUG" | perl -pe 's/(^|-)(\w)/($1 ? " " : "") . uc($2)/ge')

git ls-files -z | xargs -0 perl -pi \
  -e "s/__PROJECT_SLUG__/$SLUG/g;" \
  -e "s/__PROJECT_NAME__/$TITLE/g;" \
  -e "s/__CLIENT_NAME__/\Q$CLIENT\E/g;"

for f in $(git ls-files | grep -E '(^|/)__PROJECT_SLUG__' || true); do
  git mv "$f" "$(echo "$f" | sed "s/__PROJECT_SLUG__/$SLUG/g")"
done

if [ -f .env.example ]; then
  grep -oE '^[A-Z_]+=' .env.example > .env.local
  echo "-> .env.local generato con i soli nomi delle variabili. Compilalo a mano."
fi

git add -A
git commit -q -m "scaffold LivenBit: $TITLE per $CLIENT" || true
git push -q origin HEAD

echo "OK: $DEST"
echo "   Prossimo: apri il progetto e lancia /livenbit:nuovo-progetto"
=== END FILE ===


## Definition of done

Il lavoro è finito quando:
- tutti i file sopra esistono ai percorsi indicati, con contenuto identico;
- no-secrets.sh, typecheck.sh e livenbit-new hanno il permesso di esecuzione,
  e `git ls-files -s` riporta modo 100755 per tutti e tre;
- `claude plugin validate ./plugins/livenbit` esce 0 (senza --strict);
- l'unico warning ammesso è l'assenza di `version`, che è voluta: senza
  quel campo la versione deriva dal commit SHA e ogni push arriva agli
  aggiornamenti. Non usare --strict su questo plugin finché resta interno.
- `claude plugin validate .` esce 0;
- no-secrets.sh esce 2 su una finta chiave sk_live_ e su un percorso .env,
  ed esce 0 su contenuto pulito;
- livenbit-new esce 1 con messaggio d'errore se invocato senza --client;
- il branch è pushato.

Il repo template `livenbit/template-saas` non esiste ancora: livenbit-new
fallirà finché non verrà creato. È previsto e non è un errore da correggere qui.
