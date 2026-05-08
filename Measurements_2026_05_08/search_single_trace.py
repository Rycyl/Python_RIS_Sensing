from RIS import RIS
from analyzer_sensing import Analyzer
from generator import Generator
from config_obj import Config
import csv
from bitstring import BitArray
import threading
import time
from math import ceil
from copy import copy


class Single_Trace_Search_codebook:
    def __init__(self, Ris: RIS, Anal: Analyzer, Gen: Generator, Conf: Config, Exit_File: str, Codebook: str, set_RIS_change_time = False):
        self.Ris = Ris
        self.Anl = Anal
        self.Gen = Gen
        self.Conf = Conf
        # self.Codebook = self.load_code_book(Codebook)
        self.Meas_File = Exit_File
        if set_RIS_change_time:
            self.Ris.set_wait_time = set_RIS_change_time
            self.Ris_change_time = set_RIS_change_time
        else:
            self.Ris_change_time = 0.022
        self.meas_delay = 0.04 #Check if true and correct later
        self.Codebook = self.ready_analyzer_params_n_load_c_book(codebook=Codebook)
        self.C_trace = None

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
    
    def ready_analyzer_params_n_load_c_book(self, codebook, max_pats_per_run = 8):
        all_codes = []
        codes = self.load_code_book(codebook)
        no_of_runs = ceil(len(codes)/max_pats_per_run)
        swt = max_pats_per_run * self.Ris_change_time + self.meas_delay
        self.Conf.update_swt(swt)
        meas_prep_args = (self.Conf.freq, self.Conf.sweptime, self.Conf.span, self.Conf.analyzer_mode, self.Conf.detector, self.Conf.revlevel, self.Conf.rbw, self.Conf.swepnt)
        meas_prep = threading.Thread(target=self.Anl.meas_prep, args=meas_prep_args)
        meas_prep.start()
        for x in range(no_of_runs):
            temp = []
            for y in range(max_pats_per_run):
                temp.append(codes.pop(0))
            all_codes.append(temp)
        meas_prep.join()
        return all_codes

    def Anal_start(self):
        self.C_trace = self.Anl.trace_get()
        return self.C_trace

    def run_measure(self):
        Measure = threading.Thread(target=self.Anal_start)
        Measure.start()
        