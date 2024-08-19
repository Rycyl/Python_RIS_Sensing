import analyzer_sensing
import generator
from RIS import RIS
import json
import numpy as np
from RsSmw import *
import time
from time import sleep
import def_pattern
from bitstring import Bits, BitArray, BitStream, pack
from copy import copy, deepcopy
import threading
from config_obj import Config
import file_writer
from copy import copy

try:
    global config
    config = Config()
except FileNotFoundError:
    print("Błąd z plikiem konfiguracyjnym - search_patterns.py")
    exit()

try:
    with open("RIS_patterns.json") as json_patterns:
        patterns_obj = json.load(json_patterns)
        patterns_data = patterns_obj["PATTERNS"]
except FileNotFoundError:
    print("File with patterns doesn't exist.")
    exit()
    

def find_best_pattern_codebook(RIS, config, trace_file = 'find_best_pattern_codebook.csv'):
    generator.meas_prep(True, config.generator_mode, config.generator_amplitude, config.freq)
    analyzer_sensing.meas_prep(config.freq, config.sweptime, config.span, config.analyzer_mode, config.detector, config.revlevel, config.rbw, config.swepnt)
    file = open(trace_file, 'a+')
    file.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    file.write('\n')
    power = []
    for pattern in patterns_data:
        RIS.set_pattern(pattern["HEX"])
        p = analyzer_sensing.trace_get_mean()
        file.write(str(pattern["HEX"]) + ',' + str(p) + '\n')
        power.append(p)
    #for i in range(0, len(power)):
        #print("pattern id:: ", i, " = ",power[i])
    best_index = power.index(max(power))
    worst_index = power.index(min(power))
    best_pattern = patterns_data[best_index]
    worst_pattern = patterns_data[worst_index]
    print(best_pattern["DESC"], max(power))
    print(worst_pattern["DESC"], min(power))
    return #best_pattern #, worst_pattern


