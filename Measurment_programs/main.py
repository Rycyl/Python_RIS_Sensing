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



if __name__ == "__main__":
    '''------------------------------------Initial Setup--------------------------------------------'''
    Conf = Config()
    phy_device_input = True

    num_of_possitions = 1 #Set how many possitions will be measured

    '''
    Do you want a referance??: 
        for yes set eather strip or element
            strip - optimalization column by column, fast but works only if azimuth is the same accros Tx-RIS-Rx
            element - slow and prone to errors from noise but can work no matter the azimuth
        for no set 0, false or None
    '''
    ref = 'strip' 

    '''Name of directory where codebooks are stored, assumes that directory is in the same folder as main'''
    codebook_dir = 'codebooks'
    codebook_dir = os.path.sep + codebook_dir

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
    uwb = New_UWB_module()
    print('UWB Tag connected')
    devices_ids = ["0F83", "D599", "870B", "4F96"] #UWB Anchor IDs, used for UWB response parsing

    '''Generator and Analyzer preperation'''
    #generator.meas_prep(True, Conf.generator_mode, Conf.generator_amplitude, Conf.freq) #Use if generator connected
    analyzer.meas_prep(Conf.freq, Conf.sweptime, Conf.span, Conf.analyzer_mode, Conf.detector, Conf.revlevel, Conf.rbw, Conf.swepnt, swtcnt=1, sweptype= Conf.sweep_type)
    '''----------------------------------------------------------------------------------------------'''

    '''Script for loading in codebooks, replace codebook_dir with proper dir name if nessecery'''
    codebooks = []
    path = os.path.dirname(os.path.realpath(__file__)) + codebook_dir
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.csv'):
                codebooks.append(file)
    
    print(codebooks)
    '''----------------------------------------------------------------------------------------------'''


    print("Creating geometry obj... ")
    geometry_obj = Antenna_Geometry_MDEK1001(uwb, *devices_ids)
    angle = geometry_obj.get_angles(Print_vals=True)
    print("ANGLE\n", angle)
    print("Geometry obtained")
    if ref:
        meas_file_ref = create_file(f'ref_{ref}_by_{ref}')
        if ref == 'strip':
            meas_obj_ref = stripe_by_stripe(ris, analyzer, meas_file_ref ,Get_Men_Pow= False, Geometry=angle)
        elif ref == 'element':
            meas_obj_ref = element_by_element(ris, analyzer, meas_file_ref, Get_Men_Pow= False) # TODO Geometry for element by element
        else:
            meas_obj_ref = stripe_by_stripe(ris, analyzer, meas_file_ref ,Get_Men_Pow= False, Geometry=angle)

    meas_files = [create_file(file.strip('.csv')) for file in codebooks]
    


    print("creating codebook meas obj...")

    codebook_meas_objcts = []
    for i in range(len(meas_files)):
        meas_obj = sing_pat_per_run(ris, analyzer, meas_files[i], os.path.join(codebook_dir,codebooks[i]), False, angle) #TODO check if path join works correctly
        codebook_meas_objcts.append(meas_obj)
    print("All good starting in 10 seconds...")
    sleep(10)
    total_time_start = time()
    n = 0
    while True:
        codebook_data = []
        start_time = time()
        print("Acquiring geometry.... ")
        new_angle = geometry_obj.get_angles()
        print("Measuring....")
        if ref:
            print("Now doing REF")
            meas_obj_ref.change_geometry(new_angle)
            ref_data = meas_obj_ref.start_measure()
        print("Now doing codebooks")
        for obj in codebook_meas_objcts:
            obj.change_geometry(new_angle)
            datum = obj.start_measure()
            codebook_data.append(datum)
        print(f"Position Done, time taken {time()-start_time}")
        if ref:
            save_to_file(meas_file_ref, ref_data)
        for i in range(len(codebook_data)):
            save_to_file(meas_files[i], codebook_data[i])

        n += 1
        if n == num_of_possitions or n > num_of_possitions:
            break
        else:
            input("Move to new location, press Eneter when ready to continue... ")
            if ref:
                meas_file_ref = create_file(f'ref_{ref}_by_{ref}')
            meas_files = [create_file(file.strip('.csv')) for file in codebooks]

    print("All Done :)")
    print(f"Time taken for the whole mesurement {time()-total_time_start} seconds")
    exit()
