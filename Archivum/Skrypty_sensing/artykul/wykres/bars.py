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
            pat_name = str(row[0])
            power = float(row[2])
            data[pat_name] = power
    file.close()
    return data

def sort_dict(data):
    return dict(sorted(data.items(), key=lambda item: item[1], reverse=False))

def plot_bars(data, title, xlabel, ylabel, save_path):
    data = sort_dict(data)
    values = data.values()
    values = list(values)
    top_values = max(values) + 2
    bottom_values = min(values) - 10
    values = [value - bottom_values for value in values]
    #print(values)
    plt.figure(figsize=(10, 6))
    plt.bar(data.keys(), np.abs(values), bottom= -85, color = 'dodgerblue')#bottom_values, color='dodgerblue')
    plt.ylim(-85, -66)
    #plt.ylim(bottom_values, top_values)
    #plt.gca().invert_yaxis()
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
    parent_dir_path = os.path.dirname(current_dir_path)
    file_path = os.path.join(parent_dir_path, file_name)
    return file_path

if __name__ == '__main__':
    sub_dir = 'wyniki/TXkier_RXkier/'
    file_name = 'RX_4_100.csv'
    fn = file_name.split('.')[0]
    dat = sub_dir + file_name
    file_path = get_file_path(dat)
    data = read_from_csv(file_path)
    title = 'Moc odebrana w zależności od wybranego wzorca'
    xlabel = 'Wzorzec'
    ylabel = 'Moc [dBm]'
    sub_dir_save = 'TXkier_RXkier/'
    save_path = get_file_path('wykres/' + sub_dir_save + fn + '.png')
    plot_bars(data, title, xlabel, ylabel, save_path)
    #żeby to automatycznie przechodziło przez wszystkie pliki w folderze
    #trzeba by zrobić funkcję która w pętli po plikach wywołuje funkcję plot_bars
    