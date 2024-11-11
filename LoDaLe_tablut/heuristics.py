import math
from board import Board, ESCAPES, CAMPS

def white_heuristics(state: Board) -> int:
    king_pos = None
    for i in range(9):
        for j in range(9):
            if state.board[i][j] == 'KING':
                king_pos = (i, j)
                break
        if king_pos:
            break

    if not king_pos:
        return -float('inf')  # captured king == worst situation for white

    king_x, king_y = king_pos
    
    # 1. distance(King, nearest escape)
    min_escape_dist = min([abs(king_x - ex) + abs(king_y - ey) for ex, ey in ESCAPES])
    
    # 2. How well the king is protected by whites
    white_protection = 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for dx, dy in directions:
        adj_x, adj_y = king_x + dx, king_y + dy
        if state.is_within_bounds(adj_x, adj_y) and state.board[adj_x][adj_y] == 'WHITE':
            white_protection += 1
    
    # 3. How much in danger is the king
    surrounding_threats = 0
    for dx, dy in directions:
        adj_x, adj_y = king_x + dx, king_y + dy
        if state.is_within_bounds(adj_x, adj_y):
            adj_piece = state.board[adj_x][adj_y]
            if adj_piece == 'BLACK' or state.is_special_tile(adj_x, adj_y):
                surrounding_threats += 1
    
    escape_score = 10 * (8 - min_escape_dist)  # How close the king is to an escape
    protection_score = 5 * white_protection    # How well the king is protected by white pieces
    threat_score = -15 * surrounding_threats   # How much danger the king is in

    return escape_score + protection_score + threat_score

def black_heuristics(state: Board) -> int:
    king_pos = None
    for i in range(9):
        for j in range(9):
            if state.board[i][j] == 'KING':
                king_pos = (i, j)
                break
        if king_pos:
            break

    if not king_pos:
        return float('inf')  # captured king == best situation for white

    king_x, king_y = king_pos
    
    # 1. distance(King, nearest escape)
    min_escape_dist = min([abs(king_x - ex) + abs(king_y - ey) for ex, ey in ESCAPES])
    
    # 2.How well the king is threatened by blacks
    black_threats = 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for dx, dy in directions:
        adj_x, adj_y = king_x + dx, king_y + dy
        if state.is_within_bounds(adj_x, adj_y) and state.board[adj_x][adj_y] == 'BLACK':
            black_threats += 1
    
    # 3. How many escapes are free for the king
    escape_open = 0
    for ex, ey in ESCAPES:
        if abs(king_x - ex) + abs(king_y - ey) <= 1:  # Il re è molto vicino a una fuga
            escape_open += 1
    
    escape_distance_score = 10 * min_escape_dist    # Higher score if the king is further from an escape
    threat_score = 20 * black_threats               # Higher score if there are more black pieces threatening the king
    open_escape_penalty = -30 * escape_open         # Penalty if there are open escape routes for the king

    return escape_distance_score + threat_score + open_escape_penalty


def grey_heuristic(state: Board) -> int:
    ''' 
    MAX = white
    MIN = black
    '''
    
    # TODO: optimize with a state.get_king()
    king_pos = None
    for i in range(9):
        for j in range(9):
            if state.board[i][j] == 'KING':
                king_pos = (i, j)
                break
        if king_pos:
            break
    king_x, king_y = king_pos
    
    # 1. If the king got captured ==> white lost
    if not king_pos:
        return -float('inf')
    
    # 2. If the king is in an escape ==> white won
    if king_pos in ESCAPES:
        return float('inf')
    
    # 3. How many free routes will have the king 
    # TODO: maybe merge here all loops
    free_routes = 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for dx, dy in directions:
        adj_x, adj_y = king_x + dx, king_y + dy
        while state.is_within_bounds(adj_x, adj_y) and state.board[adj_x][adj_y]=="EMPTY":
            adj_x, adj_y = adj_x + dx, adj_y + dy
        if (adj_x,adj_y) in ESCAPES : 
            free_routes += 1
            
    # 4. distance(King, nearest escape)
    min_escape_dist = math.sqrt(min([abs(king_x - ex) + abs(king_y - ey) for ex, ey in ESCAPES]))
    
    # 5. How well the king is protected by whites (3x3 kernel on king)
    # 6. How much in danger is the king (3x3 kernel on king)
    white_protection = 0
    surrounding_threats = 0
    for dx, dy in directions:
        adj_x, adj_y = king_x + dx, king_y + dy
        if state.is_within_bounds(adj_x, adj_y):
            adj_piece = state.board[adj_x][adj_y]
            if adj_piece == 'BLACK' or state.is_special_tile(adj_x, adj_y):
                surrounding_threats += 1
            if adj_piece == 'WHITE':
                white_protection += 1

    # Checking if a black can go near the king the next move
    possible_checkers = 0
    check_pos_x, check_pos_y = king_x, king_y
    for dx, dy in directions:
        while state.is_within_bounds(check_pos_x, check_pos_y):
            check_pos_x += dx
            check_pos_y += dy
            if state.board[check_pos_x][check_pos_y] == 'BLACK':
                possible_checkers += 1
                break
            elif state.board[check_pos_x][check_pos_y] != 'EMPTY':
                break

    # 7. The black must tend to have a rombus disposition
    rombus_pos = [ 
                (1,2),       (1,6),
        (2,1),                      (2,7),

        (6,1),                      (6,7),
                (7,2),       (7,6)
    ]
    # Count the number of escape which are closed by a black
    escape_covered = [
        (1,1),(1,2),        (1,6),(1,7),
        (2,1),                    (2,7),

        (6,1),                    (6,7),
        (7,1),(7,2),        (7,6),(7,7)
    ]
    # In the corner one black cover two escapes
    double_covered_escape = [
        (1,1),          (1,7),

        (7,1),          (7,7)
    ]
    num_rombus_pos = 0
    num_covered_escapes = 0
    num_double_covered_escapes = 0
    for i in range(9):
        for j in range(9):
            if state.board[i][j] == 'BLACK' and ((i,j) in rombus_pos):
                num_rombus_pos += 1
            if state.board[i][j] == 'BLACK' and ((i,j) in escape_covered):
                num_covered_escapes += 1
            if state.board[i][j] == 'BLACK' and ((i,j) in double_covered_escape):
                num_double_covered_escapes += 1
        
    # 8. 
    
    # Compute scorings (DECIDE THE WEIGHTS also using non linear functions)
    W1, W2, W3, W4, W5 = 1, 1, 1, 1, 1     # NOTE: just for testing
    scorings = {
        'escape_score ' : W1 * (math.sqrt(50) - min_escape_dist), 
        'protection_score ' : W2 * white_protection, 
        'threat_score ' : - W3 * surrounding_threats, 
        'open_escape_bonus ' : W4 * free_routes,
        'num_rombus_pos' : - W5 * num_rombus_pos
    }
    
    return sum(scorings.values())