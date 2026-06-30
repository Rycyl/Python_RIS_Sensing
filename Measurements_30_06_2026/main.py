from re import sub
from analyzer_sensing import Analyzer
#from generator import Generator
from RIS import RIS
from element_by_element import sing_pat_per_run, element_by_element, stripe_by_stripe
from config_obj import Config
from file_creator import create_file, save_to_file
from time import time, sleep
from get_distances import UWB_module_DWM1001
from get_angle import Antenna_Geometry_MDEK1001
import os
import numpy as np


def beep_function(duration=0.1, freq=860, n_beebs=10):
    for _ in range(0, n_beebs):
        os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
        sleep(duration)
    return

if __name__ == "__main__":
    '''------------------------------------Initial Setup--------------------------------------------'''
    Conf = Config()
    phy_device_input = True
    
    a_val = 3.55
    c_val = 3.98
    e_val = 1.31
    h_val = 7.02

    num_of_possitions = 22 #24 #Set how many possitions will be measured

    '''
    Do you want a referance??: 
        for yes set eather strip or element
            strip - optimalization column by column, fast but works only if azimuth is the same accros Tx-RIS-Rx
            element - slow and prone to errors from noise but can work no matter the azimuth
        for no set 0, false or None
    '''
    ref = 'strip' 
    ref_min = True

    ref_carriers = np.linspace(0, 789, 10, dtype=np.int32)



    '''Name of directory where codebooks are stored, assumes that directory is in the same folder as main'''
    codebook_dir = 'codebooks'
    codebook_dir_w_sep = os.path.sep + codebook_dir

    custom_sweptime = 0
    if custom_sweptime:
        Conf.update_swt(custom_sweptime)

    '''Analyzer and Generator initialisation'''
    analyzer = Analyzer(Conf, phy_device_input)
    #generator = "DUMMY GENERATOR -- RUN WAVEFORM MANUALY"#Generator(Conf, phy_device_input)

    '''RIS preperation'''
    ris = RIS(port="", use_socket=True)
    print("RIS Connected")

    '''UWB preperation'''
    uwb = UWB_module_DWM1001()
    print('UWB Tag connected')
    #devices_ids = ["0F83", "D599", "870B", "4F96"] #UWB Anchor IDs, used for UWB response parsing
    a3_id = "9D15"
    ris_id="D599"

    '''Generator and Analyzer preperation'''
    #generator.meas_prep(True, Conf.generator_mode, Conf.generator_amplitude, Conf.freq) #Use if generator connected
    analyzer.meas_prep(Conf.freq, Conf.sweptime, Conf.span, Conf.analyzer_mode, Conf.detector, Conf.revlevel, Conf.rbw, Conf.swepnt, swtcnt=1, sweptype= Conf.sweep_type)
    '''----------------------------------------------------------------------------------------------'''

    '''Script for loading in codebooks, replace codebook_dir with proper dir name if nessecery'''
    codebooks = []
    path = os.path.dirname(os.path.realpath(__file__)) + codebook_dir_w_sep
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.csv'):
                codebooks.append(file)
    
    print(codebooks)
    '''----------------------------------------------------------------------------------------------'''


    print("Creating geometry obj... ")
    geometry_obj = Antenna_Geometry_MDEK1001(uwb, a3_id=a3_id, ris_id=ris_id)
    geometry_obj.lines_treshold = 100
    geometry_obj.n_sigma = 2
    geometry_obj.stat_mode = 'mean'

    #angle = geometry_obj.get_angles(Print_vals=False, a=[a_val], c=[c_val], e=[e_val], h=[h_val])
    angle = ('alfa', "beta")
    print("ANGLE\n", angle)
    print("Geometry obtained")
    ref_obj = []
    ref_files = []
    if ref:
        for c in ref_carriers:
            meas_file_ref = create_file(f'ref_{ref}_by_{ref}_carrier_{c}')
            if ref == 'strip':
                meas_obj_ref = stripe_by_stripe(ris, analyzer, meas_file_ref ,Get_Men_Pow= False, Geometry=angle, subcar_to_maxi=(c, c+10))
                if ref_min:
                    meas_file_ref_min = create_file(f'ref_{ref}_by_{ref}_carrier_{c}_min')
                    meas_obj_ref_min = stripe_by_stripe(ris, analyzer, meas_file_ref ,Get_Men_Pow= False, Geometry=angle, find_min=True, subcar_to_maxi=(c, c+10))
            elif ref == 'element':
                meas_obj_ref = element_by_element(ris, analyzer, meas_file_ref, Get_Men_Pow= False, subcar_to_maxi=(c, c+10)) # TODO Geometry for element by element
                if ref_min:
                    meas_file_ref_min = create_file(f'ref_{ref}_by_{ref}_carrier_{c}_min')
                    meas_obj_ref_min = element_by_element(ris, analyzer, meas_file_ref, Get_Men_Pow= False, find_min=True, subcar_to_maxi=(c, c+10))
            else:
                meas_obj_ref = stripe_by_stripe(ris, analyzer, meas_file_ref ,Get_Men_Pow= False, Geometry=angle, subcar_to_maxi=(c, c+10))
                if ref_min:
                    meas_file_ref_min = create_file(f'ref_{ref}_by_{ref}_carrier_{c}_min')
                    meas_obj_ref_min = stripe_by_stripe(ris, analyzer, meas_file_ref ,Get_Men_Pow= False, Geometry=angle, find_min=True, subcar_to_maxi=(c, c+10))
            ref_obj.append(meas_obj_ref)
            ref_files.append(meas_file_ref)
            if ref_min:
                ref_obj.append(meas_obj_ref_min)
                ref_files.append(meas_file_ref_min)

    meas_files = [create_file(file.strip('.csv')) for file in codebooks]
    
    print("creating codebook meas obj...")

    codebook_meas_objcts = []
    for i in range(len(meas_files)):
        meas_obj = sing_pat_per_run(ris, analyzer, meas_files[i], os.path.join(os.getcwd(),codebook_dir,codebooks[i]), False, angle) #TODO check if path join works correctly
        codebook_meas_objcts.append(meas_obj)
    print("All good starting in 10 seconds...")
    sleep(10)
    total_time_start = time()
    n = 0
    while True:
        codebook_data = []
        ref_data = []
        start_time = time()
        print("Acquiring geometry.... ")
        new_angle = geometry_obj.get_angles(Print_vals=False, a=[a_val], c=[c_val], e=[e_val], h=[h_val])
        print("Measuring....")
        if ref:
            print("Now doing REF")
            for obj in ref_obj:
                obj.change_geometry(new_angle)
                ref_datum = obj.start_measure()
                ref_data.append(ref_datum)
        print("Now doing codebooks")
        for obj in codebook_meas_objcts:
            obj.change_geometry(new_angle)
            datum = obj.start_measure()
            codebook_data.append(datum)
        print(f"Position Done, time taken {time()-start_time}")
        if ref:
            for i in range(len(ref_data)):
                save_to_file(ref_files[i], ref_data[i])
        for i in range(len(codebook_data)):
            save_to_file(meas_files[i], codebook_data[i])

        n += 1
        if n == num_of_possitions or n > num_of_possitions:
            beep_function(duration=1, freq=1720, n_beebs=2)
            break
        else:
            beep_function()
            input("Move to new location, press Eneter when ready to continue... ")
            print("Starting in 10 sec...")
            sleep(10)
            if ref:
                new_ref_files = [os.path.basename(file).split("_30_Jun")[0] for file in ref_files]
                ref_files = [create_file(file) for file in new_ref_files]
            meas_files = [create_file(file.strip('.csv')) for file in codebooks]
            

    print("All Done :)")
    print(f"Time taken for the whole mesurement {time()-total_time_start} seconds")
    exit()
