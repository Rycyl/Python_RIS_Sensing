from RsInstrument import *
import time
from time import sleep
import json
import csv
import numpy as np

class Analyzer(RsInstrument):

    def __init__(self, config):
        self.resource = f'TCPIP::{config.IP_ADDRESS_ANALYZER}::{config.PORT_ANALYZER}::{config.CONNECTION_TYPE}'  # Resource string for the device
        try:
            RsInstrument.__init__(self, self.resource, True, True, "SelectVisa='socket'")
        except:
            print("[TIMEOUT ERROR] Check is  computer and generator is connected to the same local network. Then try again.")
            exit()
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
        
    def meas_prep(self, freq : int, swt : int, span : int, mode : str, detector : str, revlevel : int, rbw : str, swepnt : int, swtcnt : int = 1):
        self.write_str_with_opc('*RST')
        self.write_str_with_opc(f'FREQuency:CENTer {freq}')  
        self.write_str_with_opc(f'FREQuency:SPAN {span}')  
        self.write_str_with_opc(f'BAND {rbw}')  
        self.write_str_with_opc(f'DISPlay:TRACe1:MODE {mode}')  
        self.write_str_with_opc(f'DISPlay:WINDow:TRACe:Y:SCALe:RLEVel {revlevel}')
        self.write_str_with_opc(f'DET {detector}')
        self.write_str_with_opc(f'SWE:COUNT {swtcnt}')
        self.write_str_with_opc(f'SWEep:TIME {swt}')
        self.write_str_with_opc(f'SWEep:POINts {swepnt}')
        self.write_str_with_opc('INITiate:CONTinuous OFF')
        mst = self.query_float('SWEep:DUR?')
        print('Measurement prepared. freq:', freq, 'span:', span, 'mode:', mode, 'revlevel:', revlevel, 'rbw:', rbw, 'swepnt:', swepnt, 'swtcnt:', swtcnt)
        print(f'Measurement time: {mst} s')


        
    def trace_get_mean_and_csv_save_trace(self, trace_file = "trace_file.csv"):
        #Initialize continuous measurement, stop it after the desired time, query trace data
        self.write_str_with_opc('INIT;*WAI')
        # Get y data (amplitude for each point)
        trace_data = self.query_bin_or_ascii_float_list_with_opc('FORM REAL,32;:TRAC:DATA? TRACe1')  
        #csv_trace_data = trace_data.split(",")  
        trace_len = len(trace_data)
        with open(trace_file, 'a+') as file:
            writer = csv.writer(file)
            writer.writerow(trace_data)
            # for i in range(trace_len):
            #     datum = float(csv_trace_data[i]) 
            #     file.write(str(datum))
            #     file.write(",")
            # file.write("\n")
            file.close() 
        return np.mean(trace_data)   



    def trace_get_mean(self):
        self.write_str_with_opc('INIT;*WAI')  
        # Get y data (amplitude for each point)
        trace_data = self.query_bin_or_ascii_float_list_with_opc('FORM REAL,32;:TRAC:DATA? TRACe1') 
        #trace_len = len(trace_data)
        x = np.mean(trace_data)
        return x

    def trace_get(self):
        self.write_str_with_opc('INIT;*WAI')  
        # Get y data (amplitude for each point)
        trace_data = self.query_bin_or_ascii_float_list_with_opc('FORM REAL,32;:TRAC:DATA? TRACe1') 
        #trace_len = len(trace_data)
        return trace_data    