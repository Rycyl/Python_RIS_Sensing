import numpy as np
from math import  radians, degrees
import matplotlib.pyplot as plt
import numpy
#import RIS_pattern_viewgenerator
import csv
import threading
import cmath
from bitstring import BitArray


global FQ, C, LAMBDA, K0, j, x_ris, y_ris, DEBUG
DEBUG = False
x_ris = 0.02
y_ris = 0.013
j = complex(0, 1)

FQ = 5.53E9     # [Hz]
C = 299792458   # [m/s]
LAMBDA = C / FQ # [m/s / 1/s = m/s * s = m]
K0 = 2 * np.pi / LAMBDA

print("LAMBDA = ", LAMBDA, "K0 = ", K0)

def ris_x_distance(m):
    return ((x_ris / 2) + (m * x_ris))
    # return (m * x_ris)

def ris_y_distance(n):
    return ((y_ris / 2) + (n * y_ris))
    # return (n * y_ris)

def sin(alfa):
    return  np.sin(radians(alfa))

def cos(alfa):
    return np.cos(radians(alfa))

def Phi_i_mn(x_m, y_n, θ_i, φ_i):
    return K0 * (ris_x_distance(x_m) *  sin(θ_i) * cos(φ_i) + ris_y_distance(y_n) *  sin(θ_i) *  sin(φ_i))

def Phi_d_mn(x_m, y_n, θ_d, φ_d):
    return K0 * (ris_x_distance(x_m) *  sin(θ_d) * cos(φ_d) + ris_y_distance(y_n) *  sin(θ_d) *  sin(φ_d))

def Phi_mn(x_m, y_n, θ_i, θ_d, φ_i, φ_d, phase_shift=0):
    ret = Phi_i_mn(x_m, y_n, θ_i, φ_i) - Phi_d_mn(x_m, y_n, θ_d, φ_d) + radians(phase_shift)
    if DEBUG:
        print("PHI_MN = ", ret)
    return ret

