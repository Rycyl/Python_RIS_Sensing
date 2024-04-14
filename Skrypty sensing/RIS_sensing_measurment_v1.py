import analyzer
import generator
import RIS_usb
import json
import numpy as np
from RsSmw import *
import time
from bitarray import bitarray
import binascii
import def_pattern
try:
    with open ("config.json") as config_f:
        config = json.load(config_f)
        trace_file = config["TRACE_FILE"]
        start_freq=config["START_FREQ"]
        end_freq=config["END_FREQ"]
        step_freq=config["STEP_FREQ"]
        motor_step=config["MOTOR_STEPS"]
        step_resolution = config["STEP_RESOLUTION"]
        number_of_angles = config["NUMBER_OF_ANGLES"]
        span=config["SPAN"]
        analyzer_mode=config["ANALYZER_MODE"]
        revlevel=config["REVLEVEL"]
        rbw=config["RBW"]
        generator_amplitude=config["GENERATOR_AMPLITUDE"]
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

def prepare_freq() -> list:
    if start_freq != end_freq:   
        freq_data = np.arange(start_freq, end_freq+step_freq, step_freq)
    else:
        freq_data = [start_freq]
    return freq_data

def pattern_loop(freq):
    for pattern in patterns_data:
        analyzer.meas_prep(freq, span, analyzer_mode, revlevel, rbw)
        RIS_usb.set_pattern(pattern["HEX"])
        with open(trace_file, 'a+') as file:
            file.write(pattern["ID"]+";"+pattern["DESC"]+";")  # Write information about pattern information
            file.close()  # CLose the file
        time.sleep(0.1)
        # RIS_usb.read_pattern() #Inofrmation about pattern set on RIS.
        analyzer.trace_get()

def pattern_iterative_state_optimization(freq):
    analyzer.meas_prep(freq, span, analyzer_mode, revlevel, rbw)
    current_pattern = bitarray(256)
    current_pattern.setall(0)
    current_pattern = current_pattern.tolist()
    RIS_usb.set_pattern(def_pattern.pattern_bin_to_hex(current_pattern)
    time.sleep(0.1)
    # RIS_usb.read_pattern() #Inofrmation about pattern set on RIS.
    current_apm = analyzer.trace_get_return()
    for i in range(len(current_pattern)):
        current_pattern[i]=1
        new_amp = analyzer.trace_get_return()
        #print("I", i, "    N: ",new_amp, "    C: ", current_amp)
        if (new_amp < current_amp):
            current_pattern[i]=0
        else:
            current_amp = new_amp
        print(def_pattern.pattern_bin_to_hex(current_pattern))
        time.sleep(0.1)
    return current_pattern

def freq_loop(freq_data):
     for freq in freq_data:
        generator.meas_prep(True, generator_mode, generator_amplitude, freq) # True means that generator is set up an generate something.
        pattern_loop(freq)

if __name__=="__main__":
    try:
        analyzer.com_prep()
        analyzer.com_check()
        generator.com_check()
        RIS_usb.reset_RIS()
        freq_data = prepare_freq()
        freq_loop(freq_data)
        analyzer.meas_close()
        generator.meas_close()
        exit()
    except KeyboardInterrupt:
        print("[KEY]Keyboard interrupt.")
        exit()
