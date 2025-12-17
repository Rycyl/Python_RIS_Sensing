import numpy as np
from math import  radians, degrees
import matplotlib.pyplot as plt
from bitstring import BitArray
from class_codebook import Codebook
import matplotlib.cm as cm
import copy

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

def plot_codebook_reduce_by_hamming(dumpfile, FONTSIZE=16):
    codebook_instance = Codebook(dumpfile=dumpfile)
    codebook_patterns = []
    for pattern in codebook_instance.patterns:
        codebook_patterns.append(pattern.pattern)

    codebooks_haming=[]
    for distance in range(0,16):
        #print(distance)
        if distance==0:
            codebooks_haming.append(codebook_patterns)
        else:
            codebooks_haming.append([codebook_patterns[0]])
            for pattern in codebook_patterns:
                haming_min = 20
                for current_codebook_pattern in codebooks_haming[-1]:
                    haming = hamming_distance(pattern, current_codebook_pattern)/16
                    if haming < haming_min:
                        haming_min = copy.copy(haming)
                if haming_min > distance:
                    codebooks_haming[-1].append(pattern)
        #print(codebooks_haming[-1])
        #print("\n\n\n")
    pat_no = []
    for x in codebooks_haming:
        pat_no.append(len(x))
    print(pat_no)
    # Create a simple line plot

    plt.rcParams['font.size'] = FONTSIZE
    plt.plot(pat_no, marker='o', linewidth=4, markersize=8)  # 'o' adds markers to the data points
    plt.xlabel('Minimum Hamming Distance Between Patterns in Codebook')
    plt.ylabel('Number of Unique Patterns in Codebook')
    # plt.yscale('log')
    plt.grid(True)
    plt.show()


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
    
    y_n = 7
    #RIS_element_index = 0
    while y_n >= -8:
        x_m = -8
        while x_m < 8:
            kat = -90
            RIS_element_index = ((y_n+8) * (x_m+8)) + x_m + 8
            while kat < 90:
                AFs[kat+90]+=(AF_single(x_m, y_n, pattern[RIS_element_index], kat, 0, theta_Tx=theta_Tx))
                kat += 1
            x_m += 1
            #end while x_m
        y_n -= 1
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
    plt.figure(figsize=(10, 6))
    x = range(-90,90)
    for y in AFs:  
        plt.plot(x, y)
    plt.xticks(np.arange(-90, 91, 10))
    plt.yticks(np.arange(0, 30, 5))
    plt.xlim(-90, 90)
    plt.xlabel("Rx location [°]")
    plt.ylabel("AF [dB]")
    plt.grid()
    plt.show()