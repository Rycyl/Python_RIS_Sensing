import analyzer
import generator
import RIS_usb
import remote_head
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
        start_step=config["START_STEP"]
        end_step=config["END_STEP"]
        motor_step=config["MOTOR_STEP"]
        step_resolution = config["STEP_RESOLUTION"]
        step_data = np.arange(start_step, end_step, motor_step)
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
    
def count_angle(step):
    angle = step*1/(step_resolution)
    return angle
    
def pattern_loop(freq):
    for pattern in patterns_data:
        analyzer.meas_prep(freq, span, analyzer_mode, revlevel, rbw)
        RIS_usb.set_pattern(pattern["HEX"])
        with open(trace_file, 'a+') as file:
            file.write(pattern["ID"]+";")  # Write information about pattern information
            file.close()  # Close the file
        time.sleep(0.1)
        # RIS_usb.read_pattern() #Inofrmation about pattern set on RIS.
        analyzer.trace_get()

def freq_loop(freq_data):
     for freq in freq_data:
        generator.meas_prep(True, generator_mode, generator_amplitude, freq) # True means that generator is set up an generate something.
        pattern_loop(freq)
        
def angle_loop(step_data):
    for step in step_data:
        with open(trace_file, 'a+') as file:
            file.write(count_angle(step) + ";")  # Write information about angle
            file.close()  # Close the file
        time.sleep(0.1)
        remote_head.obrot_prawo(step) # move few steps to the right (descroption in config file)
        freq_loop(freq_data)

    
if __name__=="__main__":
    try:
        analyzer.com_prep()
        analyzer.com_check()
        generator.com_check()
        remote_head.az360()
        RIS_usb.reset_RIS()
        freq_data = np.arange(start_freq, end_freq, step_freq)
        step_data = np.arange(start_step, end_step, motor_step)
        angle_loop(step_data)
        analyzer.meas_close()
        generator.meas_close()
        exit()
    except KeyboardInterrupt:
        print("[KEY]Keyboard interrupt.")
        exit()
