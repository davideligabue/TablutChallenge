import numpy as np
from utils import *

# CONSTANTS
WHITE_PLAYER = "WHITE"
BLACK_PLAYER = "BLACK"
CASTLE = (4, 4)
CAMPS = {   
    (0,3), (0,4), (0,5), (1,4),     # upper camps
    (8,3), (8,4), (8,5), (7,4),     # lower camps
    (3,0), (4,0), (5,0), (4,1),     # left camps
    (3,8), (4,8), (5,8), (4,7)      # right camps
}
ESCAPES = {   
    (0,1), (0,2), (1,0), (2,0),     # upper-left escapes
    (6,0), (7,0), (8,1), (8,2),     # lower-left escapes
    (8,6), (8,7), (6,8), (7,8),     # lower-right escapes
    (0,6), (0,7), (1,8), (2,8)      # upper-right escapes
}

'''
STATE (initial) :

{
    'board': 
        array([
            ['EMPTY', 'EMPTY', 'EMPTY', 'BLACK', 'BLACK', 'BLACK', 'EMPTY', 'EMPTY', 'EMPTY'],
            ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
            ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'WHITE', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
            ['BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'WHITE', 'EMPTY', 'EMPTY', 'EMPTY', 'BLACK'],
            ['BLACK', 'BLACK', 'WHITE', 'WHITE', 'KING', 'WHITE', 'WHITE', 'BLACK', 'BLACK'],
            ['BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'WHITE', 'EMPTY', 'EMPTY', 'EMPTY', 'BLACK'],
            ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'WHITE', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
            ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
            ['EMPTY', 'EMPTY', 'EMPTY', 'BLACK', 'BLACK', 'BLACK', 'EMPTY', 'EMPTY', 'EMPTY']
        ], dtype='<U5'), 
    'turn': 
        'WHITE'
}

REPRESENTED AS:

    A   B   C   D   E   F   G   H   I
  +---+---+---+---+---+---+---+---+---+
 1    |   |   | B | B | B |   |   |   |
  +---+---+---+---+---+---+---+---+---+
 2    |   |   |   | B |   |   |   |   |
  +---+---+---+---+---+---+---+---+---+
 3    |   |   |   | W |   |   |   |   |
  +---+---+---+---+---+---+---+---+---+
 4  B |   |   |   | W |   |   |   | B |
  +---+---+---+---+---+---+---+---+---+
 5  B | B | W | W | K | W | W | B | B |
  +---+---+---+---+---+---+---+---+---+
 6  B |   |   |   | W |   |   |   | B |
  +---+---+---+---+---+---+---+---+---+
 7    |   |   |   | W |   |   |   |   |
  +---+---+---+---+---+---+---+---+---+
 8    |   |   |   | B |   |   |   |   |
  +---+---+---+---+---+---+---+---+---+
 9    |   |   | B | B | B |   |   |   |
  +---+---+---+---+---+---+---+---+---+

'''

