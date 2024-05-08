import analyzer_sensing
import generator
import RIS_usb
import json
import numpy as np
from RsSmw import *
import time
import def_pattern
try:
    with open ("config_sensing.json") as config_f:
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
        analyzer_sensing.meas_prep(freq, span, analyzer_mode, revlevel, rbw)
        RIS_usb.set_pattern(pattern["HEX"])
        with open(trace_file, 'a+') as file:
            file.write(pattern["DESC"])  # Write information about pattern information
            file.write(";")
            file.close()  # CLose the file
        time.sleep(0.1)
        # RIS_usb.read_pattern() #Inofrmation about pattern set on RIS.
        analyzer_sensing.trace_get()
        #analyzer_sensing.trace_get_vect()

def clear_run (freq):
    pattern = patterns_data[0]
    for i in patterns_data:
        analyzer_sensing.meas_prep(freq, span, analyzer_mode, revlevel, rbw)
        RIS_usb.set_pattern(pattern["HEX"])
        with open(trace_file, 'a+') as file:
            file.write(pattern["DESC"])  # Write information about pattern information
            file.write(";")
            file.close()  # CLose the file
        time.sleep(0.1)
        # RIS_usb.read_pattern() #Inofrmation about pattern set on RIS.
        analyzer_sensing.trace_get()

def freq_loop(freq_data):
     for freq in freq_data:
        generator.meas_prep(True, generator_mode, generator_amplitude, freq) 
        # True means that generator is set up an generate something.
        pattern_loop(freq)
        #clear_run(freq)

if __name__=="__main__":
    try:
        analyzer_sensing.com_prep()
        analyzer_sensing.com_check()
        generator.com_check()
        RIS_usb.reset_RIS()
        time.sleep(20)
        freq_data = prepare_freq()
        freq_loop(freq_data)
        analyzer_sensing.meas_close()
        generator.meas_close()
        exit()
    except KeyboardInterrupt:
        print("[KEY]Keyboard interrupt.")
        exit()
