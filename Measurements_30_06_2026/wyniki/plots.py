from class_measures_result import Result, Results, Trace
from class_measures_result import dbm_to_mw, mw_to_dbm, linear_mean
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import os
import math
from class_codebook import *
import copy
from pathlib import Path
from typing import List, Iterable, Union
from results_for_codebook import select_results_for_codebook, select_results_for_ids
import json
from scipy.interpolate import griddata
from helpers_defs import *


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
                z[alpha].append(trace.get_truncaded_trace)
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

def plot_pow_in_pos_teams_all_in_one(results, 
                                     codebooks,
                                     show=True, 
                                     save=False, 
                                     Cbs_names=None, 
                                     save_format='png',
                                     save_filename = "pow_sort_rx_",
                                     veryfy_mins = False):
    #results = Results(dumpfile=dumpfile)
    cbs_results = []
    cbs_labels = []
    cbs_len = []
    y_vals = []
    
    Rx_list = results.results[0].Rx_Angle #taken from Rx's from any result   
    #cbs_info = json.load("")
    #TODO function to get from json the cbs_labels and ranges - maybe object to pass from main?
    #ALTERNATE: add a function in codebook class to get upper and lower ID and to name codebook properly?
    
    for cb in codebooks:
        cbs_results.append(select_results_for_codebook(results=results,codebook=cb))
        cbs_len.append(len(cb.patterns))

    powers_cbs = [] # list to store a list of powers from cb [10:20]
    powers_whole_trace_means = [] # list to store mean of all carriers
    powers_max_from_trace = [] # list to store max from traces
    powers_min_from_trace = [] # list to store min from traces

    for cb_results in cbs_results:
        powers_cbs.append([])
        powers_whole_trace_means.append([])
        powers_max_from_trace.append([])
        powers_min_from_trace.append([])
        for result in cb_results.results:
            pats_powers = [] #list to store mean power vals of selected carriers
            pats_means = []
            pats_mins = []
            pats_maxs = []
            for trace in result.traces:
                pats_powers.append(trace.get_mean_by_idx(list(range(10,21))))
                pats_means.append(trace.get_mean())
                pats_maxs.append(trace.get_max())
                pats_mins.append(trace.get_min())
            powers_cbs[-1].append(np.array(pats_powers))
            powers_whole_trace_means[-1].append(np.array(pats_means))
            powers_max_from_trace[-1].append(np.array(pats_maxs))
            powers_min_from_trace[-1].append(np.array(pats_mins))
        powers_cbs[-1] = np.array(powers_cbs[-1]).T
        powers_whole_trace_means[-1] = np.array(powers_whole_trace_means[-1]).T
        powers_max_from_trace[-1] = np.array(powers_max_from_trace[-1]).T
        powers_min_from_trace[-1] = np.array(powers_min_from_trace[-1]).T
        #powers_cbs structure: [CB][RX][PAT] 
        #needed                [RX][CB][PAT_power_vals]
    ####
    # change dims below by GPT!
    # original: powers_cbs[cb_idx][rx_idx] -> PAT_power_vals (numpy array)
    # result: powers_by_rx[RX][CB] = PAT_power_vals
    num_cbs = len(powers_cbs)
    num_rx = len(powers_cbs[0])  # assume non-empty and consistent
    powers_by_rx = []
    powers_mean_by_rx = []
    powers_maxs_by_rx = []
    powers_mins_by_rx = []
    for rx in range(num_rx):
        rx_list = []
        rx_mean = []
        rx_maxs = []
        rx_mins = []
        for cb in range(num_cbs):
            rx_list.append(powers_cbs[cb][rx])
            rx_mean.append(powers_whole_trace_means[cb][rx])
            rx_maxs.append(powers_max_from_trace[cb][rx])
            rx_mins.append(powers_min_from_trace[cb][rx])
        powers_by_rx.append(rx_list)
        powers_mean_by_rx.append(rx_mean)
        powers_maxs_by_rx.append(rx_maxs)
        powers_mins_by_rx.append(rx_mins)
    ####

    #PLOTTING ITERATION 
    # Uzyskaj nazwę folderu, w którym znajduje się skrypt
    folder_name = os.path.dirname(os.path.abspath(__file__))
    plots_folder = os.path.join(folder_name, 'power_in_position_comparison_of_CBs')
    # Utwórz folder "plots", jeśli nie istnieje
    os.makedirs(plots_folder, exist_ok=True)

    FONTSIZE=16
    plt.rcParams['font.size'] = FONTSIZE
    plt.rcParams['lines.linewidth']= 3
    # x_vals = []
    # y_vals = []
    for i,RX in enumerate(powers_by_rx):
        plt.figure(figsize=(10,8))  # Utwórz nową figurę dla każdego wykresu
        for j,CB in enumerate(RX):
            color = plt.cm.tab10(j % 10)
            plt.plot(np.sort(CB), color=color, label=f'{Cbs_names[j]}: mean(trace[10:20])')
            plt.axhline(y=mw_to_dbm(np.mean(dbm_to_mw(np.array(powers_maxs_by_rx[i][j])))), 
                        linestyle='--', 
                        color=color,
                        label=f'{Cbs_names[j]}: mean(max(traces))')
            plt.axhline(y=mw_to_dbm(np.mean(dbm_to_mw(np.array(powers_mean_by_rx[i][j])))), 
                        linestyle='dotted', 
                        color=color,
                        label=f'{Cbs_names[j]}: mean(traces)')
            plt.axhline(y=mw_to_dbm(np.mean(dbm_to_mw(np.array(powers_mins_by_rx[i][j])))), 
                        linestyle='dashdot', 
                        color=color,
                        label=f'{Cbs_names[j]}: mean(min(traces))')
            if veryfy_mins:                        
                for some_val in powers_mins_by_rx[i][j]:
                    plt.axhline(y=some_val, linestyle = '-', color = 'black', label = "",  linewidth=0.1)
        plt.axhline(y=results.get_max_for_RX(Rx_list[i]), color='violet', linestyle='--', label='SC max')
        avg = mw_to_dbm(np.mean(dbm_to_mw(np.array(CB))))
        plt.axhline(y=avg, color='cyan', linestyle='--', label='Linear average')
        #plt.axhline(y=mins[i], color='red', linestyle='--', label='SC min')
        plt.title(f'Rx at {int(Rx_list[i])}°')
        plt.xlabel('N\'th sorted pattern in recieved power')
        plt.ylabel('Recieved power [dBm]')
        #plt.ylim((np.min(data)//5)*5, ((np.max(data.all())//5))*5)  # Ustawienie stałego zakresu osi Y
        plt.grid(True)  # Włączenie linii pomocniczych
        plt.margins()
        plt.legend(loc='lower right',  markerscale=4)
        plt.subplots_adjust(left=0.16, right=0.9, top=0.95, bottom=0.16, wspace=0.2, hspace=0.2)
        if show:
            plt.show()
        if save:
            # Zapisz wykres do pliku w folderze "plots"
            plt.savefig(os.path.join(plots_folder, f'{save_filename}{int(Rx_list[i])}.{save_format}'), format=save_format)    
        plt.close()  # Zamknij figurę, aby nie pokazywać podglądu
        pass


