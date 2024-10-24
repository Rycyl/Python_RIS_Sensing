from analyzer_sensing import Analyzer
from generator import Generator
from config_obj import Config
from RIS import RIS
#import search_patterns
from search_patterns_by_element_obj_std_PK_task_CP_edit import Element_By_Element_Search_std_PK
import os

import numpy as np

from time import time, ctime, sleep
from bitstring import Bits, BitArray, BitStream, pack

config = Config()

if __name__ == "__main__":
    analyzer = Analyzer(config)
    generator = Generator(config)
    RIS = RIS(port='/dev/ttyUSB0')
    RIS.reset()
    filename = "pomiar_test_funkcji_std"
    trace_file = 'trace_file_group_mesures_PK_test_empty_room'
    path = os.getcwd()
    no_file_set = True
    i = 1
    while no_file_set:
        files = [f for f in os.listdir(path) if f.endswith('.csv')]
        for f in files:
            #print(filename + f"_{str(i)}" + '.csv')
            if filename + f"_{str(i)}" + '.csv' == f or trace_file + f"_{str(i)}" + '.csv' == f:
                print(f"File {f} already exists")
                i += 1
                continue
            else:
                filename = filename + f"_{str(i)}.csv"
                trace_file = trace_file + f"_{str(i)}.csv"
                no_file_set = False
                break
    # print(f"Filename: {filename}")
    # print(f"Trace file: {trace_file}")
    # sleep(10)
    Search_patterns = Element_By_Element_Search_std_PK(RIS, generator, analyzer, config, 4, 3, 3.0, 0.08, True, True, filename, False, trace_file, None, True)
    #sleep(10)
    Search_patterns.run()

    del Search_patterns
    generator.close()
    analyzer.close()
    exit()

# ### CHYBA ZROBIONE, NO ALE TO SIĘ OKAŻE PO ODPALENIU, składniowo mi nie krzyczy jak uruchamiam

        


