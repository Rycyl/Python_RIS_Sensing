from analyzer_sensing import Analyzer
from config_obj import Config
import time
import numpy as np
import threading

def get_trace(ANALYZER):
    global POWER_REC
    POWER_REC = ANALYZER.trace_get()
    return

def measure_thread_with_RIS_changes(ANALYZER):
        MEASURE = threading.Thread(target=get_trace, args=(ANALYZER,)) #create thread MEASUREs
        ### PERFORM MEASURE
        MEASURE.start()
        MEASURE.join()
        ### MEASURE END

CONFIG = Config()
analyzer = Analyzer(CONFIG)
CONFIG.update_swt(0.748)

analyzer.meas_prep(CONFIG.freq, CONFIG.sweptime, CONFIG.span, CONFIG.analyzer_mode, CONFIG.detector, CONFIG.revlevel, CONFIG.rbw, CONFIG.swepnt)

t = []
for i in range(2000):
    t0 = time.time()
    measure_thread_with_RIS_changes(ANALYZER=analyzer)
    t1 = time.time()
    t.append(t1-t0)

print(f"mean:: {np.mean(t)}, std:: {np.std(t)}, min {np.min(t)}, max {np.max(t)}, median {np.median(t)}")

nazwa_pliku = 'newfile.csv'

with open(nazwa_pliku, 'a+') as file:
    file.write("\n")
    file.write(str(t)[1:-1])
    file.write("\n")
    file.write(str(f"mean:: {np.mean(t)}, std:: {np.std(t)}, min {np.min(t)}, max {np.max(t)}, median {np.median(t)}"))
    file.close()
