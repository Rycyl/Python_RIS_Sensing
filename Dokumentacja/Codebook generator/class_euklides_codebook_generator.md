## Euclidean Codebook Generator

### Cel
Plik służy do generowania i analizy codebooków metodą opartą o odległość Hamminga (Euklidesową). Umożliwia tworzenie nowych codebooków losowo lub jako podzbiór większego codebooka, zapisywania ich do `.pkl` oraz obliczanie metryk jakości.

### Najważniejsze elementy

#### Funkcje pomocnicze

##### `def pattern_hamming_distance()`
Liczy odległość Hamminga między dwoma wzorcami typu `BitArray`.

##### `def get_patterns_from_codebook()`
Zwraca listę wzorców `BitArray` z obiektu `Codebook`.

##### `def calculate_metric()`
Liczy metrykę wzorca względem pozostałych wzorców jako sumę kwadratów odległości Hamminga.

#### `class Euklides_codebook`
Klasa odpowiedzialna za generowanie codebooków metodą maksymalizacji odległości Hamminga między wzorcami.

##### `def generate_random_bitarray()`
Generuje losowy wzorzec bitowy o zadanej długości.

##### `def generate_codebook()`
Generuje nowy codebook od zera, losując wzorce i iteracyjnie poprawiając najsłabszy według metryki Hamminga.

##### `def generate_codebook_from_codebook()`
Generuje mniejszy codebook jako podzbiór większego codebooka, wybierając wzorce maksymalizujące odległości Hamminga.

#### Funkcje generowania codebooków

##### `def generate_euclidean_codebooks_of_size()`
Generuje lub wczytuje z pliku `.pkl` codebooki o podanych rozmiarach.

##### `def generate_euclidean_codebooks_of_size_from_codebook()`
Generuje lub wczytuje codebooki o podanych rozmiarach na podstawie większego codebooka.

##### `def load_euclidean_codebooks()`
Wczytuje zapisane codebooki `.pkl` na podstawie rozmiaru i numeru powtórzenia.

#### Funkcje metryk

##### `def calculate_metric_for_codebook()`
Liczy sumaryczną metrykę dla jednego codebooka.

##### `def calculate_metric_for_codebooks()`
Liczy metryki dla listy codebooków.

##### `def calculate_metric_for_codebooks_div_by_len()`
Liczy metrykę znormalizowaną przez `len(codebook) - 1`.

##### `def calculate_metric_for_codebooks_sqrt_div_by_len()`
Liczy `sqrt(M) / (len(codebook) - 1)`.

##### `def calculate_metric_for_codebooks_div_div()`
Liczy metrykę znormalizowaną przez liczbę par wzorców.

#### Funkcje analizy

##### `def analyze_codebooks_with_metrics()`
Wczytuje codebooki, liczy wybrane metryki i rysuje wykresy porównawcze.

### Kompletne przykładowe wywołanie

```python
from class_codebook import Codebook
from euklides_codebook import generate_euclidean_codebooks_of_size_from_codebook

# Wczytanie bazowego codebooka
base_codebook = Codebook(
    dumpfile="euclidean_codebooks/euklides_codebook_128_0.pkl"
)

# Rozmiary mniejszych codebooków do wygenerowania
sizes = [64, 32, 16, 8]

# Generowanie codebooków na podstawie większego codebooka
codebooks = generate_euclidean_codebooks_of_size_from_codebook(
    bigger_codebook=base_codebook,
    codebooks_sizes=sizes,
    n_repeats=1,
    i_bound=10000,
    k_bound=500000
)

# Dostęp do wygenerowanego codebooka
cb = codebooks[0]

print("Liczba wzorców:", len(cb.patterns))
print("Pierwszy wzorzec:", cb.patterns[0])
```

### Uwagi

- Metryka bazuje na sumie kwadratów odległości Hamminga między wzorcami.
- Większa wartość metryki oznacza większe zróżnicowanie wzorców w codebooku.
- generate_codebook() tworzy codebook od zera.
- generate_codebook_from_codebook() wybiera podzbiór z istniejącego większego codebooka.
- Wygenerowane codebooki są zapisywane jako pliki .pkl.
- Funkcje generujące najpierw próbują wczytać istniejący plik .pkl; jeśli się nie uda, generują nowy codebook.
- Domyślny folder zapisu to euclidean_codebooks.
- Wymagane zależności: numpy, bitstring.