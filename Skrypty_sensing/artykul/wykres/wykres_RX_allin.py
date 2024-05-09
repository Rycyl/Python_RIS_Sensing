import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import io

def plot_multiple_patterns_from_csv(file_path, patterns,output_folder):
    df = pd.read_csv(file_path, sep=';', names=['Configuration', 'Frequency', 'Power','ID'])

    df['Frequency'] = df['Frequency'] / 1e9
    df = df[(df['Frequency'] >= 5.0) & (df['Frequency'] <= 5.9)]
    
    df = df.sort_values(by='Frequency')

    plt.figure(figsize=(12, 8))
    
    colors = plt.cm.tab20.colors
    
    for index, pattern in enumerate(patterns):
        specific_pattern_df = df[df['Configuration'] == pattern]

        if specific_pattern_df.empty:
            print(f"No entries found for pattern '{pattern}'.")
            continue

        color = colors[index % len(colors)]
        plt.plot(specific_pattern_df['Power'], specific_pattern_df['Frequency'], marker='o', linestyle='-', label=pattern, color=color)

    plt.xlabel('Power (dBm)')
    plt.ylabel('Frequency (GHz)')
    plt.title('Frequency vs. Power for Multiple Configurations')
    plt.ylim(5.0, 5.9)
    #plt.ylim(power_min, power_max)
    #plt.xticks([x * 0.1 for x in range(50, 60)], rotation=45)  
    #plt.yticks([y * 2 for y in range(int(power_min / 2), int(power_max / 2 + 1))])  
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 5}, ncol=1, handletextpad=2, labelspacing=1.5, borderpad=1, frameon=True)
    plt.grid(True)
    #plt.show()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='jpeg', bbox_inches='tight')
    buf.seek(0)
        
    image = Image.open(buf)
    image.save(f"{output_folder}/1_dookolna_184_allin.jpg")
    plt.close()
        

file_path = open(r'C:\Users\marsieradzka\Desktop\ris\Python_RIS_Sensing\Skrypty_sensing\artykul\wyniki\TXdookol_RXdookol\1_dookolna_184.csv')
patterns = ["All elements turn on","Only first element turn on","Only last element turn on","Left side on","Right side on","Upper half on","Lower half on","Vertical strips [1010]", "Vertical strips [0101]","Horizontal strips [1010]","Horizontal strips [0101]","Chessboard [1010/0101]","Chessboard [0101/1010]","Thick vertical strips [1100]","Thick vertical strips [0011]","Thicker vertical strips [11110000]","Thicker vertical strips [00001111]","Thick horizontal strips [1100]","Thick horizontal strips [0011]","Chessboard [11001100/00110011]", "Chest","Dartboard","Random 1","Random 2","Random 3","Random 4"]
output_folder = r'C:\Users\marsieradzka\Desktop\ris\Python_RIS_Sensing\Skrypty_sensing\artykul\wykres\TXdookol_RXdookol\all in'
plot_multiple_patterns_from_csv(file_path, patterns,output_folder)
print(f"Image saved to {plot_multiple_patterns_from_csv}")
