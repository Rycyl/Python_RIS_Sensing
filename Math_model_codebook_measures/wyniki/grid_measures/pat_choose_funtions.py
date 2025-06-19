from class_codebook import *
from class_measures_result import *
from class_select import *

import numpy as np
import random
import matplotlib.pyplot as plt
import time
import copy


# Optionally set a random seed based on the current time
random.seed(time.time())

dumpfile= "wybrane_paterny_pk_metod_v2.pkl"
# try:
selected = Selected()
# selected = load_results_from_file(selected)
selected.load_from_file(dumpfile=dumpfile)

merge = []
for s in selected.selected:
    merge.append(s.maxs)
merge = np.array(merge)

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
        print(i)
        positions = random.sample(range(len(merge)), min(N, len(merge)))
        selections = merge[positions]
        m = metric(selections)
        print(m)
        if m > best:
            best = copy.copy(m)
            best_sel = copy.copy(selections)  # Store the best selection
            best_pos = copy.copy(positions)
        i+=1
    return (metric(best_sel), np.max(best_sel, axis=0), best_pos)

y = []
for n in range(1,16):
    m, pows, pos = pat_sel_random(merge, N=n)
    y.append(m)
print(y)

################### PLOT #############################
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
plt.legend(fontsize=FONTSIZE)

plt.show()

'''
TEN KOD RYSOWAŁ WYKRS DLA KAZDEJ POZYCJI OSOBNO
'''
# results= Results()
# res_pows = []
# for x in results.results:
#     res_pows.append(x.powers)
# res_pows_array = np.array(res_pows)
# res_pows = np.max(res_pows_array, axis=0)
# print("BEST")
# print(res_pows)
# print(metric([res_pows]))
# FONTSIZE = 20
# MARKERSIZE = 18

# # Use Rx_Angle as the x-axis
# x_axis = results.results[0].Rx_Angle

# # Create a figure and axis
# plt.figure(figsize=(10, 8))

# # Plot ref_pows
# plt.plot(x_axis, np.max(merge, axis=0),  markersize=MARKERSIZE, label='max in selected', color='blue', marker='X')
# plt.plot(x_axis, res_pows,  markersize=MARKERSIZE, label='max in measures', color='green', marker='X')

# # Plot res_best_pows
# plt.plot(x_axis, np.max(best_sel, axis=0),  markersize=MARKERSIZE, label='random sel', color='red', marker='X')
# plt.xlabel('Kąt położenia odbiornika [stopnie]', fontsize=FONTSIZE)
# plt.ylabel('Wartości mocy odebranej [dBm]', fontsize=FONTSIZE)
# plt.grid()
# plt.legend(fontsize=FONTSIZE, loc='upper right')

# plt.show()