from RIS import RIS
from analyzer_sensing import Analyzer
from generator import Generator
from config_obj import Config
import csv
from bitstring import BitArray
import threading
import time
from math import ceil


class Single_Trace_Search_codebook:
    def __init__(self, Ris: RIS, Anal: Analyzer, Gen: Generator, Conf: Config, Exit_File: str, Codebook: str, set_RIS_change_time = False):
        self.Ris = Ris
        self.Anl = Anal
        self.Gen = Gen
        self.Conf = Conf
        self.Codebook = self.load_code_book(Codebook)
        self.Meas_File = Exit_File
        if set_RIS_change_time:
            self.Ris.set_wait_time = set_RIS_change_time
            self.Ris_change_time = set_RIS_change_time
        else:
            set_RIS_change_time = 0.022
        self.meas_delay = 0.04 #Check if true and correct later

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
    
    def ready_analyzer_params(self, max_pats_per_run = 8):
        all_codes = []
        no_of_runs = ceil(len(self.Codebook)/max_pats_per_run)
        swt = max_pats_per_run * self.Ris_change_time + self.meas_delay
        self.Conf.update_swt(swt)
        meas_prep_args = (self.Conf.freq, self.Conf.sweptime, self.Conf.span, self.Conf.analyzer_mode, self.Conf.detector, self.Conf.revlevel, self.Conf.rbw, self.Conf.swepnt)
        meas_prep = threading.Thread(target=self.Anl.meas_prep,) 
