## Results for Codebook

### Cel
Plik służy do wybierania podzbioru wyników (`Results`) odpowiadających konkretnemu codebookowi albo podanej liście identyfikatorów.

### Najważniejsze elementy

#### Funkcje wyboru wyników

##### `def select_results_for_codebook()`
Tworzy nowy obiekt `Results`, zawierający tylko te wyniki, których wzorce bitowe występują w podanym `Codebook`.

##### `def select_results_for_ids()`
Tworzy nowy obiekt `Results`, zawierający tylko wyniki o identyfikatorach z podanej listy.

### Użycie

Wybór wyników dla codebooka:

```python
selected_results = select_results_for_codebook(
    results=Results(),
    codebook=Codebook()
)
```