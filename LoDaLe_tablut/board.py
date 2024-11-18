import numpy as np
from utils import *

# CONSTANTS
WHITE = "WHITE"
BLACK = "BLACK"
KING = "KING"
EMPTY = "EMPTY"
CASTLE = (4, 4)

CAMPS = {   
    "upper" : [(0,3), (0,4), (0,5), (1,4)],     # upper camps
    "lower" : [(8,3), (8,4), (8,5), (7,4)],     # lower camps
    "left" : [(3,0), (4,0), (5,0), (4,1)],     # left camps
    "right" : [(3,8), (4,8), (5,8), (4,7)]      # right camps
}
CAMPS["all"] = CAMPS["upper"] + CAMPS["lower"] + CAMPS["left"] + CAMPS["right"]

ESCAPES = {   
    "up-left" : [(0,1), (0,2), (1,0), (2,0)],     # upper-left escapes
    "low-left" : [(6,0), (7,0), (8,1), (8,2)],     # lower-left escapes
    "low-right" : [(8,6), (8,7), (6,8), (7,8)],     # lower-right escapes
    "up-right" : [(0,6), (0,7), (1,8), (2,8)]      # upper-right escapes
}
ESCAPES["all"] = ESCAPES["up-left"] + ESCAPES["low-left"] + ESCAPES["low-right"] + ESCAPES["up-right"]

ROMBUS_POS = [
            (1,2),       (1,6),
    (2,1),                      (2,7),

    (6,1),                      (6,7),
            (7,2),       (7,6)
]
ROMBUS_POS = np.array(ROMBUS_POS)

ESCAPE_COVER = [
    (1,1),(1,2),        (1,6),(1,7),
    (2,1),                    (2,7),

    (6,1),                    (6,7),
    (7,1),(7,2),        (7,6),(7,7)
]
ESCAPE_COVER = np.array(ESCAPE_COVER)

DOUBLE_ESCAPE_COVER = [
    (1,1),          (1,7),

    (7,1),          (7,7)
]
DOUBLE_ESCAPE_COVER = np.array(DOUBLE_ESCAPE_COVER)

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

class Move:
    def __init__(self, start:tuple, end:tuple, piece, is_capture = False):
        self.is_capture = is_capture
        if is_capture:
            self.start = start
            self.end = self.start
            self.piece = piece
            return
        if self.is_within_bounds(end):
            self.start = start
            self.end = end
        else:
            raise Exception("'Move' class detected non valid x,y position")
        if not self.is_orthogonal():
            raise Exception("'Move' class detected non orthogonal move")
        if piece == WHITE or piece == BLACK or piece == KING:
            self.piece = piece
        else:
            raise Exception("'Move' class detected non valid piece")
        
    def is_within_bounds(self, pos):
        return 0 <= pos[0] < 9 and 0 <= pos[1] < 9
    
    def is_orthogonal(self):
        return (self.start[0] == self.end[0]) or (self.start[1] == self.end[1])

