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
    sleep(240)
    while(i<8):
        config.update_swt(0.1)
        pat.append(search_patterns.find_best_pattern_element_wise(RIS, config, find_min=True)[0])
        pat.append(search_patterns.find_best_pattern_element_wise(RIS, config)[0])
        pat.append(search_patterns.find_best_pattern_codebook(RIS=RIS, config=config))
        pat.append(search_patterns.find_best_pattern_element_wise_by_group_measures(RIS, config, 1, find_min=True)[0])
        pat.append(search_patterns.find_best_pattern_element_wise_by_group_measures(RIS, config, 1, find_min=False)[0])
        pat.append(search_patterns.find_best_pattern_element_wise_by_group_measures(RIS, config, 2, find_min=True)[0])
        pat.append(search_patterns.find_best_pattern_element_wise_by_group_measures(RIS, config, 2, find_min=False)[0])
        pat.append(search_patterns.find_best_pattern_element_wise_by_group_measures(RIS, config, 4, find_min=True)[0])
        pat.append(search_patterns.find_best_pattern_element_wise_by_group_measures(RIS, config, 4, find_min=False)[0])
        i+=1
        sleep(3600)

    with open('znalezione_patterny.txt', "a+") as file:
        for data in pat:
            print(data)
            file.write(str(data))
            file.write("\n")
        file.close()
        

    generator.close()
    analyzer_sensing.close()
    exit()

### CHYBA ZROBIONE, NO ALE TO SIĘ OKAŻE PO ODPALENIU, składniowo mi nie krzyczy jak uruchamiam

        


