from class_measures_result import Results
import numpy as np
import matplotlib.pyplot as plt
import os
results = Results()

powers   = []



for result in results.results:
    powers.append(result.powers)
#change axises
powers_np_array = np.array(powers)
data = powers_np_array.T 

# Uzyskaj nazwę folderu, w którym znajduje się skrypt
folder_name = os.path.dirname(os.path.abspath(__file__))
plots_folder = os.path.join(folder_name, 'power_in_position')

# Utwórz folder "plots", jeśli nie istnieje
os.makedirs(plots_folder, exist_ok=True)

# Rysowanie każdego wiersza na osobnym wykresie i zapisywanie do plików
for i in range(data.shape[0]):
    plt.figure()  # Utwórz nową figurę dla każdego wykresu
    plt.plot(data[i], label=f'Wiersz {i+1}')
    plt.title(f'Tx {int(results.results[0].Tx_Angle[i])}, Rx {int(results.results[0].Rx_Angle[i])}')
    plt.xlabel('N-ty_pattern')
    plt.ylabel('Moc [dBm]')
    plt.ylim(-85, -50)  # Ustawienie stałego zakresu osi Y
    plt.grid(True)  # Włączenie linii pomocniczych
    plt.legend()
    plt.show()
    # Zapisz wykres do pliku w folderze "plots"
    #plt.savefig(os.path.join(plots_folder, f'wykres_wiersz_{i+1}.png'))
    plt.close()  # Zamknij figurę, aby nie pokazywać podglądu