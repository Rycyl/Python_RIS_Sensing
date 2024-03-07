import analyzer
import generator
import RIS_usb
import json
import numpy as np
from RsSmw import *
import time

try:
    with open ("config.json") as config_f:
        config = json.load(config_f)
        trace_file = config["TRACE_FILE"]
        start_freq=config["START_FREQ"]
        end_freq=config["END_FREQ"]
        step_freq=config["STEP_FREQ"]
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

def pattern_loop(freq):
    for pattern in patterns_data:
        analyzer.meas_prep(freq, span, analyzer_mode, revlevel, rbw)
        RIS_usb.set_pattern(pattern)
        with open(trace_file, 'a+') as file:
            file.write(pattern)  # Write adequate frequency information
            file.write(";")
            file.close()  # CLose the file
        time.sleep(0.1)
        RIS_usb.read_pattern()
        analyzer.trace_get()

def freq_loop(freq_data):
     for freq in freq_data:
        generator.meas_prep(True, generator_mode, generator_amplitude, freq) # True means that generator is set up an generate something.
        pattern_loop(freq)

if __name__=="__main__":
    analyzer.com_prep()
    analyzer.com_check()
    generator.com_check()
    RIS_usb.reset_RIS()
    freq_data = np.arange(start_freq, end_freq+step_freq, step_freq)
    freq_loop(freq_data)
    analyzer.meas_close()
    generator.meas_close()