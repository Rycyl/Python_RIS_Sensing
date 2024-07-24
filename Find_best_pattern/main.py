import analyzer_sensing
import generator
from RIS import RIS
from RsSmw import *
import search_patterns

if __name__ == "__main__":
    ##time.sleep(20)
    RIS = RIS(port='/dev/ttyUSB0')

    RIS.reset()
    generator.com_check()
    analyzer_sensing.com_prep()
    analyzer_sensing.com_check()
    i = 0
    brekpoint = 1
    while(i<brekpoint):
        i+=1
        print("Iteration: ", i)
        print(search_patterns.find_best_pattern_element_wise(RIS, mask='0b110000000000000011'))

    analyzer_sensing.meas_close()
    generator.meas_close()