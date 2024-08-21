import analyzer_sensing
import generator
from RIS import RIS
#from RsSmw import *
import search_patterns
import numpy as np
from file_writer import file_write_single_power
from config_obj import Config
from time import time, ctime, sleep
from bitstring import Bits, BitArray, BitStream, pack

config = Config()

if __name__ == "__main__":

    RIS = RIS(port='/dev/ttyUSB0')
    RIS.reset()
    generator.com_check()
    analyzer_sensing.com_prep()
    analyzer_sensing.com_check()
 
    i = 0

    t = []
    pat=[]
    #sleep(10)
    while(i<100):
        config.update_swt(0.1)
        #pat.append(search_patterns.find_best_pattern_element_wise(RIS, config, find_min=True)[0])
        #pat.append(search_patterns.find_best_pattern_element_wise(RIS, config)[0])
        #pat3, pat4 = search_patterns.find_best_pattern_codebook(RIS=RIS, config=config)
        #pat.append(search_patterns.find_best_pattern_element_wise_by_group_measures(RIS, config, 2, find_min=True)[0])
        #pat.append(search_patterns.find_best_pattern_element_wise_by_group_measures(RIS, config, 2, find_min=False)[0])
        config.update_swt(0.1)
        #RIS.set_pattern(pat3)
        #print("Pow result ", analyzer_sensing.trace_get_mean())
        #RIS.set_pattern(pat4)
        #print("Pow result ", analyzer_sensing.trace_get_mean())
        
        RIS.set_pattern('0x' + '043f24bf2b98442c442b47eb021b041f107b00eb40db047f1107447c413b1138')
        #    print(x.hex)
        print("Pow result ", analyzer_sensing.trace_get_mean())
        i+=1
        #config.update_swt(0.1)
        #search_patterns.find_best_pattern_codebook(RIS, config)
        #sleep(5)



    generator.close()
    analyzer_sensing.close()
    exit()

### CHYBA ZROBIONE, NO ALE TO SIĘ OKAŻE PO ODPALENIU, składniowo mi nie krzyczy jak uruchamiam

        


