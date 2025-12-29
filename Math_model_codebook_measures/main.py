from analyzer_sensing import Analyzer
from generator import Generator
from RIS import RIS
from element_by_element import sing_pat_per_run, element_by_element, stripe_by_stripe
from config_obj import Config
from file_creator import create_file, save_to_file
from time import time, sleep
from search_patterns import find_best_pattern_element_wise
from get_distances import UWB_module
from get_angle import Antenna_Geometry, Antenna_Geometry_dummy



if __name__ == "__main__":
    Conf = Config()
    phy_device_input = True
    ris_dist = 0.815
    custom_sweptime = 0
    if custom_sweptime:
        Conf.update_swt(custom_sweptime)

    analyzer = Analyzer(Conf, phy_device_input)
    generator = "DUMMY GENERATOR -- RUN WAVEFORM MANUALY"#Generator(Conf, phy_device_input)
    ris = RIS(port="/dev/ttyUSB0")
    print("RIS done")
    #generator.meas_prep(True, Conf.generator_mode, Conf.generator_amplitude, Conf.freq)
    analyzer.meas_prep(Conf.freq, Conf.sweptime, Conf.span, Conf.analyzer_mode, Conf.detector, Conf.revlevel, Conf.rbw, Conf.swepnt, swtcnt=1, sweptype= Conf.sweep_type)
    # GENERATOR.meas_prep(True, Conf.generator_mode, Conf.generator_amplitude, Conf.freq)
    # ANALYZER.meas_prep(Conf.freq, Conf.sweptime, Conf.span, Conf.analyzer_mode, Conf.detector, Conf.revlevel, Conf.rbw, Conf.swepnt)

    meas_file_name_PK = "Mesure_PK"#"Big_codebook_measure_pos_w_grid_sec_run"
    meas_file_name_Eu_16 = "Mesure_Eu_16"
    meas_file_name_Eu_64 = "Mesure_Eu_64"
    meas_file_name_Eu_16_64 = "Mesure_Eu_16_f_64"
    #meas_file_name = 'test'
    #meas_file_name = "Ref_power_no_ris"
    #code_book_file = "Codebook.csv"
    pk_codebook = "NEW_PK_codebook.csv"
    codebook_16 = "euklides_codebook16.csv"
    codebook_64 = "euklides_codebook64.csv"
    codebook_16_from64 = "euklides_codebook16_from_64.csv"
    meas_file_PK = create_file(meas_file_name_PK)
    meas_file_Eu_16 = create_file(meas_file_name_Eu_16)
    meas_file_Eu_64 = create_file(meas_file_name_Eu_64)
    meas_file_Eu_16_f_64 = create_file(meas_file_name_Eu_16_64)
    print("Measure initated")
    UWB_A0 = "Dummy UWB"#UWB_module()##
    print("UWB connected")
    print("Calculating geometry")
    geometry_obj = Antenna_Geometry_dummy(UWB_A0, ris_dist)
    # while True:
    #     try:
    #         geometry = geometry_obj.get_angles()
    #         break
    #     except:
    #         pass
    print("Geometry obtained")
    print("creating obj...")
    meas_obj_PK = sing_pat_per_run(ris, analyzer, generator, geometry_obj, meas_file_PK, pk_codebook, False)
    meas_obj_eu_16 = sing_pat_per_run(ris, analyzer, generator, geometry_obj, meas_file_Eu_16, codebook_16, False)
    meas_obj_eu_64 = sing_pat_per_run(ris, analyzer, generator, geometry_obj, meas_file_Eu_64, codebook_64, False)
    meas_obj_eu_16_form_64 = sing_pat_per_run(ris, analyzer, generator, geometry_obj, meas_file_Eu_16_f_64, codebook_16_from64, False)
    # stripes_max = stripe_by_stripe(ris, analyzer, generator, geometry_obj, meas_file, False)
    # stripes_min = stripe_by_stripe(ris, analyzer, generator, geometry_obj, meas_file, True)

    print("All good starting in 10 seconds...")
    sleep(10)
    start_time = time()
    print("Measuring....")
    # power = analyzer.trace_get_mean()
    # data_to_save = [[0, "N/A", power, geometry[0], geometry[1], geometry[2], geometry[3], geometry[4], geometry[5], geometry[6],]]
    codebook_PK_data = meas_obj_PK.start_measure()
    codebook_eu_16_data = meas_obj_eu_16.start_measure()
    codebook_eu_64_data = meas_obj_eu_64.start_measure()
    codebook_eu_16_from_64_data = meas_obj_eu_16_form_64.start_measure()
    # stripes_max_data =  stripes_max.start_measure()
    # stripes_min_data = stripes_min.start_measure()
    print(f"Done, time taken {time()-start_time}")
    save_to_file(meas_file_PK, codebook_PK_data)
    save_to_file(meas_file_Eu_16, codebook_eu_16_data)
    save_to_file(meas_file_Eu_64, codebook_eu_64_data)
    save_to_file(meas_file_Eu_16_f_64, codebook_eu_16_from_64_data)
    # save_to_file(meas_file, stripes_max_data)
    # save_to_file(meas_file, stripes_min_data)
    # save_to_file(meas_file, data_to_save)
    print("All Done :)")
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