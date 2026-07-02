## Codebook

### Cel
Plik służy do wczytywania, przechowywania oraz zapisywania **codebooków** zawierających wzorce bitowe i przypisane do nich kąty. Obsługuje formaty `.pkl` oraz `.csv`.

### Najważniejsze elementy

#### `def dump_all_codebooks_to_csv()`
Konwertuje wszystkie codebooki zapisane jako `.pkl` w podanym folderze do plików `.csv`.

#### `class Pattern`
Reprezentuje pojedynczy wzorzec codebooka.

##### `def __init__()`
Tworzy wzorzec na podstawie:
- `idx` — indeksu wzorca,
- `pattern` — wzorca zapisanego w formacie hex,
- `angles` — listy kątów przypisanych do wzorca.

##### `def __str__()`
Zwraca wzorzec jako string hex.

#### `class Codebook`
Przechowuje listę obiektów `Pattern` w polu `patterns`.

##### `def add_pattern()`
Dodaje obiekt `Pattern` do listy `patterns`.

##### `def load_codebook()`
Ładuje codebook z pliku `.pkl`, a jeśli się nie uda, z pliku `.csv`.

##### `def dump_class_to_file()`
Zapisuje obiekt `Codebook` do pliku `.pkl`.

##### `def dump_class_to_csv()`
Zapisuje zawartość `Codebook` do pliku `.csv`.

### Kompletne przykładowe wywołanie

```python
from class_codebook import Codebook, dump_all_codebooks_to_csv

# Wczytanie codebooka.
# Najpierw próbuje odczytać plik .pkl.
# Jeśli się nie uda, ładuje dane z CSV i zapisuje je do .pkl.
codebook = Codebook(
    dumpfile="codebook.pkl",
    filename="Codebook.csv",
    do_load=True
)

# Liczba wzorców w codebooku
print("Liczba wzorców:", len(codebook.patterns))

# Dostęp do pierwszego wzorca
pattern = codebook.patterns[0]

print("Indeks wzorca:", pattern.idx)
print("Wzorzec hex:", pattern.pattern.hex)
print("Kąty:", pattern.angles)

# Zapis codebooka do pliku pickle
codebook.dump_class_to_file("codebook.pkl")

# Zapis codebooka do CSV
codebook.dump_class_to_csv("Codebook_export.csv")

# Konwersja wszystkich plików .pkl z folderu na CSV
dump_all_codebooks_to_csv(folder_path="euclidean_codebooks")
```