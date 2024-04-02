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
filename = sys.argv[2]
fi=copy.deepcopy(filename)
# Wczytanie danych z pliku CSV
data_folder = os.path.join("..","wyniki",folder)
file_path = os.path.join(data_folder, filename)
dest_folder = os.path.join(data_folder, "wykresy")
#print(dest_folder)
try:
    os.mkdir(dest_folder)
except:
    print()

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
    csv_reader = csv.reader(file, delimiter=',')
    
    next(csv_reader)  # Pominięcie nagłówka, jeśli istnieje
    for row in csv_reader:
        #print(row)
        #print("ROW", row[0])
        #print(len(row))
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
fig, axs = plt.subplots(nrows=2, ncols=2, layout='constrained', figsize=(20,16))
axs = axs.flatten()
for i in range(4):  # Loop through each subplot
    for item in data[i*4:i*4+int((len(data))/4)]:  # Plot data for each subplot
        axs[i].plot(item.measures[0], item.measures[1], label=item.pattern)
        axs[i].set_xlabel('Częstotliwość [Hz]')
        axs[i].set_ylabel('Poziom mocy [dBm]')
        axs[i].set_title(fi)
        axs[i].set_ylim(-65, -30)
        axs[i].legend()
# Tworzenie nazwy pliku
plt.title(filename)
file_name = os.path.join(dest_folder, filename + "_wykres.png")
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
plt.subplots_adjust(top=0.95)
plt.title(filename)
file_name = os.path.join(dest_folder, filename + "mean_pow.png")
plt.savefig(file_name)
plt.close()
    
    
#min/max plot points
x = data[0].measures[0]
max_handle = data[0].measures[1]
min_handle = copy.deepcopy(max_handle)
mean_handle = copy.deepcopy(max_handle)
fig, ax = plt.subplots(figsize=(15, 12))
#print(max_handle, id(max_handle))
#print(min_handle, id(min_handle))
for i in data[1:]:
    for j in range(0,(len(i.measures[1]))):
        mean_handle[j]+=i.measures[1][j]
        if(max_handle[j]<i.measures[1][j]):
            max_handle[j]=i.measures[1][j]
            
        if(min_handle[j]>i.measures[1][j]):
            min_handle[j]=i.measures[1][j]
            
for i in range(len(mean_handle)):
    mean_handle[i] = mean_handle[i]/len(data)
#print(max_handle)
#print(min_handle)
ax.plot(x, max_handle, label="maksima znalezione")
ax.plot(x, min_handle, label="minima znalezione")
ax.plot(x, mean_handle, label="średni wynik pomiarów")
ax.set_xlabel('Częstotliwość [Hz]')
ax.set_ylabel('Poziom mocy [dBm]') 
ax.grid()
plt.title(filename)
fig.legend()
file_name = os.path.join(dest_folder, filename + "_min_max.png")
plt.savefig(file_name)
plt.close()