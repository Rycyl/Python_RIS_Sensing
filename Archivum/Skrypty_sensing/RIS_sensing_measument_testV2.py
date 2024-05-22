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

def prepare_freq() -> list:
    return np.arange(start_freq, end_freq + step_freq, step_freq) if start_freq != end_freq else [start_freq]

def apply_and_modify_patterns(patterns, trace_file,freq):
    random_pattern = random.getrandbits(256)
    for pattern in patterns:
        original_hex_pattern = int(pattern['HEX'], 16)
        original_amp = measure_amplitude(original_hex_pattern, freq)

        combined_pattern = original_hex_pattern | random_pattern
        combined_amp = measure_amplitude(combined_pattern, freq)

        log_pattern_measurement(pattern['ID'], original_hex_pattern, original_amp, combined_pattern, combined_amp, trace_file)

def measure_amplitude(pattern_hex, freq):
    RIS_usb.set_pattern(def_pattern.pattern_bin_to_hex(pattern_hex))
    analyzer_sensing.meas_prep(freq, span, analyzer_mode, revlevel, rbw)
    return analyzer_sensing.trace_get_return()

def log_pattern_measurement(id, original_hex, original_amp, combined_hex, combined_amp, trace_file):
    with open(trace_file, 'a+') as file:
        file.write(f"Pattern ID: {id}; Original HEX: {original_hex}; Original AMP: {original_amp}; Combined HEX: {combined_hex}; Combined AMP: {combined_amp}\n")

def freq_loop(freq_data):
    for freq in freq_data:
        generator.meas_prep(True, generator_mode, generator_amplitude, freq)
        if patterns_data:
            apply_and_modify_patterns(patterns_data, trace_file, freq)


if __name__ == "__main__":
    try:
        analyzer_sensing.com_prep()
        analyzer_sensing.com_check()
        generator.com_check()
        RIS_usb.reset_RIS()
        freq_data = prepare_freq()
        freq_loop(freq_data)
        analyzer_sensing.meas_close()
        generator.meas_close()
    except KeyboardInterrupt:
        print("[KEY] Keyboard interrupt.")
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
    finally:
        exit()
