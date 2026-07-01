## Codebook

### Cel
Plik służy do wczytywania i przechowywania **codebooka** — listy wzorców bitowych powiązanych z kątami.

### Najważniejsze elementy

#### `class Pattern`
Reprezentuje pojedynczy wzorzec z codebooka.

##### `def __init__()`
Tworzy wzorzec na podstawie:
- `idx` — indeks wzorca,
- `pattern` — wzorzec zapisany w formacie hex,
- `angles` — lista kątów powiązanych ze wzorcem.

##### `def __repr__()`
Zwraca tekstową reprezentację obiektu `Pattern`.

#### `class Codebook`
Przechowuje listę obiektów `Pattern` w polu `patterns` oraz obsługuje ładowanie i zapis codebooka.

##### `def __init__()`
Tworzy obiekt `Codebook` i opcjonalnie automatycznie ładuje dane.

##### `def add_pattern()`
Dodaje obiekt `Pattern` do listy `patterns`.

##### `def load_codebook()`
Ładuje dane z pliku `.pkl`, a jeśli się nie uda, próbuje wczytać je z pliku `.csv`.

##### `def load_csv_codebook()`
Wczytuje wzorce z pliku CSV i tworzy na ich podstawie obiekty `Pattern`.

##### `def load_pkl_codebook()`
Wczytuje zapisany wcześniej obiekt `Codebook` z pliku pickle.

##### `def dump_class_to_file()`
Zapisuje obiekt `Codebook` do pliku `.pkl`.

### Użycie
```python
codebook = Codebook(dumpfile="codebook.pkl", filename="Codebook.csv", load = True)
print(len(codebook.patterns))
```