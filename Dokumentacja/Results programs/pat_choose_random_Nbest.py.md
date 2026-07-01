## Random Pattern Selection Test

### Cel
Plik służy do testowego wyboru losowego zestawu wzorców z wcześniej zapisanych wyników `Selected` oraz porównania ich jakości z maksimum uzyskanym z pełnych pomiarów.

### Najważniejsze elementy

#### Funkcje metryczne

##### `def przeplywnosc()`
Liczy uproszczoną przepływność na podstawie mocy odebranej i poziomu szumu.

##### `def metric()`
Liczy średnią metrykę jakości dla wybranego zestawu wzorców, biorąc maksimum mocy w każdej pozycji.

#### Skrypt główny

##### `selected.load_from_file()`
Wczytuje zapisane wcześniej wybrane wzorce z pliku `.pkl`.

##### `merge`
Tablica zawierająca wartości `maxs` dla wszystkich obiektów z `selected.selected`.

##### Losowy wybór wzorców
Losuje `N` wzorców z tablicy `merge`, liczy ich metrykę i zapamiętuje najlepszy wynik.

##### Porównanie z pełnymi wynikami
Wczytuje `Results`, wyznacza maksymalne moce z pełnych pomiarów i porównuje je z losowo wybranym zestawem.

##### Wykres
Rysuje porównanie:
- maksimum z `Selected`,
- maksimum z pełnych pomiarów,
- najlepszego losowego wyboru.

### Użycie

```python
N = 4
ITERATIONS = 1000

best = -np.inf
best_sel = None
best_pos = None

for i in range(ITERATIONS):
    positions = random.sample(range(len(merge)), N)
    selections = merge[positions]

    score = metric(selections)

    if score > best:
        best = score
        best_sel = selections
        best_pos = positions

print("Najlepsza metryka:", best)
print("Indeksy wybranych wzorców:", best_pos)
print("Wybrane wzorce:", best_sel)
print("Najlepsze moce:", np.max(best_sel, axis=0))
```
### Uwagi

- Skrypt działa eksperymentalnie i uruchamia się bez funkcji main.
- Parametry N i ITERATIONS sterują liczbą wybieranych wzorców oraz liczbą prób losowania.
- Wymaga pliku wybrane_paterny_pk_metod_v2.pkl.
- Korzysta z klas Selected oraz Results.
- Wymagane zależności: numpy, matplotlib.
