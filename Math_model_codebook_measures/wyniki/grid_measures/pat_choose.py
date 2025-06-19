from class_codebook import *
from class_measures_result import *
from class_select import *
import numpy as np



dumpfile= "wybrane_paterny_pk_metod.pkl"
# try:
selected = Selected()
selected.load_from_file(dumpfile=dumpfile)
pass
for k in selected.selected:
    k.find_max()
    print("\n\n\n")
# except:
#     results = Results()
#     codebook = Codebook()

#     print("data loaded")
#     currtent_pattern = None
#     used_patterns = [0] * 919

#     selected = Selected()
#     i = -49
#     for d in range(0, 91):
#         print("D=", d)
#         selected.selected.append(Select(i,d))
#         for x in codebook.patterns:
#             if used_patterns[x.idx] != 1:
#                 for a in x.angles:
#                     if used_patterns[x.idx] == 1:
#                         break
#                     if (a[0] == i and a[1] == d):
#                         selected.selected[-1].add_pat_idx(a[2], x.idx,  results.results[x.idx].powers)
#                         used_patterns[x.idx] = 1
#             else:
#                 continue
                        
#     selected.dump_class_to_file(dumpfile=dumpfile)