def pow_in_pos_channels(results, 
                        codebooks,
                        show=True, 
                        save=False, 
                        Cbs_names=None, 
                        save_format='png',
                        save_filename = "pow_sort_rx_",
                        veryfy_mins = False):
    """
    does plot plot_pow_in_pos_teams with additional lines:
    min, max, mean
    which represents best/worst/mean channel while using all codebook patterns
    """
    Rx_list = results.results[0].Rx_Angle #taken from Rx's from any result

    cbs_results = []
    cbs_labels = []
    cbs_len = []

    for cb in codebooks:
        cbs_results.append(select_results_for_codebook(results=results,codebook=cb))
        cbs_len.append(len(cb.patterns))

    rxs = None
    min_list = []
    max_list = [] 
    mean_list= []
    pow_list = []
    for cb_results in cbs_results:
        min_list.append([])
        max_list.append([])
        mean_list.append([])
        pow_list.append([])
        mins, rxs = cb_results.get_minimums_by_rx() #minima
        # print(rxs)
        for rx_pos_mins in mins:
            min_list[-1].append(linear_mean(rx_pos_mins))
        maxs, rxs = cb_results.get_maximums_by_rx() #maxy
        # print(rxs)
        for rx_pos_maxs in maxs:
            max_list[-1].append(linear_mean(rx_pos_maxs))
        means, rxs = cb_results.get_means_by_rx() #srednie dla rxow
        # print(rxs)
        for rx_pos_means in means:
            mean_list[-1].append(linear_mean(rx_pos_means))
        mean_pat_rx, rxs = cb_results.get_means_for_patterns_by_rx()
        for aaaaaa in mean_pat_rx:
            aaaaaa = np.sort(aaaaaa)
            pow_list[-1].append(aaaaaa)

    max_ref, trash_rx = results.get_maxs_from_maxs_by_rx()
    # print(trash_rx)
    min_ref, trash_rx = results.get_mins_from_mins_by_rx()
    # print(trash_rx)
    for i,mr in enumerate(max_ref):
        max_ref[i] = linear_mean(mr)
    for i,mr in enumerate(min_ref):
        min_ref[i] = linear_mean(mr)
    #delete duplicates
    max_ref=np.mean(max_ref, axis=1)
    min_ref=np.mean(min_ref, axis=1)

    # print(max_ref)
    # print(min_ref)
    # exit()
    num_cb = len(pow_list)
    num_rx = len(pow_list[0])

    colors = plt.cm.tab10(range(0,10))
    
    # Uzyskaj nazwę folderu, w którym znajduje się skrypt
    folder_name = os.path.dirname(os.path.abspath(__file__))
    plots_folder = os.path.join(folder_name, 'power_in_position_comparison_of_CBs_channels')
    # Utwórz folder "plots", jeśli nie istnieje
    os.makedirs(plots_folder, exist_ok=True)

    for rx in range(num_rx):
        avg = []
        
        plt.figure(figsize=(10,7))
    
        FONTSIZE=16
        plt.rcParams['font.size'] = FONTSIZE
        plt.rcParams['lines.linewidth']= 3
        for cb in range(num_cb):
            color = colors[cb%10]
            pow_vals = pow_list[cb][rx]
            avg.append(linear_mean(np.array(pow_vals)))
            # lineplot
            plt.plot(
                pow_vals,
                color=color,
                linestyle='-',
                label=f'{Cbs_names[cb]} sorted mean(trace)'
            )

            # poziome linie (jedna wartość)
            plt.axhline(
                min_list[cb][rx],
                color=color,
                linestyle='--',
                label=f'{Cbs_names[cb]} mean(min(traces))'
            )

            plt.axhline(
                max_list[cb][rx],
                color=color,
                linestyle=':',
                label=f'{Cbs_names[cb]} mean(max(traces))'
            )

            plt.axhline(
                mean_list[cb][rx],
                color=color,
                linestyle='-.',
                label=f'{Cbs_names[cb]} mean(traces)'
            )
        
        plt.axhline(y=linear_mean(np.array(avg)), color='grey', linestyle='--', label='Linear average')

        plt.axhline(
                max_ref[rx],
                color="magenta",
                linestyle='--',
                label=f'Col opt max'
            )

        plt.axhline(
                min_ref[rx],
                color="cyan",
                linestyle='--',
                label=f'Col opt min'
            )
        
        plt.title(f"Rx at {int(Rx_list[rx])}°")
        plt.grid(True)
        
        plt.legend(
            loc='lower right',
            ncol=1
        )

        plt.xlabel("N'th pattern")
        plt.ylabel("Power [dBm]")
        plt.tight_layout()
        
        if save:
            plt.savefig(os.path.join(plots_folder, f'{save_filename}_rx{rx}.{save_format}'), format=save_format,  bbox_inches='tight')  
        if show:
            plt.show()
    return


