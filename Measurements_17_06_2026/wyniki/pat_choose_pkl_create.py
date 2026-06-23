from class_codebook import *
from class_measures_result import *
from class_select import *
import numpy as np



dumpfile= "wybrane_paterny_pk_metod.pkl"

selected = Selected()
selected.load_from_file(dumpfile=dumpfile)
pass
for k in selected.selected:
    k.find_max()
    print("\n\n\n")