from RIS import RIS
from analyzer_sensing import Analyzer
from generator import Generator
from config_obj import Config
import csv
from bitstring import BitArray
import threading
import time
from copy import copy

class sing_pat_per_run():
    def __init__(self, ris: RIS, anal: Analyzer, gen: Generator, exit_file: str, codebook: str):
        self.Ris = ris
        self.Anal = anal
        self.Gen = gen
        self.file = exit_file
        self.Codebook = self.load_code_book(codebook)
        self.No_of_pats = len(self.Codebook)
        self.Mes_pow = None
        self.All_measured = {}


    def load_code_book(self, codebook):
        codes = []
        with open(codebook, "r") as f:
            lines = f.readlines()
            for line in lines:
                pattern, angle = line.split(";")
                datum = (BitArray(hex=pattern), angle.strip("\n"), "NaN")
                codes.append(datum)
                #codes.append(BitArray(hex=line))
            f.close()
        return codes
    
    def do_measure(self):
        self.Mes_pow = self.Anal.trace_get_mean()
        return self.Mes_pow
    
    def start_measure(self):       
        self.All_measured = []
        for datum in self.Codebook:
            Do_Measure = threading.Thread(target = self.do_measure)
            Do_Measure.start()
            # print(pattern)
            # print(pattern.hex)
            # print("settin pattern")
            #t_1 = time.time()
            self.Ris.set_pattern('0x' + datum[0].hex)
            # print(time.time() - t_1)
            # print("pattern set")
            Do_Measure.join()
            self.All_measured.append((datum[0],datum[1],self.Mes_pow))
        return self.save_to_file()
    
    def save_to_file(self):
        with open(self.file, 'w+') as csvfile:
            csvfile.write("Pattern, Angle, Power")
            csvfile.write("\n")
            for datum in self.All_measured:
                text = f"{datum[0]}; {datum[1]}; {datum[2]}"
                csvfile.write(text + "\n")
            csvfile.close()
        return self.All_measured
    

class sing_pat_per_run_w_wait():
    def __init__(self, ris: RIS, anal: Analyzer, gen: Generator, exit_file: str, codebook: str):
        self.Ris = ris
        self.Anal = anal
        self.Gen = gen
        self.file = exit_file
        self.Codebook = self.load_code_book(codebook)
        self.No_of_pats = len(self.Codebook)
        self.Mes_pow = None
        self.All_measured = {}


    def load_code_book(self, codebook):
        codes = []
        with open(codebook, "r") as f:
            lines = f.readlines()
            for line in lines:
                codes.append(BitArray(hex=line))
            f.close()
        return codes
    
    def do_measure(self):
        self.Mes_pow = self.Anal.trace_get_mean()
        return self.Mes_pow
    
    def start_measure(self):       
        self.All_measured = {}
        for pattern in self.Codebook:
            # Do_Measure = threading.Thread(target = self.do_measure)
            # Do_Measure.start()
            # print(pattern)
            # print(pattern.hex)
            # print("settin pattern")
            # t_1 = time.time()
            self.Ris.set_pattern('0x' + pattern.hex)
            self.do_measure()
            # print(time.time() - t_1)
            print("pattern set")
            # Do_Measure.join()
            self.All_measured['0x' + pattern.hex] = self.Mes_pow
        return self.save_to_file()
    
    def save_to_file(self):
        with open(self.file, 'w+') as csvfile:
            keys = self.All_measured.keys()
            csvfile.write("Pattern, Power")
            csvfile.write("\n")
            for key in keys:
                text = f"{key}, {self.All_measured[key]},"
                csvfile.write(text)
                csvfile.write("\n")
            csvfile.close()
        return self.All_measured