def plot_heatmap_3d(results, codebooks, show=True, save=False, Cbs_names=None, save_format='png'):
    Rx_list = results.results[0].Rx_Angle
    xy_list = results.results[0].get_rx_pos_in_xy()

    cbs_results = []
    for cb in codebooks:
        cbs_results.append(select_results_for_codebook(results=results, codebook=cb))

    max_list = []
    pow_list = []

    for cb_results in cbs_results:
        max_list.append([])
        pow_list.append([])

        maxs, _ = cb_results.get_maximums_by_rx()
        for rx_pos_maxs in maxs:
            max_list[-1].append(linear_mean(rx_pos_maxs))

        mean_pat_rx, _ = cb_results.get_means_for_patterns_by_rx()
        for arr in mean_pat_rx:
            arr = np.sort(arr)
            pow_list[-1].append(arr)

    # --- avg per RX ---
    num_cb = len(pow_list)
    num_rx = len(pow_list[0])

    avg_per_rx = []
    for rx in range(num_rx):
        avg = []
        for cb in range(num_cb):
            avg.append(linear_mean(np.array(pow_list[cb][rx])))
        avg_per_rx.append(linear_mean(np.array(avg)))

    avg_per_rx = np.array(avg_per_rx)

    # --- XY ---
    x_vals = np.array(xy_list[0])
    y_vals = np.array(xy_list[1])

    # --- folder ---
    folder_name = os.path.dirname(os.path.abspath(__file__))
    plots_folder = os.path.join(folder_name, 'heatmaps')
    os.makedirs(plots_folder, exist_ok=True)

    # --- pętla po wszystkich seriach ---
    
    # wspólna skala dla wszystkich CB
    all_z = []
    for s in range(num_cb):
        all_z.extend(np.array(max_list[s]) - avg_per_rx)

    global_vmin = np.nanmin(all_z)
    global_vmax = np.nanmax(all_z)

    #petla na ploty
    for seria in range(num_cb):

        # Z = max - avg
        z_vals = np.array(max_list[seria]) - avg_per_rx

        # interpolacja
        xi = np.linspace(x_vals.min(), x_vals.max(), 60)
        yi = np.linspace(y_vals.min(), y_vals.max(), 40)
        Xi, Yi = np.meshgrid(xi, yi)

        Zi = griddata(
            (x_vals, y_vals),
            z_vals,
            (Xi, Yi),
            method='cubic'
        )

        # plotting
        plt.figure(figsize=(10, 4))

        heatmap = plt.contourf(
            Xi, Yi, Zi,
            levels=20,
            cmap='viridis',
            vmin=global_vmin,
            vmax=global_vmax
        )

        plt.scatter(x_vals, y_vals, c='red', s=15)

        cbar = plt.colorbar(heatmap)
        cbar.set_label("max - avg [dBm]")

        title = Cbs_names[seria] if Cbs_names else f"CB {seria}"
        plt.title(f"Heatmap (max - avg) {title}")

        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid(True)

        if save:
            plt.savefig(
                os.path.join(plots_folder, f'heatmap_cb_{seria}.{save_format}'),
                format=save_format,
                bbox_inches='tight'
            )

        if show:
            plt.show()
        else:
            plt.close()

    
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

