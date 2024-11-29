#import devices OBJ
from analyzer_sensing import Analyzer
from generator import Generator
from config_obj import Config
from RIS import RIS

#import our libs:
import search_patterns 
from plot_trace import run_all, run_main
from save_trace_file import create_results_folder
import sockets

#import 3rd party libs
import os
import time
from bitstring import BitArray
import numpy as np
import  random

def get_random_pattern():
    random_range = 2**256 -1
    return BitArray(uint=random.randint(0, random_range), length=256)


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
    start_pattern = get_random_pattern()
    search_patterns.find_best_pattern_element_wise(ris, generator, analyzer, conf, START_PAT=start_pattern, MEASURE_FILE=file_path, FIND_MIN=True)
    search_patterns.find_best_pattern_element_wise(ris, generator, analyzer, conf, START_PAT=start_pattern, MEASURE_FILE=file_path, FIND_MIN=False)
    return


def main():
    ip_server = '192.168.8.104'  # 104 is a ROCK address
    port = 13245

    conf = Config()

    # Check if physical devices are connected
    phy_device_input = int(input("Czy podłączono fizyczne urządzenia (RIS, Analizator, Generator)? [y=1 / n=0]: "))
    #phy_device_input = True # dla pomiarów

    # Initialize devices and obj
    analyzer = Analyzer(conf, phy_device_input)
    generator = Generator(conf, phy_device_input)
    ris = RIS(port='/dev/ttyUSB0', phy_device=phy_device_input)
    socket = sockets.client_open_socket(ip_server, port)
    # Create results folder
    results_path = create_results_folder()
    print(f"Results will be saved in: {results_path}")

    # Define the filename and create the full path
    filename = "2D_meas_Rx_1_RISpos_"
    
    #making_measures_in_lab()

    #rotate 1_right
    #RH.rotate_right(Header_Steps)
    sockets.client_send_message(socket, message="r")
    #measure_do(filename, results_path, ris, generator, analyzer, conf)

    #1 left
    #RH.rotate_left(Header_Steps)
    sockets.client_send_message(socket, message="l")
    #measure_do(filename, results_path, ris, generator, analyzer, conf)

    #1 left
    #RH.rotate_left(Header_Steps)
    sockets.client_send_message(socket, message="l")
    #measure_do(filename, results_path, ris, generator, analyzer, conf)

    #back head do origin
    #1 right
    #RH.rotate_right(Header_Steps)
    sockets.client_send_message(socket, message="r")
    return

if __name__ == "__main__":
    main()