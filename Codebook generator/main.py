import numpy as np
from math import  radians, degrees
import matplotlib.pyplot as plt
import numpy
#import RIS_pattern_viewgenerator
import csv
import threading
import cmath
from bitstring import BitArray
from class_codebook import Codebook
import matplotlib.cm as cm

global FQ, C, LAMBDA, K0, j, x_ris, y_ris, DEBUG
DEBUG = False
j = complex(0, 1)

FQ = 5.53E9     # [Hz]
C = 299792458   # [m/s]
LAMBDA = C / FQ # [m/s / 1/s = m/s * s = m]
K0 = 2 * np.pi / LAMBDA
x_ris = 0.02
y_ris = 0.013
# print("LAMBDA = ", LAMBDA, "K0 = ", K0)

def ris_x_distance(m):
    return ((x_ris / 2) + (m * x_ris))
    #return (m * x_ris)

def ris_y_distance(n):
    return ((y_ris / 2) + (n * y_ris))
    #return (n * y_ris)

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

def Phi_mn_quant(x_m, y_n, θ_i, θ_d, φ_i, φ_d, phase_shift=0, num_values=2, for_AF=False):
    Phi = Phi_mn(x_m, y_n, θ_i, θ_d, φ_i, φ_d, phase_shift)
    Phi_a = abs(Phi)
    Phi_a = Phi_a % (2 * np.pi)
    step_size = (2 * np.pi) / num_values
    quantized_phase = round(Phi_a / step_size) * step_size
    if for_AF:
        #print(quantized_phase)
        return quantized_phase
    #print("phi: ", Phi_a, "  Quant: ", quantized_phase)
    return 0 if quantized_phase else 1

def u(θ, φ):
    return  sin(θ) * cos(φ)

def v(θ, φ):
    return  sin(θ) *  sin(φ)

def AF_single_q(x_m, y_n, θ, φ, θi, θd, φ_i=0, φ_d=0, phase_shift=0):
    a = -j * K0 * ((x_ris / 2 + x_m * x_ris) * u(θ, φ) + (y_ris / 2 + y_n * y_ris)* v(θ, φ))
    #a = -j * K0 * ((ris_x_distance(x_m)) * u(θ, φ) + (ris_y_distance(y_n))* v(θ, φ))
    one = np.exp(a)
    b = j * Phi_i_mn(x_m, y_n, θi, φ_i)
    two = np.exp(b)
    c = -j * Phi_mn_quant(x_m, y_n, θi, θd, φ_i, φ_d, phase_shift,for_AF=True)
    #print(degrees(Phi_mn_quant(x_m, y_n, θi, θd, φ_i, φ_d, phase_shift,for_AF=True)))
    three = np.exp(c)
    #print(three)
    ret_val =  one * two * three
    print((ret_val))
    #if DEBUG:
        #print(ret_val)
    return ret_val

def AF_single(x_m, y_n, θ, φ, θi, θd, φ_i=0, φ_d=0, phase_shift=0):
    a = -j * K0 * ((x_ris / 2 + x_m * x_ris) * u(θ, φ) + (y_ris / 2 + y_n * y_ris)* v(θ, φ))
    #a = -j * K0 * ((ris_x_distance(x_m)) * u(θ, φ) + (ris_y_distance(y_n))* v(θ, φ))
    one = np.exp(a)
    b = j * Phi_i_mn(x_m, y_n, θi, φ_i)
    two = np.exp(b)
    c = -j * Phi_mn(x_m, y_n, θi, θd, φ_i, φ_d, phase_shift=phase_shift)
    three = np.exp(c)
    ret_val =  one * two * three
    #if DEBUG:
        #print(ret_val)
    return ret_val

def AF(θi, θd, quant=True, af_deg_step = 1, φ_i=0, φ_d=0, phase_shift=0):
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
                    AFs[kat+90]+=(AF_single_q(x_m, y_n,  kat, 0, θi, θd, φ_i, φ_d, phase_shift))
                else:
                    AFs[kat+90]+=(AF_single(x_m, y_n,  kat, 0, θi, θd, φ_i, φ_d, phase_shift))
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
        #print(abs(x))
        abs_AF.append(abs(x))
    max_value = max(abs_AF)  # Znajdź maksymalną wartość
    max_index = abs_AF.index(max_value) - 90 # Znajdź indeks maksymalnej wartości
    max_value = 10*np.log10(max_value)

    print(f'Maksymalna wartość: {max_value}, Indeks: {max_index}')
    return abs_AF
    