class element_by_element():
    def __init__(self, ris: RIS, anal: Analyzer, gen: Generator, exit_file: str, mask = '0b1', find_min = False, no_start_from_zero = False):
        self.Ris = ris
        self.Anal = anal
        self.Gen = gen
        self.file = exit_file
        self.Mask = mask
        self.Find_Min = find_min
        #self.No_start_from_zero = no_start_from_zero
        #self.Code_list = [(None, 'N/A', "NaN") for i in range(257)]
        #For now use only mask size == 1
        self.Current_pattern = copy(no_start_from_zero) if no_start_from_zero else BitArray(length=256)
        #self.Code_list[0][0] = copy(no_start_from_zero) if no_start_from_zero else BitArray(length=256)
        self.Mes_pow = None
        self.Best_pow = 100000 if find_min else -100000
        self.All_measured = []
        self.Best_pattern = BitArray(length=256)

    def do_measure(self):
        self.Mes_pow = self.Anal.trace_get_mean()
        return self.Mes_pow
    
    def check_if_better(self):
        if self.Find_Min:
            if self.Mes_pow < self.Best_pow:
                self.Best_pattern = copy(self.Current_pattern)
                self.Best_pow = self.Mes_pow
        elif self.Mes_pow > self.Best_pow:
            self.Best_pattern = copy(self.Current_pattern)
            self.Best_pow = self.Mes_pow
        return

    def start_measure(self):
        self.All_measured = []
        for c in range(257):
            c_datum = (None, 'N/A', "NaN")
            Do_measure = threading.Thread(target=self.do_measure)
            Do_measure.start()
            self.Ris.set_pattern('0x'+self.Current_pattern.bin)
            c_datum[0] = copy(self.Current_pattern)
            mask_pattern = BitArray(length=256)
            mask_pattern.overwrite(self.Mask, c)
            Do_measure.join()
            self.check_if_better()
            c_datum[2] = self.Mes_pow
            self.All_measured.append(c_datum)
            self.Current_pattern ^= mask_pattern
        return self.All_measured
    
    def save_to_file(self):
        with open(self.file, 'w+') as csvfile:
            csvfile.write("Pattern, Angle, Power")
            csvfile.write("\n")
            for datum in self.All_measured:
                text = f"{datum[0]}; {datum[1]}; {datum[2]}"
                csvfile.write(text + "\n")
            csvfile.close()
        return self.All_measured
                    
    def ret_best(self):
        return self.Best_pattern, self.Best_pow
    
class stripe_by_stripe():
    def __init__(self, ris: RIS, anal: Analyzer, gen: Generator, exit_file: str, find_min = False, no_start_from_zero = False):
        self.Ris = ris
        self.Anal = anal
        self.Gen = gen
        self.file = exit_file
        self.Mask = '0b10000000000000001000000000000000100000000000000010000000000000001000000000000000100000000000000010000000000000001000000000000000100000000000000010000000000000001000000000000000100000000000000010000000000000001000000000000000100000000000000010000000000000001000000000000000'
        self.Find_Min = find_min
        self.Current_pattern = copy(no_start_from_zero) if no_start_from_zero else BitArray(length=256)
        self.Mes_pow = None
        self.Best_pow = 100000 if find_min else -100000
        self.All_measured = []
        self.Best_pattern = BitArray(length=256)

    def do_measure(self):
        self.Mes_pow = self.Anal.trace_get_mean()
        return self.Mes_pow
    
    def check_if_better(self):
        if self.Find_Min:
            if self.Mes_pow < self.Best_pow:
                self.Best_pattern = copy(self.Current_pattern)
                self.Best_pow = self.Mes_pow
        elif self.Mes_pow > self.Best_pow:
            self.Best_pattern = copy(self.Current_pattern)
            self.Best_pow = self.Mes_pow
        return
    
    def start_measure(self):
        self.All_measured = []
        for c in range(16):
            c_datum = (None, 'N/A', "NaN")
            Do_measure = threading.Thread(target=self.do_measure)
            Do_measure.start()
            self.Ris.set_pattern('0x'+self.Current_pattern.bin)
            c_datum[0] = copy(self.Current_pattern)
            mask_pattern = BitArray(length=256)
            mask_pattern.overwrite(self.Mask, c)
            mask_pattern = mask_pattern[:256]
            Do_measure.join()
            self.check_if_better()
            c_datum[2] = self.Mes_pow
            self.All_measured.append(c_datum)
            self.Current_pattern ^= mask_pattern
        return self.All_measured
    
    def save_to_file(self):
        with open(self.file, 'w+') as csvfile:
            csvfile.write("Pattern, Angle, Power")
            csvfile.write("\n")
            for datum in self.All_measured:
                text = f"{datum[0]}; {datum[1]}; {datum[2]}"
                csvfile.write(text + "\n")
            csvfile.close()
        return self.All_measured
                    
    def ret_best(self):
        return self.Best_pattern, self.Best_pow