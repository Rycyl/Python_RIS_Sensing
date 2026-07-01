## Selected patterns max finder

### Cel
Plik służy do wczytania zapisanych wcześniej wybranych wzorców (`Selected`) z pliku `.pkl` oraz uruchomienia dla każdego z nich metody wyszukiwania maksimum.

### Najważniejsze elementy

#### Skrypt główny

##### `selected = Selected()`
Tworzy obiekt klasy `Selected`.

##### `selected.load_from_file()`
Wczytuje dane wybranych wzorców z pliku pickle.

##### `k.find_max()`
Dla każdego obiektu z listy `selected.selected` uruchamia metodę wyszukującą maksimum.

### Użycie

```python
dumpfile = "wybrane_paterny_pk_metod.pkl"

selected = Selected()
selected.load_from_file(dumpfile=dumpfile)

for k in selected.selected:
    k.find_max()
```

### Uwagi

- Plik działa jako prosty skrypt uruchomieniowy.
- Wymaga istniejącego pliku wybrane_paterny_pk_metod.pkl.
- Korzysta z klasy Selected z modułu class_select.
- Importy class_codebook, class_measures_result i numpy nie są bezpośrednio używane w pokazanym kodzie.