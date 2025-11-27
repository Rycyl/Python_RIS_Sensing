from RIS import RIS
from analyzer_sensing import Analyzer
from generator import Generator
from config_obj import Config
import csv
from bitstring import BitArray
import threading
import time
from copy import copy
from get_angle import Antenna_Geometry
from numpy import mean

# def negate(bits):
#     ones = BitArray(hex='F' * 64)
#     bits = bits ^ ones
#     return bits

class sing_pat_per_run():
    def __init__(self, ris: RIS, anal: Analyzer, gen: Generator, geometry_obj: Antenna_Geometry, exit_file: str, codebook: str, Get_Men_Pow: bool = True):
        self.Ris = ris
        self.Anal = anal
        self.Gen = gen
        self.file = exit_file
        self.Codebook = self.load_code_book(codebook)
        self.No_of_pats = len(self.Codebook)
        self.Mes_pow = None
        self.All_measured = {}
        self.Geometry = geometry_obj
        self.Get_Men_Pow = Get_Men_Pow


    def load_code_book(self, codebook):
        codes = []
        with open(codebook, "r") as f:
            lines = f.readlines()
            for line in lines:
                n, pattern, angles = line.split(";")
                datum = (n, BitArray(hex=pattern), "Power", angles.strip("\n"), "Tx", "Rx")
                codes.append(datum)
                #codes.append(BitArray(hex=line))
            f.close()
        return codes
    
    def do_measure_mean(self):
        self.Mes_pow = self.Anal.trace_get_mean()
        return self.Mes_pow
    
    def do_measure_whole(self):
        self.Mes_pow = self.Anal.trace_get()
        return self.Mes_pow
    
    def do_get_angles(self):
        while True:
            try:
                angles = self.Geometry.get_angles()
                print(angles)
                return angles
            except Exception as e:
                print(e)
                pass
        return
    
    def start_measure(self):       
        self.All_measured = []
        if self.Get_Men_Pow:
            measure_fun = self.do_measure_mean
        else:
            measure_fun = self.do_measure_whole
        print("Get geometry")
        Tx_angle, Rx_angle, a, c, x, y, b = self.do_get_angles()
        print("Doing Measures")
        for datum in self.Codebook:
            Do_Measure = threading.Thread(target = measure_fun)
            Do_Measure.start()
            self.Ris.set_pattern('0x' + datum[1].hex)
            Do_Measure.join()
            self.All_measured.append([datum[0],datum[1],self.Mes_pow, Tx_angle, Rx_angle, a, c, x, y, b])
        return self.All_measured#self.save_to_file()
    
    def save_to_file(self):
        with open(self.file, 'w+') as csvfile:
            csvfile.write("N; Pattern; Power; Tx Angle; Rx Angle; a; c; x; y; b")
            csvfile.write("\n")
            for datum in self.All_measured:
                for d in datum:
                    csvfile.write(str(d)+";")
                csvfile.write("\n")
            csvfile.close()
        return self.All_measured
    