def plot_minmax_traces(results, 
                       codebooks,
                       show=True, 
                       save=False, 
                       Cbs_names=None, 
                       save_format='png',
                       save_filename="minmax_traces",
                       minmax='max',
                       ref_in_range=None,
                       selection_scope='rx',
                       plot_selected_avg_line=True,
                       plot_cb_linear_avg=False,
                       plot_linear_avg=True,
                       rx_tol=1e-6,
                       c_tol=1e-6):
    """
        Plot truncated traces for:
        - best/worst reference trace, depending on minmax mode,
        - best/worst pattern from each codebook,
        - linear average trace for all patterns at given RX/c position,
        - optionally linear average scalar for all patterns from each codebook.

        IMPORTANT:
        This function does NOT assume that result.traces[pos_idx] means the same
        measurement position for every Result. Instead, it searches traces by:
            (Rx_Angle, c_value)

        Parameters
        ----------
        minmax : str
            'max'  -> plot best codebook pattern and best reference from results.maxs
            'min'  -> plot worst codebook pattern and worst reference from results.mins
            'both' -> plot best/worst codebook patterns and both references

        selection_scope : str
            'rx'     -> choose best/worst pattern separately for current (Rx, c) position
            'global' -> choose best/worst pattern averaged over all available positions

        ref_in_range : None, list/range/tuple, or dict
            If None:
                all references from results.maxs/results.mins are considered.

            If list/range/tuple:
                same ids are used for selected reference source.

            If dict:
                example:
                    {
                        'max': list(range(100100, 100118)),
                        'min': list(range(200100, 200118))
                    }
    """

    if minmax not in ['max', 'min', 'both']:
        raise ValueError("minmax must be one of: 'max', 'min', 'both'")

    if selection_scope not in ['rx', 'global']:
        raise ValueError("selection_scope must be one of: 'rx', 'global'")

    if Cbs_names is None:
        Cbs_names = [f"CB_{i}" for i in range(len(codebooks))]

    if len(Cbs_names) != len(codebooks):
        raise ValueError("Cbs_names must have the same length as codebooks")

    if len(results.results) == 0:
        raise ValueError("results.results is empty")

    Rx_list = results.results[0].Rx_Angle
    C_list = results.results[0].c_values

    # ------------------------------------------------------------
    # Select codebook results
    # ------------------------------------------------------------

    cbs_results = []

    for cb in codebooks:
        cbs_results.append(
            select_results_for_codebook(results=results, codebook=cb)
        )

    # ------------------------------------------------------------
    # Select reference candidates
    # ------------------------------------------------------------

    ref_max_results = []
    ref_min_results = []

    if minmax in ['max', 'both']:
        ref_max_ids = get_ids_for_mode(ref_in_range, 'max')

        ref_max_results = select_ref_results(
            results_obj=results,
            ids=ref_max_ids,
            mode='max'
        )

        if len(ref_max_results) == 0:
            print("WARNING: No max reference candidates found.")

    if minmax in ['min', 'both']:
        ref_min_ids = get_ids_for_mode(ref_in_range, 'min')

        ref_min_results = select_ref_results(
            results_obj=results,
            ids=ref_min_ids,
            mode='min'
        )

        if len(ref_min_results) == 0:
            print("WARNING: No min reference candidates found.")

    # ------------------------------------------------------------
    # Output folder
    # ------------------------------------------------------------

    folder_name = os.path.dirname(os.path.abspath(__file__))
    plots_folder = os.path.join(folder_name, 'minmax_traces')
    os.makedirs(plots_folder, exist_ok=True)

    FONTSIZE = 16
    plt.rcParams['font.size'] = FONTSIZE
    plt.rcParams['lines.linewidth'] = 2

    # ------------------------------------------------------------
    # Plot per measurement position
    # ------------------------------------------------------------

    for pos_idx in range(len(Rx_list)):

        target_rx = Rx_list[pos_idx]
        target_c = C_list[pos_idx]

        plt.figure(figsize=(16, 12))

        # --------------------------------------------------------
        # Reference trace/traces
        # --------------------------------------------------------

        if minmax in ['max', 'both']:
            selected_ref_max, ref_max_avg = choose_ref_result_for_position(
                ref_results=ref_max_results,
                target_rx=target_rx,
                target_c=target_c,
                mode='max',
                rx_tol=rx_tol,
                c_tol=c_tol
            )

            if selected_ref_max is not None:
                ref_trace = get_trace_for_position(
                    result=selected_ref_max,
                    target_rx=target_rx,
                    target_c=target_c,
                    rx_tol=rx_tol,
                    c_tol=c_tol
                )

                if ref_trace is not None:
                    plt.plot(
                        ref_trace,
                        color='magenta',
                        linestyle='-',
                        label=(
                            f"Col opt trace max [{(ref_in_range[0]//100)%1000}:{(ref_in_range[-1]//100)%1000+10}], "
                            f"idx={selected_ref_max.idx}"
                        )
                    )

                    if plot_selected_avg_line and not np.isnan(ref_max_avg):
                        plt.axhline(
                            y=ref_max_avg,
                            color='magenta',
                            linewidth=3,
                            linestyle='--',
                            label="Col opt max avg"
                        )

        if minmax in ['min', 'both']:
            selected_ref_min, ref_min_avg = choose_ref_result_for_position(
                ref_results=ref_min_results,
                target_rx=target_rx,
                target_c=target_c,
                mode='min',
                rx_tol=rx_tol,
                c_tol=c_tol
            )

            if selected_ref_min is not None:
                ref_trace = get_trace_for_position(
                    result=selected_ref_min,
                    target_rx=target_rx,
                    target_c=target_c,
                    rx_tol=rx_tol,
                    c_tol=c_tol
                )

                if ref_trace is not None:
                    plt.plot(
                        ref_trace,
                        color='cyan',
                        linestyle='-',
                        label=(
                            f"Col opt trace min [{(ref_in_range[0]//100)%1000}:{(ref_in_range[-1]//100)%1000+10}],  "
                            f"idx={selected_ref_min.idx}"
                        )
                    )

                    if plot_selected_avg_line and not np.isnan(ref_min_avg):
                        plt.axhline(
                            y=ref_min_avg,
                            color='cyan',
                            linewidth=3,
                            linestyle='--',
                            label="Col opt min avg"
                        )

        # --------------------------------------------------------
        # Linear average trace for all patterns from full results
        # --------------------------------------------------------

        if plot_linear_avg:
            linear_avg_trace, linear_avg = linear_avg_trace_for_position(
                result_list=results.results,
                target_rx=target_rx,
                target_c=target_c,
                rx_tol=rx_tol,
                c_tol=c_tol
            )

            if linear_avg_trace is not None:
                plt.plot(
                    linear_avg_trace,
                    color='gray',
                    linestyle='-',
                    label="All patterns linear avg trace"
                )

                if not np.isnan(linear_avg):
                    plt.axhline(
                        y=linear_avg,
                        color='gray',
                        linewidth=3,
                        linestyle='--',
                        label="All patterns linear avg"
                    )

        # --------------------------------------------------------
        # Codebook traces and averages
        # --------------------------------------------------------

        for cb_idx, cb_results in enumerate(cbs_results):

            color = plt.cm.tab10(cb_idx % 10)
            cb_name = Cbs_names[cb_idx]

            # ----------------------------------------------------
            # Linear average scalar for all patterns in this codebook
            # at selected (Rx, c) position
            # ----------------------------------------------------

            if plot_cb_linear_avg:
                cb_linear_avg = codebook_linear_avg_for_position(
                    cb_results=cb_results,
                    target_rx=target_rx,
                    target_c=target_c,
                    rx_tol=rx_tol,
                    c_tol=c_tol
                )

                if not np.isnan(cb_linear_avg):
                    plt.axhline(
                        y=cb_linear_avg,
                        color=color,
                        linewidth=3,
                        linestyle='--',
                        label=f"{cb_name} all patterns linear avg"
                    )

            # ----------------------------------------------------
            # Select best/worst codebook pattern
            # ----------------------------------------------------

            modes_to_plot = []

            if minmax in ['max', 'both']:
                modes_to_plot.append('max')

            if minmax in ['min', 'both']:
                modes_to_plot.append('min')

            for mode in modes_to_plot:

                selected_result, avg_power = choose_codebook_result(
                    cb_results=cb_results,
                    target_rx=target_rx,
                    target_c=target_c,
                    mode=mode,
                    selection_scope=selection_scope,
                    rx_tol=rx_tol,
                    c_tol=c_tol
                )

                if selected_result is None:
                    continue

                trace = get_trace_for_position(
                    result=selected_result,
                    target_rx=target_rx,
                    target_c=target_c,
                    rx_tol=rx_tol,
                    c_tol=c_tol
                )

                if trace is None:
                    continue

                if mode == 'max':
                    linestyle = '-'
                    avg_line_style = '-.'
                    label_mode = 'best'
                else:
                    linestyle = '-'
                    avg_line_style = '-.'
                    label_mode = 'worst'

                plt.plot(
                    trace,
                    color=color,
                    linestyle=linestyle,
                    label=(
                        f"{cb_name} {label_mode} pattern trace, "
                        f"idx={selected_result.idx}"
                    )
                )

                if plot_selected_avg_line and not np.isnan(avg_power):
                    plt.axhline(
                        y=avg_power,
                        color=color,
                        linewidth=3,
                        linestyle=avg_line_style,
                        label=f"{cb_name} {label_mode} pattern avg"
                    )

        # --------------------------------------------------------
        # Formatting
        # ------------------------------------------------------------

        rx_angle = int(target_rx)

        plt.title(f"Rx at {rx_angle}°")
        plt.xlabel("Subcarrier index")
        plt.ylabel("Power [dBm]")
        plt.grid(True)
        plt.legend(loc='best')
        plt.tight_layout()

        if save:
            filename = (
                f"{pos_idx}_{save_filename}_rx_{rx_angle}_"
                f"{minmax}_{selection_scope}.{save_format}"
            )

            plt.savefig(
                os.path.join(plots_folder, filename),
                format=save_format,
                bbox_inches='tight'
            )
            print(f"FILE SAVED: {filename}")

        if show:
            plt.show()
        else:
            plt.close()
    print("Done plotting!")
    return

