from typing import List, Optional, Callable, Tuple
from board import Board
import random
from utils import *
from collections import deque

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
            
    def predict_opponent(self, node: 'Node', depth: int, remaining_time: float, start_time: float) -> Optional['Node']:
        """
        Simulates the opponent's best move using minimax with depth-limited search.
        Handles timeout by returning the best move found so far.
        """
        if remaining_time <= 0 or depth == 0 or node.state.is_goal_state():
            return node  # No further prediction or goal state reached

        opponent_best_move = None
        if node.state.turn == "OPPONENT":
            # Simulate opponent trying to minimize our score (minimization)
            min_value = float('inf')
            for child in node.get_children():
                # Check for timeout
                if time.time() - start_time > remaining_time:
                    return opponent_best_move
                predicted_move = self.predict_opponent(child, depth - 1, remaining_time - (time.time() - start_time), start_time)
                if predicted_move and predicted_move.h < min_value:
                    min_value = predicted_move.h
                    opponent_best_move = predicted_move
        else:
            # Our turn, try to maximize score (maximization)
            max_value = float('-inf')
            for child in node.get_children():
                # Check for timeout
                if time.time() - start_time > remaining_time:
                    return opponent_best_move
                predicted_move = self.predict_opponent(child, depth - 1, remaining_time - (time.time() - start_time), start_time)
                if predicted_move and predicted_move.h > max_value:
                    max_value = predicted_move.h
                    opponent_best_move = predicted_move

        return opponent_best_move

    
    ##############################################################################################################################################################
    # SEARCH ALGORITHMS ##########################################################################################################################################
    ##############################################################################################################################################################
    
    def random_search(self) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]] :
        '''Random search over the children of the given node'''
        nodes = self.get_children()
        return random.choice(nodes).move
    
    def depth_first_search(self, timeout: float) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        '''Depth-First Search (DFS) from the given node'''
        stack = [self]
        visited = set()
        start_time = time.time()  # Record the start time
        best_node = None  # Track the best node encountered

        while stack:
            # Check if the timeout has been exceeded
            if time.time() - start_time > timeout:
                if VERBOSE : 
                    print("Timeout exceeded during depth-first search")
                    print(best_node.move)
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
        '''Breadth-First Search (BFS) from the given node'''
        queue = deque([self])
        visited = set()
        start_time = time.time()  # Record the start time
        best_node = None  # Track the best node encountered

        while queue:
            # Check if the timeout has been exceeded
            if time.time() - start_time > timeout:
                if VERBOSE : 
                    print("Timeout exceeded during breadth-first search")
                    print(best_node.move)
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

    def greedy_best_first_search(self, timeout: float) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        '''Greedy Best-First Search from the given node'''
        start_time = time.time()
        priority_queue = [self]  # Min-heap based on heuristic value h(n)
        visited = set()
        best_node = None  # Keep track of the best node found so far

        while priority_queue:
            if time.time() - start_time > timeout:
                if VERBOSE:
                    print("Timeout exceeded during Greedy Best-First Search")
                return best_node.move if best_node else None

            current_node = min(priority_queue, key=lambda n: n.h)
            priority_queue.remove(current_node)
            
            if current_node.state in visited:
                continue
            visited.add(current_node.state)

            # Update the best node found so far
            if best_node is None or current_node.h < best_node.h:
                best_node = current_node

            # Check if we've reached the goal
            if current_node.state.is_goal_state():
                return current_node.move

            # Expand children and add them to the priority queue
            for child in current_node.get_children():
                if child.state not in visited:
                    priority_queue.append(child)

        return best_node.move if best_node else None

    def a_star_search(self, timeout: float) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        '''A* search from the given node'''
        start_time = time.time()
        priority_queue = [self]  # Min-heap based on f(n) = g(n) + h(n)
        visited = set()
        best_node = None  # Keep track of the best node found so far

        while priority_queue:
            if time.time() - start_time > timeout:
                if VERBOSE:
                    print("Timeout exceeded during A* search")
                return best_node.move if best_node else None

            current_node = min(priority_queue, key=lambda n: n.g + n.h)
            priority_queue.remove(current_node)

            if current_node.state in visited:
                continue
            visited.add(current_node.state)

            # Update the best node found so far
            if best_node is None or (current_node.g + current_node.h) < (best_node.g + best_node.h):
                best_node = current_node

            # Check if we've reached the goal
            if current_node.state.is_goal_state():
                return current_node.move

            # Expand children and add them to the priority queue
            for child in current_node.get_children():
                if child.state not in visited:
                    child.g = current_node.g + 1  # Increment the path cost
                    priority_queue.append(child)

        return best_node.move if best_node else None

    def a_star_with_opponent_prediction(self, depth: int, timeout: float) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        A* search with opponent move prediction.
        The algorithm predicts the opponent's best responses up to `depth` moves.
        Handles timeout by returning the best move found so far.
        """
        start_time = time.time()
        priority_queue = [self]  # Min-heap based on f(n) = g(n) + h(n)
        visited = set()
        best_node = None  # Keep track of the best node found so far

        while priority_queue:
            # Check for timeout
            if time.time() - start_time > timeout:
                if VERBOSE:
                    print("Timeout exceeded during A* search with opponent prediction")
                return best_node.move if best_node else None

            # Get the current node with the lowest f(n)
            current_node = min(priority_queue, key=lambda n: n.g + n.h)
            priority_queue.remove(current_node)

            if current_node.state in visited:
                continue
            visited.add(current_node.state)

            # Update the best node found so far
            if best_node is None or (current_node.g + current_node.h) < (best_node.g + best_node.h):
                best_node = current_node

            # Check if we've reached the goal
            if current_node.state.is_goal_state():
                return current_node.move

            # Expand children (our moves) and consider opponent's response
            for child in current_node.get_children():
                if child.state not in visited:
                    child.g = current_node.g + 1  # Increment the path cost
                    # Predict opponent's response for the given depth
                    opponent_move = self.predict_opponent(child, depth, timeout - (time.time() - start_time), start_time)
                    if opponent_move:
                        priority_queue.append(opponent_move)
                    else:
                        priority_queue.append(child)

        return best_node.move if best_node else None