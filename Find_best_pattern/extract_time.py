import os
from matplotlib import pyplot as plt
import numpy as np
from bitstring import BitArray


def calc_hamming_distance(pattern_1: BitArray, pattern_2: BitArray):
    hamming_distance = (pattern_1^pattern_2).count(1)
    return hamming_distance

def extract_from_file(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        time_std = lines[-1]
        mean_time = lines[-2]
        file.close
    previus_pattern = BitArray(uint=0, length=256)
    hamming_distances = []
    time_values = []
    patterns = []
    for line in lines:
        if "END" in line:
            break
        pattern, time = line.split(',')
        patterns.append(pattern)
        pattern = BitArray(hex = pattern)
        hamming = calc_hamming_distance(previus_pattern, pattern)
        hamming_distances.append(hamming)
        time_values.append(time)
        previus_pattern = pattern
    return hamming_distances, time_values, patterns, time_std, mean_time

def plot_time_vs_pattern_hamming(file_name, plot_for_pattern = False):
    hamming_distances, time_values, patterns, Time_std, Mean_time = extract_from_file(file_name)
    if plot_for_pattern:
        p_1 = patterns[1]
        p_2 = patterns[2]
        hamming_distance_for_2_pats = calc_hamming_distance(BitArray(hex=p_1), BitArray(hex=p_2))
        plt.scatter(patterns, time_values, label=f'Hamming Distance between two patterns:: {hamming_distance_for_2_pats}' , marker='x', color='b')
        plt.ylabel("Time for switch")
        plt.xlabel("Patterns")
        plt.title(f"Plot form file:: {file_name.split('/')[-1]}")
    else:
        plt.scatter(hamming_distances, time_values, label=f"Time_std:: {Time_std}, Mean_time:: {Mean_time}", marker='x', color='b')
        plt.ylabel("Time for switch")
        plt.xlabel("Hamming Distance")
        plt.title(f"Plot form file:: {file_name.split('/')[-1]}")
    plt.legend()
    plt.grid()

    return

def save_plot(file_name):
    plt.savefig(file_name)
    plt.close()
    return

if __name__ == "__main__":
    path = os.path.join(os.getcwd(), 'RIS_time_test')
    files = os.listdir(path)
    files = [f for f in files if f.endswith('.csv')]
    files.sort()
    for file in files:
        print(f"Processing file:: {file}")
        if 'rand_patt' in file:
            plot_time_vs_pattern_hamming(os.path.join(path, file))
            save_plot(os.path.join(path, file.split('.')[0] + '.png'))
        else:
            pass
            # plot_time_vs_pattern_hamming(os.path.join(path, file), True)
            # save_plot(os.path.join(path, file.split('.')[0] + '.png'))
    print("Done")
    exit()
