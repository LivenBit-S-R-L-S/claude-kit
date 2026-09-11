---
name: memoria
description: Registra come lavoriamo in LivenBit quando emerge una preferenza, e trasforma le preferenze ricorrenti in modifiche alle skill del kit. Attivati da solo quando qualcuno corregge l'output di una skill, rifiuta un default, o dice come vuole che si lavori d'ora in avanti ("da ora in poi", "sempre", "mai", "non cosi'"). Usala anche quando ti viene chiesto di consolidare o rivedere le regole imparate.
---

Il kit migliora solo se le correzioni smettono di sparire a fine sessione. Tu sei il posto dove restano.

Hai due compiti. Capisci quale prima di muoverti:

- **Cattura** — sei in un progetto qualsiasi e hai appena visto emergere una preferenza. Sezione 1, poi fermati.
- **Consolidamento** — ti è stato chiesto di aggiornare le skill con quello che è stato imparato. Sezione 2.

## 1. Cattura

Registri solo se l'osservazione supera la soglia. Nel dubbio non registri: un diario pieno di rumore è peggio di un diario vuoto, perché nessuno lo rilegge.

**Registra quando:**
- qualcuno dice "da ora in poi", "sempre", "mai", "non così", "la prossima volta";
- un output di una skill viene riscritto a mano e la riscrittura cambia una regola, non una parola;
- un default del kit viene rifiutato.

**Non registrare:**
- i fatti di un singolo cliente — nomi, cifre, scadenze, scelte di piano. Quelli stanno nel preventivo e nel contratto, non qui;
- le correzioni di forma o di battitura;
- le decisioni prese una volta per un caso particolare, dichiarate tali.

**Mai** far finire nel diario credenziali, chiavi o dati personali di un cliente. Il diario contiene regole di lavoro, non materiale di progetto. Lo script rifiuta le credenziali che riconosce, ma non può riconoscere il nome di una persona: quello tocca a te.

Registra con una riga sola:

```
livenbit-ricorda --skill <preventivo|contratto|nuovo-progetto|security-review|generale> \
  --tipo <preferenza|correzione|rifiuto> \
  --osservazione "<la regola, all'imperativo, una frase>" \
  --citazione "<le parole esatte di chi l'ha detta>"
```

L'osservazione va scritta come istruzione eseguibile, non come cronaca. "Elenca almeno sette esclusioni" si può applicare a una skill; "al cliente non piacevano le esclusioni" no.

La citazione non è ornamento. Al momento del consolidamento è l'unica prova che quella regola l'ha voluta una persona e non l'hai dedotta tu da sola.

Se la regola c'è già, lo script incrementa il contatore invece di duplicarla. È la ripetizione che distingue una preferenza da uno sfogo.

Poi dillo in una riga: cosa hai registrato. Niente riepiloghi, niente conferme cerimoniose — chi sta lavorando è nel mezzo di altro.

## 2. Consolidamento

Questo passo modifica i file del kit, quindi si fa **solo dentro un clone di `claude-kit`**. Se non ci sei, dillo e fermati: il plugin installato viene ri-clonato a ogni `marketplace update`, e qualsiasi modifica fatta lì sparirebbe al primo aggiornamento.

Verifica dove sei:

```
git remote -v && ls plugins/livenbit/skills
```

Poi leggi `${CLAUDE_PLUGIN_ROOT}/skills/memoria/consolidamento.md` e segui quella procedura. Non improvvisare: tocca prezzi e clausole contrattuali.
