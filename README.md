# LivenBit Claude Kit

Standard di sviluppo LivenBit distribuiti come plugin Claude Code.

Contiene:
- blocco delle credenziali in chiaro e typecheck automatico (hook)
- agent di review sicurezza da invocare prima di ogni PR
- skill per preventivi, contratti e personalizzazione di un progetto nuovo
- comando `livenbit-new` per creare un progetto cliente da repo template

## Prerequisiti

- accesso all'organizzazione `livenbit` su GitHub: i repo sono privati
- `gh` installato e autenticato: `gh auth login`
- `git`, `perl` e Node 18 o superiore

## Installazione

    claude plugin marketplace add livenbit/claude-kit
    claude plugin install livenbit@livenbit-kit

Installare sempre a scope utente (il default). Mai `--scope project`: il
riferimento a questo marketplace privato finirebbe committato nel repo del
cliente.

Non serve aggiornare a mano: il plugin non dichiara una versione, quindi
ogni push su `main` arriva a tutti come aggiornamento.

## Uso

Nuovo progetto cliente, da dentro Claude Code:

    livenbit-new <slug> --client "Ragione Sociale S.r.l."

Lo scaffold crea il repo, sostituisce i placeholder e fa il primo push.
Tre cose restano da fare a mano, in quest'ordine:

    cd ~/dev/<slug>
    npm install                # senza questo l'hook typecheck non gira
    cp .env.example .env.local # poi compila i valori veri

Il progetto Supabase va creato dal dashboard: le skill scrivono le
migrazioni, non provisionano l'infrastruttura.

Poi, dentro il progetto:

    /livenbit:nuovo-progetto   # intervista, schema, policy RLS, regole
    /livenbit:preventivo       # preventivo completo, non tocca il codice
    /livenbit:contratto        # contratto + allegato dati, quando il cliente accetta

I tre comandi sono in sequenza: il preventivo si salva in `preventivi/`, il
contratto lo rilegge da li' e ne deriva perimetro, prezzo e milestone. Cosi'
quanto quotato e quanto firmato non divergono.

Il contratto esce in Markdown e in `.docx` pronto da mandare. La conversione
usa uno script del plugin che si appoggia alla sola libreria standard di
Python: nessuna dipendenza da installare.

## Dove stanno i dati

L'Allegato B sul trattamento dati non dichiara la localizzazione a memoria: la
legge da `.claude/infra.json`, scritto da `/livenbit:nuovo-progetto` con la
data del rilevamento. Se il file manca, ha piu' di sei mesi, o riporta una
region fuori dall'Unione, il contratto **non scrive che i dati stanno in UE**:
riporta cio' che risulta e te lo segnala.

Per controllarlo a mano, dentro un progetto:

    bash "$CLAUDE_PLUGIN_ROOT"/scripts/check-infra.sh .

Netlify, Stripe e Resend sono societa' statunitensi: i dati transitano da loro
anche con hosting europeo. L'allegato lo dichiara invece di negarlo.

Prima di ogni PR, chiedi a Claude una review di sicurezza: l'agent
`security-review` legge il diff e riporta solo ciò che è rotto.

La destinazione dei progetti è `~/dev`. Per cambiarla:

    export LIVENBIT_PROJECTS_DIR=~/progetti

## Template

`livenbit-new` parte da `livenbit/template-saas`. Quel repo deve avere la
spunta "Template repository" nelle Settings, altrimenti la creazione
fallisce. I placeholder ammessi sono `__PROJECT_SLUG__`, `__PROJECT_NAME__`
e `__CLIENT_NAME__`, e vanno usati nei contenuti dei file. Se servono in un
nome di file devono stare all'inizio; nei nomi di directory non vanno mai.

Proprietà di LivenBit SRLS. Uso interno.
