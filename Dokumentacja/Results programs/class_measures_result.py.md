## Results / Trace

### Cel
Plik służy do wczytywania, przechowywania i analizy wyników pomiarów sygnału: mocy, kątów TX/RX oraz trace’ów. Obsługuje dane z plików `.pkl` i `.csv`.

### Najważniejsze elementy
- `def dbm_to_mw()` — konwersja mocy z dBm na mW.
- `def mw_to_dbm()` — konwersja mocy z mW na dBm.
- `def linear_mean()` — średnia liniowa wartości zapisanych w dBm.

#### `class Trace`
Przechowuje pojedynczy trace pomiarowy jako tablicę `numpy`.

##### `def get_truncaded_trace()`
Zwraca obcięty trace bez skrajnych nośnych (szum) oraz bez środkowych nośnych.

##### `def get_carriers_by_idx()`
Zwraca wybrane nośne z get_truncaded_trace() na podstawie listy indeksów.

##### `def get_mean()`
Zwraca średnią wartość trace’a.

##### `def get_max()`
Zwraca maksymalną wartość trace’a.

##### `def get_min()`
Zwraca minimalną wartość trace’a.

##### `def get_mean_by_idx()`
Zwraca średnią z wybranych nośnych wskazanych indeksami.

#### `class Result`
Reprezentuje wyniki pomiarów dla jednego wzorca: moce, kąty TX/RX, parametry pozycji oraz trace’y.

##### `def add_measure()`
Dodaje pojedynczy pomiar do obiektu `Result`.

##### `def get_rx_pos_in_xy()`
Wylicza pozycję RX w układzie XY na podstawie kąta RX i wartości `c`.

##### `def get_truncaded_traces()`
Zwraca obcięte trace’y zapisane w obiekcie.

#### `class Results`
Kontener na wiele obiektów `Result`. Odpowiada za ładowanie, zapis, sortowanie i analizę wyników.

##### `def load_results()`
Ładuje wyniki z pliku `.pkl`, a w razie błędu umożliwia wczytanie danych z `.csv`.

##### `def load_csv_results()`
Wczytuje wyniki z plików CSV pasujących do podanego prefiksu.

##### `def load_picle_results()`
Wczytuje wcześniej zapisane wyniki z pliku pickle.

##### `def dump_class_to_file()`
Zapisuje obiekt `Results` do pliku `.pkl`.

##### `def add_result()`
Dodaje obiekt `Result` do listy wyników.

##### `def sort_by_RX()`
Sortuje dane pomiarowe według wartości `c_values`.

##### `def get_traces_by_rx()`
Grupuje trace’y według pary `(Rx_Angle, c_value)`.

##### `def get_means_by_rx()`
Zwraca średnie trace’y dla każdej lokalizacji RX.

##### `def get_minimums_by_rx()`
Zwraca minimalne trace’y dla każdej lokalizacji RX.

##### `def get_maximums_by_rx()`
Zwraca maksymalne trace’y dla każdej lokalizacji RX.

##### `def get_means_for_patterns_by_rx()`
Zwraca średnie wartości trace’ów dla każdego wzorca i lokalizacji RX.

##### `def get_linear_avg_by_rx()`
Zwraca średnią liniową trace’ów pogrupowanych po RX.

### Użycie

```python
results = Results(resultfilename="measurements.csv")

means, rx_keys = results.get_means_by_rx()
mins, rx_keys = results.get_minimums_by_rx()
maxs, rx_keys = results.get_maximums_by_rx()
```