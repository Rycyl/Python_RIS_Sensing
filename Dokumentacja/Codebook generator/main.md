# THIS WAS MAIN A LONG TIME AGO

### Cel
Plik służy do generowania binarnych wzorców RIS, liczenia charakterystyk `Array Factor` oraz tworzenia dużych codebooków na podstawie kątów padania, odbicia i przesunięcia fazowego `φ_s`.

### Najważniejsze elementy

#### Funkcje geometrii i fazy

##### `def ris_x_distance()`
Oblicza pozycję elementu RIS w osi `X`.

##### `def ris_y_distance()`
Oblicza pozycję elementu RIS w osi `Y`.

##### `def Phi_i_mn()`
Liczy fazę fali padającej na element RIS.

##### `def Phi_d_mn()`
Liczy fazę fali odbitej / kierunkowej dla elementu RIS.

##### `def Phi_mn()`
Liczy idealne przesunięcie fazowe dla elementu RIS.

##### `def Phi_mn_quant()`
Kwantyzuje fazę do skończonej liczby wartości, domyślnie do postaci binarnej.

#### Funkcje Array Factor

##### `def AF_single()`
Liczy wkład pojedynczego elementu RIS do charakterystyki AF dla idealnej fazy.

##### `def AF_single_q()`
Liczy wkład pojedynczego elementu RIS do charakterystyki AF dla fazy skwantowanej.

##### `def AF()`
Liczy charakterystykę `Array Factor` dla całej macierzy RIS dla zadanego kąta TX i RX.

#### Funkcje generowania wzorców

##### `def pattern_generate()`
Generuje binarne wzorce RIS dla zakresu kątów `θ_i`, `θ_d` oraz przesunięcia fazowego `phase_shift`.

##### `def codebook_generate()`
Generuje codebook na podstawie wielu wartości `θ_d` oraz `φ_s`, zapisuje go do CSV i tworzy wersję zgodną z klasą `Codebook`.

##### `def pat_print()`
Wypisuje wzorzec RIS w czytelnej postaci `16 x 16`.

#### Funkcje wykresów

##### `def plot_no_unique_patterns()`
Rysuje liczbę unikalnych wzorców w zależności od kroku danego parametru.

##### `def plot_pattern_occurence()`
Pokazuje, dla jakich wartości `φ_s` i RX występują konkretne wzorce z codebooka.

### Kompletne przykładowe wywołanie

```python
from pattern_generator import codebook_generate, AF
import matplotlib.pyplot as plt
import numpy as np

# Generowanie codebooka dla:
# - TX ustawionego na -48 stopni,
# - RX od 0 do 89 stopni,
# - kroku RX = 1 stopień,
# - kroku przesunięcia fazowego phi_s = 10 stopni.
pattern_count = codebook_generate(
    θ_i_start=-48,
    θ_i_step=-100,
    θ_i_treshold=-90,
    θ_d_start=0,
    θ_d_treshold=90,
    theta_d_step=1,
    phase_shift_step=10,
    stack_repeats=True
)

print("Liczba unikalnych wzorców:", pattern_count)

# Obliczenie charakterystyki AF dla idealnego i binarnego wzorca
af_linear = AF(
    θi=-8,
    θd=40,
    quant=False
)

af_binary = AF(
    θi=-8,
    θd=40,
    quant=True
)

# Wykres porównania
x = range(-90, 90)

plt.figure(figsize=(10, 6))
plt.plot(x, af_linear, linestyle="--", label="Linear")
plt.plot(x, af_binary, label="Binary")
plt.legend()
plt.xticks(np.arange(-90, 91, 10))
plt.yticks(np.arange(-10, 50, 5))
plt.xlim(-90, 90)
plt.ylim(-10, 25)
plt.xlabel("Rx location [°]")
plt.ylabel("AF [dB]")
plt.grid()
plt.show()
```

### Uwagi

- Plik zakłada macierz RIS 16 x 16, czyli 256 elementów.
- Stałe globalne opisują częstotliwość 5.53 GHz, długość fali i rozmiary elementów RIS.
- pattern_generate() w aktualnej wersji przyspiesza obliczenia przez użycie tylko jednego wiersza RIS (y_n -= 100).
- codebook_generate() najpierw próbuje wczytać istniejący codebook, a jeśli się nie uda, generuje nowy.
- Wygenerowane codebooki są zapisywane w folderze codebooks.
- Po wygenerowaniu CSV wywoływana jest funkcja codebook_eval() z modułu eval.
- Wzorce są zapisywane jako BitArray, a następnie powielane 16 razy, żeby uzyskać wzorzec długości 256.
- Funkcja plot_pattern_occurence() służy do sprawdzania, które wzorce odpowiadają konkretnym kombinacjom TX, RX i φ_s.
