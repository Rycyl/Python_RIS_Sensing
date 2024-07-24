import analyzer_sensing
import generator
from RIS import RIS
from RsSmw import *
import search_patterns
from file_writer import file_write_single_power
from config_obj import Config
from time import time, ctime, sleep

config = Config()

if __name__ == "__main__":
    sweeptime_l = 0.001
    RIS = RIS(port='/dev/ttyUSB0')
    RIS.reset()
    generator.com_check()
    analyzer_sensing.com_prep()
    analyzer_sensing.com_check()
    generator.meas_prep(True, config.generator_mode, config.generator_amplitude, config.freq)

    i = 0
    ##prepare trace file

    file = open(config.trace_file, 'a+')
    file.write((str(ctime(time()))) + ',')
    file.write("SWT(ms), in 1st row, Iters, in 1st col, \n")#HEADER
    file.write(" ,1,1,2,2,4,4,8,8,16,16,32,32,64,64,128,128,256,256,512,512,1024,1024,")
    file.write('\n')
    #file.close()  # CLose the file

    analyzer_sensing.meas_prep(config.freq, sweeptime_l, config.span, config.analyzer_mode, config.detector, config.revlevel, config.rbw, config.swepnt)
    iters = 100
    sleep(20)
    while(i<iters): #100 pomiarów na jednym sweeptime
        #t1 = time()
        sweeptime_l = 0.001
        file.write(str(i) + ",")
        print("Iteration: ", i)
        while(sweeptime_l < 0.6):
            
            analyzer_sensing.meas_prep(config.freq, sweeptime_l, config.span, config.analyzer_mode, config.detector, config.revlevel, config.rbw, config.swepnt)
            RIS.set_pattern("0x0000000000000000000000000000000000000000000000000000000000000000")
            
            p1 = analyzer_sensing.trace_get_mean()
            RIS.set_pattern("0x8000000000000000000000000000000000000000000000000000000000000000")
            p2 = analyzer_sensing.trace_get_mean()
            file.write(str(p1) + "," + str(p2) + ",")

            #print("SWT= ", sweeptime_l, "p1= ", round(p1, 3), "p2= ", round(p2, 3)) ## to comment /debug
            sweeptime_l*=2
        i += 1
        file.write('\n')
        #print("czas iteracji= ", time() - t1, "                !!!!!!!!!!!!!!!!!!!!!!!")

    file.close()    
    analyzer_sensing.meas_close()
    generator.meas_close()
    exit()
