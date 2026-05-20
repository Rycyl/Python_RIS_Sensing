
from class_measures_result import Results
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import os
import math
from class_codebook import *
import copy
from pathlib import Path
from typing import List, Iterable, Union
from results_for_codebook import select_results_for_codebook

def dbm_to_mw(x):
    mW=10**(x/10)
    return mW

def mw_to_dbm(x):
    dbm=10*np.log10(x)
    return dbm


def truncade_trace(trace):
    return trace[224:1824:2]
# @CP
#TODO: ref mes to dBm
#TODO: ref - paste with high ID (1000+) to 64 codebook


#TODO: overall
#TODO: wykresy (power in position /and merged): shape rysować: min, median, max
"""
sns.lineplot(           err_style="band", errorbar=errorbar_function)

sns.lineplot(errorbar=errorbar_function, estimator=estimator_function)
patrz: pat_choose_functions.py
"""
#TODO: 3 in one teams plot
#TODO: porownać czy najlepszy pattern dla pozycji jest dla tego kąta zaprojektowany


def sort_y_by_x(y, x):
    sorted_indices = np.argsort(x)
    y = np.array(y)
    return y[sorted_indices]

def plot_mean_max_trace(results, codebooks, show = False, save = True):
    """
    This plot is a bit useless
    """    
    cbs_results = []
    x = [] 
    
    for cb in codebooks:
        cbs_results.append(select_results_for_codebook(results=results,codebook=cb))
        x.append(len(cb.patterns))

    # print("X= ", x)
    Rx_pos_number = len(cbs_results[-1].results[-1].Rx_Angle)
    y = [[] for _ in range(Rx_pos_number)]
    for i, cb_results, in enumerate(cbs_results):
        
        z = [[] for _ in range(Rx_pos_number)]
        #Z is a list of: 
        # [
        #         [ rx1, rx2,rx.....
        #             [[trace -> pat1],[trace->pat2] ....]
        #         ],
        # ]
        for result in cb_results.results:
            for alpha, trace in enumerate(result.traces):
                z[alpha].append(trace)
        for j, angle in enumerate(z):
            actual_z = []
            for pat_trace in angle:
                #actual_z.append(np.max(pat_trace))
                actual_z.append(max(pat_trace))
            #uśrednianie do wartości liniowej, potem do dBm powrót
            y[j].append(mw_to_dbm(np.mean(dbm_to_mw(np.array(actual_z)))))
    
    # wykresy
    # Uzyskaj nazwę folderu, w którym znajduje się skrypt
    folder_name = os.path.dirname(os.path.abspath(__file__))
    plots_folder = os.path.join(folder_name, 'mean_max_trace')

    # Utwórz folder "plots", jeśli nie istnieje
    os.makedirs(plots_folder, exist_ok=True)
    save_format='png'
    for j, yy in enumerate(y):
        plt.figure(figsize=(12, 9))
        plt.plot(x, yy)
        plt.xlabel("Codebook size")
        plt.ylabel("Mean max carriers power [dBm]")
        rx_angle = int(np.astype(cbs_results[0].results[0].Rx_Angle[j], int))
        plt.title(f"RX angle = {rx_angle}")
        plt.grid(True)

        if save:
            filename = f"plot{i+1}_mean_max_trace_Rx_{rx_angle}.{save_format}"
            plt.savefig(os.path.join(plots_folder, filename), bbox_inches="tight")

        if show:
            plt.show()

        plt.close()

