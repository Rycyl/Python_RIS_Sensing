from analyzer_sensing import Analyzer
from generator import Generator
from RIS import RIS
from element_by_element import sing_pat_per_run, element_by_element, stripe_by_stripe
from config_obj import Config
from file_creator import create_file
from time import time, sleep
from search_patterns import find_best_pattern_element_wise
from get_distances import UWB_module
from get_angle import Antenna_Geometry

if __name__ == "__main__":
    Conf = Config()
    phy_device_input = True
    ris_dist = 0.26

    analyzer = Analyzer(Conf, phy_device_input)
    generator = Generator(Conf, phy_device_input)
    ris = RIS(port='/dev/ttyUSB0', phy_device=phy_device_input)
    print("RIS done")
    generator.meas_prep(True, Conf.generator_mode, Conf.generator_amplitude, Conf.freq)
    analyzer.meas_prep(Conf.freq, Conf.sweptime, Conf.span, Conf.analyzer_mode, Conf.detector, Conf.revlevel, Conf.rbw, Conf.swepnt)
    # GENERATOR.meas_prep(True, Conf.generator_mode, Conf.generator_amplitude, Conf.freq)
    # ANALYZER.meas_prep(Conf.freq, Conf.sweptime, Conf.span, Conf.analyzer_mode, Conf.detector, Conf.revlevel, Conf.rbw, Conf.swepnt)

    meas_file_name = "Code_Book_test_with_angles"
    #meas_file_name = 'test'
    code_book_file = "Codebook.csv"
    meas_file = create_file(meas_file_name)
    
    UWB_A0 = UWB_module()
    geometry_obj = Antenna_Geometry(UWB_A0, ris_dist)
    meas_obj = sing_pat_per_run(ris, analyzer, generator, geometry_obj, meas_file, code_book_file)

    sleep(10)
    start_time = time()
    meas_obj.start_measure()
    print(f"Done, time taken {time()-start_time}")
    exit()

















































    # start = time.time()
    # b_pattern, b_pow = find_best_pattern_element_wise(ris, generator, analyzer, Conf, MEASURE_FILE="dump.csv")
    # meas_file = create_file(meas_file_name)
    # print("End of Old EbE: ", time.time() - start)
    # #print("create file done")
    # meas_obj = element_by_element(ris, analyzer, generator, meas_file)#stripe_by_stripe(ris, analyzer, generator, meas_file)# #sing_pat_per_run(ris, analyzer, generator, meas_file, code_book_file)
    # meas_obj_strip = stripe_by_stripe(ris, analyzer, generator, meas_file)
    # #print("obj done")
    # #print(time.time() - t_1)
    # #time.sleep(10) time for evacutation
    # start = time.time()
    # meas_obj.start_measure()
    # print("End of New EbE: ", time.time()-start)
    # start = time.time()
    # meas_obj_strip.start_measure()
    # print("End of SbS: ", time.time()-start)

    # #print(time.time() - t_1)
    # #print("Codebook done")
    # # 
    # Nb_pattern, Nb_pow = meas_obj.ret_best()
    # Nb_strip_pattern, Nb_strip_pow = meas_obj_strip.ret_best()
    # with open(meas_file, "a+") as f:
    #     f.write("\n")
    #     f.write("Old \n")
    #     f.write(f"{b_pattern}; {b_pow}\n")
    #     f.write("New \n")
    #     f.write(f"{Nb_pattern}; {Nb_pow}\n")
    #     f.write("New strip\n")
    #     f.write(f"{Nb_strip_pattern}; {Nb_strip_pow}\n")
    #     f.close()
    # #print(time.time() - t_1)
    # print("All done")
    # exit()