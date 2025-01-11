from Only_time_tests import Analyzer_time_test, Analyzer_desynch_test
from analyzer_sensing import Analyzer
from generator import Generator
from RIS import RIS
from config_obj import Config


if __name__ == "__main__":
    analyzer_time_test_file = "analyzer_time_test.csv"
    analyzer_desynch_test_file = "analyzer_desynch_test.csv"

    time_vals = [(2**x)/1000 for x in range(12)]
    wait_time = [x/1000 for x in range(22)]
    Conf = Config()
    Anal = Analyzer(Conf)
    Gen = Generator(Conf)
    Ris = RIS(port='/dev/ttyUSB0')

    pattern_1 = None
    pattern_2 = None

    Anal_t_t = Analyzer_time_test(Anal, Conf)
    Anal_d_t = Analyzer_desynch_test(Anal, Conf, Ris, swt = 0.66)



    for t in time_vals:
        Anal_t_t.set_paramiters(t)
        Anal_t_t.m_prep()
        with open(analyzer_time_test_file, "a+") as f:
            f.write("||SWT =||")
            f.write(str(t))
            f.write("\n")
            f.close()
        for i in range(1000):
            round_time = Anal_t_t.Analyzer_obj()
            with open(analyzer_time_test_file, "a+") as f:
                f.write(str(round_time))
                f.write("\n")
                f.close()
        with open(analyzer_time_test_file, "a+") as f:
            f.write("||SERIES END||")
            f.close()
    
    for w in wait_time:
        with open(analyzer_desynch_test_file, "a+") as f:
            f.write("||WAIT TIME =||")
            f.write(str(w))
            f.write("\n")
            f.close()
        for j in range(1000):
            Anal_d_t.meas(wait_time = w)
        trace_list = Anal_d_t.get_traces()
        with open(analyzer_desynch_test_file, "a+") as f:
            for trace in trace_list:
                f.write(str(trace)[1:-1])
                f.write("\n")
            f.write("||SERIES END||")
            f.close()
        
