from RsSmw import *

class Generator_Virtual():
    def __init__(self, resource_name: str, id_query: bool = True, reset: bool = False, options: str = None, direct_session: object = None):
        print("Connected to VIRTUAL Signal Generator")
        return

    def com_check(self):
        print("Hello, I'm a VIRTUAL Signal Generator")
        return
    
    def meas_prep(self, set, mode, amplitude : int, freq : int):
        print(f"Updated Virt Gen Setup: {set}, {mode}, {amplitude}")
        return







class Generator(RsSmw):

    def __init__(self, config):
        RsSmw.assert_minimum_version('5.0.44')
        self.resource = f'TCPIP::{config.IP_ADDRESS_GENERATOR}::{config.PORT_GENERATOR}::{config.CONNECTION_TYPE}'  # Resource string for the device
        self.visa_timeout = 5000  # Ustaw timeout na 5 sekund
        try:
            RsSmw.__init__(self, self.resource, True, True, "SelectVisa='socket'")
            self.com_check()
        except TimeoutError or ConnectionAbortedError:
            print("[TIMEOUT ERROR] Check is  computer and generator is connected to the same local network. Then try again.")
            i = True
            while(i):
                i = input("Create virtual generator? [Y/n]?")
                if i == 'Y' or i == 'y':
                    Generator_Virtual.__init__(self, self.resource, True, True, "SelectVisa='socket'")
                    break
                if i == 'N' or i == 'n':
                    exit()
                    break
        


    def com_check(self):
        self.visa_timeout = 500000  
        self.opc_timeout = 3000 
        self.utilities.instrument_status_checking = True
        self.repcap_hwInstance_set(repcap.HwInstance.InstA)


    def meas_prep(self, set, mode, amplitude : int, freq : int):
        self.output.state.set_value(set)
        self.source.frequency.set_mode(mode)
        self.source.power.level.immediate.set_amplitude(amplitude)
        self.source.frequency.fixed.set_value(freq)
        print(f'Channel 1 PEP level: {self.source.power.get_pep()} dBm')
        response = self.utilities.query_str('*IDN?')
        print(f'Direct SCPI response on *IDN?: {response}')