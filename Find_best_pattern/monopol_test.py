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

if __name__ == "__main__":
    ris = RIS(port='/dev/ttyUSB0')
    ris.reset()
    config = Config()
    analyzer = Analyzer(config)
    generator = Generator(config)

    search_patterns.find_best_pattern_element_wise(ris, generator, analyzer, config, MEASURE_FILE =  'monopol_test_on_level_further_min.csv', FIND_MIN = True)

    generator.close()
    analyzer.close()
    exit()