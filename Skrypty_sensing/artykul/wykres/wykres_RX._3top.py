import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import io
import numpy as np


def plot_multiple_patterns_from_csv(file_path, patterns,output_folder):
    df = pd.read_csv(file_path, sep=';', names=['Configuration', 'Frequency', 'Power'])

    df['Frequency'] = df['Frequency'] / 1e9
    df = df[(df['Frequency'] >= 5.0) & (df['Frequency'] <= 5.9)]
    
    top3_global = df.sort_values(by='Power', ascending=False).head(3)
    print(f"Our 3 top of the top are:")
    print(top3_global[['Configuration', 'Power', 'Frequency']])
    #df = df.sort_values(by='Frequency')
    
    plt.figure(figsize=(12, 8))
    colors = plt.cm.viridis(np.linspace(0, 1, 3))

    
    for idx, (index, row) in enumerate(top3_global.iterrows()):
        plt.scatter(row['Power'], row['Frequency'], color=colors[idx], s=100, 
                label=f"{row['Configuration']} ({row['Power']} dBm, {row['Frequency']} GHz)")

    plt.xlabel('Power (dBm)')
    plt.ylabel('Frequency (GHz)')
    plt.title('Top 3 Power Readings Across All Configurations (5.0-5.9 GHz)')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format='jpeg', bbox_inches='tight')
    buf.seek(0)
        
    image = Image.open(buf)
    image.save(f"{output_folder}/TX_RX_dookolna_184_thebest.jpg")
    plt.close()
        

file_path = open(r'C:\Users\marsieradzka\Desktop\ris\Python_RIS_Sensing\Skrypty_sensing\artykul\wyniki\TXdookol_RXdookol\dookolne_184.csv')
patterns = ["All elements turn on","Only first element turn on","Only last element turn on","Left side on","Right side on","Upper half on","Lower half on","Vertical strips [1010]", "Vertical strips [0101]","Horizontal strips [1010]","Horizontal strips [0101]","Chessboard [1010/0101]","Chessboard [0101/1010]","Thick vertical strips [1100]","Thick vertical strips [0011]","Thicker vertical strips [11110000]","Thicker vertical strips [00001111]","Thick horizontal strips [1100]","Thick horizontal strips [0011]","Chessboard [11001100/00110011]", "Chest","Dartboard","Random 1","Random 2","Random 3","Random 4"]
output_folder = r'C:\Users\marsieradzka\Desktop\ris\Python_RIS_Sensing\Skrypty_sensing\artykul\wykres\TXdookol_RXdookol'
plot_multiple_patterns_from_csv(file_path, patterns,output_folder)
print(f"Image saved to {plot_multiple_patterns_from_csv}")
