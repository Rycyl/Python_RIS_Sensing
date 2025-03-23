from time import time, sleep
from analyzer_sensing import Analyzer
from config_obj import Config
import generator
from bitstring import BitArray
from RIS import RIS
import threading


class Analyzer_time_test:
    def __init__(self, Analyzer_obj: Analyzer, Config_obj: Config):
        self.Analyzer_obj = Analyzer_obj
        self.Config_obj = Config_obj
        #self.swt = Config_obj.sweptime
        #self.swepnt = Config_obj.swepnt
        
    def m_prep(self):
        self.Analyzer_obj.meas_prep(self.Config_obj.freq, self.Config_obj.sweptime, self.Config_obj.span, self.Config_obj.analyzer_mode, self.Config_obj.detector, self.Config_obj.revlevel, self.Config_obj.rbw, self.Config_obj.swepnt)
        return
    
    def set_paramiters(self, swt):
        self.Config_obj.update_swt(swt)
        return
    
    def check_time(self):
        start = time()
        self.Analyzer_obj.trace_get()
        return time()-start

class Analyzer_desynch_test:
    def __init__(self, Analyzer_obj: Analyzer, Config_obj: Config, RIS_obj: RIS, pattern_1 = BitArray(length=256), pattern_2 = BitArray("0xCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC"), swt = None, swepnt = None):
        self.Analyzer_obj = Analyzer_obj
        self.Config_obj = Config_obj
        self.RIS_obj = RIS_obj
        self.pattern_1 = pattern_1
        self.pattern_2 = pattern_2
        self.set_config(swt, swepnt)
        self.Analyzer_obj.meas_prep(self.Config_obj.freq, self.Config_obj.sweptime, self.Config_obj.span, self.Config_obj.analyzer_mode, self.Config_obj.detector, self.Config_obj.revlevel, self.Config_obj.rbw, self.Config_obj.swepnt)
        self.trace = None
        self.total_trace_list = []
        
    def set_config(self, swt, swepnt):
        if swt is None and swepnt is None:
            return
        elif swt is None:
            self.Config_obj.swepnt = swepnt
        elif swepnt is None:
            self.Config_obj.update_swt(swt)
        else:
            self.Config_obj.update_swt(swt)
            self.Config_obj.swepnt = swepnt
        return
    
    def get_trace(self):
        self.trace = self.Analyzer_obj.trace_get()
        #print("#################")
        #print("Meas Done")
        #print("##################")
        return
    
    def meas(self, wait_time = 0.06):
        Measure = threading.Thread(target=self.get_trace)
        self.RIS_obj.set_pattern('0x'+self.pattern_1.hex)
        sleep(0.02)
        #start = time()
        Measure.start()
        #print("MEAS START")
        sleep(wait_time)
        #print("SLEEP DONE", time()-start)
        self.RIS_obj.set_pattern('0x'+self.pattern_2.hex)
        Measure.join()
        #print("HUH")
        #print(time()-start)
        self.total_trace_list.append(self.trace)
        return 
    
    def clear_traces(self):
        self.total_trace_list = []
        return
    
    def get_traces(self):
        return self.total_trace_list
    