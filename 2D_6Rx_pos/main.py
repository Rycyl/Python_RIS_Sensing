#import devices OBJ
from analyzer_sensing import Analyzer
from generator import Generator
from config_obj import Config
from RIS import RIS
from remote_head import Remote_Head

#import our libs:
import search_patterns 
from plot_trace import run_all, run_main
from save_trace_file import create_results_folder

#import 3rd party libs
import os
import time

def create_csv_filename(trace_file_name):
    i = 1
    while True:
        filename = f"{trace_file_name}_{i}.csv"
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                file.close()
            return filename
        else:
            i += 1

def create_csv_file(fil):
    with open(fil, 'w') as f:
        f.close()
    return

def making_measures_in_lab():
    time.sleep(10) #wait a minute to let us go away
    return


def measure_do(filename, results_path, ris, generator, analyzer, conf):
    file_path = os.path.join(results_path, filename)
    file_path = create_csv_filename(file_path)
    create_csv_file(file_path)
    print(file_path)
    # perform measure
    search_patterns.find_best_pattern_element_wise(ris, generator, analyzer, conf, MEASURE_FILE=file_path, FIND_MIN=True)
    search_patterns.find_best_pattern_element_wise(ris, generator, analyzer, conf, MEASURE_FILE=file_path, FIND_MIN=False)
    return


def main():
    conf = Config()
    Header_Steps = 10 # chyba 9 stopni

    # Check if physical devices are connected
    phy_device_input = bool(input("Czy podłączono fizyczne urządzenia (RIS, Analizator, Generator)? [y=1 / n=0]: "))
    #phy_device_input = True # dla pomiarów

    # Initialize devices
    analyzer = Analyzer(conf, phy_device_input)
    generator = Generator(conf, phy_device_input)
    ris = RIS(port='/dev/ttyUSB0', phy_device=phy_device_input)
    RH = Remote_Head(conf)

    ##SETUP REMOTE HEAD
    RH.resolution(2)

    # Create results folder
    results_path = create_results_folder()
    print(f"Results will be saved in: {results_path}")

    # Define the filename and create the full path
    filename = "2D_meas_Rx_1_RISpos_"
    
    #making_measures_in_lab()

    #rotate 1_right
    RH.rotate_right(Header_Steps)
    measure_do(filename, results_path, ris, generator, analyzer, conf)

    #1 left
    RH.rotate_left(Header_Steps)
    measure_do(filename, results_path, ris, generator, analyzer, conf)

    #1 left
    RH.rotate_left(Header_Steps)
    measure_do(filename, results_path, ris, generator, analyzer, conf)

    #back head do origin
    #1 right
    RH.rotate_right(Header_Steps)
    return

if __name__ == "__main__":
    main()