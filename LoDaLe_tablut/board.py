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

    def __init__(self):
        self.current_board = None
        self.board_history = []
    
    def load_board(self, board):
        self.current_board = board
        self.board_history.append(board)
            
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
        # Check if the destination is within board bounds
        if not self.is_within_bounds(to_x, to_y):
            return False
        
        # Check if the destination is occupied
        if self.current_board[to_x][to_y] != 'EMPTY':
            return False
        
        # Check if the move is orthogonal (pieces can only move in straight lines)
        if from_x != to_x and from_y != to_y:
            return False
                
        # Traverse the path to the destination, ensuring all intermediate cells are empty
        dx = np.sign(to_x - from_x)  # +1, -1, or 0 ==> orthogonal directions
        dy = np.sign(to_y - from_y)  # +1, -1, or 0 ==> orthogonal directions
        current_x, current_y = from_x + dx, from_y + dy
        while current_x != to_x or current_y != to_y:
            if self.current_board[current_x][current_y] != 'EMPTY':
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
                if self.current_board[x][to_y] == 'BLACK':
                    return False
        elif to_x == 8:  # Bottom escapes
            for x in range(0, to_x):
                if self.current_board[x][to_y] == 'BLACK':
                    return False
        elif to_y == 0:  # Left escapes
            for y in range(to_y + 1, 9):
                if self.current_board[to_x][y] == 'BLACK':
                    return False
        elif to_y == 8:  # Right escapes
            for y in range(0, to_y):
                if self.current_board[to_x][y] == 'BLACK':
                    return False
        
        return True
    
    def is_capture(self, x, y, to_x, to_y):
        # Determine which piece made the move
        moved_piece = self.current_board[to_x][to_y]
        
        # Define directions for orthogonal movement
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        captures = []
        
        # Check each direction for possible captures
        for dx, dy in directions:
            capture_x, capture_y = x + dx, y + dy
            opposite_x, opposite_y = x - dx, y - dy
            
            # Ensure we're still within bounds
            if not self.is_within_bounds(capture_x, capture_y) or not self.is_within_bounds(opposite_x, opposite_y):
                continue
            
            # Capture logic for normal pieces (black or white)
            if self.current_board[capture_x][capture_y] != 'EMPTY' and self.current_board[capture_x][capture_y] != moved_piece:
                if self.is_opponent_piece(moved_piece, self.current_board[capture_x][capture_y]):
                    # Check if the opposite tile contains an opponent's piece or is an impassable tile
                    if (self.current_board[opposite_x][opposite_y] == moved_piece or
                            self.is_special_tile(opposite_x, opposite_y)):
                        captures.append((capture_x, capture_y))
        
        # Special handling for the king's capture (surrounding on all 4 sides)
        if self.current_board[x][y] == 'KING':
            surrounding_tiles = [(x + dx, y + dy) for dx, dy in directions]
            count_black = 0
            for sx, sy in surrounding_tiles:
                if self.is_within_bounds(sx, sy) and (self.current_board[sx][sy] == 'BLACK' or self.is_special_tile(sx, sy)):
                    count_black += 1
            if count_black == 4:  # King is surrounded on all four sides
                captures.append((x, y))
        
        return captures if captures else None

    def get_all_moves_for_piece(self, x, y):
        piece_type = self.current_board[x][y]
        moves = []
        if piece_type not in ['WHITE', 'BLACK', 'KING']:
            return moves
        
        # Orthogonal directions (up, down, left, right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            moves.extend(self.get_moves_in_direction(x, y, dx, dy, piece_type))
        
        return moves
    
    def get_all_moves(self, turn):
        all_moves = []
        for x in range(9):
            for y in range(9):
                piece = self.current_board[x][y]
                if turn == 'WHITE' and piece in ['WHITE', 'KING']:
                    piece_moves = self.get_all_moves_for_piece(x, y)
                    if piece_moves:  # Only add if there are moves
                        all_moves.append((x, y, piece_moves))
                elif turn == 'BLACK' and piece == 'BLACK':
                    piece_moves = self.get_all_moves_for_piece(x, y)
                    if piece_moves:  # Only add if there are moves
                        all_moves.append((x, y, piece_moves))
        return all_moves

    
# if __name__ == "__main__" :
#     b = Board()
    
#     initial_state = {
#         'board': 
#             np.array([
#                 ['EMPTY', 'EMPTY', 'EMPTY', 'BLACK', 'BLACK', 'BLACK', 'EMPTY', 'EMPTY', 'EMPTY'],
#                 ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
#                 ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'WHITE', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
#                 ['BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'WHITE', 'EMPTY', 'EMPTY', 'EMPTY', 'BLACK'],
#                 ['BLACK', 'BLACK', 'WHITE', 'WHITE', 'KING', 'WHITE', 'WHITE', 'BLACK', 'BLACK'],
#                 ['BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'WHITE', 'EMPTY', 'EMPTY', 'EMPTY', 'BLACK'],
#                 ['EMPTY', 'EMPTY', 'EMPTY', 'WHITE', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
#                 ['EMPTY', 'EMPTY', 'EMPTY', 'BLACK', 'BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
#                 ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'BLACK', 'BLACK', 'EMPTY', 'EMPTY', 'EMPTY']
#             ], dtype='<U5'), 
#         'turn': 
#             'WHITE'
#     }
    
#     # # Check corrct constants ==> OK !!
#     # copy_check = initial_state['board'].copy()
#     # n = initial_state['board'].shape[0]
#     # for i in range(n):
#     #     for j in range(n):
#     #         if (i,j) in CAMPS : copy_check[i][j] = "CAMP"
#     #         if (i,j) in ESCAPES : copy_check[i][j] = "ESCAPE"
#     #         if (i,j)==CASTLE : copy_check[i][j] = "CASTLE"
#     # print(copy_check)
    
#     pretty_print(initial_state['board'])
    
#     b.load_board(initial_state['board'])
#     moves = b.get_all_moves(initial_state['turn'])[0]
    
#     _from = moves[0], moves[1]
#     _to = moves[2][0]
    
#     print(f"Moves: {tuple2alfanum(_from)} --> {tuple2alfanum(_to)}")