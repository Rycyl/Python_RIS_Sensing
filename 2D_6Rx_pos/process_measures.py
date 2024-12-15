from bitstring import BitArray
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.gridspec import GridSpec
import matplotlib.colors as mcolors
import os
from math import log10, sqrt
from scipy.optimize import curve_fit, Bounds
import numpy as np

def get_n(hamming_dist):
    n = max(hamming_dist)

    # n = 256
    plus_n = []
    for H in hamming_dist:
        n_p_n = n-H
        # n_p_n = max(0, n_p_n)
        # n_p_n = max(n_p_n, n//2)
        plus_n.append(n_p_n)
    # print(plus_n)
    # print(n)
    return plus_n


def aprox_fun(n_plus, z, c):
    # n = 256
    n = int(max(n_plus))
    print("------------------------")
    print(n)
    print("------------------------")
    # print(n_plus)

    range_l = int((n + (1/c))/2)
    x = [i for i in range(range_l, n)]
    print(x)
    # print(c_v)
    # print(n_plus)
    # for n_p in n_plus:
    #     print(2*n_p - n)
    #     print(abs(1+c_v*(2*n_p - n)))
    return [z + 20*log10(1+c*(2*n_p - n)) for n_p in x]
#     return [
#     z_v + 20 * log10(max(1e-10, abs(1 + c_v * (2 * n_p - n))))
#     for n_p in n_plus
# ]



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
    return min_powers, hamming_for_min, max_powers, hamming_for_max, best_min_pat, best_max_pat

