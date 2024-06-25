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





def find_best_pattern_element_wise(mode = 1, bsweptime = sweptime, banalyzer_mode = analyzer_mode, bdetector = detector, bswepnt = swepnt, bgenerator_amplitude = generator_amplitude):
    ### todo change to make modes work - for now all are type 1#### !!!!!!!!!!!!!!!!
    '''
        mode: 1 - po jednym elemencie
        mode: 2 - pionowe pary
        mode: 3 - poziome pary
        mode: 4 - kwadraty
    '''
    with open(trace_file, 'a+') as file:
                file.write("ELEMENT WISE MODE" + mode + '\n')
    ### MEASURE PREPARE ###
    generator.meas_prep(True, generator_mode, bgenerator_amplitude, freq)
    # power = {}
    power_pattern = []
    analyzer_sensing.meas_prep(freq, bsweptime, span, banalyzer_mode, bdetector, revlevel, rbw, bswepnt)
    ###BitArray to hold patterns
    current_pattern = BitArray(length=256)
    RIS_usb.set_pattern('0x'+current_pattern.hex)
    pow_max = -200.0
    current_amp = analyzer_sensing.trace_get()
    print("current amp:: ", current_amp)
    ### func definition ###
    if (mode == 1):
        for i in range(0,257):
            if (i != 0):
                current_pattern.overwrite('0b1',i-1)
            p = analyzer_sensing.trace_get()
            if (p>=pow_max):
                pow_max=p
            power_pattern.append([[p],[current_pattern.hex]])
            print("pattern:: ", "0x",current_pattern.hex, " = ", power_pattern[i][1])
            with open(trace_file, 'a+') as file:
                file.write("pomiar " + str(i) + ",")
                file.write(str(time.ctime(time.time())) + ",") 
                file.write("Rec_PWR,")
                file.write(str(p) + ",")
                file.write("Pattern,")
                file.write("0x" + current_pattern.hex)
                file.write('\n')
                file.close()  # CLose the file
            
            if (i != 0):
                current_pattern.overwrite('0b0',i-1)
    elif(mode == 2):
        for i in range(0,257):
            if (i != 0):
                current_pattern.overwrite('0b1',i-1)
            p = analyzer_sensing.trace_get()
            if (p>=pow_max):
                pow_max=p
            power_pattern.append([[p],[current_pattern.hex]])
            print("pattern:: ", "0x",current_pattern.hex, " = ", power_pattern[i][1])
            with open(trace_file, 'a+') as file:
                file.write("pomiar " + str(i) + ",")
                file.write(str(time.ctime(time.time())) + ",") 
                file.write("Rec_PWR,")
                file.write(str(p) + ",")
                file.write("Pattern,")
                file.write("0x" + current_pattern.hex)
                file.write('\n')
                file.close()  # CLose the file
            
            if (i != 0):
                current_pattern.overwrite('0b0',i-1)
    elif(mode == 3):
        for i in range(0,257):
            if (i != 0):
                current_pattern.overwrite('0b1',i-1)
            p = analyzer_sensing.trace_get()
            if (p>=pow_max):
                pow_max=p
            power_pattern.append([[p],[current_pattern.hex]])
            print("pattern:: ", "0x",current_pattern.hex, " = ", power_pattern[i][1])
            with open(trace_file, 'a+') as file:
                file.write("pomiar " + str(i) + ",")
                file.write(str(time.ctime(time.time())) + ",") 
                file.write("Rec_PWR,")
                file.write(str(p) + ",")
                file.write("Pattern,")
                file.write("0x" + current_pattern.hex)
                file.write('\n')
                file.close()  # CLose the file
            
            if (i != 0):
                current_pattern.overwrite('0b0',i-1)
    elif(mode == 4):
        for i in range(0,257):
            if (i != 0):
                current_pattern.overwrite('0b1',i-1)
            p = analyzer_sensing.trace_get()
            if (p>=pow_max):
                pow_max=p
            power_pattern.append([[p],[current_pattern.hex]])
            print("pattern:: ", "0x",current_pattern.hex, " = ", power_pattern[i][1])
            with open(trace_file, 'a+') as file:
                file.write("pomiar " + str(i) + ",")
                file.write(str(time.ctime(time.time())) + ",") 
                file.write("Rec_PWR,")
                file.write(str(p) + ",")
                file.write("Pattern,")
                file.write("0x" + current_pattern.hex)
                file.write('\n')
                file.close()  # CLose the file
            
            if (i != 0):
                current_pattern.overwrite('0b0',i-1)


    best = -220.0
    best_pattern = 0
    for i in range(0,length(power_pattern)):
        if (power_pattern[i][0]>best):
            best_pattern = power_pattern[i][1]
            best = power_pattern[i][0]
    return best_pattern