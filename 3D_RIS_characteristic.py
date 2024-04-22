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
        azimuth_step=config["AZIMUTH_STEP"]
        azimuth_no_angles = config["AZIMUTH_NO_ANGLES"]
        elevation_step=config["ELEVATION_STEP"]
        elevation_start_position = config["ELEVATION_START_STEPS"]  
        step_resolution = config["STEP_RESOLUTION"]
        elevation_no_angles = config["ELEVATION_NO_ANGLES"]
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
    with open("RIS_patterns_copy_for_tests.json") as json_patterns:
        patterns_obj = json.load(json_patterns)
        patterns_data = patterns_obj["PATTERNS"]
except FileNotFoundError:
    print("File with patterns doesn't exist.")
    exit()
    
def count_angle(step : int) -> str:
    angle = step*1/(step_resolution)*1.8
    return str(float(angle))

def prepare_freq() -> list:
    if start_freq != end_freq:   
        freq_data = np.arange(start_freq, end_freq+step_freq, step_freq)
    else:
        freq_data = [start_freq]
    return freq_data

def pattern_loop(freq : int, azimuth_angle : str, elevation_angle : str):
    for pattern in patterns_data:
        analyzer.meas_prep(freq, span, analyzer_mode, revlevel, rbw)
        RIS_usb.set_pattern(pattern["HEX"])
        with open(trace_file, 'a+') as file:
            file.write(azimuth_angle+";"+elevation_angle+";"+pattern["ID"]+";")  # Write information about pattern and angle
            file.close()  # Close the file
        time.sleep(0.1)
        analyzer.trace_get()

def freq_loop(freq_data : list, azimuth_angle : str, elevation_angle : str):
     for freq in freq_data:
        generator.meas_prep(True, generator_mode, generator_amplitude, freq) # True means that generator is set up an generate something.
        pattern_loop(freq, azimuth_angle, elevation_angle)
        
def angle_loop(freq_data : list, azimuth_steps_form_start : int, elevation_steps_from_start : int, elevation_no_angles : int) -> bool:
    for i in range(azimuth_no_angles+1):
        azimuth_angle = count_angle(azimuth_steps_form_start)
        print(f"######################[AZYMUT]: - {azimuth_angle} ############################")
        for i in range(elevation_no_angles+1):
            elevation_angle = count_angle(elevation_steps_from_start)
            print("[Aktualny kąt elewacji]: ", elevation_angle)
            print("[Ilość kroków od początku]: ", elevation_steps_from_start)
            freq_loop(freq_data, azimuth_angle, elevation_angle)
            remote_head.rotate_up(elevation_step)
            elevation_steps_from_start+=elevation_step
        time.sleep(1)
        remote_head.rotate_down((2*elevation_steps_from_start) - elevation_step) # back to elevation start postion
        elevation_steps_from_start = -elevation_start_position
        remote_head.rotate_right(azimuth_step) # move few steps to the right (descroption in config file)
        azimuth_steps_form_start += azimuth_step
    return True
       

if __name__=="__main__":
    try:
        analyzer.com_prep()
        analyzer.com_check()
        generator.com_check()
        RIS_usb.reset_RIS()
        #remote_head.az360()
        remote_head.rotate_down(elevation_start_position)
        elevation_steps_from_start = -elevation_start_position
        azimuth_steps_form_start = 0 # counts how many steps remote head did. Could be used to count actual measurement angle.
        freq_data = prepare_freq()
        measure_ended = angle_loop(freq_data, azimuth_steps_form_start, elevation_steps_from_start, elevation_no_angles)
        analyzer.meas_close()
        generator.meas_close()
        exit()
    except KeyboardInterrupt:
        print("[KEY]Keyboard interrupt.")
        exit()