def plot_hamming_vs_power(file_names: list, test = False):
    data_for_plots = []
    best_pats = []
    file_names.sort()
    for file_name in file_names:
        min_powers, hamming_for_min, max_powers, hamming_for_max, best_min_pat, best_max_pat = extract_from_file(file_name)
        data_for_plots.append((hamming_for_min, min_powers))
        data_for_plots.append((hamming_for_max ,max_powers))
        c_file = os.path.split(file_name)[-1][:-4]
        best_pats.append((best_max_pat, max(max_powers), c_file))
        best_pats.append((best_min_pat, min(min_powers), c_file))

    help_text = []

    lenght_of_bp = len(best_pats)//2
    for i in range(lenght_of_bp):
        print("-------------------")
        print(i)
        print("--------------------")
        best_pat = best_pats[i][0]
        best_pow = best_pats[i][1]
        ref_pat = best_pats[i+lenght_of_bp][0]
        ref_pow = best_pats[i+lenght_of_bp][1]
        ham = hamming_distance(best_pat, ref_pat)
        power = abs(abs(best_pow)-abs(ref_pow))
        text = f"{"min" if i%2 else "max"} pos:: {best_pats[i][2].split("__")[-1]}, hamming:: {ham}, power dif {power}"
        help_text.append(text)

    # print("-----------------------")
    # print(best_pats)
    # print("-----------------------")
    # print(len(best_pats))
    # print("-----------------------")
    
    lenght = int(len(data_for_plots)//2)
    fig = plt.figure(figsize=(20, 11))
    gs = GridSpec(2, lenght, figure=fig)
    axs = []
    j = 0

    if test:
        xdata = []
        for x in data_for_plots:
            xdata.append(get_n(x[0]))
    else:
        xdata = []
        for x in data_for_plots:
            xdata.append(x[0])

    ydata = [data[1] for data in data_for_plots]

    for i in range(lenght):

        axs.append(fig.add_subplot(gs[0, i]))
        axs[i].grid()
        axs[i].scatter(xdata[i+j], ydata[i+j], label='Min power', marker='o', color='b')
        axs[i].scatter(xdata[i+j+1], ydata[i+j+1], label='Max power', marker='x', color='r')
        j+=1
        axs[i].set_xlabel('Hamming distance')
        axs[i].set_ylabel('Power')
        c_file_name = os.path.split(file_names[i])[1][:-4]

        axs[i].set_title(f'Power Max - Min Pos: {c_file_name.split('_')[-1]} {'Ref' if 'ref' in c_file_name else 'Rand'}')
        #axs[i].set_title(f'Power Minimization to Maximization for Pos {i}')
        #print(file_list[i])
    
    fin_ax = fig.add_subplot(gs[1, :])
    fin_ax.grid()
    j=0
    colors = ['tab:blue', 'tab:red', 'tab:cyan', 'tab:pink', 'tab:green', 'tab:orange', 'tab:olive', 'tab:purple', 'tab:gray', 'tab:brown', 'm', 'k', 'teal', 'crimson' ]
    for i in range(lenght):
        #print(i+j)
        c_file_name = os.path.split(file_names[i])[1][:-4]
        label_min = f'Min pos {c_file_name.split('_')[-1]} {'Ref' if 'ref' in c_file_name else 'Rand'}'
        label_max = f'Max pos {c_file_name.split('_')[-1]} {'Ref' if 'ref' in c_file_name else 'Rand'}'
        fin_ax.scatter(data_for_plots[i+j][0], data_for_plots[i+j][1], label=label_min, marker='o', color=colors[i+j])
        fin_ax.scatter(data_for_plots[i+j+1][0], data_for_plots[i+j+1][1], label=label_max, marker='x', color=colors[i+j+1])
        j+=1
        fin_ax.set_xlabel('Hamming distance')
        fin_ax.set_ylabel('Power')
        fin_ax.set_title('Power Minimization to Maximization')
        fin_ax.legend()
    fig.suptitle(f'From file:: {c_file_name[:-6]}')
    text_str = '\n'.join(help_text)
    fig.text(0.03, 0.91, text_str)
    #fig.legend(loc = 'outside right upper')
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

def fit_to_curve(file_names: list):
    data = []
    for file in file_names:
        min_powers, hamming_for_min, max_powers, hamming_for_max = extract_from_file(file)
        temp_powers = min_powers[:]
        temp_powers.extend(max_powers)
        temp_hamming = hamming_for_min[:]
        temp_hamming.extend(hamming_for_max)
        n_plus = get_n(temp_hamming)
        data.append((temp_powers, n_plus))
    
    lenght = int(len(data)//2)
    # print(lenght)
    # print(len(data))
    if lenght == 0:
        rows = 1
        cols = len(data)
    else:
        rows = 2
        cols = len(data)//2
    fig = plt.figure(figsize=(20, 11))
    fig.tight_layout()
    # print(rows)
    # print(cols)
    gs = GridSpec(rows, cols, figure=fig)
    axs = []
    for i in range(rows):
        for l in range(cols):
            axs.append(fig.add_subplot(gs[i, l]))
            # print('i=',i)
            # print('l=',l)
            # print('lenght=',lenght)
    bound = ([-np.inf, 0], [np.inf, np.inf])
    j = 0
    # print(len(axs))
    for datum in data:
        y_data = datum[0]
        x_data = datum[1]
        # print(j)
        axs[j].grid()
        axs[j].scatter(x_data, y_data, marker='x', color='b')
        popt, pcov = curve_fit(aprox_fun, x_data, y_data, bounds=bound)
        axs[j].scatter(x_data, aprox_fun(x_data, *popt), color='r', label=f'fit:: z={popt[0]}, c={popt[1]}')
        axs[j].legend()
        c_file_name = os.path.split(file_names[j])[1][:-4]
        axs[j].set_title(f'Power Max - Min Pos: {c_file_name.split('_')[-1]} {'Ref' if 'ref' in c_file_name else 'Rand'}')
        j +=1

    fig.suptitle(f'From file:: {c_file_name}')
    return axs

def get_just_pow(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
        f.close()
    max_pow = []
    min_pow = []
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
            #pate = BitArray(hex=pate)
            min_pow.append(powe)
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
            # pate = BitArray(hex=pate)
            max_pow.append(powe)
        #print(lines[i])
        i += 1
    return min_pow, max_pow

def element_by_element_pow(file_names: list):
    max_pows = []
    min_pows = []
    for file in file_names:
        min_pow, max_pow = get_just_pow(file)
        max_pows.append(max_pow)
        min_pows.append(min_pow)
    x = [i for i in range(len(max_pows[0])-1)]

    max_data = []

    for max_pow in max_pows:
        # print("----------------------")
        # print("Max_pow")
        # print(len(max_pow))
        # #print(max_pow)
        # print("-----------------------")
        pre_switch_temp = []
        post_switch_temp = []
        for i in range(len(max_pow)-1):
            # print(i)
            # print(i+1)
            pre_switch_temp.append(max_pow[i])
            post_switch_temp.append(max_pow[i+1])
        #print(len(post_switch_temp))
        max_data.append((pre_switch_temp, post_switch_temp))
    
    min_data = []

    for min_pow in min_pows:
        # print("-------------------------")
        # print("min_pow")
        # print(len(min_pow))
        # #print(min_pow)
        # print("-------------------------")
        pre_switch_temp = []
        post_switch_temp = []
        for i in range(len(min_pow)-1):
            # print(i)
            # print(i+1)
            pre_switch_temp.append(min_pow[i])
            post_switch_temp.append(min_pow[i+1])
        min_data.append((pre_switch_temp, post_switch_temp))

    fig_max = plt.figure(figsize=(20, 11))
    fig_min = plt.figure(figsize=(20, 11))

    lenght = len(min_data)//2

    if lenght == 0:
        rows = 1
        cols = len(min_data)
    else:
        rows = 2
        cols = len(min_data)//2

    gs_x = GridSpec(rows, cols, figure=fig_max)
    gs_n = GridSpec(rows, cols, figure=fig_min)

    axs_x = []
    axs_n = []

    for i in range(rows):
        for j in range(cols):
            axs_x.append(fig_max.add_subplot(gs_x[i, j]))
            axs_n.append(fig_min.add_subplot(gs_n[i, j]))

 
    #print(pre_switch_max)
    c_file_name = file_names[0]
    #print(c_file_name)
    #print(file_names[0])
    c_file_name = os.path.split(c_file_name)[-1]
    c_file_name = c_file_name[:-4]

    a_max = []

    for pre, post in max_data:
        a_temp = []
        # print("---------------------")
        # # print(len(pre))
        # # #print(pre)
        # # print(len(post))
        # print("----------------------")
        for i in range(len(pre)):
            pre_lin = 10**(pre[i]/10)
            post_lin = 10**(post[i]/10)
            a_i = abs((sqrt(post_lin) - sqrt(pre_lin))/2)
            a_temp.append(a_i)
        a_max.append(a_temp)

    a_min = []

    for pre, post in min_data:
        a_temp = []
        for i in range(len(pre)):
            pre_lin = 10**(pre[i]/10)
            post_lin = 10**(post[i]/10)
            a_i = abs((sqrt(post_lin) - sqrt(pre_lin))/2)
            a_temp.append(a_i)
        a_min.append(a_temp)

    k = 0
    for a in a_max:
        a.sort(key=lambda tup: tup[0])
        axs_x[k].grid()
        axs_x[k].plot(x, a[0], color = 'r', marker = 'o', label='normal')
        axs_x[k].plot(x, a[1], color = 'r', marker = 'x', label='ref')
        axs_x[k].set_title(f"Max from file {c_file_name}")
        axs_x[k].legend()
        k += 1        

    k = 0
    for a in a_min:
        a.sort(key=lambda tup: tup[0])
        axs_x[k].grid()
        axs_x[k].plot(x, a[0], color = 'r', marker = 'o', label='normal')
        axs_x[k].plot(x, a[1], color = 'r', marker = 'x', label='ref')
        axs_n[k].set_title(f"Min from file {c_file_name}")
        axs_n[k].legend()
        k += 1

    # k = 0
    # #print(c_file_name)
    # for pre, post in max_data: #(pre_switch_max, post_switch_max):
    #     axs_x[k].grid()
    #     axs_x[k].scatter(x, pre, color = 'b', marker = 'o', label='pre switch')
    #     axs_x[k].scatter(x, post, color = 'r', marker = 'x', label='post switch')
    #     axs_x[k].set_title(f"Max from file {c_file_name}")
    #     axs_x[k].legend()
    #     k += 1
        
    # k = 0
    # for pre, post in min_data:
    #     axs_n[k].grid()
    #     axs_n[k].plot(x, pre, color = 'b', marker = 'o', label='pre switch')
    #     axs_n[k].plot(x, post, color = 'r', marker = 'x', label='post switch')
    #     axs_n[k].set_title(f"Min from file {c_file_name}")
    #     axs_n[k].legend()
    #     k += 1

    # fig_max.suptitle(f'From file:: {c_file_name}')
    # fig_min.suptitle(f'From file:: {c_file_name}')
    return


def element_by_element_pow_with_ref(file_names: list, all_file_names: list):
    max_pows = []
    min_pows = []
    max_pows_ref = []
    min_pows_ref = []
    for file in file_names:
        if "ref" in file:
            continue
        else:
            file_n = os.path.split(file)[-1]
            loc = file_n.split("_")[6]
            pos = file_n.split("_")[-1].split(".")
        min_pow, max_pow = get_just_pow(file)
        max_pows.append(max_pow)
        min_pows.append(min_pow)
        for f in all_file_names:
            file_n = os.path.split(f)[-1]
            # print("--------------------")
            # print(file_n)
            # print("--------------------")
            if file_n.split("_")[6] == loc and file_n.split("_")[-1].split(".") == pos and "ref" in file_n:
                print("------------------")
                print(file_n)
                print("-------------------")
                min_pow_ref, max_pow_ref = get_just_pow(f)
                min_pows_ref.append(min_pow_ref)
                max_pows_ref.append(max_pow_ref)
                break
    #print(max_pows)
    #print(len(max_pows[0]))
    x = [i for i in range(len(max_pows[0])-1)]

    max_data = []

    for max_pow in max_pows:
        # print("----------------------")
        # print("Max_pow")
        # print(len(max_pow))
        # #print(max_pow)
        # print("-----------------------")
        pre_switch_temp = []
        post_switch_temp = []
        for i in range(len(max_pow)-1):
            # print(i)
            # print(i+1)
            pre_switch_temp.append(max_pow[i])
            post_switch_temp.append(max_pow[i+1])
        #print(len(post_switch_temp))
        max_data.append((pre_switch_temp, post_switch_temp))
    
    min_data = []

    for min_pow in min_pows:
        # print("-------------------------")
        # print("min_pow")
        # print(len(min_pow))
        # #print(min_pow)
        # print("-------------------------")
        pre_switch_temp = []
        post_switch_temp = []
        for i in range(len(min_pow)-1):
            # print(i)
            # print(i+1)
            pre_switch_temp.append(min_pow[i])
            post_switch_temp.append(min_pow[i+1])
        min_data.append((pre_switch_temp, post_switch_temp))
    
    max_ref_data = []

    for max_pow in max_pows_ref:
        # print("----------------------")
        # print("Max_pow")
        # print(len(max_pow))
        # #print(max_pow)
        # print("-----------------------")
        pre_switch_temp = []
        post_switch_temp = []
        for i in range(len(max_pow)-1):
            # print(i)
            # print(i+1)
            pre_switch_temp.append(max_pow[i])
            post_switch_temp.append(max_pow[i+1])
        #print(len(post_switch_temp))
        max_ref_data.append((pre_switch_temp, post_switch_temp))

    min_ref_data = []

    for min_pow in min_pows_ref:
        # print("-------------------------")
        # print("min_pow")
        # print(len(min_pow))
        # #print(min_pow)
        # print("-------------------------")
        pre_switch_temp = []
        post_switch_temp = []
        for i in range(len(min_pow)-1):
            # print(i)
            # print(i+1)
            pre_switch_temp.append(min_pow[i])
            post_switch_temp.append(min_pow[i+1])
        min_ref_data.append((pre_switch_temp, post_switch_temp))

    fig_max = plt.figure(figsize=(20, 11))
    fig_min = plt.figure(figsize=(20, 11))

    lenght = len(min_data)//2

    if lenght == 0:
        rows = 1
        cols = len(min_data)
    else:
        rows = 2
        cols = len(min_data)//2

    gs_x = GridSpec(rows, cols, figure=fig_max)
    gs_n = GridSpec(rows, cols, figure=fig_min)

    axs_x = []
    axs_n = []

    for i in range(rows):
        for j in range(cols):
            axs_x.append(fig_max.add_subplot(gs_x[i, j]))
            axs_n.append(fig_min.add_subplot(gs_n[i, j]))

 
    #print(pre_switch_max)
    c_file_name = file_names[0]
    #print(c_file_name)
    #print(file_names[0])
    c_file_name = os.path.split(c_file_name)[-1]
    c_file_name = c_file_name[:-4]

    a_max = []

    for pre, post in max_data:
        a_temp = []
        # print("---------------------")
        # # print(len(pre))
        # # #print(pre)
        # # print(len(post))
        # print("----------------------")
        for i in range(len(pre)):
            pre_lin = 10**(pre[i]/10)
            post_lin = 10**(post[i]/10)
            a_i = (sqrt(post_lin) - sqrt(pre_lin))/2
            a_i = abs(a_i)
            a_temp.append(a_i)
        a_max.append(a_temp)

    a_min = []

    for pre, post in min_data:
        a_temp = []
        for i in range(len(pre)):
            pre_lin = 10**(pre[i]/10)
            post_lin = 10**(post[i]/10)
            a_i = (sqrt(post_lin) - sqrt(pre_lin))/2
            a_i = abs(a_i)
            a_temp.append(a_i)
        a_min.append(a_temp)

    a_ref_min = []

    for pre, post in min_ref_data:
        a_temp = []
        for i in range(len(pre)):
            pre_lin = 10**(pre[i]/10)
            post_lin = 10**(post[i]/10)
            a_i = (sqrt(post_lin) - sqrt(pre_lin))/2
            a_i = abs(a_i)
            a_temp.append(a_i)
        a_ref_min.append(a_temp)

    a_ref_max = []

    for pre, post in max_ref_data:
        a_temp = []
        for i in range(len(pre)):
            pre_lin = 10**(pre[i]/10)
            post_lin = 10**(post[i]/10)
            a_i = (sqrt(post_lin) - sqrt(pre_lin))/2
            a_i = abs(a_i)
            a_temp.append(a_i)
        a_ref_max.append(a_temp)
    
    a_max_w_ref = []
    #print(a_ref_max)
    #print(len(a_max))
    for i in range(len(a_max)):
        temp = []
        with open ("debug.txt", "a+") as dfile:
            dfile.write("####################\n")
            dfile.write(str(a_max))
            dfile.write("\n")
            dfile.write(str(a_ref_max))
            dfile.write("\n")
        for j in range(len(a_max[i])):
            temp.append((a_max[i][j], a_ref_max[i][j]))
        a_max_w_ref.append(temp)

    a_min_w_ref = []

    for i in range(len(a_min)):
        temp = []
        for j in range(len(a_min[i])):
            temp.append((a_min[i][j], a_ref_min[i][j]))
        a_min_w_ref.append(temp)

    k = 0
    for a in a_max_w_ref:
        a.sort(key=lambda tup: tup[0])
        reg = [i[0] for i in a]
        ref = [i[1] for i in a]
        axs_x[k].grid()
        axs_x[k].plot(x, reg, color = 'r', marker = 'o', label='normal')
        axs_x[k].plot(x, ref, color = 'b', marker = 'x', label='ref')
        axs_x[k].set_title(f"Max from file {c_file_name}")
        axs_x[k].legend()
        k += 1        

    k = 0
    for a in a_min_w_ref:
        a.sort(key=lambda tup: tup[0])
        reg = [i[0] for i in a]
        ref = [i[1] for i in a]
        axs_n[k].grid()
        axs_n[k].plot(x, reg, color = 'r', marker = 'o', label='normal')
        axs_n[k].plot(x, ref, color = 'b', marker = 'x', label='ref')
        axs_n[k].set_title(f"Min from file {c_file_name}")
        axs_n[k].legend()
        k += 1
    return


if __name__ == '__main__':
    #############################################
    date = "30-11"
    file_name = "2D_meas_rand_start_omni_Rx"
    #file_name = "2D_meas_Rx_1_RISpos_"
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
    
    # for file_list in mes_file_lists:
    #     plot_hamming_vs_power(file_list)
    # pdf_file = file_name + '_V4.pdf'
    # pdf_file = os.path.join(path, pdf_file)
    # save_plots_to_pdf(pdf_file)

    for file_list in mes_file_lists:
        for file in file_list:
            if "ref" in file:
                continue
            file_tab = [file]
            element_by_element_pow_with_ref(file_tab, file_list)
    pdf_file_pow_dif = file_name + "_pow_dif_ref.pdf"
    pdf_file_pow_dif = os.path.join(path, pdf_file_pow_dif)
    save_plots_to_pdf(pdf_file_pow_dif)

    # for file_list in mes_file_lists:
    #     for file in file_list:
    #         file_tab = [file]
    #         fit_to_curve(file_tab)
    # pdf_file_curve_fit = file_name + "_curve_fit.pdf"
    # pdf_file_pow_dif = os.path.join(path, pdf_file_curve_fit)
    # save_plots_to_pdf(pdf_file_curve_fit)

    # for file_list in mes_file_lists:
    #     #print(file_list)
    # #     plot_hamming_vs_power(file_list)
    # pdf_file = file_name + "V2.pdf"
    # pdf_file = os.path.join(path, pdf_file)
    # #print(pdf_file)
    # save_plots_to_pdf(pdf_file)
    # print(mes_file_list_1)
    # fit_to_curve(mes_file_list_1)
    # pdf_file_curve = file_name + "curve_fit.pdf"
    # pdf_file_curve = os.path.join(path, pdf_file_curve)
    # save_plots_to_pdf(pdf_file_curve)
    # element_by_element_pow(mes_file_list_1)
    # pdf_file_pow_dif = file_name + "pow_dif.pdf"
    # pdf_file_pow_dif = os.path.join(path, pdf_file_pow_dif)
    # save_plots_to_pdf(pdf_file_pow_dif)
    exit()
