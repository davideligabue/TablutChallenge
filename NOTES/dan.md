# Euristica:

non c'è molto da poter cambiare alle variabili (bisognerebbe studarsi un pò il tablut e poi e poi) che valutano e successivaente classificano diverse posizioni.
Di seguito quelle attualmente presenti:
    per il bianco:
        - distanza del re dall'uscita più vicina; | da rivedere?
        - quanto bene il re è protetto da pedine bianche; | peso medio?
        - quanto il re è in pericolo (quante pedine nere ha intorno); | peso medio?
    per il nero:
        - distanza del re dall'uscita più vicina; | da rivedere?
        - quando bene il re è circondato da pedine nere; | peso alto
        - quante uscite ('scappatoie', movimenti) libere ha il re. (molto importante secand me) | peso alto

Si potrebbe aggiungere:
    per il bianco:
        - potenziali pezzi catturabili; | peso medio
        - potenziali pezzi in presa; | peso basso
        - liberà di movimento dei propri pezzi; | peso molto basso ?conviene?
        - più punteggio per arrivare a celle 'evidenziate' | peso medio-alto
        - cercare di occupare posizioni del rombo | peso medio-alto
        

    per il nero:
        - potenziali pezzi catturabili;
        - potenziali pezzi in presa;
        - liberà di movimento dei propri pezzi;
        - la formazione di uno dei rombi (varie dimensioni) vale tanto



Comunque, bianco o nero che sia, in generale le variabili (gli indicatori) sono sempre:
    1. accerchiamento
    2. righe e colonne libere
    3. scacco al re (accostamento pedina al re)

Quello su cui si può e si deve lavorare sono i pesi della funzione che bilanciano le diverse variabili, come deciderli?

## ALGORITMO GENETICO!

Mi spiego meglio. Per avere delle idee di mosse 'buone' e mosse 'cattive' sarà fondamentale il dataset (esempio banale ma non scontato: la mossa prima della mossa vincente è sempre buona), quindi il dataset andrà anche ampliato, parecchio, anche con partite giocate con sole mosse random, più sarà grande, più sarà affidabile. (nota_pelle: secondo me le mosse random rappresentano noise)
Sucessivamente si crea una popolazione di valutazioni (ovvero di considerazioni su una data posizione) che hanno come uniche caratteristiche, cioè come geni, i pesi rispetto alle diverse variabili, supponiamo essi vadano da 0 a 1.
Quindi si iniziano ad accoppiare ecc... (Importante inserire anche mutazioni, crossover per non arrivare a soluzioni sub-ottimali e per cercare di arrivare il più vicino possibile alla soluzione anche se è vicino ai due estremi). Accoppiando due valutazioni (genitori) il figlio avrà come geni (pesi) la media esatta di quelle dei genitori.
Così facendo si sceglie poi la valutazione che porterebbe a scegliere le mosse corrette, copiandone quindi i pesi nella nostra euristica.
Tutto questo è un'operazione da fare chiaramente prima del torneo, prima di lanciare il codice, una volta trovati dei buoni pesi, quelli sono e basta.

Molto più importante posizione re che pedine prese, in ambo i casi.

Per guidare algoritmo genetico (?):
    - buone mosse per il bianco:
        - la pedina si accosta al Re occupando la linea di una pedina Nera
        - la pedina si accosta ad una pedina bianca
        - la pedina si accosta a più di una pedina bianca
    - buone mosse per il nero:
        - la pedina si accosta al Re
        - la pedina si accosta ad una pedina bianca il cui lato opposto è occupato
        - la pedina si accosta a più di una pedina bianca
        - Quarta pedina adiacente al Re nel castello (VITTORIA)
        - Terza pedina adiacente al Re se adiacente al castello (VITTORIA)
        - Seconda pedina adiacente al Re contando anche un campo (VITTORIA)
        - Se il nero vede il re scoperto, è saggio muovercisi di fianco

oppure all'opposto:
    - cattive mosse per il bianco:
        - Bianco non deve lasciare re scoperto muovendosi
        - Meglio muovere il re solo quando c'è un basso numero di neri
        - Avere una pedina avversaria adiacente mette a rischio
    - cattive mosse per il nero:
        - la pedina sblocca una via d'uscita per il Re
        - la pedina sblocca una via d'uscita per una pedina Bianca
        - Avere una pedina avversaria adiacente mette a rischio

# Algoritmo di ricerca:

max-min con alpha-beta cuts, non vedo molte altre alternative.

All chess programs consult the library of openings (there are openings that have been previously fully explored and that can affect the entire game) --> Possiamo creare una piccola libreria che contiene delle aperture così che ad inizio gioco si prova a seguire quelle(?) (chiaramente quelle che ci portano a vincere in più partite). (nota_pelle: può avere senso, si possono considerare le prime N mosse vincenti del dataset)


