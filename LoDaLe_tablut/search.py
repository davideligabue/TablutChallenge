from typing import List, Optional, Callable, Tuple
from board import Board
import random
from utils import *
from collections import deque

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
                                        move=res_moves[i]))
        
        # Build the sibilings of each node
        for n in self.children :
            n.sibilings = self.children.copy().remove(n)
            
        return self.children.copy() 
            
    # TODO: c'è sicuramente altro da implementare
    
    ##############################################################################################################################################################
    # SEARCH ALGORITHMS ##########################################################################################################################################
    ##############################################################################################################################################################
    
    def random_search(self) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]] :
        '''Random search over the children of the given node'''
        nodes = self.get_children()
        return random.choice(nodes).move
    
    def depth_first_search(self, timeout: float) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Performs Depth-First Search (DFS) with a timeout, returning the best move found within the time limit."""
        stack = [self]
        visited = set()
        start_time = time.time()  # Record the start time
        best_node = None  # Track the best node encountered

        while stack:
            # Check if the timeout has been exceeded
            if time.time() - start_time > timeout:
                print("Timeout exceeded during depth-first search")
                return best_node.move if best_node else None

            current_node = stack.pop()
            if current_node.state in visited:
                continue
            visited.add(current_node.state)

            # Check if this is the best node (goal state) encountered so far
            if current_node.state.is_goal_state():  # Assuming the method exists to check for a goal state
                return current_node.move

            # Update the best node as we explore
            if best_node is None or current_node.h < best_node.h:
                best_node = current_node

            # Expand the current node and add its children to the stack
            for child in current_node.get_children():
                stack.append(child)

        # Return the best node move if no goal was found within the time
        return best_node.move if best_node else None

    def breadth_first_search(self, timeout: float) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Performs Breadth-First Search (BFS) with a timeout, returning the best move found within the time limit."""
        queue = deque([self])
        visited = set()
        start_time = time.time()  # Record the start time
        best_node = None  # Track the best node encountered

        while queue:
            # Check if the timeout has been exceeded
            if time.time() - start_time > timeout:
                print("Timeout exceeded during breadth-first search")
                return best_node.move if best_node else None

            current_node = queue.popleft()
            if current_node.state in visited:
                continue
            visited.add(current_node.state)

            # Check if this is the best node (goal state) encountered so far
            if current_node.state.is_goal_state():  # Assuming the method exists to check for a goal state
                return current_node.move

            # Update the best node as we explore
            if best_node is None or current_node.h < best_node.h:
                best_node = current_node

            # Expand the current node and add its children to the queue
            for child in current_node.get_children():
                queue.append(child)

        # Return the best node move if no goal was found within the time
        return best_node.move if best_node else None















##############################################################################
# TEST #######################################################################
##############################################################################

if __name__ == "__main__":
    initial_state = {
    'board': 
        [
            ['EMPTY', 'EMPTY', 'EMPTY', 'BLACK', 'BLACK', 'BLACK', 'EMPTY', 'EMPTY', 'EMPTY'],
            ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
            ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'WHITE', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
            ['BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'WHITE', 'EMPTY', 'EMPTY', 'EMPTY', 'BLACK'],
            ['BLACK', 'BLACK', 'WHITE', 'WHITE', 'KING', 'WHITE', 'WHITE', 'BLACK', 'BLACK'],
            ['BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'WHITE', 'EMPTY', 'EMPTY', 'EMPTY', 'BLACK'],
            ['EMPTY', 'EMPTY', 'EMPTY', 'WHITE', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
            ['EMPTY', 'EMPTY', 'EMPTY', 'BLACK', 'BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
            ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'BLACK', 'BLACK', 'EMPTY', 'EMPTY', 'EMPTY']
        ], 
    'turn': 
        'WHITE'
    }
    
    initial_board = Board(state=initial_state)
    
    # Compute search
    root_node = Node(state=initial_board)
    final_node = root_node.random_search()

    # Verify
    root_node.state.pretty_print()
    move = final_node.move
    print(tuple2alfanum(move[0]), tuple2alfanum(move[1]))
    final_node.state.pretty_print()
    
    # # Esegui un movimento di esempio
    # _from_x, _from_y = 2, 4  
    # _to_x, _to_y = 2, 2 
    # _from = tuple2alfanum((_from_x, _from_y))
    # _to = tuple2alfanum((_to_x, _to_y))
    # initial_board.pretty_print()
    # print(_from, _to, initial_board.board[_from_x][_from_y])

    # try:
    #     initial_board.apply_move((_from_x, _from_y), (_to_x, _to_y))
    # except ValueError as e:
    #     print(e)




##############################################################################
##############################################################################