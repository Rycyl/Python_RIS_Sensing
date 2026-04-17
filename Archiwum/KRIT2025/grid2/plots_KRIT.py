from class_measures_result import Results
from class_measures_ref import Results_Ref
import numpy as np
import matplotlib.pyplot as plt
import os
import math
from statistics import mean
results = Results()
results_ref = Results_Ref()

best_idx = [775, 517, 346, 882, 149, 610, 738, 583, 92, 6, 640, 566, 529, 783, 75, 730]

res_pows = []
kol_kol_bests = results.maxs[-2].powers

for x in results.results:
    res_pows.append(x.powers)
res_pows_array = np.array(res_pows)
res_pows = res_pows_array[best_idx]

ref_pows = results_ref.results[0].powers
print("RES")
print("RX_angle")
print(results.results[0].Rx_Angle)
print("X")
print(results.results[0].x_values)
print("Y")
print(results.results[0].y_values)
print("REFS")
print("RX_angle")
print(results_ref.results[0].Rx_Angle)
print("X")
print(results_ref.results[0].x_values)
print("Y")
print(results_ref.results[0].y_values)
res_best_pows = np.max(res_pows, axis=0)
max_indices = np.argmax(res_pows, axis=0)
print(res_best_pows)
# print(max_indices)
print(ref_pows)
pass
pass

FONTSIZE = 30
MARKERSIZE = 18
# Use Rx_Angle as the x-axis
x_axis = results.results[0].Rx_Angle

# Create a figure and axis
plt.figure(figsize=(10, 8))

# Plot ref_pows
plt.plot(x_axis, ref_pows,  markersize=MARKERSIZE, label='Bez RIS', color='blue', marker='X')

# Plot res_best_pows
plt.plot(x_axis, res_best_pows,  markersize=MARKERSIZE, label='Ograniczona książka', color='red', marker='X')

plt.plot(x_axis, kol_kol_bests,  markersize=MARKERSIZE, label='Opt. kolumnami', color='green', marker='X')
# Adding titles and labels
plt.xlabel('Kąt położenia odbiornika [stopnie]', fontsize=FONTSIZE)
plt.ylabel('Wartości mocy odebranej [dBm]', fontsize=FONTSIZE)

plt.xticks(fontsize=FONTSIZE)  # Ustawia rozmiar czcionki etykiet na osi X
plt.yticks(fontsize=FONTSIZE)  # Ustawia rozmiar czcionki etykiet na osi Y
plt.legend(fontsize=FONTSIZE, loc='upper right')

# Set manual y-axis limits
plt.ylim(-50.5, -30)  # Set y-axis from 0 to 12

plt.grid()

# Show the plot
# plt.show()

c_mes = []
c_ref = []
c_kol = []

def przeplywnosc(x, W = 80E6, noise = -50): # x = rec pwr
    if noise > x:
        return 0.0
    return W * np.log2(1 + (x - noise))/8/1024/1024 # in MB/s

for p in kol_kol_bests:
    c_kol.append(przeplywnosc(p))

for p in res_best_pows:
    c_mes.append(przeplywnosc(p))

for p in ref_pows:
    c_ref.append(przeplywnosc(p))


FONTSIZE = 28
MARKERSIZE = 18
# Use Rx_Angle as the x-axis
x_axis = results.results[0].Rx_Angle

# Create a figure and axis
plt.figure(figsize=(12, 8))

# Plot ref_pows
plt.plot(x_axis, c_ref,  markersize=MARKERSIZE, label='Bez RIS', color='blue', marker='X')

# Plot res_best_pows
plt.plot(x_axis, c_mes,  markersize=MARKERSIZE, label='Ograniczona książka', color='red', marker='X')

plt.plot(x_axis, c_kol,  markersize=MARKERSIZE, label='Opt. kolumnami', color='green', marker='X')
# Adding titles and labels
plt.xlabel('Kąt położenia odbiornika [stopnie]', fontsize=FONTSIZE)
plt.ylabel('Przepływność kanału [MB/s]', fontsize=FONTSIZE)

plt.xticks(fontsize=FONTSIZE)  # Ustawia rozmiar czcionki etykiet na osi X
plt.yticks(fontsize=FONTSIZE)  # Ustawia rozmiar czcionki etykiet na osi Y
plt.legend(fontsize=FONTSIZE, loc='lower center', bbox_to_anchor=(0.5, 1.02), ncol=3)
plt.ylim(0, 40)

plt.grid()
plt.savefig('przeplywnosc.png', dpi=300, bbox_inches='tight')
# Show the plot
plt.show()



# print("KAT, P_REF, P_KOL, P_MES, CREF, C MES & C_kol \\\\")
# for i in range(len(c_mes)):
#     print(
#         round(results.results[0].Rx_Angle[i], 1),
#         "&", round(res_best_pows[i], 1),
#         "&", round(kol_kol_bests[i], 1),
#         "&", round(ref_pows[i], 1),
#         "&", round(c_mes[i],1), 
#         "&", round(c_kol[i], 1),
#         "&", round(c_ref[i], 1),
        
#         "\\\\")
# print(
#     "ŚREDNIA &",
#     round(mean(res_best_pows), 1), "&",
#     round(mean(kol_kol_bests), 1), "&",
#     round(mean(ref_pows), 1), "&",
#     round(mean(c_mes), 1), "&",
#     round(mean(c_kol), 1), "&",
#     round(mean(c_ref), 1), 
#     "\\\\"
# )


# print ("P_MES= ", np.max(res_best_pows))
# print ("C_MES = ", np.max(c_mes))#MB/s
# print ("P_REF= ", np.max(ref_pows))
# print ("C_REF = ", np.max(c_ref))