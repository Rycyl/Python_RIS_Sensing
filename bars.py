import csv
import matplotlib.pyplot as plt
import os
import numpy as np


def read_from_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        data = {}
        for row in reader:
            #print(row)
            pat_name = str(row[1])
            power = float(row[3])
            data[pat_name] = power
    file.close()
    return data

def sort_dict(data):
    return dict(sorted(data.items(), key=lambda item: item[1], reverse=False))

def plot_bars(data, title, xlabel, ylabel, save_path):
    data = sort_dict(data)
    val = data.values()
    val = list(val)
    values = [float(v) for v in val]
    x_vals = data.keys()
    base_value = -73
    y = [value - base_value for value in values ]
    plt.figure(figsize=(12, 8))
    plt.bar(x_vals, y, bottom = base_value)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=50, ha = 'right')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()

def get_file_path(file_name):
    current_file_path = os.path.abspath(__file__)
    current_dir_path = os.path.dirname(current_file_path)
    #parent_dir_path = os.path.dirname(current_dir_path)
    #file_path = os.path.join(parent_dir_path, file_name)
    file_path = os.path.join(current_dir_path, file_name)
    print("--------------------------")
    print(file_path)
    print("--------------------------")
    return file_path

if __name__ == '__main__':
    #sub_dir = 'RPYTHON_RIS_SENSING/'
    file_name = 'Trace_file_z_elewacja3.csv'
    fn = file_name.split('.')[0]
    #dat = sub_dir + file_name
    #file_path = get_file_path(file_name)
    data = read_from_csv(file_name)
    title = 'Moc odebrana w zależności od wybranego wzorca'
    xlabel = 'Wzorzec'
    ylabel = 'Moc [dBm]'
    #sub_dir_save = 'RPYTHON_RIS_SENSING/'
    #save_path = get_file_path(fn + '.png')
    plot_bars(data, fn, xlabel, ylabel, fn+ '.png')
    #żeby to automatycznie przechodziło przez wszystkie pliki w folderze
    #trzeba by zrobić funkcję która w pętli po plikach wywołuje funkcję plot_bars
    