def find_best_pattern_element_wise(RIS, config, mask = '0b1', trace_file = 'find_best_pattern_element_wise.csv'):
    ### MASKA MUSI BYĆ BINARNA!!! ###
    '''
        maska - jakim mini patternem przesuwamy sie po RIS
    '''
    ### Obliczenia dlugosci maski ###
    mask_len = len(mask) - 2
    mask_y_size = 1 #default shortest mask
    mask_x_size = mask_len % 16
    i = 1
    while(1):
        if ( mask_len // (16 * i) ):
            print("mask_len // (16 * i):: ", mask_len // (16 * i))
            mask_y_size += 1
        else:
            break
        i += 1
        continue
    #print("mask_y_size:: ", mask_y_size)
    #print("mask_x_size:: ", mask_x_size)
    x_iters = 16 // mask_x_size
    y_iters = 16 // mask_y_size
    

    ###FILE MESURE START HEADER###
    file = open(trace_file, 'a+')
    file.write("ELEMENT WISE MASK = " + mask + '\n')
    file.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    file.write('\n')

    ### MEASURE PREPARE ###
    generator.meas_prep(True, config.generator_mode, config.generator_amplitude, config.freq)
    analyzer_sensing.meas_prep(config.freq, config.sweptime, config.span, config.analyzer_mode, config.detector, config.revlevel, config.rbw, config.swepnt)
    power_pattern = [] ###lista do zbierania wyników

    current_pattern = BitArray(length=256)  ## all zeros
    previous_pattern = BitArray(length=256) ## all zeros

    RIS.set_pattern('0x'+current_pattern.hex)
    pow_max = analyzer_sensing.trace_get_mean()
    #print("current amp:: ", pow_max)
    ### func definition ###
    
    timings = []
    
    y = 0
    i = 1
    while(y<16):
        x = 0
        j = 1
        while(x<16):
            current_element = 16*y + x
            current_pattern.overwrite(mask, current_element)
            current_pattern |= previous_pattern
            #t1 = time.time()
            RIS.set_pattern('0x'+current_pattern.hex)
            p = analyzer_sensing.trace_get_mean()
            #t2 = time.time()
            #timings.append(t2-t1)
            power_pattern.append([[p],[current_pattern.hex]])
            #print("pattern:: ", "0x",current_pattern.hex, " = ", p)
            '''
            with open(trace_file, 'a+') as file:
                file.write("pomiar " + str(i) + ",")
                #file.write(str(time.ctime(time.time())) + ",") 
                file.write("Rec_PWR,")
                file.write(str(p) + ",")
                file.write("Pattern,")
                file.write("0x" + current_pattern.hex)
                file.write('\n')
                file.close()  # CLose the file
            '''
            if (p>pow_max):
                pow_max=p
                previous_pattern = copy(current_pattern)
            else:
                current_pattern = copy(previous_pattern)
            x += mask_x_size #iterate
            j += 1
            if (j > x_iters):
                break
            continue # NEXT X
        file.write("wiersz RISa: " + str(y) + "," + str(current_pattern.hex) + ',' + str(pow_max) + '\n')    
        y += mask_y_size #iterate
        i += 1
        if(i > y_iters):
            break
        continue # NEXT Y

    #print("max power:: ", pow_max)

    #print(timings)
    #print("ŚREDNI CZAS ODPOWIEDZI - set pattern:trace_get_mean = ", np.mean(timings))
    
    best_pow = -220.0
    best_pattern = None
    for p, pattern in power_pattern:
        if p[0] > best_pow:
            best_pattern = pattern[0]
            best_pow = p[0]

    return #best_pattern, best_pow

def get_trace():
    global POWER_REC
    POWER_REC = analyzer_sensing.trace_get()
    return

def find_best_pattern_element_wise_by_group_measures(RIS, config, n_elements = 4, trace_file = 'find_best_pattern_element_wise_by_group_measures.csv'):
    """   adnotacje:
    1) DODAĆ OPCJONALNE ZAPISYWANIE MIEDZYPOMIAROW DO PLIKU
    2) N=nie wincyj jak 4 elementy bo sie zapycha cpu
    """
    ### INIT MEASURE POINTS AND ANAL AND GEN
    current_best_pow = -300.0
    combinations = (2 ** n_elements)
    points = config.swepnt
    centr_of_pat_trace = int(((points/combinations)//2)) # kompensacja? teoretycznie jest sleep dodany na to ## - points*0.05)
    point_range = config.swepnt // combinations // 4 ## 3 to testowa wartosc, sprawdzic czy trafiamy w trace odpowiednio
    print("POINST TOTAL = ", points, "Point Range = ", point_range, "Centr = ", centr_of_pat_trace)
    
    generator.meas_prep(True, config.generator_mode, config.generator_amplitude, config.freq)
    analyzer_sensing.meas_prep(config.freq, config.sweptime, config.span, config.analyzer_mode, config.detector, config.revlevel, config.rbw, config.swepnt) 
    file = open(trace_file, 'a+')
    file.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "N_elements ," + str(n_elements) + ", swt = ," + str(config.sweptime))
    file.write('\n')

    ###Set 0 on RIS as current best
    current_best_pattern = BitArray(length=256)
    RIS.set_pattern('0x' + current_best_pattern.hex)

    ## PREPARE PATTERNS TO SWAP
    pat_array = []
    for x in range(0, combinations):
        pat_array.append(BitArray(uint=x, length=256))
    pat_array_copy = copy(pat_array)
    pat_array_copy.append(current_best_pattern)

    n = 0
    write_patterns = []
    write_powers = []
    write_std = []
    while(n<256):
        MEASURE = threading.Thread(target=get_trace)
        
        ### PERFORM MEASURE
        MEASURE.start()
        sleep(0.05)
            ###przełącz RIS z pat_array
        for y in pat_array_copy:
            sleep(config.sweptime/combinations)
            RIS.set_pattern('0x' + y.hex)
            ###
        MEASURE.join()
        ### MEASURE END
        #t1 = time.time()
        
        #file.write(str(pat_array)[1:-1] + '\n')
        #file.write(str(POWER_REC)[1:-1] + '\n')
        
        ###wybierz najlepszy pattern z trace_rec
        for i in range (0, combinations):
            new_centre = centr_of_pat_trace + (config.swepnt//combinations)*i
            power_slice = POWER_REC[new_centre-point_range:new_centre+point_range]
            power = np.mean(power_slice)
            write_patterns.append(pat_array_copy[i])
            write_powers.append(power)
            write_std.append(np.std(power_slice))
            #print(pat_array[i])
            #print(type(power), "POWER TYPE", type(current_best_pow))
            if(power > current_best_pow):
                current_best_pattern = copy(pat_array_copy[i])
                current_best_pow = copy(power)

        #print("PAT: ", current_best_pattern.hex, "POW MAX: ", current_best_pow)
        ###

        ###przesuń wzory w pat_array o n_elements, następnie wzory OR current best
        for i in range(0,combinations):
            pat_array[i].rol(n_elements)
            pat_array_copy[i] = pat_array[i] | current_best_pattern
        ###
        pat_array_copy[-1] = current_best_pattern
        #print("EST TIME: ", time.time() - t1)
        n += n_elements
    file.write("\n Wynnik optymalizacji MASOWEJ \n")
    new_write_patterns = []
    for x in write_patterns:
        new_write_patterns.append(x.hex)
    file.write(str(new_write_patterns)[1:-1] + '\n')
    file.write(str(write_powers)[1:-1] + '\n')
    file.write(str(write_std)[1:-1] + '\n')
    file.close()
    return current_best_pattern, current_best_pow
