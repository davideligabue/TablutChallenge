from typing import List, Tuple
import networkx as nx
import matplotlib.pyplot as plt
import random

VERBOSE = True
ID = 0

class Node:
    
    ##############################################################################################################################################################
    # NODE REPRESENTATION ########################################################################################################################################
    ##############################################################################################################################################################
    
    def __init__(   
            self,  
            state: List,
            depth: int = 0
        ):
        
        # Attributes
        global ID
        self.id = ID
        ID += 1
        self.state = state
        self.children = []                  
        self.depth = depth                  # 0 if is the root
        self.score = []
    
    
    def __repr__(self) -> str:
        return f"Node({self.state})"
    
    def set_score(self, score):
        self.score = score
    
    def get_children(self) -> List['Node']:
        # Lazy loading
        if len(self.children) != 0: 
            return self.children
        else :
            n_moves = random.randint(1,5)
            for _ in range(n_moves):
                new_state = self.state.copy()
                new_state.append(random.randint(-5,5))
                self.children.append(Node(
                    state=new_state,
                    depth=self.depth+1,
                ))        
            return self.children
        
    def plot_tree(self, heuristic=None):
        def add_edges_and_nodes(graph, node, parent=None):
            # Converte lo stato in stringa per usarlo come etichetta univoca
            label = str([node.id, node.score])

            # Aggiunge il nodo al grafo
            graph.add_node(label)
            if parent:
                graph.add_edge(parent, label)

            # Aggiunge ricorsivamente i figli
            for child in node.children:
                add_edges_and_nodes(graph, child, label)

        # Creazione del grafo
        graph = nx.DiGraph()
        # root_label = str(self.state)  # Usa la rappresentazione stringa dello stato root
        add_edges_and_nodes(graph, self)
        
        pos = nx.nx_pydot.pydot_layout(graph, prog="dot")  # Migliore per strutture ad albero

        plt.figure(figsize=(12, 8))
        nx.draw(graph, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=5, font_weight="bold")
        plt.title("Tree Plot")
        plt.show()

    ##############################################################################################################################################################
    # SEARCH ALGORITHMS ##########################################################################################################################################
    ##############################################################################################################################################################    
    
    def minimax_alpha_beta(
            self,
            maximizing_player: bool,
            depth: int,
            alpha: float = -float('inf'),
            beta: float = float('inf')
        ):
        
        # Caso base: profondità 0 o nodo foglia
        if depth == 0 or not self.get_children():
            score = sum(self.state)
            return score, None

        # Inizializza i valori per il calcolo
        best_move = None
        res_eval = -float('inf') if maximizing_player else float('inf')

        # Itera sui figli del nodo corrente
        for child in self.get_children():
            eval, _ = child.minimax_alpha_beta(
                maximizing_player=not maximizing_player,
                depth=depth - 1,
                alpha=alpha,
                beta=beta
            )
            child.set_score(eval)

            if maximizing_player:
                if eval > res_eval:
                    res_eval = eval
                    best_move = child.state[-1]
                alpha = max(alpha, eval)
            else:
                if eval < res_eval:
                    res_eval = eval
                    best_move = child.state[-1]
                beta = min(beta, eval)

            if beta <= alpha:
                break

        return res_eval, best_move

node = Node([0])
score, _ = node.minimax_alpha_beta(True, 3)
node.set_score(score)
node.plot_tree()