## CSV merge utils

### Cel
Plik służy do scalania wielu plików CSV z wynikami pomiarów oraz modyfikowania wartości identyfikatora `N` (id patternów) w pierwszej kolumnie.

### Najważniejsze elementy

#### Funkcje scalania plików

##### `def merge_specific_files_builtin()`
Scala konkretną listę plików CSV do jednego pliku wynikowego.  
Nagłówek jest kopiowany tylko z pierwszego pliku.

##### `def merge_csv_builtin()`
Wyszukuje pliki CSV po prefiksie nazwy i scala je do jednego pliku.

#### Funkcje modyfikacji danych

##### `def increment_n_in_files()`
Modyfikuje pierwszą kolumnę `N` (id patternu) w plikach CSV pasujących do podanego prefiksu.

Może działać w dwóch trybach:
- dodaje stałą wartość do istniejącego `N`,
- nadaje nowe kolejne wartości `N` od `add_value`.

### Użycie

Scalenie plików po prefiksie:

```python
merge_csv_builtin(
    file_prefix="results_prefix",
    output_filename="output_merged_filename.csv"
)
```