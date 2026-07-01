## Class Select

### Cel
Plik służy do tworzenia zbiorów wybranych wzorców z `Codebook` na podstawie parametrów `i`, `d` oraz kroku `phi_s`. Następnie dla każdej grupy wyznacza najlepsze moce i zapisuje wynik do pliku `.pkl`.

### Najważniejsze elementy

#### `def load_results_from_file()`
Buduje obiekt `Selected` na podstawie danych z `Results` i `Codebook`.

##### Najważniejsze działanie
- ładuje wyniki pomiarów i codebook,
- filtruje wzorce po parametrach `i`, `d`, `phi_s`,
- tworzy obiekty `Select`,
- przypisuje do nich indeksy wzorców i odpowiadające im moce.

#### `class Selected`
Kontener przechowujący listę obiektów `Select`.

##### `def dump_class_to_file()`
Zapisuje obiekt `Selected` do pliku `.pkl`.

##### `def load_from_file()`
Wczytuje obiekt `Selected` z pliku `.pkl`.

#### `class Select`
Reprezentuje grupę wzorców dla jednej pary parametrów `i` oraz `d`.

##### `def add_pat_idx()`
Dodaje wzorzec, jego przesunięcie `s`, indeks oraz wartości mocy.

##### `def find_max()`
Wyznacza:
- `maxs` — najlepsze moce dla kolejnych pozycji RX,
- `maxs_idx` — indeksy wzorców, które dały te maksima.

### Użycie
1. Utwórz `Selected` dla wybranego kroku `phi_s`.
2. Wczytaj dane z `Results` i `Codebook` przez `load_results_from_file()`.
3. Dla każdego obiektu `Select` uruchom `find_max()`.
4. Zapisz wynik przez `dump_class_to_file()`.

### Uwagi
- `Selected.selected` zawiera listę obiektów `Select`.
- `Select.powers` przechowuje moce wzorców przypisanych do danej pary `(i, d)`.
- `Select.maxs` zawiera najlepsze moce dla każdej pozycji RX.
- `Select.maxs_idx` zawiera indeksy wzorców odpowiadających wartościom z `maxs`.
- Kod zakłada, że indeks wzorca z `Codebook` odpowiada indeksowi w `results.results`.
- Lista `used_patterns` ma stały rozmiar `919`, więc kod jest powiązany z konkretnym rozmiarem codebooka.
- Warto jawnie dodać `import pickle`, ponieważ jest używany do zapisu i odczytu `.pkl`.

### Kompletne przykładowe wywołanie

```python
from class_select import Selected, load_results_from_file

# Krok próbkowania kąta phi_s.
# Np. PHI_S_STEP = 30 oznacza użycie wartości:
# 0, 30, 60, ..., 330
PHI_S_STEP = 30

# Nazwa pliku, do którego zapisany zostanie gotowy obiekt Selected
dumpfile = f"wybrane_paterny_pk_metod_s_step_{PHI_S_STEP}.pkl"

# Utworzenie pustego obiektu Selected
selected = Selected(phi_s_step=PHI_S_STEP)

# Zbudowanie obiektu Selected na podstawie danych z Results i Codebook.
# I = -49 oznacza wybraną wartość parametru i.
# Funkcja przechodzi po wartościach d od 0 do 89
# i wybiera pasujące wzorce z codebooka.
selected = load_results_from_file(
    selected=selected,
    I=-49,
    PHI_S_STEP=PHI_S_STEP
)

# Dla każdej grupy Select wyznacz najlepsze moce oraz indeksy wzorców,
# które dały maksimum dla kolejnych pozycji RX.
for select_obj in selected.selected:
    select_obj.find_max()

# Zapis gotowego obiektu Selected do pliku pickle
selected.dump_class_to_file(dumpfile=dumpfile)

# Przykładowy dostęp do pierwszego obiektu Select
first_select = selected.selected[0]

print("Parametr i:", first_select.i)
print("Parametr d:", first_select.d)
print("Dostępne przesunięcia s:", first_select.s)
print("Indeksy wzorców:", first_select.pat_idx)
print("Najlepsze moce:", first_select.maxs)
print("Indeksy wzorców dających maksimum:", first_select.maxs_idx)
```