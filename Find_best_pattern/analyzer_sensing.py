from RsInstrument import *
import csv
import numpy as np

class Analyzer_virtual:
    def __init__(self, resource_name: str, id_query: bool = True, reset: bool = False, options: str = None, direct_session: object = None):
        # Inicjalizacja atrybutów symulowanego analizatora
        print("Silent Analyzer initialized. No physical device is connected.")

    def com_check(self):
        # Zamiast komunikacji z urządzeniem, po prostu symulujemy odpowiedź
        print('Hello, I am a Silent Analyzer (simulated device).')

    def meas_prep(self, freq: int, swt: int, span: int, mode: str, detector: str, revlevel: int, rbw: str, swepnt: int, swtcnt: int = 1):
        # Symulacja przygotowania pomiaru
        print(f'Measurement prepared (simulated). freq: {freq}, span: {span}, mode: {mode}, revlevel: {revlevel}, rbw: {rbw}, swepnt: {swepnt}, swtcnt: {swtcnt}')
        print('Measurement time: simulated value')

    def trace_get_mean_and_csv_save_trace(self, trace_file="trace_file.csv"):
        # Symulacja pobierania danych i zapisywania ich do pliku
        simulated_trace_data = np.random.rand(100)  # Symulowane dane
        mean_value = np.mean(simulated_trace_data)
        print(f'Simulated trace data mean: {mean_value}')
        
        with open(trace_file, 'a+') as file:
            writer = csv.writer(file)
            writer.writerow(simulated_trace_data)
        
        return mean_value

    def trace_get_mean(self):
        # Symulacja pobierania średniej z danych
        simulated_trace_data = np.random.rand(100)  # Symulowane dane
        mean_value = np.mean(simulated_trace_data)
        print(f'Simulated trace data mean: {mean_value}')
        return mean_value

    def trace_get(self):
        # Symulacja pobierania danych
        simulated_trace_data = np.random.rand(100)  # Symulowane dane
        print(f'Simulated trace data: {simulated_trace_data}')
        return simulated_trace_data





class Analyzer(RsInstrument, Analyzer_virtual):

    def __init__(self, config):
        self.resource = f'TCPIP::{config.IP_ADDRESS_ANALYZER}::{config.PORT_ANALYZER}::{config.CONNECTION_TYPE}'  # Resource string for the device
        self.visa_timeout = 5000  # Ustaw timeout na 5 sekund
        try:
            RsInstrument.__init__(self, self.resource, True, True, "SelectVisa='socket'")
            self.com_prep()
            self.com_check()
        except:
            print("[TIMEOUT ERROR] Check is  computer and generator is connected to the same local network. Then try again.")
            i = True
            while(i):
                i = input("Create virtual analyzer? [Y/n]?")
                if i == 'Y' or i == 'y':
                    Analyzer_virtual.__init__(self, self.resource, True, True, "SelectVisa='socket'")
                    break
                if i == 'N' or i == 'n':
                    exit()
                    break
        

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

    def trace_get(self):
        self.write_str_with_opc('INIT;*WAI')  
        # Get y data (amplitude for each point)
        trace_data = self.query_bin_or_ascii_float_list_with_opc('FORM REAL,32;:TRAC:DATA? TRACe1') 
        #trace_len = len(trace_data)
        return trace_data   
        
    def trace_get_mean_and_csv_save_trace(self, trace_file = "trace_file.csv"):
        trace_data = self.trace_get()
        trace_len = len(trace_data)
        with open(trace_file, 'a+') as file:
            writer = csv.writer(file)
            writer.writerow(trace_data)
            file.close() 
        return np.mean(trace_data)   

    def trace_get_mean(self):
        x = np.mean(self.trace_get())
        return x