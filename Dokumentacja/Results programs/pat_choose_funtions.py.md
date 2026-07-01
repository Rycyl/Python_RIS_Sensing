## Pattern Selection / Bitrate Analysis

### Cel
Plik służy do porównywania metod wyboru wzorców RIS oraz oceny ich jakości na podstawie metryki przepływności / efektywności widmowej. Zawiera algorytmy wyboru wzorców, funkcje metryczne, zapis/odczyt wyników oraz funkcje do generowania wykresów i heatmap.

### Najważniejsze elementy

#### Funkcje pomocnicze

##### `def dump_array_to_file()`
Zapisuje tablicę lub obiekt do pliku `.pkl`.

##### `def read_array_from_file()`
Odczytuje tablicę lub obiekt z pliku `.pkl`.

##### `def dbm_to_mw()`
Konwertuje moc z dBm na mW.

##### `def mw_to_dbm()`
Konwertuje moc z mW na dBm.

##### `def white_noise()`
Oblicza poziom szumu cieplnego dla podanego pasma.

##### `def przeplywnosc()`
Liczy efektywność widmową na podstawie mocy odebranej i poziomu szumu.

##### `def metric()`
Liczy sumaryczną metrykę jakości dla zestawu wybranych wzorców.

#### Funkcje przygotowania danych

##### `def mean_power_with_ris()`
Liczy średnią moc dla wyników RIS.

##### `def global_maximum_powers_in_pos()`
Wyznacza maksymalne moce dla każdej pozycji odbiornika.

##### `def merge_selections()`
Scala wybrane wyniki do tablicy wartości maksymalnych.

##### `def save_powers()`
Zapisuje dane mocy do pliku CSV.

#### `class PatternSelector`
Klasa implementująca algorytmy wyboru najlepszych wzorców na podstawie zadanej metryki.

##### `def Greedy()`
Wybiera wzorce zachłannie, dodając kolejne dające największy przyrost metryki.

##### `def Random()`
Losowo wybiera zestawy wzorców i zwraca najlepszy znaleziony wynik.

##### `def Genetic()`
Wybiera wzorce za pomocą algorytmu genetycznego.

##### `def fitness()`
Liczy wartość dopasowania osobnika w algorytmie genetycznym.

##### `def metric()`
Liczy metrykę jakości dla zestawu wzorców.

##### `def przeplywnosc()`
Liczy efektywność widmową dla pojedynczej wartości mocy.

#### Funkcje uruchamiania selekcji

##### `def run_select_function()`
Uruchamia wybraną metodę selekcji (`Greedy`, `Random`, `Genetic`) dla kolejnych wartości liczby wzorców `N`.

##### `def get_patterns_amount_from_sel()`
Oblicza rzeczywistą liczbę wzorców użytych w danej selekcji.

#### Funkcje analizy wyników

##### `def global_max_curve_finder_direct_results()`
Szuka globalnej krzywej maksimum bezpośrednio na podstawie wyników.

##### `def global_max_curve_finder_from_heuristics_results()`
Buduje krzywą najlepszego wyniku na podstawie rezultatów metod heurystycznych.

##### `def metric_cohenence_time()`
Liczy metrykę z uwzględnieniem czasu koherencji i czasu przełączania RIS.

#### Funkcje wykresów

##### `def plot_reg()`
Rysuje wykres regresji dla jednej serii danych.

##### `def plot_reg_series()`
Rysuje kilka serii wyników na jednym wykresie.

##### `def plot_reg_series_by_no_of_patterns()`
Rysuje wyniki względem rzeczywistej liczby użytych wzorców.

##### `def plot_n_pats_bitrate()`
Rysuje efektywność widmową w funkcji liczby wybranych wzorców.

##### `def plot_bitrate_in_loc()`
Rysuje przepływność lub moc dla poszczególnych lokalizacji odbiornika.

##### `def plot_metric_cohenence_time()`
Rysuje wpływ liczby wzorców i czasu przełączania RIS na metrykę jakości.

#### Funkcje heatmap

##### `def plot_heatmap_bitrate()`
Tworzy heatmapy efektywności widmowej dla różnych metod wyboru wzorców.

##### `def plot_heatmap_powers()`
Tworzy heatmapy SNR / mocy dla wyników referencyjnych i heurystycznych.

##### `def plot_heatmap_powers_snr_to_mean_ris()`
Tworzy heatmapy różnicy względem średniego wyniku RIS.

#### Funkcje statystyczne

##### `def errorbar_function()`
Wyznacza zakres błędu na podstawie dolnych i górnych 10% wartości.

##### `def estimator_function()`
Liczy średnią obciętą po odrzuceniu skrajnych wartości.

##### `def badanie_genetycznego_save_result()`
Zapisuje wyniki testów algorytmu genetycznego do pliku CSV.

### Użycie

Uruchomienie selekcji wzorców:

```python
pattern_selector = PatternSelector(
    data=merge,
    mean_power_with_ris=mean_power_with_ris,
    N=4,
    iterations=1000
)

score, powers, positions = pattern_selector.Genetic()
```

Uruchomienie wybranej metody dla wielu wartości N:
```python
y, powss, poss = run_select_function(2    merge=merge,3    pattern_selector=pattern_selector,4    range_low=1,5    range_max=16,6    i_bound=50,7    pat_sel_function_name="Random"
```

Rysowanie wyników:
```python
plot_reg_series_by_no_of_patterns(
    yy,
    yy_legend,
    yy_number_of_patterns,
    XLOG=True,
    SHOW=True,
    SAVE=False)
```

Zapis / odczyt wyników (pliki):
```python
dump_array_to_file(yy, "yy_data.pkl")
yy = read_array_from_file("yy_data.pkl")
```

####Uwagi

- Plik korzysta z klas Results, Selected, Results_Ref, Codebook.
- Porównywane metody wyboru wzorców to głównie Random, Greedy i Genetic.
- Metryka bazuje na efektywności widmowej liczonej z mocy odebranej.
- Wyniki pośrednie są cache’owane w plikach .pkl.
- Wykresy mogą być zapisywane automatycznie do folderów nazwanych jak funkcje.
- Wymagane zależności: numpy, matplotlib, scipy, seaborn, pandas.