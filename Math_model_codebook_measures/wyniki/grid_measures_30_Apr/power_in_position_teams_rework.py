from class_measures_result import Results
import numpy as np
import matplotlib.pyplot as plt
import os
import math
from class_codebook import *
results = Results()


def dbm_to_mw(x):
    mW=10**(x/10)
    return mW
def mw_to_dbm(x):
    dbm=10*math.log10(x)
    return dbm

powers   = []
#wez wartości z metody opt kolumnami i wylicz które to min/max
ma1 = (results.maxs[-3].powers)
ma2 = (results.maxs[-2].powers)
mi1 = (results.mins[-3].powers)
mi2 = (results.mins[-2].powers)

maxs = []
for i in range(len(ma1)):
    if ma1[i]>ma2[i]:
        maxs.append(ma1[i])
    else:
        maxs.append(ma2[i])

mins = []
for i in range(len(mi1)):
    if mi1[i]<mi2[i]:
        mins.append(mi1[i])
    else:
        mins.append(mi2[i])
#############################
#codebook zeby wybrac tylko patterny z niego
codebook_tx48=Codebook(dumpfile='Codebook_tx48.pkl')
for result in results.results:
    for pat in codebook_tx48.patterns:
            if pat.pattern == result.pattern:
                pow = result.powers
                powers.append(pow)
print(maxs, mins)
#change axis
powers_np_array = np.array(powers)
data = powers_np_array.T #transpose

# Uzyskaj nazwę folderu, w którym znajduje się skrypt
folder_name = os.path.dirname(os.path.abspath(__file__))
plots_folder = os.path.join(folder_name, 'power_in_position_teams_rework')

# Utwórz folder "plots", jeśli nie istnieje
os.makedirs(plots_folder, exist_ok=True)
FONTSIZE=16
# Rysowanie każdego wiersza na osobnym wykresie i zapisywanie do plików
for i in range(data.shape[0]):
    
    dat = np.sort((data[i]))
    wat_dat = []
    for x in dat:
        wat_dat.append(dbm_to_mw(x))
    avg = np.mean(wat_dat)
    avg = mw_to_dbm(avg)
    plt.figure()  # Utwórz nową figurę dla każdego wykresu
    plt.rcParams['font.size'] = FONTSIZE
    plt.rcParams['lines.linewidth']= 3
    plt.plot(dat, color='royalblue', label=f'Full codebook entries')
    plt.axhline(y=maxs[i], color='orangered', linestyle='--', label='SC max')
    plt.axhline(y=avg, color='cyan', linestyle='--', label='Linear average')
    plt.axhline(y=mins[i], color='violet', linestyle='--', label='SC min')
    #plt.title(f'Rx at {int(results.results[0].Rx_Angle[i])}°')
    plt.xlabel('N\'th sorted pattern in recieved power')
    plt.ylabel('Recieved power [dBm]')
    plt.ylim((min(mins)//5)*5, ((max(maxs)//5)+2)*5)  # Ustawienie stałego zakresu osi Y
    plt.grid(True)  # Włączenie linii pomocniczych
    plt.margins()
    plt.legend(loc='lower right',  markerscale=4)
    plt.subplots_adjust(left=0.16, right=0.9, top=0.95, bottom=0.16, wspace=0.2, hspace=0.2)
    # plt.show()
    # Zapisz wykres do pliku w folderze "plots"
    save_format='svg'
    plt.savefig(os.path.join(plots_folder, f'wykres_{i+1}_pow_sort_rx_{int(results.results[0].Rx_Angle[i])}.{save_format}'), format=save_format)
    plt.close()  # Zamknij figurę, aby nie pokazywać podglądu