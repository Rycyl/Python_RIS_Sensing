from bitstring import BitArray
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.gridspec import GridSpec
import os

def hamming_distance(pat_one: BitArray, pat_two: BitArray):
    hamming_distance = (pat_one ^ pat_two).count(1)
    return hamming_distance

def extract_from_file(file_name: str):
    with open(file_name, 'r') as f:
        lines = f.readlines()
        f.close()
    min_powers_with_pat = []
    max_powers_with_pat = []
    i = 0
    while True:
        if "MIN" in lines[i]:
            pass
        elif "MAX" in lines[i]:
            break
        else:
            # print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            # print(lines[i])
            # print(lines[i].split(','))
            # print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            powe, pate = lines[i].split(',')
            powe = float(powe)
            pate = BitArray(hex=pate)
            min_powers_with_pat.append((powe,pate))
        i += 1
    i = 0
    start = False
    while i<len(lines):
        if "MAX" in lines[i]:
            start = True
            pass
        elif "MIN" in lines[i]:
            pass
        elif start:
            powe, pate = lines[i].split(',')
            powe = float(powe)
            pate = BitArray(hex=pate)
            max_powers_with_pat.append((powe,pate))
        #print(lines[i])
        i += 1
    min_powers_with_pat.sort(key=lambda tup: tup[0])
    max_powers_with_pat.sort(key=lambda tup: tup[0], reverse=True)
    best_min_pat = min_powers_with_pat[0][1]
    best_max_pat = max_powers_with_pat[0][1]
    lenght = len(min_powers_with_pat)
    min_powers = []
    max_powers = []
    hamming_for_min = []
    hamming_for_max = []
    for j in range(lenght):
        min_powers.append(min_powers_with_pat[j][0])
        max_powers.append(max_powers_with_pat[j][0])
        hamming_min = hamming_distance(best_max_pat, min_powers_with_pat[j][1])
        hamming_max = hamming_distance(best_max_pat, max_powers_with_pat[j][1])
        hamming_for_min.append(hamming_min)
        hamming_for_max.append(hamming_max)
    return min_powers, hamming_for_min, max_powers, hamming_for_max

def plot_hamming_vs_power(file_names: list):
    data_for_plots = []
    for file_name in file_names:
        min_powers, hamming_for_min, max_powers, hamming_for_max = extract_from_file(file_name)
        data_for_plots.append((hamming_for_min, min_powers))
        data_for_plots.append((hamming_for_max ,max_powers))
    
    lenght = int(len(data_for_plots)//2)
    fig = plt.figure(figsize=(15, 7))
    gs = GridSpec(2, lenght, figure=fig)
    axs = []
    j = 0
    for i in range(lenght):
        axs.append(fig.add_subplot(gs[0, i]))
        axs[i].grid()
        axs[i].scatter(data_for_plots[i+j][0], data_for_plots[i+j][1], label='Min power', marker='o', color='b')
        axs[i].scatter(data_for_plots[i+j+1][0], data_for_plots[i+j+1][1], label='Max power', marker='x', color='r')
        j+=1
        axs[i].set_xlabel('Hamming distance')
        axs[i].set_ylabel('Power')
        axs[i].set_title(f'Power Minimization to Maximization for Pos {i}')
    
    fin_ax = fig.add_subplot(gs[1, :])
    fin_ax.grid()
    j=0
    colors = ['b', 'r', 'c', 'm', 'g', 'y']
    for i in range(lenght):
        fin_ax.scatter(data_for_plots[i+j][0], data_for_plots[i+j][1], label='Min power', marker='o', color=colors[i+j])
        fin_ax.scatter(data_for_plots[i+j+1][0], data_for_plots[i+j+1][1], label='Max power', marker='x', color=colors[i+j+1])
        j+=1
        fin_ax.set_xlabel('Hamming distance')
        fin_ax.set_ylabel('Power')
        fin_ax.set_title('Power Minimization to Maximization')
        
    fig.legend(loc = 'outside right upper')
    return 'AAAAAAAAAAAAAAAAA'

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
    #############################################
    date = "21-11"
    #############################################
    
    path = os.getcwd()
    path = os.path.join(path, 'Wyniki', date)
    mes_file_list = ['2D_meas_Rx_1_RISpos__1.csv', '2D_meas_Rx_1_RISpos__2.csv', '2D_meas_Rx_1_RISpos__3.csv']
    mes_file_list = [os.path.join(path, file) for file in mes_file_list]
    mes_file_list.sort()
    plot_hamming_vs_power(mes_file_list)
    save_plots_to_pdf('2D_meas_Rx_1.pdf')
    exit()
