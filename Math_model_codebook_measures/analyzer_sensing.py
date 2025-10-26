from RsInstrument import *
import csv
import numpy as np
from Traces import Trace
from Traces import read_all_SWT

class Analyzer_virtual():
    def __init__(self, config):
        self.config = config
        self.traces = [] #tablica obj Trace
        self.traces_init()
        # Inicjalizacja atrybutów symulowanego analizatora
        print("Silent Analyzer initialized. No physical device is connected.")

    def traces_init(self):
        SWTs = read_all_SWT()
        self.traces = []
        for S in SWTs:
            self.traces.append(Trace(S))
        return

    def com_check(self):
        # Zamiast komunikacji z urządzeniem, po prostu symulujemy odpowiedź
        print('Hello, I am a Silent Analyzer (simulated device).')

    def meas_prep(self, freq: int, swt: int, span: int, mode: str, detector: str, revlevel: int, rbw: str, swepnt: int, swtcnt: int = 1):
        # Symulacja przygotowania pomiaru
        print(f'Measurement prepared (simulated). freq: {freq}, span: {span}, mode: {mode}, revlevel: {revlevel}, rbw: {rbw}, swepnt: {swepnt}, swtcnt: {swtcnt}')
        print('Measurement time: simulated value')

    def trace_get(self):
        # Symulacja pobierania danych
        SWT = self.config.sweptime
        #print("------------------------")
        #print(f"Aktualne SWT to {SWT}")
        #print(type(SWT))
        #print("------------------------")
        simulated_trace_data = []
        for T in self.traces:
            #print(f"Znalezione SWT {T.SWT}")
            #print(type(T.SWT))
            #print("-----------------------")
            if T.SWT == SWT:
                simulated_trace_data = T.return_trace()
                return simulated_trace_data
        print("Can't find trace for given SWT, exiting....")
        exit()

    def trace_get_mean_and_csv_save_trace(self, trace_file="trace_file.csv"):
        # Symulacja pobierania danych i zapisywania ich do pliku
        simulated_trace_data = self.trace_get()
        mean_value = np.mean(simulated_trace_data)        
        with open(trace_file, 'a+') as file:
            writer = csv.writer(file)
            writer.writerow(simulated_trace_data)
        return mean_value

    def trace_get_mean(self):
        # Symulacja pobierania średniej z danych
        simulated_trace_data = self.trace_get()
        mean_value = np.mean(simulated_trace_data)
        print(f'Simulated trace data mean: {mean_value}')
        return mean_value

    def close(self):
        print("Analyzer closed")



