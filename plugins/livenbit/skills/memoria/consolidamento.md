# Consolidamento: dal diario alle skill

Trasformare osservazioni in modifiche al kit. Si fa dentro un clone di
`claude-kit`, mai sul plugin installato.

## 1. Leggi cosa c'è

```
livenbit-ricorda --da-valutare
```

Se il diario è vuoto, dillo e fermati. Non inventare regole plausibili: una
skill modificata su una preferenza mai espressa è peggio della skill di
partenza, perché nessuno sa da dove viene.

## 2. Decidi cosa merita una modifica

Promuovi a modifica una regola solo se vale almeno una di queste:

- **tre occorrenze o più** — è un modo di lavorare, non un caso isolato;
- **una sola occorrenza, ma esplicita e generale** — la citazione contiene
  "sempre", "mai", "da ora in poi". Chi parla così sta dettando una regola,
  non commentando un output.

Tutto il resto resta nel diario. Non è scartato: aspetta di ripetersi.

Se due regole si contraddicono, non scegliere tu. Portale entrambe alla
persona con le rispettive citazioni e le date: quasi sempre è cambiata
un'intenzione nel frattempo, e solo lei sa quale delle due vale.

## 3. Trova il punto giusto da toccare

| Cosa riguarda la regola | File |
|---|---|
| struttura, voci, esclusioni del preventivo | `skills/preventivo/SKILL.md` |
| clausole, allegati, intervista del contratto | `skills/contratto/SKILL.md` |
| prezzi e contenuto dei piani di gestione | `skills/contratto/piani.md` |
| scaffold e personalizzazione iniziale | `skills/nuovo-progetto/SKILL.md` |
| cosa la review di sicurezza deve guardare | `agents/security-review.md` |
| pattern di credenziali da bloccare | `scripts/no-secrets.sh` |
| regole trasversali a tutto il kit | la skill che le usa, non un file nuovo |

Modifica il testo esistente. Non aggiungere una sezione "Regole apprese" in
fondo: dopo sei mesi la skill avrebbe due parti che si contraddicono e
vincerebbe quella che il modello legge per ultima.

Ogni skill ha un costo in token pagato a ogni invocazione. Se la modifica
allunga il file di più di qualche riga, taglia altrove: sostituire una regola
vaga con una precisa è quasi sempre possibile a parità di lunghezza.

## 4. Chiedi prima di scrivere

Presenta ogni modifica come diff, con accanto la citazione che la giustifica.
Usa `AskUserQuestion`: una domanda per modifica, approvata o scartata
singolarmente. Non un blocco unico da prendere o lasciare.

**Non modificare mai senza approvazione esplicita e nominale:**

- i prezzi in `piani.md`;
- le clausole di responsabilità, garanzia, proprietà intellettuale e recesso
  in `contratto/SKILL.md`;
- l'elenco dell'art. 1341 c.c. — se una modifica aggiunge o cambia una
  clausola vessatoria, quell'elenco va aggiornato di conseguenza, e la cosa
  va detta ad alta voce perché una clausola vessatoria non richiamata lì
  è inefficace;
- i pattern in `no-secrets.sh`, se la modifica ne **toglie** uno.

Per queste, "l'ha chiesto tre volte" non basta. Serve un sì detto adesso,
su quella riga.

## 5. Applica e verifica

Dopo ogni approvazione:

```
claude plugin validate ./plugins/livenbit ; echo "exit=$?"
```

Deve uscire 0. L'avvertimento sul campo `version` mancante è atteso e va
ignorato: la versione del plugin è il commit.

Se hai toccato uno script, eseguilo almeno una volta sul caso che la regola
descrive. Una skill sbagliata produce un documento da correggere; uno script
sbagliato blocca il lavoro di tutti.

## 6. Chiudi il giro

```
git checkout -b memoria/<argomento-in-due-parole>
git add -A && git commit
livenbit-ricorda --segna-consolidata "<osservazione esatta>"
```

Commit sul branch, mai su `main` diretto: le modifiche al kit passano da una
PR come tutto il resto, così qualcuno le legge prima che finiscano nel
plugin di tutti.

Segna consolidata solo **dopo** che la modifica è nel commit. Se quella
regola riemergerà, lo script la rimetterà da sola tra quelle da valutare —
ed è il segnale che la modifica non aveva risolto il problema.

Chiudi dicendo, in tre righe: quali regole sono diventate modifiche, quali
restano in attesa di ripetersi, e quali hai portato alla persona senza
decidere tu.
