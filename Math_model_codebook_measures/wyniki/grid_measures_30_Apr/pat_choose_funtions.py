from class_codebook import *
from class_measures_result import *
from class_select import *
from class_measures_ref import *

from heat_map import *

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
import seaborn as sns
import pandas as pd

import inspect
import random
import time
import copy
import threading
import math
import os

def dbm_to_mw(x):
    mW=10**(x/10)
    return mW

def mw_to_dbm(x):
    dbm=10*math.log10(x)
    return dbm

def mean_power_with_ris():
    snrs = []
    results = Results()
    powers   = []
    for result in results.results:
        if result.idx < 1000:
            pow = result.powers
            powers.append(pow)
    powers_np_array = np.array(powers)
    data = powers_np_array.T #transpose
    for i in range(data.shape[0]):
        dat = (data[i])
        wat_dat = []
        for x in dat:
            wat_dat.append(dbm_to_mw(x))
        avg = mw_to_dbm(np.mean(wat_dat))
        snrs.append(avg)
    return snrs

def global_maximum_powers_in_pos(selected):
    results = Results()
    powers   = []
    for result in selected.selected:
        pow = np.max(result.powers, axis=0)
        powers.append(pow)
    pow_list = np.max(powers, axis=0)
    return pow_list



def white_noise(B=20e6):
    lvl = -174 + 10 * np.log10(B)
    return lvl




def przeplywnosc(x, W = 20E6, B = 20E6): # x = rec pwr
        noise_pow = dbm_to_mw(white_noise(B))
        signal_pow = dbm_to_mw(x-50)
        return W * np.log2(1 + (signal_pow / noise_pow) )/W # in b/s/Hz

def metric(selections):
    max_values = np.max(selections, axis=0)
    for j in range(len(max_values)):
        max_values[j] = przeplywnosc(max_values[j])
    ret_val = np.sum(max_values) #np.mean
    return ret_val

