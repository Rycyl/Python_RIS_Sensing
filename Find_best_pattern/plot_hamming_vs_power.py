from bitstring import BitArray
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.gridspec import GridSpec
import os

def hamming_distance(best_patt: BitArray, current_patt: BitArray) -> int:
    hamming_dist = (best_patt ^ current_patt).count(1)
    # if best_patt.uint < current_patt.uint:
    #     return hamming_dist*(-1)
    return hamming_dist


def extract_power_and_pattern(meas_file: str, best_patt = None) -> dict:
    with open(meas_file, 'r') as f:
        lines = f.readlines()
        f.close()
    if best_patt is None:
        best_patt = lines[-1].split(',')[1]
        best_patt = BitArray(hex=best_patt)
    hamming_vs_power = {}
    for line in lines:
        if line.startswith('best'):
            break
        power, patt = line.split(',')
        power = float(power)
        patt = BitArray(hex=patt)
        hamming = hamming_distance(best_patt, patt)
        hamming_vs_power[power] = hamming
    return hamming_vs_power, best_patt


def plot_hamming_vs_power(meas_file_max: str, meas_file_min: str):
    hamming_vs_power, best_patt = extract_power_and_pattern(meas_file_max)
    power_list = list(hamming_vs_power.keys())
    power_list.sort()
    hamming_list = []
    for power in power_list:
        hamming_list.append(hamming_vs_power[power])

    
    min_hamming_vs_power, min_best_patt = extract_power_and_pattern(meas_file_min)
    min_power_list = list(min_hamming_vs_power.keys())
    min_power_list.sort()
    min_hamming_list = []
    for power in min_power_list:
        min_hamming_list.append(min_hamming_vs_power[power])

    
    min_hamming_vs_power_to_max = extract_power_and_pattern(meas_file_min, best_patt)[0]
    min_power_list_to_max = list(min_hamming_vs_power_to_max.keys())
    min_power_list_to_max.sort()
    min_hamming_list_to_max = []
    for power in min_power_list_to_max:
        min_hamming_list_to_max.append(min_hamming_vs_power_to_max[power])


    # min_hamming_list_to_max[:0] = hamming_list
    # min_power_list_to_max[:0] = power_list
    
    fig = plt.figure(figsize=(15, 7))
    gs = GridSpec(2, 2, figure=fig)

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, :])
    ax1.grid()
    ax1.scatter(hamming_list, power_list, label='Max power', marker='x', color='r')
    ax1.set_xlabel('Hamming distance')
    ax1.set_ylabel('Power')
    ax1.set_title('Power Maximilization')
    ax2.grid()
    ax2.scatter(min_hamming_list, min_power_list, label='Min power', marker='o', color='b')
    ax2.set_xlabel('Hamming distance')
    ax2.set_ylabel('Power')
    ax2.set_title('Power Minimization')
    ax3.grid()
    ax3.scatter(hamming_list, power_list, label='Max power', marker='x', color='r')
    ax3.scatter(min_hamming_list_to_max, min_power_list_to_max, label='Min power to max power', marker='o', color='b')
    ax3.set_xlabel('Hamming distance')
    ax3.set_ylabel('Power')
    ax3.set_title('Power Minimization to Maximization')
    
    fig.legend(loc = 'outside right upper')
    fig.suptitle(meas_file_max.split('\\')[-1])

    return "PAIN"


def save_plots_to_pdf(filename: str):
    fig_nums = plt.get_fignums()
    figs = [plt.figure(num) for num in fig_nums]
    p = PdfPages(filename)
    for fig in figs:
        p.savefig(fig)
    p.close()

    plt.close('all')
    return 1


if __name__ == '__main__':
    path = os.getcwd()
    meas_file_name = 'anntena_test_14_11'
    meas_files_min = [f for f in os.listdir(path) if f.endswith('.csv') and f.startswith(meas_file_name) and 'min' in f]
    meas_files_max = [f for f in os.listdir(path) if f.endswith('.csv') and f.startswith(meas_file_name) and not f in meas_files_min]
    for i in range(len(meas_files_min)):
        meas_file_min = os.path.join(path, meas_files_min[i])
        meas_file_max = os.path.join(path, meas_files_max[i])
        plot_hamming_vs_power(meas_file_max, meas_file_min)
        #plt.show()
    save_plots_to_pdf(meas_file_name + '.pdf')
    exit()
        
            

