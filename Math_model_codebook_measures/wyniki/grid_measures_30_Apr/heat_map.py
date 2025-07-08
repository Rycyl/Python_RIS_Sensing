import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import inspect
import os

def plot_heat_map(heatmap_data,
                title="",
                SCALE_LABEL='',
                V_MIN=2,
                V_MAX=12,
                SAVE = False,
                SAVE_NAME = 'figure',
                SAVE_FORMAT = 'png',
                FONTSIZE=20):

    # Plotting
    plt.figure(figsize=(10, 6))
    ax = sns.heatmap(
        np.flip(heatmap_data.T, axis=1),
        annot=True, cmap='viridis',
        cbar_kws={'label': SCALE_LABEL},
        annot_kws={"size": 14, "weight": "bold",},
        vmax=V_MAX, # Maximum value for the color scale
        vmin=V_MIN  # Minimum value for the color scale
        ) 
    colorbar = ax.collections[0].colorbar
    colorbar.ax.tick_params(labelsize=FONTSIZE)
    colorbar.ax.yaxis.label.set_size(FONTSIZE)
    #colorbar.ax.yaxis.label.set_weight("bold")
    colorbar.ax.tick_params(labelsize=FONTSIZE, width=1.5)
    for tick in colorbar.ax.get_yticklabels():
        tick.set_weight("bold")
    x_labels = np.arange(2.64, -0.66, -0.66)
    x_labels = [abs(round(x, 2)) for x in x_labels]
    plt.xticks(ticks=np.arange(0.5, 5.5, step=1), labels=x_labels, fontsize = FONTSIZE)
    plt.yticks(ticks=np.arange(0.5, 3, step=1), labels=np.arange(1.5, 3, 0.5), fontsize = FONTSIZE)
    if title!="":
        plt.title(title, fontsize=FONTSIZE, fontweight='bold') #f"Heatmap for Pattern: {pattern_title}"
    plt.xlabel("Odległość Rx od Osi Y RIS'a [m]", fontsize=FONTSIZE)
    plt.ylabel("Odległość Rx od Osi X RIS'a [m]", fontsize=FONTSIZE)
    plt.gca().invert_yaxis()  # Optional: match matrix orientation
    plt.tight_layout()
    if SAVE:
        folder_name = os.path.dirname(os.path.abspath(__file__))
        plots_folder = os.path.join(folder_name, inspect.currentframe().f_code.co_name)
        # Utwórz folder "plots", jeśli nie istnieje
        os.makedirs(plots_folder, exist_ok=True)
        plt.savefig(os.path.join(plots_folder, f"{SAVE_NAME}.{SAVE_FORMAT}"), format=SAVE_FORMAT)
        print("PLOT SAVED:", f"{SAVE_NAME}.{SAVE_FORMAT}")
    else:
        plt.show()
    plt.close()
    return

def input_dat(data, x_y):
    #x_y = [(4,2), (3,2), (2,2), (1,2), (0,2), (0,1), (1,1), (2,1), (3,1), (4,1), (4,0), (3,0), (2,0), (1,0), (0,0)]
    
    heatmap_data = np.full((5, 3), np.nan)
    for i in range(len(x_y)):
        x, y = x_y[i]
        heatmap_data[x][y] = data[i]
    return heatmap_data

if __name__ == "__main__":
    Codebook_POWS = [-37.6423952, -39.25942525, -41.56216294, -47.31328839, -37.67257822, 
         -40.9102518, -40.84429866, -38.48896182, -42.23777336, -41.06956309, 
         -41.68972993, -46.0392988, -48.06770182, -41.14027181, -44.47917482]
    
    REF_POWS = [-46.70075942, -44.99466065, -48.93914243, -50.23832524, -42.47576393, 
         -39.82441953, -44.45100205, -42.70086365, -48.27907339, -49.73079157, 
         -46.2658791, -47.62619389, -43.87240453, -45.06303278, -50.09625047]
    
    #SNR_Codebook_POWS = [P+100 for P in Codebook_POWS]
    x_y = [(0,0), (0,1), (0,2), (1,2), (1,1), (1,0), (2,2), (2,1), (3,2), (2,0), (3,1), (4,2), (4,1), (3,0), (4,0)]
    heat_map_data = input_dat(Codebook_POWS, x_y)
    #plot_heat_map(heat_map_data, "Codebook", True)

    ref_x_y = [(0,0), (0,2), (0,1), (1,2), (1,1), (1,0), (2,2), (2,1), (3,2), (2,0), (4,2), (3,1), (4,0), (3,0), (4,1)]
    heat_map_data_ref = input_dat(REF_POWS, x_y)
    #plot_heat_map(heat_map_data_ref, "No RIS", True)

    normalized_heat_map =np.full((5,3), np.nan)
    for i in range(5):
        for j in range(3):
            normalized_heat_map[i][j] = -heat_map_data_ref[i][j] + heat_map_data[i][j]
    
    plot_heat_map(normalized_heat_map, r"Moc odebrana w punktach $R_{i=(x,y)}$")
