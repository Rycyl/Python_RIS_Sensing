from RsInstrument import *
import time
from time import sleep
import json
import csv
import numpy as np

try:
    with open ("config_sensing.json") as config_f:
        config = json.load(config_f)
        IP_ADDRESS_ANALYZER = config["IP_ADDRESS_ANALYZER"]
        PORT_ANALYZER = config["PORT"]
        CONNECTION_TYPE = config["CONNECTION_TYPE"]
        TRACE_FILE = config["TRACE_FILE"] 
        MEASURE_TIME = config["MEASURE_TIME"]
        DETECTOR = config["DETECTOR"]
        resource = f'TCPIP::{IP_ADDRESS_ANALYZER}::{PORT_ANALYZER}::{CONNECTION_TYPE}'  # Resource string for the device
        try:
            analyzer = RsInstrument(resource, True, True, "SelectVisa='socket'")   
        except TimeoutError or ConnectionAbortedError:
            print("[TIMEOUT ERROR] Check is computer and analyzer is connected to the same local network. Then try again.")
            exit()
<<<<<<< Updated upstream
        config_f.close()
except FileNotFoundError:
    print("Brak pliku konfiguracyjnego.")
    exit()


def com_prep():
    print(f'VISA Manufacturer: {analyzer.visa_manufacturer}')  
    analyzer.visa_timeout = 100000  
    analyzer.opc_timeout = 300000  
    analyzer.instrument_status_checking = True  
    analyzer.clear_status()  
  
    
def close():
    analyzer.close()


def com_check():
    idn_response = analyzer.query_str('*IDN?')
    print('Hello, I am ' + idn_response)
=======
        self.com_prep()
        self.com_check()

    def com_prep(self):
        print(f'VISA Manufacturer: {self.visa_manufacturer}')  
        self.visa_timeout = 100000  
        self.opc_timeout = 300000  
        self.instrument_status_checking = True  
        self.clear_status()  
        
    def com_check(self):
        idn_response = self.query_str('*IDN?')
        print('Hello, I am ' + idn_response)
        
>>>>>>> Stashed changes
    
   
def meas_prep(freq : int, swt : int, span : int, mode : str, detector : str, revlevel : int, rbw : str, swepnt : int, swtcnt : int = 1):
    analyzer.write_str_with_opc('*RST')
    analyzer.write_str_with_opc(f'FREQuency:CENTer {freq}')  
    analyzer.write_str_with_opc(f'FREQuency:SPAN {span}')  
    analyzer.write_str_with_opc(f'BAND {rbw}')  
    analyzer.write_str_with_opc(f'DISPlay:TRACe1:MODE {mode}')  
    analyzer.write_str_with_opc(f'DISPlay:WINDow:TRACe:Y:SCALe:RLEVel {revlevel}')
    analyzer.write_str_with_opc(f'DET {detector}')
    analyzer.write_str_with_opc(f'SWE:COUNT {swtcnt}')
    analyzer.write_str_with_opc(f'SWEep:TIME {swt}')
    analyzer.write_str_with_opc(f'SWEep:POINts {swepnt}')
    analyzer.write_str_with_opc('INITiate:CONTinuous OFF')
    mst = analyzer.query_float('SWEep:DUR?')
    print('Measurement prepared. freq:', freq, 'span:', span, 'mode:', mode, 'revlevel:', revlevel, 'rbw:', rbw, 'swepnt:', swepnt, 'swtcnt:', swtcnt)
    print(f'Measurement time: {mst} s')


    
def trace_get_vect_fx():
    #Initialize continuous measurement, stop it after the desired time, query trace data
    analyzer.write_str_with_opc('INIT;*WAI')
    # Get y data (amplitude for each point)
    trace_data = analyzer.query_bin_or_ascii_float_list_with_opc('FORM REAL,32;:TRAC:DATA? TRACe1')  
    #csv_trace_data = trace_data.split(",")  
    trace_len = len(trace_data)
    with open(TRACE_FILE, 'a+') as file:
        file.write(str(trace_len))
        file.write(",")
        writer = csv.writer(file)
        writer.writerow(trace_data)
        # for i in range(trace_len):
        #     datum = float(csv_trace_data[i]) 
        #     file.write(str(datum))
        #     file.write(",")
        # file.write("\n")
        file.close() 
    return np.mean(trace_data)   



def trace_get_mean():
    analyzer.write_str_with_opc('INIT;*WAI')  
    # Get y data (amplitude for each point)
    trace_data = analyzer.query_bin_or_ascii_float_list_with_opc('FORM REAL,32;:TRAC:DATA? TRACe1') 
    #trace_len = len(trace_data)
    x = np.mean(trace_data)
    return x

def trace_get():
    analyzer.write_str_with_opc('INIT;*WAI')  
    # Get y data (amplitude for each point)
    trace_data = analyzer.query_bin_or_ascii_float_list_with_opc('FORM REAL,32;:TRAC:DATA? TRACe1') 
    #trace_len = len(trace_data)
    return trace_data    