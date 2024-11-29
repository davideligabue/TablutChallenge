import sys
import time
from socket_manager import SocketManager
from board import Board
from utils import *
from search import Node
import traceback
from heuristics import grey_heuristic, heuristic_1, heuristic_2, heuristic_3
import random


PORT = {"WHITE":5800, "BLACK":5801}

VERBOSE = False      # quickly enable/disable verbose
              
def main():
    
    ## Check that there aren't missing or excessing args ##
    if len(sys.argv) < 4:
        if VERBOSE : print("Wrong number of args, it should be: python3 __main__.py <color(White/Black)> <timeout(seconds)> <IP_server>")
        sys.exit(1)
    
    ## Check args are corrected ##
    # - Color
    color = sys.argv[1].upper()
    if color not in PORT.keys():
        if VERBOSE : print("Wrong color, it should be \"White\" or \"Black\"")
        sys.exit(1)
        
    # - Timeout
    try:
        timeout = int(sys.argv[2])
    except ValueError:
        if VERBOSE : print("Wrong timeout, it should be an integer")
        sys.exit(1)
    
    # - Ip address 
    ip = sys.argv[3]          
    if not check_ip(ip):
        if VERBOSE : print("Wrong ip format")
        sys.exit(1)
    port = PORT[color]
    
    sock = SocketManager(ip, port, player_name="LoDaLe") # ho tolto LoDaLe solo per il limite di caratteris
    sock.create_socket()
    sock.connect()
    
    ###############################################################################
    ### GAME CYCLE ################################################################
    ###############################################################################
    
    err_count = 0
    try:
        while True:
            
            ## 1) Read current state / state updated by the opponent move
            try: current_state = sock.get_state()
            except TypeError: 
                if err_count==0 : 
                    err_count += 1
                    pass # if loses can't read
                else : raise Exception("Server error")
            board = Board(current_state)

            if VERBOSE : 
                print(f"Current table:\n")
                board.pretty_print()

            # If we are still playing
            if current_state["turn"] == color:
                if VERBOSE : print("It's your turn")

                ## 2) Compute the move
                timeout = timeout - (time.time() - initial_time) # consider initialization time   
                # Initialize current node
                n = Node(board)  

                heuristic = grey_heuristic

                # Call alpha-beta pruning
                score, move = n.minimax_alpha_beta(
                    maximizing_player=(color=="WHITE"),
                    depth=3,
                    heuristic=heuristic
                )

                if VERBOSE : 
                    print("\nExploration recap:")
                    # n.plot_tree(heuristic=heuristic)
                    print(f"- Score={score}")
                    print(f"- Nodes_explored={n.get_num_nodes("explored")}")
                    print(f"- Time={round(time.time()-initial_time, 3)}s")
                    print()
                            

                if VERBOSE : print(move)

                ## 3) Send the move
                sock.send_move(move.to_alfanum_tuple())
                
                ## 4) Read the new updated state after my move
                current_state = sock.get_state()
                board = Board(current_state) 
                
                if VERBOSE : 
                    print(f"After my move:\n")
                    board.pretty_print()
              
                    
            if current_state["turn"] == "WHITEWIN":
                if VERBOSE : print("WHITE wins!")
                sys.exit(0)
                
            if current_state["turn"] == "BLACKWIN":
                if VERBOSE : print("BLACK wins!")
                sys.exit(0)
                
            if current_state["turn"] == "DRAW":
                if VERBOSE : print("It's a draw!")
                sys.exit(0)
                
            else :
                if VERBOSE : print("Waiting for your opponent move...")

    except Exception:
        if VERBOSE : print(f"An error occurred during the game:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()