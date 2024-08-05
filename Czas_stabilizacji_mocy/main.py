import analyzer_sensing
import generator
from RIS import RIS
from RsSmw import *
import search_patterns
from file_writer import file_write_single_power
from config_obj import Config
from time import time, ctime, sleep
from bitstring import Bits, BitArray, BitStream, pack
from random import randint
import threading

def get_trace():
    global POWER_REC
    POWER_REC = analyzer_sensing.trace_get()

def single_power_measurement(pattern):
    RIS.set_pattern(pattern)
    power = analyzer_sensing.trace_get_mean()
    return power

config = Config()

if __name__ == "__main__":
    #------------------------------------
    # Zmienne konfiguracyjne
    swt = 1
    points = 12500
    iters = 10
    trace_file = 'long_vs_normal_trace.csv'
    #------------------------------------

    RIS = RIS(port='/dev/ttyUSB0')
    RIS.reset()
    generator.com_check()
    analyzer_sensing.com_prep()
    analyzer_sensing.com_check()
    generator.meas_prep(True, config.generator_mode, config.generator_amplitude, config.freq)
    analyzer_sensing.meas_prep(config.freq, swt, config.span, config.analyzer_mode, config.detector, config.revlevel, config.rbw, points) 
    #test funkcji do odczytania mocy z długiego trace vs normalny pomiar
    file = open(trace_file, 'a+')
    #sleep(20)
    thread = threading.Thread(target=get_trace)
    n = 0
    centr_of_pat_trace = (points/4)/2
    point_range = (centr_of_pat_trace*5)//100
    test_patterns = ['0x0000000000000000000000000000000000000000000000000000000000000000', '0x8000000000000000000000000000000000000000000000000000000000000000', '0xC000000000000000000000000000000000000000000000000000000000000000', '0x4000000000000000000000000000000000000000000000000000000000000000']
    while(n < iters):
        RIS.set_pattern(test_patterns[0])
        thread.start()
        #Dodatkowy sleep żeby poczekać na start pomiaru ??
        sleep(swt/4)
        RIS.set_pattern(test_patterns[1])
        sleep(swt/4)
        RIS.set_pattern(test_patterns[2])
        sleep(swt/4)
        RIS.set_pattern(test_patterns[3])
        #zmiana elementów - kod greya
        thread.join()
        #centr_of_pat_trace = POWER_REC.len()/2
        controll_power_mes = []
        for pattern in test_patterns:
            power = single_power_measurement(pattern)
            controll_power_mes.append(power)
            #file.write(str(power) + ',')
            #file.write('\n')
        
        power_reading = []
        for i in range (1, 5):
            new_centre = centr_of_pat_trace*i
            power_slice = POWER_REC[new_centre-point_range:new_centre+point_range]
            power = power_slice.mean()
            power_reading.append(power)
        file.write((str(POWER_REC))[1:-1])
        file.write('\n')
        file.write((str(power_reading))[1:-1])
        file.write('\n')
        file.write((str(controll_power_mes))[1:-1])
        file.write('\n')
        n += 1
    file.write('\n')
    file.close()
    generator.com_close()
    analyzer_sensing.com_close()
    exit()



        


