import time
import os
import numpy as np
from RIS import RIS
import json


class Controller:
    def __init__(self, db_path = "temp_db.json"):
        self.db_path = db_path
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
            db.write(",\n")
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
        RIS_patterns  = {}
        for ris in self.RIS_list:
            RIS_patterns[f"{ris}_pattern"] = self.RIS_list[ris].c_pattern
        power_reading.update(RIS_patterns)
        additional_data = {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
        power_reading.update(additional_data)
        with open(self.db_path, "a") as db:
            json.dump(power_reading, db)
            db.write(",\n")
        return True
    
    def save_raport(self, raport):
        with open(self.db_path, "a") as db:
            json.dump(raport, db)
            db.write(",\n")
        return True
    


#dodać funkcje do sterowania parametrami przesyłu między Tx i Rx

