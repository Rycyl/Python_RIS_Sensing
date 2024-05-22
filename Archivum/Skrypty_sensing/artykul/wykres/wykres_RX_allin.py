import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io


def plot_bar_chart_from_csv(file_path, patterns, output_path):

    df = pd.read_csv(file_path, sep=';', names=['Configuration', 'Frequency', 'Power','id'])

    df['Config_with_Power'] = " (" + df['Power'].round(2).astype(str) + " dBm)     " + df['Configuration']

    
    df['Frequency'] = df['Frequency'] / 1e9
    power_min = df['Power'].min() // 2 * 2  
    power_max = df['Power'].max() // 2 * 2 + 2  

    df_sorted = df.sort_values(by='Power', ascending=False)

    plt.figure(figsize=(14, 10))
    bars = plt.bar(df_sorted['Config_with_Power'], df_sorted['Power'], color='dodgerblue')
    
    
    plt.xlabel('Config_with_Power')
    plt.ylabel('Power (dBm)')
    plt.ylim([-62, df_sorted['Power'].max() + 1])
    #plt.gca().invert_yaxis()
    plt.title('Power Level by Configuration')

    plt.yticks([y * 2 for y in range(int(power_min / 2), int(power_max / 2 + 1))])  
    
    plt.grid(True)

    
    plt.xticks(rotation=90)
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='jpeg', bbox_inches='tight')
    buf.seek(0)
        
    image = Image.open(buf)
    image.save(f"{output_folder}/4_TXdookolna_RXdookol_184_allin_bar.jpg")
    plt.close()
        

file_path = open(r'C:\Users\marsieradzka\Desktop\ris\Python_RIS_Sensing\Skrypty_sensing\artykul\wyniki\TXdookol_RXdookol\4_dookolna_184.csv')
patterns = ["All elements turn on","Only first element turn on","Only last element turn on","Left side on","Right side on","Upper half on","Lower half on","Vertical strips [1010]", "Vertical strips [0101]","Horizontal strips [1010]","Horizontal strips [0101]","Chessboard [1010/0101]","Chessboard [0101/1010]","Thick vertical strips [1100]","Thick vertical strips [0011]","Thicker vertical strips [11110000]","Thicker vertical strips [00001111]","Thick horizontal strips [1100]","Thick horizontal strips [0011]","Chessboard [11001100/00110011]", "Chest","Dartboard","Random 1","Random 2","Random 3","Random 4"]
output_folder = r'C:\Users\marsieradzka\Desktop\ris\Python_RIS_Sensing\Skrypty_sensing\artykul\wykres\TXdookol_RXdookol\all_in_bar'
plot_bar_chart_from_csv(file_path, patterns,output_folder)
print(f"Image saved to {plot_bar_chart_from_csv}")
