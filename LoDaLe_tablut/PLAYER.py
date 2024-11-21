import sys
import time
from socket_manager import SocketManager
from board import Board
from utils import *
from search import Node
import traceback
from timer_procedures import TimerProc

PORT = {"WHITE":5800, "BLACK":5801}

H_FLAGS = ["grey", "1", "2", "3"]

VERBOSE = True      # quickly enable/disable verbose
              

def main():
    
    ## Check that there aren't missing or excessing args ##
    if len(sys.argv) != 5:
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
    
    # - Heuristic FLAG        # TODO: togliere
    h_flag = sys.argv[4]
    if h_flag not in H_FLAGS:
        if VERBOSE : print(f"Wrong heuristic_flag (must be in {H_FLAGS})")
        sys.exit(1)
    
    ## Initialize the socket ##
    sock = SocketManager(ip, port)
    sock.create_socket()
    sock.connect()

    timer = TimerProc("TimerProva", "descrizione")
    
    ###############################################################################
    ### GAME CYCLE ################################################################
    ###############################################################################
    
    try:
        while True:
            initial_time = time.time()
            
            ## 1) Read current state / state updated by the opponent move
            try: current_state = sock.get_state()
            except TypeError: pass # if loses can't read
            board = Board(current_state, timer)

            # if VERBOSE : print(f"Current table:\n{current_state}")
            if VERBOSE : 
                print(f"Current table:\n")
                board.pretty_print()

            # If we are still playing
            match current_state["turn"] :
                case _ if current_state["turn"] == color:
                    if VERBOSE : print("It'sock your turn")

                    ## 2) Compute the move
                    timeout = timeout - (time.time() - initial_time) # consider initialization time   
                    
                    timer.start("total_search_minmax")

                    n = Node(board)  
                    score, move = n.minimax_alpha_beta(
                                maximizing_player=(color=="WHITE"),
                                h_flag=h_flag,
                                depth=3
                            )
                    
                    timer.end("total_search_minmax")

                    if VERBOSE : 
                        print(move)

                    ## 3) Send the move
                    sock.send_move(move.to_alfanum_tuple())
                    
                    ## 4) Read the new updated state after my move
                    current_state = sock.get_state()
                    
                    # memorize my move
                    if VERBOSE : 
                        print(f"After my move:\n")
                        board.pretty_print()
                        
                case "WHITEWIN":
                    if VERBOSE : print("WHITE wins!")
                    print(timer)
                    sys.exit(0)
                    
                case "BLACKWIN":
                    if VERBOSE : print("BLACK wins!")
                    print(timer)
                    sys.exit(0)
                    
                case "DRAW":
                    if VERBOSE : print("It's a draw!")
                    print(timer)
                    sys.exit(0)
                    
                case _ :
                    if VERBOSE : print("Waiting for your opponent move...")

    except Exception:
        if VERBOSE : print(f"An error occurred during the game:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()