import os
import numpy as np
from bitstring import BitArray

def calc_hamming(pat_1: BitArray, pat_2: BitArray):
    hamming = (pat_1 ^ pat_2).count(1)
    return hamming


def extract_from_file(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
        std_time = lines[-1]
        mean_time = lines[-2]
        f.close()
    previus_pattern = BitArray(uint=0, length=256)
    hamming_with_time = {}
    time_with_hamming = {}
    for line in lines[:-2]:
        if "END" in line:
            break
        pattern, time = line.split(",")
        pattern = BitArray(hex=pattern)
        time = float(time)
        hamming = calc_hamming(pattern, previus_pattern)
        previus_pattern = pattern
        hamming_with_time[hamming] = time
        time_with_hamming[time] = hamming
    return hamming_with_time, time_with_hamming, mean_time, std_time

def analize_time(file_name, output_file):
    hamming_with_time, time_with_hamming, mean_time, std_time = extract_from_file(file_name)
    hamming_vals = list(hamming_with_time.keys())
    hamming_vals.sort()
    time_vals = list(time_with_hamming.keys())
    time_vals.sort()
    time_orderd_as_hamming = [hamming_with_time[hamming] for hamming in hamming_vals]
    hamming_orderd_as_time = [time_with_hamming[time] for time in time_vals]
    largest_time = time_vals[-1]
    second_largest_time = time_vals[-2]
    hamming_for_largest_time = hamming_orderd_as_time[-1]
    hamming_for_second_largest_time = hamming_orderd_as_time[-2]
    largest_hamming = hamming_vals[-1]
    try:
        second_largest_hamming = hamming_vals[-2]
    except IndexError:
        second_largest_hamming = "None"
    time_for_largest_hamming = time_orderd_as_hamming[-1]
    time_for_second_largest_hamming = time_orderd_as_hamming[-2]
    smallest_time = time_vals[0]
    second_smallest_time = time_vals[1]
    hamming_for_smallest_time = hamming_orderd_as_time[0]
    hamming_for_second_smallest_time = hamming_orderd_as_time[1]
    smallest_hamming = hamming_vals[0]
    try:
        second_smallest_hamming = hamming_vals[1]
    except IndexError:
        second_smallest_hamming = "None"
    time_for_smallest_hamming = time_orderd_as_hamming[0]
    time_for_second_smallest_hamming = time_orderd_as_hamming[1]
    if second_largest_hamming == smallest_hamming:
        second_largest_hamming = "None"
    with open(output_file, 'w') as f:
        f.write("Basic analisis")
        f.write("\n")
        f.write(mean_time)
        f.write("\n")
        f.write(std_time)
        f.write("\n")
        f.write(f"Largest time:: {largest_time} with hamming distance {hamming_for_largest_time}")
        f.write("\n")
        f.write(f"Second largest time:: {second_largest_time} with hamming distance {hamming_for_second_largest_time}")
        f.write("\n")
        f.write(f"Smallest time:: {smallest_time} with hamming distance {hamming_for_smallest_time}")
        f.write("\n")
        f.write(f"Second smallest time:: {second_smallest_time} with hamming distance {hamming_for_second_smallest_time}")
        f.write("\n")
        f.write(f"Largest hamming distance:: {largest_hamming} with time {time_for_largest_hamming}")
        f.write("\n")
        f.write(f"Second largest hamming distance:: {second_largest_hamming} with time {time_for_second_largest_hamming}")
        f.write("\n")
        f.write(f"Smallest hamming distance:: {smallest_hamming} with time {time_for_smallest_hamming}")
        f.write("\n")
        f.write(f"Second smallest hamming distance:: {second_smallest_hamming} with time {time_for_second_smallest_hamming}")
        f.write("\n")
        f.write("All values")
        f.write("\n")
        for i in range(len(hamming_vals)):
            f.write(f"Hamming Distance: {hamming_vals[i]} Time: {time_orderd_as_hamming[i]}")
            f.write("\n")
        f.close()



if __name__ == "__main__":
    # path = os.getcwd()
    # path = os.path.join(path, "RIS_Time_test")
    # files = [f for f in os.listdir(path) if f.endswith('.csv')]
    # for file in files:
    #     print(f"Analizing file {file}")
    #     analize_time(os.path.join(path, file), os.path.join(path, file.split('.')[0] + "_time_analisis.txt"))
    file = "C:\\Users\\PC\\Documents\\GitHub\\Python_RIS_Sensing\\Find_best_pattern\\RIS_time_test\\RIS_Time_test_rand_patt.csv"
    output_file = file.split('.')[0] + "_time_analisis.txt"
    analize_time(file, output_file)
    print("Done")
    exit()







    