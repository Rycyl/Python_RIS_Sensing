from class_codebook import *
from class_measures_result import *
from class_select import *

import numpy as np
import random
import matplotlib.pyplot as plt
import scipy.stats as st
import seaborn as sns
import pandas as pd
import time
import copy
import threading


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


def pat_sel_random(merge, N = 1, ITERATIONS = 10000):

    positions = random.sample(range(len(merge)), min(N, len(merge)))
    selections = merge[positions]

    best = 0
    best_sel = None
    best_pos = None

    i = 0
    while i < ITERATIONS:
        positions = random.sample(range(len(merge)), min(N, len(merge)))
        selections = merge[positions]
        m = metric(selections)
        if m > best:
            best = copy.copy(m)
            best_sel = copy.copy(selections)  # Store the best selection
            best_pos = copy.copy(positions)
        i+=1
    return (metric(best_sel), np.max(best_sel, axis=0), best_pos)


#### GENETIC START OF CODE ####
def fitness(individual):
    sc = merge[individual]
    ret = metric(sc)
    return ret

def pat_sel_genetic(merge, N = 2, population_size = 100, ITERATIONS = 20, mutation_rate = 0.4):
    
    data = merge
    num_patterns, num_locations = data.shape
    population_size = population_size
    generations = ITERATIONS
    mutation_rate = 0.2

    # Inicjalizacja populacji
    population = [random.sample(range(num_patterns), N) for _ in range(population_size)]

    licz = 0
    # Algorytm genetyczny
    for generation in range(generations):
        
        # Ocena populacji
        fitness_scores = [fitness(ind) for ind in population]
        #print(f'GENERACJA {licz}, max fitness = {np.max(fitness_scores)}')
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
    
    return (best_value, np.max(data[best_individual], axis=0), best_individual)

#### END OF GENETIC CODE ####

def plot_reg(y, #plot data
            X_LABEL = 'N-1 paternow',
            Y_LABEL = 'Przeplywnosc [MB/s]',
            TITLE = 'Regression Plot with 95% Confidence Interval',
            SAVE = False,
            SAVE_NAME = 'figure',
            SAVE_FORMAT = 'png',
            SHOW = True):
    
    '''
    y is data matrix:
        cols -> data points (kolenje x)
        rows -> kolejne wartosci f(x)
    '''
    # Convert to a DataFrame, transposing the data
    data = pd.DataFrame(y).T  # Transpose to have each point in a column

    # Create a new DataFrame for plotting
    data_melted = data.melt(var_name='Data Point', value_name='Values')

    # Plotting using seaborn's regplot
    plt.figure(figsize=(10, 6))
    sns.regplot(x='Data Point', y='Values', data=data_melted, ci=95, marker='o', order=7)

    #names and labels
    plt.title(TITLE)
    plt.xlabel(X_LABEL)
    plt.ylabel(Y_LABEL)
    plt.grid()
    # Show plot
    if SHOW:
        plt.show()
    if SAVE:
        plt.savefig(f"{SAVE_NAME}.{SAVE_FORMAT}", format=SAVE_FORMAT)
    return

def plot_reg_series(yy, # plot data
                    YY_LABELS=None,
                    X_LABEL='N-1 paternow',
                    Y_LABEL='Przeplywnosc [MB/s]',
                    TITLE='Regression Plot with 95% Confidence Interval',
                    SAVE=False,
                    SAVE_NAME='figure',
                    SAVE_FORMAT='png',
                    ORDER = 7,
                    SHOW=True):
    
    '''
    yy is data matrix:
        cols -> data points (kolenje x)
        rows -> kolejne wartosci f(x)
        3d -> series
    '''
    plt.figure(figsize=(10, 6))  # Create a single figure for all series

    for i, y in enumerate(yy):
        # Convert to a DataFrame, transposing the data
        data = pd.DataFrame(y).T  # Transpose to have each point in a column

        # Create a new DataFrame for plotting
        data_melted = data.melt(var_name='Data Point', value_name='Values')

        # Plotting using seaborn's regplot
        sns.regplot(x='Data Point', y='Values', data=data_melted, ci=95, marker='o', order=ORDER, label=YY_LABELS[i] if YY_LABELS else None)

    # Names and labels
    plt.title(TITLE)
    plt.xlabel(X_LABEL)
    plt.ylabel(Y_LABEL)
    plt.grid()
    
    # Add legend if labels are provided
    if YY_LABELS:
        plt.legend(title='Series')

    # Show plot
    if SHOW:
        plt.show()
    if SAVE:
        plt.savefig(f"{SAVE_NAME}.{SAVE_FORMAT}", format=SAVE_FORMAT)
    
    return


