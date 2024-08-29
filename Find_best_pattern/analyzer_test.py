import analyzer_sensing
import generator
from RIS import RIS
#from RsSmw import *
import search_patterns
import numpy as np
from file_writer import file_write_single_power
from config_obj import Config
from time import time, ctime, sleep
from bitstring import Bits, BitArray, BitStream, pack
import threading
config = Config()

global start_time

global get_trace_time
get_trace_time = []

def get_trace():
    global POWER_REC
    POWER_REC = analyzer_sensing.trace_get()
    get_trace_time.append(time() - start_time)
    return

if __name__ == "__main__":
    
    RIS = RIS(port='/dev/ttyUSB0')
    RIS.reset()
    generator.com_check()
    analyzer_sensing.com_prep()
    analyzer_sensing.com_check()
    #sleep(120)
    '''
    search_patterns.find_best_pattern_element_wise_by_group_measures(RIS, config, 1, find_min=False, debug=True, trace_file='trace_file_group_1.csv')
    search_patterns.find_best_pattern_element_wise_by_group_measures(RIS, config, 2, find_min=False, debug=True, trace_file='trace_file_group_2.csv')
    search_patterns.find_best_pattern_element_wise_by_group_measures(RIS, config, 4, find_min=False, debug=True, trace_file='trace_file_group_44.csv')
    
    search_patterns.find_best_pattern_element_wise_by_group_measures(RIS, config, 1, find_min=False, debug=True, trace_file='trace_file_group_11.csv')
    search_patterns.find_best_pattern_element_wise_by_group_measures(RIS, config, 2, find_min=False, debug=True, trace_file='trace_file_group_22.csv')
    search_patterns.find_best_pattern_element_wise_by_group_measures(RIS, config, 4, find_min=False, debug=True, trace_file='trace_file_group_44.csv')
    '''
    combinations = (2 ** 1)

    RIS_change_time = 0.022
    Total_ris_changing_time = combinations * RIS_change_time
    
    config.update_swt(Total_ris_changing_time * 3) ## 1/3 danych jest niewiadomej reputacji teraz
    points = config.swepnt
    point_range = int( points // combinations )
    print("POINST TOTAL = ", points, "Point Range = ", point_range)

    delta_t = config.sweptime/points
    N_pts_delete = int((RIS_change_time / delta_t) //2)
    sleeptime = config.sweptime / combinations - 0.022 
    sleeptime2 = sleeptime + 0.022
    n = 0
    generator.meas_prep(True, config.generator_mode, config.generator_amplitude, config.freq)
    analyzer_sensing.meas_prep(config.freq, config.sweptime, config.span, config.analyzer_mode, config.detector, config.revlevel, config.rbw, config.swepnt) 
    idx_change = []
    slep_end_time = []
    start_time = time()
    
    while(n<100):
        MEASURE = threading.Thread(target=get_trace) #create thread MEASUREs
        
        RIS.set_pattern('0x0000000000000000000000000000000000000000000000000000000000000000')
        MEASURE.start()
        #sleep(0.04)
        sleep(sleeptime2)
        RIS.set_pattern('0x00f807f009f804f801f802f80bfe007e01f80af803fc04fe01fe42f025d0c17c')
        sleep(sleeptime)
        slep_end_time.append( time() - start_time)
        MEASURE.join()

        trace = POWER_REC
        std = np.std(trace[0:20])
        m1 = np.mean(trace[0:20])
        
        for x in range(0,len(trace)):
            #print(trace[x])
            if(m1 + 5< trace[x]  or trace[x] < m1 - 5): 
                idx_change.append(x)
                break
        n+=1
        print(n)

    file = open("log_analizator_proba_zmian_3.txt", 'a+')
    file.write(str(idx_change)[1:-1])

    mean = np.mean(idx_change)
    std2 = np.std(idx_change)
    max = np.max(idx_change)
    min = np.min(idx_change)
    file.write('\n')
    file.write('mean = ' + str(mean))
    file.write('\n')
    file.write('std = ' + str(std2))
    file.write('\n')
    file.write('max = ' + str(max))
    file.write('\n')
    file.write('min = ' + str(min))
    file.write('\n')    
    file.close()
    file_time = open('timings.csv', 'a+')
    print(get_trace_time)
    file_time.write(str(get_trace_time)[1:-1])
    file_time.write('\n')
    print(slep_end_time)
    file_time.write(str(slep_end_time)[1:-1])
    file_time.close()
    generator.close()
    analyzer_sensing.close()
    exit()

### CHYBA ZROBIONE, NO ALE TO SIĘ OKAŻE PO ODPALENIU, składniowo mi nie krzyczy jak uruchamiam

        


