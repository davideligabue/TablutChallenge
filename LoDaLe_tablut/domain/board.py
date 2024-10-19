import numpy as np


################################################################################################
# METODI DI UTILS CHE NON RIESCO A FARGLI LEGGERE ZIO PERA #####################################
################################################################################################

# TODO: rimediare assolutamente

def pretty_print(board):
    # Board dimension
    n = board.shape[0]
    
    # Literal labels (A, B, C, ...)
    column_labels = '    ' + '   '.join([chr(i + ord('A')) for i in range(n)])  # Quattro spazi
    print(column_labels)
    
    # Separators
    separator = '  ' + '+---' * n + '+'
    
    for i in range(n):
        print(separator)
        
        # Row + pieces
        row = f'{i+1:2d} ' + '|'.join([f' {cell[0]} ' if cell != 'EMPTY' else '   ' for cell in board[i]]) + ' |'
        print(row)
    
    print(separator)
    
def tuple2alfanum(tuple_pos):
    row, col = tuple_pos
    col_alfnum = chr(ord('a') + col)
    row_alfnum = str(1+row)
    return col_alfnum + row_alfnum

################################################################################################
################################################################################################

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
STATE:

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
'''

'''
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
        """Check if the position is within the 9x9 grid."""
        return 0 <= x < 9 and 0 <= y < 9

    def is_valid_move(self, x, y, piece_type):
        """Check if the position (x, y) is a valid move destination for the piece."""
        if not self.is_within_bounds(x, y):
            return False
        if self.current_board[x][y] != 'EMPTY':
            return False
        if (x, y) == CASTLE and piece_type != 'KING':  # Only the King can move to the castle
            return False
        if (x, y) in CAMPS:  # Camps can't be entered or crossed by White or Black (once left)
            return False
        return True
    
    def get_moves_in_direction(self, x, y, dx, dy, piece_type):
        """Generate all possible moves in one orthogonal direction."""
        moves = []
        new_x, new_y = x + dx, y + dy
        while self.is_valid_move(new_x, new_y, piece_type):
            moves.append((new_x, new_y))
            new_x += dx
            new_y += dy
        return moves

    def get_all_moves_for_piece(self, x, y):
        """Get all possible moves for a piece at position (x, y)."""
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
        """Get all possible moves for the current player (WHITE or BLACK)."""
        all_moves = []
        for x in range(9):
            for y in range(9):
                piece = self.current_board[x][y]
                # print(piece, (x,y), tuple2alfanum((x,y)))
                if turn == 'WHITE' and piece in ['WHITE', 'KING']:
                    piece_moves = self.get_all_moves_for_piece(x, y)
                    if piece_moves:  # Only add if there are moves
                        all_moves.append((x, y, piece_moves))
                        # print(f"Piece at {tuple2alfanum((x, y))} can move to: {[tuple2alfanum(move) for move in piece_moves]}")
                elif turn == 'BLACK' and piece == 'BLACK':
                    piece_moves = self.get_all_moves_for_piece(x, y)
                    if piece_moves:  # Only add if there are moves
                        all_moves.append((x, y, piece_moves))
                        # print(f"Piece at {tuple2alfanum((x, y))} can move to: {[tuple2alfanum(move) for move in piece_moves]}")
        return all_moves

    
if __name__ == "__main__" :
    b = Board()
    
    initial_state = {
        'board': 
            np.array([
                ['EMPTY', 'EMPTY', 'EMPTY', 'BLACK', 'BLACK', 'BLACK', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'WHITE', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'WHITE', 'EMPTY', 'EMPTY', 'EMPTY', 'BLACK'],
                ['BLACK', 'BLACK', 'WHITE', 'WHITE', 'KING', 'WHITE', 'WHITE', 'BLACK', 'BLACK'],
                ['BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'WHITE', 'EMPTY', 'EMPTY', 'EMPTY', 'BLACK'],
                ['EMPTY', 'EMPTY', 'EMPTY', 'WHITE', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['EMPTY', 'EMPTY', 'EMPTY', 'BLACK', 'BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'BLACK', 'BLACK', 'EMPTY', 'EMPTY', 'EMPTY']
            ], dtype='<U5'), 
        'turn': 
            'WHITE'
    }
    
    # # Check corrct constants ==> OK !!
    # copy_check = initial_state['board'].copy()
    # n = initial_state['board'].shape[0]
    # for i in range(n):
    #     for j in range(n):
    #         if (i,j) in CAMPS : copy_check[i][j] = "CAMP"
    #         if (i,j) in ESCAPES : copy_check[i][j] = "ESCAPE"
    #         if (i,j)==CASTLE : copy_check[i][j] = "CASTLE"
    # print(copy_check)
    
    pretty_print(initial_state['board'])
    
    b.load_board(initial_state['board'])
    moves = b.get_all_moves(initial_state['turn'])[0]
    
    _from = moves[0], moves[1]
    _to = moves[2][0]
    
    print(f"Moves: {tuple2alfanum(_from)} --> {tuple2alfanum(_to)}")