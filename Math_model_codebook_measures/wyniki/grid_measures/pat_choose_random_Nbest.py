from class_codebook import *
from class_measures_result import *
import numpy as np
import random
import matplotlib.pyplot as plt
import time
import copy
# Optionally set a random seed based on the current time
random.seed(time.time())

def load_results_from_file(selected):
    results = Results()
    codebook = Codebook()
    print("source data loaded")
    currtent_pattern = None

    selected = Selected()
    i = -49
    for d in range(0, 90):
        used_patterns = [0] * 919
        print("D=", d)
        selected.selected.append(Select(i,d))
        for x in codebook.patterns:
            if used_patterns[x.idx] != 1:
                for a in x.angles:
                    if used_patterns[x.idx] == 1:
                        break
                    if (a[0] == i and a[1] == d):
                        selected.selected[-1].add_pat_idx(a[2], x.idx,  results.results[x.idx].powers)
                        used_patterns[x.idx] = 1
            else:
                continue         
    selected.dump_class_to_file(dumpfile=dumpfile)
    return selected


class Selected:
    def __init__(self):
        self.selected = []
    

    def dump_class_to_file(self, dumpfile):
        # Serializacja obiektu do pliku
        with open(dumpfile, 'wb') as file:
            pickle.dump(self, file)
        print("Results class dumpted to a file: ", dumpfile)

    def load_from_file(self, dumpfile):
        try:
            with open(dumpfile, 'rb') as file:
                loaded_object = pickle.load(file)
            self.selected = loaded_object.selected
            print("pikle loaded")
        except:
            print("error while pikle loading")
            pass

class Select:
    def __init__(self,i,d):
        self.i = i
        self.d = d
        self.s = []
        self.pat_idx = []
        self.powers = []
        self.maxs = []
        self.maxs_idx = []

    def add_pat_idx(self, s, idx, pows):
        self.s.append(s)
        self.pat_idx.append(idx)
        self.powers.append(pows)

    def show(self):
        print("i = ", self.i, " d = ", self.d)
        for j in range(len(self.s)):
            print(f"For shift = {self.s[j]}, pat_idx = {self.pat_idx[j]}")
    
    def show_pows(self):
        print("i = ", self.i, " d = ", self.d, "len = ", len(self.powers))
        for x in self.powers:
            print([f"{value:.3f}" for value in x])
    
    def find_max(self):
        if self.powers != []:
            array = np.array(self.powers)
            max_values = np.max(array, axis=0)
            max_indices = np.argmax(array, axis=0)
            for l in range(len(max_indices)):
                max_indices[l] = self.pat_idx[max_indices[l]]
            self.maxs  = (max_values)
            self.maxs_idx = (max_indices)
        return
        



dumpfile= "wybrane_paterny_pk_metod_v2.pkl"
# try:
selected = Selected()
# selected = load_results_from_file(selected)
selected.load_from_file(dumpfile=dumpfile)

merge = []
for s in selected.selected:
    merge.append(s.maxs)
merge = np.array(merge)

def przeplywnosc(x, W = 2E9, noise = -60): # x = rec pwr
    if noise > x:
        return 0.0
    return W * np.log2(1 + (x - noise))/8/1024/1024 # in MB/s

def metric(selections):
    max_values = np.max(selections, axis=0)
    for j in range(len(max_values)):
        max_values[j] = przeplywnosc(max_values[j])
    ret_val = np.mean(max_values)
    return ret_val

N = 4
ITERATIONS = 1000

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

print(np.max(best_sel, axis=0))
print(metric(best_sel))
print(best_pos)


results= Results()
res_pows = []
for x in results.results:
    res_pows.append(x.powers)
res_pows_array = np.array(res_pows)
res_pows = np.max(res_pows_array, axis=0)
print("BEST")
print(res_pows)
print(metric([res_pows]))
FONTSIZE = 20
MARKERSIZE = 18

# Use Rx_Angle as the x-axis
x_axis = results.results[0].Rx_Angle

# Create a figure and axis
plt.figure(figsize=(10, 8))

# Plot ref_pows
plt.plot(x_axis, np.max(merge, axis=0),  markersize=MARKERSIZE, label='max in selected', color='blue', marker='X')
plt.plot(x_axis, res_pows,  markersize=MARKERSIZE, label='max in measures', color='green', marker='X')

# Plot res_best_pows
plt.plot(x_axis, np.max(best_sel, axis=0),  markersize=MARKERSIZE, label='random sel', color='red', marker='X')
plt.xlabel('Kąt położenia odbiornika [stopnie]', fontsize=FONTSIZE)
plt.ylabel('Wartości mocy odebranej [dBm]', fontsize=FONTSIZE)
plt.grid()
plt.legend(fontsize=FONTSIZE, loc='upper right')

plt.show()