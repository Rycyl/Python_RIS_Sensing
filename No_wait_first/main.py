from analyzer_sensing import Analyzer
from generator import Generator
from RIS import RIS
from element_by_element import sing_pat_per_run
from config_obj import Config
from file_creator import create_file
import time
from search_patterns import find_best_pattern_element_wise

if __name__ == "__main__":
    t_1 = time.time()
    Conf = Config()
    phy_device_input = True

    analyzer = Analyzer(Conf, phy_device_input)
    generator = Generator(Conf, phy_device_input)
    ris = RIS(port='COM5', phy_device=phy_device_input)
    print("RIS done")
    generator.meas_prep(True, Conf.generator_mode, Conf.generator_amplitude, Conf.freq)
    analyzer.meas_prep(Conf.freq, Conf.sweptime, Conf.span, Conf.analyzer_mode, Conf.detector, Conf.revlevel, Conf.rbw, Conf.swepnt)
    # GENERATOR.meas_prep(True, Conf.generator_mode, Conf.generator_amplitude, Conf.freq)
    # ANALYZER.meas_prep(Conf.freq, Conf.sweptime, Conf.span, Conf.analyzer_mode, Conf.detector, Conf.revlevel, Conf.rbw, Conf.swepnt)

    meas_file_name = "Walidacja"
    #meas_file_name = 'test'
    code_book_file = "Codebook.csv"
    time.sleep(10)
    meas_file = create_file(meas_file_name)
    print("create file done")
    meas_obj = sing_pat_per_run(ris, analyzer, generator, meas_file, code_book_file)
    print("obj done")
    print(time.time() - t_1)
    #time.sleep(10) time for evacutation
    meas_obj.start_measure()
    print(time.time() - t_1)
    print("Codebook done")
    b_pattern, b_pow = find_best_pattern_element_wise(ris, generator, analyzer, Conf, MEASURE_FILE="dump.csv")
    with open(meas_file, "a+") as f:
        f.write("\n")
        f.write("Optimization \n")
        f.write(f"{b_pattern}; {b_pow}")
        f.close()
    print(time.time() - t_1)
    print("All done")
    exit()