import numpy as np
from pat_choose_funtions import *
import random

dumpfile = "wybrane_paterny_pk_metod_v2.pkl"
selected = Selected()
selected.load_from_file(dumpfile=dumpfile)
data = merge_selections(selected)

# Parametry
num_patterns = 90  # Liczba wzorców
num_locations = 15   # Liczba lokalizacji
N = 4             # Liczba wzorców do wybrania
population_size = 1000
generations = 100
mutation_rate = 0.2


def przeplywnosc(x, W = 20E6, noise = -68): # x = rec pwr
    if noise > x:
        return 0.0
    return W * np.log2(1 + (x - noise))/8/1024/1024 # in MB/s

def metric(selections):
    max_values = np.max(selections, axis=0)
    for j in range(len(max_values)):
        max_values[j] = przeplywnosc(max_values[j])
    ret_val = np.sum(max_values) #np.mean
    return ret_val

# Funkcja oceny
def fitness(individual):
    sc = data[individual]
    ret = metric(sc)
    return ret

# Inicjalizacja populacji
population = [random.sample(range(num_patterns), N) for _ in range(population_size)]

licz = 0
# Algorytm genetyczny
for generation in range(generations):
    
    # Ocena populacji
    fitness_scores = [fitness(ind) for ind in population]
    print(f'GENERACJA {licz}, max fitness = {np.max(fitness_scores)}')
    licz+=1
    # Selekcja
    selected_indices = np.argsort(fitness_scores)[-population_size//2:]  # Wybieramy najlepsze połowę
    selected_population = [population[i] for i in selected_indices]
    
    # Krzyżowanie
    new_population = []
    while len(new_population) < population_size:
        parent1, parent2 = random.sample(selected_population, 2)
        crossover_point = random.randint(1, N-1)
        child = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
        new_population.append(child)  # Unikalne wzorce
    
    # Mutacja
    for i in range(len(new_population)):
        if random.random() < mutation_rate:
            mutation_index = random.randint(0, N-1)
            new_population[i][mutation_index] = random.randint(0, num_patterns-1)
    
    population = new_population

# Najlepszy wynik
best_individual = max(population, key=fitness)
best_value = fitness(best_individual)

print("Najlepsze wzorce:", best_individual)
print("Maksymalna suma wartości:", best_value)