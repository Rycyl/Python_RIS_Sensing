import analyzer_sensing
import generator
from RIS import RIS
from RsSmw import *
import search_patterns
from file_writer import file_write_single_power
from config_obj import Config

config = Config()

if __name__ == "__main__":
    ##time.sleep(20)
    #RIS = RIS(port='/dev/ttyUSB0')
    sweeptime_l = 0.001
    #RIS.reset()
    generator.com_check()
    analyzer_sensing.com_prep()
    analyzer_sensing.com_check()
    generator.meas_prep(True, config.generator_mode, config.generator_amplitude, config.freq)
    analyzer_sensing.meas_prep(config.freq, sweeptime_l, config.span, config.analyzer_mode, config.detector, config.revlevel, config.rbw, config.swepnt)

    
    
    while(sweeptime_l < 0.6):
        i = 0

        with open(config.trace_file, 'a+') as file:
                file.write("Połączenie kablem we-wy" + ',')
                #file.write("Pattern ID1 [dBm]" + "," + "Pattern ID3 [dBm]" + ",")
                file.write(str(sweeptime_l) + ',')
                file.write('\n')
                file.close
        brekpoint = 100
        while(i<brekpoint): #100 pomiarów na jednym sweeptime
            i+=1
            print("Iteration: ", i)
            #RIS.set_pattern("0x0000000000000000000000000000000000000000000000000000000000000000")
            p1 = analyzer_sensing.trace_get_mean()
            #RIS.set_pattern("0x8000000000000000000000000000000000000000000000000000000000000000")
            p2 = analyzer_sensing.trace_get_mean()
            with open(config.trace_file, 'a+') as file:
                file.write(str(p1) + "," + str(p2) + ",")
                file.write('\n')
                file.close()  # CLose the file
            # }
        sweeptime_l*=2
        analyzer_sensing.meas_prep(config.freq, sweeptime_l, config.span, config.analyzer_mode, config.detector, config.revlevel, config.rbw, config.swepnt)
        # }    
    analyzer_sensing.meas_close()
    generator.meas_close()