def plot_mean_max_per_carrier_in_trace(results, codebooks, show = False, save = True):    
    cbs_results = []
    x = [] 
    
    for cb in codebooks:
        cbs_results.append(select_results_for_codebook(results=results,codebook=cb))
        x.append(len(cb.patterns))

    Rx_pos_number = len(cbs_results[-1].results[-1].Rx_Angle)
    yyy = [[] for _ in range(Rx_pos_number)]
    yy  = [[] for _ in range(Rx_pos_number)]
    for i, cb_results, in enumerate(cbs_results):
        
        z = [[] for _ in range(Rx_pos_number)]
        #Z is a list of: 
        # [
        #         [ rx1, rx2,rx.....
        #             [[trace -> pat1],[trace->pat2] ....]
        #         ],
        # ]
        for result in cb_results.results:
            for alpha, trace in enumerate(result.traces):
                z[alpha].append(truncade_trace(trace))
        for j, rx_pos_traces in enumerate(z):
            y_vals = np.max(rx_pos_traces, axis=0)
            yyy[j].append(y_vals)
            #uśrednianie do wartości liniowej, potem do dBm powrót
            yy[j].append(mw_to_dbm(np.mean(dbm_to_mw(np.array(y_vals)))))
    pass


    for i in range(len(yyy)):
        yyy[i]= sort_y_by_x(yyy[i], x)
        yy[i] = sort_y_by_x(yy[i], x)
    x = sort_y_by_x(x, x)
    # wykresy
    # Uzyskaj nazwę folderu, w którym znajduje się skrypt
    folder_name = os.path.dirname(os.path.abspath(__file__))
    plots_folder = os.path.join(folder_name, 'max_pow_per_codebook-carrier')

    # Utwórz folder "plots", jeśli nie istnieje
    os.makedirs(plots_folder, exist_ok=True)
    save_format='png'
    for j, y in enumerate(yy):
        plt.figure(figsize=(12, 9))
        plt.plot(x, y)
        plt.xlabel("Codebook size")
        plt.ylabel("Mean max carriers power [dBm]")
        rx_angle = int(np.astype(cbs_results[0].results[0].Rx_Angle[j], int))
        plt.title(f"RX angle = {rx_angle}")
        plt.grid(True)

        if save:
            filename = f"plot{i+1}_mean_max_trace_Rx_{rx_angle}.{save_format}"
            plt.savefig(os.path.join(plots_folder, filename), bbox_inches="tight")

        if show:
            plt.show()

        plt.close()
    return x, yyy

def plot_power_in_position(
        results, 
        title=None,
        ylabel = 'Power [dBm]',
        xlabel = 'Index of pattern in codebook',
        grid = True,
        y_lim = (-100, -85),
        savefig = True,
        showfig = False,
        label = ""
        ):
    #results = Results(dumpfile=dumpfile)
    powers   = []

    for result in results.results:
        powers.append(result.powers)
    #change axises
    powers_np_array = np.array(powers)
    data = powers_np_array.T 
    # Uzyskaj nazwę folderu, w którym znajduje się skrypt
    folder_name = os.path.dirname(os.path.abspath(__file__))
    plots_folder = os.path.join(folder_name, 'power_in_position')

    # Utwórz folder "plots", jeśli nie istnieje
    os.makedirs(plots_folder, exist_ok=True)

    # Rysowanie każdego wiersza na osobnym wykresie i zapisywanie do plików
    for i in range(data.shape[0]):
        plt.figure()  # Utwórz nową figurę dla każdego wykresu
        plt.plot(data[i], label=f'Wiersz {i+1}')
        if title == None:
            plt.title(f'Tx {int(results.results[0].Tx_Angle[i])}, Rx {int(results.results[0].Rx_Angle[i])}')
        else:
            plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.ylim(-90, -70)  # Ustawienie stałego zakresu osi Y
        plt.grid(True)  # Włączenie linii pomocniczych
        plt.legend()
        
        # Zapisz wykres do pliku w folderze "plots"
        plt.savefig(os.path.join(plots_folder, f'wykres_wiersz_{i+1}.png'))
        plt.close()  # Zamknij figurę, aby nie pokazywać podglądu

