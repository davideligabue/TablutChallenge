from board import Board, ESCAPES, CAMPS
from search import Node

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
