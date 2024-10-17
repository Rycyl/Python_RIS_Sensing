from analyzer_sensing import Analyzer
from generator import Generator
from config_obj import Config
from RIS import RIS
#import search_patterns
from search_patterns_by_element_obj_std_PK_task import Element_By_Element_Search_std_PK

import numpy as np

from time import time, ctime, sleep
from bitstring import Bits, BitArray, BitStream, pack

config = Config()

if __name__ == "__main__":
    analyzer = Analyzer(config)
    generator = Generator(config)
    RIS = RIS(port='/dev/ttyUSB0')
    RIS.reset()
    Search_patterns = Element_By_Element_Search_std_PK(RIS, generator, analyzer, config, 4, 3, 3.0, 0.08, True, True, 'find_best_pattern_element_wise_by_group_measures_PK_test_empty_room.csv', False, 'trace_file_group_mesures_PK_test_empty_room.csv', None)
    sleep(10)
    Search_patterns.run()

#     search_patterns.find_best_pattern_element_wise_by_group_measures(RIS, generator, analyzer, config, 4, FIND_MIN=False, DEBUG_FLAG=True, TRACE_FILE='trace_file_group_4.csv')
    del Search_patterns
    generator.close()
    analyzer.close()
    exit()

# ### CHYBA ZROBIONE, NO ALE TO SIĘ OKAŻE PO ODPALENIU, składniowo mi nie krzyczy jak uruchamiam

        


