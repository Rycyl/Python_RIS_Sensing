import analyzer_sensing
import generator
import RIS_usb
import json
import numpy as np
from RsSmw import *
import time
from bitarray import bitarray
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

def pattern_iterative_state_optimization(freq):
    analyzer_sensing.meas_prep(freq, span, analyzer_mode, revlevel, rbw)
    current_pattern = bitarray(256)
    current_pattern.setall(0)
    current_pattern = current_pattern.tolist()
    index_of_on_elemets = []
    RIS_usb.set_pattern(def_pattern.pattern_bin_to_hex(current_pattern))
    time.sleep(0.05)
    #RIS_usb.read_pattern() #Inofrmation about pattern set on RIS.
    current_amp = analyzer_sensing.trace_get_return()
    print(current_amp)
    for i in range(len(current_pattern)):
        #print(i)
        analyzer_sensing.meas_prep(freq, span, analyzer_mode, revlevel, rbw)
        current_pattern[i]=1
        #print(current_pattern)
        #print(len(current_pattern))
        #print(def_pattern.pattern_bin_to_hex(current_pattern))
        RIS_usb.set_pattern(def_pattern.pattern_bin_to_hex(current_pattern))
        time.sleep(0.1)
        new_amp = analyzer_sensing.trace_get_return()
        #print(type(new_amp))
        print("I", i, "    N: ",new_amp, "    C: ", current_amp)
        #RIS_usb.read_pattern()
        if (new_amp < current_amp):
            current_pattern[i]=0
        else:
            #current_amp = new_amp
            index_of_on_elemets.append(i)
            current_pattern[i]=0

    for j in index_of_on_elemets:
        analyzer_sensing.meas_prep(freq, span, analyzer_mode, revlevel, rbw)
        current_pattern[j]=1
        RIS_usb.set_pattern(def_pattern.pattern_bin_to_hex(current_pattern))
        time.sleep(0.1)
        amp = analyzer_sensing.trace_get_return()
        with open(trace_file, 'a+') as file:
              file.write(str(def_pattern.pattern_bin_to_hex(current_pattern)))
              file.write(";")
              file.write(str(amp))
              file.write("\n")
              file.close()    


def on_off_measurement(freq):
    analyzer_sensing.meas_prep(freq, span, analyzer_mode, revlevel, rbw)
    all_off = 0
    on_element = 0x8000000000000000000000000000000000000000000000000000000000000000
    for i in range (256):
        analyzer_sensing.meas_prep(freq, span, analyzer_mode, revlevel, rbw)
        RIS_usb.set_pattern(def_pattern.turntohex(all_off))
        time.sleep(0.1)
        off_amp = analyzer_sensing.trace_get_return()
        RIS_usb.set_pattern(def_pattern.turntohex(on_element))
        time.sleep(0.1)
        on_amp = analyzer_sensing.trace_get_return()
        with open(trace_file, 'a+') as file:
            file.write("Element NO:"+str(i))
            file.write(";")
            file.write("OFF AMP:"+str(off_amp))
            file.write(";")
            file.write("ON AMP:"+str(on_amp))
            file.write("\n")
            file.close()
        on_element = on_element >> 1
            

        


def freq_loop(freq_data):
     for freq in freq_data:
        generator.meas_prep(True, generator_mode, generator_amplitude, freq) # True means that generator is set up an generate something.
        pattern_iterative_state_optimization(freq)
        pattern_loop(freq)

if __name__=="__main__":
    try:
        analyzer_sensing.com_prep()
        analyzer_sensing.com_check()
        generator.com_check()
        RIS_usb.reset_RIS()
        freq_data = prepare_freq()
        freq_loop(freq_data)
        analyzer_sensing.meas_close()
        generator.meas_close()
        exit()
    except KeyboardInterrupt:
        print("[KEY]Keyboard interrupt.")
        exit()
