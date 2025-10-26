from analyzer_sensing import Analyzer
from config_obj import Config
import numpy as np
from RIS import RIS

conf = Config(config_path = "config_test.json")

anal = Analyzer(conf)
print("Analyzer Created")
anal.write_str_with_opc('*RST')
anal.write_str_with_opc(f'FREQuency:CENTer {5.36E9}')
anal.write_str_with_opc(f'FREQuency:SPAN {102400000}')
anal.write_str_with_opc(f'BAND {10000}')
anal.write_str_with_opc(f'DISPlay:TRACe1:MODE WRITe')
anal.write_str_with_opc(f'DISPlay:WINDow:TRACe:Y:SCALe:RLEVel {-50}')
anal.write_str_with_opc(f'DET RMS')
anal.write_str_with_opc(f'SWE:COUNT {1}')
anal.write_str_with_opc(f'SWEep:TIME:AUTO 1')
swepnt = int(102400000/10000)
anal.write_str_with_opc(f'SWEep:POINts {swepnt}')
anal.write_str_with_opc('INITiate:CONTinuous OFF')
anal.write_str_with_opc('SWEep:TYPE FFT')
anal.write_str_with_opc(f'BWIDth:VIDeo {10000 * 10}')
mst = anal.query_float('SWEep:DUR?')
print(f'Measurement time: {mst} s')

tens = np.ones(swepnt) * 10

power = []

freq = anal.get_freq_range()

for n in range(256):
    

with open("temp_data.csv", "w+") as f:
    for fq in freq:
        f.write(str(fq)+";")
    f.write("\n")
    for i in range(100):
        power = anal.trace_get()
        for p in power:
            f.write(str(p)+";")
        f.write("\n")
    f.write("\n")
    f.close()

# for i in range(100):
#     p = anal.trace_get()
    # p = np.divide(p, tens)
    # p = np.power(tens, p)
    # power.append(np.mean(p))

# m_power = np.mean(power)
# std_power = np.std(power)

# # print(m_power)
# # print(std_power)

# print(10*np.log10(m_power))
# print(10*np.log10(std_power))
#print(std_power)
# print(np.mean(power))
# print(np.std(power))



# signal_span = 80000000

# for i in range(len())




