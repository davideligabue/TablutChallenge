import random
from board_prova import Board

def random_choice(board:Board, turn) :
    all_possible_moves_for_all_pieceS = board.get_all_moves(turn)
    _from_x, _from_y, all_possible_moves_for_one_piece = random.choice(all_possible_moves_for_all_pieceS)
    random_move = random.choice(all_possible_moves_for_one_piece)
    
    return (_from_x, _from_y), random_move
