from board import *
from heuristics import grey_heuristic
import random
import numpy as np

# Limiti per i pesi
WEIGHT_BOUNDS = {
    "W2": (10, 500),
    "W3": (1, 5),
    "W4": (5, 50),
    "W5": (10, 50),
    "W6": (5, 30),
    "W7": (5, 20),
    "W8": (5, 20),
    "W9": (1, 20),
    "W10": (1, 20),
    "W11": (10, 50),
    "W12": (5, 30),
    "W13": (5, 30),
}

# Parametri del GA
POPULATION_SIZE = 20
GENERATIONS = 50
MUTATION_RATE = 0.1
TOURNAMENT_SIZE = 5

# Genera un individuo casuale (configurazione dei pesi)
def generate_individual():
    return {key: random.uniform(*bounds) for key, bounds in WEIGHT_BOUNDS.items()}

# Valutazione di un individuo (fitness)
def evaluate_individual(individual):
    # Simula partite e ritorna la fitness (numero di vittorie)
    wins = simulate_games(individual)
    return wins

# Simulazione di partite per valutare un individuo
def simulate_games(weights):
    # Implementare una funzione che giochi partite contro un avversario
    # (potrebbe essere un altro algoritmo o una configurazione di riferimento).
    # Qui ritorniamo un punteggio casuale come segnaposto.
    return random.randint(0, 10)

# Selezione tramite torneo
def tournament_selection(population, fitnesses):
    tournament = random.sample(list(population.items()), TOURNAMENT_SIZE)
    winner = max(tournament, key=lambda x: fitnesses[x[0]])
    return winner[1]

# Crossover tra due individui
def crossover(parent1, parent2):
    child = {}
    for key in parent1.keys():
        child[key] = random.choice([parent1[key], parent2[key]])
    return child

# Mutazione di un individuo
def mutate(individual):
    for key in individual.keys():
        if random.random() < MUTATION_RATE:
            individual[key] = random.uniform(*WEIGHT_BOUNDS[key])
    return individual

# Algoritmo genetico
def genetic_algorithm():
    # Popolazione iniziale
    population = {i: generate_individual() for i in range(POPULATION_SIZE)}

    for generation in range(GENERATIONS):
        # Valutazione della popolazione
        fitnesses = {i: evaluate_individual(individual) for i, individual in population.items()}

        # Stampa il miglior individuo della generazione
        best_individual = max(fitnesses, key=fitnesses.get)
        print(f"Generazione {generation + 1}, Miglior fitness: {fitnesses[best_individual]}")

        # Nuova generazione
        new_population = {}
        for i in range(POPULATION_SIZE):
            # Selezione
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)

            # Crossover
            child = crossover(parent1, parent2)

            # Mutazione
            child = mutate(child)

            new_population[i] = child

        population = new_population

    # Restituisci il miglior individuo finale
    fitnesses = {i: evaluate_individual(individual) for i, individual in population.items()}
    best_individual = max(fitnesses, key=fitnesses.get)
    return population[best_individual], fitnesses[best_individual]

# Esecuzione dell'algoritmo genetico
best_weights, best_fitness = genetic_algorithm()
print("Miglior configurazione trovata:", best_weights)
print("Fitness:", best_fitness)
