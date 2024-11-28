from matplotlib import pyplot as plt
import os
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from bitstring import BitArray

def extract_data_from_file(file_name, date):
    path = os.getcwd()
    file_path = os.path.join(path, "Wyniki", date, file_name)
    max_powers_n_patts = {}
    min_powers_n_patts = {}
    with open (file_path, "r") as f:
        lines = f.readlines()
        f.close()
    start = False
    for line in lines:
        if "MAX" in line and not start:
            start = True
        elif "MIN" in line:
            break
        else:
            pass
        power, pattern = line.split(",")
        power = float(power)
        max_powers_n_patts[pattern] = power

    start = False
    for line in lines:
        if "MIN" in line and not start:
            start = True
        elif "MAX" in line:
            break
        else:
            pass
        power, pattern = line.split(",")
        power = float(power)
        min_powers_n_patts[pattern] = power
    
    return max_powers_n_patts, min_powers_n_patts

def plot_from_files(file_start, date):
    path = os.getcwd()
    path = os.path.join(path, "Wyniki", date)
    files = [f for f in os.listdir(path) if f.endswith(".csv") and f.startswith(file_start)]
    files.sort()
    extracted_data = []
    for file in files:
        max_pows, min_pows = extract_data_from_file(file, date)
        extracted_data.append((max_pows, min_pows))
    x_vect = np.linspace(0, 256)
    colors = ["r", "b", "m", "c", "g", "k"]
    fig = plt.figure(layout= 'constrained', figsize= (15, 7))
    plt.subplot(1,1,1)
    plt.grid()
    for data in extracted_data:
        max_power = data[0].vals()
        min_power = data[1].vals()
        plt.plot(x_vect, max_power, c=colors.pop())
        plt.plot(x_vect, max_power, c=colors.pop())
    return 1


if __name__ == "__main__":
    