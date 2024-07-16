import time
import os
import numpy as np
from RIS import RIS
import json


class Controller:
    def __init__(self, db_path = "temp_db.json", c_freq = 5.2e9, b_gain = 60.0, sample_rate = 1e6):
        self.db_path = db_path
        self.c_freq = c_freq
        self.b_gain = b_gain
        self.sample_rate = sample_rate
        self.RIS_list = {}

    def init_ris(self, port, id):
        ris = RIS(port, id)
        ris.reset()
        self.RIS_list[f"RIS_No_{id}"] = ris
        return repr(ris)
    
    def set_pattern(self, id, pattern):
        ris = self.RIS_list[f"RIS_No_{id}"]
        with open(self.db_path, "a") as db:
            json.dump({"pattent_change": f"RIS_NO_{id}","timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f"RIS_No_{id}_pattern": pattern}, db)
            db.write("\n")
        return ris.set_pattern(pattern)
    
    def reset(self, id):
        ris = self.RIS_list[f"RIS_No_{id}"]
        return ris.reset()

    def c_pattern(self, id):
        ris = self.RIS_list[f"RIS_No_{id}"]
        return ris.c_pattern

    def veryfy_pattern(self, id):
        ris = self.RIS_list[f"RIS_No_{id}"]
        return ris.read_pattern()

    def save_power_reading(self, power_reading):
        if not self.RIS_list:
            RIS_patterns = {"No RIS connected": "No RIS connected"}
        else:
            RIS_patterns  = {}
            for ris in self.RIS_list:
                RIS_patterns[f"{ris}_pattern"] = self.RIS_list[ris].c_pattern
        power_reading.update(RIS_patterns)
        additional_data = {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
        power_reading.update(additional_data)
        with open(self.db_path, "a") as db:
            json.dump(power_reading, db)
            db.write("\n")
        return True
    
    def save_raport(self, raport):
        with open(self.db_path, "a") as db:
            json.dump(raport, db)
            db.write("\n")
        return True
    
    
    def set_tran_param(self, freq, gain, samp_rate):
        self.c_freq = freq
        self.b_gain = gain
        self.sample_rate = samp_rate
        with open(self.db_path, "a") as db:
            json.dump({"status": "transmision_paramiters_change", "c_freq": freq, "gain": gain, "sample_rate": samp_rate,"timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}, db)
            db.write("\n")
        return f"frequencie set to {freq}, gain set to {gain} and sample rate set to {samp_rate}"
    
    def send_transmision_params(self):
        return {"c_freq": self.c_freq, "gain": self.b_gain, "sample_rate": self.sample_rate}
    


#dodać funkcje do sterowania parametrami przesyłu między Tx i Rx