class PatternSelector:
    def __init__(self, data, mean_power_with_ris, N=4, population_size=100, iterations=1000, mutation_rate=0.4):
        self.data = data
        self.mean_power_with_ris = mean_power_with_ris
        self.N = N
        self.population_size = population_size
        self.iterations = iterations
        self.mutation_rate = mutation_rate

    def setup_constants(population_size=100, iterations=1000, mutation_rate=0.4):
        self.population_size = population_size
        self.iterations = iterations
        self.mutation_rate = mutation_rate
        return

    def przeplywnosc(self, x, j, W = 20E6, B = 20E6): # x = rec pwr
        # if self.snrs[j] > x:
        #     return -100
        return W * np.log2(1 + (dbm_to_mw(x-50) / dbm_to_mw(white_noise(B)) ) )/W # in b/s/HZ

    def metric(self, selections):
        max_values = np.max(selections, axis=0)
        for j in range(len(max_values)):
            max_values[j] = self.przeplywnosc(max_values[j], j)
        ret_val = np.sum(max_values) #np.mean
        return ret_val

    def pat_sel_greedy(self):
        '''
            Do selecta trafiają kolejno wzorce dający największe zyski
        '''
        #WATCH IN DEBUG
        best_selected = [0]
        best_metric = self.metric(self.data[best_selected])
        selected = []
        while (len(selected)< self.N):
            i = 0
            selected.append(0)
            c_metric = self.metric(self.data[selected])
            while i < len(self.data):
                if(i not in best_selected):
                    selected[-1] = i
                    c_metric = self.metric(self.data[selected])
                if (c_metric >= best_metric):
                    best_metric = copy.copy(c_metric)
                    best_selected = copy.copy(selected)
                i+=1
            selected = copy.copy(best_selected)
        return (self.metric(self.data[best_selected]), np.max(self.data[best_selected], axis=0), best_selected)

    def pat_sel_random(self):
        positions = random.sample(range(len(self.data)), min(self.N, len(self.data)))
        selections = self.data[positions]

        best = -100000
        best_sel = None
        best_pos = None

        for k in range(self.iterations):
            # print(k, self.N)
            positions = random.sample(range(len(self.data)), min(self.N, len(self.data)))
            selections = self.data[positions]
            m = self.metric(selections)
            if m > best:
                best = copy.copy(m)
                best_sel = copy.copy(selections)  # Store the best selection
                best_pos = copy.copy(positions)

        return (self.metric(best_sel), np.max(best_sel, axis=0), best_pos)

    def fitness(self, individual):
        sc = self.data[individual]
        return self.metric(sc)

    def pat_sel_genetic(self):
        num_patterns, num_locations = self.data.shape

        # Initialize population
        population = [random.sample(range(num_patterns), self.N) for _ in range(self.population_size)]

        for generation in range(self.iterations):
            # Evaluate population
            fitness_scores = [self.fitness(ind) for ind in population]

            # Selection
            selected_indices = np.argsort(fitness_scores)[-self.population_size // 2:]  # Select the best half
            selected_population = [population[i] for i in selected_indices]

            # Crossover
            new_population = []
            if self.N > 1:
                while len(new_population) < self.population_size:
                    parent1, parent2 = random.sample(selected_population, 2)
                    crossover_point = random.randint(1, self.N - 1)
                    child = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
                    new_population.append(child)  # Unique patterns
            else:
                while len(new_population) < self.population_size:
                    parent1, parent2 = random.sample(selected_population, 2)
                    crossover_point = random.randint(0, self.N - 1)
                    child = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
                    new_population.append(child)  # Unique patterns

            # Mutation
            if self.N>1:
                for i in range(len(new_population)):
                    if random.random() < self.mutation_rate:
                        mutation_index = random.randint(0, self.N - 1)
                        new_population[i][mutation_index] = random.randint(0, num_patterns - 1)
            else:
                for i in range(len(new_population)):
                    if random.random() < self.mutation_rate:
                        mutation_index = 0
                        new_population[i][mutation_index] = random.randint(0, num_patterns - 1)

            population = new_population

        # Best result
        best_individual = max(population, key=self.fitness)
        best_value = self.fitness(best_individual)

        return (best_value, np.max(self.data[best_individual], axis=0), best_individual)

def plot_reg(y, #plot data
            X_LABEL = 'N-1 patters',
            Y_LABEL = 'bitrate [b/s/Hz]',
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
        folder_name = os.path.dirname(os.path.abspath(__file__))
        plots_folder = os.path.join(folder_name, inspect.currentframe().f_code.co_name)

        # Utwórz folder "plots", jeśli nie istnieje
        os.makedirs(plots_folder, exist_ok=True)
        plt.savefig(os.path.join(plots_folder, f"{SAVE_NAME}.{SAVE_FORMAT}", format=SAVE_FORMAT))
    return


def plot_reg_series(yy, # plot data
                    YY_LABELS=None,
                    X_LABEL='N patterns',
                    Y_LABEL='Total spectrum efficiency [b/s/Hz]',
                    CI=95,
                    TITLE='',
                    SAVE=False,
                    SAVE_NAME='figure',
                    SAVE_FORMAT='png',
                    SHOW=True):
    if TITLE=='':
        TITLE = f'Regression Plot with {CI}% Confidence Interval'
    '''
    yy is data matrix:
        cols -> data points (kolenje x)
        rows -> kolejne wartosci f(x)
        3d -> series
    '''
    plt.figure(figsize=(10, 6))  # Create a single figure for all series
    palette = sns.color_palette()
    for i, y in enumerate(yy):
        # Convert to a DataFrame, transposing the data
        data = pd.DataFrame(y).T  # Transpose to have each point in a column

        # Create a new DataFrame for plotting
        data_melted = data.melt(var_name='Data Point', value_name='Values')
        data_melted['Data Point'] += 1
        # Plotting using seaborn's regplot
        if YY_LABELS[i] == GLOBAL_MAX_LABEL:
            sns.lineplot(x='Data Point',
                     y='Values',
                     data=data_melted,
                     color=palette[i % len(palette)],
                     label=YY_LABELS[i] if YY_LABELS else None,
                     legend='full',
                     linestyle='--'
                     )
        elif YY_LABELS[i]==GLOBAL_MAX_CURVE:
            sns.lineplot(x='Data Point',
                        y='Values',
                        data=data_melted,
                        label=YY_LABELS[i] if YY_LABELS else None,
                        legend='full',
                        err_style="band", errorbar=('ci', CI),
                        color=palette[i % len(palette)],
                        linestyle='--',markers=True
                        )
        elif YY_LABELS[i]==GLOBAL_MEAN_BITRATE_WITH_RIS:
            sns.lineplot(x='Data Point',
                     y='Values',
                     data=data_melted,
                     color=palette[i % len(palette)],
                     label=YY_LABELS[i] if YY_LABELS else None,
                     legend='full',
                     linestyle='--'
                     )
        else:
            sns.lineplot(x='Data Point',
                        y='Values',
                        data=data_melted,
                        label=YY_LABELS[i] if YY_LABELS else None,
                        legend='full',
                        err_style="band", errorbar=('ci', CI),
                        color=palette[i % len(palette)],
                        linestyle='',marker='o' 
                        
                        )
            sns.lineplot(x='Data Point',
                        y='Values',
                        data=data_melted,
                        err_style="bars", errorbar=('ci', CI),
                        color=palette[i % len(palette)],
                        linestyle=''
                        )
        
        # sns.pointplot(x='Data Point',
        #              y='Values',
        #              label=YY_LABELS[i] if YY_LABELS else None,
        #              data=data_melted,
        #              errorbar="ci",
        #              color=palette[i],
        #              )

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
        folder_name = os.path.dirname(os.path.abspath(__file__))
        plots_folder = os.path.join(folder_name, inspect.currentframe().f_code.co_name)

        # Utwórz folder "plots", jeśli nie istnieje
        os.makedirs(plots_folder, exist_ok=True)
        plt.savefig(os.path.join(plots_folder, f"{SAVE_NAME}.{SAVE_FORMAT}", format=SAVE_FORMAT))
        plt.savefig(os.path.join(plots_folder, f"{SAVE_NAME}.{SAVE_FORMAT}"), format=SAVE_FORMAT)
    
    return

def plot_reg_series_by_no_of_patterns(yy, # plot data
                    YY_LABELS=None,
                    YY_NUMBER_OF_PATTERNS=None,
                    X_LABEL='N patterns',
                    Y_LABEL='Total spectrum efficiency [b/s/Hz]',
                    CI=95,
                    TITLE='',
                    SAVE=False,
                    SAVE_NAME='figure',
                    SAVE_FORMAT='png',
                    SHOW=True):
    if TITLE=='':
        TITLE = f'Regression Plot with {CI}% Confidence Interval'
    '''
    yy is data matrix:
        cols -> data points (kolenje x)
        rows -> kolejne wartosci f(x)
        3d -> series
    '''
    plt.figure(figsize=(10, 6))  # Create a single figure for all series
    palette = sns.color_palette()
    for i, y in enumerate(yy):
        # Convert to a DataFrame, transposing the data
        data = pd.DataFrame(y).T  # Transpose to have each point in a column

        # Create a new DataFrame for plotting
        data_melted = data.melt(var_name='Data Point', value_name='Values')
        
        # Use YY_NUMBER_OF_PATTERNS for the X coordinates
        if YY_NUMBER_OF_PATTERNS is not None:
            x_values = YY_NUMBER_OF_PATTERNS[i]
            for j,data_point in enumerate(data_melted['Data Point']):
                data_melted['Data Point'][j] = x_values[data_point]  # Set the X values from YY_NUMBER_OF_PATTERNS
        # Plotting using seaborn's regplot
        if YY_LABELS[i] == GLOBAL_MAX_LABEL:
            sns.lineplot(x='Data Point',
                     y='Values',
                     data=data_melted,
                     color=palette[i % len(palette)],
                     label=YY_LABELS[i] if YY_LABELS else None,
                     legend='full',
                     linestyle='--'
                     )
        elif YY_LABELS[i]==GLOBAL_MAX_CURVE:
            sns.lineplot(x='Data Point',
                        y='Values',
                        data=data_melted,
                        label=YY_LABELS[i] if YY_LABELS else None,
                        legend='full',
                        err_style="band", errorbar=('ci', CI),
                        color=palette[i % len(palette)],
                        linestyle='--',markers=True
                        )
        elif YY_LABELS[i]==GLOBAL_MEAN_BITRATE_WITH_RIS:
            sns.lineplot(x='Data Point',
                     y='Values',
                     data=data_melted,
                     color=palette[i % len(palette)],
                     label=YY_LABELS[i] if YY_LABELS else None,
                     legend='full',
                     linestyle='--'
                     )
        else:
            sns.lineplot(x='Data Point',
                        y='Values',
                        data=data_melted,
                        label=YY_LABELS[i] if YY_LABELS else None,
                        legend='full',
                        err_style="band", errorbar=('ci', CI),
                        color=palette[i % len(palette)],
                        linestyle='',marker='o' 
                        
                        )
            sns.lineplot(x='Data Point',
                        y='Values',
                        data=data_melted,
                        err_style="bars", errorbar=('ci', CI),
                        color=palette[i % len(palette)],
                        linestyle=''
                        )
        
        # sns.pointplot(x='Data Point',
        #              y='Values',
        #              label=YY_LABELS[i] if YY_LABELS else None,
        #              data=data_melted,
        #              errorbar="ci",
        #              color=palette[i],
        #              )

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
        folder_name = os.path.dirname(os.path.abspath(__file__))
        plots_folder = os.path.join(folder_name, inspect.currentframe().f_code.co_name)

        # Utwórz folder "plots", jeśli nie istnieje
        os.makedirs(plots_folder, exist_ok=True)
        plt.savefig(os.path.join(plots_folder, f"{SAVE_NAME}.{SAVE_FORMAT}", format=SAVE_FORMAT))
        plt.savefig(os.path.join(plots_folder, f"{SAVE_NAME}.{SAVE_FORMAT}"), format=SAVE_FORMAT)
    
    return

def plot_n_pats_bitrate(y, #plot data
                        X_LABEL = 'N-1 patterns',
                        Y_LABEL = 'Spectrum efficiency [b/s/Hz]',
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
    plt.xlabel('Number of selected patterns [N]', fontsize=FONTSIZE)
    plt.ylabel('Spectrum efficiency [b/s/Hz]', fontsize=FONTSIZE)
    plt.grid()
    #plt.legend(fontsize=FONTSIZE)

    # Show plot
    if SHOW:
        plt.show()
    if SAVE:
        folder_name = os.path.dirname(os.path.abspath(__file__))
        plots_folder = os.path.join(folder_name, inspect.currentframe().f_code.co_name)

        # Utwórz folder "plots", jeśli nie istnieje
        os.makedirs(plots_folder, exist_ok=True)
        plt.savefig(os.path.join(plots_folder, f"{SAVE_NAME}.{SAVE_FORMAT}", format=SAVE_FORMAT))

    return

def plot_bitrate_in_loc(data, #lista list do wykresowania
                        data_LABELS, #lista opisów do wykresowania
                        X_LABEL = 'N-1 patterns',
                        Y_LABEL = 'Spectrum efficiency [b/s/Hz]',
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
        plt.plot(x_axis, y,  markersize=MARKERSIZE, label=data_LABELS[i], marker='X')
    # ref max from results
    if PLT_REF:
        res_pows = []
        for x in results.results:
            res_pows.append(x.powers)
        res_pows_array = np.array(res_pows)
        res_pows = np.max(res_pows_array, axis=0)
        plt.plot(x_axis, res_pows,  markersize=MARKERSIZE, label='FULL CODEBOOK i=[0;90],d=[0;90]', color='yellow', marker='X')

    plt.xlabel('Kąt położenia odbiornika [stopnie]', fontsize=FONTSIZE)
    plt.ylabel('Wartości mocy odebranej [dBm]', fontsize=FONTSIZE)
    if TITLE!='':
        plt.title(TITLE)
    plt.grid()
    plt.legend(fontsize=FONTSIZE, loc='upper right')

    if SAVE:
        folder_name = os.path.dirname(os.path.abspath(__file__))
        plots_folder = os.path.join(folder_name, inspect.currentframe().f_code.co_name)

        # Utwórz folder "plots", jeśli nie istnieje
        os.makedirs(plots_folder, exist_ok=True)
        plt.savefig(os.path.join(plots_folder, f"{SAVE_NAME}.{SAVE_FORMAT}", format=SAVE_FORMAT))

    # Show the plot if requested
    if SHOW:
        plt.show()
    return

def plot_heatmap_bitrate(powers, SAVE=True):
    ''' [co oznacza indeks jest w nawiasach]
        Powers -> tablica [funkcja_generująca_listę_mocy][ilość patternów uzytych][iteracja wyników (może być jedna)]
    '''
    ref_x_y = [(0,0), (0,2), (0,1), (1,2), (1,1), (1,0), (2,2), (2,1), (3,2), (2,0), (4,2), (3,1), (4,0), (3,0), (4,1)]
    x_y = [(0,0), (0,1), (0,2), (1,2), (1,1), (1,0), (2,2), (2,1), (3,2), (2,0), (3,1), (4,2), (4,1), (3,0), (4,0)]
    white_noise_lvls = np.full(15, white_noise(20e6)) # SET NOISE LVL 
    #HEATMAP PRZEPLYWNOSC
    bitrates = []
    for p_funkcji in powers: #iteruj wykonane funkcje
        bitrates.append([])
        for p_n_elementow in p_funkcji: #iteruj liczby elementów
            bitrates[-1].append([])
            if p_n_elementow==[]:
                continue
            if len(p_n_elementow)>1:
                maks = 0,0
                for indeks, iteracja in enumerate(p_n_elementow):
                    t = np.sum(iteracja)
                    if maks[0] < t:
                        maks = (t, indeks)
                tmp_p = p_n_elementow[maks[1]]
            else:
                tmp_p = p_n_elementow[0]
            for p in tmp_p: #iteruj pojedyncze moce i oblicz przeplywnosci dla nich w koncu
                bitrates[-1][-1].append(przeplywnosc(p))

    heat_map_data = input_dat(bitrates[0][0], ref_x_y)            
    plot_heat_map(
                heat_map_data,
                f"REF NO_RIS, sum:{np.round(np.sum(bitrates[0][0]), decimals=1)} b/s/Hz",
                SAVE=SAVE, SAVE_NAME=f"heatmap_bitrate_NO_RIS_{yy_legend[0]}",
                SCALE_LABEL="Spectrum efficiency [b/s/Hz]",
                SAVE_FORMAT='png'
                )

    heat_map_data = input_dat(bitrates[1][0], x_y)            
    plot_heat_map(
                heat_map_data,
                f"REF NO_RIS, sum:{np.round(np.sum(bitrates[1][0]), decimals=1)} b/s/Hz",
                SAVE=SAVE, SAVE_NAME=f"heatmap_bitrate_{yy_legend[1]}",
                SCALE_LABEL="Spectrum efficiency [b/s/Hz]",
                SAVE_FORMAT='png'
                )
    
    heat_map_data = input_dat(bitrates[2][0], x_y)            
    plot_heat_map(
                heat_map_data,
                f"REF NO_RIS, sum:{np.round(np.sum(bitrates[2][0]), decimals=1)} b/s/Hz",
                SAVE=SAVE, SAVE_NAME=f"heatmap_bitrate_{yy_legend[2]}",
                SCALE_LABEL="Spectrum efficiency [b/s/Hz]",
                SAVE_FORMAT='png'
                )

    j=0
    while j < len(bitrates[-1]):
        dat=[bitrates[0][0]]
        i = 3
        while i < len(bitrates):
            if bitrates[i][j]!=[]:
                heat_map_data = input_dat(bitrates[i][j], x_y)
                plot_heat_map(
                            heat_map_data,
                            f"N={j+1}, {yy_legend[i][8:-4]}, sum:{np.round(np.sum(bitrates[i][j]), decimals=1)} [b/s/Hz]",
                            SAVE=SAVE,
                            SAVE_NAME=f"heatmap_bitrate_liczba_wzorcy_{j+1}_{yy_legend[i]}",
                            SCALE_LABEL="Spectrum efficiency [b/s/Hz]",
                            SAVE_FORMAT='png'
                            )
            i+=1
        #plot_bitrate_in_loc(dat, yy_legend, TITLE=f"Liczba wzorcy={j+1}")
        j+=1

def plot_heatmap_powers(powers, SAVE=True):
    #HEATMAPS POWER
    white_noise_lvls = np.full(15, white_noise(20e6)) # SET NOISE LVL 

    #PLOT REF HEATMAP
    ref_x_y = [(0,0), (0,2), (0,1), (1,2), (1,1), (1,0), (2,2), (2,1), (3,2), (2,0), (4,2), (3,1), (4,0), (3,0), (4,1)]
    x_y = [(0,0), (0,1), (0,2), (1,2), (1,1), (1,0), (2,2), (2,1), (3,2), (2,0), (3,1), (4,2), (4,1), (3,0), (4,0)]

    heat_map_data = input_dat(powers[0][0][0]-white_noise_lvls-50, ref_x_y)
    plot_heat_map(heat_map_data, f"NO_RIS", SAVE=True,SCALE_LABEL="SNR [dBm]", SAVE_NAME=f"heatmap_power_no_ris", SAVE_FORMAT='png',V_MIN=0, V_MAX=10)

    heat_map_data = input_dat(powers[1][0][0]-white_noise_lvls-50, x_y)
    plot_heat_map(heat_map_data, f"GLOBAL MAX", SAVE=True,SCALE_LABEL="SNR [dBm]", SAVE_NAME=f"heatmap_power_glob_max", SAVE_FORMAT='png',V_MIN=0, V_MAX=10)

    heat_map_data = input_dat(powers[2][0][0]-white_noise_lvls-50, x_y)
    plot_heat_map(heat_map_data, f"MEAN RIS", SAVE=True,SCALE_LABEL="SNR [dBm]", SAVE_NAME=f"heatmap_power_ris_mean", SAVE_FORMAT='png',V_MIN=0, V_MAX=10)

    j = 0
    x_y = [(0,0), (0,1), (0,2), (1,2), (1,1), (1,0), (2,2), (2,1), (3,2), (2,0), (3,1), (4,2), (4,1), (3,0), (4,0)]
    while j < len(powers[-1]):
        dat = [powers[0][0][0]]
        i = 3
        while i < len(powers):
            if powers[i][j]!=[]:

                maks = 0,0
                for indeks, iteracja in enumerate(powers[i][j]):
                    t = np.sum(iteracja)
                    if maks[0] < t:
                        maks = (t, indeks)
                tmp_p = powers[i][j][maks[1]]
                dat.append(tmp_p)

                heat_map_data = input_dat(dat[-1]-50-white_noise_lvls, x_y)
                plot_heat_map(
                              heat_map_data,
                              f"Liczba wzorcy={j+1}, {yy_legend[i]}",
                              SAVE=True,
                              SCALE_LABEL="SNR [dBm]",
                              SAVE_NAME=f"heatmap_power_liczba_wzorcy_{j+1}_{yy_legend[i]}",
                              SAVE_FORMAT='png',
                              V_MIN=0, V_MAX=10
                              )
            i+=1
        j+=1

def plot_heatmap_powers_snr_to_mean_ris(powers, mean_ris_pow, SAVE=True):
    #HEATMAPS POWER
    white_noise_lvls = np.full(15, white_noise(20e6)) # SET NOISE LVL 

    #PLOT REF HEATMAP
    ref_x_y = [(0,0), (0,2), (0,1), (1,2), (1,1), (1,0), (2,2), (2,1), (3,2), (2,0), (4,2), (3,1), (4,0), (3,0), (4,1)]
    x_y = [(0,0), (0,1), (0,2), (1,2), (1,1), (1,0), (2,2), (2,1), (3,2), (2,0), (3,1), (4,2), (4,1), (3,0), (4,0)]

    heat_map_data = input_dat(powers[0][0][0]-np.array(mean_ris_pow), ref_x_y)
    plot_heat_map(heat_map_data, f"NO_RIS", SAVE=True,SCALE_LABEL="SNR to mean ris [dB]", SAVE_NAME=f"heatmap_power_no_ris_to_mean_ris", SAVE_FORMAT='png',V_MIN=0, V_MAX=10)

    heat_map_data = input_dat(powers[1][0][0]-np.array(mean_ris_pow), x_y)
    plot_heat_map(heat_map_data, f"GLOBAL MAX", SAVE=True,SCALE_LABEL="SNR to mean ris [dB]", SAVE_NAME=f"heatmap_power_glob_max_to_mean_ris", SAVE_FORMAT='png',V_MIN=0, V_MAX=10)

    heat_map_data = input_dat(powers[2][0][0]-np.array(mean_ris_pow), x_y)
    plot_heat_map(heat_map_data, f"MEAN RIS", SAVE=True,SCALE_LABEL="SNR to mean ris [dB]", SAVE_NAME=f"heatmap_power_ris_mean_to_mean_ris", SAVE_FORMAT='png',V_MIN=0, V_MAX=10)

    j = 0
    x_y = [(0,0), (0,1), (0,2), (1,2), (1,1), (1,0), (2,2), (2,1), (3,2), (2,0), (3,1), (4,2), (4,1), (3,0), (4,0)]
    while j < len(powers[-1]):
        dat = [powers[0][0][0]]
        i = 3
        while i < len(powers):
            if powers[i][j]!=[]:

                maks = 0,0
                for indeks, iteracja in enumerate(powers[i][j]):
                    t = np.sum(iteracja)
                    if maks[0] < t:
                        maks = (t, indeks)
                tmp_p = powers[i][j][maks[1]]
                dat.append(tmp_p)

                heat_map_data = input_dat(dat[-1]-np.array(mean_ris_pow), x_y)
                plot_heat_map(
                              heat_map_data,
                              f"N patterns={j+1}, {yy_legend[i]}",
                              SAVE=True,
                              SCALE_LABEL="SNR to mean ris [dB]",
                              SAVE_NAME=f"heatmap_snr_to_mean_ris_liczba_wzorcy_{j+1}_{yy_legend[i]}",
                              SAVE_FORMAT='png',
                              V_MIN=0, V_MAX=10
                              )
            i+=1
        j+=1

def merge_selections(selected):
    merge = []
    for s in selected.selected:
        merge.append(s.maxs)
    merge = np.array(merge)
    return merge

def run_select_function(merge, pattern_selector, range_low = 1, range_max = 16, i_bound = 1, pat_sel_function_name='pat_sel_genetic'):
    y, powss, poss = [], [], []
    # Get the method from the pattern_selector instance
    pat_sel_function = getattr(pattern_selector, pat_sel_function_name)

    for n in range(1, range_max):
        print("N: ", n)
        #extend list dims
        y.append([])
        powss.append([])
        poss.append([])
        if range_low>n:
            continue
        else:
            i = 0
            while i < i_bound:
                pattern_selector.N=n
                m, pows, pos = pat_sel_function()
                y[n - 1].append(m)
                powss[n - 1].append(pows)
                poss[n - 1].append(pos)
                i += 1
    return y, powss, poss

def save_powers(data):
    flattened_data = []
    for sublist in data:
        for item in sublist:
            if isinstance(item, list):
                for subitem in item:
                    flattened_data.append(subitem)
            else:
                flattened_data.append(item)

    # Tworzymy DataFrame
    df = pd.DataFrame(flattened_data)

    # Zapisz do pliku CSV
    df.to_csv('datapowers.csv', index=False, header=False)

    print("Dane zostały zapisane do pliku 'data.csv'.")

def badanie_genetycznego_save_result(yy, yy_legend, RET=True):
    ret_labels = []
    ret_vals = []
    ret_sums_vals = []
    with open('genetic_badanie.csv', 'w') as f:
        for i,xx in enumerate(yy[3:]):
            print(i)
            f.write(yy_legend[i+3] + ';')
            srednie = []
            for j,x in enumerate(xx):
                if x!=[]:
                    srednie.append(np.mean(x))
            if(RET):
                print(i)
                ret_labels.append(yy_legend[i+3])
                ret_vals.append(srednie)
                ret_sums_vals.append(np.sum(srednie))
            srednie.append(np.sum(srednie))
            f.write(';'.join(map(str, srednie)) + '\n')

        f.close()
    print("GENETIC SAVED TO FILE")
    return ret_vals, ret_sums_vals, ret_labels

def global_max_curve_finder(yy):
    maksy = [0] * 15
    for i, y in enumerate(yy):
        for j,val_list in enumerate(y):
            mx = np.max(val_list)
            if maksy[j] < mx:
                maksy[j]=mx
            pass
        pass
    pass
    return maksy


if __name__ == "__main__":
    #### INIT #####
    
    # Optionally set a random seed based on the current time
    random.seed(time.time())
    #dumpfile for pickle name:
    
    ref_mes = Results_Ref()
    ref_metric = []
    rm = metric([ref_mes.results[0].powers])
    for _ in range(0,15):
        ref_metric.append(rm)

    ## LOAD DATASET with diffrent phi_s stepping
    selected = Selected(1)
    selected_30 = Selected(30)
    selected_45 = Selected(45)
    selected_90 = Selected(90)
    selected_180 = Selected(180)
    selected_360 = Selected(360)
    '''
    uncomment one to:
        - load data from source csv
        - from preprepared picle
    '''
    # selected = load_results_from_file(selected)
    dumpfile = "wybrane_paterny_pk_metod_s_step_1.pkl"
    selected.load_from_file(dumpfile=dumpfile)

    dumpfile = "wybrane_paterny_pk_metod_s_step_30.pkl"
    selected_30.load_from_file(dumpfile=dumpfile)

    dumpfile = "wybrane_paterny_pk_metod_s_step_45.pkl"
    selected_45.load_from_file(dumpfile=dumpfile)

    dumpfile = "wybrane_paterny_pk_metod_s_step_90.pkl"
    selected_90.load_from_file(dumpfile=dumpfile)

    dumpfile = "wybrane_paterny_pk_metod_s_step_180.pkl"
    selected_180.load_from_file(dumpfile=dumpfile)

    dumpfile = "wybrane_paterny_pk_metod_s_step_360.pkl"
    selected_360.load_from_file(dumpfile=dumpfile)

    selections_list = [selected,
                       selected_30,
                       selected_45,
                       selected_90, 
                       selected_180,
                       selected_360
                       ]

    # FIND GLOBAL MAX POWERS AND ITS METRIC
    global GLOBAL_MAX_LABEL
    GLOBAL_MAX_LABEL = "GLOBAL MAX"
    global_maximum_powers = global_maximum_powers_in_pos(selected)
    global_max_metric = []
    glmm =  metric([global_maximum_powers])
    global_max_metric = [glmm] * 15


    #create merged array with maximums from patterns for given i,d generations
    merge_list = []

    for sel in selections_list:
        merge_list.append(merge_selections(sel))

    ## MEAN WITH RIS
    mean_power_with_ris = mean_power_with_ris()
    mean_bitrate_with_ris = []
    mb = 0
    for p in mean_power_with_ris:
        mb+=(przeplywnosc(p))
    mean_bitrate_with_ris = [mb]*15
    global GLOBAL_MEAN_BITRATE_WITH_RIS
    GLOBAL_MEAN_BITRATE_WITH_RIS = "Mean bitrate with RIS"

    

    #select patterns by functions

    #LISTA: pat_sel_genetic, pat_sel_random
    selection_functions = ["pat_sel_random", "pat_sel_greedy","pat_sel_genetic"]
    genetic_params = [[10,10,0.3],[50,20,0.3]]#,[200,50,0.3]] #population, generations, mutations
    random_params = [[100],[1000]]#,[10000]]

    # '''GENETIC BADANE'''
    # selection_functions = ["pat_sel_genetic"]
    # genetic_params = []
    # for i in range(10,500):
    #     for j in range (5,500): 
    #         operacje = 1000/(i*j)
    #         if operacje < 1.0011 and operacje > 0.991:
    #             print("i, j:: ", i, j)
    #             mutacje = 0.2
    #             while mutacje < 0.41:
    #                 genetic_params.append([i,j,mutacje])
    #                 mutacje+=0.1
    #     continue


    # '''FAST RUN'''
    selection_functions = ["pat_sel_greedy"]
    random_params = [[400]]
    genetic_params = [[20,20,0.3]]



    I_BOUND = 4
    RANGE_MAX = 16 #max 16
    RANGE_LOW = 1
    # Loop through each selection function and generate data
    powers = [[[ref_mes.results[0].powers]],[[global_maximum_powers]], [[mean_power_with_ris]]]
    yy = [ref_metric, global_max_metric, mean_bitrate_with_ris]
    yy_legend = ["NO_RIS", GLOBAL_MAX_LABEL, GLOBAL_MEAN_BITRATE_WITH_RIS]
    yy_number_of_patterns = [[np.linspace(0,919,920)],[np.linspace(0,919,920)],[np.linspace(0,919,920)]]
    for i,merge in enumerate(merge_list):
        # if i > 2: #breaking early to fasten run
        #     break
        phi_s_step = selections_list[i].phi_s_step
        pattern_selector = PatternSelector(data=merge, mean_power_with_ris=mean_power_with_ris, iterations=10)

        for selection_function in selection_functions:
            print(f"Using function: {selection_function}")
            if selection_function=="pat_sel_random":
                for p in random_params:
                    print("RANDOM", p)
                    t0 = time.time()
                    pattern_selector.iterations = p[0]
                    y, pow, pos = run_select_function(merge, pattern_selector, range_low=RANGE_LOW, range_max=RANGE_MAX, i_bound=I_BOUND, pat_sel_function_name=selection_function)
                    # print(y)
                    powers.append(pow)
                    # print(pow)
                    # print(pos)
                    yy.append(y)
                    yy_number_of_patterns.append(np.linspace(360/phi_s_step,RANGE_MAX*(360/phi_s_step),RANGE_MAX-RANGE_LOW+1))
                    yy_legend.append(selection_function +" " + "ϕs_step" +str(phi_s_step) + "° " + str(p[0]) +" "+ str((time.time()-t0)/I_BOUND)[0:3] + "s")
            elif selection_function=="pat_sel_genetic":
                range_low_bac = None
                if RANGE_LOW<2:
                    range_low_bac = copy.copy(RANGE_LOW)
                    RANGE_LOW=2
                for p in genetic_params:
                    print("GENETIC", p)
                    t0 = time.time()
                    pattern_selector.iterations=p[1]
                    pattern_selector.population_size=p[0]
                    pattern_selector.mutation_rate=p[2]
                    # pattern_selector.setup_constants(population_size=p[0], iterations=p[1], mutation_rate=p[2])
                    y, pow, pos = run_select_function(merge, pattern_selector, range_low=RANGE_LOW, range_max=RANGE_MAX, i_bound=I_BOUND, pat_sel_function_name=selection_function)
                    # print(y)
                    powers.append(pow)
                    yy_number_of_patterns.append(np.linspace(360/phi_s_step,RANGE_MAX*(360/phi_s_step),RANGE_MAX-RANGE_LOW+1))
                    # print(pow)
                    # print(pos)
                    yy.append(y)
                    yy_legend.append(selection_function +" " + "ϕs_step" +str(phi_s_step) + "° " +str(p)+" "+ str((time.time()-t0)/I_BOUND)[0:3] + "s")
            elif selection_function == "pat_sel_greedy":
                print("greedy running",)
                t0 = time.time()
                y, pow, pos = run_select_function(merge, pattern_selector, range_low=RANGE_LOW, range_max=RANGE_MAX, i_bound=2, pat_sel_function_name=selection_function)
                # print(y)
                powers.append(pow)
                # print(pow)
                # print(pos)
                yy.append(y)
                yy_number_of_patterns.append(np.linspace(360/phi_s_step,RANGE_MAX*(360/phi_s_step),RANGE_MAX-RANGE_LOW+1))
                yy_legend.append(selection_function +" "+"ϕs_step" +str(phi_s_step) + "° " + str((time.time()-t0)/I_BOUND)[0:3] + "s")
    # yy.append(global_max_curve_finder(yy[3:]))
    global GLOBAL_MAX_CURVE
    GLOBAL_MAX_CURVE = "GLOBAL MAX CURVE"
    # yy_legend.append(GLOBAL_MAX_CURVE)
    plot_reg_series_by_no_of_patterns(yy[3:], yy_legend[3:], yy_number_of_patterns[3:], CI=95)
    # plot_reg_series(yy[1:], yy_legend[1:], CI=95)
    # plot_heatmap_powers_snr_to_mean_ris(powers=powers, mean_ris_pow=mean_power_with_ris)
    # plot_heatmap_bitrate(powers)
    # plot_heatmap_powers(powers=powers)
    
    


    '''GENETYCZNY BADANIE DO FUNKCJI'''
    # gen_vals, gen_sums, gen_labels = badanie_genetycznego_save_result(yy, yy_legend)
    # gen_vals = np.array(gen_vals)
    # gen_sums = np.array(gen_sums)
    # gen_labels = np.array(gen_labels)
    # sorted_indices = np.argsort(gen_sums)[::-1] 
    # gen_sums_sorted = gen_sums[sorted_indices]
    # gen_vals_sorted = gen_vals[sorted_indices]
    # gen_labels_sorted = gen_labels[sorted_indices]
    # for i in range(len(gen_sums_sorted)):
    #     print(i,"'th best:: ",gen_labels_sorted[i], gen_sums_sorted[i])


    





