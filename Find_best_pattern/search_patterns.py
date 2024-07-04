import analyzer_sensing
import generator
import RIS_usb
import json
import numpy as np
from RsSmw import *
import time
import def_pattern
from bitstring import Bits, BitArray, BitStream, pack

try:
    with open ("config_sensing.json") as config_f:
        config = json.load(config_f)
        trace_file = config["TRACE_FILE"]
        freq = config['CENTRAL_FREQ']
        span=config["SPAN"]
        analyzer_mode=config["ANALYZER_MODE"]
        revlevel=config["REVLEVEL"]
        rbw=config["RBW"]
        swepnt = config["SWEEP_POINTS"]
        generator_amplitude=config["GENERATOR_AMPLITUDE"]
        detector = config["DETECTOR"]
        sweptime = config["SWEEP_TIME"]
        # More modes will be add later.
        if config["GENERATOR_MODE"] == "CW":
            generator_mode = enums.FreqMode.CW
        else: 
            generator_mode = enums.FreqMode.CW
        config_f.close()
except FileNotFoundError:
    print("File with configuration doesn't exist.")
    exit()

try:
    with open("RIS_patterns.json") as json_patterns:
        patterns_obj = json.load(json_patterns)
        patterns_data = patterns_obj["PATTERNS"]
except FileNotFoundError:
    print("File with patterns doesn't exist.")
    exit()
    

def find_best_pattern_codebook(bsweptime = sweptime, banalyzer_mode = analyzer_mode, bdetector = detector, bswepnt = swepnt, bgenerator_amplitude = generator_amplitude):
    generator.meas_prep(True, generator_mode, bgenerator_amplitude, freq)
    # power = {}
    power = []
    analyzer_sensing.meas_prep(freq, bsweptime, span, banalyzer_mode, bdetector, revlevel, rbw, bswepnt)
    for pattern in patterns_data:
        RIS_usb.set_pattern(pattern["HEX"])
        p = analyzer_sensing.trace_get()
        
        power.append(p)
    for i in range(0, len(power)):
        print("pattern id:: ", i, " = ",power[i])
    best_index = power.index(max(power))
    worst_index = power.index(min(power))
    best_pattern = patterns_data[best_index]
    worst_pattern = patterns_data[worst_index]
    print(best_pattern["DESC"], max(power))
    print(worst_pattern["DESC"], min(power))
    return best_pattern #, worst_pattern





def find_best_pattern_element_wise(mask = '0b1', bsweptime = sweptime, banalyzer_mode = analyzer_mode, bdetector = detector, bswepnt = swepnt, bgenerator_amplitude = generator_amplitude):
    ### MASKA MUSI BYĆ BINARNA!!! ###
    ### MASKI O DŁUGOSCI X != dzielnik 16 nie działają poprawnie ###
    ### MASKI O DLUGOSI Y!= 1 nie działają poprawnie ### (prawdopodobnie rozwiazanie to XOR z poprzednim patternem przed zerowaniem)
    ### todo change to make modes work - for now all are type 1#### !!!!!!!!!!!!!!!!
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
    print("mask_y_size:: ", mask_y_size)
    print("mask_x_size:: ", mask_x_size)

    inverted_maska = '0b'
    for i in range(2, mask_len+2):
                        inverted_maska += '0'
    print("light off mask:: ", inverted_maska)

    with open(trace_file, 'a+') as file:
                file.write("ELEMENT WISE MASK = " + mask + '\n')
    ### MEASURE PREPARE ###
    generator.meas_prep(True, generator_mode, bgenerator_amplitude, freq)
    # power = {}
    power_pattern = []
    analyzer_sensing.meas_prep(freq, bsweptime, span, banalyzer_mode, bdetector, revlevel, rbw, bswepnt)
    ###BitArray to hold patterns
    current_pattern = BitArray(length=256)
    RIS_usb.set_pattern('0x'+current_pattern.hex)
    pow_max = analyzer_sensing.trace_get()
    print("current amp:: ", pow_max)
    ### func definition ###
    
    y = 0
    while(y<16):
        x = 0
        while(x<16):
            current_element = 16*y + x
            current_pattern.overwrite(mask, current_element)
            RIS_usb.set_pattern('0x'+current_pattern.hex)
            p = analyzer_sensing.trace_get()
            power_pattern.append([[p],[current_pattern.hex]])
            print("pattern:: ", "0x",current_pattern.hex, " = ", p)
            with open(trace_file, 'a+') as file:
                file.write("pomiar " + str(i) + ",")
                file.write(str(time.ctime(time.time())) + ",") 
                file.write("Rec_PWR,")
                file.write(str(p) + ",")
                file.write("Pattern,")
                file.write("0x" + current_pattern.hex)
                file.write('\n')
                file.close()  # CLose the file
            if (p>pow_max):
                pow_max=p
            else:
                current_pattern.overwrite(inverted_maska, current_element)
            x += mask_x_size #iterate
            continue

        y += mask_y_size #iterate
        continue

    print("max power:: ", pow_max)

    best_pow = -220.0
    best_pattern = None
    for p, pattern in power_pattern:
        if p[0] > best_pow:
            best_pattern = pattern[0]
            best_pow = p[0]

    return best_pattern, best_pow