# Ottimizzazione classe Board

## Obiettivi:
1. Ottimizzare ricerca del Re: si può salvare la posizione senza cercarla ogni volta
2. Riorganizzare la sequenza di chiamate ai metodi delle mosse: fare un metodo generale per richiedere possibili mosse di un pezzo
3. Creare un metodo di Board che permetta di applicare una sequenza di mosse: è opportuno creare un metodo che data una lista di mosse, le applichi temporaneamente in sequenza (senza salvarle nello stato principale) e poi generi una lista di possibili mosse a partire da questa
4. Creare classe Mossa: creare una classe mossa che permetta di fare un check degli argomenti e che salvi in un unico oggetto le coordinate finali ed il tipo di pezzo mosso
5. Rendere la classe Node compatibile con le scelte sopra riportate
6. Aggiungi metodo a classe board che restituisce una lista di pezzi o punti di interesse presenti data una linea retta sulla griglia
7. Aggiungi metodo a classe Board che restituisce una lista di pezzi o punti di interesse presenti dato un anello di raggio n a partire da un centro sulla griglia

## Cose modificate:
- Aggiunta la classe Move: rappresenta una mossa, con una posizione iniziale e una finale e il colore del pezzo mosso. Il costrutture della classe svolge controlli solo sulla correttezza formale della mossa in sè, ovvero se è nei limiti della griglia e se è ortogonale, non fa controlli sulla presenza di altri pezzi (questi controlli vengono fatti nella classe Board con il metodo is_valid_move)

- Cambiamento metodo is_valid_move in classe Board: ora il metodo accetta il parametro di tipo Move e controlla che la mossa sia corretta in realzione ad altri pezzi presenti sulla griglia