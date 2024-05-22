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
  
    
def meas_close():
    analyzer.close()


def com_check():
    idn_response = analyzer.query_str('*IDN?')
    print('Hello, I am ' + idn_response)
    
   
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



def trace_get():
    """Initialize continuous measurement, stop it after the desired time, query trace data"""
    analyzer.write_str_with_opc('INIT;*WAI')  
    # Get y data (amplitude for each point)
    trace_data = analyzer.query_bin_or_ascii_float_list_with_opc('FORM REAL,32;:TRAC:DATA? TRACe1') #zobaczyć czy to zadziała bo interpreter nie widzi definicji
    trace_len = len(trace_data)
    #print(type(trace_data[0]))
    #jeśli zwraca to jako str to zamienić na float
    #jeśli nie działa to zamiast tego użyć poniższego kodu
    #-----------------------------------------------------
    #trace_data = analyzer.query('Trace:DATA? TRACe1')
    #csv_trace_data = trace_data.split(",")  
    #trace_len = len(csv_trace_data) 
    #----------------------------------------------------- 
    x = np.mean(trace_data)
    #-----------------------------------------------------
    # jeśli jednak trzeba maksa to wtedy:
    # max_amp = -150
    # x = 0  # Set counter to 0 as list starts with 0
    # while x < int(trace_len):  # Perform loop until all sweep points are covered
    #     amp = float(trace_data[x])
    #     if amp > max_amp:
    #         max_amp = amp
    #         max_x = x
    #     x = x+1
    # with open(TRACE_FILE, 'a+') as file:
    #     file.write(";")
    #     file.write(f'{max_amp:.2f}')  # Write adequate amplitude information
    #     file.write("\n")
    #     file.close()  # CLose the file
    return x
    #wywalić komentarze jak sformalizuje się to
        