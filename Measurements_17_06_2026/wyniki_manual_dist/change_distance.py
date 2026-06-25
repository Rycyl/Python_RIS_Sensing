from mes_grid import PointGrid
import pandas as pd
import os
import numpy as np

Ea_file = 'EA_tx_-69_-72_RX_0_80_17_Jun_2026_'
Eu_file = 'euklides_codebook_128_0_17_Jun_2026_'
ref_file_head = 'ref_strip_by_strip_carrier_'
ref_file_tail = '_17_Jun_2026_'

start_x = 0
start_y = 240
dx = 122
dy = 122
rows = 3
cols = 6

A3_y = 6.98

num_of_points = rows*cols

grid = PointGrid(start_x, start_y, dx, dy, rows, cols)

c_list = np.linspace(0, 789, 10, dtype=np.int16)

for i in range(num_of_points):
    input_Ea = Ea_file+f'{i+1}.csv'
    input_Eu = Eu_file+f'{i+1}.csv'
    c, beta = grid.get_polar(i+1)
    e = grid.get_distance_from_y_axis_point(i+1, A3_y)
    # print(c)
    # print(beta)
    # print(e)
    df_s = []
    df_s.append(pd.read_csv(input_Ea,sep=';',index_col=False))
    df_s.append(pd.read_csv(input_Eu,sep=';',index_col=False))
    for c in c_list:
        input_ref = ref_file_head+f'{c}'+ref_file_tail+f'{i+1}.csv'
        df_s.append(pd.read_csv(input_ref,sep=';',index_col=False))
    for df in df_s:
        df[' Beta'] = str(beta)
        df[' c'] = str(c/100)
        df[' e'] = str(e/100)
    Ea_df = df_s.pop(0)
    Eu_df = df_s.pop(0)
    Ea_df.to_csv(input_Ea, sep=';', index=False)
    Eu_df.to_csv(input_Eu, sep=';', index=False)
    for c in c_list:
        output_ref = ref_file_head+f'{c}'+ref_file_tail+f'{i+1}.csv'
        Ref_df = df_s.pop(0)
        Ref_df.to_csv(output_ref, sep=';', index=False)

print("Done")

    