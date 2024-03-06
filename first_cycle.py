import analyzer
import generator
import json
import numpy as np
from RsSmw import *

try:
    with open ("config.json") as config_f:
        config = json.load(config_f)
        start_freq=config["START_FREQ"]
        end_freq=config["END_FREQ"]
        step_freq=config["STEP_FREQ"]
        span=config["SPAN"]
        analyzer_mode=config["ANALYZER_MODE"]
        revlevel=config["REVLEVEL"]
        rbw=config["RBW"]
        generator_amplitude=config["GENRATOR_AMPLITUDE"]
        # More modes will be add later.
        if config["GENERATOR_MODE"] == "CW":
            generator_mode = enums.FreqMode.CW
        else: 
            generator_mode = enums.FreqMode.CW
        config_f.close()
except FileNotFoundError:
    print("Brak pliku konfiguracyjnego.")
    exit()


def pattern_loop():
     analyzer.trace_get()

def freq_loop():
     for freq in freq_data:
        analyzer.meas_prep(freq, span, analyzer_mode, revlevel, rbw)
        generator.meas_prep(True, generator_mode, generator_amplitude, freq) # True means that generator is set up an generate something.
        pattern_loop()#TODO pętla po patternach tutaj, ale nie mam patternów
       

if __name__=="__main__":
    analyzer.com_prep()
    analyzer.com_check()
    generator.com_check()
    freq_data = np.arange(start_freq, end_freq+step_freq, step_freq)
    freq_loop(freq_data)
    analyzer.close()
    generator.close()