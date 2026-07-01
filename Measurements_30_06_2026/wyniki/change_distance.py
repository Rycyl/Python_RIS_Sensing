from mes_grid import PointGrid
import pandas as pd
import os
import numpy as np
import re

def process_folder(folder_path, grid, A3_y):
    # dopasowanie numeru punktu z końcówki nazwy (_N.csv)
    pattern = re.compile(r'_(\d+)\.csv$')

    # {punkt: [pliki]}
    points_files = {}

    # zbieranie plików
    for file in os.listdir(folder_path):
        match = pattern.search(file)
        if match:
            point_id = int(match.group(1))
            points_files.setdefault(point_id, []).append(file)

    # przetwarzanie
    for i in sorted(points_files.keys()):
        c, beta = grid.get_polar(i)
        e = grid.get_distance_from_y_axis_point(i, A3_y)

        print(f"Point {i}")
        print(c / 100)
        print(beta)
        print(e / 100)

        for file in points_files[i]:
            full_path = os.path.join(folder_path, file)

            # wczytaj
            df = pd.read_csv(full_path, sep=';', index_col=False)

            # dodaj kolumny
            df[' Beta'] = str(beta)
            df[' c'] = str(c / 100)
            df[' e'] = str(e / 100)

            # nadpisz plik
            df.to_csv(full_path, sep=';', index=False)

    print("Done")

if __name__ == "__main__":
    
    start_x = 0
    start_y = 240
    dx = 122
    dy = 122
    rows = 4
    cols = 6

    A3_y = 7.02

    num_of_points = rows*cols

    grid = PointGrid(start_x, start_y, dx, dy, rows, cols)
    c_list = np.linspace(0, 789, 10, dtype=np.int32)

    folder = os.getcwd()

    process_folder(
        folder_path=folder,
        grid=grid,     # zakładam, że masz już utworzony obiekt grid
        A3_y=A3_y
    )