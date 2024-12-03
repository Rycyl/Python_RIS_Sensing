from bitstring import BitArray
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.gridspec import GridSpec
import matplotlib.colors as mcolors
import os

def get_n(hamming_dist):
    n = max(hamming_dist)
    plus_n = []
    for H in hamming_dist:
        plus_n.append(n-H)
    return plus_n


def aprox_fun()


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
    fig = plt.figure(figsize=(20, 11))
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
    colors = ['tab:blue', 'tab:red', 'tab:cyan', 'tab:pink', 'tab:green', 'tab:orange', 'tab:olive', 'tab:purple', 'tab:gray', 'tab:brown', 'm', 'k', 'teal', 'crimson' ]
    for i in range(lenght):
        #print(i+j)
        fin_ax.scatter(data_for_plots[i+j][0], data_for_plots[i+j][1], label=f'Min power for pos {i}', marker='o', color=colors[i+j])
        fin_ax.scatter(data_for_plots[i+j+1][0], data_for_plots[i+j+1][1], label=f'Max power for pos {i}', marker='x', color=colors[i+j+1])
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
    date = "30-11"
    file_name = "2D_meas_rand_start_omni_Rx"
    #############################################
    
    path = os.getcwd()
    path = os.path.join(path, 'Wyniki', date)
    mes_file_list_1 = [file for file in os.listdir(path) if file_name + "_1" in file and file.endswith(".csv")]
    mes_file_list_1 = [os.path.join(path, file) for file in mes_file_list_1]
    mes_file_list_1.sort()
    mes_file_list_2 = [file for file in os.listdir(path) if file_name + "_2" in file and file.endswith(".csv")]
    mes_file_list_2 = [os.path.join(path, file) for file in mes_file_list_2]
    mes_file_list_2.sort()
    mes_file_list_3 = [file for file in os.listdir(path) if file_name + "_3" in file and file.endswith(".csv")]
    mes_file_list_3 = [os.path.join(path, file) for file in mes_file_list_3]
    mes_file_list_3.sort()
    mes_file_list_4 = [file for file in os.listdir(path) if file_name + "_4" in file and file.endswith(".csv")]
    mes_file_list_4 = [os.path.join(path, file) for file in mes_file_list_4]
    mes_file_list_4.sort()
    mes_file_list_5 = [file for file in os.listdir(path) if file_name + "_5" in file and file.endswith(".csv")]
    mes_file_list_5 = [os.path.join(path, file) for file in mes_file_list_5]
    mes_file_list_5.sort()
    mes_file_list_6 = [file for file in os.listdir(path) if file_name + "_6" in file and file.endswith(".csv")]
    mes_file_list_6 = [os.path.join(path, file) for file in mes_file_list_6]
    mes_file_list_6.sort()
    mes_file_lists = [mes_file_list_1, mes_file_list_2, mes_file_list_3, mes_file_list_4, mes_file_list_5, mes_file_list_6]
    #mes_file_list = [os.path.join(path, file) for file in mes_file_list]
    #mes_file_list.sort()
    for file_list in mes_file_lists:
        #print(file_list)
        plot_hamming_vs_power(file_list)
    pdf_file = file_name + ".pdf"
    pdf_file = os.path.join(path, pdf_file)
    #print(pdf_file)
    save_plots_to_pdf(pdf_file)
    exit()