class Analyzer(RsInstrument, Analyzer_virtual):

    def __init__(self, config, phy_device = True):
        self.resource = f'TCPIP::{config.IP_ADDRESS_ANALYZER}::{config.PORT_ANALYZER}::{config.CONNECTION_TYPE}'  # Resource string for the device
        print(self.resource)
        if phy_device:
            try:
                print("Physical Analyzer connection attepmt")
                RsInstrument.__init__(self, self.resource, True, True, "SelectVisa='socket'")#, VisaTimeout = 5000)
                self.com_prep()
                self.com_check()
            except: #Exception as e:
                #print(e)
                print("[TIMEOUT ERROR] Check is  computer and generator is connected to the same local network. Then try again.")
                i = input("Create virtual device? [Y/n]")
                if i in ['y', 'Y']:
                    Analyzer_virtual.__init__(self, config=config)
        else:
            Analyzer_virtual.__init__(self, config=config)
        return

    def com_prep(self):
        try:
            print(f'VISA Manufacturer: {self.visa_manufacturer}')  
            self.visa_timeout = 100000  
            self.opc_timeout = 300000  
            self.instrument_status_checking = True  
            self.clear_status()
        except:
            Analyzer_virtual.com_prep()
        
    def com_check(self):
        try:
            idn_response = self.query_str('*IDN?')
            print('Hello, I am ' + idn_response)
        except:
            Analyzer_virtual.com_check()
        
    def meas_prep(self, freq : int, swt : int, span : int, mode : str, detector : str, revlevel : int, rbw : str, swepnt : int, swtcnt : int = 1):
        try:
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
        except:
            Analyzer_virtual.meas_prep(freq, swt, span, mode, detector, revlevel, rbw, swepnt, swtcnt)

    def trace_get(self):
        try:
            self.write_str_with_opc('INIT;*WAI')  
            # Get y data (amplitude for each point)
            trace_data = self.query_bin_or_ascii_float_list_with_opc('FORM REAL,32;:TRAC:DATA? TRACe1') 
            #trace_len = len(trace_data)
            return trace_data   
        except:
            return super().trace_get()
    
    def get_freq_range(self):
        start_freq = self.query_float_with_opc('FREQuency:STARt?')
        span = self.query_float_with_opc('FREQuency:SPAN?')
        trace_len = self.query_int_with_opc('SWEep:POINts?')
        
        step_size = span/(trace_len-1)

        x = [(start_freq + f *step_size) for f in range(trace_len)]
        return x
        
    def trace_get_mean_and_csv_save_trace(self, trace_file = "trace_file.csv"):
        try:
            trace_data = self.trace_get()
            trace_len = len(trace_data)
            with open(trace_file, 'a+') as file:
                writer = csv.writer(file)
                writer.writerow(trace_data)
                file.close() 
            return np.mean(trace_data)
        except:
            Analyzer_virtual.trace_get_mean_and_csv_save_trace(trace_file)

    def trace_get_mean(self):
        try:
            x = np.mean(self.trace_get())
            return x
        except:
            super().trace_get_mean()

    def close(self):
        try:
            RsInstrument.close(self)
        except:
            Analyzer_virtual.close(self)


# import numpy as np
# import csv
# from RsInstrument import RsInstrument  # Assuming this is the correct import

# class Analyzer:
#     def __init__(self, config, phy_device=True):
#         self.config = config
#         self.phy_device = phy_device
#         self.analyzer = None

#         if phy_device:
#             try:
#                 print("Attempting to connect to Physical Analyzer...")
#                 self.analyzer = PhysicalAnalyzer(config)
#                 print("Connected to Physical Analyzer.")
#             except Exception as e:
#                 print(f"Physical Analyzer connection failed: {e}")
#                 choice = input("Create virtual Analyzer? [Y/n]: ")
#                 if choice.lower() == 'y':
#                     self.analyzer = VirtualAnalyzer(config)
#                     print("Virtual Analyzer created.")
#                 else:
#                     print("Exiting...")
#                     exit()
#         else:
#             self.analyzer = VirtualAnalyzer(config)
#             print("Virtual Analyzer created.")

#     def __getattr__(self, name):
#         return getattr(self.analyzer, name)

# # Define the PhysicalAnalyzer class
# class PhysicalAnalyzer(RsInstrument):
#     def __init__(self, config):
#         resource = f'TCPIP::{config.IP_ADDRESS_ANALYZER}::{config.PORT_ANALYZER}::{config.CONNECTION_TYPE}'
#         print("Physical Analyzer connection attempt...")
#         super().__init__(resource, True, True, "SelectVisa='socket'")
#         self.config = config
#         self.com_prep()
#         self.com_check()

#     def com_prep(self):
#         print(f'VISA Manufacturer: {self.visa_manufacturer}')
#         self.visa_timeout = 100000
#         self.opc_timeout = 300000
#         self.instrument_status_checking = True
#         self.clear_status()

