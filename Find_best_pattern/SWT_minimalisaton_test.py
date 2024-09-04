from analyzer_sensing import Analyzer
from generator import Generator
from config_obj import Config
from RIS import RIS
import search_patterns
import plot_trace

import numpy as np

# from time import time, ctime, sleep
# from bitstring import Bits, BitArray, BitStream, pack

config = Config()

if __name__ == "__main__":
    analyzer = Analyzer(config)
    generator = Generator(config)
    ris = RIS(port='/dev/ttyUSB0')
    ris.reset()

    swt_vals = np.linspace(3.0, 1.0 , num = 10)

    swt_vals =  np.around(swt_vals, decimals=2)

    x = 0

    for swt_val in swt_vals:
        search_patterns.find_best_pattern_element_wise_by_group_measures(ris, Generator, Analyzer, config, 4, MEASURE_FILE= f'find_best_pattern_element_wise_by_group_measures_swt_test_{x}.csv' , FIND_MIN=False, DEBUG_FLAG=True, TRACE_FILE=f'trace_file_group_swt_test{x}.csv', swt_val = swt_val)
        x += 1

    plot_trace.run_all()

    generator.close()
    analyzer.close()
    exit()