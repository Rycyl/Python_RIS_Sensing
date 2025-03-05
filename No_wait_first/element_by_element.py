from RIS import RIS
from analyzer_sensing import Analyzer
from generator import Generator
from config_obj import Config
import csv
from bitstring import BitArray
import threading
import time


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



    

            