import csv
import matplotlib.pyplot as plt
import numpy as np
from number_encoder import *
import os


# # Ścieżka do pliku CSV
# file_path = "test_05_Mar_2025_1.csv"

def get_mes_number(file_path):
    if file_path[-6]!='_':
        return file_path[-6]+file_path[-5]
    else:
        return file_path[-5]

def funkcja(file_path):
    x = []
    y = []
    labels = []
    mes_number = get_mes_number(file_path)

    # Odczyt pliku CSV
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            row[1] = row[1][1:]
            pattern = row[0].strip()
            angles = row[1].strip().split()  # Usunięcie zbędnych spacji i podział na części
            power = row[2].strip()
            theta_i = angles[0].split('=')[-1]
            theta_d = angles[1].split('=')[-1]
            print([pattern, theta_i, theta_d, power])
            
            y.append(float(power))
            x.append(int(theta_d))
            labels.append(theta_i)



    # Tworzenie wykresu
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, color='b', label="θ_i")

    # Dodawanie etykiet do punktów
    for i, txt in enumerate(labels):
        plt.annotate(txt, (x[i], y[i]), textcoords="offset points", xytext=(5,5), ha='right')


    # Ustawienie skali na osi X co 5 jednostek
    x_min, x_max = min(x), max(x)
    plt.xticks(np.arange(x_min, x_max + 1, 5))
    # Opis osi
    plt.xlabel("θ_d")
    plt.ylabel("Power recieved")
    title = "Pattern for angles when antennas are in " + get_angles(n=mes_number)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt_name = title + '.png'
    plt.plot()
    plt.savefig(plt_name)
    print("saving figure as: " + plt_name)

for filename in os.listdir(os.getcwd()):
    if filename.endswith('.csv'):
        # Pełna ścieżka do pliku
        file_path = filename
        print("Reading file:: ", filename )
        funkcja(file_path)

