from analyzer_sensing import Analyzer
from generator import Generator
from config_obj import Config
from RIS import RIS
#import search_patterns
from search_patterns_by_element_obj_std_PK_task_CP_edit import Element_By_Element_Search_std_PK
import os
import search_patterns 

import numpy as np

from time import time, ctime, sleep
from bitstring import Bits, BitArray, BitStream, pack

config = Config()

if __name__ == "__main__":
    analyzer = Analyzer(config)
    generator = Generator(config)
    RIS = RIS(port='/dev/ttyUSB0')
    RIS.reset()
    Search_patterns = Element_By_Element_Search_std_PK(RIS, generator, analyzer, config, N_ELEMENTS = 4, N_SIGMA = 3, TIME_SAFETY_MARGIN = 3.0, STD_TRS = 0.08, STD_CHECK_ON = True, DEBUG_FLAG = False, MEASURE_FILE = 'find_best_pattern_element_wise_by_group_measures_v2.csv', FIND_MIN = False, TRACE_FILE = 'trace_file_group_mesures.csv', TIME_FILE = None)
    Search_patterns.prepare_patterns()
    Search_patterns.measure_thread_with_RIS_changes()
    Trace = Search_patterns.POWER_REC
    ## dodać zapis do pliku ## 
   
    generator.close()
    analyzer.close()
    exit()

# ### CHYBA ZROBIONE, NO ALE TO SIĘ OKAŻE PO ODPALENIU, składniowo mi nie krzyczy jak uruchamiam

        


