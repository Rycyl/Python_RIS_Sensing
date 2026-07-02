## What is in dataset

Dataset contains several CSV files with measured traces for diffrent RIS patterns. 
Dataset contains a total of 24 measurement points (1–24).
Each file has a name in the format:

`{what_was_measured}_{date}_{position}.csv`

### `what_was_measured`

Codebook names:

- `Arranged_codebook_Tx-72_RX0-90_`
- `full_codebook_TXat-72_RXAT0-90_6rot_`
- `euklides_codebook_128_0`

Or optimization process (`min` or `max`):

 - `max` - `ref_strip_by_strip_carrier_{carrier_id}`

 - `min` - `ref_strip_by_strip_carrier_{carrier_id}_min`

`carrier_id` is first of 10 carriers (total carriers are list of size [0:800]) among which the recieved power was optimised.

### `date`

Is coded as `{day}_{month}_{year}`

### `position`

Point numbers increase from bottom to top within each column, then continue at the bottom of the next column, as shown below. In general this scheme can be put the mesurment Rx grid in `Room_scheme_mes_grid_and_eq.png` file. 

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

## Codebooks

Three codebooks ware measured:

- `Arranged_codebook_Tx-72_RX0-90_` - envoirment aware arranged codebook
- `full_codebook_TXat-72_RXAT0-90_6rot_` - envoirment aware full codebook
- `euklides_codebook_128_0` - euclidean codebook

### Envoirment aware arranged codebook

Codebook generated with script `RIS_Azimuth_aware_codebook_generation_SAVE_TO_FILE.m` from `/Codebook generator/EA_codebook`

### Envoirment aware full codebook
Codebook generated with script `linear_array_save_to_file.m` from `/Codebook generator/EA_codebook`

### Euclidean codebook

Codebook generated with script `class_euklides_codebook_generator.py` from `/Codebook generator` by calling:
```python
sizes = [128]
N = 1
generate_euclidean_codebooks_of_size(codebooks_sizes=[128], N=1, i_bound=10000, k_bound=1000000)
```
