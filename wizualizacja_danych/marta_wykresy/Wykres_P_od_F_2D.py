import pandas as pd
import matplotlib.pyplot as plt

def plot_multiple_patterns_from_csv(file_path, patterns):
    df = pd.read_csv(file_path, sep=';', names=['Configuration', 'Frequency', 'Power'])

    # Convert Frequency from Hz to GHz for easier handling and filter the data
    df['Frequency'] = df['Frequency'] / 1e9
    df = df[(df['Frequency'] >= 5.0) & (df['Frequency'] <= 5.9)]
    
    # Ensure the DataFrame is sorted by 'Frequency' to connect points in ascending frequency order
    df = df.sort_values(by='Frequency')
    
    power_min = df['Power'].min() // 2 * 2  
    power_max = df['Power'].max() // 2 * 2 + 2  

    plt.figure(figsize=(12, 8))
    
    colors = plt.cm.tab20.colors
    
    for index, pattern in enumerate(patterns):
        specific_pattern_df = df[df['Configuration'] == pattern]

        if specific_pattern_df.empty:
            print(f"No entries found for pattern '{pattern}'.")
            continue

        color = colors[index % len(colors)]
        plt.plot(specific_pattern_df['Frequency'], specific_pattern_df['Power'], marker='o', linestyle='-', label=pattern, color=color)

    plt.xlabel('Frequency (GHz)')
    plt.ylabel('Power (dBm)')
    plt.title('Frequency vs. Power for Multiple Configurations')
    plt.xlim(5.0, 5.9)
    plt.ylim(power_min, power_max)
    plt.xticks([x * 0.1 for x in range(50, 60)], rotation=45)  
    plt.yticks([y * 2 for y in range(int(power_min / 2), int(power_max / 2 + 1))])  
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 5}, ncol=1, handletextpad=2, labelspacing=1.5, borderpad=1, frameon=True)
    plt.grid(True)
    plt.show()

# Adjusted for demonstration; replace with your actual file path and patterns
file_path = open(r'C:\Users\marsieradzka\Desktop\ris\Python_RIS\wyniki\18_03_24_03\19_03_reflection_20cm_3_5cm_17cm.csv')
patterns = ["Right side on","Upper half on","Lower half on","Vertical strips [1010]", "Vertical strips [0101]","Horizontal strips [1010]"]#,"Horizontal strips [0101]","Chessboard [1010/0101]","Chessboard [0101/1010]","Thick vertical strips [1100]","Thick vertical strips [0011]","Thicker vertical strips [11110000]","Thicker vertical strips [00001111]","Thick horizontal strips [1100]","Thick horizontal strips [0011]","Chessboard [11001100/00110011]", "Chest","Dartboard","Random 1","Random 2","Random 3","Random 4"]
plot_multiple_patterns_from_csv(file_path, patterns)#"All elements turn on","Only first element turn on","Only last element turn on","Left side on",