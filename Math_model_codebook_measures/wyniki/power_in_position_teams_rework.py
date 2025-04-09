from class_measures_result import Results
import numpy as np
import matplotlib.pyplot as plt
import os
import math
results = Results()

def dbm_to_mw(x):
    mW=10**(x/10)
    return mW
def mw_to_dbm(x):
    dbm=10*math.log10(x)
    return dbm

powers   = []

maxs = None
mins = None

for result in results.results:
    if result.idx < 1000:
        pow = result.powers
        powers.append(pow)
    elif result.idx == 1016:
        maxs = result.powers
    elif result.idx == 2016:
        mins = result.powers
#change axis
powers_np_array = np.array(powers)
data = powers_np_array.T #transpose

# Uzyskaj nazwę folderu, w którym znajduje się skrypt
folder_name = os.path.dirname(os.path.abspath(__file__))
plots_folder = os.path.join(folder_name, 'power_in_position_teams_rework')

# Utwórz folder "plots", jeśli nie istnieje
os.makedirs(plots_folder, exist_ok=True)

# Rysowanie każdego wiersza na osobnym wykresie i zapisywanie do plików
for i in range(data.shape[0]):
    dat = np.sort((data[i]))
    wat_dat = []
    for x in dat:
        wat_dat.append(dbm_to_mw(x))
    avg = np.mean(wat_dat)
    avg = mw_to_dbm(avg)
    plt.figure()  # Utwórz nową figurę dla każdego wykresu
    plt.plot(dat, label=f'Wiersz {i+1}')
    plt.axhline(y=maxs[i], color='r', linestyle='--', label='colcol_max')
    plt.axhline(y=avg, color='y', linestyle='--', label='avg')
    plt.axhline(y=mins[i], color='g', linestyle='--', label='colcol_min')
    plt.title(f'Tx {int(results.results[0].Tx_Angle[i])}, Rx {int(results.results[0].Rx_Angle[i])}')
    plt.xlabel('N-ty_pattern')
    plt.ylabel('Moc [dBm]')
    plt.ylim(-95, -50)  # Ustawienie stałego zakresu osi Y
    plt.grid(True)  # Włączenie linii pomocniczych
    plt.legend()
    
    # Zapisz wykres do pliku w folderze "plots"
    plt.savefig(os.path.join(plots_folder, f'wykres_wiersz_{i+1}.png'))
    plt.close()  # Zamknij figurę, aby nie pokazywać podglądu