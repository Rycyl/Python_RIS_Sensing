## Plotting / Analysis utils

### Cel
Plik zawiera funkcje do analizy wyników pomiarów oraz generowania wykresów porównujących codebooki, trace’y, moce, odległości Hamminga i przebieg optymalizacji.

### Najważniejsze elementy

#### Funkcje wykresów mocy i codebooków

##### `def pow_in_pos_channels()`
Rysuje posortowane moce wzorców oraz linie min/max/mean dla kanałów i referencji.

#### Funkcje wykresów trace’ów

##### `def plot_minmax_traces()`
Rysuje trace najlepszego/najgorszego wzorca z codebooka oraz trace referencyjne `max` / `min`.

##### `def plot_optimization_process_traces()`
Rysuje trace’y kolejnych iteracji procesu optymalizacji dla wybranej nośnej `N`.

#### Funkcje dodatkowych analiz
##### `def plot_heatmap_3d()`
Tworzy heatmapy różnicy `max - avg` dla pozycji RX w układzie XY.

#### Funkcje pomocnicze

##### `def sort_y_by_x()`
Sortuje wartości `y` zgodnie z kolejnością rosnącą wartości `x`.

##### `def hamming_distance()`
Liczy odległość Hamminga między dwoma wzorcami bitowymi.

##### `def list_files_from_folder()`
Zwraca listę plików z folderu, opcjonalnie filtrowaną po rozszerzeniach.

### Stare funkcje 

#### Funkcje wykresów mocy i codebooków
##### `def plot_power_in_position()`
Tworzy osobne wykresy mocy wzorców dla kolejnych pozycji RX.

##### `def plot_pow_in_pos_teams_all_in_one()`
Porównuje kilka codebooków na jednym wykresie dla każdej pozycji RX.

##### `def plot_pow_in_pos_teams()`
Tworzy wykresy posortowanej mocy dla wszystkich wzorców w wynikach.

##### `def plot_pow_in_pos_merge()`
Tworzy jeden zbiorczy wykres mocy dla wszystkich pozycji RX/TX.

#### Funkcje wykresów trace’ów

##### `def plot_mean_max_trace()`
Rysuje średnie maksimum trace’ów w zależności od rozmiaru codebooka.

##### `def plot_mean_max_per_carrier_in_trace()`
Analizuje maksymalne wartości per nośna dla codebooków.

#### Funkcje dodatkowych analiz

##### `def plot_pattern_characteristics()`
Rysuje charakterystyki pojedynczych wzorców względem kąta RX.

##### `def plot_hamming()`
Rysuje odległość Hamminga wzorców względem najlepszego wzorca dla danej pozycji.

### Użycie

```python
    results = Results(dumpfile="results.pkl")

    cbs_files = ["cb_name1.pkl", "cb_name2.pkl", "cb_name3.pkl"]
    cbs_names = ["NAME1", "NAME2", "NAME3"]

    cbs = []
    for cb_file in cbs_files:
        cbs.append(Codebook(dumpfile=cb_file, filename=cb_file))
    #some unified parameters
    save = True
    show = not save
    veryfy_mins = False
    save_file_format = 'png'

    pow_in_pos_channels(results=results,
                                     codebooks=cbs,
                                     show=show, 
                                     save=save, 
                                     Cbs_names=cbs_names, 
                                     save_format=save_file_format,
                                     veryfy_mins = veryfy_mins,
                                     save_filename="Min_weryfikacja_rx"
                                    )
    plot_heatmap_3d(results=results,
                    codebooks=cbs,
                    show=show, 
                    save=save, 
                    Cbs_names=cbs_names, 
                    save_format=save_file_format
                    )

    plot_minmax_traces(
        results=results,
        codebooks=cbs,
        Cbs_names=cbs_names,
        minmax='max',
        ref_in_range=list(range(100001, 100017)),
        show=show,
        save=save
    )

    plot_minmax_traces(
        results=results,
        codebooks=cbs,
        Cbs_names=cbs_names,
        minmax='min',
        ref_in_range=list(range(200001, 200017)),
        show=show,
        save=save
    )

    plot_optimization_process_traces(
        results=results,
        process='min',
        opt_N=0,
        show=show,
        save=save,
        cmap_name="Reds"
    )   

    plot_optimization_process_traces(
        results=results,
        process='max',
        opt_N=0,
        show=show,
        save=save,
        cmap_name="Reds"
    )   