import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.patches import Patch

def plot_all_patterns_one_chart_refined(file_paths, patterns, output_folder, how_far_from_box):
    
    colors = ['dodgerblue', 'orange', 'green', 'red']
    bar_width = 0.1
    group_width = len(file_paths) * bar_width
    space_between_groups = 0.05
    
    plt.figure(figsize=(len(patterns) * 2, 8))

    all_positions = []
    for idx, pattern in enumerate(patterns):
        power_values = []
        for i, path in enumerate(file_paths):
            df = pd.read_csv(path, sep=';', names=['Configuration', 'Frequency', 'Power','ID'])
            config_data = df[df['Configuration'] == pattern]
            if not config_data.empty:
                power_values.append(config_data.iloc[0]['Power'].round(2))
            else:
                power_values.append(None)

        start_position = idx * (group_width + space_between_groups)
        positions = [start_position + i * bar_width for i in range(len(file_paths))]
        all_positions.append(sum(positions) / len(positions))
        
        for i, power in enumerate(power_values):
            if power is not None:
                plt.bar(positions[i], power + 100, bottom=-100, color=colors[i], width=bar_width, label=f"Position {i+1}" if idx == 0 else "")

    plt.xlabel('Pattern')
    plt.ylabel('Power (dBm)')
    plt.title(f'Power Levels Across All Patterns and Paths for distance {how_far_from_box}')
    plt.xticks(all_positions, patterns, rotation=45, ha="right")
    plt.ylim([-90, -60])
    legend_handles = [Patch(facecolor=colors[i], label=f'Position {i+1}') for i in range(len(file_paths))]
    plt.legend(handles=legend_handles, title="Position", loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    #plt.gca().invert_yaxis()
    plt.tight_layout()

    
    output_path = f"{output_folder}/all_patterns_one_chart_refined_{how_far_from_box}.png"
    plt.savefig(output_path)
    plt.close()

    print(f"Image saved to {output_path}")


file_paths = [
    r'C:\Users\marsieradzka\Desktop\ris\Python_RIS_Sensing\Skrypty_sensing\artykul\wyniki\TXdookol_RXdookol\1_dookolna_184.csv',
    r'C:\Users\marsieradzka\Desktop\ris\Python_RIS_Sensing\Skrypty_sensing\artykul\wyniki\TXdookol_RXdookol\2_dookolna_184.csv',
    r'C:\Users\marsieradzka\Desktop\ris\Python_RIS_Sensing\Skrypty_sensing\artykul\wyniki\TXdookol_RXdookol\3_dookolna_184.csv',
    r'C:\Users\marsieradzka\Desktop\ris\Python_RIS_Sensing\Skrypty_sensing\artykul\wyniki\TXdookol_RXdookol\4_dookolna_184.csv',
]
how_far_from_box = 184
patterns = ["All elements turn off","All elements turn on","Only first element turn on","Only last element turn on","Left side on","Right side on","Upper half on","Lower half on","Vertical strips [1010]", "Vertical strips [0101]","Horizontal strips [1010]","Horizontal strips [0101]","Chessboard [1010/0101]","Chessboard [0101/1010]","Thick vertical strips [1100]","Thick vertical strips [0011]","Thicker vertical strips [11110000]","Thicker vertical strips [00001111]","Thick horizontal strips [1100]","Thick horizontal strips [0011]","Chessboard [11001100/00110011]", "Chest","Dartboard","Random 1","Random 2","Random 3","Random 4"]
output_folder = r'C:\Users\marsieradzka\Desktop\ris\Python_RIS_Sensing\Skrypty_sensing\artykul\wykres\TXdookol_RXdookol'
plot_all_patterns_one_chart_refined(file_paths, patterns, output_folder, how_far_from_box)
