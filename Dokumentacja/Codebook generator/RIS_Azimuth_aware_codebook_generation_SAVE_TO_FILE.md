## Arranged Codebook Generator

### Cel
Skrypt MATLAB generuje uporządkowany codebook RIS (arranged envoirment aware codebook) dla zadanego kąta `TX_angle` oraz zakresu kątów `set_RX`.

Codebook jest budowany przez grupowanie kątów RX, które generują takie same lub wystarczająco podobne wzorce binarne po obrotach fazowych. Następnie liczba rotacji fazowych jest ograniczana i wynik zapisywany jest do pliku `Arranged_codebook.csv`.

### Najważniejsze elementy

#### Parametry główne

##### `TX_angle`
Kąt nadajnika, dla którego generowany jest codebook.

##### `set_RX`
Zakres kątów odbiornika analizowanych przy generowaniu wzorców.

##### `ile_phase_rotations`
Liczba rotacji fazowych używana w końcowym codebooku.

##### `ile_patternow_moze_sie_powtarzac`
Parametr określający, ile wzorców może się powtarzać między azymutami RX zanim kolejny kąt RX zostanie przypisany do istniejącej grupy.

#### Grupowanie wzorców

##### `Patterny`
Lista grup unikalnych wzorców binarnych przypisanych do reprezentatywnych kątów RX.

##### `katy_RX_uzyte`
Lista kątów RX przypisanych do danej grupy wzorców.

##### `maks_rotacji_per_azymut`
Liczba unikalnych rotacji dla kolejnych azymutów RX.

#### Ograniczenie liczby rotacji

##### `set_phi_s2`
Lista ograniczonych rotacji fazowych używanych w końcowym codebooku.

##### `Patterns_limited_rotations`
Wzorce binarne po ograniczeniu liczby rotacji.

##### `Rotations_limited`
Lista rotacji fazowych, które pozostały po usunięciu duplikatów.

##### `Total_codebook_size`
Całkowita liczba wzorców w wygenerowanym codebooku.

#### Zapis do CSV

##### `Arranged_codebook.csv`
Plik wynikowy zawierający:
- wzorzec binarny powtórzony `16` razy,
- listę parametrów `[TX_angle, RX_angle, rotation]`, które opisują dany wzorzec.

Format linii:

`pattern;[[Tx, Rx, Rotation], [Tx, Rx, Rotation], ...]`

### Użycie

1. Ustaw kąt nadajnika:

`TX_angle = 45`

2. Ustaw zakres kątów odbiornika:

`set_RX = [-90:0]`

3. Ustaw liczbę końcowych rotacji fazowych:

`ile_phase_rotations = 6`

4. Uruchom skrypt w MATLAB-ie.

5. Po wykonaniu powstanie plik:

`Arranged_codebook.csv`

### Uwagi
- Skrypt generuje wzorce dla liniowego RIS-a o `L = 16` elementach.
- Każdy wzorzec bazowy ma długość `16`, ale przy zapisie jest powtarzany `16` razy, tworząc wzorzec długości `256`.
- `ile_phase_rotations = 6` oznacza użycie rotacji co `60°`.
- `ile_patternow_moze_sie_powtarzac = 0` tworzy najmniejszy zbiór kątów RX, bo już jeden wspólny wzorzec powoduje przypisanie RX do istniejącej grupy.
- Wartość `-1` dla `ile_patternow_moze_sie_powtarzac` oznacza, że RX nie zostanie dodany tylko wtedy, gdy wszystkie jego wzorce powtarzają się względem istniejącej grupy.
- `Patterns_limited_rotations_mat` zawiera wszystkie końcowe wzorce w postaci jednej macierzy.
- Plik CSV używa separatora `;`.
- Wynikowy format jest zgodny z dalszym wczytywaniem codebooka jako `pattern;angles`.
`