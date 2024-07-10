import time
import os
import numpy as np
from RIS import RIS
import json


class Controller:
    def __init__(self, db_path = "temp_db.json"):
        self.db_path = db_path
        self.current_pattern = "0x0000000000000000000000000000000000000000000000000000000000000000"

    def init_ris(self, port, id):
        ris = RIS(port, id)
        ris.reset()
        return repr(ris)
    
    def set_pattern(self, ris, pattern):
        if(ris.set_pattern(pattern)):
            self.current_pattern = pattern
            return True
        else:
            return False
    
    def reset(self, ris):
        if(ris.reset()):
            self.current_pattern = "0x0000000000000000000000000000000000000000000000000000000000000000"
            return True
        else:
            return False

    def read_pattern(self, ris):
        pat = ris.read_pattern()
        if(pat == "TIMEOUT"):
            return pat
        else:
            self.current_pattern = pat
            return pat

    def save_power_reading(self, power_reading):
        #power_r = json.loads(power_reading)
        additional_data = {"pattern": self.current_pattern, "timestamp": time.localtime()}
        power_reading.update(additional_data)
        with open(self.db_path, "a") as db:
            json.dump(power_reading, db)
            db.write("\n")
            db.close()
        return True
    
    def save_raport(self, raport):
        with open(self.db_path, "a") as db:
            json.dump(raport, db)
            db.write("\n")
            db.close()
        return True
    

#dodać funkcje do sterowania parametrami przesyłu między Tx i Rx

