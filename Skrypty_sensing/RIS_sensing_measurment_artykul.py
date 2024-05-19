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
        swepnt = config["SWEEP_POINTS"]
        generator_amplitude=config["GENERATOR_AMPLITUDE"]
        detector = config["DETECTOR"]
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

def pattern_loop(freq, mestime):
    for pattern in patterns_data:
        analyzer_sensing.meas_prep(freq, mestime, span, analyzer_mode, detector, revlevel, rbw, swepnt)
        RIS_usb.set_pattern(pattern["HEX"])
        with open(trace_file, 'a+') as file:
            file.write(pattern["DESC"])  # Write information about pattern information
            file.write(",")
            file.close()  # CLose the file
        time.sleep(0.1)
        # RIS_usb.read_pattern() #Inofrmation about pattern set on RIS.
        analyzer_sensing.trace_get()
        #analyzer_sensing.trace_get_vect()

def clear_run (freq, mestime):
    pattern = patterns_data[0]
    for i in patterns_data:
        analyzer_sensing.meas_prep(freq, mestime, span, analyzer_mode, detector, revlevel, rbw, swepnt)
        RIS_usb.set_pattern(pattern["HEX"])
        with open(trace_file, 'a+') as file:
            file.write(pattern["DESC"])  # Write information about pattern information
            file.write(";")
            file.close()  # CLose the file
        time.sleep(0.1)
        # RIS_usb.read_pattern() #Inofrmation about pattern set on RIS.
        analyzer_sensing.trace_get()
    
def vector_mes(freq, mestime, pattern_1, pattern_2):
    analyzer_sensing.meas_prep(freq, mestime, span, analyzer_mode, detector, revlevel, rbw, swepnt)
    analyzer_sensing.trace_get_vect_fx()
    RIS_usb.set_pattern(pattern_1["HEX"])
    analyzer_sensing.meas_prep(freq, mestime, span, analyzer_mode, detector, revlevel, rbw, swepnt)
    generator.meas_prep(True, generator_mode, generator_amplitude, freq)
    #time.sleep(0.1)
    analyzer_sensing.trace_get_vect_fx()
    RIS_usb.set_pattern(pattern_2["HEX"])
    analyzer_sensing.meas_prep(freq, mestime, span, analyzer_mode, detector, revlevel, rbw, swepnt)
    #time.sleep(0.1)
    analyzer_sensing.trace_get_vect_fx()
    

def freq_loop(freq_data):
     for freq in freq_data:
        #generator.meas_prep(True, generator_mode, generator_amplitude, freq) 
        # True means that generator is set up an generate something.
        #pattern_loop(freq)
        #clear_run(freq)
        vector_mes(freq, 20, patterns_data[0], patterns_data[18])
        


time.sleep(20)
i=1
RIS_usb.reset_RIS()
analyzer_sensing.com_prep()
analyzer_sensing.com_check()
generator.com_check()
while (True):
                freq_data = prepare_freq()
                with open(trace_file, 'a+') as file:
                    file.write("pomiar " + str(i) + ",")
                    file.write(str(time.ctime(time.time())))
                    file.write("\n")
                    file.close
                i+=1
                freq_loop(freq_data)
                generator.meas_prep(True, generator_mode, -135.0, freq_data[0])
                time.sleep(10)    
analyzer_sensing.meas_close()
generator.meas_close()

'''
if __name__=="__main__":
    try:

        #time.sleep(20)
        for y in range (1,13):
            for x in range(1,6):
                analyzer_sensing.com_prep()
                analyzer_sensing.com_check()
                generator.com_check()
                RIS_usb.reset_RIS()
                freq_data = prepare_freq()
                with open(trace_file, 'a+') as file:
                    file.write("pomiar " + str(x*y))
                    file.write("\n")
                    file.close
                freq_loop(freq_data)
                generator.meas_close()
                time.sleep(5)
            time.sleep(60)    
        analyzer_sensing.meas_close()
        generator.meas_close()
        exit()
    except KeyboardInterrupt:
        print("[KEY]Keyboard interrupt.")
        exit()


#RX1 pwr TX lev = -40dBm
'''