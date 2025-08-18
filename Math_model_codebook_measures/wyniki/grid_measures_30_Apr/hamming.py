from class_measures_result import Results
import numpy as np
import matplotlib.pyplot as plt
import os
import math
import copy
from class_codebook import *

def hamming_distance(a, b):
    c = a ^ b
    return c.count(1)

def dbm_to_mw(x):
    mW=10**(x/10)
    return mW
def mw_to_dbm(x):
    dbm=10*math.log10(x)
    return dbm

codebook_tx48=Codebook(dumpfile='Codebook_tx48.pkl')

results = Results()
powers   = []
patterns = []

max_pat = results.maxs[-2].pattern
min_pat = results.mins[-2].pattern

for result in results.results:
    if result.idx < 1000:
        for pat in codebook_tx48.patterns:
            if pat.pattern == result.pattern:
                patterns.append(result.pattern)
                pow = result.powers
                powers.append(pow)
print(len(patterns))
#change axis
powers_np_array = np.array(powers)
data = powers_np_array.T #transpose

# Uzyskaj nazwę folderu, w którym znajduje się skrypt
folder_name = os.path.dirname(os.path.abspath(__file__))
plots_folder = os.path.join(folder_name, 'hamming')

# Utwórz folder "plots", jeśli nie istnieje
os.makedirs(plots_folder, exist_ok=True)
FONTSIZE=16
# Rysowanie każdego wiersza na osobnym wykresie i zapisywanie do plików
for i in range(data.shape[0]):
    sorted_indices = None
    pats = copy.deepcopy(patterns)
    sorted_indices = np.argsort(data[i])  
    pats = [pats[j] for j in sorted_indices]
    hamming_distances = []
    for x in pats:
        hamming_distances.append(hamming_distance(x, max_pat[i])/16)
    plt.figure()  # Utwórz nową figurę dla każdego wykresu
    plt.rcParams['font.size'] = FONTSIZE
    plt.plot(hamming_distances, label=f'Wiersz {i+1}')
    
    # plt.title(f'Tx {int(results.results[0].Tx_Angle[i])}, Rx {int(results.results[0].Rx_Angle[i])}')
    plt.xlabel('N\'th sorted pattern in recieved power')
    plt.ylabel('Hamming distance to opt best')
    plt.ylim(0, 16)  # Ustawienie stałego zakresu osi Y
    plt.grid(True)  # Włączenie linii pomocniczych
    #plt.legend()
    plt.subplots_adjust(left=0.16, right=0.9, top=0.95, bottom=0.16, wspace=0.2, hspace=0.2)
    # Zapisz wykres do pliku w folderze "plots"
    save_format='svg'
    plt.savefig(os.path.join(plots_folder, f'wykres_{i+1}_hamming_rx_{int(results.results[0].Rx_Angle[i])}.{save_format}'))
    plt.close()  # Zamknij figurę, aby nie pokazywać podglądu