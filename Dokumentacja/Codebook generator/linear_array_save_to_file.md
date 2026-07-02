## MATLAB Codebook Generator

### Cel
Skrypt generuje binarny codebook RIS dla zadanych zakresów kątów `TX` i `RX`.  (Envoirment aware full codebook)
Dla każdego kąta nadajnika, odbiornika oraz obrotu fazowego tworzy binarny prekoder, usuwa duplikaty i zapisuje unikalne wzorce do pliku CSV.

### Najważniejsze elementy

#### Parametry główne

##### `f_c`
Częstotliwość nośna.

##### `c`
Prędkość światła.

##### `d`
Odległość między elementami RIS.

##### `L`
Liczba elementów RIS w jednym wymiarze / długość wzorca bazowego.

##### `set_TX`
Zakres kątów nadajnika.

##### `set_RX`
Zakres kątów odbiornika.

##### `rotations`
Lista obrotów fazowych używanych do generowania wzorców:

#### Generowanie wzorców

##### `prekoder_ideal`
Idealny zespolony prekoder wyznaczany dla kombinacji `TX` i `RX`.

##### `prekoder_binary`
Binarna wersja prekodera tworzona na podstawie znaku części rzeczywistej po zadanym obrocie fazowym.

##### `B`
Macierz zawierająca wszystkie wygenerowane binarne wzorce.

##### `params`
Macierz przechowująca parametry `[Tx, Rx, Rotation]` odpowiadające każdemu wzorcowi w `B`.

#### Usuwanie duplikatów

##### `unique(B, 'rows')`
Usuwa powtarzające się wzorce binarne.

Wyniki:
- `BB` — unikalne wzorce binarne,
- `ic` — indeks mówiący, który oryginalny wzorzec odpowiada któremu unikalnemu wzorcowi.

#### Zapis do CSV

##### `codebook_test.csv`
Plik wynikowy zawierający:
- wzorzec binarny powtórzony `16` razy,
- listę parametrów `[Tx, Rx, Rotation]`, które wygenerowały ten wzorzec.

Format linii:

`pattern;[[Tx, Rx, Rotation], [Tx, Rx, Rotation], ...]`

### Użycie

1. Ustaw zakresy kątów:

`set_TX = -72:-68`

`set_RX = 0:80`

2. Ustaw parametry RIS:

`f_c`, `c`, `d`, `L`

3. Uruchom skrypt w MATLAB-ie.

4. Po wykonaniu powstanie plik:

`codebook_test.csv`

### Uwagi
- Skrypt generuje wzorce dla liniowego RIS-a o długości `L = 16`.
- Każdy wzorzec bazowy ma długość `16`, ale przy zapisie jest powtarzany `16` razy, tworząc wzorzec długości `256`.
- Obroty fazowe są zapisywane w stopniach dzięki `rad2deg()`.
- `BB` zawiera tylko unikalne wzorce.
- Jeden unikalny wzorzec może odpowiadać wielu kombinacjom `Tx`, `Rx` i `Rotation`.
- Plik CSV używa separatora `;`.
- Wynikowy format jest zgodny z dalszym wczytywaniem codebooka jako `pattern;angles`.