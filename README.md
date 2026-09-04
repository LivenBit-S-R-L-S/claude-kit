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
