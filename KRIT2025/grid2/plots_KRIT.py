from class_measures_result import Results
from class_measures_ref import Results_Ref
import numpy as np
import matplotlib.pyplot as plt
import os
import math
results = Results()
results_ref = Results_Ref()

best_idx = [775, 517, 346, 882, 149, 610, 738, 583, 92, 6, 640, 566, 529, 783, 75, 730]

res_pows = []

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

FONTSIZE = 20
MARKERSIZE = 18
# Use Rx_Angle as the x-axis
x_axis = results.results[0].Rx_Angle

# Create a figure and axis
plt.figure(figsize=(20, 12))

# Plot ref_pows
plt.plot(x_axis, ref_pows, linestyle='None', markersize=MARKERSIZE, label='Bez RMA', color='blue', marker='o')

# Plot res_best_pows
plt.plot(x_axis, res_best_pows, linestyle='None', markersize=MARKERSIZE, label='Ograniczona książka', color='red', marker='X')

# Adding titles and labels
plt.xlabel('Kąt położenia nadajnika [stopnie]', fontsize=FONTSIZE)
plt.ylabel('Wartości mocy odebranej [dBm]', fontsize=FONTSIZE)

plt.xticks(fontsize=FONTSIZE)  # Ustawia rozmiar czcionki etykiet na osi X
plt.yticks(fontsize=FONTSIZE)  # Ustawia rozmiar czcionki etykiet na osi Y
plt.legend(fontsize=FONTSIZE)
plt.grid()

# Show the plot
#plt.show()

c_mes = []
c_ref = []

for p in res_best_pows:
    c_mes.append(p)

for p in ref_pows:
    c_ref.append(p)

c_mes = 20000000 * np.log2(1 + abs(-100 - np.mean(c_mes)))
c_ref =  20000000 * np.log2(1 + abs(-100 - np.mean(c_ref)))
print ("C_MES = ", c_mes/8/1024/1024)#MB/s
print ("C_REF = ", c_ref/8/1024/1024)