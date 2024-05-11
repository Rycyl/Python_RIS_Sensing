import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
from matplotlib.patches import Patch


def plot_bar_for_configurations(file_paths, patterns, output_folder, how_far_from_box):
    colors = ['dodgerblue', 'orange', 'green', 'red']

    for pattern in patterns:
        power_values = []
        labels = []
        first_id = None  # Variable to store the first ID found for the pattern

        for i, path in enumerate(file_paths, start=1):
            df = pd.read_csv(path, sep=';', header=None)
            df.columns = ['Configuration', 'Frequency', 'Power', 'ID']
            config_data = df[df['Configuration'].str.strip() == pattern.strip()]

            if not config_data.empty:
                if first_id is None:
                    first_id = config_data.iloc[0]['ID']  # Capture the first ID
                power = config_data.iloc[0]['Power'].round(2)
                power_values.append(power)
                labels.append(f"Path {i} ({power} dBm)")
            else:
                power_values.append(0)  # Assume zero power if no data
                labels.append(f"Path {i} (N/A)")

        plt.figure(figsize=(10, 6))
        plt.bar(labels, power_values, color=colors)
        plt.xlabel('Path Index and Power')
        plt.ylabel('Power (dBm)')
        plt.title(f'Power Levels for "{pattern}" Across Different Paths for {how_far_from_box}')
        plt.xticks(rotation=45, ha="right")
        plt.grid(True, linestyle='--', linewidth=0.5)
        plt.gca().invert_yaxis()
        plt.tight_layout()

        if first_id is not None:
            output_path = f"{output_folder}/power_levels_id_{first_id}_{how_far_from_box}.png"
            plt.savefig(output_path)
            plt.close()
            print(f"Image saved to {output_path}")
        else:
            print(f"No data found for pattern '{pattern}'")

file_paths = [
    r'C:\Users\marsieradzka\Desktop\ris\Python_RIS_Sensing\Skrypty_sensing\artykul\wyniki\TXdookol_RXdookol\1_dookolna_184.csv',
    r'C:\Users\marsieradzka\Desktop\ris\Python_RIS_Sensing\Skrypty_sensing\artykul\wyniki\TXdookol_RXdookol\2_dookolna_184.csv',
    r'C:\Users\marsieradzka\Desktop\ris\Python_RIS_Sensing\Skrypty_sensing\artykul\wyniki\TXdookol_RXdookol\3_dookolna_184.csv',
    r'C:\Users\marsieradzka\Desktop\ris\Python_RIS_Sensing\Skrypty_sensing\artykul\wyniki\TXdookol_RXdookol\4_dookolna_184.csv',
]
how_far_from_box = 184
patterns = ["All elements turn off","All elements turn on","Only first element turn on","Only last element turn on","Left side on","Right side on","Upper half on","Lower half on","Vertical strips [1010]", "Vertical strips [0101]","Horizontal strips [1010]","Horizontal strips [0101]","Chessboard [1010/0101]","Chessboard [0101/1010]","Thick vertical strips [1100]","Thick vertical strips [0011]","Thicker vertical strips [11110000]","Thicker vertical strips [00001111]","Thick horizontal strips [1100]","Thick horizontal strips [0011]","Chessboard [11001100/00110011]", "Chest","Dartboard","Random 1","Random 2","Random 3","Random 4"]
output_folder = r'C:\Users\marsieradzka\Desktop\ris\Python_RIS_Sensing\Skrypty_sensing\artykul\wykres\TXdookol_RXdookol\for_one_pattern_four_position'

plot_bar_for_configurations(file_paths, patterns, output_folder,how_far_from_box)