def plot_pow_in_pos_teams_all_in_one(results, codebooks, show=True, save=False):
    #results = Results(dumpfile=dumpfile)
    cbs_results = []

    for cb in codebooks:
        cbs_results.append(select_results_for_codebook(results=results,codebook=cb))
        x.append(len(cb.patterns))

    powers_cbs = []
    data_cbs = np.array([])
    """
    power_cbs = [[cb1_powers], [cb2_powers], .....]
    data_cbs has transposed inside arrays
    """

    
    for cb_results in cbs_results:
        powers_cbs.append([])
        np.append(data_cbs, [])
        for result in cb_results.results:
            powers[-1].append(result.trace_mean_idx(list(range(10, 20))))
        #change axis
        powers_np_array = np.array(powers[-1])
        data = powers_np_array.T #transpose
        np.append(data_cbs[-1], data)

    
    
    """
    #wez wartości z metody opt kolumnami i wylicz max
    ma1 = (results.maxs[-3].powers)
    ma2 = (results.maxs[-2].powers)

    maxs = []
    for i in range(len(ma1)):
        if ma1[i]>ma2[i]:
            maxs.append(ma1[i])
        else:
            maxs.append(ma2[i])
    """

    x_vals = []
    y_vals = []


    # Uzyskaj nazwę folderu, w którym znajduje się skrypt
    folder_name = os.path.dirname(os.path.abspath(__file__))
    plots_folder = os.path.join(folder_name, 'power_in_position_comparison_of_CBs')

    # Utwórz folder "plots", jeśli nie istnieje
    os.makedirs(plots_folder, exist_ok=True)
    FONTSIZE=16
 
    plt.figure()  # Utwórz nową figurę dla każdego wykresu
    plt.rcParams['font.size'] = FONTSIZE
    plt.rcParams['lines.linewidth']= 3
    plt.plot(dat, color='royalblue', label=f'Full codebook entries')
    #plt.axhline(y=maxs[i], color='orangered', linestyle='--', label='SC max')
    plt.axhline(y=avg, color='cyan', linestyle='--', label='Linear average')
    #plt.axhline(y=mins[i], color='violet', linestyle='--', label='SC min')
    #plt.title(f'Rx at {int(results.results[0].Rx_Angle[i])}°')
    plt.xlabel('N\'th sorted pattern in recieved power')
    plt.ylabel('Recieved power [dBm]')
    #plt.ylim((np.min(data)//5)*5, ((np.max(data.all())//5))*5)  # Ustawienie stałego zakresu osi Y
    plt.ylim(-90, -70)
    plt.grid(True)  # Włączenie linii pomocniczych
    plt.margins()
    plt.legend(loc='lower right',  markerscale=4)
    plt.subplots_adjust(left=0.16, right=0.9, top=0.95, bottom=0.16, wspace=0.2, hspace=0.2)
    if show:
        plt.show()
    if save:
        # Zapisz wykres do pliku w folderze "plots"
        save_format='svg'
        plt.savefig(os.path.join(plots_folder, f'wykres_{i+1}_pow_sort_rx_{int(results.results[0].Rx_Angle[i])}.{save_format}'), format=save_format)
    plt.close()  # Zamknij figurę, aby nie pokazywać podglądu

def plot_pow_in_pos_teams(results):
    #results = Results(dumpfile=dumpfile)

    def dbm_to_mw(x):
        mW=10**(x/10)
        return mW
    def mw_to_dbm(x):
        dbm=10*math.log10(x)
        return dbm

    powers   = []
    for result in results.results:
        powers.append(result.powers)
    
    """
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
    ############################

    print(maxs, mins)
    """
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
    print(data.shape)
    for i in range(data.shape[0]):
        print(i)
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
        #plt.axhline(y=maxs[i], color='orangered', linestyle='--', label='SC max')
        plt.axhline(y=avg, color='cyan', linestyle='--', label='Linear average')
        #plt.axhline(y=mins[i], color='violet', linestyle='--', label='SC min')
        #plt.title(f'Rx at {int(results.results[0].Rx_Angle[i])}°')
        plt.xlabel('N\'th sorted pattern in recieved power')
        plt.ylabel('Recieved power [dBm]')
        #plt.ylim((np.min(data)//5)*5, ((np.max(data.all())//5))*5)  # Ustawienie stałego zakresu osi Y
        plt.ylim(-90, -70)
        plt.grid(True)  # Włączenie linii pomocniczych
        plt.margins()
        plt.legend(loc='lower right',  markerscale=4)
        plt.subplots_adjust(left=0.16, right=0.9, top=0.95, bottom=0.16, wspace=0.2, hspace=0.2)
        # plt.show()
        # Zapisz wykres do pliku w folderze "plots"
        save_format='svg'
        plt.savefig(os.path.join(plots_folder, f'wykres_{i+1}_pow_sort_rx_{int(results.results[0].Rx_Angle[i])}.{save_format}'), format=save_format)
        plt.close()  # Zamknij figurę, aby nie pokazywać podglądu

