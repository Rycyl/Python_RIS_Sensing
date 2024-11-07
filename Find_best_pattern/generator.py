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
        i = True
        while(i):
            i = input("Create simulated device? [Y/n]?")
            if i == 'Y' or i == 'y':
                RsSmw.__init__(self, self.resource, True, True, "Simulate=True, DriverSetup=No, SelectVisa='socket'")
                self.com_check()
                break
            if i == 'N' or i == 'n':
                try:
                    RsSmw.__init__(self, self.resource, True, True, "SelectVisa='socket'")
                    self.com_check()
                except TimeoutError or ConnectionAbortedError:
                    print("[TIMEOUT ERROR] Check is  computer and generator is connected to the same local network. Then try again.")
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


# class Generator():
#     def __init__(self, config):
#         RsSmw.assert_minimum_version('5.0.44')
#         self.resource = f'TCPIP::{config.IP_ADDRESS_GENERATOR}::{config.PORT_GENERATOR}::{config.CONNECTION_TYPE}'
#         try: