## Optimization / Reference selection utils

### Cel
Plik zawiera funkcje pomocnicze do wyboru najlepszych/najgorszych wzorców, liczenia średnich mocy oraz filtrowania wyników optymalizacji dla obiektów `Results` / `Result`.

### Najważniejsze elementy

#### Funkcje konwersji i średnich

##### `def is_standard_pattern()`
Sprawdza, czy wynik jest zwykłym wzorcem codebooka (`idx < 100000`), ignorując wzorce referencyjne/min/max.

##### `def get_trace_for_position()`
Zwraca obcięty trace dla konkretnej pozycji pomiarowej `(Rx_Angle, c_value)`.

##### `def result_avg_for_position()`
Liczy średnią liniową trace’a dla jednego `Result` w wybranej pozycji RX.

##### `def result_avg_global()`
Liczy średnią liniową dla jednego `Result` po wszystkich jego trace’ach.

##### `def linear_avg_trace_for_position()`
Liczy średni trace oraz średnią skalarną dla listy wyników w wybranej pozycji RX.

##### `def codebook_linear_avg_for_position()`
Liczy jedną średnią moc dla całego codebooka w konkretnej pozycji RX.

#### Funkcje wyboru wyników

##### `def choose_codebook_result()`
Wybiera najlepszy (`max`) lub najgorszy (`min`) wzorzec z codebooka dla danej pozycji RX albo globalnie.

##### `def choose_ref_result_for_position()`
Wybiera najlepszy/najgorszy wynik referencyjny dla konkretnej pozycji RX.

##### `def select_ref_results()`
Wybiera wyniki referencyjne z `results.maxs` lub `results.mins` na podstawie listy ID.

##### `def get_ids_for_mode()`
Zwraca listę ID referencji dla trybu `max` albo `min`.

#### Funkcje obsługi wyników optymalizacji

##### `def parse_optimization_result_id()`
Parsuje ID wyniku optymalizacji i zwraca proces (`max`/`min`), numer nośnej `N` oraz iterację.

##### `def select_optimization_results()`
Filtruje wyniki optymalizacji z `results.maxs` lub `results.mins` według procesu, nośnej `N` i zakresu iteracji.

### Use example

```python
selected_result, avg = choose_codebook_result(
    cb_results=results,
    target_rx=30,
    target_c=1.5,
    mode="max",
    selection_scope="rx"
)
```