#     def com_check(self):
#         idn = self.query_str('*IDN?')
#         print(f'Instrument IDN: {idn}')
#         if 'FSV' in idn:
#             print('Connection OK.')
#         else:
#             raise Exception('Unknown device.')
#     def meas_prep(self, freq : int, swt : int, span : int, mode : str, detector : str, revlevel : int, rbw : str, swepnt : int, swtcnt : int = 1):
#         self.write_str_with_opc('*RST')
#         self.write_str_with_opc(f'FREQuency:CENTer {freq}')  
#         self.write_str_with_opc(f'FREQuency:SPAN {span}')  
#         self.write_str_with_opc(f'BAND {rbw}')  
#         self.write_str_with_opc(f'DISPlay:TRACe1:MODE {mode}')  
#         self.write_str_with_opc(f'DISPlay:WINDow:TRACe:Y:SCALe:RLEVel {revlevel}')
#         self.write_str_with_opc(f'DET {detector}')
#         self.write_str_with_opc(f'SWE:COUNT {swtcnt}')
#         self.write_str_with_opc(f'SWEep:TIME {swt}')
#         self.write_str_with_opc(f'SWEep:POINts {swepnt}')
#         self.write_str_with_opc('INITiate:CONTinuous OFF')
#         mst = self.query_float('SWEep:DUR?')
#         print('Measurement prepared. freq:', freq, 'span:', span, 'mode:', mode, 'revlevel:', revlevel, 'rbw:', rbw, 'swepnt:', swepnt, 'swtcnt:', swtcnt)
#         print(f'Measurement time: {mst} s')

#     def trace_get(self):
#         print("Getting trace data from Physical Analyzer...")
#         self.write_str_with_opc('INIT;*WAI')
#         trace_data = self.query_bin_or_ascii_float_list_with_opc('FORM REAL,32;:TRAC:DATA? TRACe1')
#         return trace_data

#     def trace_get_mean(self):
#         trace_data = self.trace_get()
#         mean_value = np.mean(trace_data)
#         print(f'Trace data mean: {mean_value}')
#         return mean_value

#     def trace_get_mean_and_csv_save_trace(self, trace_file="trace_file.csv"):
#         trace_data = self.trace_get()
#         with open(trace_file, 'a+') as file:
#             writer = csv.writer(file)
#             writer.writerow(trace_data)
#         mean_value = np.mean(trace_data)
#         print(f'Trace data mean saved to CSV: {mean_value}')
#         return mean_value

#     def close(self):
#         print("Closing Physical Analyzer connection...")
#         self.close()

# # Define the VirtualAnalyzer class
# class VirtualAnalyzer:
#     def __init__(self, config):
#         self.config = config
#         print("Initialized Virtual Analyzer.")
    
#     def meas_prep(self, freq: int, swt: int, span: int, mode: str, detector: str, revlevel: int, rbw: str, swepnt: int, swtcnt: int = 1):
#         # Symulacja przygotowania pomiaru
#         print(f'Measurement prepared (simulated). freq: {freq}, span: {span}, mode: {mode}, revlevel: {revlevel}, rbw: {rbw}, swepnt: {swepnt}, swtcnt: {swtcnt}')
#         print('Measurement time: simulated value')

#     def trace_get(self):
#         # Symulacja pobierania danych
#         SWT = self.config.sweptime
#         #print("------------------------")
#         #print(f"Aktualne SWT to {SWT}")
#         #print(type(SWT))
#         #print("------------------------")
#         simulated_trace_data = []
#         for T in self.traces:
#             #print(f"Znalezione SWT {T.SWT}")
#             #print(type(T.SWT))
#             #print("-----------------------")
#             if T.SWT == SWT:
#                 simulated_trace_data = T.return_trace()
#                 return simulated_trace_data
#         print("Can't find trace for given SWT, exiting....")
#         exit()

#     def trace_get_mean(self):
#         simulated_trace_data = self.trace_get()
#         mean_value = np.mean(simulated_trace_data)
#         print(f'Simulated trace data mean: {mean_value}')
#         return mean_value

#     def trace_get_mean_and_csv_save_trace(self, trace_file="trace_file.csv"):
#         simulated_trace_data = self.trace_get()
#         with open(trace_file, 'a+') as file:
#             writer = csv.writer(file)
#             writer.writerow(simulated_trace_data)
#         mean_value = np.mean(simulated_trace_data)
#         print(f'Simulated trace data mean saved to CSV: {mean_value}')
#         return mean_value

#     def close(self):
#         print("Virtual Analyzer closed.")
