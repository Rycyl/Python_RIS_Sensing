import analyzer_sensing
import generator
from RIS import RIS
from RsSmw import *
import search_patterns
from file_writer import file_write_single_power

if __name__ == "__main__":
    ##time.sleep(20)
    RIS = RIS(port='/dev/ttyUSB0')

    RIS.reset()
    generator.com_check()
    analyzer_sensing.com_prep()
    analyzer_sensing.com_check()
    generator.meas_prep(True, generator_mode, bgenerator_amplitude, freq)
    analyzer_sensing.meas_prep(freq, bsweptime, span, banalyzer_mode, bdetector, revlevel, rbw, bswepnt)

        
    bsweptime = 0.001
    while(bsweptime < 0.1):
        i = 0
        brekpoint = 100
        while(i<brekpoint): #100 pomiarów na jednym sweeptime
            i+=1
            print("Iteration: ", i)
            RIS.set_pattern("0x0000000000000000000000000000000000000000000000000000000000000000")
            p = analyzer_sensing.trace_get_mean()
            with open(trace_file, 'a+') as file:
                file.write("Pattern ID1")
                file.write(str(bsweptime))
                file.write(str(p) + ",")
                file.write('\n')
                file.close()  # CLose the file
            RIS.set_pattern("0x8000000000000000000000000000000000000000000000000000000000000000")
            p = analyzer_sensing.trace_get()
            with open(trace_file, 'a+') as file:
                file.write("Pattern ID3")
                file.write(str(p) + ",")
                file.write('\n')
                file.close()  # CLose the file
            continue
        analyzer_sensing.meas_close()
        generator.meas_close()
        bsweptime*=2
        continue