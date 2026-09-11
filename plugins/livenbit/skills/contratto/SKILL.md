---
name: contratto
description: Genera il contratto di sviluppo LivenBit e l'allegato sul trattamento dati, partendo dal preventivo gia' prodotto. Usalo quando il cliente ha accettato e serve il documento da firmare.
disable-model-invocation: true
---

Genera il contratto per: $ARGUMENTS

Il contratto sta a valle del preventivo, non in parallelo. Perimetro, esclusioni, prezzo e milestone li prendi da li', non li reinventi: se contratto e preventivo dicono cose diverse sullo stesso lavoro, il problema nasce alla prima contestazione.

## 1. Raccogli i fatti, non le impressioni

Leggi il preventivo piu' recente in `preventivi/`. Se non ce n'e' nessuno, fermati e dillo: senza preventivo non si scrive un contratto, si scrive un tema.

Se il piano scelto e' il **1**, salta il controllo infrastrutturale: gli account sono del cliente, non c'e' nulla da verificare, e l'Allegato B va in versione ridotta (vedi sotto).

Negli altri piani esegui `bash "${CLAUDE_PLUGIN_ROOT}"/scripts/check-infra.sh` nella radice del progetto. L'esito decide cosa puo' dichiarare l'Allegato B, e non e' negoziabile:
- esce 0: dichiara l'hosting in UE, con le region che il comando ha stampato;
- esce diverso da 0: **non scrivere che i dati stanno in UE**. Riporta quello che risulta davvero, e avvisa l'utente in cima alla tua risposta finale prima di consegnare il documento.

Un contratto che dichiara il falso sulla localizzazione dei dati e' peggio di un contratto che ammette di non saperlo.

## 2. Chiedi il piano, poi solo cio' che manca

Leggi `piani.md`, nella stessa cartella di questo file: contiene il listino e la differenza di ruoli fra i piani. I prezzi prendili da li', non dalla memoria.

Con AskUserQuestion chiedi sempre, in quest'ordine:
- **quale piano di gestione ha scelto il cliente** (1, 2, 3 o 4). Da questa risposta dipendono clausole intere, non solo delle cifre;
- se il piano e' il 4, il canone concordato: il preventivo dedicato deve gia' riportarlo;
- l'intestazione del dominio: di norma LivenBit, salvo richiesta espressa del cliente di intestarselo;
- ripartizione dei pagamenti (proponi 40% alla firma e 60% alla consegna, ma chiedila sempre: cambia da cliente a cliente);
- entro quanti giorni il cliente deve fornire contenuti, accessi e riscontri;
- categorie di interessati e di dati personali trattati.

Non chiedere altro. Il resto e' politica LivenBit ed e' scritta qui sotto.

**Genera il contratto del piano scelto, non un testo con quattro ipotesi.** Un contratto che elenca alternative e' illeggibile e il cliente firma senza sapere cosa ha scelto. Il quadro completo dei piani sta nell'Allegato A, che serve proprio a rendere trasparente il confronto.

## 3. Scrivi il contratto

Struttura, in quest'ordine:

1. **Parti** — LivenBit SRLS e il cliente, con dati identificativi.
2. **Premesse** — il preventivo e' parte integrante e si allega.
3. **Oggetto e perimetro** — lo scope del preventivo, in punti verificabili.
4. **Esclusioni** — le esclusioni esplicite del preventivo, per intero.
5. **Corrispettivo** — tantum del piano scelto oltre IVA, ripartizione concordata, fattura a 30 giorni data fattura.
5-bis. **Canone di gestione** — solo per i piani 2, 3 e 4. Importo mensile del piano, oltre IVA. Durata minima dodici mesi dalla pubblicazione, rinnovo tacito di anno in anno salvo disdetta scritta con sessanta giorni di preavviso. Il mancato pagamento legittima la sospensione del servizio previo sollecito scritto. Nel **Piano 1** scrivi invece, esplicitamente, che non e' previsto alcun canone e che hosting e banca dati restano a carico del cliente.
5-ter. **Dominio** — fee annuale nella misura indicata in `piani.md`. Di norma il dominio e' registrato a nome di LivenBit, che lo amministra per conto del cliente; **a fine rapporto, su richiesta scritta del cliente e previo integrale pagamento di quanto dovuto, LivenBit ne trasferisce la titolarita' entro trenta giorni**. Se il cliente ha chiesto di esserne intestatario fin dall'inizio, scrivi che la titolarita' e' sua e che LivenBit si limita alla gestione tecnica, che cessa con il rapporto.
5-quater. **Limiti della piattaforma** — solo per i piani 2, 3 e 4. I servizi di hosting e banca dati sono erogati entro i limiti dei piani sottoscritti da LivenBit presso i fornitori. Al superamento LivenBit ne da' avviso scritto e propone il passaggio a un piano superiore o un preventivo dedicato; fino all'accettazione i costi eccedenti restano a carico del cliente. In tutti i piani il cliente e' informato per iscritto dei limiti tecnici prima della consegna.
6. **Tempi** — le fasi del preventivo diventano date, decorrenti dalla firma e dall'acconto.
7. **Obblighi del cliente** — contenuti, accessi e riscontri entro i termini emersi. Decorso il termine le scadenze slittano di pari durata: e' la clausola che salva i progetti fermi in attesa dei testi del cliente.
8. **Varianti di perimetro** — ogni richiesta fuori dallo scope genera un nuovo preventivo, anche per interventi di due ore.
9. **Proprieta' intellettuale** — il codice resta di LivenBit; al cliente e' concessa licenza d'uso. La cessione della proprieta' e' possibile solo a pagamento separato e a prezzo pieno.
10. **Riservatezza** — reciproca, oltre la cessazione.
11. **Trattamento dati personali** — rinvio all'Allegato B.
12. **Garanzia** — sei mesi dalla consegna, sui soli difetti di conformita' rispetto a quanto pattuito. Non copre in nessun caso disservizi imputabili alle piattaforme di terzi. Nel **Piano 1** precisalo ancora piu' nettamente: la garanzia riguarda il codice consegnato, mentre hosting e banca dati sono gestiti dal cliente e ogni disservizio che ne derivi e' fuori garanzia e fuori assistenza. Non copre richieste nuove, che restano varianti di perimetro. Decorsa la garanzia, ogni intervento e' oggetto di preventivo separato. Non nominare tariffe orarie: il meccanismo si', il prezzo no.
13. **Responsabilita'** — su due livelli, in quest'ordine: in via principale l'unico rimedio e' che LivenBit elimini il difetto a proprie spese, senza obbligo risarcitorio; in via subordinata, ove un risarcimento fosse comunque dovuto, e' limitato a quanto il cliente ha corrisposto nei dodici mesi precedenti. Il secondo livello esiste perche' se il primo viene ritenuto inefficace non resti responsabilita' illimitata. Marca la clausola come da confermare con un legale.
14. **Recesso e risoluzione** — preavviso scritto; sospensione del servizio per morosita' previo sollecito; effetti sui dati per rinvio all'Allegato B.
15. **Rinvio** — per quanto non previsto, legge italiana. **Nessuna clausola sul foro competente**: valgono le regole ordinarie.
16. **Approvazione specifica ex artt. 1341 e 1342 c.c.** — secondo blocco firme, separato da quello principale. Richiama per numero, come risultano nel documento che hai scritto, le clausole su: rinnovo tacito del canone e sospensione del servizio per mancato pagamento; addebito dei costi eccedenti i limiti di piattaforma; limiti della garanzia; responsabilita'; recesso e risoluzione. Indicale per contenuto e non fidarti di una numerazione fissa: cambia con il piano scelto. Senza questa seconda sottoscrizione quelle clausole non producono effetto, ed e' l'errore che rende inutili proprio le clausole che proteggono LivenBit: non ometterla mai.

