import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import csv
import os

plt.rcParams["figure.figsize"] = (10, 6)

def save_plots_to_pdf(filname):
    p = PdfPages(filname)
    fig_nums = plt.get_fignums()
    figs = [plt.figure(num) for num in fig_nums]

    for fig in figs:
        fig.savefig(p, format='pdf')

    p.close()

def plot_trace(data):
    header = data[0]
    full_trace = data[1]
    power_slices = data[2]
    patterns = data[3]
    # print(type(power_slices))
    # print(header)
    # print(type(header))
    # print(header[0])
    # exit()
    power_slices.remove('')
    # print(type(power_slices))
    for datum in power_slices:
        if type(datum) == str:
            print("-------------------------------")
            print(datum)
            print("-------------------------------")
            print("FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK FUCK ")
    # print(type(power_slices))
    temp_power_slice = power_slices.copy()
    # print(type(temp_power_slice))
    #temp_power_slice.remove(-150)
    temp_power_slice.sort()
    temp_power_slice = set(temp_power_slice)
    temp_power_slice.remove(-150)
    bottom_y = min(temp_power_slice)
    bottom_y -= 0.5
    #print(bottom_y)
    #bottom_y = -70
    # print(type(power_slices[1]))
    top_y = max(power_slices)
    top_y += 0.5

    all_patterns = set(patterns)
    all_patterns.remove('NONE_PAT')
    all_patterns.remove('')
    all_patterns = list(all_patterns)

    start_end_for_patterns = {}

    for pattern in all_patterns:
        start = patterns.index(pattern)
        end = len(patterns) - patterns[::-1].index(pattern) - 1
        start_end_for_patterns[pattern] = (start, end)
    # print(all_patterns)
    #print(start_end_for_patterns)
    
    x = np.arange(len(full_trace))
    plt.figure()
    plt.subplot(1, 1, 1)
    plt.grid()
    plt.xlabel('Point')
    plt.ylabel('Power')
    plt.title(header[0])
    plt.ylim(bottom_y, top_y)
    plt.xlim(0, len(full_trace))

    plt.plot(x, full_trace, label='Full Trace')

    for pattern in all_patterns:
        start, end = start_end_for_patterns[pattern]
        # print("START------------------------")
        # print(start, end)
        # print("END------------------------")
        x_axis = x[start:end]
        y_axis = power_slices[start:end]
        #print(x_axis)
        plt.plot(x_axis, y_axis, label=pattern)

    #plt.legend(loc = 'outside right upper')

    return 1


def extract_trace(trace_file):
    data = []
    with open(trace_file, 'r') as f:
        trace_reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in trace_reader:
            if len(data) == 4:
                plot_trace(data)
                data = []
            data.append(row)

def run_main(file_path):
    extract_trace(file_path)
    pdfile = file_path.split('.')[0] + '.pdf'
    save_plots_to_pdf(pdfile)
    plt.close('all')


if __name__ == '__main__':
    path = os.getcwd()
<<<<<<< Updated upstream
    filename = 'trace_file_group_444444'
=======
    filename = 'trace_file_group_4'
>>>>>>> Stashed changes
    file_path = os.path.join(path, filename + '.csv')
    extract_trace(file_path)
    save_plots_to_pdf(filename + '.pdf')
    plt.close('all')
    # trace_files = [f for f in os.listdir(path) if f.endswith('.csv') and f.startswith('trace_file_group')]
    # for trace_file in trace_files:
    #     file_path = os.path.join(path, trace_file)
    #     extract_trace(file_path)
    #     save_plots_to_pdf(trace_file.split('.')[0] + '.pdf')
    #     plt.close('all')