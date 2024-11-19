import math
from board import *
import numpy as np


#### I WILL RECIVE ############################################################################
# - il metodo segment occupation e ring occupation devono ritornare anche: camps ed escapes (non prioritari)
# - 'C' = CAMP, 'E' = EMPTY, 'S' = ESCAPE, 'B' = BLACK, 'W' = WHITE
# - il metodo highlight_covered_escapes che restituisce le caselle a partire dalle escapes che sono libere (prima di incontrare ostacoli o pedine nere) 
#   (quindi potenzialmente occupabili da pedoni bianchi). Restituisce un np.array contenente le tuple delle celle desiderate.
###############################################################################################

def grey_heuristic(board: Board) -> int:
    '''
    MAX = white

    MIN = black
    '''

    ### ALL VARIABLES ##################################################################################################################
    king_pos = None                     # 1. Check if the player has won or lost
    free_routes_to_escapes = 0          # 2. How many free routes will have the king to reach the escapes
    free_routes = 0                     # 3. How many free routes will have the king
    surrounding_protection = 0          # 4. How well the king is protected by whites (with adjacent whites)
    surrounding_threats = 0             # 5. How much in danger (has non-white obstacles) is the king (with adjacent black or camps)
    possible_protection = 0             # 6. How well the king is protected by whites (untill the first obstalces)
    possible_checkers = 0               # 7. How many black can be adjacent to the king the next move
    possible_threats = 0                # 8. How much in danger (has non-white obstacles) is the king (untill the first obstalces)
    num_rombus_pos = 0                  # 9. The black must tend to have a rombus disposition
    num_covered_escapes = 0             # 10. The black may tend to cover the escapes
    num_double_covered_escapes = 0      # 11. The black should prefer the double cover escapes (covers 2 with 1 pawn)
    # freecell_near_escapes = 0         # 12. The white should tend to cover free cells near escapes before black
    # white_covers_escape = 0             # 12. Escapes which are covered first by a white
    num_whites = 0                      # 13. The number of whites
    num_blacks = 0                      # 14. The number of blacks
    ####################################################################################################################################


    ### CHECK THE TABLE ###################################################################################################
    whites = board.get_all_pieces_of_color(WHITE)
    blacks = board.get_all_pieces_of_color(BLACK)
    num_whites = len(whites)
    num_blacks = len(blacks)
    king_pos = board.get_king()

    intersection_rombus = np.isin(num_blacks, ROMBUS_POS).all(axis=1)
    num_rombus_pos = np.sum(intersection_rombus)
    intersection_covered_escapes = np.isin(num_blacks, ESCAPE_COVER).all(axis=1)
    num_covered_escapes = np.sum(intersection_covered_escapes)
    intersection_double_covered_escapes = np.isin(num_blacks, DOUBLE_ESCAPE_COVER).all(axis=1)
    num_double_covered_escapes = np.sum(intersection_double_covered_escapes)
    ########################################################################################################################



    # If the king got captured ==> white lost
    if not king_pos:
        return -float('inf')



    ### CHECK ALL AROUND THE KING ###########################################################################################
    king_ring = board.ring_occupation(king_pos, 1)["str"]
    for i in range(4):
        if king_ring[i*2] == 'W':
            surrounding_protection += 1
        if king_ring[i*2] == 'B' or king_ring[i*2] == 'C':
            surrounding_threats += 1

    king_x, king_y = king_pos
    checking_start = [(king_x-1, king_y), (king_x, king_y+1), (king_x+1, king_y), (king_x, king_y-1)]
    checking_arrive = [(0, king_y),(king_x, 8), (8, king_y), (king_x, 0)]
    temp_arrive = [(king_x-1, 0), (0, king_y+1), (king_x+1, 8), (0, king_y-1), (king_x-1, 8), (8, king_y+1), (king_x+1, 0), (8, king_y-1)]
    # Check the column and the row of the king
    for i in range(4):
        column_check = board.segment_occupation(king_pos, checking_arrive[i])["str"]
        if column_check[-1] == 'S' and (all(c == 'E' for c in column_check[:-1]) or len(column_check) == 1):
            free_routes_to_escapes += 1
        else:
            for car in column_check:
                if car == 'B':
                    possible_checkers += 1
                    possible_threats += 1
                    break
                elif car == 'W':
                    possible_protection += 1
                    break
    # Check the column and the row near the king
    for i in range(8):
        column_check = board.segment_occupation(checking_start[i%2], temp_arrive)["str"]
        for car in column_check:
            if car == 'B':
                possible_checkers += 1
                break
            elif car == 'W':
                possible_protection += 1
                break
            elif car == 'S' or car == 'C':
                break
    #############################################################################################################################



    ### Check covered escapes by white ##########################################################################################
    # highlight_space = board.highlight_covered_escapes()
    # values_in_highlight_escapes = board[highlight_space[:, 0], highlight_space[:, 1]]
    # white_covers_escape = np.sum(values_in_highlight_escapes == 'W')
    ##############################################################################################################################


    free_routes = 4 - possible_threats - possible_protection - surrounding_threats - surrounding_protection



    ### Compute scorings (DECIDE THE WEIGHTS also using non linear functions) #####################################

    # Use weight to optimize the module of the score
    # W1 = 3    # Bilancia la distanza dall'escape
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
        # 'nearest_escape_distance_score':
            # W1 * (math.sqrt(50) - get_min_escape_dist())    if free_routes_to_escapes==0
                                                            # else 0,

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

        # The king must consider them only if he is inside the rombus and if the blacks are enough to create the rombus
        'rombus_position_score':
            - W8 * num_rombus_pos       if free_routes_to_escapes == 0 and num_blacks > 8
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