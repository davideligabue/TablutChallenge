from typing import List, Tuple
from board import Board, Move
from utils import *
import networkx as nx
import matplotlib.pyplot as plt
from heuristics import INF

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
    
    def get_children(self, color) -> List['Node']:
        # Lazy loading
        if len(self.children) != 0: 
            return self.children
        else :
            backtrack_moves = self.board.apply_moves(self.state)
            moves = self.board.get_all_moves(color, self.state)
            self.board.reverse_moves(backtrack_moves)
            for m in moves: # all the pieces
                # Update the list of moves
                new_state = self.state.copy()
                new_state.append(m)
                self.children.append(Node(
                    board=self.board,
                    state=new_state,
                    depth=self.depth+1,
                ))        
            return self.children
        
    def plot_tree(self, heuristic=None):
        def add_edges_and_nodes(graph, node, parent=None):
            # Converte lo stato in stringa per usarlo come etichetta univoca
            label = str(node.state)
            if heuristic:
                # Applica le mosse di backtrack per calcolare l'euristica
                backtrack_moves = node.board.apply_moves(node.state)
                h_value = heuristic(node.board)
                node.board.reverse_moves(backtrack_moves)
                label += f"\n(h={h_value})"

            # Aggiunge il nodo al grafo
            graph.add_node(label)
            if parent:
                graph.add_edge(parent, label)

            # Aggiunge ricorsivamente i figli
            for child in node.children:
                add_edges_and_nodes(graph, child, label)

        # Creazione del grafo
        graph = nx.DiGraph()
        root_label = str(self.state)  # Usa la rappresentazione stringa dello stato root
        add_edges_and_nodes(graph, self)

        # Funzione per generare le posizioni per il layout ad albero
        def hierarchy_pos(G, root=None, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5):
            def _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter, pos=None, parent=None):
                if pos is None:
                    pos = {root: (xcenter, vert_loc)}
                else:
                    pos[root] = (xcenter, vert_loc)
                children = list(G.neighbors(root))
                if not isinstance(G, nx.DiGraph) and parent is not None:
                    children.remove(parent)
                if len(children) != 0:
                    dx = width / len(children)
                    nextx = xcenter - width / 2 - dx / 2
                    for child in children:
                        nextx += dx
                        pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                            vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos,
                                            parent=root)
                return pos

            return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)

        # Verifica che il nodo radice sia presente nel grafo
        # if root_label not in graph.nodes:
        #     raise ValueError(f"Il nodo radice '{root_label}' non è presente nel grafo. "
        #                     f"Nodi disponibili: {list(graph.nodes)}")

        # Genera il layout e disegna il grafo
        
        # CUSTOM
        # pos = hierarchy_pos(graph, root=root_label)
        
        pos = nx.nx_pydot.pydot_layout(graph, prog="dot")  # Migliore per strutture ad albero

        plt.figure(figsize=(12, 8))
        nx.draw(graph, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold")
        plt.title("Tree Plot")
        plt.show()

    ##############################################################################################################################################################
    # SEARCH ALGORITHMS ##########################################################################################################################################
    ##############################################################################################################################################################    
    
    def minimax_alpha_beta(
            self,
            maximizing_player: bool,
            depth: int,
            heuristic: callable,
            alpha: float = -INF,
            beta: float = INF
        ) -> Tuple[int, Move]:
        
        # Determina il colore del giocatore corrente
        color = "WHITE" if maximizing_player else "BLACK"

        # Caso base: profondità 0 o nodo foglia
        if depth == 0 or not self.get_children(color):
            backtrack_moves = self.board.apply_moves(self.state)
            score = heuristic(self.board) / self.depth
            self.board.reverse_moves(backtrack_moves)
            return score, None

        # Inizializza i valori per il calcolo
        best_move = None
        res_eval = -INF if maximizing_player else INF

        # Itera sui figli del nodo corrente
        for child in self.get_children(color):
            eval, _ = child.minimax_alpha_beta(
                maximizing_player=not maximizing_player,
                depth=depth - 1,
                heuristic=heuristic,
                alpha=alpha,
                beta=beta
            )

            if maximizing_player:
                if eval >= res_eval:
                    res_eval = eval
                    best_move = child.state[-1]
                alpha = max(alpha, eval)
            else:
                if eval <= res_eval:
                    res_eval = eval
                    best_move = child.state[-1]
                beta = min(beta, eval)

            if beta <= alpha:
                break

        return res_eval, best_move
