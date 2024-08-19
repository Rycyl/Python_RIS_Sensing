import analyzer_sensing
import generator
from RIS import RIS
from RsSmw import *
import search_patterns
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
    
    while(i<8):
        config.update_swt(0.1)
        #search_patterns.find_best_pattern_codebook(RIS, config)
        search_patterns.find_best_pattern_element_wise(RIS, config, '0b1')
        search_patterns.find_best_pattern_element_wise_by_group_measures(RIS,config, 1)
        search_patterns.find_best_pattern_element_wise(RIS, config, '0b11')
        search_patterns.find_best_pattern_element_wise(RIS, config, '0b1010')
        config.update_swt(1)
        search_patterns.find_best_pattern_element_wise_by_group_measures(RIS,config, 1)
        search_patterns.find_best_pattern_element_wise_by_group_measures(RIS,config, 2)
        search_patterns.find_best_pattern_element_wise_by_group_measures(RIS,config, 3)
        search_patterns.find_best_pattern_element_wise_by_group_measures(RIS,config, 4)
        search_patterns.find_best_pattern_element_wise_by_group_measures(RIS,config, 5)
        search_patterns.find_best_pattern_element_wise_by_group_measures(RIS,config, 6)
        
        config.update_swt(0.5)
        search_patterns.find_best_pattern_element_wise_by_group_measures(RIS,config, 1)
        search_patterns.find_best_pattern_element_wise_by_group_measures(RIS,config, 2)
        search_patterns.find_best_pattern_element_wise_by_group_measures(RIS,config, 3)
        search_patterns.find_best_pattern_element_wise_by_group_measures(RIS,config, 4)
        search_patterns.find_best_pattern_element_wise_by_group_measures(RIS,config, 5)
        search_patterns.find_best_pattern_element_wise_by_group_measures(RIS,config, 6)
        i+=1
        sleep(3600.0)

    print("END SUCCESFULL ETA: ", time() - t1)
    print("ostatni uposledzony")
    t1 = time()
    config.update_swt(8)
    search_patterns.find_best_pattern_element_wise_by_group_measures(RIS,config, 8, trace_file='find_best_pattern_element_wise_by_group_measures_8sec_8bit.csv')
    print("STRESS END SUCCESFULL ETA: ", time() - t1)
    generator.close()
    analyzer_sensing.close()
    exit()

### CHYBA ZROBIONE, NO ALE TO SIĘ OKAŻE PO ODPALENIU, składniowo mi nie krzyczy jak uruchamiam

        


