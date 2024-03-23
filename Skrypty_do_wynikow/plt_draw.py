import csv
import matplotlib.pyplot as plt
import os
import os.path
import sys

#name_of_script = sys.argv[0]
folder = sys.argv[1]
file = sys.argv[2]
# Wczytanie danych z pliku CSV
data_folder = os.path.join("..","wyniki",folder)
file_path = os.path.join(data_folder, file)


class baza: #klasa przechowuje poukładane pomiary wg patternów na RIS
        def __init__(self, pattern,fq,lvl):
            self.pattern = pattern
            print("Added measurements of:: ", self.pattern)
            self.measures = [[fq],[lvl]]
            self.mean_pow = 0
        
        def add_measure(self,fq,lvl):
            self.measures[0].append(fq)
            self.measures[1].append(lvl)
       
        def mean_power(self):
            sum = 0
            n = 0
            for i in self.measures:
                sum += i[1]
                n+=1
            self.mean_pow = sum/n
            return

data = []

with open(file_path, 'r') as file:
    csv_reader = csv.reader(file, delimiter=';')
    next(csv_reader)  # Pominięcie nagłówka, jeśli istnieje
    for row in csv_reader:
        #print("ROW", row[0])
        if len(row) < 3: #jezeli wiersz jest za krotki pomin
            continue
        found = False
        for i in data:
            if (row[0] == i.pattern) :
                i.add_measure(float(row[1]), float(row[2]))  # Konwertowanie na float + wpisanie do obiektu wynikow
                found = True
                break
        if not found:
            x = baza(row[0], float(row[1]), float(row[2]))
            data.append(x)

for i in data:
    i.mean_power()

#print(data)
# Wykres
for i in range(5):
    fig, ax = plt.subplots(figsize=(8, 6))

    for item in data[i*5:i*5+5]:
        ax.plot(item.measures[0], item.measures[1], label=item.pattern)
    ax.set_xlabel('Częstotliwość')
    ax.set_ylabel('Poziom mocy (dBm)')
    ax.grid()
    fig.legend()
    # Tworzenie nazwy pliku
    file_name = os.path.splitext(file_path)[0] + "_wykres" + str(i+1) + ".png"
    plt.savefig(file_name)
    plt.close()