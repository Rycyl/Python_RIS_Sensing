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

def get_trace(ANALYZER):
    global POWER_REC
    POWER_REC = ANALYZER.trace_get()
    return

def measure_thread_with_RIS_changes(ANALYZER, RIS, PAT_ARRAY, SLEEPTIME):
        MEASURE = threading.Thread(target=get_trace, args=(ANALYZER,)) #create thread MEASUREs
        RIS.set_pattern('0x' + PAT_ARRAY[0].hex)
        ### PERFORM MEASURE
        MEASURE.start()
        sleep(0.06)
        sleep(0.022) ## wait for ris margin
            ###przełącz RIS z pat_array
        for y in PAT_ARRAY[1:]:
            sleep(SLEEPTIME)
            RIS.set_pattern('0x' + y.hex)
            ###
        MEASURE.join()
        ### MEASURE END

def find_best_pattern_codebook(RIS, GENERATOR, ANALYZER, CONFIG, MEASURE_FILE = 'find_best_pattern_codebook.csv'):
    GENERATOR.meas_prep(True, CONFIG.generator_mode, CONFIG.generator_amplitude, CONFIG.freq)
    ANALYZER.meas_prep(CONFIG.freq, CONFIG.sweptime, CONFIG.span, CONFIG.analyzer_mode, CONFIG.detector, CONFIG.revlevel, CONFIG.rbw, CONFIG.swepnt)
    file = open(MEASURE_FILE, 'a+')
    file.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    file.write('\n')
    power = []
    for pattern in patterns_data:
        RIS.set_pattern(pattern["HEX"])
        p = ANALYZER.trace_get_mean()
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

def find_best_pattern_element_wise(RIS, GENERATOR, ANALYZER, CONFIG, MASK = '0b1', MEASURE_FILE = 'find_best_pattern_element_wise.csv', FIND_MIN=False):
    ### MASKA MUSI BYĆ BINARNA!!! ###
    '''
        maska - jakim mini patternem przesuwamy sie po RIS
    '''
    ### Obliczenia dlugosci maski ###
    mask_len = len(MASK) - 2
    mask_y_size = 1 #default shortest MASK
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
    GENERATOR.meas_prep(True, CONFIG.generator_mode, CONFIG.generator_amplitude, CONFIG.freq)
    ANALYZER.meas_prep(CONFIG.freq, CONFIG.sweptime, CONFIG.span, CONFIG.analyzer_mode, CONFIG.detector, CONFIG.revlevel, CONFIG.rbw, CONFIG.swepnt)
    power_pattern = [] ###lista do zbierania wyników

    current_pattern = BitArray(length=256)  ## all zeros
    previous_pattern = BitArray(length=256) ## all zeros

    RIS.set_pattern('0x'+current_pattern.hex)
    pow_max = ANALYZER.trace_get_mean()
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
            current_pattern.overwrite(MASK, current_element)
            current_pattern |= previous_pattern
            #t1 = time.time()
            RIS.set_pattern('0x'+current_pattern.hex)
            pp = ANALYZER.trace_get()
            p = np.mean(pp)
            #t2 = time.time()
            #timings.append(t2-t1)
            power_pattern.append([[p],[current_pattern.hex]])
            print("pattern:: ", "0x",current_pattern.hex, " = ", p)
            
            with open(MEASURE_FILE, 'a+') as file:
                file.write(str(p) + ",")
                file.write("0x" + current_pattern.hex)
                file.write('\n')
                file.close()  # CLose the file
            
            if(FIND_MIN):
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

def prepare_measurement_files(MEASURE_FILE, TIME_FILE, CONFIG, N_ELEMENTS):
    file = open(MEASURE_FILE, 'a+')
    file.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "N_elements ," + str(N_ELEMENTS) + ", swt = ," + str(CONFIG.sweptime))
    file.write('\n')
    
    if TIME_FILE:
        t0 = []
        t1 = []
        return file, t0, t1
    return file, None, None

def prepare_patterns(N_ELEMENTS):
    combinations = 2 ** N_ELEMENTS
    pat_array = [BitArray(uint=x, length=256) for x in range(combinations)]
    return pat_array, copy(pat_array)

def update_config_sweep_time(CONFIG, combinations, TIME_SAFETY_MARGIN, RIS_change_time):
    Total_ris_changing_time = combinations * RIS_change_time
    CONFIG.update_swt(Total_ris_changing_time * TIME_SAFETY_MARGIN + 2 * RIS_change_time)
    return CONFIG

def calculate_shift(mean, power_slice, std, std_check, point_range, shift, PAT_ARRAY, ANALYZER, RIS, sleeptime, DEBUG_FLAG):
    minpow = min(power_slice)
    maxpow = max(power_slice)
    max_out = (maxpow > mean + 2 * std)
    min_out = (minpow < mean - 2 * std)

    if min_out and max_out:
        measure_thread_with_RIS_changes(ANALYZER=ANALYZER, RIS=RIS, PAT_ARRAY=PAT_ARRAY, SLEEPTIME=sleeptime)
        shift = 0
    elif max_out:
        if power_slice.index(maxpow) > point_range // 2:
            shift -= int(point_range * 0.1)
        else:
            shift += int(point_range * 0.1)
    elif min_out:
        if power_slice.index(minpow) > point_range // 2:
            shift -= int(point_range * 0.1)
        else:
            shift += int(point_range * 0.1)
    
    return shift

