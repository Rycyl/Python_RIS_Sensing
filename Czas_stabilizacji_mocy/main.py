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

config = Config()

if __name__ == "__main__":
    sweeptime_l = 0.001
    RIS = RIS(port='/dev/ttyUSB0')
    RIS.reset()
    generator.com_check()
    analyzer_sensing.com_prep()
    analyzer_sensing.com_check()
    generator.meas_prep(True, config.generator_mode, config.generator_amplitude, config.freq)

    i = 0
    ##prepare trace file
    current_pattern = BitArray(length=256) ## all zeros
    element_on1 = randint(0, 255)
    element_on2 = randint(0, 255)
    element_on3 = randint(0, 255)
    """
    file = open(config.trace_file, 'a+')
    file.write((str(ctime(time()))) + ',')
    file.write("SWT(ms), in 1st row, Iters, in 1st col, \n")#HEADER
    file.write("patterns:, all off," + str(element_on1) + " el on," + str(element_on2) + " el on," + str(element_on3) + " el on, \n" )
    file.write(" ,1,1,1,1,2,2,2,2,4,4,4,4,8,8,8,8,16,16,16,16,32,32,32,32,64,64,64,64,128,128,128,128,256,256,256,256,512,512,512,512,1024,1024,1024,1024,")
    file.write('\n')

    analyzer_sensing.meas_prep(config.freq, sweeptime_l, config.span, config.analyzer_mode, config.detector, config.revlevel, config.rbw, config.swepnt)
    iters = 100
    sleep(20)
    while(i < iters): # 100 pomiarów na jednym sweeptime
        sweeptime_l = 0.001
        file.write(str(i) + ",")
        print("Iteration: ", i)
        while(sweeptime_l < 0.6):
            analyzer_sensing.meas_prep(config.freq, sweeptime_l, config.span, config.analyzer_mode, config.detector, config.revlevel, config.rbw, config.swepnt)
            RIS.set_pattern('0x' + current_pattern.hex)
            p1 = analyzer_sensing.trace_get_mean()

            current_pattern.overwrite('0b1', element_on1)
            RIS.set_pattern('0x' + current_pattern.hex)
            p2 = analyzer_sensing.trace_get_mean()
            current_pattern.overwrite('0b0', element_on1)

            current_pattern.overwrite('0b1', element_on2)
            RIS.set_pattern('0x' + current_pattern.hex)
            p3 = analyzer_sensing.trace_get_mean()
            current_pattern.overwrite('0b0', element_on2)

            current_pattern.overwrite('0b1', element_on3)
            RIS.set_pattern('0x' + current_pattern.hex)
            p4 = analyzer_sensing.trace_get_mean()
            current_pattern.overwrite('0b0', element_on3)

            file.write(str(p1) + "," + str(p2) + "," + str(p3) + "," + str(p4) + ",")
            sweeptime_l *= 2

        i += 1
        file.write('\n')
    file.close()
    """
    ##### DRUGI POMIAR
    analyzer_sensing.meas_prep(config.freq, 1, config.span, config.analyzer_mode, config.detector, config.revlevel, config.rbw, 12500)
    RIS.reset()
    
    # Uruchom nowy wątek
    n=0
    file2 = open("Ris_przelacz_w_czasie_tracea.csv", 'a+')
    sleep(20)
    while(n<20):
        RIS.set_pattern("0x0000000000000000000000000000000000000000000000000000000000000000")
        thread = threading.Thread(target=get_trace)
        thread.start() # w czasie pomiaru w wątku przełączamy RISA co 0.25s
        sleep(0.25)
        RIS.set_pattern("0xFFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000")
        sleep(0.25)
        RIS.set_pattern("0x8000000000000000000000000000000000000000000000000000000000000000")
        sleep(0.25)
        RIS.set_pattern("0x0000000000000000FFFFFFFFFFFFFFFF0000000000000000FFFFFFFFFFFFFFFF")
        
        # Poczekaj na zakończenie wątku
        thread.join()
        
        # Zapisz wynik
        file2.write((str(POWER_REC))[1:-1])
        file2.write('\n')
        n+=1
    file2.close()
    analyzer_sensing.meas_close()
    generator.meas_close()
    exit()
