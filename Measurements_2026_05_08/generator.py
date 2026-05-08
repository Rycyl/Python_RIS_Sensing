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

    def __init__(self, config, phy_device = True):
        RsSmw.assert_minimum_version('5.0.44')
        self.resource = f'TCPIP::{config.IP_ADDRESS_GENERATOR}::{config.PORT_GENERATOR}::{config.CONNECTION_TYPE}'  # Resource string for the device
        if phy_device:
            try:
                RsSmw.__init__(self, self.resource, True, True, "SelectVisa='socket'")
                self.com_check()
            except TimeoutError or ConnectionAbortedError:
                print("[TIMEOUT ERROR] Check is  computer and generator is connected to the same local network. Then try again.")
                exit()
        else:
            RsSmw.__init__(self, self.resource, True, True, "Simulate=True, DriverSetup=No, SelectVisa='socket'")
            self.com_check()      


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

    def meas_prep_fOFMD(self, set, c_freq, cp_no_symbols, total_sub_car, sub_car_offset, seq_len, no_occ_sub):
        self.output.state.set_value(set)
        self.source.frequency.fixed.set_value(c_freq)

        self.source.bb.ofdm.set_modulation(mod_type=enums.C5Gmod.FOFDm)
        self.source.bb.ofdm.set_cp_symbols(cp_no_symbols)
        self.source.bb.ofdm.set_nsubcarriers(total_sub_car)
        self.source.bb.ofdm.set_offset(offset= sub_car_offset)
        self.source.bb.ofdm.set_seq_length(seq_len)
        self.source.bb.ofdm.set_noccupied(no_occ_sub)



if __name__ == "__main__":
    from config_obj import Config
    config = Config()
    Generator = Generator(config, False)
    print("Succeeded")