import csv
import matplotlib.pyplot as plt

# Wczytanie danych z pliku CSV
file_path = "12_03_24_reflection.csv"  # Zastąp nazwa_pliku.csv właściwą ścieżką do pliku

class baza: #klasa przechowuje poukładane pomiary wg patternów na RIS
      def __init__(self, pattern,fq,lvl):
        self.pattern = pattern
        self.measures = [[fq],[lvl]]
        
      def add_measure(self,fq,lvl):
            self.measures[0].append(fq)
            self.measures[1].append(lvl)

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
            if row[0] == i.pattern:
                i.add_measure(float(row[1]), float(row[2]))  # Konwertowanie na float
                found = True
                break
        if not found:
            x = baza(row[0], float(row[1]), float(row[2]))
            data.append(x)

#print(data)
# Wykres
plt.figure()

for item in data:
    plt.plot(item.measures[0], item.measures[1], label=item.pattern)

#plt.plot(data[1].measures[0], data[1].measures[1], label=data[1].pattern)

plt.xlabel('Częstotliwość [GHz]')
plt.ylabel('Poziom mocy [dBm]')
#plt.legend()  # Tutaj legend() zostanie automatycznie dodane na podstawie etykiet przekazanych do plt.plot
plt.grid()
plt.show()