def plot_pow_in_pos_merge(results):
    #results = Results(dumpfile=dumpfile)
    powers   = []

    for result in results.results:
        powers.append(result.powers)
    #change axises
    powers_np_array = np.array(powers)
    data = powers_np_array.T 

    # Uzyskaj nazwę folderu, w którym znajduje się skrypt
    folder_name = os.path.dirname(os.path.abspath(__file__))
    plots_folder = os.path.join(folder_name, 'power_in_position')

    # Utwórz folder "plots", jeśli nie istnieje
    os.makedirs(plots_folder, exist_ok=True)
    plt.figure(figsize=(15, 10))
    # Plot each row
    for i in range(data.shape[0]):
        plt.plot(data[i], label=f'Tx {int(results.results[0].Tx_Angle[i])}, Rx {int(results.results[0].Rx_Angle[i])}')

    # Add labels and title
    plt.xlabel('Pattern ID')
    plt.ylabel('Power')
    plt.title('Power for patterns')
    plt.legend()
    plt.grid(True)
        
    # Zapisz wykres do pliku w folderze "plots"
    plt.savefig(os.path.join(plots_folder, f'plot.png'))
    plt.close()  # Zamknij figurę, aby nie pokazywać podglądu

def plot_pattern_characteristics(dumpfile):
    results = Results(dumpfile=dumpfile)

    # Create the directory if it doesn't exist
    output_directory = 'pattern_characteristics'
    os.makedirs(output_directory, exist_ok=True)

    # Assuming results is a list of objects with attributes powers, Rx_Angle, and idx
    for result in results.results:
        powers = result.powers
        rx = result.Rx_Angle
        idx = result.idx
        print("plotting.... ", idx)
        # Combine rx and powers into a list of tuples and sort by rx
        sorted_pairs = sorted(zip(rx, powers))
        
        # Unzip the sorted pairs back into sorted rx and powers
        sorted_rx, sorted_powers = zip(*sorted_pairs)

        # Create a new figure
        plt.figure()
        
        # Scatter plot
        plt.scatter(sorted_rx, sorted_powers, color='blue', label='Data Points')
        
        # Line plot to connect the dots
        plt.plot(sorted_rx, sorted_powers, color='orange', linestyle='-', label='Connecting Line')
        
        # Set the title with the id
        plt.title(f'Result ID: {idx}')
        
        # Set labels
        plt.xlabel('Rx Angle')
        plt.ylabel('Power')
        
        # Set y-axis limits
        plt.ylim(-90, -70)
        
        # Add a legend
        plt.legend()
        
        # Show the grid
        plt.grid()
        
        # Save the plot to the specified directory
        plt.savefig(os.path.join(output_directory, f'plot_{idx}.png'))
        
        # Close the figure to free up memory
        plt.close()


def hamming_distance(a, b):
    c = a ^ b
    return c.count(1)

def dbm_to_mw(x):
    mW=10**(x/10)
    return mW
def mw_to_dbm(x):
    dbm=10*math.log10(x)
    return dbm


