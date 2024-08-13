from RsSmw import *
import json

try:
    with open ("config_sensing.json") as config_f:
        RsSmw.assert_minimum_version('5.0.44')
        config = json.load(config_f)
        IP_ADDRESS_GENERATOR = config["IP_ADDRESS_GENERATOR"]
        PORT = config["PORT"]
        CONNECTION_TYPE = config["CONNECTION_TYPE"]
        TRACE_FILE = config["TRACE_FILE"] 
        MEASURE_TIME = config["MEASURE_TIME"]
        resource = f'TCPIP::{IP_ADDRESS_GENERATOR}::{PORT}::{CONNECTION_TYPE}'  # Resource string for the device
        try:
            generator = RsSmw(resource, True, True, "SelectVisa='socket'")   
        except TimeoutError or ConnectionAbortedError:
            print("[TIMEOUT ERROR] Check is  computer and generator is connected to the same local network. Then try again.")
            exit()
        config_f.close()
except FileNotFoundError:
    print("Brak pliku konfiguracyjnego.")
    exit()

def com_check():
    generator.visa_timeout = 500000  
    generator.opc_timeout = 3000 
    generator.utilities.instrument_status_checking = True
    generator.repcap_hwInstance_set(repcap.HwInstance.InstA)


def meas_prep(set : True, mode, amplitude : int, freq : int):
    generator.output.state.set_value(set)
    generator.source.frequency.set_mode(mode)
    generator.source.power.level.immediate.set_amplitude(amplitude)
    generator.source.frequency.fixed.set_value(freq)
    print(f'Channel 1 PEP level: {generator.source.power.get_pep()} dBm')
    response = generator.utilities.query_str('*IDN?')
    print(f'Direct SCPI response on *IDN?: {response}')

def close():
    generator.close()

if __name__ == "__main__":
    com_check()
    meas_prep(True, enums.FreqMode.CW, -10, 5.5E9)
    exit()
