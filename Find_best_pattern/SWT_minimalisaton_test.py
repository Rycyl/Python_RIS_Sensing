from analyzer_sensing import Analyzer
from generator import Generator
from config_obj import Config
from RIS import RIS
import search_patterns
import plot_trace
from time import sleep
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
    print(swt_vals)
    swt_vals =  np.around(swt_vals, decimals=2)

    x = 0
    sigma = 3
    
    config.update_swt(0.1)
    sleep(30)
    search_patterns.find_best_pattern_element_wise(RIS=ris, ANALYZER=analyzer, GENERATOR=generator, CONFIG=config)
    
    for swt_val in swt_vals:
        if(swt_val < 1.5):
            sigma = 2
        else:
            sigma = 3
        search_patterns.find_best_pattern_element_wise_by_group_measures(ris, generator, analyzer, config, 4, N_SIGMA=sigma, STD_CHECK_ON=False ,MEASURE_FILE= f'find_best_pattern_element_wise_by_group_measures_swt_test_v2_{x}.csv' , FIND_MIN=False, DEBUG_FLAG=True, TRACE_FILE=f'trace_file_group_swt_test{x}.csv', time_safety_margin = swt_val)
        x += 1

    config.update_swt(0.1)
    search_patterns.find_best_pattern_element_wise(RIS=ris, ANALYZER=analyzer, GENERATOR=generator, CONFIG=config)
    
    plot_trace.run_all()
    
    generator.close()
    analyzer.close()
    exit()