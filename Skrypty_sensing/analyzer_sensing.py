from RsInstrument import *
from time import sleep
import json

try:
    with open ("config_sensing.json") as config_f:
        config = json.load(config_f)
        IP_ADDRESS_ANALYZER = config["IP_ADDRESS_ANALYZER"]
        PORT_ANALYZER = config["PORT"]
        CONNECTION_TYPE = config["CONNECTION_TYPE"]
        TRACE_FILE = config["TRACE_FILE"] 
        MEASURE_TIME = config["MEASURE_TIME"]
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
    analyzer.visa_timeout = 5000  
    analyzer.opc_timeout = 3000  
    analyzer.instrument_status_checking = True  
    analyzer.clear_status()  
  
    
def meas_close():
    analyzer.close()


def com_check():
    idn_response = analyzer.query_str('*IDN?')
    print('Hello, I am ' + idn_response)
    
   
def meas_prep(freq : int, span : int, mode : str, revlevel : int, rbw : str):
    analyzer.write_str_with_opc(f'FREQuency:CENTer {freq}')  
    analyzer.write_str_with_opc(f'FREQuency:SPAN {span}')  
    analyzer.write_str_with_opc(f'BAND {rbw}')  
    analyzer.write_str_with_opc(f'DISPlay:TRACe1:MODE {mode}')  
    analyzer.write_str_with_opc(f'DISPlay:WINDow:TRACe:Y:SCALe:RLEVel {revlevel}')
    


def trace_get():
    """Initialize continuous measurement, stop it after the desired time, query trace data"""
    analyzer.write_str_with_opc('INITiate:CONTinuous ON')  
    sleep(int(MEASURE_TIME))  # Wait for preset record time
    analyzer.write('DISPlay:TRACe1:MODE VIEW')
    analyzer.query_opc()
    sleep(0.1) # Wait for data
    # Get y data (amplitude for each point)
    trace_data = analyzer.query('Trace:DATA? TRACe1') 
    csv_trace_data = trace_data.split(",")  
    trace_len = len(csv_trace_data)  
    # Reconstruct x data (frequency for each point) as it can not be directly read from the analyzer
    start_freq = analyzer.query_float('FREQuency:STARt?')
    span = analyzer.query_float('FREQuency:SPAN?')
    step_size = span / (trace_len-1)
    # Now write values into file
    max_amp = -150
    x = 0  # Set counter to 0 as list starts with 0
    while x < int(trace_len):  # Perform loop until all sweep points are covered
        amp = float(csv_trace_data[x])
        if amp > max_amp:
            max_amp = amp
            max_x = x
        x = x+1
    with open(TRACE_FILE, 'a+') as file:
        file.write(f'{(start_freq + max_x * step_size):.1f}')  # Write adequate frequency information
        file.write(";")
        file.write(f'{max_amp:.2f}')  # Write adequate amplitude information
        file.write("\n")
        file.close()  # CLose the file
        
def trace_get_vect(mes_time):
    """Initialize continuous measurement, stop it after the desired time, query trace data"""
    analyzer.write_str_with_opc('INITiate:CONTinuous ON')  
    sleep(int(mes_time))  # Wait for preset record time
    analyzer.write('DISPlay:TRACe1:MODE VIEW')
    analyzer.query_opc()
    sleep(0.1) # Wait for data
    # Get y data (amplitude for each point)
    trace_data = analyzer.query('Trace:DATA? TRACe1') 
    csv_trace_data = trace_data.split(",")  
    trace_len = len(csv_trace_data)
    with open(TRACE_FILE, 'a+') as file:
        file.write(str(trace_len))
        file.write(";")
        file.write(str(csv_trace_data))
        file.write("\n")
        file.close()
    # ---------------------------------------------------------
    # Alternatywna wersja z rozdzielaniem komurek danych
    # ---------------------------------------------------------
    # with open(TRACE_FILE, 'a+') as file:
    #     file.write(str(trace_len))
    #     file.write(";")
    #     for i in range(trace_len):
    #         file.write(str(csv_trace_data[i]))
    #         file.write(",")
    #     file.write("\n")
    #     file.close()
    # ---------------------------------------------------------
    # Stara wersja funkcji
    # ---------------------------------------------------------
    # # Reconstruct x data (frequency for each point) as it can not be directly read from the analyzer
    # start_freq = analyzer.query_float('FREQuency:STARt?')
    # span = analyzer.query_float('FREQuency:SPAN?')
    # step_size = span / (trace_len-1)
    # # Now write values into file
    # max_amp = -150
    # x = 0  # Set counter to 0 as list starts with 0
    # amp_vec = []
    # while x < int(trace_len):  # Perform loop until all sweep points are covered
    #     amp = float(csv_trace_data[x])
    #     amp_vec.append(amp)
    #     x += 1
        
    # with open(TRACE_FILE, 'a+') as file:
    #     file.write(str(amp_vec))  # Write adequate amplitude information
    #     file.write("\n")
    #     file.close()  # CLose the file
        
        
