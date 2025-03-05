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
                self.swepnt = int(self.sweptime/(1/int(self.rbw[0:-3]))) if (int(self.sweptime/(1/int(self.rbw[0:-3])))>=101) else 101
                self.generator_mode = enums.FreqMode.CW if config["GENERATOR_MODE"] == "CW" else enums.FreqMode.CW
                self.IP_ADDRESS_ANALYZER = config["IP_ADDRESS_ANALYZER"]
                self.PORT_ANALYZER = config["PORT"]
                self.CONNECTION_TYPE = config["CONNECTION_TYPE"]
                self.TRACE_FILE = config["TRACE_FILE"] 
                self.MEASURE_TIME = config["MEASURE_TIME"]
                self.DETECTOR = config["DETECTOR"]
                self.IP_ADDRESS_GENERATOR = config["IP_ADDRESS_GENERATOR"]
                self.PORT_GENERATOR = config["PORT"]
                self.azimuth_step_time = config["AZIMUTH_STEP_TIME"]
                self.elevation_step_time = config["ELEVATION_STEP_TIME"]
                self.step_resolution = config["STEP_RESOLUTION"]
                self.header_steps_az = config["HEADER_STEPS_AZ"]
                self.header_steps_el = config["HEADER_STEPS_EL"]
        except FileNotFoundError:
            print("File with configuration doesn't exist.")
            exit()

    def update_rbw(self, rbw):
        self.rbw = rbw
        self.swepnt = int(self.sweptime/(1/int(self.rbw[0:-3]))) if (int(self.sweptime/(1/int(self.rbw[0:-3])))>=101) else 101
        return

    def update_swt(self, swt):
        self.sweptime = swt
        self.swepnt = int(self.sweptime/(1/int(self.rbw[0:-3]))) if (int(self.sweptime/(1/int(self.rbw[0:-3])))>=101) else 101
        return

        



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


