# Ottimizzazione classe Board

## Obiettivi:
1. ✅ Ottimizzare ricerca del Re: si può salvare la posizione senza cercarla ogni volta 
2. ✅ Riorganizzare la sequenza di chiamate ai metodi delle mosse: fare un metodo generale per richiedere possibili mosse di un pezzo
3. ✅ Creare un metodo di Board che permetta di applicare una sequenza di mosse: è opportuno creare un metodo che data una lista di mosse, le applichi temporaneamente in sequenza (senza salvarle nello stato principale) e poi generi una lista di possibili mosse a partire da questa
4. ✅ Creare classe Mossa: creare una classe mossa che permetta di fare un check degli argomenti e che salvi in un unico oggetto le coordinate finali ed il tipo di pezzo mosso
5. ✅ Rendere la classe Node compatibile con le scelte sopra riportate
6. ✅ Aggiungi metodo a classe board che restituisce una lista di pezzi o punti di interesse presenti data una linea retta sulla griglia
7. ✅ Aggiungi metodo a classe Board che restituisce una lista di pezzi o punti di interesse presenti dato un anello di raggio n a partire da un centro sulla griglia
8. ✅ Rendi il metodo che restituisce la lista di pezzi nell'anello di raggio n funzionante anche quando l'anello è in parte out of bounds (implica sistemare anche il metodo che restituisce l'occupazione dei segmenti)
9. ✅ Fai classe di testing che verifichi le seguenti cose:
    - ✅ test delle valid moves
    - ✅ movimento pezzi ed escape del King
    - ✅ cattura di pezzi semplici in tutte le casistiche
    - ✅ cattura del re in tutte le casistiche
    - ✅ controllo sul numero e la tipologia di mosse possibili
    - ✅ controllo sul funzionamento corretto del reverse moves
10. Correggi cattura del king e degli alti pezzi in is_a_capture_move (ora è più semplice perchè ho modificato la segment_occupation)
10. (❓ forse non serve)Aggiungi metodo che restituisca in qualche modo in ordine di vicinanza tutti gli escapes del re in una data posizione (lookup table tridimensionale??) -> implica la creazione di un algoritmo apposito che per ogni cella metta la lista di escapes in ordine di vicinanza con le relative distanze e salvi il tutto in un file leggibile all'avvio di board
11. Classe timer semplice con label per misurare performance dei metodi singoli (così da vedere quali tradurre in c++)
12. Fare BoardInterface per astrarre metodi pubblici da privati 


## Todo
- ✅ incapsula in get all moves l'apply ed il reverse 
- ✅ aggiungi get_king 
- ✅ metodi get_all_blacks get_all_whites get_king 
- ✅ il metodo segment occupation e ring occupation devono ritornare anche camps e escapes (non prioritari)

- metodo per 'evidenziare' celle libere verso camps (partire dai camps)
- i tuple2alfanum vanno messi come metodi di Move

## Cose modificate:
- Aggiunta la classe Move: rappresenta una mossa, con una posizione iniziale e una finale e il colore del pezzo mosso. Il costrutture della classe svolge controlli solo sulla correttezza formale della mossa in sè, ovvero se è nei limiti della griglia e se è ortogonale, non fa controlli sulla presenza di altri pezzi (questi controlli vengono fatti nella classe Board con il metodo is_valid_move)

## Metodi pubblici:
- segment_occupation
- ring_occupation
- is_adjacent
- is_caputre_move
- is_king_escaped
- is_king_captured
- get_all_moves
- apply_moves
