from analyzer_sensing import Analyzer
#from generator import Generator
from RIS import RIS
from element_by_element import sing_pat_per_run, element_by_element, stripe_by_stripe
from config_obj import Config
from file_creator import create_file, save_to_file
from time import time, sleep
from get_distances import New_UWB_module
from get_angle import Antenna_Geometry_MDEK1001
import os



if __name__ == "__main__":
    Conf = Config()
    phy_device_input = True
    ris_dist = 0.815
    custom_sweptime = 0
    if custom_sweptime:
        Conf.update_swt(custom_sweptime)

    analyzer = Analyzer(Conf, phy_device_input)
    #generator = "DUMMY GENERATOR -- RUN WAVEFORM MANUALY"#Generator(Conf, phy_device_input)
    ris = RIS(port="/dev/ttyUSB0")
    uwb = New_UWB_module()
    devices_ids = ["0F83", "D599", "870B", "4F96"]
    print("RIS done")
    #generator.meas_prep(True, Conf.generator_mode, Conf.generator_amplitude, Conf.freq)
    analyzer.meas_prep(Conf.freq, Conf.sweptime, Conf.span, Conf.analyzer_mode, Conf.detector, Conf.revlevel, Conf.rbw, Conf.swepnt, swtcnt=1, sweptype= Conf.sweep_type)
    # GENERATOR.meas_prep(True, Conf.generator_mode, Conf.generator_amplitude, Conf.freq)
    # ANALYZER.meas_prep(Conf.freq, Conf.sweptime, Conf.span, Conf.analyzer_mode, Conf.detector, Conf.revlevel, Conf.rbw, Conf.swepnt)

    #meas_file_name = 'test'
    #meas_file_name = "Ref_power_no_ris"
    #code_book_file = "Codebook.csv"
    codebooks = []
    path = os.path.dirname(os.path.realpath(__file__)) + '/codebooks'
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.csv'):
                codebooks.append(file)
    meas_file_ref = create_file('ref_strp_by_strp')
    meas_files = [create_file(file.strip('.csv')) for file in codebooks]
    print(codebooks)

    print("Measure initated")
    #UWB_A0 = "Dummy UWB"#UWB_module()##
    print("UWB connected")
    print("Calculating geometry")
    geometry_obj = Antenna_Geometry_MDEK1001(uwb, *devices_ids)
    angle = geometry_obj.get_angles(Print_vals=True)
    print("ANGLE\n", angle)
    print("Geometry obtained")
    print("creating obj...")
    meas_obj_ref = stripe_by_stripe(ris, analyzer, meas_file_ref,Get_Men_Pow= False, Geometry=angle)
    codebook_meas_objcts = []

    for i in range(len(meas_files)):
        meas_obj = sing_pat_per_run(ris, analyzer, meas_files[i], "codebooks/"+codebooks[i], False, angle)
        codebook_meas_objcts.append(meas_obj)
    codebook_data = []
    print("All good starting in 10 seconds...")
    sleep(10)
    start_time = time()
    print("Measuring....")
    print("Starting with REF")
    ref_data = meas_obj_ref.start_measure()
    print("Now codebooks")
    for obj in codebook_meas_objcts:
        datum = obj.start_measure()
        codebook_data.append(datum)
    print(f"Done, time taken {time()-start_time}")
    save_to_file(meas_file_ref, ref_data)
    for i in range(len(codebook_data)):
        save_to_file(meas_files[i], codebook_data[i])

    print("All Done :)")
    exit()
