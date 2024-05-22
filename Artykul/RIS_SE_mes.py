import analyzer_sensing
import generator
import RIS_usb
import json
import numpy as np
from RsSmw import *
import time

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
    
def find_best_pattern(bsweptime = sweptime, banalyzer_mode = analyzer_mode, bdetector = detector, bswepnt = swepnt, bgenerator_amplitude = generator_amplitude):
    generator.meas_prep(True, generator_mode, bgenerator_amplitude, freq)
    power = {}
    analyzer_sensing.meas_prep(freq, bsweptime, span, banalyzer_mode, bdetector, revlevel, rbw, bswepnt)
    for pattern in patterns_data:
        RIS_usb.set_pattern(pattern["HEX"])
        p = analyzer_sensing.trace_get()
        power[pattern["ID"]] = p
    s_power = dict(sorted(power.items(), key=lambda item: item[1], reverse=True))
    #print(s_power)
    #best_pattern = dict(list(s_power.items())[0:1])
    B_n_W_pattern = dict(list(s_power.items())[::len(s_power)-1])
    keys_iter = iter(B_n_W_pattern)
    best_id = int(next(keys_iter))
    worst_id = int(next(keys_iter))
    best_pattern = patterns_data[best_id-1]
    worst_pattern = patterns_data[worst_id-1]
    return best_pattern, worst_pattern

def time_mesurment(best_pattern, worst_pattern):
    with open(trace_file, 'a+') as file:
        file.write("noise") 
        file.write(',')
        file.close()  # CLose the file
    analyzer_sensing.meas_prep(freq, sweptime, span, analyzer_mode, detector, revlevel, rbw, swepnt) #tu można wsadzić funkcję która zrobi poziom szumu zamiast poprostu szum ale no
    analyzer_sensing.trace_get_vect_fx()
    RIS_usb.set_pattern(worst_pattern["HEX"])
    with open(trace_file, 'a+') as file:
        file.write(worst_pattern["DESC"]) 
        file.write(',')
        file.close()  # CLose the file
    analyzer_sensing.meas_prep(freq, sweptime, span, analyzer_mode, detector, revlevel, rbw, swepnt)
    generator.meas_prep(True, generator_mode, generator_amplitude, freq)
    time.sleep(0.1)
    analyzer_sensing.trace_get_vect_fx()
    RIS_usb.set_pattern(best_pattern["HEX"])
    with open(trace_file, 'a+') as file:
        file.write(best_pattern["DESC"]) 
        file.write(',')
        file.close()  # CLose the file
    analyzer_sensing.meas_prep(freq, sweptime, span, analyzer_mode, detector, revlevel, rbw, swepnt)
    analyzer_sensing.trace_get_vect_fx()
    
    
if __name__ == "__main__":
    #time.sleep(20)
    RIS_usb.reset_RIS()
    generator.com_check()
    analyzer_sensing.com_prep()
    analyzer_sensing.com_check()
    best_pattern, worst_pattern = find_best_pattern(bsweptime = 50E-3, banalyzer_mode= "WRITe", bdetector= "SAMP", bgenerator_amplitude= -10 )
    #print(best_pattern, worst_pattern)
    generator.meas_prep(True, generator_mode, -135.0, freq)
    time_mesurment(best_pattern, worst_pattern)
    analyzer_sensing.meas_close()
    generator.meas_close()