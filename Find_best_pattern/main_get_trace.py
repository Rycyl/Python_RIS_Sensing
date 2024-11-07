from analyzer_sensing import Analyzer
from generator import Generator
from config_obj import Config
from RIS import RIS
#import search_patterns
from search_patterns_by_element_obj_std_PK_task_CP_edit import Element_By_Element_Search_std_PK
import os
#import search_patterns 
from save_trace_file import create_trace_file_header, write_trace_file

import numpy as np

from time import time, ctime, sleep
from bitstring import Bits, BitArray, BitStream, pack

config = Config()

if __name__ == "__main__":
    start = time()
    file_name = "Trace_for_virtual_analyzer"
    n_elemets = 4
    analyzer = Analyzer(config)
    generator = Generator(config)
    ris = RIS(port='/dev/ttyUSB0')
    ris.reset()
    Search_patterns = Element_By_Element_Search_std_PK(ris, generator, analyzer, config, N_ELEMENTS = n_elemets, N_SIGMA = 3, TIME_SAFETY_MARGIN = 3.0, STD_TRS = 0.08, STD_CHECK_ON = True, DEBUG_FLAG = False, MEASURE_FILE = 'find_best_pattern_element_wise_by_group_measures_v2.csv', FIND_MIN = False, TRACE_FILE = 'trace_file_group_mesures.csv', TIME_FILE = None)
    swt = Search_patterns.CONFIG.sweptime
    created_filename = create_trace_file_header(file_name, swt, n_elemets)
    #Search_patterns.prepare_patterns()
    for i in range(10):
        #sleep(10)
        Search_patterns.pat_array, Search_patterns.pat_array_copy = Search_patterns.prepare_random_patterns()
        Search_patterns.measure_thread_with_RIS_changes()
        Trace = Search_patterns.POWER_REC
        write_trace_file(created_filename, Trace)
    ## dodać zapis do pliku ## 
    print(f"Time elapsed: {time() - start}")
    generator.close()
    analyzer.close()
    Search_patterns.__del__()
    exit()

# ### CHYBA ZROBIONE, NO ALE TO SIĘ OKAŻE PO ODPALENIU, składniowo mi nie krzyczy jak uruchamiam

        