def plot_optimization_process_traces(results,
                                     process='max',
                                     opt_N=None,
                                     iteration_range=None,
                                     show=True,
                                     save=False,
                                     save_format='png',
                                     save_filename='optimization_process_traces',
                                     rx_tol=1e-6,
                                     c_tol=1e-6,
                                     cmap_name=None,
                                     highlight_optimized_range=False,
                                     optimized_range_len=10):
    """
        Plot truncated traces only for optimization results from results.maxs/results.mins.

        The plotted traces are selected by optimization process encoded in Result.idx.

        ID format:
            first digit:
                1 -> maximization
                2 -> minimization

            middle digits:
                first optimized subcarrier N

            last two digits:
                i-th optimization in given localization/process

        Parameters
        ----------
        results : Results
            Main Results object.

        process : str
            'max' -> plot traces from results.maxs
            'min' -> plot traces from results.mins

        opt_N : int
            First optimized subcarrier N.
            Example:
                opt_N=10 means process optimized subcarriers N...N+10.

        iteration_range : iterable or None
            Optional filter for optimization iterations.
            Example:
                range(0, 18)

        show : bool
            If True, show plots.

        save : bool
            If True, save plots.

        save_format : str
            File format, e.g. 'png', 'svg', 'pdf'.

        save_filename : str
            Prefix of saved files.

        rx_tol, c_tol : float
            Tolerances for matching measurement position:
                (Rx_Angle, c_value)

        cmap_name : str or None
            Matplotlib colormap name.
            If None:
                'Blues' for max,
                'Reds' for min.

        highlight_optimized_range : bool
            If True, marks optimized carrier range [N, N + optimized_range_len].

        optimized_range_len : int
            Length of optimized carrier range.
    """

    if process not in ['max', 'min']:
        raise ValueError("process must be one of: 'max', 'min'")

    if opt_N is None:
        raise ValueError("opt_N must be given, e.g. opt_N=10")

    if len(results.results) == 0:
        raise ValueError("results.results is empty")

    Rx_list = results.results[0].Rx_Angle
    C_list = results.results[0].c_values

    selected = select_optimization_results(
        results=results,
        process=process,
        opt_N=opt_N,
        iteration_range=iteration_range
    )

    if len(selected) == 0:
        print(
            f"WARNING: No optimization results found for "
            f"process={process}, opt_N={opt_N}, iteration_range={iteration_range}"
        )
        return

    iterations = np.array([parsed["iteration"] for _, parsed in selected])

    iter_min = np.min(iterations)
    iter_max = np.max(iterations)

    if iter_max == iter_min:
        norm_iterations = np.ones_like(iterations, dtype=float)
    else:
        norm_iterations = (iterations - iter_min) / (iter_max - iter_min)

    if cmap_name is None:
        if process == 'max':
            cmap_name = 'Blues'
        else:
            cmap_name = 'Reds'

    cmap = plt.get_cmap(cmap_name)

    # Avoid very pale colors.
    colors = [
        cmap(0.25 + 0.75 * norm_val)
        for norm_val in norm_iterations
    ]

    folder_name = os.path.dirname(os.path.abspath(__file__))
    plots_folder = os.path.join(folder_name, 'optimization_process_traces')
    os.makedirs(plots_folder, exist_ok=True)

    FONTSIZE = 16
    plt.rcParams['font.size'] = FONTSIZE
    plt.rcParams['lines.linewidth'] = 2

    process_label = "Maximization" if process == 'max' else "Minimization"

    for pos_idx in range(len(Rx_list)):

        target_rx = Rx_list[pos_idx]
        target_c = C_list[pos_idx]

        plt.figure(figsize=(12, 8))

        plotted_any = False

        for (result, parsed), color in zip(selected, colors):

            trace = get_trace_for_position(
                result=result,
                target_rx=target_rx,
                target_c=target_c,
                rx_tol=rx_tol,
                c_tol=c_tol
            )

            if trace is None:
                continue

            iteration = parsed["iteration"]

            plt.plot(
                trace,
                color=color,
                linestyle='-',
                label=f"i={iteration}, idx={result.idx}"
            )

            plt.axhline(
                y = linear_mean(trace[opt_N:opt_N+optimized_range_len]),
                color = color,
                linestyle = "--"
            )
            plotted_any = True

        if not plotted_any:
            plt.close()
            print(
                f"WARNING: No traces found for Rx={target_rx}, c={target_c}, "
                f"process={process}, opt_N={opt_N}"
            )
            continue

        if highlight_optimized_range:
            plt.axvspan(
                opt_N,
                opt_N + optimized_range_len,
                color='gray',
                alpha=0.15,
                label=f"Optimized carriers {opt_N}:{opt_N + optimized_range_len}"
            )

        rx_angle = int(target_rx)

        plt.title(
            f"{process_label} col opt {opt_N}:{opt_N+10}, Rx at {rx_angle}°"
        )

        plt.xlabel("Subcarrier index")
        plt.ylabel("Power [dBm]")
        plt.grid(True)

        sm = plt.cm.ScalarMappable(
            cmap=cmap,
            norm=plt.Normalize(vmin=iter_min, vmax=iter_max)
        )
        sm.set_array([])

        cbar = plt.colorbar(sm, ax=plt.gca())
        cbar.set_label("Optimization iteration i")

        # plt.legend(loc='best')
        plt.tight_layout()

        if save:
            filename = (
                f"{pos_idx}_{save_filename}_"
                f"{process}_N{opt_N}_"
                f"rx_{rx_angle}.{save_format}"
            )

            plt.savefig(
                os.path.join(plots_folder, filename),
                format=save_format,
                bbox_inches='tight'
            )
            print(f"Saved plot: {filename}")
        if show:
            plt.show()
        else:
            plt.close()
    print("Done plotting optimisation process:", process)
    return


