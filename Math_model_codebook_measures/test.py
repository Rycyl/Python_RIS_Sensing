# from analyzer_sensing import Analyzer
# from config_obj import Config
# import numpy as np
# from RIS import RIS
# import time

# conf = Config(config_path = "config_test.json")
# rbw = 50000
# span = 102400000
# anal = Analyzer(conf)
# print("Analyzer Created")
# anal.write_str_with_opc('*RST')
# anal.write_str_with_opc(f'FREQuency:CENTer {5.36E9 - (rbw/2)}')
# anal.write_str_with_opc(f'FREQuency:SPAN {span}')
# anal.write_str_with_opc(f'BAND {rbw}')
# anal.write_str_with_opc(f'DISPlay:TRACe1:MODE WRITe')
# anal.write_str_with_opc(f'DISPlay:WINDow:TRACe:Y:SCALe:RLEVel {-50}')
# anal.write_str_with_opc(f'DET RMS')
# anal.write_str_with_opc(f'SWE:COUNT {1}')
# anal.write_str_with_opc(f'SWEep:TIME:AUTO 1')
# swepnt = int(span/rbw)
# anal.write_str_with_opc(f'SWEep:POINts {swepnt}')
# anal.write_str_with_opc('INITiate:CONTinuous OFF')
# anal.write_str_with_opc('SWEep:TYPE FFT')
# anal.write_str_with_opc(f'BWIDth:VIDeo {rbw * 10}')
# mst = anal.query_float('SWEep:DUR?')
# print(f'Measurement time: {mst} s')

# tens = np.ones(swepnt) * 10

# power = []

# freq = anal.get_freq_range()
# #print(freq)
# # for n in range(256):
# ris = RIS("COM5", set_wait_time=0.000001)

# with open("temp_data_cfreq_p_half_rbw_no_synch_50_test_w_RIS5.csv", "w+") as f:
#     for fq in freq:
#         f.write(str(fq)+";")
#     f.write("\n")
#     for i in range(11):
#         ris.set_pattern("0x0000000000000000000000000000000000000000000000000000000000000000")
#         time.sleep(0.0023*i)
#         power = anal.trace_get()
#         ris.set_pattern("0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
#         for p in power:
#             f.write(str(p)+";")
#         f.write("\n")
#     f.write("\n")
#     f.close()

# # for i in range(100):
# #     p = anal.trace_get()
#     # p = np.divide(p, tens)
#     # p = np.power(tens, p)
#     # power.append(np.mean(p))

# # m_power = np.mean(power)
# # std_power = np.std(power)

# # # print(m_power)
# # # print(std_power)

# # print(10*np.log10(m_power))
# # print(10*np.log10(std_power))
# #print(std_power)
# # print(np.mean(power))
# # print(np.std(power))



# # signal_span = 80000000

# # for i in range(len())



print(type("L"))
print(type(["L"]))

if type(["L"]) == list:
    print("TAK")
