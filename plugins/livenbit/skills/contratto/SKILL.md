---
name: contratto
description: Genera il contratto di sviluppo LivenBit e l'allegato sul trattamento dati, partendo dal preventivo gia' prodotto. Usalo quando il cliente ha accettato e serve il documento da firmare.
disable-model-invocation: true
---

Genera il contratto per: $ARGUMENTS

Il contratto sta a valle del preventivo, non in parallelo. Perimetro, esclusioni, prezzo e milestone li prendi da li', non li reinventi: se contratto e preventivo dicono cose diverse sullo stesso lavoro, il problema nasce alla prima contestazione.

## 1. Raccogli i fatti, non le impressioni

Leggi il preventivo piu' recente in `preventivi/`. Se non ce n'e' nessuno, fermati e dillo: senza preventivo non si scrive un contratto, si scrive un tema.

Esegui `bash "${CLAUDE_PLUGIN_ROOT}"/scripts/check-infra.sh` nella radice del progetto. L'esito decide cosa puo' dichiarare l'Allegato B, e non e' negoziabile:
- esce 0: dichiara l'hosting in UE, con le region che il comando ha stampato;
- esce diverso da 0: **non scrivere che i dati stanno in UE**. Riporta quello che risulta davvero, e avvisa l'utente in cima alla tua risposta finale prima di consegnare il documento.

Un contratto che dichiara il falso sulla localizzazione dei dati e' peggio di un contratto che ammette di non saperlo.

## 2. Chiedi solo cio' che manca

Con AskUserQuestion, e solo se il dato non e' gia' nel preventivo o in `.claude/infra.json`:
- ripartizione dei pagamenti (proponi 40% alla firma e 60% alla consegna, ma chiedila sempre: cambia da cliente a cliente);
- entro quanti giorni il cliente deve fornire contenuti, accessi e riscontri;
- categorie di interessati e di dati personali trattati.

Non chiedere altro. Il resto e' politica LivenBit ed e' scritta qui sotto.

## 3. Scrivi il contratto

Struttura, in quest'ordine:

1. **Parti** — LivenBit SRLS e il cliente, con dati identificativi.
2. **Premesse** — il preventivo e' parte integrante e si allega.
3. **Oggetto e perimetro** — lo scope del preventivo, in punti verificabili.
4. **Esclusioni** — le esclusioni esplicite del preventivo, per intero.
5. **Corrispettivo** — importo, ripartizione concordata, fattura a 30 giorni data fattura.
6. **Tempi** — le fasi del preventivo diventano date, decorrenti dalla firma e dall'acconto.
7. **Obblighi del cliente** — contenuti, accessi e riscontri entro i termini emersi. Decorso il termine le scadenze slittano di pari durata: e' la clausola che salva i progetti fermi in attesa dei testi del cliente.
8. **Varianti di perimetro** — ogni richiesta fuori dallo scope genera un nuovo preventivo, anche per interventi di due ore.
9. **Proprieta' intellettuale** — il codice resta di LivenBit; al cliente e' concessa licenza d'uso. La cessione della proprieta' e' possibile solo a pagamento separato e a prezzo pieno.
10. **Riservatezza** — reciproca, oltre la cessazione.
11. **Trattamento dati personali** — rinvio all'Allegato B.
12. **Garanzia** — sei mesi dalla consegna, sui soli difetti di conformita' rispetto a quanto pattuito. Non copre richieste nuove, che restano varianti di perimetro. Decorsa la garanzia, ogni intervento e' oggetto di preventivo separato. Non nominare tariffe orarie: il meccanismo si', il prezzo no.
13. **Responsabilita'** — su due livelli, in quest'ordine: in via principale l'unico rimedio e' che LivenBit elimini il difetto a proprie spese, senza obbligo risarcitorio; in via subordinata, ove un risarcimento fosse comunque dovuto, e' limitato a quanto il cliente ha corrisposto nei dodici mesi precedenti. Il secondo livello esiste perche' se il primo viene ritenuto inefficace non resti responsabilita' illimitata. Marca la clausola come da confermare con un legale.
14. **Recesso e risoluzione** — preavviso scritto; sospensione del servizio per morosita' previo sollecito; effetti sui dati per rinvio all'Allegato B.
15. **Rinvio** — per quanto non previsto, legge italiana. **Nessuna clausola sul foro competente**: valgono le regole ordinarie.
16. **Approvazione specifica ex artt. 1341 e 1342 c.c.** — secondo blocco firme che richiama per numero le clausole 8, 12, 13 e 14. Senza questa seconda sottoscrizione quelle clausole non producono effetto: non ometterla mai.

## 4. Scrivi l'Allegato B — trattamento dati

Cliente titolare, LivenBit responsabile ex art. 28 GDPR. Contiene:

- oggetto, durata, natura e finalita' del trattamento, ricavati dal progetto;
- categorie di interessati e di dati, dall'intervista;
- **sub-responsabili**, uno per riga, con sede legale della societa' e finalita': prendili da `.claude/infra.json`. Il cliente li autorizza firmando, e va avvisato prima di ogni sostituzione;
- **trasferimenti extra-UE**: dichiarali, non negarli. Netlify, Stripe e Resend sono societa' statunitensi: i dati transitano da loro anche quando l'hosting e' europeo. Un allegato che nega i trasferimenti perde credibilita' su tutto il resto al primo controllo;
- misure di sicurezza effettive del progetto: RLS attiva, cifratura in transito e a riposo, gestione degli accessi, registrazione degli eventi;
- **violazioni**: comunicazione al titolare senza ingiustificato ritardo e comunque entro 24 ore dalla conoscenza;
- **fine del rapporto**: il cliente sceglie fra cancellazione integrale e restituzione entro 30 giorni dalla cessazione. In assenza di scelta, cancellazione decorsi 60 giorni previo sollecito scritto. La restituzione comprende export della banca dati in formato aperto, trasferimento della titolarita' del repository ed elenco delle variabili d'ambiente. Ogni attivita' ulteriore, fra cui ricostruzione dell'ambiente presso terzi, migrazione assistita e affiancamento a fornitori subentranti, e' oggetto di preventivo separato;
- diritto del titolare di chiedere evidenze sul rispetto degli obblighi.

## 5. Consegna

Scrivi `contratti/<slug>-<AAAA-MM-GG>.md`, poi convertilo:

    python3 "${CLAUDE_PLUGIN_ROOT}"/scripts/md-to-docx.py contratti/<file>.md contratti/<file>.docx

Chiudi elencando: il percorso dei due file, i punti che hai dovuto assumere, e in modo esplicito **le clausole da far verificare a un legale la prima volta** — la 13 e il blocco delle approvazioni specifiche su tutte. Se `check-infra.sh` non e' uscito 0, dillo come prima riga della risposta.
