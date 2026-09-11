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

## Consegna

Scrivi il preventivo in `preventivi/<slug>-<AAAA-MM-GG>.md` dentro il repo del progetto, oltre a mostrarlo in risposta. Non e' burocrazia: la skill `contratto` legge quel file, e cosi' quanto quotato e quanto firmato non possono divergere. Ti resta anche lo storico delle revisioni.

Clausole da riportare in ogni bozza contrattuale:
- Il codice prodotto resta di proprietà di LivenBit. Al cliente è concessa licenza d'uso. La cessione della proprietà intellettuale è possibile solo a pagamento separato e a prezzo pieno.
- Ogni richiesta fuori dallo scope elencato genera un nuovo preventivo, anche per interventi di due ore.
- Il GDPR è una voce di costo del progetto: informativa, base giuridica, minimizzazione, registro trattamenti.

Quando il cliente accetta, il contratto si genera con `/livenbit:contratto`.