def plot_hamming(results):
    #results = Results(dumpfile=dumpfile)
    powers   = []
    patterns = []

    # max_pat = results.maxs[-2].pattern
    # min_pat = results.mins[-2].pattern
    for result in results.results:
        powers.append(result.powers)
        patterns.append(result.pattern)
    #change axis
    powers_np_array = np.array(powers)
    data = powers_np_array.T #transpose

    #weź najlepsze i najgorsze patterny
    max_pat_idxs = np.argmax(powers_np_array, axis=0)
    min_pat_idxs = np.argmin(powers_np_array, axis=0)
    #print(min_pat, max_pat)
    max_pats = []
    min_pats = []
    for k in max_pat_idxs:
        max_pats.append(results.results[k].pattern)
    for k in min_pat_idxs:
        min_pats.append(results.results[k].pattern)
    # max_pat = results.results[max_pat]
    # min_pat = results.results[min_pat]
    # print(max_pat)
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
            hamming_distances.append(hamming_distance(x, max_pats[i])/16)
        plt.figure()  # Utwórz nową figurę dla każdego wykresu
        plt.rcParams['font.size'] = FONTSIZE
        plt.plot(hamming_distances, label=f'Wiersz {i+1}')
        
        # plt.title(f'Tx {int(results.results[0].Tx_Angle[i])}, Rx {int(results.results[0].Rx_Angle[i])}')
        plt.xlabel('N\'th sorted pattern in recieved power')
        plt.ylabel('Hamming distance to best')
        plt.ylim(0, 16)  # Ustawienie stałego zakresu osi Y

        ax = plt.gca()                       # pobierz aktualne osie
        ax.xaxis.set_major_locator(MultipleLocator(4))   # tick co 4 jednostki
        ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))  # bez przecinków (całe liczby)

        plt.grid(True)  # Włączenie linii pomocniczych
        #plt.legend()
        plt.subplots_adjust(left=0.16, right=0.9, top=0.95, bottom=0.16, wspace=0.2, hspace=0.2)
        # Zapisz wykres do pliku w folderze "plots"
        save_format='svg'
        plt.savefig(os.path.join(plots_folder, f'plot{i+1}_hamming_rx_{int(results.results[0].Rx_Angle[i])}.{save_format}'))
        plt.close()  # Zamknij figurę, aby nie pokazywać podglądu        



def list_files_from_folder(folder: str, rozszerzenia: Union[None, str, Iterable[str]] = None) -> List[str]:
    # Examples:
    # list_files_from_folder("/ścieżka")                  -> all files
    # list_files_from_folder("/ścieżka", "txt")           -> just .txt
    # list_files_from_folder("/ścieżka", [".py", "md"])   -> .py and .md
    p = Path(folder)
    if not p.is_dir():
        raise NotADirectoryError(f"{folder} nie jest folderem")
    if rozszerzenia is None:
        exts = None
    else:
        if isinstance(rozszerzenia, str):
            rozszerzenia = [rozszerzenia]
        # normalizuj: usuń wiodącą kropkę i zamień na małe litery
        exts = {e.lower().lstrip('.') for e in rozszerzenia}
    result = []
    for f in p.iterdir():
        if not f.is_file():
            continue
        if exts is None:
            result.append(f.name)
        else:
            if f.suffix.lower().lstrip('.') in exts:
                result.append(f.name)
    return result


if __name__=="__main__":
    dumpfile = "euklides_codebook_128_0_08_May_2026.pkl"
    results = Results(load_results=False)
    results.load_picle_results(dumpfile=dumpfile)

    #codebooks_names = ["euklides_codebook_8_from_64_0.csv", "euklides_codebook_16_from_64_0.csv", "euklides_codebook_32_from_64_0.csv", "euklides_codebook_64_0.csv"]
    codebooks_names = list_files_from_folder(Path.cwd() / "e_cb", "pkl")

    print(codebooks_names)

    cbs = []
    for name in codebooks_names:
        pwd = Path.cwd()                       # bieżący katalog
        path = pwd / "e_cb" / name     # dołącz folder i plik
        cb = Codebook(load=False)
        print(path, str(path)[0:-4])
        cbs.append(cb.load_pkl_codebook(path, ret=True))

    plot_mean_max_per_carrier_in_trace(results=results, codebooks=cbs, save=False, show=True)