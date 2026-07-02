## Arranged Codebook Formatter

### Cel
Plik konwertuje codebook zapisany w formacie binarnym z skryptów Matlaba do formatu zgodnego z klasą `Codebook`.

Wejściowy plik CSV zawiera:

`pattern;metadata`

a plik wynikowy zawiera:

`idx;pattern_hex;metadata`

### Najważniejsze elementy

#### Skrypt główny

##### `file_name`
Nazwa wejściowego pliku CSV.

##### `exit_file`
Nazwa wynikowego pliku CSV.

##### `BitArray`
Konwertuje binarny zapis wzorca, np. `010101...`, na reprezentację hex.

##### `lines_to_write`
Lista linii przygotowanych do zapisania w pliku wynikowym.

### Działanie
- otwiera plik `Arranged_codebook.csv`,
- odczytuje każdą linię,
- rozdziela ją po `;`,
- pobiera binarny wzorzec,
- konwertuje go do formatu hex,
- dodaje kolejny indeks wzorca `i`,
- zapisuje wynik do `Arranged_codebook_test.csv`.

### Kompletne przykładowe wywołanie

```python
from bitstring import BitArray

file_name = "Arranged_codebook.csv"
exit_file = "Arranged_codebook_test.csv"

i = 0
lines_to_write = []

with open(file_name, "r") as f:
    lines = f.readlines()

    for line in lines:
        line_list = line.split(";")

        # Wzorzec binarny, np. "010101..."
        pattern = line_list[0]

        # Metadane, np. lista [Tx, Rx, Rotation]
        meta_data = line_list[1]

        # Konwersja wzorca binarnego do BitArray
        bit_pattern = BitArray("0b" + pattern)

        # Format zgodny z Codebook:
        # idx;pattern_hex;metadata
        exit_line = f"{i};{bit_pattern.hex};{meta_data}"

        i += 1
        lines_to_write.append(exit_line)

with open(exit_file, "w+") as f:
    f.writelines(lines_to_write)
```

### Uwagi

- Plik wejściowy musi używać separatora ;.
- Pierwsza kolumna musi zawierać wzorzec binarny.
- Druga kolumna zawiera metadane wzorca.
- Indeksy wzorców są nadawane automatycznie od 0.
- Wynikowy wzorzec jest zapisywany w formacie hex.
- Plik wynikowy może być później wczytywany przez klasę Codebook.
