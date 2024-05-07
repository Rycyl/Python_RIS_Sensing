import analyzer_sensing
import generator
import json
import numpy as np
from RsSmw import *
import time

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


 
def prepare_freq() -> list:
    if start_freq != end_freq:   
        freq_data = np.arange(start_freq, end_freq+step_freq, step_freq)
    else:
        freq_data = [start_freq]
    return freq_data

def ref_run_max(freq, lenght):
    for i in range(lenght):
        analyzer_sensing.meas_prep(True, generator_mode, generator_amplitude, freq)
        time.sleep(0.1)
        amp = analyzer_sensing.trace_get_return
        with open(trace_file, 'a+') as file:
            file.write(str(i))
            file.write(";")
            file.write(str(amp))
            file.write("\n")
            file.close()    

def ref_run_mean(freq, lenght):
    for i in range(lenght):
        analyzer_sensing.meas_prep(True, generator_mode, generator_amplitude, freq)
        time.sleep(0.1)
        amp = analyzer_sensing.trace_get_return_mean
        with open(trace_file, 'a+') as file:
            file.write(str(i))
            file.write(";")
            file.write(str(amp))
            file.write("\n")
            file.close()    

def ref_run_vec(freq, lenght):
    for i in range(lenght):
        analyzer_sensing.meas_prep(True, generator_mode, generator_amplitude, freq)
        time.sleep(0.1)
        amp = analyzer_sensing.trace_get_return
        with open(trace_file, 'a+') as file:
            file.write(str(i))
            file.write(";")
            file.write(str(len(amp)))
            file.write(";")
            file.write(str(amp))
            file.write("\n")
            file.close()    

def freq_loop(freq_data):
     for freq in freq_data:
        generator.meas_prep(True, generator_mode, generator_amplitude, freq) 
        # True means that generator is set up an generate something.
        ref_run_max(freq, 30)
        ref_run_mean(freq, 30)
        ref_run_vec(freq, 30)
        

if __name__=="__main__":
    try:
        analyzer_sensing.com_prep()
        analyzer_sensing.com_check()
        generator.com_check()
        time.sleep(20)
        freq_data = prepare_freq()
        freq_loop(freq_data)
        analyzer_sensing.meas_close()
        generator.meas_close()
        exit()
    except KeyboardInterrupt:
        print("[KEY]Keyboard interrupt.")
        exit()
