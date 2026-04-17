import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re
from math import sqrt, cos, radians, sin

def calc_z(x, b, theta):
    half_b = b/2
    return sqrt(x**2 + half_b**2 - 2*x*half_b*cos(theta))

def polar_to_cartesian(z, theta):
    x = z * cos(theta)
    y = z * sin(theta)
    return x, y

def normalize_to_grid(x, y, x_min, x_max, y_min, y_max):
    norm_x = (x - x_min) / (x_max - x_min)
    norm_y = (y - y_min) / (y_max - y_min)
    return norm_x, norm_y

# def get_heatmap_position(x_mm, y_mm, x_min, y_min, cell_width=660, cell_height=500):
#     grid_x = int(round((x_mm - x_min) / cell_width))
#     grid_y = int(round((y_mm - y_min) / cell_height))

#     # Optional: flip X if needed
#     # grid_x = max_x_index - grid_x

#     return (grid_y, grid_x)

def extract_number(filename):
    match = re.search(r'(\d+)(?=\.csv$)', filename)
    return int(match.group(1)) if match else -1  # Return -1 if no number found

def read_from_files(N):
    # Folder with your CSVs
    folder = os.path.join(os.getcwd(), "Math_model_codebook_measures", "wyniki", "grid_measures_30_Apr")
    csv_files = [f for f in os.listdir(folder) if f.endswith('.csv') and f.startswith("Big_codebook")]
    csv_files.sort(key=extract_number)
    print(csv_files)
    # Initialize empty heatmap data and pattern (assume pattern is same for all rows in a file)
    heatmap_data = np.full((5, 3), np.nan)
    pattern_title = ""

    x_y = [(4,2), (3,2), (2,2), (1,2), (0,2), (0,1), (1,1), (2,1), (3,1), (4,1), (4,0), (3,0), (2,0), (1,0), (0,0)]

    # Choose a specific state to visualize (e.g., N == 0)
    TARGET_N = N
    
    # Gather all x and y to compute mins
    x_vals, y_vals = [], []
    for f in csv_files:
        df = pd.read_csv(os.path.join(folder, f), sep=';', dtype={'Pattern': str}, skipinitialspace=True, index_col=False)
        row = df[df['N'] == TARGET_N]
        if not row.empty:
            x_vals.append(float(row['x'].iloc[0]))
            y_vals.append(float(row['y'].iloc[0]))

    x_min, x_max = min(x_vals), max(x_vals)
    y_min, y_max = min(y_vals), max(y_vals)
    

    for i in range(len(x_y)):
        df = pd.read_csv(os.path.join(folder, csv_files[i]), sep=';', dtype={'Pattern': str}, skipinitialspace=True, index_col=False)
        row = df[df['N'] == TARGET_N]
        if not row.empty:
            x, y = x_y[i]
            c_x, c_y = float(row['x'].iloc[0]), float(row['y'].iloc[0])
            print("Data in:: ")
            print(c_x, c_y)
            print("Data out:: ")
            theta = radians(float(row['Rx Angle'].iloc[0]))
            b = float(row['b'].iloc[0]) / 2
            z = calc_z(c_x, b, theta)
            cart_x, cart_y = polar_to_cartesian(z, theta)
            grid_x, grid_y = normalize_to_grid(cart_x, cart_y, x_min, x_max, y_min, y_max)
            print(grid_x, grid_y)
            power = float(row['Power'].iloc[0])
            #print(power)
            pattern_title = row['Pattern'].values[0]  # Assume consistent pattern
            heatmap_data[x][y] = power
    return heatmap_data, pattern_title


def plot_heat_map(heatmap_data, title, save = False):
    # Plotting
    plt.figure(figsize=(6, 5))
    ax = sns.heatmap(np.flip(heatmap_data.T, axis=1), annot=True, cmap='viridis', cbar_kws={'label': 'Power'}, annot_kws={"size": 14, "weight": "bold",})
    colorbar = ax.collections[0].colorbar
    colorbar.ax.tick_params(labelsize=12)
    colorbar.ax.yaxis.label.set_size(13)
    colorbar.ax.yaxis.label.set_weight("bold")
    colorbar.ax.tick_params(labelsize=12, width=1.5)
    for tick in colorbar.ax.get_yticklabels():
        tick.set_weight("bold")
    plt.xticks(ticks=np.arange(0.5, 5, step=1), labels=np.arange(4, -1, -1), fontsize = 12, fontweight='bold')
    plt.yticks(ticks=np.arange(0.5, 3, step=1), fontsize = 12, fontweight='bold')
    plt.title(title, fontsize=14, fontweight='bold') #f"Heatmap for Pattern: {pattern_title}"
    plt.xlabel("X", fontsize=13, fontweight='bold')
    plt.ylabel("Y", fontsize=13, fontweight='bold')
    plt.gca().invert_yaxis()  # Optional: match matrix orientation
    plt.tight_layout()
    if not save:
        plt.show()
    else:
        plt.savefig(f"Heat_map_{title}.png")

def read_and_plot(N, save = False):
    heatmap_data, pattern_title = read_from_files(N)
    title = f"Heatmap for Pattern: {pattern_title}"
    plot_heat_map(heatmap_data, title, save)



if __name__ == "__main__":
    read_and_plot(1)