def trace_get_return():
    """Initialize continuous measurement, stop it after the desired time, query trace data"""
    analyzer.write_str_with_opc('INITiate:CONTinuous ON')  
    sleep(int(MEASURE_TIME))  # Wait for preset record time
    analyzer.write('DISPlay:TRACe1:MODE VIEW')
    analyzer.query_opc()
    sleep(0.1) # Wait for data
    # Get y data (amplitude for each point)
    trace_data = analyzer.query('Trace:DATA? TRACe1') 
    csv_trace_data = trace_data.split(",")  
    trace_len = len(csv_trace_data)  
    # Reconstruct x data (frequency for each point) as it can not be directly read from the analyzer
    start_freq = analyzer.query_float('FREQuency:STARt?')
    span = analyzer.query_float('FREQuency:SPAN?')
    step_size = span / (trace_len-1)
    # Now write values into file
    max_amp = -150
    x = 0  # Set counter to 0 as list starts with 0
    while x < int(trace_len):  # Perform loop until all sweep points are covered
        amp = float(csv_trace_data[x])
        if amp > max_amp:
            max_amp = amp
            max_x = x
        x = x+1
    """ with open(TRACE_FILE, 'a+') as file:
        file.write(f'{(start_freq + max_x * step_size):.1f}')  # Write adequate frequency information
        file.write(";")
        file.write(f'{max_amp:.2f}')  # Write adequate amplitude information
        file.write("\n")
        file.close()  # CLose the file """
    return max_amp

def trace_get_return_mean():
    """Initialize continuous measurement, stop it after the desired time, query trace data"""
    analyzer.write_str_with_opc('INITiate:CONTinuous ON')  
    sleep(int(MEASURE_TIME))  # Wait for preset record time
    analyzer.write('DISPlay:TRACe1:MODE VIEW')
    analyzer.query_opc()
    sleep(0.1) # Wait for data
    # Get y data (amplitude for each point)
    trace_data = analyzer.query('Trace:DATA? TRACe1') 
    csv_trace_data = trace_data.split(",")  
    trace_len = len(csv_trace_data)  
    # Reconstruct x data (frequency for each point) as it can not be directly read from the analyzer
    start_freq = analyzer.query_float('FREQuency:STARt?')
    span = analyzer.query_float('FREQuency:SPAN?')
    step_size = span / (trace_len-1)
    # Now write values into file
    max_amp = -150
    x = 0  # Set counter to 0 as list starts with 0
    amp_mean = 0
    while x < int(trace_len):  # Perform loop until all sweep points are covered
        amp = float(csv_trace_data[x])
        amp_mean += amp
        x+=1
    
    amp_mean = amp_mean/x 
    return amp_mean

def trace_get_return_vect():
    """Initialize continuous measurement, stop it after the desired time, query trace data"""
    analyzer.write_str_with_opc('INITiate:CONTinuous ON')  
    sleep(int(MEASURE_TIME))  # Wait for preset record time
    analyzer.write('DISPlay:TRACe1:MODE VIEW')
    analyzer.query_opc()
    sleep(0.1) # Wait for data
    # Get y data (amplitude for each point)
    trace_data = analyzer.query('Trace:DATA? TRACe1') 
    csv_trace_data = trace_data.split(",")  
    trace_len = len(csv_trace_data)  
    x = 0  # Set counter to 0 as list starts with 0
    amp_vect = []
    while x < int(trace_len):  # Perform loop until all sweep points are covered
        amp = float(csv_trace_data[x])
        amp_vect.append(amp)
        x+=1

    return amp_vect


    
if __name__ == "__main__":
    com_prep()
    com_check()
    meas_prep(5.5E9, 0, "MAXHold ", -30, "500 Hz")
    trace_get()
    meas_close()
    print('Program successfully ended.')
    print('Wrote trace data into', TRACE_FILE)
    exit()