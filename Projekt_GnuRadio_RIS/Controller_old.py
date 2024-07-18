import time
import os
import numpy as np
from RIS import RIS
import json
import serial.tools.list_ports
from enum import Enum



class Controller:
    def __init__(self, db_path = "temp_db.json", c_freq = 5.2e9, b_gain = 60.0, sample_rate = 1e6):
        self.db_path = db_path
        self.c_freq = c_freq
        self.b_gain = b_gain
        self.sample_rate = sample_rate
        self.RIS_list = {}
        self.port_list = Enum("Ports", self.find_port())

    # def init_db(self):
    #     if not os.path.exists(self.db_path):
    #         with open(self.db_path, "w") as db:
                

    def init_ris(self, port_obj, id):
        if port_obj is None:
            return "No port selected"
        port = port_obj.value
        ris = RIS(port, id)
        ris.reset()
        self.RIS_list[f"RIS_No_{id}"] = ris
        self.port_list = Enum("Ports", self.find_port())
        return repr(ris)
    
    def set_pattern(self, id, pattern):
        ris = self.RIS_list[f"RIS_No_{id}"]
        with open(self.db_path, "a") as db:
            json.dump({"pattern_change": f"RIS_NO_{id}","timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f"RIS_No_{id}_pattern": pattern}, db)
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
    
    
    def is_port_free(self, port, ris):
        if port == ris.port:
            return False
        else:
            return True


    def find_port(self):
        ports = {}
        for i in serial.tools.list_ports.comports():
            if i.description == "Open Source RIS - Open Source RIS":
                if not any(ris.port == i.device for ris in self.RIS_list.values()):
                    ports[i.device] = i.device
        #         else:
        #             print("port is busy")
        # print(ports)
        return ports


        

#dodać funkcje do sterowania parametrami przesyłu między Tx i Rx