def pattern_generate(θ_i_treshold=-90, θ_i_step=10, θ_i_start=0, θ_d_treshold=90, θ_d_step=10, θ_d_start=0, phase_shift=0, stack_repeats=True):
    patterns_bin = [] #skwantowane patterny
    patterns_deg = [] #patterny w formie idealnych przesunięć - faz
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
                #print("generating pattern for θ_i, θ_d, θ_r, shift::", θ_i, θ_d, θ_r, phase_shift)
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

#######################
## CODEBOOK GENERATOR #
#######################

def codebook_generate(θ_i_treshold=-90, θ_i_step=-100, θ_i_start=-48, θ_d_treshold=90, theta_d_step=1, θ_d_start=0, stack_repeats=True, phase_shift=0, phase_shift_step=1):
    try:
        print("try load codebook")
        filename = "Big_Codebook_by_"+str(phase_shift_step)+"_phi_s_step_"+ str(theta_d_step)+ "_theta_d_step.csv"
        filename = filename[0:-4] + "_v2.csv"
        codebook_object = Codebook(dumpfile=(filename[0:-4]+".pkl"), filename=filename)
        return len(codebook_object.patterns)
    except:
        print("generating codebook")
        RIS_patterns = []
        patterns_angles = []
        pat_counter = 0
        phase_shift = 0
        while phase_shift < 360:
            p_b, p_d, degs = pattern_generate(θ_i_treshold=θ_i_treshold, θ_i_step=θ_i_step, θ_i_start=θ_i_start, θ_d_treshold=θ_d_treshold, θ_d_step=theta_d_step, θ_d_start=θ_d_start, stack_repeats=stack_repeats, phase_shift=phase_shift)
            for i in range(len(p_b)):
                #print(degs[i])
                #pat_print(p_b[i])
                c_pat = BitArray(p_b[i]) # tu trzeba by 16 razy powielać, wtedy codebook eval bedzie niepotrzebne bo sie poprawnie zmerguja ale z jakiegos powodu nie dziala wtedy
                if c_pat not in RIS_patterns:
                    pat_counter += 1
                    RIS_patterns.append(c_pat*16)  # dodaj pattern do listy
                    patterns_angles.append(degs[i])  # dodaj kąty patternu do listy
                else:
                    # Jeśli wzór już istnieje, znajdź jego indeks
                    index = RIS_patterns.index(c_pat)  # Używamy powielonego wzoru do znalezienia indeksu
                    if c_pat in patterns_angles:
                        patterns_angles[c_pat].extend(degs)
            phase_shift+=phase_shift_step

        #    if i > 1:
        #        prev_pat = p_b[i-1]
        #        if prev_pat == p_b[i]:
        #            print("Takie same")
            #print("\n\n\n")

        print("N diff patterns:: ", pat_counter)


        #  # Write to CSV
        filename = "Big_Codebook_by_"+str(phase_shift_step)+"_phi_s_step_"+ str(theta_d_step)+ "_theta_d_step.csv"
        with open(filename, mode='w', newline='') as file:
            for i in range(len(RIS_patterns)):
                #file.write(RIS_patterns[i].hex + ";" + "θ_i=" + str(degs[i][0]) + " θ_d=" + str(degs[i][1]) + "\n")
                file.write(RIS_patterns[i].hex + ";" + str(patterns_angles[i]) + "\n")
        print(f'Data written to {filename}')

        from eval import codebook_eval

        codebook_eval(filename)

        filename = filename[0:-4] + "_v2.csv"
        codebook_object = Codebook(dumpfile=(filename[0:-4]+".pkl"), filename=filename)
        return len(codebook_object.patterns)



def plot_no_unique_patterns(xs, ys, labels, FONTSIZE=16):
    
    plt.figure(figsize=(10, 6))
    for i,y in enumerate(ys):
        plt.plot(y, xs[i], marker='o', linestyle='-', label=labels[i])
    # Adding titles and labels
    plt.xscale('log')
    plt.xlabel('Step of parameter [◦]', fontsize=FONTSIZE)
    plt.ylabel('Unique Pattern Amount in Codebook', fontsize=FONTSIZE)
    # Show grid
    plt.legend(fontsize=FONTSIZE)
    plt.grid()

    # Display the plot
    plt.show()




