import math
from board import Board, ESCAPES, CAMPS, ROMBUS_POS, DOUBLE_ESCAPE_COVER, ESCAPE_COVER
from utils import cells_on_line

def heuristic_1(state: Board) -> int:
    pass

def heuristic_2(state: Board) -> int:
    pass

def heuristic_3(state: Board) -> int:
    pass

def grey_heuristic(state: Board) -> int:
    ''' 
    MAX = white
    
    MIN = black
    '''
    
    ### ALL VARIABLES ##################################################################################################################
    king_pos = None                     # 1. Check if the player has won or lost
    free_routes_to_escapes = 0          # 2. How many free routes will have the king to reach the escapes
    free_routes = 0                     # 3. How many free routes will have the king
    surrounding_protection = 0          # 4. How well the king is protected by whites (3x3 kernel on king)
    surrounding_threats = 0             # 5. How much in danger (has non-white obstacles) is the king (3x3 kernel on king)
    possible_threats = 0                # 6. How well the king is protected by whites (untill the first obstalces)
    possible_protection = 0             # 7. How much in danger (has non-white obstacles) is the king (untill the first obstalces)
    num_rombus_pos = 0                  # 8. The black must tend to have a rombus disposition
    num_covered_escapes = 0             # 9. The black may tend to cover the escapes
    num_double_covered_escapes = 0      # 10. The black should prefer the double cover escapes (covers 2 with 1 pawn)
    min_escape_dist = 0                 # 11. Distance(King, nearest escape)
    num_whites = 0                      # 12. The number of whites     
    num_blacks = 0                      # 13. The number of blacks
    ####################################################################################################################################
    
    
    
    ### LOOP OVER THE TABLE #############################################################
    for i in range(9):
        for j in range(9):
            piece = state.board[i][j]
            if piece == 'BLACK':
                num_blacks += 1
                if ((i,j) in ROMBUS_POS):
                    num_rombus_pos += 1
                if ((i,j) in ESCAPE_COVER):
                    num_covered_escapes += 1
                if ((i,j) in DOUBLE_ESCAPE_COVER):
                    num_double_covered_escapes += 1
            elif (piece == 'WHITE') or (piece == 'KING'):
                num_whites += 1
                if piece == 'KING':
                    king_pos = (king_x, king_y) = i, j
                    if king_pos in ESCAPES:  #If the king is in an escape ==> white won
                        return float('inf') 
    ####################################################################################
    
    
    # If the king got captured ==> white lost
    if not king_pos:
        return -float('inf')
    
    
    
    ### LOOP ALL AROUND THE KING ##########################################################
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for dx, dy in directions:
        adj_x, adj_y = king_x + dx, king_y + dy
        
        # First layer check
        if state.is_within_bounds(adj_x, adj_y):
            adj_piece = state.board[adj_x][adj_y]
            if adj_piece == 'BLACK' or state.is_special_tile(adj_x, adj_y):
                surrounding_threats += 1
                continue    # Already found an obstacle in this direction, try a new one
            if adj_piece == 'WHITE':
                surrounding_protection += 1
                continue    # Already found an obstacle in this direction, try a new one
        
        # First + following layers check
        while state.is_within_bounds(adj_x, adj_y):
            adj_x, adj_y = adj_x + dx, adj_y + dy
            if state.is_within_bounds(adj_x, adj_y):
                if state.board[adj_x][adj_y] == 'BLACK' or state.is_special_tile(adj_x, adj_y):
                    possible_threats += 1
                    break   # Already found an obstacle in this direction, try a new one
                if state.board[adj_x][adj_y] == 'WHITE':
                    possible_protection += 1
                    break   # Already found an obstacle in this direction, try a new one
            
        if (adj_x - dx, adj_y - dy) in ESCAPES :
            free_routes_to_escapes += 1
    #######################################################################################
    
    
    
    free_routes = 4 - possible_threats - possible_protection - surrounding_threats - surrounding_protection
    
    
    
    def get_min_escape_dist():
        min_dist = min([abs(king_x - ex) + abs(king_y - ey) for ex, ey in ESCAPES])
        c = 0
        ex_min, ey_min = None, None
        for ex, ey in ESCAPES:
            if abs(king_x - ex) + abs(king_y - ey) == min_dist:
                c += 1
                ex_min, ey_min = ex, ey
        if c in [1,2] :
            cells_among_king_escape_min = [state.board[x][y] for x,y in cells_on_line(king_x, king_y, ex_min, ey_min)]
            if "BLACK" not in cells_among_king_escape_min:
                return math.sqrt(min_dist)
            else: 
                return math.sqrt(50)  # we don't consider the distance if there are blacks in the middle  (the difference will be 0)
        else :
            return math.sqrt(50)      # we don't consider the distance if it is equidistant from 2 points (the difference will be 0)
    
    
    
    ### Compute scorings (DECIDE THE WEIGHTS also using non linear functions) #####################################
    
    # Use weight to optimize the module of the score
    W1 = 3    # Bilancia la distanza dall'escape
    W2 = 800  # Diminuisce l'enfasi sui percorsi liberi verso l'escape
    W3 = 40   # Incentiva percorsi liberi solo se l'escape non è immediato
    W4 = 25   # Migliora la protezione del re
    W5 = 15   # Diminuire l'effetto negativo delle minacce
    W6 = 8    # Diminuire l'effetto negativo delle minacce più lontane
    W7 = 12   # Migliora leggermente la protezione lontana
    W8 = 30   # Riduce l'enfasi su rombo
    W9 = 60   # Diminuire l'effetto negativo di escape coperti
    W10 = 150 # Riduce l'enfasi su doppi escape coperti
    W11 = 10  # Bilancia il vantaggio numerico
    
    # Use a dict for better usability and debug
    scorings = { 
        
        # The king should consider the nearest escape only if it is not surrounded by blacks 
        # in that direction (???)
        'nearest_escape_distance_score':
            W1 * (math.sqrt(50) - get_min_escape_dist())    if free_routes_to_escapes==0
                                                            else 0, 

        # The king must always consider options where he can win in one move 
        # NOTE: forse potremmo usare direttamente +infinito ma così magari eviteremmo 
        # scelte in cui ci sono più di 2 vie libere (btw vittoria assicurata)
        'free_routes_to_escapes_score': W2 * free_routes_to_escapes,
        
        # The king must consider free routes that don't lead to victory only if 
        # there are not free routes to escapes
        # NOTE: dobbiamo mettere che altrimenti il peso è negativo perchè altrimenti lo score 
        # resterebbe più o meno uguale e dobbiamo rimarcare che sia una brutta idea
        'free_routes_score': 
            W3 * free_routes    if free_routes_to_escapes==0 
                                else - W3 * free_routes,

        # The king should consider how well he is protected only if he is not in a winning 
        # position, so if he is not that much surrounded by blacks and he is next to an escape
        # NOTE: dobbiamo mettere che altrimenti il peso è negativo perchè altrimenti lo score 
        # resterebbe più o meno uguale e dobbiamo rimarcare che sia una brutta idea
        'surrounding_protection_score':
            W4 * surrounding_protection     if free_routes_to_escapes == 0
                                            else - W4 * surrounding_protection,  

        # The king should consider how much he is in danger only if he is not in a winning 
        # position, so if he is not that much surrounded by blacks and he is next to an escape
        'surrounding_threats_score':
            - W5 * surrounding_threats  if free_routes_to_escapes == 0 
                                        else 0,

        # Same as before (???)
        # NOTE: ancora meno importante se il re è vicino agli escapes
        'possible_threats_score':
            - W6 * possible_threats     if free_routes_to_escapes == 0 
                                        else 0,

        # Same as before (???)
        # NOTE: ancora meno importante se il re è vicino agli escapes
        'possible_protection_score':
            W7 * possible_protection    if free_routes_to_escapes == 0 
                                        else - W7 * possible_protection,

        # The king must consider them only if he is inside the rombus
        'rombus_position_score':
            - W8 * num_rombus_pos       if free_routes_to_escapes == 0 or \
                                            min_escape_dist < 2
                                        else 0,

        # The king must consider them only if he has no other escapes
        # NOTE: servono pesi alti
        'covered_escapes_score':
            - W9 * num_covered_escapes  if free_routes_to_escapes == 0 
                                        else 0,

        # The king must consider them only if he has no other escapes
        # NOTE: servono pesi molto molto alti
        'double_covered_escapes_score':
            - W10 * num_double_covered_escapes  if free_routes_to_escapes == 0 
                                                else 0,
        
        # The player must consider the numerical advantage only if he is not in 
        # a winning position                    
        'numerical_advantage' : 
            W11 * (num_whites-num_blacks)   if free_routes_to_escapes == 0 
                                            else 0
    }
    
    # state.pretty_print()
    # print(f"State evaluated with score {sum(scorings.values())}")
    
    return sum(scorings.values())