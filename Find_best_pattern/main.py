import analyzer_sensing
import generator
import RIS_usb
import json
import numpy as np
from RsSmw import *
import time
import def_pattern
from bitstring import Bits, BitArray, BitStream, pack
import search_patterns

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
    
if __name__ == "__main__":
    ##time.sleep(20)
    RIS_usb.reset_RIS()
    generator.com_check()
    analyzer_sensing.com_prep()
    analyzer_sensing.com_check()
    #generator.meas_prep(True, generator_mode, -140.0, freq)
    i = 0
    brekpoint = 1
    while(i<brekpoint):
        i+=1
        print("Iteration: ", i)
        print(search_patterns.find_best_pattern_element_wise(mask='0b11111'))


    analyzer_sensing.meas_close()
    generator.meas_close()