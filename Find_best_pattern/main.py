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
    #sleep(120)
    '''
    search_patterns.find_best_pattern_element_wise_by_group_measures(RIS, config, 1, find_min=False, debug=True, trace_file='trace_file_group_1.csv')
    search_patterns.find_best_pattern_element_wise_by_group_measures(RIS, config, 2, find_min=False, debug=True, trace_file='trace_file_group_2.csv')
    search_patterns.find_best_pattern_element_wise_by_group_measures(RIS, config, 4, find_min=False, debug=True, trace_file='trace_file_group_44.csv')
    
    search_patterns.find_best_pattern_element_wise_by_group_measures(RIS, config, 1, find_min=False, debug=True, trace_file='trace_file_group_11.csv')
    search_patterns.find_best_pattern_element_wise_by_group_measures(RIS, config, 2, find_min=False, debug=True, trace_file='trace_file_group_22.csv')
    search_patterns.find_best_pattern_element_wise_by_group_measures(RIS, config, 4, find_min=False, debug=True, trace_file='trace_file_group_44.csv')
    '''
    RIS.set_pattern('0x00f807f009f804f801f802f80bfe007e01f80af803fc04fe01fe42f025d0c17c')

    search_patterns.find_best_pattern_element_wise_by_group_measures(RIS, config, 4, find_min=False, debug=True, trace_file='trace_file_group_444444.csv')

    generator.close()
    analyzer_sensing.close()
    exit()

### CHYBA ZROBIONE, NO ALE TO SIĘ OKAŻE PO ODPALENIU, składniowo mi nie krzyczy jak uruchamiam

        


