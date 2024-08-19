import analyzer_sensing
import generator
from RIS import RIS
from RsSmw import *
import search_patterns
from file_writer import file_write_single_power
from config_obj import Config
from time import time, ctime, sleep
from bitstring import Bits, BitArray, BitStream, pack

config = Config()

if __name__ == "__main__":

    RIS = RIS(port='/dev/ttyUSB0')
    RIS.reset()
    generator.com_check()
    analyzer_sensing.com_prep()
    analyzer_sensing.com_check()
    t1 = time()
    search_patterns.find_best_pattern_element_wise_by_group_measures(RIS,config)
    print(time() - t1)
  
    generator.close()
    analyzer_sensing.close()
    exit()

### CHYBA ZROBIONE, NO ALE TO SIĘ OKAŻE PO ODPALENIU, składniowo mi nie krzyczy jak uruchamiam

        


