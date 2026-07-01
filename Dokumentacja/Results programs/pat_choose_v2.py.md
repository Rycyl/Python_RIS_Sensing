## Selected Max Plot

### Cel
Plik wczytuje zapisane wcześniej obiekty `Selected`, pobiera z nich maksymalne moce (`maxs`), wyznacza najlepszą wartość dla każdej pozycji RX i rysuje wykres tych wartości względem kąta odbiornika.

### Najważniejsze elementy

#### Skrypt główny

##### `selected = Selected()`
Tworzy obiekt klasy `Selected`, który przechowuje listę wybranych konfiguracji / wzorców.

##### `selected.load_from_file()`
Wczytuje zapisany obiekt `Selected` z pliku `.pkl`.

##### `merge`
Lista wartości `maxs` pobranych z każdego elementu `selected.selected`.

```python
merge = []
for s in selected.selected:
    merge.append(s.maxs)
```
##### `max_values`
Najlepsze wartości mocy dla każdej pozycji RX spośród wszystkich elementów merge.
``` python
max_values = np.max(merge, axis=0)
```
##### 'max_indices'
Indeksy elementów z selected.selected, które dały maksimum dla danej pozycji RX.

```python
max_indices = np.argmax(merge, axis=0)Show more lines
```

##### 'best_selects'
Lista obiektów Select, które osiągnęły maksimum dla kolejnych pozycji RX.

```python
best_selects = [selected.selected[i] for i in max_indices]Show more lines
```

#### Kompletne przykładowe wywołanie

```python
from class_select import Selected
from class_measures_result import Results

import numpy as np
import matplotlib.pyplot as plt

dumpfile = "wybrane_paterny_pk_metod_v2.pkl"

# Wczytanie wybranych wzorców
selected = Selected()
selected.load_from_file(dumpfile=dumpfile)

# Zebranie maksymalnych mocy z każdego obiektu Select
merge = []

for s in selected.selected:
    merge.append(s.maxs)

merge = np.array(merge)

# Najlepsza moc dla każdej pozycji RX
max_values = np.max(merge, axis=0)

# Indeks obiektu Select, który dał maksimum dla każdej pozycji RX
max_indices = np.argmax(merge, axis=0)

# Oryginalne obiekty Select dające maksimum
best_selects = [selected.selected[i] for i in max_indices]

print("Najlepsze wartości mocy:")
print(max_values)

print("Indeksy najlepszych obiektów Select:")
print(max_indices)

print("Najlepszy obiekt dla pierwszej pozycji RX:")
print(best_selects[0])

# Wczytanie wyników, żeby pobrać kąty RX do osi X
results = Results()
x_axis = results.results[0].Rx_Angle

# Wykres
plt.figure(figsize=(10, 8))
plt.plot(
    x_axis,
    max_values,
    markersize=18,
    label="max in selected",
    color="blue",
    marker="X"
)

plt.xlabel("Kąt położenia odbiornika [stopnie]", fontsize=20)
plt.ylabel("Wartości mocy odebranej [dBm]", fontsize=20)
plt.grid()
plt.legend(fontsize=20, loc="upper right")
plt.show()
```

#### Jak dostać najlepszy obiekt dla konkretnej pozycji RX
```python 
rx_idx = 0

best_idx = max_indices[rx_idx]
best_select = selected.selected[best_idx]
best_power = max_values[rx_idx]

print(best_idx)
print(best_select)
print(best_power)
```

### Uwagi

- merge[i] odpowiada wartościom selected.selected[i].maxs.
- max_values[j] mówi, jaka była najlepsza moc dla pozycji RX o indeksie j.
- max_indices[j] mówi, który obiekt Select dał tę najlepszą moc.
- best_selects[j] zawiera oryginalny obiekt Select najlepszy dla pozycji RX j.
- Plik wymaga istniejącego dumpa: wybrane_paterny_pk_metod_v2.pkl.
- Do osi X wykorzystywane są kąty Rx_Angle z obiektu Results.
- Zakomentowany fragment kodu służy do ponownego wygenerowania danych Selected z Codebook i Results.
- Wymagane zależności: numpy, matplotlib.

