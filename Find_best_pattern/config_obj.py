import json
from RsSmw import *

class Config:
    def __init__(self, config_path = "config_sensing.json", ):
        self.load_config(config_path)
        

    def load_config(self, config_path):
        try:
            with open(config_path) as config_f:
                config = json.load(config_f)
                self.trace_file = config["TRACE_FILE"]
                self.freq = config["CENTRAL_FREQ"]
                self.span = config["SPAN"]
                self.analyzer_mode = config["ANALYZER_MODE"]
                self.revlevel = config["REVLEVEL"]
                self.rbw = config["RBW"]
                self.generator_amplitude = config["GENERATOR_AMPLITUDE"]
                self.detector = config["DETECTOR"]
                self.sweptime = config["SWEEP_TIME"]
                self.swepnt = int(sweptime/(1/int(rbw[0:-3])))
                self.generator_mode = enums.FreqMode.CW if config["GENERATOR_MODE"] == "CW" else enums.FreqMode.CW
        except FileNotFoundError:
            print("File with configuration doesn't exist.")
            exit()

class Patterns:
    def __init__(self, patterns_path = "RIS_patterns.json"):
        self.load_patterns(patterns_path)
    
    def load_patterns(self, patterns_path):
        try:
            with open(patterns_path) as json_patterns:
                patterns_obj = json.load(json_patterns)
                self.patterns_data = patterns_obj["PATTERNS"]
        except FileNotFoundError:
            print("File with patterns doesn't exist.")
            exit()
        return


