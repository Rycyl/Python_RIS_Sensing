import analyzer_sensing
import generator
import RIS_usb
import json
import numpy as np
import random
import time
import def_pattern
from enum import Enum

class FreqMode(Enum):
    CW = 'CW'
    OTHER = 'Other' 

try:
    with open("config_sensing.json") as config_f:
        config = json.load(config_f)
        trace_file = config["TRACE_FILE"]
        start_freq = config["START_FREQ"]
        end_freq = config["END_FREQ"]
        step_freq = config["STEP_FREQ"]
        span = config["SPAN"]
        analyzer_mode = config["ANALYZER_MODE"]
        revlevel = config["REVLEVEL"]
        rbw = config["RBW"]
        generator_amplitude = config["GENERATOR_AMPLITUDE"]
        generator_mode = FreqMode.CW if config["GENERATOR_MODE"] == "CW" else FreqMode.OTHER
except FileNotFoundError:
    print("File with configuration doesn't exist.")
    exit()


try:
    with open("RIS_patterns.json") as json_patterns:
        patterns_data = json.load(json_patterns)["PATTERNS"]
except FileNotFoundError:
    print("File with patterns doesn't exist.")
    exit()

def prepare_freq(start_freq, end_freq, step_freq):
    return np.arange(start_freq, end_freq + step_freq, step_freq) if start_freq != end_freq else [start_freq]

def apply_and_measure_specific_pattern(pattern, trace_file, freq):
    original_hex_pattern = int(pattern['HEX'], 16)
    original_amp = measure_amplitude(original_hex_pattern, freq)
    log_pattern_measurement(pattern['ID'], pattern['HEX'], original_amp, pattern['HEX'], original_amp, trace_file)
    
    zero_pattern = 0
    zero_amp = measure_amplitude(zero_pattern, freq)
    log_pattern_measurement(pattern['ID'], pattern['HEX'], original_amp, hex(zero_pattern), zero_amp, trace_file)
    
    modified_pattern = original_hex_pattern
    for i in range(1, 17):
        hex_zeros = '0' * (4 * i)
        hex_as = '5' * (64 - 4 * i)
        modified_hex = '0x' + hex_as + hex_zeros
        modified_pattern = int(modified_hex, 16)
        
        modified_amp = measure_amplitude(modified_pattern, freq)
        log_pattern_measurement(pattern['ID'], pattern['HEX'], original_amp, modified_hex, modified_amp, trace_file)

def measure_amplitude(pattern_hex, freq):
    RIS_usb.set_pattern(def_pattern.pattern_bin_to_hex(pattern_hex))
    analyzer_sensing.meas_prep(freq, span, analyzer_mode, revlevel, rbw)
    return analyzer_sensing.trace_get_return()

def log_pattern_measurement(id, original_hex, original_amp, modified_hex, modified_amp, trace_file):
    with open(trace_file, 'a+') as file:
        file.write(f"Pattern ID: {id}; Original HEX: {original_hex}; Original AMP: {original_amp}; "
                   f"Modified HEX: {modified_hex}; Modified AMP: {modified_amp}\n")

def main():
    freq_data = prepare_freq(config['START_FREQ'], config['END_FREQ'], config['STEP_FREQ'])
    
    pattern_to_measure = next((p for p in patterns_data if p["ID"] == "10"), None) #[0101]
    if pattern_to_measure:
        for freq in freq_data:
            apply_and_measure_specific_pattern(pattern_to_measure, config["TRACE_FILE"], freq)
    else:
        print("Specific pattern with ID '9' not found.")

if __name__ == "__main__":
    main()

