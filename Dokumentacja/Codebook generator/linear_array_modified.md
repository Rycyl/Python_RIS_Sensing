## MATLAB AF / Binary Precoder Generator

### Cel
Skrypt MATLAB służy do analizy charakterystyki kierunkowej `Array Factor` dla liniowego RIS-a oraz do generowania binarnych prekoderów / wzorców RIS dla różnych kątów TX i RX.

Porównuje:
- idealny prekoder fazowy,
- binarny prekoder,
- binarny prekoder obrócony fazowo o `π/2`.

### Najważniejsze elementy

#### Parametry główne

##### `f_c`
Częstotliwość nośna.

##### `d`
Odległość między elementami RIS.

##### `L`
Liczba elementów antenowych / RIS.

##### `kat_TX`
Kąt nadajnika względem RIS-a.

##### `kat_RX`
Kąt odbiornika względem RIS-a.

#### Obliczanie kanału i prekodera

##### `kanal_do_od_RIS`
Model kanału od TX do RIS i od RIS do RX.

##### `prekoder`
Idealny prekoder liczony jako sprzężenie zespolone kanału.

##### `prekoder_bin`
Binarna wersja prekodera wyznaczana na podstawie znaku części rzeczywistej.

### Główne części skryptu

#### Porównanie charakterystyk AF
Skrypt rysuje `Array Factor` dla:
- dokładnego prekodera zespolonego,
- binarnego prekodera,
- binarnego prekodera obróconego o `π/2`.

#### Wizualizacja prekoderów
Tworzy mapy:
- fazy idealnego prekodera,
- binarnego wzorca,
- binarnego wzorca obróconego o `π/2`.

#### Generowanie zbioru wzorców
Dla zakresów:
- `set_TX = 0:90`,
- `set_RX = -90:90`,

generowane są binarne wzorce dla czterech obrotów fazowych:
- `0`,
- `π/2`,
- `π`,
- `3π/2`.

Następnie usuwane są duplikaty.

#### Redukcja po odległości Hamminga
Skrypt usuwa wzorce zbyt podobne do już wybranych.

Warunek usuwania:

```matlab
sum(xor(BB(i,:), BB(ii,:))) <= 2
```