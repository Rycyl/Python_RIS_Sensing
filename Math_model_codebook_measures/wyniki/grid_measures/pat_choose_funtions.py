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

def pat_sel_random(merge, N = 1, ITERATIONS = 1000):

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

def plot_reg(y, #plot data
            X_LABEL = 'N-1 paternow',
            Y_LABEL = 'Przeplywnosc [MB/s]',
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
    plt.title('Regression Plot with 95% Confidence Interval')
    plt.xlabel(X_LABEL)
    plt.ylabel(Y_LABEL)
    plt.grid()
    # Show plot
    if SHOW:
        plt.show()
    if SAVE:
        plt.savefig(f"{SAVE_NAME}.{SAVE_FORMAT}", format=SAVE_FORMAT)
    return

def plot_n_pats_bitrate(y, #plot data
                        X_LABEL = 'N-1 paternow',
                        Y_LABEL = 'Przeplywnosc [MB/s]',
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

def run_select_function(merge, i_bound = 1, pat_sel_function = pat_sel_random):
    y = []
    for n in range(1, 16):
        y.append([])
        i = 0
        while i < i_bound:
            print("N: ", n, " i: ", i)
            m, pows, pos = pat_sel_function(merge, N=n)
            y[n - 1].append(m)
            i += 1
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
    selection_functions = [pat_sel_random]

    I_BOUND = 10

    # Loop through each selection function and generate data
    for selection_function in selection_functions:
        print(f"Using function: {selection_function.__name__}")
        y = run_select_function(merge, i_bound=I_BOUND, pat_sel_function=selection_function)
        #plot scores
        plot_reg(y)










