import csv
import matplotlib.pyplot as plt
import os
# Wczytanie danych z pliku CSV
file_path = "12_03_24_reflection.csv"  # Zastąp nazwa_pliku.csv właściwą ścieżką do pliku

def check_pattern(pattern):
    if pattern == "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000000000000000000000000000":
        return "Góra włączona, dół wyłączony"
    elif pattern == "0x00000000000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF":
        return "Góra wyłączona, dół włączony"
    elif pattern == "0xFF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00":
        return "Lewa włączona, prawa wyłączona"
    elif pattern == "0x00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF":
        return "Prawa włączona, lewa wyłączona"
    elif pattern == "0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA":
        return "Pasy wertykalne (1 0 1 0)"
    elif pattern == "0x5555555555555555555555555555555555555555555555555555555555555555":
        return "Pasy wertykalne (0 1 0 1)"
    elif pattern == "0xFFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000":
        return "Pasy horyzontalne (on - off)"
    elif pattern == "0x0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF0000FFFF":
        return "Pasy horyzontalne (off - on)"
    elif pattern == "0xAAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555":
        return "Szachownica (1 0 1 0 / 0 1 0 1)"
    elif pattern == "0x5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA":
        return "Szachownica (0 1 0 1 / 1 0 1 0)"
    elif pattern == "0xF0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0":
        return "Pasy wertykalne (1 1 1 1 - 0 0 0 0)"
    elif pattern == "0x0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F":
        return "Pasy wertykalne (0 0 0 0 - 1 1 1 1)"
    elif pattern == "0xFFFFFFFFFFFFFFFF0000000000000000FFFFFFFFFFFFFFFF0000000000000000":
        return "Pasy horyzontalne (grube start on)"
    elif pattern == "0x0000000000000000FFFFFFFFFFFFFFFF0000000000000000FFFFFFFFFFFFFFFF":
        return "Pasy horyzontalne (grube start off)"
    elif pattern == "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF":
        return "Wszystkie aktywne"
    elif pattern == "0xF0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0":
        return "F0F0"
    elif pattern == "0x0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F":
        return "0F0F"
    elif pattern == "0x0000000000000000000000000000000000000000000000000000000000000000":
        return "Wyłączony"       
    elif pattern == "0x8000000000000000000000000000000000000000000000000000000000000000":
        return "włączony pierwszy element"        
    elif pattern == "0x0000000000000000000000000000000000000000000000000000000000000001":
        return "Włącznony ostatni element"   
    elif pattern == "0XCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC":
        return "CCCC"
    elif pattern == "0XAAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555AAAA5555":
        return "AAAA5555..."
    elif pattern == "0XFFFFFFFF00000000FFFFFFFF00000000FFFFFFFF00000000FFFFFFFF00000000":
        return "FFFFFFFF00000000"
    elif pattern == "0x3A7B2F4C6E8D1F0A2C4E6B8D1F2A3B5C7E9F0A2B4C6E8F1A3B5C7E9F0A2B4C6D":
        return "random 1"
    elif pattern == "0x9F8D6B5A3C2E1D0F9B7A5C3E1D0F9B7A5C3E1D0F9B7A5C3E1D0F9B7A5C3E1D0F":
        return "random 2"
    elif pattern == "0xD3E7F0A2B4C6E8D1F2A3B5C7E9F0A2B4C6E8D1F2A3B5C7E9F0A2B4C6E8D1F28C":
        return "random 3"
    elif pattern == "0x5A3C2E1D0F9B7A5C3E1D0F9B7A5C3E1D0F9B7A5C3E1D0F9B7A5C3E1D0F9B7AB3":
        return "random 4"
    elif pattern == "0XCCCCCCCC33333333CCCCCCCC33333333CCCCCCCC33333333CCCCCCCC33333333":
        return "CCCCCCCC33333333"
    elif pattern == "0X00007FFE40025FFA500A57EA542A55AA55AA542A57EA500A5FFA40027FFE0000":
        return "random 6"
    elif pattern == "0X000000003FFC3FFC300C300C33CC33CC33CC33CC300C300C3FFC3FFC00000000":
        return "random 5"
        
    else:
        return pattern

class baza: #klasa przechowuje poukładane pomiary wg patternów na RIS
        def __init__(self, pattern,fq,lvl):
            self.pattern = check_pattern(pattern)
            print(self.pattern)
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
        #print(row)
        if len(row) < 3:
        # Ten wiersz nie zawiera wystarczającej liczby kolumn
        # Możesz zdecydować, jak obsłużyć ten przypadek, np. pominąć wiersz lub podjąć inne działania
            continue
        found = False
        for i in data:
            if check_pattern(row[0]) == i.pattern:
                i.add_measure(float(row[1]), float(row[2]))  # Konwertowanie na float
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
    handles, labels = [], []
    for item in data[i*5:i*5+5]:
        ax.plot(item.measures[0], item.measures[1])
        handles.append(ax.plot([], [], label=item.pattern)[0])
        labels.append(item.pattern)
        

    ax.set_xlabel('Częstotliwość')
    ax.set_ylabel('Poziom mocy (dBm)')
    ax.grid()
    fig.legend(handles, labels, loc='upper right')
    # Tworzenie legendy
    #handles, labels = [], []
    #for item in data[i*5:i*5+5]:
    #    handles.append(ax.plot([], [], label=item.pattern)[0])
    #    labels.append(item.pattern)

    #fig.legend(handles, labels, loc='upper right')
    
    # Tworzenie nazwy pliku
    file_name = os.path.splitext(file_path)[0] + "_wykres" + str(i+1) + ".png"
    plt.savefig(file_name)
    plt.close()