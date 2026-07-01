### Cel i działanie
Zawiera funckje do podmiany lokalizacji w plikach CSV na podstawie ręcznych pomiarów oraz siatki pomiarowej.
Podmiana jest na podstawie numeru punktu z końcówki nazwy (_N.csv)


### Parametry
if __name__ == "__main__" zawiera wywołanie i parametry:
 - 'start_x' - początek OX układu współrzędnych które mają być wprowadzone
 - 'start_y' - początek OY układu współrzędnych które mają być wprowadzone
 - 'dx' - krok w osi X
 - 'dy' - krok w osi Y
 - 'rows' - ilość wierszy na siatce
 - 'cols' - ilość kolumn na siatce
 - 'A3_y' - odkległość TAGA A3 (był mierzony ręcznie) - pukt znajdujący się w osi RISa


### Use example
```python
process_folder(folder_path, grid, A3_y)
```
funkcja która przetwarza pliki csv w podanym folderze

