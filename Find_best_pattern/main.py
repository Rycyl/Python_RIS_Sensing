from analyzer_sensing import Analyzer
from generator import Generator
from config_obj import Config
from RIS import RIS
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

    search_patterns.find_best_pattern_element_wise_by_group_measures(RIS, generator, analyzer, config, 4, FIND_MIN=False, DEBUG_FLAG=True, TRACE_FILE='trace_file_group_4.csv')

    generator.close()
    analyzer.close()
    exit()

### CHYBA ZROBIONE, NO ALE TO SIĘ OKAŻE PO ODPALENIU, składniowo mi nie krzyczy jak uruchamiam

        


