from RsSmw import *

RsSmw.assert_minimum_version('5.0.44')
smw = RsSmw('TCPIP::192.168.0.30::5025::SOCKET', True, True, "SelectVisa=SocketIo")

# Driver's instrument status checking ( SYST:ERR? ) after each command (default value is True):
smw.utilities.instrument_status_checking = True

# The smw object uses the global HW instance one - RF out A
smw.repcap_hwInstance_set(repcap.HwInstance.InstA)


smw.output.state.set_value(True)
smw.source.frequency.set_mode(enums.FreqMode.CW)
smw.source.power.level.immediate.set_amplitude(-20)
smw.source.frequency.fixed.set_value(23E9)
print(f'Channeel 1 PEP level: {smw.source.power.get_pep()} dBm')


# Direct SCPI interface:
response = smw.utilities.query_str('*IDN?')
print(f'Direct SCPI response on *IDN?: {response}')
smw.close()
