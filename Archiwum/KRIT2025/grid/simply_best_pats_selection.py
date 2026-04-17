from class_measures_result import Results
import numpy as np
import matplotlib.pyplot as plt
import os
import math

results = Results()

def dbm_to_mw(x):
    mW=10**(x/10)
    return mW
def mw_to_dbm(x):
    dbm=10*math.log10(x)
    return dbm

powers   = []



for result in results.results:
    if result.idx < 1000:
        pow = result.powers
        powers.append(pow)
print(powers)

max_values = np.max(powers, axis=0)
max_indices = np.argmax(powers, axis=0)
print(max_values)
print(max_indices)
print(len(set(max_indices)))