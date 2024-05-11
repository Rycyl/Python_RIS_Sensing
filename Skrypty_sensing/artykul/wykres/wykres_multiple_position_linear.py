import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.patches import Patch


def plot_all_patterns_one_line_chart(file_paths, patterns, output_folder, how_far_from_box):
    
    colors = ['dodgerblue', 'orange', 'green', 'red']  # Line colors for each file path
    plt.figure(figsize=(len(patterns) * 2, 8))

    # Plot data for each pattern across all file paths
    for i, path in enumerate(file_paths):
        power_values = []
        for pattern in patterns:
            df = pd.read_csv(path, sep=';', names=['Configuration', 'Frequency', 'Power','ID'])
            config_data = df[df['Configuration'] == pattern]
            if not config_data.empty:
                power_values.append(config_data.iloc[0]['Power'].round(2))
            else:
                power_values.append(None)

        plt.plot(patterns, power_values, marker='o', linestyle='-', color=colors[i], label=f"Path {i+1}")

    plt.xlabel('Pattern')
    plt.ylabel('Power (dBm)')
    plt.title(f'Power Levels Across All Patterns and Paths for distance {how_far_from_box}')
    plt.xticks(rotation=45, ha="right")
    plt.ylim([-90, -60])
    plt.legend(title="Path")
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.gca().invert_yaxis()
    plt.tight_layout()

    output_path = f"{output_folder}/all_patterns_one_line_chart_{how_far_from_box}.png"
    plt.savefig(output_path)
    plt.close()

    print(f"Image saved to {output_path}")


file_paths = [
    r'C:\Users\marsieradzka\Desktop\ris\Python_RIS_Sensing\Skrypty_sensing\artykul\wyniki\TXkier_RXkier\RX_1_184.csv',
    r'C:\Users\marsieradzka\Desktop\ris\Python_RIS_Sensing\Skrypty_sensing\artykul\wyniki\TXkier_RXkier\RX_2_184.csv',
    r'C:\Users\marsieradzka\Desktop\ris\Python_RIS_Sensing\Skrypty_sensing\artykul\wyniki\TXkier_RXkier\RX_3_184.csv',
    r'C:\Users\marsieradzka\Desktop\ris\Python_RIS_Sensing\Skrypty_sensing\artykul\wyniki\TXkier_RXkier\RX_4_184.csv',
]
how_far_from_box = 184
patterns = ["All elements turn off","All elements turn on","Only first element turn on","Only last element turn on","Left side on","Right side on","Upper half on","Lower half on","Vertical strips [1010]", "Vertical strips [0101]","Horizontal strips [1010]","Horizontal strips [0101]","Chessboard [1010/0101]","Chessboard [0101/1010]","Thick vertical strips [1100]","Thick vertical strips [0011]","Thicker vertical strips [11110000]","Thicker vertical strips [00001111]","Thick horizontal strips [1100]","Thick horizontal strips [0011]","Chessboard [11001100/00110011]", "Chest","Dartboard","Random 1","Random 2","Random 3","Random 4"]
output_folder = r'C:\Users\marsieradzka\Desktop\ris\Python_RIS_Sensing\Skrypty_sensing\artykul\wykres\TXkier_RXkier'
plot_all_patterns_one_line_chart(file_paths, patterns, output_folder, how_far_from_box)