class sing_pat_per_run_w_wait():
    def __init__(self, ris: RIS, anal: Analyzer, gen: Generator, exit_file: str, codebook: str, Get_Men_Pow: bool = True):
        self.Ris = ris
        self.Anal = anal
        self.Gen = gen
        self.file = exit_file
        self.Codebook = self.load_code_book(codebook)
        self.No_of_pats = len(self.Codebook)
        self.Mes_pow = None
        self.All_measured = {}
        self.Get_Men_Pow = Get_Men_Pow


    def load_code_book(self, codebook):
        codes = []
        with open(codebook, "r") as f:
            lines = f.readlines()
            for line in lines:
                codes.append(BitArray(hex=line))
            f.close()
        return codes
    
    def do_measure_mean(self):
        self.Mes_pow = self.Anal.trace_get_mean()
        return self.Mes_pow
    
    def do_measure_whole(self):
        self.Mes_pow = self.Anal.trace_get()
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
            if self.Get_Men_Pow:
                self.do_measure_mean()
            else:
                self.do_measure_whole()
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
    def __init__(self, ris: RIS, anal: Analyzer, gen: Generator, exit_file: str, mask = '0b1', find_min = False, no_start_from_zero = False, Get_Men_Pow: bool = True, subcar_to_maxi: tuple = (10, 20)):
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
        self.Get_Men_Pow = Get_Men_Pow
        self.Subcar_to_Maxi = subcar_to_maxi
        self.Whole_Trace = None

    def do_measure_mean(self):
        self.Mes_pow = self.Anal.trace_get_mean()
        return self.Mes_pow
    
    def do_measure_whole(self):
        trace = self.Anal.trace_get()
        self.Whole_Trace = trace[:]
        trace = trace[224:1824:2]
        data = trace[self.Subcar_to_Maxi[0], self.Subcar_to_Maxi[1]]
        lin_data = [10**(x/10) for x in data]
        self.Mes_pow = mean(lin_data)
        return self.Mes_pow
        
    def check_if_better(self):
        if self.Find_Min:
            #print(self.Find_Min)
            if self.Mes_pow < self.Best_pow:
                self.Best_pattern = copy(self.Current_pattern)
                self.Best_pow = self.Mes_pow
        elif self.Mes_pow > self.Best_pow:
            #print(self.Mes_pow)
            #print(self.Best_pow)
            self.Best_pattern = copy(self.Current_pattern)
            self.Best_pow = self.Mes_pow
            
        return

    def start_measure(self):
        self.All_measured = []
        print(self.Current_pattern)
        print(len(self.Current_pattern))
        if self.Get_Men_Pow:
            mesure_fun = self.do_measure_mean
        else:
            mesure_fun = self.do_measure_whole
        for c in range(256):
            #print("Iteration: ", c)
            #print("Current pattern: ", self.Current_pattern)
            Do_measure = threading.Thread(target=mesure_fun)
            s_time = time.time()
            Do_measure.start()
            
            self.Ris.set_pattern('0x'+self.Current_pattern.hex)
            
            c_datum_0 = copy(self.Current_pattern)
            
            mask_pattern = BitArray(length=256)
            
            mask_pattern.overwrite(self.Mask, c)
            #print("Inside: ",time.time() - s_time)
            Do_measure.join()
            #print(time.time() - s_time)
            self.check_if_better()
            c_datum_2 = self.Mes_pow if(self.Get_Men_Pow) else self.Whole_Trace
            c_datum = (c_datum_0, 'N/A', c_datum_2)
            self.All_measured.append(c_datum)
            self.Current_pattern = self.Best_pattern ^ mask_pattern
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
    def __init__(self, ris: RIS, anal: Analyzer, gen: Generator, geometry_obj: Antenna_Geometry, exit_file: str, find_min = False, no_start_from_zero = False, Get_Men_Pow: bool = True, subcar_to_maxi: tuple = (10, 20)):
        self.Ris = ris
        self.Anal = anal
        self.Gen = gen
        self.file = exit_file
        self.Mask = '0x8000800080008000800080008000800080008000800080008000800080008000'
        self.Find_Min = find_min
        self.Current_pattern = copy(no_start_from_zero) if no_start_from_zero else BitArray(length=256)
        self.Mes_pow = None
        self.Best_pow = 100000 if find_min else -100000
        self.All_measured = []
        self.Best_pattern = BitArray(length=256)
        self.Geometry = geometry_obj
        self.Get_Men_Pow = Get_Men_Pow
        self.Subcar_to_Maxi = subcar_to_maxi
        self.Whole_Trace = None

    def do_measure_mean(self):
        self.Mes_pow = self.Anal.trace_get_mean()
        return self.Mes_pow
    
    def do_measure_whole(self):
        trace = self.Anal.trace_get()
        self.Whole_Trace = trace[:]
        trace = trace[224:1824:2]
        data = trace[self.Subcar_to_Maxi[0], self.Subcar_to_Maxi[1]]
        lin_data = [10**(x/10) for x in data]
        self.Mes_pow = mean(lin_data)
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
    
    def do_get_angles(self):
        while True:
            try:
                angles = self.Geometry.get_angles()
                print(angles)
                return angles
            except Exception as e:
                print(e)
                pass
        return

    def start_measure(self):
        self.All_measured = []
        Tx_angle, Rx_angle, a, cc, x, y, b = self.do_get_angles()
        if self.Get_Men_Pow:
            mesure_fun = self.do_measure_mean
        else:
            mesure_fun = self.do_measure_whole
        if self.Find_Min:
            n = 2000
        else:
            n = 1000
        for c in range(17):
            #print("Iteration: ", c)
            #print("Pattern: ", self.Current_pattern)
            Do_measure = threading.Thread(target=mesure_fun)
            Do_measure.start()
            self.Ris.set_pattern('0x'+self.Current_pattern.hex)
            c_datum_0 = copy(self.Current_pattern)
            mask_pattern = BitArray(length=256)
            mask_pattern.overwrite(self.Mask, c)
            mask_pattern = mask_pattern[:256]
            Do_measure.join()
            self.check_if_better()
            c_datum_2 = self.Mes_pow if(self.Get_Men_Pow) else self.Whole_Trace
            c_datum = [n, c_datum_0, c_datum_2, Tx_angle, Rx_angle, a, cc, x, y, b]
            self.All_measured.append(c_datum)
            self.Current_pattern = self.Best_pattern ^ mask_pattern
            n += 1
        # negated = copy(self.Best_pattern)
        # negated.invert()
        # self.Ris.set_pattern('0x'+negated.hex)
        # self.do_measure()
        # negated_measure = [n, negated, self.Mes_pow, Tx_angle, Rx_angle, a, cc, x, y, b]
        # self.All_measured.append(negated_measure)
        return self.All_measured
    
    def save_to_file(self):
        with open(self.file, 'w+') as csvfile:
            csvfile.write("Pattern, Angle, Power")
            csvfile.write("\n")
            for datum in self.All_measured:
                csvfile.write(n+";")
                for d in datum:
                    csvfile.write(str(d)+";")
                csvfile.write("\n")
                n+=1
            csvfile.close()
        return self.All_measured
                    
    def ret_best(self):
        return self.Best_pattern, self.Best_pow