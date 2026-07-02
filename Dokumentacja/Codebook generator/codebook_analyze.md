## Codebook Analyze

### Cel
Plik zawiera funkcje do analizy wzorców RIS i codebooków, głównie pod kątem:
- odległości Hamminga między wzorcami,
- charakterystyk AF (`Array Factor`),
- redukcji codebooka na podstawie minimalnej odległości Hamminga,
- wizualizacji metryk i porównań codebooków.

### Najważniejsze elementy

#### Funkcje pomocnicze geometrii RIS

##### `def ris_x_distance()`
Oblicza pozycję elementu RIS w osi `X`.

##### `def ris_y_distance()`
Oblicza pozycję elementu RIS w osi `Y`.

##### `def sin()`, `def cos()`
Liczą sinus i cosinus dla kąta podanego w stopniach.

##### `def u()`, `def v()`
Liczą składowe kierunkowe używane przy wyznaczaniu `Array Factor`.

#### Funkcje analizy wzorców

##### `def hamming_distance()`
Liczy odległość Hamminga między dwoma wzorcami bitowymi.

##### `def AF_from_pattern()`
Wyznacza charakterystykę `Array Factor` dla podanego wzorca RIS i kąta nadajnika.

#### Funkcje wykresów AF

##### `def plot_AFs()`
Rysuje charakterystyki AF dla listy wzorców.

##### `def plot_codebooks_AFs()`
Rysuje charakterystyki AF dla wielu codebooków na jednym wykresie.

#### Funkcje redukcji codebooka

##### `def reduce_codebook_by_hamming()`
Tworzy kolejne podzbiory codebooka, ograniczając je minimalną odległością Hamminga między wzorcami.

##### `def plot_codebooks_reduce_by_hamming()`
Rysuje zależność liczby wzorców w codebooku od minimalnej odległości Hamminga.

#### Funkcje metryk

##### `def plot_codebooks_metrics()`
Rysuje porównanie metryk dla wielu codebooków w funkcji ich rozmiaru.

### Kompletne przykładowe wywołanie

```python
from class_codebook import Codebook
from codebook_analyze import (
    AF_from_pattern,
    plot_AFs,
    reduce_codebook_by_hamming,
    plot_codebooks_reduce_by_hamming
)

# Wczytanie codebooka
codebook = Codebook(
    dumpfile="codebook.pkl",
    filename="Codebook.csv"
)

# Pobranie pierwszego wzorca
pattern = codebook.patterns[0].pattern

# Obliczenie Array Factor dla wzorca
af = AF_from_pattern(
    pattern=pattern,
    theta_Tx=-49,
    phi_Tx=0,
    silent=False
)

# Wykres AF dla jednego wzorca
plot_AFs([af])

# Redukcja codebooka według odległości Hamminga
reduced_codebooks = reduce_codebook_by_hamming(codebook)

# Wykres liczby wzorców po redukcji
plot_codebooks_reduce_by_hamming([
    (reduced_codebooks, "Codebook reduced by Hamming")
])
```

### Uwagi

 - Funkcje operują głównie na obiektach Codebook oraz wzorcach typu BitArray.
 - AF_from_pattern() zakłada siatkę RIS 16 x 16, czyli 256 elementów.
 - Charakterystyka AF liczona jest dla kątów od -90° do 89°.
 - reduce_codebook_by_hamming() zwraca listę list wzorców, a nie obiekty Codebook.
 - Odległość Hamminga jest dzielona przez 16 w funkcji redukcji, więc próg distance_lim odnosi się do przeskalowanej wartości.
 - W kodzie używane są funkcje sin i cos zdefiniowane lokalnie, które przyjmują kąty w stopniach.
 - Funkcja AF_from_pattern() wykorzystuje stałą częstotliwość 5.53 GHz.