class Board:

    def __init__(self, state):
        self.turn = state['turn']
        self.board = np.array(state['board'])
        king_pos = np.where(self.board == KING)
        if king_pos[0].size == 0:
            self.king = None
        elif king_pos[0].size == 1:
            self.king = (king_pos[1][0], king_pos[0][0])
        else:
            raise Exception("More than one king in the board") 
    
    # controlla se la data posizione è interna alla griglia  ?? da togliere perchè aggiunto come metodo statico di classe Move
    def is_within_bounds(self, pos):
        return 0 <= pos[0] < 9 and 0 <= pos[1] < 9

    # controlla se due pezzi sono di fazione diversa
    def is_opponent_piece(self, piece_one, piece_two):
        if (piece_one == WHITE and piece_two == KING) or (piece_one == KING and piece_two == WHITE):
            return False
        if piece_one != piece_two:
            return True
        return False

    # controlla se una casella è speciale ?? non capisco perchè dovrebbe interessare se è speciale senza distinguere castle o camps
    def is_special_tile(self, pos):
        # Castle and camp positions are pre-defined (as constants or in the board setup)
        if (pos[0], pos[1]) == CASTLE["all"]:
            return True
        if (pos[0], pos[1]) in CAMPS["all"]:
            return True
        return False
    
    def get_cell(self, pos): 
        if self.is_within_bounds(pos):
            return self.board[pos[0]][pos[1]]
        else:
            raise Exception("Trying to get value from out of bounds cell")
    
    # given a segment of cells identified by starting position pos1 and end position pos2
    # returns a string which gives a summary of the content of each cell ordered from pos1 to pos2
    # in the segment (starting point not included, end point included), format example: 'bbwee...' there are two blacks, one white and two empty
    def segment_occupation(self, pos1, pos2) -> dict:
        str_result = ""
        cells_result = []
        delta = (pos2[0]-pos1[0],pos2[1]-pos1[1])
        # when the move is vertical
        if delta[0] == 0:
            sign = np.sign(delta[1])
            for i in range( sign, delta[1]+sign, sign ):
                # get the frist letter of each cell in the path of the segment B for black W for white E for empty K for king
                str_result += self.get_cell((pos1[0], pos1[1]+i))[0]
                cells_result.append( (pos1[0], pos1[1]+i) )
        # when the move is orizontal
        elif delta[1] == 0:
            sign = np.sign(delta[0])
            for i in range( sign, delta[0]+sign, sign ):
                # get the frist letter of each cell in the path of the segment B for black W for white E for empty K for king
                str_result += self.get_cell((pos1[0]+i, pos1[1]))[0]
                cells_result.append( (pos1[0]+i, pos1[1]) )
        return {"str":str_result, "cells":cells_result}
    
    # given a center in the grid, it returns the Summary Object for the cells in the ring (of radius 1 or 2)
    # the Summary Object is a dictionary which has under the key "str" the string containing the info about cell occupations,
    # under the key "cells" the position tuple corresponding to the string letter
    def ring_occupation(self, center, radius) -> dict:
        str_result = ""
        cell_result = []
        if radius < 1 or radius > 2:
            raise Exception("In 'ring_occupation' radius must be either 1 or 2")
        # take the corners of the ring around the center (in order: top-left, top-right, bottom-right, bottom-left)
        corners = [(center[0]-radius, center[1]-radius),(center[0]+radius, center[1]-radius),(center[0]+radius, center[1]+radius),(center[0]-radius, center[1]+radius)]
        for corner in corners:
            # if the corner is outside the grid return None
            if not self.is_within_bounds(corner):
                return None
        # get the summary object for the content of the ring, using the method 'segment_occupation'
        # the resulting object is composed by the cells of the content of cells starting from top left corner (not included) going in 
        # clockwise direction (until it includes the top left corner)
        for i in range(4):
            occupation_obj = self.segment_occupation(corners[i%4], corners[(i+1)%4])
            str_result += occupation_obj["str"]
            for cell in occupation_obj["cells"]:
                cell_result.append( cell )
        return {"str": str_result, "cells": cell_result}
    
    # check whether pos1 and pos2 positions are adjacent on the grid (they have a common side)
    def is_adjacent(self, pos1, pos2):
        delta = (pos1[0]-pos2[0], pos1[1]-pos2[1])
        return (delta[0] == 0 and abs(delta[1]) == 1) or (delta[1] == 0 and abs(delta[0]) == 1)

    def is_valid_move(self, move:Move):
        # The starting position must contain the piece specified in move
        if self.get_cell(move.start) != move.piece:
            return False
       
        # this check shouldn't be needed, all the Moves should altready be through empty spaces
        # for the traversed path every cell must be empty
        #segment_info = self.segment_occupation(move.start, move.end)
        #for char in segment_info:
            #if char != EMPTY[0]:
                #return False
        
        # only the king can move in the castle
        if move.end == CASTLE and move.piece != KING:
            return False
        
        # only the black can move in camps
        if move.end in CAMPS['all'] and move.piece != BLACK:
            return False
        
        # if a black piece is outside a camp it cannot re-enter
        if (move.end in CAMPS['all']) and (move.start not in CAMPS['all']):
            return False
        
        ## ???? non trovo il senso di questo controllo

        # For the king, check if it is moving towards an escape point
        #if piece_type == 'KING' and (to_x, to_y) in ESCAPES:
            # The king can only move to an escape if there is a clear path (no black pieces in the way)
            #if not self.is_escape_clear(to_x, to_y):
                #return False
        
        # If all checks pass, the move is valid
        return True
    
    def is_king_escaped(self):
        return self.king in ESCAPES["all"]
    
    def is_king_captured(self):
        return self.king == None
    
    # returns a tuple (True, pos) if this move brings to the capture of a piece in the 'pos' position
    # else it returns (False, xx). IT DOESN'T CHECK WHETHER IS A VALID MOVE (you should check before calling this method)
    def is_a_capture_move(self, move: Move):
        # if the moving piece is black, check if it is capturing the king
        if move.piece == BLACK:
            # if the end position of the move has a king adjacent
            if self.is_adjacent(move.end, self.king):
                # check the surrounding of the king in even positions (up, down, left, right)
                king_surround = self.ring_occupation(CASTLE, 1)
                black_occupation = find_all(king_surround["str"], BLACK[0])
                blacks_in_even_position = 0
                for index in black_occupation:
                    if index % 2 == 0:
                        blacks_in_even_position += 1
                # If the King is in the Castle, it must be already surrounded on 3 sides (the 4th is the end position of this move)
                if self.king == CASTLE:
                    return (blacks_in_even_position==3, self.king)
                # if the king is adjacent to the castle, it must be already surrounded on 2 sides (the 3rd is the end position of this move)
                if self.is_adjacent(self.king, CASTLE):
                    return (blacks_in_even_position==2, self.king)
                # if the end position makes the king between a black piece and a camp, it is a capture
                # check for every even surrounding cell if the king has on opposite sides the end of this move and a camp
                for cell in king_surround["cells"]:
                    if cell in CAMPS["all"]:
                        delta = (cell[0]-move.end[0], cell[1]-move.end[1])
                        if (delta[0] == 0 and abs(delta[1]) == 2) or (delta[1] == 0 and abs(delta[0]) == 2):
                            return (True, self.king)
        # now all the general rules for all checkers BLACK, WHITE and KING
        surround = self.ring_occupation(move.end, 1) # take the surround of the move end point
        string_indexes = []
        if move.piece == WHITE or move.piece == KING: # if the moved piece is white or king we are interested in black 
            string_indexes = find_all(surround["str"], BLACK[0])
        if move.piece == BLACK: # if the moved piece is black we are interested in white
            string_indexes = find_all(surround["str"], WHITE[0])
        # for each surrounding adversary
        for elem in string_indexes:
            if elem % 2 == 0:
                # at this point elem is an adjacent adversary 1.1 0.1  1.0
                delta = (move.end[0] - surround["cells"][elem][0], move.end[1] - surround["cells"][elem][1])
                opposite_cell_coordinates = (surround["cells"][elem][0] - delta[0], surround["cells"][elem][1] - delta[1])
                if self.get_cell(opposite_cell_coordinates) == move.piece: # it means that the cell of the adversary is between an ally and your next move, so this move is a capture
                    return (True, (surround["cells"][elem][0], surround["cells"][elem][1]))
                # check if the opposite cell is the castle, or a camp. In this case this move is a capture
                if opposite_cell_coordinates == CASTLE or opposite_cell_coordinates in CAMPS["all"]:
                    return (True, (surround["cells"][elem][0], surround["cells"][elem][1]))
        return (False, None)
        
    # take a position on the grid and returns the list of all possible legal moves for that piece
    def get_all_moves_for_piece(self, pos):
        if not self.is_within_bounds(pos):
            raise Exception("Position not in the grid for 'get_all_moves_for_piece' call")
        piece = self.get_cell(pos)
        if piece == EMPTY:
            raise Exception("Empty piece when calling 'get_all_moves_for_piece'")
        # coordinates of all the cells on the border of the grid moving orthogonally
        borders = [(pos[0], 0), (9, pos[1]), (pos[0], 9), (0, pos[1])]
        segment_occupations = [self.segment_occupation(pos, borders[0]), 
                               self.segment_occupation(pos, borders[1]),
                               self.segment_occupation(pos, borders[2]),
                               self.segment_occupation(pos, borders[3])]
        result = []
        for direction in segment_occupations:
            for i in range(len(direction["str"])):
                if direction["str"][i] != EMPTY[0]:
                    break
                move = Move(pos, direction["cells"][i], piece)
                if self.is_valid_move(move):
                    result.append(move)
        return result
    
    # given a list of Move, it applies them in order (the moves are supposed to be altready legal)
    def apply_moves(self, moves_list:list):
        sequence_list = []
        for move in moves_list:
            self.board[move.start[0]][move.start[1]] = EMPTY
            self.board[move.end[0]][move.end[1]] = move.piece
            if move.piece == KING:
                self.king = move.end
            sequence_list.append(move)
            # check if there is a capture to perform
            capturing_result = self.is_a_capture_move(move)
            if capturing_result[0]:
                captured_piece = self.board[capturing_result[1][0]][capturing_result[1][1]]
                self.board[capturing_result[1][0]][capturing_result[1][1]] = EMPTY
                # add the capture action to the sequence list so it can be tracked down and eventually reversed
                sequence_list.append(Move((capturing_result[1][0], capturing_result[1][1]), 0, captured_piece, True))
                if captured_piece == KING:
                    self.king = None
        return sequence_list
    
    # given a list of Move, it applies them in reverse order and from end to start (the moves are supposed to be altready legal)
    def reverse_moves(self, sequence_list:list,):
        for move in sequence_list[::-1]:
            if move.is_capture:
                self.board[move.start[0]][move.start[1]] = move.piece
                if move.piece == KING:
                    self.king = (move.start[0], move.start[1])
            else:
                self.board[move.end[0]][move.end[1]] = EMPTY
                self.board[move.start[0]][move.start[1]] = move.piece
                if move.piece == KING:
                    self.king = move.start
    
    # returns all the current possible moves in the board, based on the specified color
    def get_all_moves(self, color):
        # select the right mask based on color
        mask = None
        result = []
        if color == WHITE:
            mask = (self.board == WHITE) | (self.board == KING)
        elif color == BLACK:
            mask = (self.board == BLACK)
        positions = np.where(mask)
        for i in range(len(positions[0])):
            moves = self.get_all_moves_for_piece((positions[0][i], positions[1][i]))
            for mv in moves:
                result.append(mv)
        return result

    
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