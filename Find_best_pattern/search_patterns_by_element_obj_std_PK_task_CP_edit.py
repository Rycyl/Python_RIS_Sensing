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
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


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
        self.point_range = int((self.CONFIG.sweptime - 2*self.RIS_change_time) /(1/int(self.CONFIG.rbw[0:-3]))) // len(self.pat_array)
        self.N_pts_delete = int(10) * self.N_SIGMA
        self.plots_list = []
        self.pdf_file = PdfPages(MEASURE_FILE.split('.')[0] + '.pdf')

    def run(self, new_mesure_file_no = None):
        if new_mesure_file_no:
            self.MEASURE_FILE = self.MEASURE_FILE.split('.')[0] + f'_{new_mesure_file_no}.csv'
        if new_mesure_file_no:
            self.TRACE_FILE = self.TRACE_FILE.split('.')[0] + f'_{new_mesure_file_no}.csv'
        self.search()
        return
        
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
    
    def write_debug_info(self, n, power_debug, pattern_debug, shift):
        with open (self.TRACE_FILE, 'a+') as trace_f:
            trace_f.write(f'"Grupowy pomiar N_el{self.N_ELEMENTS} 1szy opt elem w sekwencji={n}||SWT = {self.CONFIG.sweptime}|| ||Shift = {shift}||"\n')
            trace_f.write(f'{str(self.POWER_REC)[1:-1]}\n')
            trace_f.write(f'{str(power_debug)[1:-1]}\n')
            for napis in pattern_debug:
                trace_f.write(f'"{str(napis)}",')
            trace_f.write('\n')
    
    def get_trace(self):
        self.POWER_REC = self.ANALYZER.trace_get()
        return
    
    def measure_thread_with_RIS_changes(self):
        Measure = threading.Thread(target=self.get_trace) # cel wątku
        self.RIS.set_pattern('0x' + self.pat_array_copy[0].hex) # ustawienie pierwszego wzorca
        Measure.start() # rozpoczęcie wątku
        sleep(0.06) # czas oczekiwania na analizator
        sleep(0.022) # offset na początku pomiaru (?)
        for y in self.pat_array_copy[1:]: # start pętli po wzorcach
            sleep(self.SLEEPTIME) # 
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
            power_debug_shift =[]
            pattern_debug_shift = []
        else:
            power_debug = None
            pattern_debug = None
        powers = []
        stds_from_trace_shift_maxs = []
        stds_from_trace_shift = [[]]*len(self.pat_array)
        shift = 0
        end_pat = 0
        start_pat = 0

        ### iterate shift
        while end_pat<len(self.POWER_REC)-1:
            shift += 1
            enum = 0
            print(shift, start_pat, end_pat, len(self.POWER_REC))
            ### iterate patterns
            for i in range(len(self.pat_array)):
                enum = 0
                ## pętla ale po co
                while True:
                    enum += 1
                    start_pat = max(0, int(self.point_range * i + shift)) # self.N_pts_delete ))
                    end_pat = min(len(self.POWER_REC), int(self.point_range * (i + 1) + shift )) #- self.N_pts_delete ))
                    start_pat = min(start_pat, end_pat)
                    power_slice = self.POWER_REC[start_pat:end_pat]
                    if power_slice == []:
                        break
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
                    
                    print(f"start:: {start_pat}, end:: {end_pat}, shift:: {shift}, pat_no:: {i}")


                    powers.append(mean)

                    
                    if self.DEBUG_FLAG:
                        for xx in range(start_pat, end_pat):
                            power_debug[xx] = self.POWER_REC[xx]
                            pattern_debug[xx] = str(self.pat_array[i].hex)
                    break #koniec while
                if self.DEBUG_FLAG:
                    power_debug_shift.append(power_debug)
                    pattern_debug_shift.append(pattern_debug)
        #znajdz max std z każdego shifta
        x = 0
        ### find max std from all shifts 
        while (x < shift):
            stds = []
            for i in range(len(self.pat_array)):
                stds.append(stds_from_trace_shift[i][x])                
            stds_from_trace_shift_maxs.append(np.max(stds))
            x+=1
        #temp powers cut for std checkout##############33
        powers = powers[0:len(self.pat_array)]
        ###############################################33
        best_power = np.min(powers) if self.FIND_MIN else np.max(powers)
        best_idx = powers.index(best_power)
        
        return best_idx, best_power, power_debug_shift, pattern_debug_shift, powers, stds_from_trace_shift_maxs, stds_from_trace_shift
    
    def plot_stds(self, stds_maxs, n):
        lenght = len(stds_maxs)
        shifts = np.arange(lenght)
        fig = plt.figure(layout= "constrained", figsize= (15, 7))
        plt.subplot(1, 1, 1)
        plt.grid()
        plt.xlabel('Delta_X')
        plt.ylabel('Max_sigma^2')
        plt.title('Maximal std for eavry shift')
        
        plt.plot(shifts, stds_maxs, label = f"STDS for N = {n}")

        self.plots_list.append(fig)

        return
    
    def save_plots_to_pdf(self):

        for fig in self.plots_list:
            fig.savefig(self.pdf_file, format='pdf')
        
        return

    def search(self):
        n = 0
        power_write = []
        pattern_write = []

        #### loop all ris elements

        while n < 256:
            if self.TIME_FILE:
                self.t1.append(time.time())
            self.measure_thread_with_RIS_changes()
            if self.TIME_FILE:
                self.t0.append(time.time())
                
            best_idx, current_best_power, power_debug, pattern_debug, powers, stds_maxs, stds_all = self.measure_patterns()
            current_best_pattern = self.pat_array_copy[best_idx]
            power_write.extend(powers)
            
            ### copy pat_array
            for pat in self.pat_array_copy:
                pattern_write.append(pat.hex)
            
            if self.DEBUG_FLAG:
                shift = 0
                print(f"Pat:: {current_best_pattern}, Pow:: {current_best_power}")
                for i in range(len(power_debug)):
                    shift += 1
                    power_debug_table = power_debug[i]
                    pattern_debug_table = pattern_debug[i]
                    self.write_debug_info(n, power_debug_table, pattern_debug_table, shift)
            
            ### rol_patterns
            for i in range(len(self.pat_array)):
                self.pat_array[i].rol(self.N_ELEMENTS)
                self.pat_array_copy[i] = self.pat_array[i] | current_best_pattern
            
            self.plot_stds(stds_maxs, n)
            
            n += self.N_ELEMENTS
        
        self.meas_file.write(f"{str(pattern_write)[1:-1]}\n{str(power_write)[1:-1]}\n\n")
        self.save_plots_to_pdf()
        
        if self.TIME_FILE:
            ### zamienic na w funkcji
            with open (f"{self.TIME_FILE}.csv", 'a+') as timefile:
                timefile.write(str(self.t0)[1:-1])
                timefile.write('\n')
                timefile.write(str(self.t1)[1:-1])
                timefile.close()
        return
    
    def __del__(self):
        self.meas_file.close()
        self.pdf_file.close()
        return
