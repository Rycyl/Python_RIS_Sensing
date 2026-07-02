## What is in dataset

Dataset contains several CSV files in two directories with measured traces for diffrent RIS patterns. 

- `/wyniki` contains raw data from measurments
- `/wyniki_manual_distances` contains results with manual measured locallisation points, as it occures that UWB measurments were very inaccurate.

Dataset contains results for a 24 measurement points (1–24).
Each file has a name in the format:

`{what_was_measured}_{date}_{position}.csv`

### `what_was_measured`

Codebooks:

- `Arranged_codebook_Tx-72_RX0-90_`
- `full_codebook_TXat-72_RXAT0-90_6rot_`
- `euklides_codebook_128_0`

Or optimization processes (`min` or `max`):

 - `max` - `ref_strip_by_strip_carrier_{carrier_id}`

 - `min` - `ref_strip_by_strip_carrier_{carrier_id}_min`

`carrier_id` is first of 10 carriers among which optimisation was done (all carriers are list of size [0:800]).

### `date`

Measurment date, coded as `{day}_{month}_{year}`

### `position`

Measurment point position number: increase from bottom to top within each column, then continue at the bottom of the next column, as shown below.

```text
  4 ----- 8 ----- 12 ----- 16 ----- 20 ----- 24
  |        |        |        |        |      |
  |        |        |        |        |      |
  3 ----- 7 ----- 11 ----- 15 ----- 19 ----- 23
  |        |        |        |        |      |
  |        |        |        |        |      |
  2 ----- 6 ----- 10 ------ 14 ---- 18 ----- 22
  |        |        |        |        |      |
  |        |        |        |        |      |
  1 ----- 5 -----  9 ----- 13 ----- 17 ----- 21
```
In general this scheme can be put on the mesurment Rx grid in `Room_scheme_mes_grid_and_eq.png` file. 

## `.csv` files inside:
a few columns:
```
N	 Pattern	 Power	 Alfa	 Beta	 a	 b	 c	 d	 e	 f	 trace
```
* N	 - Pattern ID
* Pattern - RIS pattern written in HEX
* Power - Mean power of whole trace (with noise)
* 	 Alfa - Tx angle
* 	 Beta - Rx angle
* 	 a, b, c, d, e, f - distances look into `Room_scheme_distances_abcdef.png`
*  trace - complete trace from spectrum analyser

## Measured Codebooks

Three codebooks ware measured:

- `Arranged_codebook_Tx-72_RX0-90_` - envoirment aware arranged codebook
- `full_codebook_TXat-72_RXAT0-90_6rot_` - envoirment aware full codebook
- `euklides_codebook_128_0` - euclidean codebook

### Envoirment aware arranged codebook

Codebook generated with script `RIS_Azimuth_aware_codebook_generation_SAVE_TO_FILE.m` from `/Codebook generator/EA_codebook`. Tx as -72 degs. Rx 0:90. 6 rotations every pi/3.

### Envoirment aware full codebook
Codebook generated with script `linear_array_save_to_file.m` from `/Codebook generator/EA_codebook`. Tx as -72 degs. Rx 0:90. 6 rotations every pi/3.

### Euclidean codebook

Codebook generated with script `class_euklides_codebook_generator.py` from `/Codebook generator` by calling:
```python
sizes = [128]
N = 1
generate_euclidean_codebooks_of_size(codebooks_sizes=[128], N=1, i_bound=10000, k_bound=1000000)
```

## Optimisation `strip_by_strip`

TO DO

## Used hardware and setup

### Hardware:

- spectrum analyser (TODO MODEL)
- signal generator (TODO MODEL)
- RIS matrix (`https://github.com/mheinri/OpenSourceRIS`)
- Custom made RIS rotable stand (wasn't rotated during this measurments)
- ROCK64 - Single Board Computer - to pass patterns to RIS via USB from PC via Ethernet
- notebook (Lenovo ThinkPad L480 with i5-TODO XXXX and TODO X GB RAM)
- UWB modules MDEK1001 (it occures that was inaccurate, so we changed distances to grid we performed manually - those are in /wyniki_manual_distances)
- Router TP-Link TL-WDR4300 (only wired connections ware used)
- Cables, cables, cables...

### Signal generator setup
TODO
### Spectrum analyser setup
TODO


## PS
`All_measurements_merged.csv` contains all measurments in one file. 
The N (Pattern IDs) are in ranges:

- 0:5k for Euclidean Codebook
- 5k:10k for Envoirment aware arranged codebook
- 10k:100k for Envoirment aware full codebook
- 100k:200k for `strip_by_strip` maximalisation
- 200k+ for `strip_by_strip` minimalisation

For `strip_by_strip` results the Patterns ID's are codes
`{mode}_{1st subcarrier}_{Nth RIS column switch}`:

- `mode`: 1 = maximalisation; 2 = minimalisation
- `1st subcarrier`: id of first subcarrier of truncaded trace (800 subcariers in total)
- `Nth RIS column switch`: which optimisation step it was


There is also a bunch of functions we made to obtain this dataset and process it and it can be found at GitHub: `TODO proponuje nowe repo na publikacje pomiarów i kodu` 