if __name__=="__main__":
    # dumpfile = "euklides_codebook_128_0_08_May_2026.pkl"
    # results = Results(load_results=False)
    # results.load_picle_results(dumpfile=dumpfile)

    # #codebooks_names = ["euklides_codebook_8_from_64_0.csv", "euklides_codebook_16_from_64_0.csv", "euklides_codebook_32_from_64_0.csv", "euklides_codebook_64_0.csv"]
    # codebooks_names = list_files_from_folder(Path.cwd() / "e_cb", "pkl")

    # print(codebooks_names)

    # cbs = []
    # for name in codebooks_names:
    #     pwd = Path.cwd()               # bieżący katalog
    #     path = pwd / "e_cb" / name     # dołącz folder i plik
    #     cb = Codebook(load=False)
    #     print(path, str(path)[0:-4])
    #     cbs.append(cb.load_pkl_codebook(path, ret=True))

    # plot_mean_max_per_carrier_in_trace(results=results, codebooks=cbs, save=False, show=True)

    results = Results(dumpfile="results.pkl")
    pass
    cbs_files = ["codebooks/Arranged_codebook_Tx-72_RX0-90_.csv", "codebooks/full_codebook_TXat-72_RXAT0-90_6rot_.csv", "codebooks/full_codebook_TXat-72_RXAT0-90_6rot_.csv"]
    cbs_names = ["EA_CB", "FEA_CB", "EU_CB"]
    cbs = []
    for cb_file in cbs_files:
        cbs.append(Codebook(dumpfile=cb_file, filename=cb_file))
    
    pass

    # for i, t in enumerate(results.results[-1].traces[-1].trace):
    #     if i<(len(results.results[-1].traces[-1].trace)/2 -100):
    #         continue
    #     else:
    #         print(i, t)
    #     if i > (len(results.results[-1].traces[-1].trace)/2 + 100):
    #         break
    # print(len(results.results[-1].traces[-1].trace))
    # exit()
    save = True
    show = not save
    veryfy_mins = True
    save_file_format = 'png'
    # pow_in_pos_channels(results=results,
    #                                  codebooks=cbs,
    #                                  show=show, 
    #                                  save=save, 
    #                                  Cbs_names=["EU_CB", "EA_CB"], 
    #                                  save_format=save_file_format,
    #                                  veryfy_mins = veryfy_mins,
    #                                  save_filename="Min_weryfikacja_rx"
    #                                 )

    plot_heatmap_3d(results=results,
                    codebooks=cbs,
                    show=show, 
                    save=save, 
                    Cbs_names=cbs_names, 
                    save_format=save_file_format
                    )

    # plot_minmax_traces(
    #     results=results,
    #     codebooks=cbs,
    #     Cbs_names=["EU_CB", "EA_CB"],
    #     minmax='max',
    #     ref_in_range=list(range(100001, 100017)),
    #     show=show,
    #     save=save
    # )

    # plot_minmax_traces(
    #     results=results,
    #     codebooks=cbs,
    #     Cbs_names=["EU_CB", "EA_CB"],
    #     minmax='min',
    #     ref_in_range=list(range(200001, 200017)),
    #     show=show,
    #     save=save
    # )

    # plot_optimization_process_traces(
    #     results=results,
    #     process='min',
    #     opt_N=0,
    #     show=show,
    #     save=save,
    #     cmap_name="Reds"
    # )   