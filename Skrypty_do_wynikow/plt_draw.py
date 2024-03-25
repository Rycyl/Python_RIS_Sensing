import csv
import matplotlib.pyplot as plt
import os
import os.path
import sys
import numpy as np
import copy
if len(sys.argv)<3:
    print("podaj argumenty: plt_draw.py [folder name] [file name]")
    input("Press enter to exit...")
    exit()
#name_of_script = sys.argv[0]
folder = sys.argv[1]
file = sys.argv[2]
# Wczytanie danych z pliku CSV
data_folder = os.path.join("..","wyniki",folder)
file_path = os.path.join(data_folder, file)


class baza: #klasa przechowuje poukładane pomiary wg patternów na RIS
        def __init__(self, pattern,fq,lvl):
            self.pattern = pattern
            #print("Added measurements of:: ", self.pattern)
            self.measures = [[fq],[lvl]]
            self.mean_pow = 0
        
        def add_measure(self,fq,lvl):
            self.measures[0].append(fq)
            self.measures[1].append(lvl)
       
        def mean_power(self):
            sum = 0
            n = 0
            #print(self.measures)
            for i in self.measures[1]:
                #print("i::",i)
                sum += i
                n+=1
            self.mean_pow = sum/n
            return

data = []
mes_max=-100.0
mes_min=0
with open(file_path, 'r') as file:
    csv_reader = csv.reader(file, delimiter=';')
    
    next(csv_reader)  # Pominięcie nagłówka, jeśli istnieje
    for row in csv_reader:
        #print(row)
        #print("ROW", row[0])
        if len(row) < 3: #jezeli wiersz jest za krotki pomin
            continue
        found = False
        for i in data:
            if float(row[2])>mes_max:
                mes_max=float(row[2])
            if float(row[2])<mes_min:
                mes_min=float(row[2])
            if (row[0] == i.pattern) :
                i.add_measure(float(row[1]), float(row[2]))  # Konwertowanie na float + wpisanie do obiektu wynikow
                found = True
                break
        if not found:
            data.append(baza(row[0], float(row[1]), float(row[2])))

for i in data:
    i.mean_power()



# Wykresy normalne
for i in range(5):
    fig, ax = plt.subplots(figsize=(15, 12))

    for item in data[i*5:i*5+5]:
        ax.plot(item.measures[0], item.measures[1], label=item.pattern)
    ax.set_xlabel('Częstotliwość [Hz]')
    ax.set_ylabel('Poziom mocy [dBm]')
    ax.grid()
    ax.set_ylim(-65, -30)
    fig.legend()
    # Tworzenie nazwy pliku
    file_name = os.path.splitext(file_path)[0] + "_wykres" + str(i+1) + ".png"
    plt.savefig(file_name)
    plt.close()

##poziomy średnie
fig, ax = plt.subplots(figsize=(15, 12))
y=[[],[]]
for item in data:
    y[0].append(item.mean_pow)
    #print(item.mean_pow)
    y[1].append(item.pattern)
y_pos = np.arange(len(y[1]))
min=min(y[0])
max=max(y[0])
ax.barh(y_pos, y[0], align='center')
ax.set_xlabel('Średni poziom mocy [dBm]')
ax.set_yticks(y_pos, labels=y[1])
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlim(min-1, max + 5)
plt.tight_layout()
file_name = os.path.splitext(file_path)[0] + "_mean_pow" + ".png"
plt.savefig(file_name)
plt.close()
    
    
#min/max plot points
x = data[0].measures[0]
max_handle = data[0].measures[1]
min_handle = copy.deepcopy(max_handle)
fig, ax = plt.subplots(figsize=(15, 12))
#print(max_handle, id(max_handle))
#print(min_handle, id(min_handle))
for i in data[1:]:
    for j in range(0,(len(i.measures[1]))):
    
        if(max_handle[j]<i.measures[1][j]):
            max_handle[j]=i.measures[1][j]
            
        if(min_handle[j]>i.measures[1][j]):
            min_handle[j]=i.measures[1][j]
            
#print(max_handle)
#print(min_handle)
ax.plot(x, max_handle, label="maksima znalezione")
ax.plot(x, min_handle, label="minima znalezione")
ax.set_xlabel('Częstotliwość [Hz]')
ax.set_ylabel('Poziom mocy [dBm]') 
ax.grid()
fig.legend()
file_name = os.path.splitext(file_path)[0] + "_min_max" + ".png"
plt.savefig(file_name)
plt.close()