class Board:

    def __init__(self, state):
        self.turn = state['turn']
        # Board must be np.ndarray
        self.board = state['board'] \
                    if type(state['board'])==np.ndarray \
                    else np.array(state['board'])   
    
    def is_within_bounds(self, x, y):
        return 0 <= x < 9 and 0 <= y < 9

    def is_opponent_piece(self, moved_piece, other_piece):
        if moved_piece == 'WHITE' and other_piece == 'BLACK':
            return True
        if moved_piece == 'BLACK' and other_piece == 'WHITE':
            return True
        if moved_piece == 'KING' and other_piece == 'BLACK':
            return True
        return False

    def is_special_tile(self, x, y):
        # Castle and camp positions are pre-defined (as constants or in the board setup)
        if (x, y) == CASTLE:
            return True
        if (x, y) in CAMPS:
            return True
        return False

    def is_valid_move(self, from_x, from_y, to_x, to_y, piece_type):
        
        # Black can't move the king
        if piece_type=="KING" and self.turn=="BLACK":
            return False
        
        # Can't move opponents pieces
        if (piece_type=="WHITE" or piece_type=="BLACK") and self.turn!=piece_type:
            return False
        
        # Can't move the empty pos
        if piece_type=="EMPTY":
            return False
        
        # Can't move the tower
        if piece_type=="THRONE":
            return False
        
        # Check if the destination is within board bounds
        if not self.is_within_bounds(to_x, to_y):
            return False
        
        # Check if the destination is occupied
        if self.board[to_x][to_y] != 'EMPTY':
            return False
        
        # Check if the move is orthogonal (pieces can only move in straight lines)
        if from_x != to_x and from_y != to_y:
            return False
                
        # Traverse the path to the destination, ensuring all intermediate cells are empty
        dx = np.sign(to_x - from_x)  # +1, -1, or 0 ==> orthogonal directions
        dy = np.sign(to_y - from_y)  # +1, -1, or 0 ==> orthogonal directions
        current_x, current_y = from_x + dx, from_y + dy
        while current_x != to_x or current_y != to_y:
            if self.board[current_x][current_y] != 'EMPTY':
                return False
            current_x += dx
            current_y += dy
        
        # Check special conditions for the king and camps
        if (to_x, to_y) == CASTLE:
            # Only the king can move into or land on the castle
            if piece_type != 'KING':
                return False
        if (to_x, to_y) in CAMPS:
            # Only black pieces can land in camps, but once they leave, they cannot re-enter
            if piece_type == 'WHITE' or piece_type == 'KING':
                return False
        
        # Ensure black pieces cannot return to camps once they have left
        if (from_x, from_y) not in CAMPS and (to_x, to_y) in CAMPS and piece_type == 'BLACK':
            return False
        
        # For the king, check if it is moving towards an escape point
        if piece_type == 'KING' and (to_x, to_y) in ESCAPES:
            # The king can only move to an escape if there is a clear path (no black pieces in the way)
            if not self.is_escape_clear(to_x, to_y):
                return False
        
        # If all checks pass, the move is valid
        return True

    def is_goal_state(self):
        king_pos = None

        # Find the King on the board
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 'KING':
                    king_pos = (i, j)
                    break
            if king_pos:
                break

        if not king_pos:
            # If there's no King on the board, it's an invalid state, or the King has been captured
            return self.turn == BLACK_PLAYER  # Black wins if the King has been captured

        king_x, king_y = king_pos

        # Check if the King is on an escape point (White victory)
        if (king_x, king_y) in ESCAPES:
            return self.turn == WHITE_PLAYER  # White wins if the King reaches an escape point

        # Check if the King is surrounded (Black victory)
        # Directions for orthogonal checking
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        surrounding_black = 0

        for dx, dy in directions:
            adj_x, adj_y = king_x + dx, king_y + dy

            if not self.is_within_bounds(adj_x, adj_y):
                continue

            adj_piece = self.board[adj_x][adj_y]

            # Check if it's either a black piece or a special tile (camp or castle)
            if adj_piece == 'BLACK' or self.is_special_tile(adj_x, adj_y):
                surrounding_black += 1

        # The King is captured if surrounded on all four sides
        if surrounding_black == 4:
            return self.turn == BLACK_PLAYER  # Black wins if the King is surrounded

        return False  # No player has won yet

    def get_moves_in_direction(self, x, y, dx, dy, piece_type):
        moves = []
        new_x, new_y = x + dx, y + dy
        while self.is_valid_move(x, y, new_x, new_y, piece_type):
            moves.append((new_x, new_y))
            new_x += dx
            new_y += dy
        return moves

    def is_escape_clear(self, to_x, to_y):
        # Check if there are no black pieces blocking the escape path for the king
        if to_x == 0:  # Top escapes
            for x in range(to_x + 1, 9):
                if self.board[x][to_y] == 'BLACK':
                    return False
        elif to_x == 8:  # Bottom escapes
            for x in range(0, to_x):
                if self.board[x][to_y] == 'BLACK':
                    return False
        elif to_y == 0:  # Left escapes
            for y in range(to_y + 1, 9):
                if self.board[to_x][y] == 'BLACK':
                    return False
        elif to_y == 8:  # Right escapes
            for y in range(0, to_y):
                if self.board[to_x][y] == 'BLACK':
                    return False
        
        return True
    
    def get_captures(self, from_x, from_y):
        captures = []
        moved_piece = self.board[from_x][from_y]
        
        # Directions for orthogonal movement
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        # Check all directions from (from_x, from_y) to see if any move results in a capture
        for dx, dy in directions:
            x, y = from_x, from_y
            
            # Move along the direction until we hit a block or the edge of the board
            while True:
                x += dx
                y += dy
                
                # Stop if we go out of bounds
                if not self.is_within_bounds(x, y):
                    break
                
                # Stop if we hit a non-empty tile
                if self.board[x][y] != 'EMPTY':
                    break
                
                # Check if moving to (x, y) results in a capture
                adj_x, adj_y = x + dx, y + dy  # Adjacent square in the direction we're checking
                opp_x, opp_y = x + 2*dx, y + 2*dy  # Opposite square beyond the adjacent one

                # Ensure adjacent and opposite squares are within bounds
                if not (self.is_within_bounds(adj_x, adj_y) and self.is_within_bounds(opp_x, opp_y)):
                    continue

                adj_piece = self.board[adj_x][adj_y]
                opp_piece = self.board[opp_x][opp_y]

                # Check if the adjacent piece is an opponent's piece and can be captured
                if self.is_opponent_piece(moved_piece, adj_piece):
                    if opp_piece == moved_piece or self.is_special_tile(opp_x, opp_y):
                        captures.append((x, y))  # Add this position as a valid capture move

        return captures if captures else None

    def is_capture(self, from_x, from_y, to_x, to_y):
        moved_piece = self.board[from_x][from_y]

        # Directions for orthogonal movement
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        # Check in all directions for possible captures
        for dx, dy in directions:
            adj_x, adj_y = to_x + dx, to_y + dy  # Adjacent square in the direction of the move
            opp_x, opp_y = to_x + 2*dx, to_y + 2*dy  # Opposite square beyond the adjacent one

            # Ensure adjacent and opposite squares are within bounds
            if not (self.is_within_bounds(adj_x, adj_y) and self.is_within_bounds(opp_x, opp_y)):
                continue

            adj_piece = self.board[adj_x][adj_y]
            opp_piece = self.board[opp_x][opp_y]

            # Check if the adjacent piece is an opponent's piece and can be captured
            if self.is_opponent_piece(moved_piece, adj_piece):
                if opp_piece == moved_piece or self.is_special_tile(opp_x, opp_y):
                    return True  # Capture found

        # Special handling for capturing the king
        if moved_piece == 'KING':
            count_black = 0
            surrounding_tiles = [(to_x + dx, to_y + dy) for dx, dy in directions]
            for sx, sy in surrounding_tiles:
                if self.is_within_bounds(sx, sy) and (self.board[sx][sy] == 'BLACK' or self.is_special_tile(sx, sy)):
                    count_black += 1
            if count_black == 4:  # King is surrounded on all four sides
                return True
        
        return False
    
    def apply_move(self, from_pos, to_pos):
        _from_x, _from_y = from_pos
        _to_x, _to_y = to_pos

        # Controlla se il movimento è valido
        piece_type = self.board[_from_x][_from_y]
        if not self.is_valid_move(_from_x, _from_y, _to_x, _to_y, piece_type):
            raise ValueError("Invalid move")

        # Esegue il movimento
        self.board[_to_x][_to_y] = piece_type  # Sposta il pezzo nella nuova posizione
        self.board[_from_x][_from_y] = 'EMPTY'  # Libera la posizione precedente

        # Gestisce la cattura, se presente
        if self.is_capture(_from_x, _from_y, _to_x, _to_y):
            self.capture_piece(_from_x, _from_y, _to_x, _to_y)

        # Cambia il turno
        self.turn = WHITE_PLAYER if self.turn == BLACK_PLAYER else BLACK_PLAYER

    def capture_piece(self, from_x, from_y, to_x, to_y):
        # Logica per rimuovere il pezzo catturato, se necessario
        moved_piece = self.board[from_x][from_y]
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        for dx, dy in directions:
            adj_x, adj_y = to_x + dx, to_y + dy
            opp_x, opp_y = to_x + 2*dx, to_y + 2*dy

            # Controlla se ci sono pezzi avversari da catturare
            if self.is_within_bounds(adj_x, adj_y) and self.is_within_bounds(opp_x, opp_y):
                adj_piece = self.board[adj_x][adj_y]
                if self.is_opponent_piece(moved_piece, adj_piece):
                    # Cattura il pezzo avversario
                    self.board[adj_x][adj_y] = 'EMPTY'  # Rimuovi il pezzo avversario

    def get_all_moves_for_piece(self, x, y):
        piece_type = self.board[x][y]
        moves = []
        if piece_type not in ['WHITE', 'BLACK', 'KING']:
            return moves
        
        # Orthogonal directions (up, down, left, right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            moves.extend(self.get_moves_in_direction(x, y, dx, dy, piece_type))

        return moves
    
    def get_all_moves(self):
        all_moves = []
        for x in range(9):
            for y in range(9):
                piece = self.board[x][y]
                if self.turn == 'WHITE' and piece in ['WHITE', 'KING']:
                    piece_moves = self.get_all_moves_for_piece(x, y) 
                    if piece_moves:  # Only add if there are moves
                        all_moves.append((x, y, piece_moves))
                elif self.turn == 'BLACK' and piece == 'BLACK':
                    piece_moves = self.get_all_moves_for_piece(x, y)
                    if piece_moves:  # Only add if there are moves
                        all_moves.append((x, y, piece_moves))
        return all_moves
    
    def pretty_print(self):
        # Board dimension
        n = self.board.shape[0]
        
        # Literal labels (A, B, C, ...)
        column_labels = '    ' + '   '.join([chr(i + ord('A')) for i in range(n)])  # Quattro spazi
        print(column_labels)
        
        # Separators
        separator = '  ' + '+---' * n + '+'
        
        for i in range(n):
            print(separator)
            
            # Row + pieces
            row = f'{i+1:2d} ' + '|'.join([f' {cell[0]} ' if cell != 'EMPTY' else '   ' for cell in self.board[i]]) + ' |'
            print(row)
        
        print(separator)