from Only_time_tests import Analyzer_time_test, Analyzer_desynch_test
from analyzer_sensing import Analyzer
from generator import Generator
from RIS import RIS
from config_obj import Config
from bitstring import BitArray
from time import sleep
from numpy import arange

if __name__ == "__main__":
    analyzer_time_test_file = "analyzer_time_test.csv"
    analyzer_desynch_test_file = "analyzer_desynch_test.csv"

    time_vals = [(2**x)/1000 for x in range(12)]
    #wait_time = [x/1000 for x in range(50,400)]
    wait_time = arange(0.06, 0.36, 0.06)
    print(wait_time)
    Conf = Config()
    Anal = Analyzer(Conf)
    Anal.com_check()
    Gen = Generator(Conf)
    Gen.com_check()
    Ris = RIS(port='/dev/ttyUSB0')

    pattern_1 = BitArray("0x0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F")
    pattern_2 = BitArray("0x00007FFE40025FFA500A57EA542A55AA55AA542A57EA500A5FFA40027FFE0000")

    Anal_t_t = Analyzer_time_test(Anal, Conf)


    sleep(60)
    print("STARTED PT ONE")

    Anal_d_t = Analyzer_desynch_test(Anal, Conf, Ris, swt = 0.6, pattern_1= pattern_1, pattern_2= pattern_2)
    Gen.meas_prep(True, Conf.generator_mode, Conf.generator_amplitude, Conf.freq)

    for w in wait_time:
        with open(analyzer_desynch_test_file, "a+") as f:
            f.write("||WAIT TIME =||, ")
            f.write(str(w))
            f.write(",")
            f.write(f"||SWPNTS =||, {Conf.swepnt}")
            f.write("\n")
            f.close()
            print("STARTED", w)
        for j in range(1000):
            Anal_d_t.meas(wait_time = w)
        trace_list = Anal_d_t.get_traces()
        with open(analyzer_desynch_test_file, "a+") as f:
            for trace in trace_list:
                f.write(str(trace)[1:-1])
                f.write("\n")
            f.write("||SERIES END||")
            f.write("\n")
            f.close()
        Anal_d_t.clear_traces()
        print("ENDED", w)

    #############################################################
    ######################END OF Pt. ONE#########################
    #############################################################
    print("STARTED PT TWO")
        
    for t in time_vals:
        Anal_t_t.set_paramiters(t)
        Anal_t_t.m_prep()
        with open(analyzer_time_test_file, "a+") as f:
            f.write("||SWT =||, ")
            f.write(str(t))
            f.write(" , ||ANAL SWT=||, ")
            f.write(str(Conf.sweptime))
            f.write(" , ||SWPNT=||, ")
            f.write(str(Conf.swepnt))
            f.write("\n")
            f.close()
        for i in range(1000):
            round_time = Anal_t_t.check_time()
            with open(analyzer_time_test_file, "a+") as f:
                f.write(str(round_time))
                f.write("\n")
                f.close()
        with open(analyzer_time_test_file, "a+") as f:
            f.write("||SERIES END||")
            f.write("\n")
            f.close()