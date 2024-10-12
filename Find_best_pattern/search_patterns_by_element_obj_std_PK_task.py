import analyzer_sensing
import generator
from RIS import RIS
import json
import numpy as np
from RsSmw import *
import time
from time import sleep
import def_pattern
from bitstring import Bits, BitArray, BitStream, pack
from copy import copy, deepcopy
import threading
from config_obj import Config
import file_writer
from copy import copy


class Element_By_Element_Search_std_PK:
    def __init__(self, RIS, GENERATOR, ANALYZER, CONFIG, N_ELEMENTS = 4, N_SIGMA = 3, TIME_SAFETY_MARGIN = 3.0, STD_TRS = 0.08, STD_CHECK_ON = True, DEBUG_FLAG = False, MEASURE_FILE = 'find_best_pattern_element_wise_by_group_measures_v2.csv', FIND_MIN = False, TRACE_FILE = 'trace_file_group_mesures.csv', TIME_FILE = None):
        self.RIS = RIS
        self.GENERATOR = GENERATOR
        self.ANALYZER = ANALYZER
        self.CONFIG = CONFIG
        self.N_ELEMENTS = N_ELEMENTS
        self.N_SIGMA = N_SIGMA
        self.TIME_SAFTY_MARGIN = TIME_SAFETY_MARGIN
        self.STD_TRS = STD_TRS
        self.STD_CHECK_ON = STD_CHECK_ON
        self.DEBUG_FLAG = DEBUG_FLAG
        self.MEASURE_FILE = MEASURE_FILE
        self.FIND_MIN = FIND_MIN
        self.TRACE_FILE = TRACE_FILE
        self.TIME_FILE = TIME_FILE
        self.RIS_change_time = 0.022
        self.combinations = 2 ** self.N_ELEMENTS
        self.pat_array, self.pat_array_copy = self.prepare_patterns()
        self.current_best_power = 1000.0 if self.FIND_MIN else -1000.0
        self.update_config_sweep_time()
        self.GENERATOR.meas_prep(True, self.CONFIG.generator_mode, self.CONFIG.generator_amplitude, self.CONFIG.freq)
        self.ANALYZER.meas_prep(self.CONFIG.freq, self.CONFIG.sweptime, self.CONFIG.span, self.CONFIG.analyzer_mode, self.CONFIG.detector, self.CONFIG.revlevel, self.CONFIG.rbw, self.CONFIG.swepnt)
        self.meas_file, self.t0, self.t1 = self.prepare_measurement_files()
        self.POWER_REC = None
        self.SLEEPTIME = (self.CONFIG.sweptime / len(self.pat_array) - self.RIS_change_time)
        self.point_range = self.CONFIG.swepnt // len(self.pat_array)
        self.N_pts_delete = int(10) * self.N_SIGMA
        
    def prepare_patterns(self):
        pat_array = [BitArray(uint=x, length=256) for x in range(self.combinations)]
        return pat_array, copy(pat_array)
    
    def update_config_sweep_time(self):
        Total_ris_changing_time = self.combinations * self.RIS_change_time * self.TIME_SAFTY_MARGIN
        self.CONFIG.update_swt(Total_ris_changing_time + 2 * self.RIS_change_time)
        return
    
    def prepare_measurement_files(self):
        file = open(self.MEASURE_FILE, 'a+')
        file.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "N_elements ," + str(self.N_ELEMENTS) + ", swt = ," + str(self.CONFIG.sweptime))
        file.write('\n')
        
        if self.TIME_FILE:
            t0 = []
            t1 = []
            return file, t0, t1
        return file, None, None
    
    def write_debug_info(self, n, power_debug, pattern_debug):
        with open (self.TRACE_FILE, 'a+') as trace_f:
            trace_f.write(f'"Grupowy pomiar N_el{self.N_ELEMENTS} 1szy opt elem w sekwencji={n}||SWT = {self.CONFIG.sweptime}||"\n')
            trace_f.write(f'{str(self.POWER_REC)[1:-1]}\n')
            trace_f.write(f'{str(power_debug)[1:-1]}\n')
            for napis in pattern_debug:
                trace_f.write(f'"{str(napis)}",')
            trace_f.write('\n')
    
    def get_trace(self):
        self.POWER_REC = self.ANALYZER.trace_get()
        return
    
    def measure_thread_with_RIS_changes(self):
        Measure = threading.Thread(target=self.get_trace)
        self.RIS.set_pattern('0x' + self.pat_array_copy[0].hex)
        Measure.start()
        sleep(0.06)
        sleep(0.022)
        for y in self.pat_array_copy[1:]:
            sleep(self.SLEEPTIME)
            self.RIS.set_pattern('0x' + y.hex)
        Measure.join()
        return
    
    def calculate_shift(self, power_slice, std, mean):
        minpow = min(power_slice)
        maxpow = max(power_slice)
        max_out = (maxpow > mean + std)
        min_out = (minpow < mean - std)
        
        if max_out:
            if power_slice.index(maxpow) < (self.point_range * 0.7):
                shift -= int(self.point_range * 0.07)
            else:
                shift += int(self.point_range * 0.03)
        else:
            if power_slice.index(minpow) < (self.point_range * 0.3):
                shift -= int(self.point_range * 0.07)
            else:
                shift += int(self.point_range * 0.03)
        
        return shift
    
    def measure_patterns(self):
        if self.DEBUG_FLAG:
            power_debug = [-150] * len(self.POWER_REC)
            pattern_debug = [None] * len(self.POWER_REC)
        else:
            power_debug = None
            pattern_debug = None
        powers = []
        stds_from_trace_shift_maxs = []
        stds_from_trace_shift = [[]]*len(self.pat_array)
        shift = 0
        for i in range(len(self.pat_array)):
            enum = 0
            while True:
                enum += 1
                start_pat = max(0, int(self.point_range * i + shift)) # self.N_pts_delete ))
                end_pat = min(len(self.POWER_REC), int(self.point_range * (i + 1) + shift )) #- self.N_pts_delete ))
                power_slice = self.POWER_REC[start_pat:end_pat]
                
                std = np.std(power_slice)
                mean = np.mean(power_slice)
                
                if self.DEBUG_FLAG:
                    print(f"STD:: {std}, mean:: {mean}, enum:: {enum}, len_power_slice:: {len(power_slice)}")
                
                '''    
                if std > self.STD_TRS and self.STD_CHECK_ON and enum < 20 and i == 0 and len(power_slice)>20:
                    shift = self.calculate_shift(power_slice, std, mean)
                    print(f"shift:: {shift}")
                    continue
                '''
                
                stds_from_trace_shift[i].append(std) #i-ty pattern, dodaj jego bierzące std
                

                if end_pat<len(self.POWER_REC):
                    shift += 1
                    continue

                powers.append(mean)
                if self.DEBUG_FLAG:
                    for xx in range(start_pat, end_pat):
                        power_debug[xx] = self.POWER_REC[xx]
                        pattern_debug[xx] = str(self.pat_array[i].hex)
                
                break #koniec while
        x = 0
        while (x < shift):
            stds = []
            for i in range(len(self.pat_array)):
                stds.append(stds_from_trace_shift[i][x])                
            stds_maxs.append(np.max(stds_from_trace_shifts))
            x+=1

        best_power = np.min(powers) if self.FIND_MIN else np.max(powers)
        best_idx = powers.index(best_power)
        
        return best_idx, best_power, power_debug, pattern_debug, powers
    
    def search(self):
        n = 0
        power_write = []
        pattern_write = []
        while n < 256:
            if self.TIME_FILE:
                self.t1.append(time.time())
            self.measure_thread_with_RIS_changes()
            if self.TIME_FILE:
                self.t0.append(time.time())
                
            best_idx, current_best_power, power_debug, pattern_debug, powers = self.measure_patterns()
            
            current_best_pattern = self.pat_array_copy[best_idx]
            
            power_write.extend(powers)
            
            for pat in self.pat_array_copy:
                pattern_write.append(pat.hex)
            
            if self.DEBUG_FLAG:
                print(f"Pat:: {current_best_pattern}, Pow:: {current_best_power}")
                self.write_debug_info(n, power_debug, pattern_debug)
            
            for i in range(len(self.pat_array)):
                self.pat_array[i].rol(self.N_ELEMENTS)
                self.pat_array_copy[i] = self.pat_array[i] | current_best_pattern
            
            n += self.N_ELEMENTS
        
        self.meas_file.write(f"{str(pattern_write)[1:-1]}\n{str(power_write)[1:-1]}\n\n")
        
        if self.TIME_FILE:
            with open (f"{self.TIME_FILE}.csv", 'a+') as timefile:
                timefile.write(str(self.t0)[1:-1])
                timefile.write('\n')
                timefile.write(str(self.t1)[1:-1])
                timefile.close()
