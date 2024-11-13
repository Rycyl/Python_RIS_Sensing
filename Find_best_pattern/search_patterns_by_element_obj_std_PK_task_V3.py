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
import random


class Element_By_Element_Search_std_PK:
    def __init__(self, RIS, GENERATOR, ANALYZER, CONFIG, N_ELEMENTS = 4, N_SIGMA = 3, TIME_SAFETY_MARGIN = 3.0, STD_TRS = 0.08, STD_CHECK_ON = True, DEBUG_FLAG = False, MEASURE_FILE = 'find_best_pattern_element_wise_by_group_measures_v2.csv', FIND_MIN = False, TRACE_FILE = 'trace_file_group_mesures.csv', TIME_FILE = None,):
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
        self.best_power = 1000.0 if self.FIND_MIN else -1000.0
        self.update_config_sweep_time()
        self.GENERATOR.meas_prep(True, self.CONFIG.generator_mode, self.CONFIG.generator_amplitude, self.CONFIG.freq)
        self.ANALYZER.meas_prep(self.CONFIG.freq, self.CONFIG.sweptime, self.CONFIG.span, self.CONFIG.analyzer_mode, self.CONFIG.detector, self.CONFIG.revlevel, self.CONFIG.rbw, self.CONFIG.swepnt)
        self.meas_file, self.t0, self.t1 = self.prepare_measurement_files()
        self.POWER_REC = None
        self.SLEEPTIME = (self.CONFIG.sweptime / len(self.pat_array) - self.RIS_change_time)
        self.point_range = int((self.CONFIG.sweptime - 2*self.RIS_change_time) /(1/int(self.CONFIG.rbw[0:-3]))) // len(self.pat_array)
        self.N_pts_delete = (int(10) * self.point_range) // 100
        self.plots_list = []
        self.pdf_file = PdfPages(MEASURE_FILE.split('.')[0] + '.pdf')
        self.powers = None
        self.stds_from_trace_shift_maxs = None
        self.stds_from_trace_shift = None
        self.shift = None
        self.end_pat = None
        self.start_pat = None
        self.best_idx = None
        self.power_debug_shift  = None
        self.pattern_debug_shift  = None
        self.stds_max_over_sum = []
        self.best_shift = None

    def run(self, new_mesure_file_no = None):
        if new_mesure_file_no:
            self.MEASURE_FILE = self.MEASURE_FILE.split('.')[0] + f'_{new_mesure_file_no}.csv'
        if new_mesure_file_no:
            self.TRACE_FILE = self.TRACE_FILE.split('.')[0] + f'_{new_mesure_file_no}.csv'
        self.search()
        return
        
    def prepare_patterns(self):
        pat_array = [BitArray(uint=x, length=256) for x in range(self.combinations)]
        #print(pat_array)
        return pat_array, copy(pat_array)
    
    def prepare_random_patterns(self):
        random_range = 2**256 -1
        pat_array = [BitArray(uint=random.randint(0, random_range), length=256) for x in range(self.combinations)]
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
    
    def write_debug_info(self, n, power_debug, pattern_debug, c_shift):
        with open (self.TRACE_FILE, 'a+') as trace_f:
            trace_f.write(f'"Grupowy pomiar N_el{self.N_ELEMENTS} 1szy opt elem w sekwencji={n}||SWT = {self.CONFIG.sweptime}|| ||Shift = {c_shift}||"\n')
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
#Never used, delete?
    def calculate_shift(self, power_slice, std, mean):
        minpow = min(power_slice)
        maxpow = max(power_slice)
        max_out = (maxpow > mean + std)
        min_out = (minpow < mean - std)
        
        if max_out:
            if power_slice.index(maxpow) < (self.point_range * 0.7):
                self.shift -= int(self.point_range * 0.07)
            else:
                self.shift += int(self.point_range * 0.03)
        else:
            if power_slice.index(minpow) < (self.point_range * 0.3):
                self.shift -= int(self.point_range * 0.07)
            else:
                self.shift += int(self.point_range * 0.03)
        return self.shift
    

    def iterate_by_group_of_patterns(self):
        prev_std = []
        beginings = []
        ends = []
        c_segment_starts = []
        c_segment_ends = []
        n_points_range = self.N_pts_delete #Temporary value, find better solution
        self.start_pat = 0
        self.end_pat = n_points_range
        while self.end_pat < len(self.POWER_REC)-1:
            power_slice = self.POWER_REC[self.start_pat:self.end_pat]
            if power_slice == []:
                break
            std = np.std(power_slice)
            if prev_std == [] or len(prev_std) < 3:
                prev_std.append(std)
                c_segment_starts.append(self.start_pat)
                c_segment_ends.append(self.end_pat)
                # if len(prev_std) == 3:
                #     print("Add later")
            else:
                if std <= self.STD_TRS:
                    prev_std.pop(0)
                    prev_std.append(std)
                    c_segment_starts.append(self.start_pat)
                    c_segment_ends.append(self.end_pat)
                else:
                    beginings.append(c_segment_starts[0])
                    ends.append(c_segment_ends[0])
                    c_segment_starts = []
                    c_segment_ends = []
                    prev_std = []
            self.start_pat += n_points_range
            self.end_pat += n_points_range
        print(f"Beginings Len:: {len(beginings)}, Ends Len:: {len(ends)}")
        return self.calculate_power_from_slices(beginings, ends)

    def calculate_power_from_slices(self, beginings, ends):
        powers = []
        for i in range(len(beginings)):
            power_slice = self.POWER_REC[beginings[i]:ends[i]]
            mean = np.mean(power_slice)
            powers.append(mean)
        print(f"Powers Len:: {len(powers)}")
        return powers
                    
                        


    # def iterate_by_group_of_patterns(self):
    #     temp_stds_table = []
    #     temp_powers_table = []
    #     if self.DEBUG_FLAG:
    #         power_debug_shift_local = [-150] * len(self.POWER_REC)
    #         pattern_debug_shift_local = [None] * len(self.POWER_REC)
    #     for i in range(len(self.pat_array)):
    #         self.start_pat = max(0, int(self.point_range * i + self.shift)) + self.N_pts_delete
    #         self.end_pat = min(len(self.POWER_REC), int(self.point_range * (i + 1) + self.shift )) - self.N_pts_delete
    #         self.start_pat = min(self.start_pat, self.end_pat)
    #         power_slice = self.POWER_REC[self.start_pat:self.end_pat]
    #         if power_slice == []:
    #             break
    #         std = np.std(power_slice)
    #         mean = np.mean(power_slice)
            
    #         if self.DEBUG_FLAG:
    #             print(f"STD:: {std}, mean:: {mean}, len_power_slice:: {len(power_slice)}")

    #         # self.stds_from_trace_shift[i].append(std) #i-ty pattern, dodaj jego bierzące std ###old version###
    #         temp_stds_table.append(std)
    #         print(f"start:: {self.start_pat}, end:: {self.end_pat}, shift:: {self.shift}, pat_no:: {i}")

    #         #self.powers.append(mean)
    #         temp_powers_table.append(mean)
            
    #         if self.DEBUG_FLAG:
    #             for xx in range(self.start_pat, self.end_pat):
    #                 power_debug_shift_local[xx] = self.POWER_REC[xx]
    #                 pattern_debug_shift_local[xx] = str(self.pat_array[i].hex)
    #     self.stds_from_trace_shift.append(temp_stds_table)
    #     self.powers.append(temp_powers_table)
        # # print("/////////////////////////////////////////////////////")
        # # print(f"STDs_table:: {self.stds_from_trace_shift}")
        # # print("/////////////////////////////////////////////////////")
        # if self.DEBUG_FLAG:            
        #     self.power_debug_shift.append(power_debug_shift_local)
        #     self.pattern_debug_shift.append(pattern_debug_shift_local)
        # #print(f"Power_debug_shift_3:: {self.power_debug_shift}")
        # return


    def iterate_shift(self):
        while self.end_pat<len(self.POWER_REC)-self.N_pts_delete:
            self.shift += 1
            print(self.shift, self.start_pat, self.end_pat, len(self.POWER_REC))
            ### iterate patterns
            self.iterate_by_group_of_patterns()
            #print("Exiting iterate_by_group_of_patterns")
            #print(f"Power_debug_shift_4:: {self.power_debug_shift}")
        #print(f"Shift:: {self.shift}")
        #print("Exiting iterate_shift")
        return
    ### OLD VERSION ###
    # def find_max_std_from_each_shift(self):
    #     x = 0
    #     while (x < self.shift):
    #         stds = []
    #         for i in range(len(self.pat_array)):
    #             stds.append(self.stds_from_trace_shift[i][x])                
    #         self.stds_from_trace_shift_maxs.append(np.max(stds))

    #         x+=1
    #     return

    def find_max_std_from_each_shift(self):
        stds_max_over_sum = []
        for shift_table in self.stds_from_trace_shift:
            stds = shift_table[:]
            max_std = np.max(stds)
            self.stds_from_trace_shift_maxs.append(max_std)
            stds_sum = sum(stds)
            stds_max_over_sum.append(max_std/stds_sum) #czy to na pewno musi być self??
        self.best_shift = stds_max_over_sum.index(min(stds_max_over_sum))
        return
   

    def measure_patterns(self):
        if self.DEBUG_FLAG:
            self.power_debug_shift =[]
            #print("DEBUG_FLAG:: ", self.DEBUG_FLAG)
            #print("POWER_DEBUG_SHIFT_1:: ", self.power_debug_shift)
            self.pattern_debug_shift = []
        self.powers = []
        self.stds_from_trace_shift_maxs = []
        # self.stds_from_trace_shift = [[]]*len(self.pat_array) old version
        self.stds_from_trace_shift = []
        self.shift = -1
        self.end_pat = 0
        self.start_pat = 0

        ### iterate self.shift
        #self.iterate_shift()
        #print("Exiting measure_patterns")
        #print(f"Power_debug_shift_2:: {self.power_debug_shift}")
        
        #znajdz max std z każdego shifta
        #self.find_max_std_from_each_shift()
        
        #temp self.powers cut for std checkout##############33
        # self.powers = self.powers[self.best_shift]
        # self.powers = self.powers[0:len(self.pat_array)]
        ###############################################33
        self.powers = self.iterate_by_group_of_patterns()
        self.best_power = np.min(self.powers) if self.FIND_MIN else np.max(self.powers)
        self.best_idx = self.powers.index(self.best_power)
        if self.DEBUG_FLAG:
            print(f"Best_power:: {self.best_power}, Best_idx:: {self.best_idx}")
            # self.power_debug_shift = self.power_debug_shift[self.best_shift]
            # self.pattern_debug_shift = self.pattern_debug_shift[self.best_shift]
        
        return
    
    def plot_stds(self, n):
        lenght = len(self.stds_from_trace_shift_maxs)
        shifts = np.arange(lenght)
        fig = plt.figure(layout= "constrained", figsize= (15, 7))
        plt.subplot(1, 1, 1)
        plt.grid()
        plt.xlabel('Delta_X')
        plt.ylabel('Max_sigma^2')
        plt.title('Maximal std for eavry shift')
        plt.plot(shifts, self.stds_from_trace_shift_maxs, label = f"STDS for N = {n}")
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
                
            self.measure_patterns()
            print("############################################################")
            print("############################################################")
            print(f"Best power:: {self.best_power}, Best_idx:: {self.best_idx}, Best_shift:: {self.best_shift}")
            print(f"Best pattern:: {self.pat_array_copy[self.best_idx].hex}")
            print("############################################################")
            print("############################################################")
            current_best_pattern = self.pat_array_copy[self.best_idx]
            power_write.extend(self.powers)
            
            ### copy pat_array
            for pat in self.pat_array_copy:
                pattern_write.append(pat.hex)

            # if self.DEBUG_FLAG:
            #     self.write_debug_info(n, self.power_debug_shift, self.pattern_debug_shift, self.best_shift)            
            
            ### rol_patterns
            for i in range(len(self.pat_array)):
                self.pat_array[i].rol(self.N_ELEMENTS)
                self.pat_array_copy[i] = self.pat_array[i] | current_best_pattern
            
            # self.plot_stds(n)
            
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
        plt.close('all')
        return


####    DODAC DEF zwracający shift
###     Rodzielić obliczanie shifta i fukcje zwracania sredniej
#       dodac funkcje z rysunku do sprawdzania akuratnosci wybranego minimum std
#       