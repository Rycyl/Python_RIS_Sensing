import csv
import threading
import os
import random

import numpy as np
from bitstring import BitArray

from class_codebook import Codebook, Pattern


def pattern_hamming_distance(a, b):
    c = a ^ b
    return c.count(1)

def get_patterns_from_codebook(codebook):
    patterns_from_codebook = []
    for pat in codebook.patterns:
        patterns_from_codebook.append(pat.pattern)
    return patterns_from_codebook

class Euklides_codebook():
    def __init__(self, Q, i):
        self.Q = Q #how much patterns to generate
        self.i_bound = i #how much iterations of alghoritm
        return

    def generate_random_bitarray(self, length=16):
        # gen random numpy bits of len=lenght
        random_bits = np.random.choice([0, 1], size=length)
        # make bitarray from random_bits
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


    def generate_codebook(self, Q=None, i_bound=None, k_bound=None):
        """
            Generates a codebook based on a previously generated codebook 
                using the Euclidean (Hamming) method.
            Q: the number of RIS elements (default = 16 [columns])
            i_bound: the number of iterations for the algorithm
            k_bound: the limit on searching for a new better candidate;
                    if exceeded - break
            Returns a Codebook() object
        """
        if Q != None:
            self.Q = Q
        if i_bound != None:
            self.i_bound = i_bound
        if k_bound == None:
            k_bound = 2147483646 #int32 size -1

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
            if k>k_bound:
                break

        #put patterns into codebook object
        codebook = Codebook(do_load=False)
        for i,pattern in enumerate(patterns):
            codebook.add_pattern(pattern=Pattern(idx=i, pattern=(pattern*16).hex))

        return codebook


    def generate_codebook_from_codebook(self, bigger_codebook, Q=None, i_bound=None, k_bound=None):
        """
            Generates a codebook based on a previously generated codebook 
                using the Euclidean (Hamming) method.
            bigger_codebook: previously generated codebook
            Q: the number of RIS elements (default = 16 [columns])
            i_bound: the number of iterations for the algorithm
            k_bound: the limit on searching for a new better candidate;
                    if exceeded - break
            Returns a Codebook() object
        """
        patterns_from_codebook = get_patterns_from_codebook(bigger_codebook)

        patterns = []
        metrics = []
        
        if Q != None:
            self.Q = Q
        if i_bound != None:
            self.i_bound = i_bound
        if k_bound == None:
            k_bound = (len(patterns_from_codebook)-Q) * 50 #50 times a number of posibilites

        #select Q random patterns from given codebook
        for i in range(self.Q): 
            pat = random.choice(patterns_from_codebook)
            patterns.append(pat)


        #count metrics
        for i,pattern in enumerate(patterns):
            metrics.append(self.calculate_metric(patterns, i))
        
        #main loop
        i = 0
        k = 0
        while i < self.i_bound:
            
            min_index = metrics.index(min(metrics))
            #select non selected patter from codebook
            not_done = True
            while not_done:
                new_pattern = random.choice(patterns_from_codebook)
                if new_pattern in patterns:
                    new_pattern = random.choice(patterns_from_codebook)
                else:
                    not_done = False

            new_metric = self.calculate_metric(patterns, min_index, pat=new_pattern)
            if new_metric>metrics[min_index]:
                patterns[min_index] = new_pattern
                metrics[min_index]  = new_metric
                i = i + 1
                print("i: ", i)
                k = 0
            k+=1
            if k>k_bound:
                print("k bound reached, breaking loop, returning codebook for")
                print("Q = ", self.Q, "; i_bound = ", self.i_bound, "; k_bound = ", k_bound, "; i = ", i, "; k = ", k)
                break
        
        codebook = Codebook(do_load=False)
        for i,pattern in enumerate(patterns):
            codebook.add_pattern(pattern=Pattern(idx=i, pattern=pattern.hex))

        return codebook

if __name__=="__main__":
    euklides_codebook = Euklides_codebook(64, 640)
    try:
        e_codebook_64 = Codebook(dumpfile="codebooks/euklides_codebook64.pkl")
        e_codebook_16 = Codebook(dumpfile="codebooks/euklides_codebook16.pkl")
        e_codebook_16_from_64 = Codebook(dumpfile="codebooks/euklides_codebook16_from_64.pkl")
    except:
        e_codebook_64 = euklides_codebook.generate_codebook(Q=64)
        e_codebook_64.dump_class_to_file(dumpfile="codebooks/euklides_codebook64.pkl")
        e_codebook_16 = euklides_codebook.generate_codebook(Q=16, i_bound=2048, k_bound=100000)
        e_codebook_16.dump_class_to_file(dumpfile="codebooks/euklides_codebook16.pkl")
        e_codebook_16_from = euklides_codebook.generate_codebook_from_codebook(e_codebook_64, Q=16, i_bound=512, k_bound=8096)
        e_codebook_16_from.dump_class_to_file(dumpfile="codebooks/euklides_codebook16_from_64.pkl")
        print("codebooks dumpted")
   
    from codebook_analyze import *

    reduced_by_hamming_codebooks = []
    # reduced_by_hamming_codebooks.append((reduce_by_hamming(e_codebook_64), "Euclidean codebook, s=64"))
    reduced_by_hamming_codebooks.append((reduce_codebook_by_hamming(e_codebook_16_from_64), "Euclidean codebook from s=64, s=16"))
    reduced_by_hamming_codebooks.append((reduce_codebook_by_hamming(e_codebook_16), "Euclidean codebook, s=16"))
    plot_codebooks_reduce_by_hamming(reduced_by_hamming_codebooks)
    codebooks_AFs = []
    for x in [e_codebook_16_from_64, e_codebook_16]:
        AFs = []
        for i,pattern in enumerate(x.patterns):
            print(i+1, "/", len(x.patterns)) 
            AFs.append(AF_from_pattern(pattern.pattern, -48))
        codebooks_AFs.append(AFs)
    plot_codebooks_AFs(codebooks_AFs, ["Euclidean codebook from s=64, s=16", "Euclidean codebook, s=16"])


    pass