def write_debug_info(DEBUG_FLAG, TRACE_FILE, N_ELEMENTS, CONFIG, POWER_REC, power_debug, pattern_debug, n):
    if DEBUG_FLAG:
        with open(TRACE_FILE, 'a+') as trace_f:
            trace_f.write(f'"Grupowy pomiar N_el{N_ELEMENTS} 1szy opt elem w sekwencji={n}||SWT = {CONFIG.sweptime}||"\n')
            trace_f.write(f'{str(POWER_REC)[1:-1]}\n')
            trace_f.write(f'{str(power_debug)[1:-1]}\n')
            for napis in pattern_debug:
                trace_f.write(f'"{str(napis)}",')
            trace_f.write('\n')

def measure_patterns(ANALYZER, RIS, PAT_ARRAY, sweeptime, sleeptime, point_range, N_pts_delete, shift, POWER_REC, STD_TRS, STD_CHECK_ON, DEBUG_FLAG, best_power, FIND_MIN):
    power_debug = [-150] * len(POWER_REC) if DEBUG_FLAG else None
    pattern_debug = [None] * len(POWER_REC) if DEBUG_FLAG else None
    powers = []
    for i in range(len(PAT_ARRAY)):
        enum = 0
        while True:
            enum += 1
            start_pat = max(0, int(point_range * i + N_pts_delete + shift))
            end_pat = min(len(POWER_REC), int(point_range * (i + 1) - N_pts_delete + shift))
            power_slice = POWER_REC[start_pat:end_pat]
            std = np.std(power_slice)
            mean = np.mean(power_slice)

            if DEBUG_FLAG:
                print(f"STD:: {std}, enum:: {enum}, len_power_slice:: {len(power_slice)}")          

            if std > STD_TRS and STD_CHECK_ON and enum < 10:
                shift = calculate_shift(mean, power_slice, std, STD_CHECK_ON, point_range, shift, PAT_ARRAY, ANALYZER, RIS, sleeptime, DEBUG_FLAG)
                continue

            powers.append(mean)

            if DEBUG_FLAG:
                for xx in range(start_pat, end_pat):
                    power_debug[xx] = POWER_REC[xx]
                    pattern_debug[xx] = str(PAT_ARRAY[i].hex)

            break

    best_power = np.min(powers) if FIND_MIN else np.max(powers)
    best_idx = powers.index(best_power)
    
    return best_idx, best_power, power_debug, pattern_debug, powers

def find_best_pattern_element_wise_by_group_measures(RIS, GENERATOR, ANALYZER, CONFIG, N_ELEMENTS = 4, N_SIGMA = 3, TIME_SAFETY_MARGIN = 3.0, STD_TRS = 0.08, STD_CHECK_ON = True, DEBUG_FLAG = False, MEASURE_FILE = 'find_best_pattern_element_wise_by_group_measures_v2.csv', FIND_MIN = False, TRACE_FILE = 'trace_file_group_mesures.csv', TIME_FILE = None):
    RIS_change_time = 0.022
    pat_array, pat_array_copy = prepare_patterns(N_ELEMENTS)
    current_best_power = 1000.0 if FIND_MIN else -1000.0
    CONFIG = update_config_sweep_time(CONFIG, len(pat_array), TIME_SAFETY_MARGIN, RIS_change_time)

    GENERATOR.meas_prep(True, CONFIG.generator_mode, CONFIG.generator_amplitude, CONFIG.freq)
    ANALYZER.meas_prep(CONFIG.freq, CONFIG.sweptime, CONFIG.span, CONFIG.analyzer_mode, CONFIG.detector, CONFIG.revlevel, CONFIG.rbw, CONFIG.swepnt)

    file, t0, t1 = prepare_measurement_files(MEASURE_FILE, TIME_FILE, CONFIG, N_ELEMENTS)
    
    n = 0
    power_write = []
    pattern_write = []
    while n < 256:
        if TIME_FILE:
            t1.append(time.time())
        measure_thread_with_RIS_changes(ANALYZER=ANALYZER, RIS=RIS, PAT_ARRAY=pat_array_copy, SLEEPTIME=(CONFIG.sweptime / len(pat_array)) - RIS_change_time)
        if TIME_FILE:
            t0.append(time.time())

        point_range = CONFIG.swepnt // len(pat_array)
        N_pts_delete = int(10) * N_SIGMA
        best_idx, current_best_power, power_debug, pattern_debug, powers = measure_patterns(ANALYZER, RIS, pat_array_copy, CONFIG.sweptime, CONFIG.sweptime / len(pat_array) - RIS_change_time, point_range, N_pts_delete, 0, POWER_REC, STD_TRS, STD_CHECK_ON, DEBUG_FLAG, current_best_power, FIND_MIN)

        current_best_pattern = pat_array_copy[best_idx]

        
        power_write.extend(powers)
        
        for pat in pat_array_copy:
            pattern_write.append(pat.hex)

        if DEBUG_FLAG:
            print(f"Pat:: {current_best_pattern}, Pow:: {current_best_power}")

        if (DEBUG_FLAG):
            write_debug_info(DEBUG_FLAG, TRACE_FILE, N_ELEMENTS, CONFIG, POWER_REC, power_debug, pattern_debug, n)

        for i in range(len(pat_array)):
            pat_array[i].rol(N_ELEMENTS)
            pat_array_copy[i] = pat_array[i] | current_best_pattern

        n += N_ELEMENTS

    file.write(f"{str(pattern_write)[1:-1]}\n{str(power_write)[1:-1]}\n\n")

    if TIME_FILE:
        timefile = open(f"{TIME_FILE}.csv", 'a+')
        timefile.write(str(t0)[1:-1])
        timefile.write('\n')
        timefile.write(str(t1)[1:-1])
        timefile.close()

    file.close()
    return current_best_pattern.hex, current_best_power