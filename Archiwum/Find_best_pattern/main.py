from analyzer_sensing import Analyzer
from generator import Generator
from config_obj import Config
from RIS import RIS
#import search_patterns
#from search_patterns_by_element_obj_std_PK_task_CP_edit import Element_By_Element_Search_std_PK
from search_patterns_by_element_obj_std_PK_task_V3 import Element_By_Element_Search_std_PK
import os
import search_patterns 
from plot_trace import run_all, run_main

import numpy as np

from time import time, ctime, sleep
from bitstring import Bits, BitArray, BitStream, pack

config = Config()

config.update_swt(0.06)

def create_trace_file(trace_file_name):
    i = 1
    while True:
        filename = f"{trace_file_name}_{i}.csv"
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                file.close()
            return filename
        else:
            i += 1
if __name__ == "__main__":
    analyzer = Analyzer(config)
    generator = Generator(config)
    RIS = RIS(port='/dev/ttyUSB0')
    RIS.reset()
    filename = "Test_opóźnień"
    trace_file = 'trace_file_group_mesures_test_opóźnień'

    # filename = create_trace_file(filename)
    # trace_file = create_trace_file(trace_file)
    # Search_patterns = Element_By_Element_Search_std_PK(RIS, generator, analyzer, config, 4, 3, 3.0, 0.08, True, True, filename, False, trace_file, None)
    # #sleep(10)
    # Search_patterns.run()
    search_patterns.find_best_pattern_codebook(RIS, generator, analyzer, config, 'tset.csv')
    # del Search_patterns
    generator.close()
    analyzer.close()
    #run_main(trace_file)
    exit()

# ### CHYBA ZROBIONE, NO ALE TO SIĘ OKAŻE PO ODPALENIU, składniowo mi nie krzyczy jak uruchamiam

        


