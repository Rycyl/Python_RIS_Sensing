import numpy as np
from math import  radians, degrees
import matplotlib.pyplot as plt
from bitstring import BitArray
from class_codebook import Codebook
import matplotlib.cm as cm
import copy
from matplotlib.cm import get_cmap

def ris_x_distance(m, x_ris=0.02):
    return ((x_ris / 2) + (m * x_ris))
    #return (m * x_ris)

def ris_y_distance(n, y_ris = 0.013):
    return ((y_ris / 2) + (n * y_ris))
    #return (n * y_ris)

def u(θ, φ):
    return  sin(θ) * cos(φ)

def v(θ, φ):
    return  sin(θ) *  sin(φ)

def hamming_distance(a, b):
    c = a ^ b
    return c.count(1)

def sin(alfa):
    return  np.sin(radians(alfa))

def cos(alfa):
    return np.cos(radians(alfa))

def AF_from_pattern(pattern, theta_Tx, phi_Tx=0, silent = False):
    """
        Return AF generated for given pattern for angles -90;90
        Inputs:
            pattern : RIS pattern - BitArray(256) / list of len=256
            theta_Tx: Angle of azimuth of Tx 
            phi_Tx  : angle of elevation of Tx
    """
    def AF_single(x_m, y_n, pattern_bit, theta_obs, phi_obs, theta_Tx, phi_Tx=0):

        def Phi_i_mn(x_m, y_n, theta_Tx, phi_Tx):
            a = ris_x_distance(x_m) * sin(theta_Tx) * cos(phi_Tx)
            b = ris_y_distance(y_n) * sin(theta_Tx) * sin(phi_Tx)
            return  K0 * (a + b)

        j = complex(0, 1)
        FQ = 5.53E9     # [Hz]
        C = 299792458   # [m/s]
        LAMBDA = C / FQ # [m/s / 1/s = m/s * s = m]
        K0 = 2 * np.pi / LAMBDA

        a1 =  ris_x_distance(x_m) * u(theta_obs, phi_obs)
        a2 =  ris_y_distance(y_n) * v(theta_obs, phi_obs)
        one = np.exp(-j * K0 *(a1 + a2))
        b = j * Phi_i_mn(x_m, y_n, theta_Tx, phi_Tx)
        two = np.exp(b)
        c = 1 if pattern_bit else -1
        ret_val =  one * two * c
        return ret_val

    AFs = [0] * 180
    if not silent:
        print("AF for pattern: ", pattern.hex)
    
    y_n = 0
    #RIS_element_index = 0
    while y_n < 16:
        x_m = 0
        while x_m < 16:
            kat = -90
            RIS_element_index = (y_n * 16) + x_m
            #print(RIS_element_index)
            while kat < 90:
                AFs[kat+90]+=(AF_single(x_m, y_n, pattern[RIS_element_index], kat, 0, theta_Tx=theta_Tx))
                kat += 1
            x_m += 1
            #end while x_m
        y_n += 1
        #end while y_n
    abs_AF = []
    for x in AFs:
        abs_AF.append(10*np.log10(abs(x)))
    max_value = max(abs_AF)
    max_index = abs_AF.index(max_value) - 90
    if not silent:
        print(f'Maksymalna wartość: {max_value}, Indeks: {max_index}')
    return abs_AF

def plot_AFs(AFs):
    """
        Plot Array Factors
        Inputs:
        AFs : a list of array factors: [[AF1],[AF2],[AF3]....]
    """
    plt.figure(figsize=(10, 6))
    x = range(-90,90)
    for y in AFs:  
        plt.plot(x, y)
    plt.xticks(np.arange(-90, 91, 10))
    plt.yticks(np.arange(0, 30, 5))
    plt.xlim(-90, 90)
    plt.ylim(0, 25)
    plt.xlabel("Rx location [°]")
    plt.ylabel("AF [dB]")
    plt.grid()
    plt.show()

