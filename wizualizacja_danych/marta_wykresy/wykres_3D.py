import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import re
from mpl_toolkits.mplot3d import Axes3D

def extract_distance_from_filename(filename):
    match = re.search(r'(\d+)cm', filename)
    return int(match.group(1)) if match else None

def process_csv_files_for_pattern(file_paths, selected_pattern):
    aggregated_data = []

    for file_path in file_paths:
        print(f"Processing file: {file_path}")
        distance = extract_distance_from_filename(os.path.basename(file_path))
        if distance is None:
            continue

        df = pd.read_csv(file_path, sep=';', names=['Configuration', 'Frequency', 'Power'])
        filtered_df = df[(df['Configuration'] == selected_pattern) & (df['Frequency'] >= 5e9) & (df['Frequency'] <= 5.9e9)]
        filtered_df['Frequency'] = filtered_df['Frequency'] / 1e9
        
        mean_power_df = filtered_df.groupby('Frequency')['Power'].mean().reset_index()
        mean_power_df['Distance'] = distance
        aggregated_data.append(mean_power_df)

    return pd.concat(aggregated_data, ignore_index=True) if aggregated_data else pd.DataFrame()

def plot_data_3d(data):
    if data.empty:
        print("No data to plot.")
        return

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    distances = data['Distance'].unique()
    colors = plt.cm.jet(np.linspace(0, 1, len(distances)))
    
    for color, distance in zip(colors, distances):
        dist_data = data[data['Distance'] == distance]
        dist_data = dist_data.sort_values(by='Frequency')
        ax.plot(dist_data['Frequency'], [distance] * len(dist_data), dist_data['Power'], marker='o', linestyle='-', color=color, label=f'Distance {distance} cm')

    ax.set_xlabel('Frequency (GHz)')
    ax.set_ylabel('Distance (cm)')
    ax.set_zlabel('Power (dBm)')
    ax.set_title('Name of pattern: ' + selected_pattern)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title="Distance")
    plt.tight_layout()
    plt.show()

file_paths = [
    r'C:\Users\marsieradzka\Desktop\ris\Python_RIS\wyniki\18_03_24_03\19_03_reflection_20cm_3_5cm_17cm.csv',
    r'C:\Users\marsieradzka\Desktop\ris\Python_RIS\wyniki\18_03_24_03\22_03_24_reflection_30cm_3_5cm.csv',
    r'C:\Users\marsieradzka\Desktop\ris\Python_RIS\wyniki\18_03_24_03\22_03_24_reflection_40cm_3_5cm.csv',
   
]

selected_pattern = "Horizontal strips [0101]"


aggregated_data = process_csv_files_for_pattern(file_paths, selected_pattern)
plot_data_3d(aggregated_data)
