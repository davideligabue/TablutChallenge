import random
import sys
import numpy as np
import time
from socket_manager import SocketManager
from board import Board
from utils import *

PORT = {"WHITE":5800, "BLACK":5801}
V = True # in order to quickly enable or disable verbose

def main():
    
    ## Check that there aren't missing or excessing args ##
    if len(sys.argv) != 4:
        if V : print("Wrong number of args, it should be: python3 __main__.py <color(White/Black)> <timeout(seconds)> <IP_server>")
        sys.exit(1)
    
    ## Check args are corrected ##
    # - Color
    color = sys.argv[1].upper()
    if color not in PORT.keys():
        if V : print("Wrong color, it should be \"White\" or \"Black\"")
        sys.exit(1)
        
    # - Timeout
    try:
        timeout = int(sys.argv[2])
    except ValueError:
        if V : print("Wrong timeout, it should be an integer")
        sys.exit(1)
    
    # - Ip address + 
    ip = sys.argv[3]          
    if not check_ip(ip):
        if V : print("Wrong ip format")
        sys.exit(1)
    port = PORT[color]
    
    ## Initialize the socket ##
    s = SocketManager(ip, port)
    s.create_socket()
    s.connect()
    
    ###############################################################################
    ### GAME CYCLE ################################################################
    ###############################################################################
    
    # May be useful
    boards_history = []     # List of the boards, useful to track the game
    b = Board()
    
    try:
        while True:
            initial_time = time.time()
            
            # 1) Read current state / state updated by the opponent move
            current_state = s.get_state()
            board = current_state['board']
            turn = current_state['turn']
            
            # Memorize opponent move
            boards_history.append(board) 
            b.load_board(board)

            # if V : print(f"Current table:\n{current_state}")
            if V : print(f"Current table:\n"); pretty_print(b.current_board)

            # If we are still playing
            if turn == color:
                if V : print("It's your turn")

                # 2) Compute the move
                timeout = timeout - (time.time() - initial_time) # consider initialization time
                
                ### AI STUFF f(timeout, board) [forse board_history ??] ####
                # 1) RANDOM PLAYER #########################################
                all_possible_moves_for_all_pieceS = b.get_all_moves(turn)
                _from_x, _from_y, all_possible_moves_for_one_piece = random.choice(all_possible_moves_for_all_pieceS)
                random_move = random.choice(all_possible_moves_for_one_piece)
                
                # 2) ...
                
                #####
                
                # Translate 
                _from = tuple2alfanum((_from_x, _from_y))
                _to = tuple2alfanum(random_move)
                
                move = (_from, _to, color) 
                if V : print(f"Move: {move}")
                
                # 3) Send the move
                s.send_move(move)
                
                # 4) Read the new updated state after my move
                current_state = s.get_state()
                board = current_state['board']
                turn = current_state['turn']
                
                # memorize my move
                boards_history.append(board) 
                b.load_board(board)
                if V : print(f"After my move:\n"); pretty_print(b.current_board)
                    
            # Else the game ends for many reasons
            elif current_state['turn'] == "WHITEWIN":
                if V : print("WHITE wins!")
                sys.exit(0)
            elif current_state['turn'] == "BLACKWIN":
                if V : print("BLACK wins!")
                sys.exit(0)
            elif current_state['turn'] == "DRAW":
                if V : print("It's a draw!")
                sys.exit(0)
            else:
                if V : print("Waiting for your opponent move...")

    except Exception as e:
        if V : print(f"An error occurred during the game: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()