def plot_codebooks_AFs(codebooks_AFs, labels):
    """
        Plot Array Factors
        Inputs:
        AFs : a list of array factors of codebooks: [ [ [AF1],...,[AFn] ], [ [AF1],...,[AFn] ] ]
                            so also like that:    [ [ codebook 1      ], [ codebook 2      ] ]
    """
    colors = get_cmap('tab10')
    plt.figure(figsize=(10, 6))
    x = range(-90,90)
    for i,AFs in enumerate(codebooks_AFs):
        for AF in AFs:
            plt.plot(x, AF, color=colors(i % 10))
        plt.plot([], [], label=labels[i], color=colors(i % 10))  #empty plt for label
    plt.xticks(np.arange(-90, 91, 10))
    plt.yticks(np.arange(0, 30, 5))
    plt.xlim(-90, 90)
    plt.ylim(0, 25)
    plt.xlabel("Rx location [°]")
    plt.ylabel("AF [dB]")
    plt.legend()
    plt.grid()
    plt.show()


def reduce_codebook_by_hamming(codebook):
    """
        Limits the size of a codebook based on Hamming distances between patterns.

        This function iterates through the patterns in the provided 
        codebook and builds a series of codebooks, each corresponding 
        to a specified maximum Hamming distance. The first pattern 
        is always included, and subsequent patterns are added only if 
        they satisfy the distance constraint relative to the already 
        included patterns.

        Inputs:
        - codebook: Codebook object.

        Returns:
        - codebooks_haming: A LIST of codebooks, each consisting of patterns that 
                            adhere to the allowable Hamming distance constraints. 
                            The length of this list corresponds to the range of 
                            distance limits from 0 to 16.

        TO DO:
            maybe change returns to Codebook() obj.
    """
    codebook_patterns=[]
    for pattern in codebook.patterns:
        codebook_patterns.append(pattern.pattern)

    codebooks_haming=[]
    for distance_lim in range(0,17):
        print(distance_lim)
        if distance_lim==0:#0 distance lim are all patterns
            codebooks_haming.append(codebook_patterns)
        else:
            codebooks_haming.append([codebook_patterns[0]])
            for pattern in codebook_patterns: #loop in all patterns
                hamming_min = 1024
                for current_codebook_pattern in codebooks_haming[-1]: #loop current selections
                    haming = hamming_distance(pattern, current_codebook_pattern)/16 #get current pat distance
                    if haming < hamming_min: #if smalller - store
                        haming_min = haming
                if haming >= distance_lim: # if min distance to others > limit distance - add to codebook
                        codebooks_haming[-1].append(pattern)
        #print(codebooks_haming[-1])
        #print("\n\n\n")
    pat_no = []
    for x in codebooks_haming:
        pat_no.append(len(x))
    print(pat_no)

    return codebooks_haming

def plot_codebooks_reduce_by_hamming(codebooks_list, FONTSIZE=16):
    """
        Plots a few codebooks (in list format) sizes, from lists 
        returned by reduce_codebook_by_hamming().

        input:
        codebooks_list: list of lists from reduce_codebook_by_hamming()
        FONTSIZE: font size for plot :O
    """
    plt.plot()
    
    for data,label in codebooks_list:
        pat_no = []
        for y in data:
            pat_no.append(len(y))
        plt.plot(pat_no, marker='o', linewidth=4, markersize=8, label=label)  # 'o' adds markers to the data points
    plt.xlabel('Minimum Hamming Distance Between Patterns in Codebook')
    plt.ylabel('Number of Unique Patterns in Codebook')
    # plt.yscale('log')
    plt.legend()
    plt.rcParams['font.size'] = FONTSIZE
    plt.grid(True)
    plt.show()



def plot_codebooks_metrics(codebooks_metrics, codebooks_lenght, labels):
    """
    This function generates a line plot to visualize the performance metrics of codebooks
    Parameters:
    codebooks_metrics : list of lists
        A list where each inner list contains the metric values for the corresponding codebook. 
    codebooks_length : list
        A list of integers where each integer corresponds to the length of the codebook for which
        the metrics are provided. It should have the same length as the `codebooks_metrics`.
    labels:
        A list of string labels for each codebook
    """
    # Plotting
    labels = labels

    plt.figure(figsize=(10, 6))

    import matplotlib.pyplot as plt
    # Plot each set of metrics
    for i in range(len(all_metrics_modified)):
        plt.plot(all_lengths[i], all_metrics[i], marker='o', label=labels[i])

    #plt.title("Sum of metric of Codebook")
    plt.xlabel("Length of Codebook")
    plt.ylabel("Metric Value")
    plt.legend()
    plt.grid(True)
    plt.show()