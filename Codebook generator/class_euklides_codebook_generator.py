import csv
import threading
import os

import numpy as np
from bitstring import BitArray
from class_codebook import Codebook, Pattern

def pattern_hamming_distance(a, b):
    c = a ^ b
    return c.count(1)

class Euklides_codebook():
    def __init__(self, Q, i):
        self.Q = Q #how much patterns to generate
        self.i_bound = i #how much iterations of alghoritm
        return

    def generate_random_bitarray(self, length=16):
        # Generowanie losowego bitu jako tablicy numpy
        random_bits = np.random.choice([0, 1], size=length)
        # Tworzenie BitArray z losowych bitów
        return BitArray(bin=''.join(map(str, random_bits)))

    def calculate_metric(self, patterns, i, pat=None):
        ret_val = 0
        if pat==None:
            for j, pattern in enumerate(patterns):
                if j==i:
                    continue
                else:
                    ret_val += (pattern_hamming_distance(pattern, patterns[i]))**2
        else:
            for j,pattern in enumerate(patterns):
                if j==i:
                    continue
                else:
                    ret_val += (pattern_hamming_distance(pat, patterns[j]))**2
        return ret_val


    def generate_codebook(self):
        codebook = Codebook(do_load=False)
        patterns = []
        metrics = []
        
        #inicjalizacja algorytmu
        for i in range(self.Q):
            patterns.append(self.generate_random_bitarray(16))

        for i,pattern in enumerate(patterns):
            metrics.append(self.calculate_metric(patterns, i))
        
        #pętla algorytmu
        i = 0
        k = 0
        while i < self.i_bound:
            print("i,k", i, k)
            min_index = metrics.index(min(metrics))
            new_pattern = self.generate_random_bitarray(16)
            new_metric = self.calculate_metric(patterns, min_index, pat=new_pattern)
            if new_metric>metrics[min_index]:
                patterns[min_index] = new_pattern
                metrics[min_index]  = new_metric
                i = i + 1
                k = 0
            k+=1
            if k>10000:
                break
        
        for i,pattern in enumerate(patterns):
            codebook.add_pattern(pattern=Pattern(idx=i, pattern=(pattern*16).hex))

        return codebook

if __name__=="__main__":
    euklides_codebook = Euklides_codebook(100, 1000)
    e_codebook = euklides_codebook.generate_codebook()
    print(e_codebook)
    dumpname = "codebooks\euklides_codebook.pkl"
    e_codebook.dump_class_to_file(dumpfile=dumpname)
    pass
    
    test_load = Codebook(dumpfile=dumpname, filename=None, do_load=True)
    pass
    pass

