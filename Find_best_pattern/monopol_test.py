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

    mes_file_name = 'anntena_test_14_11_omni_no_LOS_pos_2'
    sleep(60)
    for i in range(1, 8):
        mes_file = mes_file_name + '_' + str(i) + '.csv'

        best_pattern, best_power = search_patterns.find_best_pattern_element_wise(ris, generator, analyzer, config, MEASURE_FILE =  mes_file, FIND_MIN = False)

        with open(mes_file, 'a') as file:
            file.write('best pattern')
            file.write('\n')
            file.write(str(best_power) + ",")
            file.write(str(best_pattern))
            file.write('\n')
            file.close()

        mes_file_min = mes_file[:-4] + '_min.csv'

        best_pattern_min, best_power_min = search_patterns.find_best_pattern_element_wise(ris, generator, analyzer, config, MEASURE_FILE =  mes_file_min, FIND_MIN = True)

        with open(mes_file_min, 'a') as file:
            file.write('best pattern')
            file.write('\n')
            file.write(str(best_power_min) + ",")
            file.write(str(best_pattern_min))
            file.write('\n')
            file.close()
        sleep(600) # 10 min
        #break

    generator.close()
    analyzer.close()
    exit()