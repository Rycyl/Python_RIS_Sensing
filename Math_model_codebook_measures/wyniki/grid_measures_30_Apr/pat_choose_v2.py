from class_codebook import *
from class_measures_result import *
from class_select import *
import numpy as np

dumpfile= "wybrane_paterny_pk_metod_v2.pkl"
# try:
selected = Selected()
#selected = load_results_from_file(selected)
selected.load_from_file(dumpfile=dumpfile)
# for k in selected.selected:
#         k.find_max()
#         print("\n\n\n")
# selected.dump_class_to_file(dumpfile=dumpfile)
merge = []
for s in selected.selected:
    merge.append(s.maxs)
print(merge)
max_values = np.max(merge, axis=0)
max_indices = np.argmax(merge, axis=0)
print(max_values)


# # except:
# results = Results()
# codebook = Codebook()

# print("data loaded")
# currtent_pattern = None


# selected = Selected()
# i = -49
# for d in range(0, 90):
#     used_patterns = [0] * 919
#     print("D=", d)
#     selected.selected.append(Select(i,d))
#     for x in codebook.patterns:
#         if used_patterns[x.idx] != 1:
#             for a in x.angles:
#                 if used_patterns[x.idx] == 1:
#                     break
#                 if (a[0] == i and a[1] == d):
#                     selected.selected[-1].add_pat_idx(a[2], x.idx,  results.results[x.idx].powers)
#                     used_patterns[x.idx] = 1
#         else:
#             continue
# for x in selected.selected:
#     x.find_max()
                    
# selected.dump_class_to_file(dumpfile=dumpfile)
import matplotlib.pyplot as plt
FONTSIZE = 20
MARKERSIZE = 18

# Use Rx_Angle as the x-axis
results= Results()
x_axis = results.results[0].Rx_Angle
# Create a figure and axis
plt.figure(figsize=(10, 8))

# Plot ref_pows
plt.plot(x_axis, max_values,  markersize=MARKERSIZE, label='max in selected', color='blue', marker='X')

# Plot res_best_pows
plt.xlabel('Kąt położenia odbiornika [stopnie]', fontsize=FONTSIZE)
plt.ylabel('Wartości mocy odebranej [dBm]', fontsize=FONTSIZE)
plt.grid()
plt.legend(fontsize=FONTSIZE, loc='upper right')

plt.show()