def plot_pattern_occurence(codebook_dumpfile):
    codebook_instance = Codebook(dumpfile=codebook_dumpfile)
    indeksy_wystapien = []
    xs = []
    ys = []

    tx_pos = -48
    rx_pos = 40
    for i,pattern in enumerate(codebook_instance.patterns):
        for angl in pattern.angles:
            if angl[0]==tx_pos and angl[1]==rx_pos: #and angl[2]==0:
                if i not in indeksy_wystapien:
                    indeksy_wystapien.append(i)

    # print(indeksy_wystapien)
    # print()
    # print(len(indeksy_wystapien))
    unique_points = set() 
    for i in indeksy_wystapien:
        # print("I",i)
        xs.append([])
        ys.append([])
        for ang in codebook_instance.patterns[i].angles:
            ys[-1].append(ang[1])
            xs[-1].append(ang[2])
            y_value = ang[1]
            x_value = ang[2]
            unique_points.add((x_value, y_value))

            

    # Check if the number of unique points is equal to the total number of points
    total_points = sum(len(ys[i]) for i in range(len(ys)))
    if len(unique_points) == total_points:
        print("All points are different.")
    else:
        print("There are duplicate points.")

    # print(len(ys))
    # Create a scatter plot
    cmap = plt.get_cmap('tab20')
    i_val=[]
    for i,y in enumerate(ys):
        if i%2:
            plt.scatter(xs[i], y, marker='o',s=10,label=f"ID={indeksy_wystapien[i]}")
            i_val.append(-(i//2))
        else:
            plt.scatter(xs[i], y, marker='o',s=10,label=f"ID={indeksy_wystapien[i]}")
            i_val.append((i//2+1))
    # print(sorted(i_val))
    FONTSIZE = 28
    # Adding titles and labels
    #plt.title(f"Patterns occurrences for generating pattern for TX at {tx_pos}° and RX at {rx_pos}°", fontsize=FONTSIZE)
    plt.xlabel('φ_s [°]', fontsize=FONTSIZE)
    plt.ylabel('Rx target localization [°]', fontsize=FONTSIZE)
    # Setting the limits for the axes
    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.legend(title='Pattern codebook ID', title_fontsize=FONTSIZE-4, loc='upper left', bbox_to_anchor=(1, 1), fontsize=FONTSIZE-8, markerscale=5., ncol=2)
    plt.xlim(0, 359)  # X-axis from 0 to 359
    plt.ylim(0, 90)   # Y-axis from 0 to 90
    # Show the plot
    plt.grid(True)
    plt.show()

""" AF """
# af_lin = 10*np.log10(AF(-48,40,quant=False))
# af_1 = 10*np.log10(AF(-48,40,quant=True))
# # af_2 = 10*np.log10(AF(-48,40,quant=True,phase_shift=45))
# plt.figure(figsize=(10, 6))
# x = range(-90,90)
# plt.plot(x, af_lin, linestyle="--", label="Linear")
# plt.plot(x, af_1, label="Binary")
# # plt.plot(x, af_2, label="Binary rotated")
# plt.legend()
# plt.xticks(np.arange(-90, 91, 10))
# plt.yticks(np.arange(-10, 50, 5))
# plt.xlim(-90, 90)
# plt.ylim(-10, 25)
# plt.xlabel("Rx location [°]")
# plt.ylabel("AF [dB]")
# plt.grid()
# plt.show()

"""Patterns occurances in codebook plotting"""
phase_shift_step_list = range(1,90)#[1,2,4,10,20,30,45,90,180]
theta_d_step_list = range(1,90)
pattern_amount = []
pattern_amount_phi = []
pattern_amount_theta=[]
unique_pattern_amount = []
phi_s_stepping = []
theta_d_stepping = []

for theta_d_step in theta_d_step_list:
    phase_shift_step = 1
    print(theta_d_step, phase_shift_step)
    pat_no = codebook_generate(phase_shift_step=phase_shift_step, theta_d_step=theta_d_step)
    unique_pattern_amount.append(pat_no)
    theta_d_stepping.append(pat_no)
    pattern_amount.append(90//theta_d_step * 360//phase_shift_step)
    pattern_amount_theta.append(90//theta_d_step * 360//phase_shift_step)

for phase_shift_step in phase_shift_step_list:
    theta_d_step = 1
    print(theta_d_step, phase_shift_step)
    pat_no = codebook_generate(phase_shift_step=phase_shift_step, theta_d_step=theta_d_step)
    phi_s_stepping.append(pat_no)
    unique_pattern_amount.append(pat_no)
    pattern_amount.append(90//theta_d_step * 360//phase_shift_step)
    pattern_amount_phi.append(90//theta_d_step * 360//phase_shift_step)

plot_no_unique_patterns([phi_s_stepping, theta_d_stepping], [phase_shift_step_list, theta_d_step_list], ['φ_s', "θ_d"])
print("DONE")