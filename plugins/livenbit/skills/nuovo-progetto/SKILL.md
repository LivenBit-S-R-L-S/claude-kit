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
