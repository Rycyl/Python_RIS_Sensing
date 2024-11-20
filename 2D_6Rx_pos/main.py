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

def create_csv_file(trace_file_name):
    i = 1
    while True:
        filename = f"{trace_file_name}_{i}.csv"
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                file.close()
            return filename
        else:
            i += 1

def making_measures_in_lab():
    time.sleep(60) #wait a minute to let us go away
    return


def measure_do(filename):
    filename = create_csv_file(filename)
    file_path = os.path.join(results_path, filename)
    # perform measure
    search_patterns.find_best_pattern_element_wise(Ris, Generator, Analyzer, Config, MEASURE_FILE=filename, FIND_MIN=True)
    search_patterns.find_best_pattern_element_wise(Ris, Generator, Analyzer, Config, MEASURE_FILE=filename, FIND_MIN=False)
    return


def main():
    Config = Config()
    Header_Steps = 10 # chyba 9 stopni

    # Check if physical devices are connected
    phy_device_input = bool(input("Czy podłączono fizyczne urządzenia (RIS, Analizator, Generator)? [y=1 / n=0]: "))
    #phy_device_input = True # dla pomiarów

    # Initialize devices
    Analyzer = Analyzer(config, phy_device_input)
    Generator = Generator(config, phy_device_input)
    Ris = RIS(port='/dev/ttyUSB0', phy_device=phy_device_input)
    Remote_Head = Remote_Head(Config)

    ##SETUP REMOTE HEAD
    Remote_Head.resolution(2)

    # Create results folder
    results_path = create_results_folder()
    print(f"Results will be saved in: {results_path}")

    # Define the filename and create the full path
    filename = "2D_meas_Rx_1_RISpos_"
    
    #making_measures_in_lab()

    #rotate 1_right
    Remote_Head.rotate_right(10)
    measure_do(filename)

    #1 left
    Remote_Head.rotate_left(10)
    measure_do(filename)

    #1 left
    Remote_Head.rotate_left(10)
    measure_do(filename)

    #back head do origin
    #1 right
    Remote_Head.rotate_right(10)
    return

if __name__ == "__main__":
    main()