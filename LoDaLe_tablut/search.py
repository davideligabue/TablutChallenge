from typing import List, Optional, Callable, Tuple
from board import Board
import random
from utils import *
from collections import deque
from heuristics import black_heuristics, white_heuristics, grey_heuristic
import math

VERBOSE = True

class Node:
    
    ##############################################################################################################################################################
    # NODE REPRESENTATION ########################################################################################################################################
    ##############################################################################################################################################################
    
    def __init__(   
            self,  
            state: Board, 
            parent: Optional['Node'] = None, 
            sibilings: List['Node'] = None,
            depth: int = 0, 
            g: int = 0, 
            h: Optional[Callable[[Board], float]] = None,
            move: Tuple[Tuple[int, int], Tuple[int, int]]=None
        ):
        
        # Attributes
        self.state = state
        self.parent = parent                # None if it is the root
        self.children = []                  
        self.sibilings = sibilings          # None if it is the root
        self.depth = depth                  # 0 if is the root
        self.g = g                          # Cost to reach this node
        self.h = h(state) if h else 0       # Estimation of the cost to reach the goal
        self.move = move                    # The move which led to this state
        
    def add_neighbor(self, neighbor_node: Optional['Node'] | List['Node']):
        if isinstance(neighbor_node, Node):
            self.neighbors.append(neighbor_node)
        elif isinstance(neighbor_node, list):  # In case we want to append all the neighbors at once
            self.neighbors.extend(neighbor_node)

    def __eq__(self, other: 'Node') -> bool:
        return self.state == other.state

    def __lt__(self, other: 'Node') -> bool:
        return (self.g + self.h) < (other.g + other.h)
    
    def __repr__(self) -> str:
        return f"Node({self.state})"
    
    def get_children(self):
        moves = self.state.get_all_moves()
        children_boards = []
        res_moves = []
        for m in moves: # all the pieces
            _from_x, _from_y, _to_list = m
            for _to in _to_list : # all the moves for a piece
                board_copy = self.state.board.copy() # Copy otherwise we modify the actual state
                _to_x, _to_y = _to
                
                b = Board({"board":board_copy, "turn":self.state.turn})
                move = (_from_x, _from_y), (_to_x, _to_y)
                b.apply_move((_from_x, _from_y), (_to_x, _to_y))
                
                children_boards.append(b)
                res_moves.append(move)
            
        # Build the nodes
        for i, b in enumerate(children_boards):
            self.children.append(Node(  state=b, 
                                        parent=self, 
                                        depth=self.depth+1,
                                        move=res_moves[i]
                                    )
                                )
        
        # Build the sibilings of each node
        for n in self.children :
            n.sibilings = self.children.copy().remove(n)
            
        return self.children.copy() 
    
    ##############################################################################################################################################################
    # SEARCH ALGORITHMS ##########################################################################################################################################
    ##############################################################################################################################################################
    
    def random_search(self) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]] :
        '''Random search over the children of the given node'''
        nodes = self.get_children()
        return random.choice(nodes).move
    
    
    def minimax_alpha_beta(
            self, 
            depth: int, 
            alpha: float = -float('inf'), 
            beta: float = float('inf')
        ) -> Tuple[int, Optional[Tuple[Tuple[int, int], Tuple[int, int]]]]:

    
        maximizing_player = (self.state.turn == "WHITE")
        best_move = None  

        # If the node is at the maximum depth or is a leaf
        if depth == 0 or not self.get_children():
            return grey_heuristic(self.state), None
        
        if maximizing_player:
            max_eval = -float('inf')
            for child in self.get_children():
                eval, _ = child.minimax_alpha_beta(depth - 1, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    best_move = child.move  # Update best move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta Cutoff
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for child in self.get_children():
                eval, _ = child.minimax_alpha_beta(depth - 1, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    best_move = child.move  # Update best move
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha Cutoff
            return min_eval, best_move
