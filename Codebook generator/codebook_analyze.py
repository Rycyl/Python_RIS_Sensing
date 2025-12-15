import numpy as np
from math import  radians, degrees
import matplotlib.pyplot as plt
from bitstring import BitArray
from class_codebook import Codebook
import matplotlib.cm as cm
import copy

def hamming_distance(a, b):
    c = a ^ b
    return c.count(1)

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