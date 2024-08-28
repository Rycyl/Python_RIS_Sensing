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
    with open("RIS_patterns.json") as json_patterns:
        patterns_obj = json.load(json_patterns)
        patterns_data = patterns_obj["PATTERNS"]
except FileNotFoundError:
    print("File with patterns doesn't exist.")
    exit()

def get_trace():
    global POWER_REC
    POWER_REC = analyzer_sensing.trace_get()
    return



def find_best_pattern_codebook(RIS, config, mesure_file = 'find_best_pattern_codebook.csv'):
    generator.meas_prep(True, config.generator_mode, config.generator_amplitude, config.freq)
    analyzer_sensing.meas_prep(config.freq, config.sweptime, config.span, config.analyzer_mode, config.detector, config.revlevel, config.rbw, config.swepnt)
    file = open(mesure_file, 'a+')
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
    return best_pattern["HEX"], worst_pattern["HEX"]



def find_best_pattern_element_wise(RIS, config, mask = '0b1', mesure_file = 'find_best_pattern_element_wise.csv', find_min=False):
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
            pp = analyzer_sensing.trace_get()
            p = np.mean(pp)
            #t2 = time.time()
            #timings.append(t2-t1)
            power_pattern.append([[p],[current_pattern.hex]])
            print("pattern:: ", "0x",current_pattern.hex, " = ", p)
            
            with open(mesure_file, 'a+') as file:
                file.write(str(p) + ",")
                file.write("0x" + current_pattern.hex)
                file.write('\n')
                file.close()  # CLose the file
            
            if(find_min):
                if (p<pow_max): ### < min find
                    pow_max=p
                    previous_pattern = copy(current_pattern)
                else:
                    current_pattern = copy(previous_pattern)
            else:
                if (p>pow_max): ### >maks find
                    pow_max=p
                    previous_pattern = copy(current_pattern)
                else:
                    current_pattern = copy(previous_pattern)
            x += mask_x_size #iterate
            j += 1
            if (j > x_iters):
                break
            continue # NEXT X
       # file.write("wiersz RISa: " + str(y) + "," + str(current_pattern.hex) + ',' + str(pow_max) + '\n')    
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

    return best_pattern, best_pow



def find_best_pattern_element_wise_by_group_measures(RIS, config, n_elements = 4, mesure_file = 'find_best_pattern_element_wise_by_group_measures_v2.csv', find_min = False, debug = False, trace_file = 'trace_file_group_mesures.csv'):
    """   adnotacje:
    1) DODAĆ OPCJONALNE ZAPISYWANIE MIEDZYPOMIAROW DO PLIKU
    2) N=nie wincyj jak 4 elementy bo sie zapycha cpu
    """
    ### INIT MEASURE POINTS AND ANAL AND GEN
    if (find_min):
        current_best_pow = 1000.0
    else:
        current_best_pow = -1000.0
    combinations = (2 ** n_elements)

    RIS_change_time = 0.022
    Total_ris_changing_time = combinations * RIS_change_time
    
    config.update_swt(Total_ris_changing_time * 3) ## 1/3 danych jest niewiadomej reputacji teraz
    points = config.swepnt
    point_range = int( points // combinations )
    print("POINST TOTAL = ", points, "Point Range = ", point_range)

    delta_t = config.sweptime/points
    N_pts_delete = int((RIS_change_time / delta_t) //2)
    
    generator.meas_prep(True, config.generator_mode, config.generator_amplitude, config.freq)
    analyzer_sensing.meas_prep(config.freq, config.sweptime, config.span, config.analyzer_mode, config.detector, config.revlevel, config.rbw, config.swepnt) 
    file = open(mesure_file, 'a+')
    file.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "N_elements ," + str(n_elements) + ", swt = ," + str(config.sweptime))
    file.write('\n')


    ## PREPARE PATTERNS TO SWAP
    pat_array = []
    for x in range(0, combinations):
        pat_array.append(BitArray(uint=x, length=256))
    pat_array_copy = copy(pat_array)
    
    n = 0
    write_patterns = []
    write_powers = []
    write_std = []

    ###Set 0 on RIS as current best
    current_best_pattern = BitArray(length=256)
    RIS.set_pattern('0x' + current_best_pattern.hex)

    while(n<256):
        MEASURE = threading.Thread(target=get_trace) #create thread MEASUREs
        RIS.set_pattern('0x' + pat_array_copy[0].hex)
        ### PERFORM MEASURE
        MEASURE.start()
        sleep(0.05)
            ###przełącz RIS z pat_array
        for y in pat_array_copy[1:]:
            sleep(config.sweptime/combinations)
            RIS.set_pattern('0x' + y.hex)
            ###
        MEASURE.join()
        ### MEASURE END
        #t1 = time.time()
        
        powers = []
        if(debug):
            trace_f = open(trace_file, 'a+')
            trace_f.write('"Grupowy pomiar N_el' + str(n_elements) + ' 1szy opt elem w sekwencji=' + str(n) + '"')
            trace_f.write("\n")

        if(debug):
            trace_f.write(str(POWER_REC)[1:-1])
            trace_f.write("\n")

        power_slice = []
        ###wybierz najlepszy pattern z trace_rec
        for i in range (0, combinations):
            start_pat = point_range*i + N_pts_delete
            end_pat = point_range*(i+1) - N_pts_delete
            power_slice = POWER_REC[start_pat:end_pat]
            std = np.std(power_slice)
            powers.append(np.mean(power_slice))

            if(debug):
                for ij in range(0, N_pts_delete):
                    trace_f.write( '-150,')
                trace_f.write(str(power_slice)[1:-1])
                trace_f.write(",")
                for ij in range(0, N_pts_delete):
                    trace_f.write( '-150,')

            write_patterns.append(pat_array_copy[i])
            write_powers.append(powers[-1])
            write_std.append(std)

        
            if (find_min):
                    current_best_pow = np.min(powers)
            else:
                    current_best_pow = np.max(powers)

        if(debug):
                trace_f.write("\n")
                for abc in pat_array_copy:
                    for ij in range(0, N_pts_delete):
                        trace_f.write('"NONE_PAT",')
                    for xx in range(0, len(power_slice)):
                        trace_f.write('"' + str(abc.hex) + '"' + ',')
                    for ij in range(0, N_pts_delete):
                        trace_f.write('"NONE_PAT",')
                trace_f.write("\n")
                trace_f.close()

        for i in range (0, combinations):
            if(current_best_pow == powers[i]):
                current_best_pattern = copy(pat_array_copy[i])
        print("PAT: ", current_best_pattern.hex, "POW MAX: ", current_best_pow) ##debug

        ###przesuń wzory w pat_array o n_elements, następnie wzory OR current best
        for i in range(0,combinations):
            pat_array[i].rol(n_elements)
            pat_array_copy[i] = pat_array[i] | current_best_pattern
        ###
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
    return current_best_pattern.hex, current_best_pow
