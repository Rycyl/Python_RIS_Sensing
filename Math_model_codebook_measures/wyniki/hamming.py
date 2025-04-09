from class_measures_result import Results
import numpy as np
import matplotlib.pyplot as plt
import os
import math
import copy

def hamming_distance(a, b):
    c = a ^ b
    return c.count(1)

def dbm_to_mw(x):
    mW=10**(x/10)
    return mW
def mw_to_dbm(x):
    dbm=10*math.log10(x)
    return dbm

results = Results()
powers   = []
patterns = []
max_pat = None
min_pat = None

for result in results.results:
    if result.idx < 1000:
        patterns.append(result.pattern)
        pow = result.powers
        powers.append(pow)
    elif result.idx == 1016:
        max_pat = result.pattern
    elif result.idx == 2016:
        min_pat = result.pattern
#change axis
powers_np_array = np.array(powers)
data = powers_np_array.T #transpose

# Uzyskaj nazwę folderu, w którym znajduje się skrypt
folder_name = os.path.dirname(os.path.abspath(__file__))
plots_folder = os.path.join(folder_name, 'hamming')

# Utwórz folder "plots", jeśli nie istnieje
os.makedirs(plots_folder, exist_ok=True)

# Rysowanie każdego wiersza na osobnym wykresie i zapisywanie do plików
for i in range(data.shape[0]):
    pats = copy.deepcopy(patterns)
    sorted_indices = np.argsort(data[i])
    pats = [pats[j] for j in sorted_indices]
    hamming_distances = []
    for x in pats:
        hamming_distances.append(hamming_distance(x, max_pat))
    plt.figure()  # Utwórz nową figurę dla każdego wykresu
    plt.plot(hamming_distances, label=f'Wiersz {i+1}')

    plt.title(f'Tx {int(results.results[0].Tx_Angle[i])}, Rx {int(results.results[0].Rx_Angle[i])}')
    plt.xlabel('N-ty_pattern')
    plt.ylabel('Hamming distance')
    #plt.ylim(-95, -50)  # Ustawienie stałego zakresu osi Y
    plt.grid(True)  # Włączenie linii pomocniczych
    plt.legend()
    
    # Zapisz wykres do pliku w folderze "plots"
    plt.savefig(os.path.join(plots_folder, f'wykres_wiersz_{i+1}.png'))
    plt.close()  # Zamknij figurę, aby nie pokazywać podglądu