def Phi_mn_quant(x_m, y_n, θ_i, θ_d, φ_i, φ_d, phase_shift=0, num_values=2):
    Phi = Phi_mn(x_m, y_n, θ_i, θ_d, φ_i, φ_d, phase_shift)
    Phi_a = abs(Phi)
    Phi_a = Phi_a % (2 * np.pi)
    step_size = (2 * np.pi) / num_values
    quantized_phase = (Phi_a // step_size) * step_size
    #print("phi: ", Phi_a, "  Quant: ", quantized_phase)
    return 0 if quantized_phase else 1

def u(θ, φ):
    return  sin(θ) * cos(φ)

def v(θ, φ):
    return  sin(θ) *  sin(φ)

def AF_single_q(x_m, y_n, θ, φ, θi, θd, φ_i=0, φ_d=0):
    a = -j * K0 * ((x_ris / 2 + x_m * x_ris) * u(θ, φ) + (y_ris / 2 + y_n * y_ris)* v(θ, φ))
    one = np.exp(a)
    b = j * Phi_i_mn(x_m, y_n, θi, φ_i)
    two = np.exp(b)
    c = -j * Phi_mn(x_m, y_n, θi, θd, φ_i, φ_d)
    three = np.exp(c)
    #binary Quant
    if three.real > 0:
    	three = 1
    else:
    	three = -1
    # print(1, one, abs(one), cmath.phase(one))
    # print(2, two, abs(two), cmath.phase(two))
    # print(3, three, abs(three), cmath.phase(three))
    ret_val =  one * two * three
    #if DEBUG:
        #print(ret_val)
    return ret_val

def AF_single(x_m, y_n, θ, φ, θi, θd, φ_i=0, φ_d=0):
    a = -j * K0 * ((x_ris / 2 + x_m * x_ris) * u(θ, φ) + (y_ris / 2 + y_n * y_ris)* v(θ, φ))
    one = np.exp(a)
    b = j * Phi_i_mn(x_m, y_n, θi, φ_i)
    two = np.exp(b)
    c = -j * Phi_mn(x_m, y_n, θi, θd, φ_i, φ_d)
    three = np.exp(c)
    # print(one, abs(one), cmath.phase(one))
    # print(two, abs(two), cmath.phase(two))
    # print(three, abs(three), cmath.phase(three))
    ret_val =  one * two * three
    #if DEBUG:
        #print(ret_val)
    return ret_val

def AF(θi, θd, quant=True, af_deg_step = 1, φ_i=0, φ_d=0):
    kat = -90
    AFs = [0] * 180
    print("AF for: θi = ", θi, " θd = ", θd)
    y_n = 7
    while y_n >= -8:
        x_m = -8
        while x_m < 8:
            kat = -90
            while kat < 90:
                #print(kat, kat+90)
                if quant:
                    AFs[kat+90]+=(AF_single_q(x_m, y_n,  kat, 0, θi, θd, φ_i, φ_d))
                else:
                    AFs[kat+90]+=(AF_single(x_m, y_n,  kat, 0, θi, θd, φ_i, φ_d))
                kat += af_deg_step
            x_m += 1
            #end while x_m
        y_n -= 1
        #end while y_n
    if DEBUG:
        i = 0
        for x in AFs:
            if x!=0:
                print(i, abs(x))
                i+=1
    abs_AF = []
    for x in AFs:
        abs_AF.append(abs(x)**2)
    max_value = max(abs_AF)  # Znajdź maksymalną wartość
    max_index = abs_AF.index(max_value) - 90 # Znajdź indeks maksymalnej wartości

    print(f'Maksymalna wartość: {max_value}, Indeks: {max_index}')
    return abs_AF
    

def pattern_generate(θ_i_treshold=-90, θ_i_step=10, θ_i_start=0, θ_d_treshold=90, θ_d_step=10, θ_d_start=0, phase_shift=0, stack_repeats=False):
    patterns_bin = []
    patterns_deg = []
    θ_i = θ_i_start
    φ_i, φ_d = 0, 0
    degs = []
    while θ_i > θ_i_treshold:
        θ_d = θ_d_start
        while θ_d < θ_d_treshold:
            θ_r = 0
            while θ_r <= 9:
                θi, θd = θ_i + θ_r, θ_d - θ_r
                pattern_bin, pattern_deg = [], []
                print("generating pattern for θ_i, θ_d, θ_r, shift::", θ_i, θ_d, θ_r, phase_shift)
                y_n = 7
                while y_n >= -8:
                    x_m = -8
                    while x_m < 8:
                        pattern_bin.append(int(Phi_mn_quant(x_m, y_n, θi, θd, φ_i, φ_d, phase_shift=phase_shift)))
                        pattern_deg.append(int(degrees(Phi_mn(x_m, y_n, θi, θd, φ_i, φ_d))))
                        x_m += 1
                        #end while x_m
                    y_n -= 100 #normalnie -1 ale chcemy przyspieszyc bo nie ma elewacji
                    #end while y_n
                if stack_repeats:
                    if pattern_bin in patterns_bin:
                        index = patterns_bin.index(pattern_bin)
                        degs[index].append([θi, θd, phase_shift])
                    else:
                        patterns_bin.append(pattern_bin)
                        patterns_deg.append(pattern_deg)
                        degs.append([[θi, θd, phase_shift]])
                else:
                    patterns_bin.append(pattern_bin)
                    patterns_deg.append(pattern_deg)
                    degs.append([θi, θd, phase_shift])
                θ_r += 100
            θ_d += θ_d_step
        θ_i += θ_i_step
    return patterns_bin, patterns_deg, degs

def pat_print(pattern):
    for i, x in enumerate(pattern):
        print(x, "  ", end="" if (i + 1) % 16 else "\n")
    print()

def thread_target(θ_i, θ_d, quant):
    result = AF(θ_i, θ_d, quant)
    AFs.append(result)

## AF generator

# AFs = []
# θ_i = 0
# while θ_i >= -90:
#     θ_d = float(input("podaj kat:: "))
#     while θ_d <= 90:
#         AFs.append(AF(θ_i, θ_d, quant=True, af_deg_step=1))
#         θ_d = float(input("podaj kat:: "))
#         #θ_d += 20
#     θ_i -= 100

# # Specify the filename
# filename = 'output.csv'

# # Write to CSV
# with open(filename, mode='w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(AFs)

# print(f'Data written to {filename}')


#######################
## PATTERN GENERATOR ##
#######################

RIS_patterns = []
patterns_angles = []
pat_counter = 0
phase_shift = 0
while phase_shift < 360:
    p_b, p_d, degs = pattern_generate(θ_i_treshold=-90, θ_i_step=-1, θ_i_start=0, θ_d_treshold=90, θ_d_step=1, θ_d_start=0, stack_repeats=True, phase_shift=phase_shift)
    for i in range(len(p_b)):
        #print(degs[i])
        #pat_print(p_b[i])
        c_pat = BitArray(p_b[i])
        if c_pat not in RIS_patterns:
            pat_counter += 1
            RIS_patterns.append(c_pat * 16)  # Powielanie wzoru 16 razy
            patterns_angles.append(degs[i])  
        else:
            # Jeśli wzór już istnieje, znajdź jego indeks
            index = RIS_patterns.index(c_pat * 16)  # Używamy powielonego wzoru do znalezienia indeksu
            if c_pat in patterns_angles:
                patterns_angles[c_pat].extend(degs)
    phase_shift+=1

#    if i > 1:
#        prev_pat = p_b[i-1]
#        if prev_pat == p_b[i]:
#            print("Takie same")
    #print("\n\n\n")

print("N diff patterns:: ", pat_counter)


#  # Write to CSV
filename = "Big_Codebook.csv"
with open(filename, mode='w', newline='') as file:
    for i in range(len(RIS_patterns)):
        #file.write(RIS_patterns[i].hex + ";" + "θ_i=" + str(degs[i][0]) + " θ_d=" + str(degs[i][1]) + "\n")
        file.write(RIS_patterns[i].hex + ";" + str(patterns_angles[i]) + "\n")



print(f'Data written to {filename}')

