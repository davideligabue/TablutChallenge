from typing import List, Tuple
from board import Board, Move
from utils import *
from heuristics import grey_heuristic, heuristic_1, heuristic_2, heuristic_3

VERBOSE = True

class Node:
    
    ##############################################################################################################################################################
    # NODE REPRESENTATION ########################################################################################################################################
    ##############################################################################################################################################################
    
    def __init__(   
            self,  
            board: Board,
            state: List[Move] = [], 
            depth: int = 0
        ):
        
        # Attributes
        self.board = board
        self.state = state
        self.children = []                  
        self.depth = depth                  # 0 if is the root

    def __eq__(self, other: 'Node') -> bool:
        return self.state == other.state
    
    def __repr__(self) -> str:
        return f"Node({self.state})"
    
    def get_children(self, color):
        # Lazy loading
        if len(self.children) != 0: 
            return self.children
        else :
            moves = self.board.get_all_moves(color, self.state)
            for m in moves: # all the pieces
                new_state = self.state.copy()
                new_state.append(m)
                self.children.append(Node(
                    board=self.board,
                    state=new_state,
                    depth=self.depth+1
                ))        
            return self.children
            
    ##############################################################################################################################################################
    # SEARCH ALGORITHMS ##########################################################################################################################################
    ##############################################################################################################################################################    
    
    def minimax_alpha_beta(
            self, 
            maximizing_player: bool,
            h_flag: str,
            depth: int, 
            alpha: float = -float('inf'), 
            beta: float = float('inf')
        ) -> Tuple[int, Move]:

        best_move = None  
        color = "WHITE" if maximizing_player else "BLACK"

        # Se siamo alla profondità massima o in un nodo fogli
        if (depth==0) or (len(self.get_children(color))==0):
            match h_flag:
                case "1" : heuristic = heuristic_1
                case "2" : heuristic = heuristic_2
                case "3" : heuristic = heuristic_3
                case "grey" : heuristic = grey_heuristic
            return heuristic(self.board), None  

        max_eval = -float('inf')
        min_eval = float('inf')
        for child in self.get_children(color):
            print(maximizing_player, alpha, beta)
            eval, move = child.minimax_alpha_beta(
                maximizing_player=not maximizing_player,
                h_flag=h_flag, 
                depth=depth - 1,
                alpha=alpha, 
                beta=beta
            )
            
            if maximizing_player:
                if eval > max_eval:
                    max_eval = eval
                    best_move = child.state[-1]  
                alpha = max(alpha, eval)
                res_eval = max_eval
            else :
                if eval < min_eval:
                    min_eval = eval
                    best_move = child.state[-1]  
                beta = min(beta, eval)
                res_eval = min_eval
            if beta <= alpha:
                break  # Beta Cutoff
        return res_eval, best_move