from class_measures_result import Results
import numpy as np
import matplotlib.pyplot as plt
import os
import math


def dbm_to_mw(x):
    mW=10**(x/10)
    return mW
def mw_to_dbm(x):
    dbm=10*math.log10(x)
    return dbm
def power_in_position(results: Results, file_name: str):
    powers   = []

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


    for result in results.results:
        if result.idx < 1000:
            pow = result.powers
            powers.append(pow)
    #print(maxs, mins)
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
        plt.plot(dat, label=f'Rec pwr')
        plt.axhline(y=maxs[i], color='r', linestyle='--', label='Opt max')
        plt.axhline(y=avg, color='c', linestyle='--', label='Lin avg')
        plt.axhline(y=mins[i], color='g', linestyle='--', label='Opt min')
        plt.title(f'Tx {int(results.results[0].Tx_Angle[i])}, Rx {i}')#{int(results.results[0].Rx_Angle[i])}')
        plt.xlabel('N\'th pattern in recieved power')
        plt.ylabel('Recieved power [dBm]')
        #plt.ylim(-95, -80)  # Ustawienie stałego zakresu osi Y
        plt.grid(True)  # Włączenie linii pomocniczych
        plt.legend(loc='lower left')
        
        # Zapisz wykres do pliku w folderze "plots"
        plt.savefig(os.path.join(plots_folder, f'wykres_pos_pow_wiersz_{i+1}_z_{file_name}.png'))
        plt.close()  # Zamknij figurę, aby nie pokazywać podglądu