## 4. Scrivi l'Allegato A — piano di gestione

Riporta la tabella dei quattro piani da `piani.md`, con evidenziato quello scelto, e sotto il dettaglio del solo piano prescelto: tipologia, tantum, canone, fee dominio, chi gestisce hosting e banca dati. Serve a rendere trasparente il confronto senza sporcare il corpo del contratto.

Per il **Piano 4**, riporta il canone concordato che hai ricevuto. Mai la dicitura "da definire": un contratto con un prezzo aperto non e' un contratto.

## 5. Scrivi l'Allegato B — trattamento dati

**Nei piani 2, 3 e 4** cliente titolare, LivenBit responsabile ex art. 28 GDPR, versione piena. Contiene:

- oggetto, durata, natura e finalita' del trattamento, ricavati dal progetto;
- categorie di interessati e di dati, dall'intervista;
- **sub-responsabili**, uno per riga, con sede legale della societa' e finalita': prendili da `.claude/infra.json`. Il cliente li autorizza firmando, e va avvisato prima di ogni sostituzione;
- **trasferimenti extra-UE**: dichiarali, non negarli. Netlify, Stripe e Resend sono societa' statunitensi: i dati transitano da loro anche quando l'hosting e' europeo. Un allegato che nega i trasferimenti perde credibilita' su tutto il resto al primo controllo;
- misure di sicurezza effettive del progetto: RLS attiva, cifratura in transito e a riposo, gestione degli accessi, registrazione degli eventi;
- **violazioni**: comunicazione al titolare senza ingiustificato ritardo e comunque entro 24 ore dalla conoscenza;
- **fine del rapporto**: il cliente sceglie fra cancellazione integrale e restituzione entro 30 giorni dalla cessazione. In assenza di scelta, cancellazione decorsi 60 giorni previo sollecito scritto. La restituzione comprende export della banca dati in formato aperto, trasferimento della titolarita' del repository ed elenco delle variabili d'ambiente. Ogni attivita' ulteriore, fra cui ricostruzione dell'ambiente presso terzi, migrazione assistita e affiancamento a fornitori subentranti, e' oggetto di preventivo separato;
- diritto del titolare di chiedere evidenze sul rispetto degli obblighi.

**Nel Piano 1** l'allegato va in versione ridotta, e la differenza non e' di dettaglio: gli account della piattaforma sono intestati al cliente, quindi alla consegna il trattamento passa a lui. Scrivi che il rapporto titolare-responsabile riguarda la sola fase di sviluppo e cessa con la consegna; che dopo la consegna LivenBit non tratta piu' dati personali per conto del cliente; che i fornitori della piattaforma diventano sub-responsabili del cliente, con cui e' lui a dover regolare il rapporto; e che **la localizzazione dei dati non e' garantita da LivenBit**, perche' dipende da account che non controlla. Non dichiarare region europee in questo caso: non hai modo di verificarle.

## 6. Consegna

Scrivi `contratti/<slug>-<AAAA-MM-GG>.md`, poi convertilo:

    python3 "${CLAUDE_PLUGIN_ROOT}"/scripts/md-to-docx.py contratti/<file>.md contratti/<file>.docx

Chiudi elencando: il percorso dei due file, i punti che hai dovuto assumere, e in modo esplicito **le clausole da far verificare a un legale la prima volta** — la 13 e il blocco delle approvazioni specifiche su tutte. Se `check-infra.sh` non e' uscito 0, dillo come prima riga della risposta. Nel Piano 1 di' invece, sempre in apertura, che la localizzazione dei dati non e' garantita perche' gli account sono del cliente.