def plot_n_pats_bitrate(y, #plot data
                        X_LABEL = 'N-1 paternow',
                        Y_LABEL = 'Przeplywnosc [MB/s]',
                        TITLE = '',
                        SAVE = False,
                        SAVE_NAME = 'figure',
                        SAVE_FORMAT = 'png',
                        SHOW = True):
    #rysuje wykres przepływności w zależności od wybranej liczby paternów, na wejscie bierze array z danymi juz

    FONTSIZE = 18
    MARKERSIZE = 10
    # Use Rx_Angle as the x-axis
    x_axis = np.arange(1, 16)

    # Create a figure and axis
    plt.figure(figsize=(12, 8))

    # Plot ref_pows
    plt.plot(x_axis, y,  markersize=MARKERSIZE, label='Suma', color='blue', marker='X')

    # Plot res_best_pows
    plt.xlabel('Ilość wybieranych paternów [N]', fontsize=FONTSIZE)
    plt.ylabel('Przepływność - suma [MB/s]', fontsize=FONTSIZE)
    plt.grid()
    #plt.legend(fontsize=FONTSIZE)

    # Show plot
    if SHOW:
        plt.show()
    if SAVE:
        plt.savefig(f"{SAVE_NAME}.{SAVE_FORMAT}", format=SAVE_FORMAT)

    return

def plot_bitrate_in_loc(data, #lista list do wykresowania
                        data_LABELS, #lista labeli do wykresowania
                        X_LABEL = 'N-1 paternow',
                        Y_LABEL = 'Przeplywnosc [MB/s]',
                        SAVE = False,
                        TITLE = '',
                        SAVE_NAME = 'figure',
                        SAVE_FORMAT = 'png',
                        SHOW = True,
                        PLT_REF = True):
    '''
    TEN KOD RYSOWAŁ WYKRS DLA KAZDEJ POZYCJI OSOBNO
    '''
    FONTSIZE = 20
    MARKERSIZE = 18

    # Use Rx_Angle from Results as the x-axis
    results= Results()
    x_axis = results.results[0].Rx_Angle

    # Create a figure and axis
    plt.figure(figsize=(10, 8))

    # Plot data and labels
    for i, y in enumerate(data):
        plt.plot(x_axis, y,  markersize=MARKERSIZE, label=y[i], marker='X')
    # ref max from results
    if PLT_REF:
        res_pows = []
        for x in results.results:
            res_pows.append(x.powers)
        res_pows_array = np.array(res_pows)
        res_pows = np.max(res_pows_array, axis=0)
        plt.plot(x_axis, res_pows,  markersize=MARKERSIZE, label='max in measures', color='green', marker='X')

    plt.xlabel('Kąt położenia odbiornika [stopnie]', fontsize=FONTSIZE)
    plt.ylabel('Wartości mocy odebranej [dBm]', fontsize=FONTSIZE)
    plt.grid()
    plt.legend(fontsize=FONTSIZE, loc='upper right')

    if SAVE:
        plt.savefig(f"{SAVE_NAME}.{SAVE_FORMAT}", format=SAVE_FORMAT)

    # Show the plot if requested
    if SHOW:
        plt.show()
    return

def merge_selections(selected):
    merge = []
    for s in selected.selected:
        merge.append(s.maxs)
    merge = np.array(merge)
    return merge



def run_select_function(merge, range_low = 1, range_max = 16, i_bound = 1, pat_sel_function = pat_sel_random):
    t_start = time.time()
    y = []
    for n in range(1, range_max):
        if range_low>n:
            y.append([])
            continue
        else:
            y.append([])
            i = 0
            while i < i_bound:
                #print("N: ", n, " i: ", i)
                m, pows, pos = pat_sel_function(merge, N=n)
                y[n - 1].append(m)
                i += 1
    print(f"{pat_sel_function.__name__} TIME =  {time.time() - t_start}")
    return y






if __name__ == "__main__":
    #### INIT #####

    # Optionally set a random seed based on the current time
    random.seed(time.time())
    #dumpfile for pickle name:
    dumpfile= "wybrane_paterny_pk_metod_v2.pkl"

    selected = Selected()
    '''
    uncomment one to:
        - load data from source csv
        - from preprepared picle
    '''
    # selected = load_results_from_file(selected)
    selected.load_from_file(dumpfile=dumpfile)

    #create merged array with maximums from patterns for given i,d generations
    merge = merge_selections(selected)

    #select patterns by functions
    #LISTA: pat_sel_genetic, pat_sel_random
    selection_functions = [pat_sel_genetic, pat_sel_random]

    I_BOUND = 3

    # Loop through each selection function and generate data
    yy = []
    yy_legend = []
    for selection_function in selection_functions:
        print(f"Using function: {selection_function.__name__}")
        y = run_select_function(merge, range_low=2, range_max=10, i_bound=I_BOUND, pat_sel_function=selection_function)
        yy.append(y)
        yy_legend.append(selection_function.__name__)
        #plot scores
        #plot_reg(y, TITLE='Regression 95% with Polynomial interpolation order=7; Genetic')
    plot_reg_series(yy, yy_legend, ORDER= 5)










