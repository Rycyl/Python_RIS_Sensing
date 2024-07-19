import time
import os
import numpy as np
from RIS import RIS
import json
import serial.tools.list_ports
from enum import Enum
import sqlite3
import csv

class Controller:
    def __init__(self, db_path = "temp_db.db", c_freq = 5.2e9, b_gain = 60.0, sample_rate = 1e6):
        #self.db_path = db_path
        self.c_freq = c_freq
        self.b_gain = b_gain
        self.sample_rate = sample_rate
        self.RIS_list = {}
        self.port_list = Enum("Ports", self.find_port())
        self.conn = sqlite3.connect(db_path)
        self.curs = self.conn.cursor()
        self.init_db()
        self.param_id = 0
        self.data_set_name = Enum("Data_sets", {"logs":"logs", "power_readings":"power_readings", "transmision_params":"transmision_params"})

    def init_db(self):
        self.curs.execute('''CREATE TABLE IF NOT EXISTS logs (source TEXT, Message TEXT, timestamp TEXT, source_timestamp TEXT) ''')
        self.curs.execute('''CREATE TABLE IF NOT EXISTS power_readings (params_id INTEGER, source TEXT, power FLOAT, timestamp TEXT, source_timestamp TEXT, RIS_connected TEXT)''')
        self.curs.execute('''CREATE TABLE IF NOT EXISTS transmision_params (id INTEGER PRIMARY KEY, c_freq FLOAT, b_gain FLOAT, sample_rate FLOAT, timestamp TEXT)''') 
        self.conn.commit()
        return True

    def add_ris_to_db(self, id):
        self.curs.execute(f'''ALTER TABLE power_readings ADD COLUMN RIS_{id}_pattern TEXT''')
        self.conn.commit()

    def init_ris(self, port_obj, id):
        if port_obj is None:
            return "No port selected"
        port = port_obj.value
        ris = RIS(port, id)
        ris.reset()
        self.RIS_list[f"RIS_No_{id}"] = ris
        self.port_list = Enum("Ports", self.find_port())
        self.add_ris_to_db(id)
        return repr(ris)
    
    def set_pattern(self, id, pattern):
        ris = self.RIS_list[f"RIS_No_{id}"]
        self.curs.execute('''INSERT INTO logs (source, Message, timestamp, source_timestamp) VALUES (?, ?, ?, ?)''', ("Controller", f"RIS NO {id} pattern change to {pattern}", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "N/A"))
        self.conn.commit()
        # with open(self.db_path, "a") as db:
        #     json.dump({"pattern_change": f"RIS_NO_{id}","timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f"RIS_No_{id}_pattern": pattern}, db)
        #     db.write("\n")
        return ris.set_pattern(pattern)
    
    def reset(self, id):
        ris = self.RIS_list[f"RIS_No_{id}"]
        self.curs.execute('''INSERT INTO logs (source, Message, timestamp, source_timestamp) VALUES (?, ?, ?, ?)''', ("Controller", f"RIS NO {id} reset", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "N/A"))
        return ris.reset()

    def c_pattern(self, id):
        ris = self.RIS_list[f"RIS_No_{id}"]
        return ris.c_pattern

    def veryfy_pattern(self, id):
        ris = self.RIS_list[f"RIS_No_{id}"]
        return ris.read_pattern()

    def save_power_reading(self, power_reading):
        self.curs.execute('''INSERT INTO power_readings (params_id, source, power, timestamp, source_timestamp) VALUES (?, ?, ?, ?, ?)''', (self.param_id ,power_reading["source"], power_reading["power"], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), power_reading["source_timestamp"]))
        if not self.RIS_list:
            #RIS_connected = "No"
            self.curs.execute('''INSERT INTO power_readings (RIS_connected) VALUES (?)''', ("No",))
        else:
            self.curs.execute('''INSERT INTO power_readings (RIS_connected) VALUES (?)''', ("Yes",))
            for ris in self.RIS_list:
                self.curs.execute(f'''INSERT INTO power_readings (RIS_{ris.id}_pattern) VALUES (?)''', (ris.c_pattern))
        self.conn.commit()
            #RIS_connected = "Yes"

        # if not self.RIS_list:
        #     RIS_patterns = {"No RIS connected": "No RIS connected"}
        # else:
        #     RIS_patterns  = {}
        #     for ris in self.RIS_list:
        #         RIS_patterns[f"{ris}_pattern"] = self.RIS_list[ris].c_pattern
        # power_reading.update(RIS_patterns)
        # additional_data = {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
        # power_reading.update(additional_data)
        # with open(self.db_path, "a") as db:
        #     json.dump(power_reading, db)
        #     db.write("\n")
        return True
    
    def save_raport(self, raport):
        message_content = f"status: {raport['status']}, Set paramiters: Freq = {raport['c_freq']}, Gain = {raport['b_gain']}, Sample_rate = {raport['sample_rate']}"
        self.curs.execute('''INSERT INTO logs (source, Message, timestamp, source_timestamp) VALUES (?, ?, ?, ?)''', (raport["source"], message_content, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), raport["source_timestamp"]))
        self.conn.commit()
        # with open(self.db_path, "a") as db:
        #     json.dump(raport, db)
        #     db.write("\n")
        return True
    
    
    def set_tran_param(self, freq, gain, samp_rate):
        self.c_freq = freq
        self.b_gain = gain
        self.sample_rate = samp_rate
        self.param_id += 1
        self.curs.execute('''INSERT INTO transmision_params (id, c_freq, b_gain, sample_rate, timestamp) VALUES (?, ?, ?, ?, ?)''', (self.param_id ,freq, gain, samp_rate, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        self.curs.execute(''' INSERT INTO logs (source, Message, timestamp, source_timestamp) VALUES (?, ?, ?, ?)''', ("Controller", f"Transmision parameters changed to: freq = {freq}, gain = {gain}, sample_rate = {samp_rate}", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "N/A"))
        self.conn.commit()
        # with open(self.db_path, "a") as db:
        #     json.dump({"status": "transmision_paramiters_change", "c_freq": freq, "gain": gain, "sample_rate": samp_rate,"timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}, db)
        #     db.write("\n")
        return f"frequencie set to {freq}, gain set to {gain} and sample rate set to {samp_rate}"
    
    def send_transmision_params(self):
        return {"c_freq": self.c_freq, "gain": self.b_gain, "sample_rate": self.sample_rate}
    
    
    # def is_port_free(self, port, ris):
    #     if port == ris.port:
    #         return False
    #     else:
    #         return True


    def find_port(self):
        ports = {}
        for i in serial.tools.list_ports.comports():
            if i.description == "Open Source RIS - Open Source RIS":
                if not any(ris.port == i.device for ris in self.RIS_list.values()):
                    ports[i.device] = i.device
        return ports


    def write_db_to_file(self, data_set_name):
        self.curs.execute(f"SELECT * FROM {data_set_name}")
        data = self.curs.fetchall()
        with open(f"{data_set_name}.csv", 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(data)
        return True

    def clear_db(self, data_set_name):
        self.curs.execute(f"DELETE FROM {data_set_name}")
        self.conn.commit()
        return True



#Con = Controller()