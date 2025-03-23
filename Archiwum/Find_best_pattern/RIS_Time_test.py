from RIS import RIS
import random
from bitstring import BitArray
from time import time
import numpy as np


def get_random_pattern():
    random_range = 2**256 -1
    return BitArray(uint=random.randint(0, random_range), length=256)


if __name__ == "__main__":
    ris = RIS('/dev/ttyUSB0')
    #print(ris)
    ris.reset()
    meas_file = 'RIS_Time_test_all_off_to_all_on_take_2.csv'
    file = open(meas_file, 'w')
    times_vector = []
    all_off = BitArray(uint=0, length=256)
    all_on = BitArray(uint=2**256 - 1, length=256)
    stripes_hex = "0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    shifted_stripes_hex = "0x5555555555555555555555555555555555555555555555555555555555555555"
    vertical_stripes_hex = "0xFFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000"
    vertical_stripes = BitArray(hex=vertical_stripes_hex)
    stripes = BitArray(hex=stripes_hex)
    shifted_stripes = BitArray(hex=shifted_stripes_hex)
    for i in range(27200):
        #pattern = get_random_pattern()
        if i % 2 == 0:
            pattern = all_off
        else:
            pattern = all_on
        change_time = ris.set_pattern(pattern)
        times_vector.append(change_time)
        file.write(f"0x{pattern.hex},{change_time}\n")
    file.write("END\n")
    file.write(f"Mean time: {np.mean(times_vector)}\n")
    file.write(f"Std time: {np.std(times_vector)}\n")
    file.close()
    exit()
