import csv
import threading
import os
import random

import numpy as np
from bitstring import BitArray

from class_codebook import Codebook, Pattern


def pattern_hamming_distance(a, b):
    """
    Calculate Hamming distance beetween two patterns
    Input:
    a: BitArray() pattern1
    b: BitArray() pattern2
    Returns:
    int() of value of Hamming distance
    """
    c = a ^ b
    return c.count(1)

def get_patterns_from_codebook(codebook):
    """
    Extracts patterns from codebook
    IN:
    codebook: Codebook() obj
    RET:
    list of patterns [BitArray(), BitArray(), ...]
    """
    patterns_from_codebook = []
    for pat in codebook.patterns:
        patterns_from_codebook.append(pat.pattern)
    return patterns_from_codebook

def calculate_metric(patterns, i, pat=None):
    """
    calculate hamming distance metric (from idx=i) of given set of patterns
    Inptuts:
        patterns: set of patterns (BitArray format)
        i: idx of pattern which metric is calculated
        pat: (def None): new pattern, to calculate it's metric,
                            i'th pattern is ommited while calculating
    """
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

class Euklides_codebook():
    def __init__(self, Q, i):
        """
        IN:
        Q: how much patterns to generate
        i: how much iterations of alghoritm
        """
        self.Q = Q #how much patterns to generate
        self.i_bound = i #how much iterations of alghoritm
        return

    def generate_random_bitarray(self, length=16):
        # gen random numpy bits of len=lenght
        random_bits = np.random.choice([0, 1], size=length)
        # make bitarray from random_bits
        return BitArray(bin=''.join(map(str, random_bits)))

    def calculate_metric(self, patterns, i, pat=None):
        """
        calculate hamming distance metric of given set of patterns
        Inptuts:
            patterns: set of patterns (BitArray format)
            i: idx of pattern which metric is calculated
            pat: (def None): new pattern, to calculate it's metric,
                             i'th pattern is ommited while calculating
        """
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
            Q: the number of RIS patterns (default = 16)
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
            while True:
                pattern = self.generate_random_bitarray(16)
                if pattern not in patterns:
                    break
            patterns.append(pattern)

        for i,pattern in enumerate(patterns):
            metrics.append(self.calculate_metric(patterns, i))
        
        #pętla algorytmu
        i = 0
        k = 0
        while i < self.i_bound:
            #print("i,k", i, k)
            min_index = metrics.index(min(metrics))
            while True:
                new_pattern = self.generate_random_bitarray(16)
                if new_pattern not in patterns:
                    break
            new_metric = self.calculate_metric(patterns, min_index, pat=new_pattern)
            if new_metric>metrics[min_index]:
                patterns[min_index] = new_pattern
                metrics[min_index]  = new_metric
                print(f"{i}/{self.i_bound}")
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
            bigger_codebook: previously generated Codebook() obj
            Q: the number of RIS elements (default = 16 [columns])
            i_bound: the number of iterations for the algorithm
            k_bound: OLD FEATURE - does nothing - now break is specifed as searching throught all 
                     patterns without finding better metric
            Returns a Codebook() object
        """
        patterns_from_codebook = get_patterns_from_codebook(bigger_codebook)

        patterns = []
        metrics = []
        
        if Q != None:
            self.Q = Q
        if i_bound != None:
            self.i_bound = i_bound

        #select Q random patterns from given codebook
        for i in range(self.Q):
            while True: 
                pattern = random.choice(patterns_from_codebook)
                if pattern not in patterns:
                    break
            patterns.append(pattern)
        
        #count metrics
        for i,pattern in enumerate(patterns):
            metrics.append(self.calculate_metric(patterns, i))
        
        #main loop
        # main loop
        i = 0
        k = 0
        codebook_len = len(patterns_from_codebook)

        while i < self.i_bound:
            print("i:", i)
            min_index = metrics.index(min(metrics))

            # cyclic select patterns - specified end of the loop
            new_pattern = patterns_from_codebook[i % codebook_len]

            # do not use patterns from codebook -- check
            if new_pattern in patterns:
                k += 1
            else:
                new_metric = self.calculate_metric(patterns, min_index, pat=new_pattern)
                if new_metric > metrics[min_index]:
                    patterns[min_index] = new_pattern
                    metrics[min_index] = new_metric
                    k = 0
                else:
                    k += 1

            if k > codebook_len:
                print("k bound reached, breaking loop, returning codebook")
                print(
                    "Q = ", self.Q,
                    "; i_bound = ", self.i_bound,
                    "; k_bound = ", codebook_len,
                    "; i = ", i,
                    "; k = ", k
                )
                break
            
            i += 1 # <-- loop iteration
            #END WHILE (main loop)

        codebook = Codebook(do_load=False)
        for i,pattern in enumerate(patterns):
            codebook.add_pattern(pattern=Pattern(idx=i, pattern=pattern.hex))

        return codebook

def generate_euclidean_codebooks_of_size(
    codebooks_sizes, n_repeats,
    i_bound=2048, k_bound=1000000):
    """
    Generates a codebook based on a previously generated codebook 
        using the Euclidean (Hamming) method.
    IN:
    codebooks_sizes: sizes of codebooks to generate
    n_repeats: number of codebooks to generate of each size
    i_bound: the number of iterations for the algorithm
    k_bound: the limit on searching for a new better candidate;
            if exceeded - break
    Returns:
    a list of Codebook() objs [book1, book2 ....]
    """
    e_c = Euklides_codebook(64, 640)
    e_codebooks = []

    for size in codebooks_sizes:
        for n in range(n_repeats):
            dumpfile = f"codebooks/euklides_codebook_{size}_{n}.pkl"
            try:
                print(f"Loading codebook size={size}, n={n}")
                e_codebooks.append(Codebook(dumpfile=dumpfile))
            except:
                print(f"Loading failed, generating codebook size={size}, n={n}")
                cb = e_c.generate_codebook(
                    Q=size, i_bound=i_bound, k_bound=k_bound
                )
                cb.dump_class_to_file(dumpfile=dumpfile)
                e_codebooks.append(cb)
                print(f"Codebook size={size}, n={n} dumped")

    print("Codebooks done")
    return e_codebooks

def generate_euclidean_codebooks_of_size_from_codebook(
    bigger_codebook, codebooks_sizes, n_repeats=1, i_bound=10000, k_bound=1000000):
    """
    Generates a codebook based on a previously generated codebook 
        using the Euclidean (Hamming) method.
    IN:
    bigger_codebook: previously generated Codebook() obj
    codebooks_sizes: sizes of codebooks to generate
    n_repeats: number of codebooks to generate of each size
    i_bound: the number of iterations for the algorithm
    k_bound: the limit on searching for a new better candidate;
            if exceeded - break
    Returns:
    a list of Codebook() objs [book1, book2 ....]
    """
    e_c = Euklides_codebook(64, 640)
    e_codebooks = []
    bigger_codebook_size = len(bigger_codebook.patterns)

    for size in codebooks_sizes:
        if size >= bigger_codebook_size:
            print(f"size={size} >= {bigger_codebook_size}, skipping")
            continue

        for n in range(n_repeats):
            dumpfile = (
                f"codebooks/euklides_codebook_"
                f"{size}_from_{bigger_codebook_size}_{n}.pkl"
            )
            try:
                print(f"Loading codebook size={size} from {bigger_codebook_size}, n={n}")
                e_codebooks.append(Codebook(dumpfile=dumpfile))
            except:
                print(f"Generating codebook size={size} from {bigger_codebook_size}, n={n}")
                cb = e_c.generate_codebook_from_codebook(
                    bigger_codebook,
                    Q=size,
                    i_bound=i_bound,
                    k_bound=k_bound
                )
                cb.dump_class_to_file(dumpfile=dumpfile)
                e_codebooks.append(cb)
                print(f"Codebook size={size} from {bigger_codebook_size}, n={n} dumped")

    print("Codebooks from codebook done")
    return e_codebooks

def calculate_metric_for_codebook(codebook_patterns):
    """
    Calculates the aggregate metric for a single codebook based on its patterns.
    This function iterates through the given patterns of a codebook and 
    accumulates a metric value by invoking the `calculate_metric` function 
    for each pattern.
    Parameters:
    ----------
    codebook_patterns : list
        A list of patterns from codebook
    Returns:
    -------
    float
        The accumulated metric value for the provided codebook patterns.
    """
    metric = 0
    for i, pattern in enumerate(codebook_patterns):
        metric += calculate_metric(codebook_patterns, i)
    return metric

def calculate_metric_for_codebooks(codebooks):
    """
    Calculates metrics for multiple codebooks.

    This function processes a list of codebooks to extract their patterns and computes
    the corresponding metrics using the `calculate_metric_for_codebook` function for each codebook.

    So the result is a sum of all metrics of all patterns: 
    sum of squared Hamming distance from each to each pattern in codebook

    Parameters:
    ----------
    codebooks : list of Codebook() objects

    Returns:
    -------
    list of floats/int?
        A list of metric values calculated for each codebook.
    """
    metrics = []
    for codebook in codebooks:
        codebook_patterns = get_patterns_from_codebook(codebook)
        metric = calculate_metric_for_codebook(codebook_patterns=codebook_patterns)
        metrics.append(metric)
    return metrics

def calculate_metric_for_codebooks_div_by_len(codebooks):
    """
    Calculates metrics for multiple codebooks.

    This function processes a list of codebooks to extract their patterns and computes
    the corresponding metrics using the `calculate_metric_for_codebook` function for each codebook.

    The result is a
    M / len(codebook)-1

    Parameters:
    ----------
    codebooks : list of Codebook() objects

    Returns:
    -------
    list of floats/int?
        A list of metric values calculated for each codebook.
    """
    metrics = []
    for codebook in codebooks:
        codebook_patterns = get_patterns_from_codebook(codebook)
        metric = calculate_metric_for_codebook(codebook_patterns=codebook_patterns)
        metrics.append(metric)

    for i in range(len(codebooks)):
        codebook_patterns = get_patterns_from_codebook(codebooks[i])
        metrics[i] = metrics[i] / (len(codebook_patterns)-1)

    return metrics

def calculate_metric_for_codebooks_sqrt_div_by_len(codebooks):
    """
    Calculates metrics for multiple codebooks.

    This function processes a list of codebooks to extract their patterns and computes
    the corresponding metrics using the `calculate_metric_for_codebook` function for each codebook.

    The result is a
    sqrt(M) / len(codebook)-1

    Parameters:
    ----------
    codebooks : list of Codebook() objects

    Returns:
    -------
    list of floats/int?
        A list of metric values calculated for each codebook.
    """
    metrics = []
    for codebook in codebooks:
        codebook_patterns = get_patterns_from_codebook(codebook)
        metric = calculate_metric_for_codebook(codebook_patterns=codebook_patterns)
        metrics.append(metric)

    for i in range(len(codebooks)):
        codebook_patterns = get_patterns_from_codebook(codebooks[i])
        metrics[i] = np.sqrt(metrics[i]) / (len(codebook_patterns)-1)

    return metrics

def calculate_metric_for_codebooks_div_by_len_sqrt(codebooks):
    """
    Calculates metrics for multiple codebooks.

    This function processes a list of codebooks to extract their patterns and computes
    the corresponding metrics using the `calculate_metric_for_codebook` function for each codebook.

    The result is a
    sqrt(M / len(codebook)-1)

    Parameters:
    ----------
    codebooks : list of Codebook() objects

    Returns:
    -------
    list of floats/int?
        A list of metric values calculated for each codebook.
    """
    metrics = []
    for codebook in codebooks:
        codebook_patterns = get_patterns_from_codebook(codebook)
        metric = calculate_metric_for_codebook(codebook_patterns=codebook_patterns)
        metrics.append(metric)

    for i in range(len(codebooks)):
        codebook_patterns = get_patterns_from_codebook(codebooks[i])
        metrics[i] = np.sqrt(metrics[i] / (len(codebook_patterns)-1))

    return metrics

def calculate_metric_for_codebooks_sqrt_div_by_len_div_by_len(codebooks):
    """
    Calculates metrics for multiple codebooks.

    This function processes a list of codebooks to extract their patterns and computes
    the corresponding metrics using the `calculate_metric_for_codebook` function for each codebook.

    The result is a
    sqrt(M) / len(codebook)-1 / len(codebook)

    Parameters:
    ----------
    codebooks : list of Codebook() objects

    Returns:
    -------
    list of floats/int?
        A list of metric values calculated for each codebook.
    """
    metrics = []
    for codebook in codebooks:
        codebook_patterns = get_patterns_from_codebook(codebook)
        metric = calculate_metric_for_codebook(codebook_patterns=codebook_patterns)
        metrics.append(metric)

    for i in range(len(codebooks)):
        codebook_patterns = get_patterns_from_codebook(codebooks[i])
        metrics[i] = np.sqrt(metrics[i]) / (len(codebook_patterns)-1) / len(codebook_patterns)

    return metrics

def calculate_metric_for_codebooks_sqrt(codebooks):
    """
    Calculates metrics for multiple codebooks.

    This function processes a list of codebooks to extract their patterns and computes
    the corresponding metrics using the `calculate_metric_for_codebook` function for each codebook.

    The result is a
    sqrt(M) / len(codebook)-1 / len(codebook)

    Parameters:
    ----------
    codebooks : list of Codebook() objects

    Returns:
    -------
    list of floats/int?
        A list of metric values calculated for each codebook.
    """
    metrics = []
    for codebook in codebooks:
        codebook_patterns = get_patterns_from_codebook(codebook)
        metric = calculate_metric_for_codebook(codebook_patterns=codebook_patterns)
        metrics.append(metric)

    for i in range(len(codebooks)):
        codebook_patterns = get_patterns_from_codebook(codebooks[i])
        metrics[i] = np.sqrt(metrics[i])

    return metrics

def calculate_metric_for_codebooks_div_div(codebooks):
    """
    Calculates metrics for multiple codebooks.

    This function processes a list of codebooks to extract their patterns and computes
    the corresponding metrics using the `calculate_metric_for_codebook` function for each codebook.

    The result is a
    M / len(codebook)-1 / len(codebook)

    Parameters:
    ----------
    codebooks : list of Codebook() objects

    Returns:
    -------
    list of floats/int?
        A list of metric values calculated for each codebook.
    """
    metrics = []
    for codebook in codebooks:
        codebook_patterns = get_patterns_from_codebook(codebook)
        metric = calculate_metric_for_codebook(codebook_patterns=codebook_patterns)
        metrics.append(metric)

    for i in range(len(codebooks)):
        codebook_patterns = get_patterns_from_codebook(codebooks[i])
        metrics[i] = metrics[i] / len(codebook_patterns) / (len(codebook_patterns)-1)

    return metrics

if __name__=="__main__":
    sizes = range(2,17)
    # ec_obj = Euklides_codebook(1,1)
    # a = ec_obj.generate_codebook(64, 10000, 10000000)
    # a.dump_class_to_file(dumpfile="codebooks/euklides_codebook64.pkl")
    e_codebook_64 = Codebook(dumpfile="codebooks/euklides_codebook64.pkl")
    e_codebooks = generate_euclidean_codebooks_of_size(sizes)
    e_codebook_16 = Codebook(dumpfile="codebooks/euklides_codebook16.pkl")
    e_codebooks_from16 = generate_euclidean_codebooks_of_size_from_codebook(e_codebook_16, sizes)
    e_codebooks_from64 = generate_euclidean_codebooks_of_size_from_codebook(e_codebook_64, sizes)
    #exit()
    from codebook_analyze import *

    # M / Q-1 / Q
    # Calculate metrics for each set of codebooks
    metrics = calculate_metric_for_codebooks(e_codebooks)
    metrics_from16 = calculate_metric_for_codebooks(e_codebooks_from16)
    metrics_from64 = calculate_metric_for_codebooks(e_codebooks_from64)

    # Get lengths of the codebooks
    lengths = [len(codebook.patterns) for codebook in e_codebooks]
    lengths_from16 = [len(codebook.patterns) for codebook in e_codebooks_from16]
    lengths_from64 = [len(codebook.patterns) for codebook in e_codebooks_from64]

    # Prepare data for plotting
    all_metrics = [metrics, metrics_from16, metrics_from64]
    all_lengths = [lengths, lengths_from16, lengths_from64]
    labels = [
        'euclidean codebooks generated directly',
        'euclidean codebooks generated from codebook of size 16',
        'euclidean codebooks generated from codebook of size 64'
    ]
    plot_codebooks_metrics(all_metrics, all_lengths, labels, TITLE="M / (Q-1) / Q")

    # Calculate metrics for each set of codebooks
    metrics = calculate_metric_for_codebooks(e_codebooks)
    metrics_from16 = calculate_metric_for_codebooks(e_codebooks_from16)
    metrics_from64 = calculate_metric_for_codebooks(e_codebooks_from64)

    # Get lengths of the codebooks
    lengths = [len(codebook.patterns) for codebook in e_codebooks]
    lengths_from16 = [len(codebook.patterns) for codebook in e_codebooks_from16]
    lengths_from64 = [len(codebook.patterns) for codebook in e_codebooks_from64]

    # Prepare data for plotting
    all_metrics = [metrics, metrics_from16, metrics_from64]
    all_lengths = [lengths, lengths_from16, lengths_from64]
    labels = [
        'euclidean codebooks generated directly',
        'euclidean codebooks generated from codebook of size 16',
        'euclidean codebooks generated from codebook of size 64'
    ]
    plot_codebooks_metrics(all_metrics, all_lengths, labels, TITLE="M")

    # METRIC / Q-1
    # Calculate metrics for each set of codebooks
    metrics = calculate_metric_for_codebooks_div_by_len(e_codebooks)
    metrics_from16 = calculate_metric_for_codebooks_div_by_len(e_codebooks_from16)
    metrics_from64 = calculate_metric_for_codebooks_div_by_len(e_codebooks_from64)

    # Get lengths of the codebooks
    lengths = [len(codebook.patterns) for codebook in e_codebooks]
    lengths_from16 = [len(codebook.patterns) for codebook in e_codebooks_from16]
    lengths_from64 = [len(codebook.patterns) for codebook in e_codebooks_from64]

    # Prepare data for plotting
    all_metrics = [metrics, metrics_from16, metrics_from64]
    all_lengths = [lengths, lengths_from16, lengths_from64]
    labels = [
        'euclidean codebooks generated directly',
        'euclidean codebooks generated from codebook of size 16',
        'euclidean codebooks generated from codebook of size 64'
    ]
    plot_codebooks_metrics(all_metrics, all_lengths, labels, TITLE="M / (Q-1)")

    # sqrt(M) / Q-1
    # Calculate metrics for each set of codebooks
    metrics = calculate_metric_for_codebooks_sqrt_div_by_len(e_codebooks)
    metrics_from16 = calculate_metric_for_codebooks_sqrt_div_by_len(e_codebooks_from16)
    metrics_from64 = calculate_metric_for_codebooks_sqrt_div_by_len(e_codebooks_from64)

    # Get lengths of the codebooks
    lengths = [len(codebook.patterns) for codebook in e_codebooks]
    lengths_from16 = [len(codebook.patterns) for codebook in e_codebooks_from16]
    lengths_from64 = [len(codebook.patterns) for codebook in e_codebooks_from64]

    # Prepare data for plotting
    all_metrics = [metrics, metrics_from16, metrics_from64]
    all_lengths = [lengths, lengths_from16, lengths_from64]
    labels = [
        'euclidean codebooks generated directly',
        'euclidean codebooks generated from codebook of size 16',
        'euclidean codebooks generated from codebook of size 64'
    ]
    plot_codebooks_metrics(all_metrics, all_lengths, labels, TITLE="sqrt(M) / (Q-1)")

    #sqrt(M) / (Q-1) / Q
    # Calculate metrics for each set of codebooks
    metrics = calculate_metric_for_codebooks_sqrt_div_by_len_div_by_len(e_codebooks)
    metrics_from16 = calculate_metric_for_codebooks_sqrt_div_by_len_div_by_len(e_codebooks_from16)
    metrics_from64 = calculate_metric_for_codebooks_sqrt_div_by_len_div_by_len(e_codebooks_from64)

    # Get lengths of the codebooks
    lengths = [len(codebook.patterns) for codebook in e_codebooks]
    lengths_from16 = [len(codebook.patterns) for codebook in e_codebooks_from16]
    lengths_from64 = [len(codebook.patterns) for codebook in e_codebooks_from64]

    # Prepare data for plotting
    all_metrics = [metrics, metrics_from16, metrics_from64]
    all_lengths = [lengths, lengths_from16, lengths_from64]
    labels = [
        'euclidean codebooks generated directly',
        'euclidean codebooks generated from codebook of size 16',
        'euclidean codebooks generated from codebook of size 64'
    ]
    plot_codebooks_metrics(all_metrics, all_lengths, labels, TITLE="sqrt(M) / (Q-1) / Q")

    # sqrt(M/(Q-1))
    # Calculate metrics for each set of codebooks
    metrics = calculate_metric_for_codebooks_div_by_len_sqrt(e_codebooks)
    metrics_from16 = calculate_metric_for_codebooks_div_by_len_sqrt(e_codebooks_from16)
    metrics_from64 = calculate_metric_for_codebooks_div_by_len_sqrt(e_codebooks_from64)

    # Get lengths of the codebooks
    lengths = [len(codebook.patterns) for codebook in e_codebooks]
    lengths_from16 = [len(codebook.patterns) for codebook in e_codebooks_from16]
    lengths_from64 = [len(codebook.patterns) for codebook in e_codebooks_from64]

    # Prepare data for plotting
    all_metrics = [metrics, metrics_from16, metrics_from64]
    all_lengths = [lengths, lengths_from16, lengths_from64]
    labels = [
        'euclidean codebooks generated directly',
        'euclidean codebooks generated from codebook of size 16',
        'euclidean codebooks generated from codebook of size 64'
    ]
    plot_codebooks_metrics(all_metrics, all_lengths, labels,TITLE="sqrt(M/(Q-1))")

    # sqrt(M)
    # Calculate metrics for each set of codebooks
    metrics = calculate_metric_for_codebooks_sqrt(e_codebooks)
    metrics_from16 = calculate_metric_for_codebooks_sqrt(e_codebooks_from16)
    metrics_from64 = calculate_metric_for_codebooks_sqrt(e_codebooks_from64)

    # Get lengths of the codebooks
    lengths = [len(codebook.patterns) for codebook in e_codebooks]
    lengths_from16 = [len(codebook.patterns) for codebook in e_codebooks_from16]
    lengths_from64 = [len(codebook.patterns) for codebook in e_codebooks_from64]

    # Prepare data for plotting
    all_metrics = [metrics, metrics_from16, metrics_from64]
    all_lengths = [lengths, lengths_from16, lengths_from64]
    labels = [
        'euclidean codebooks generated directly',
        'euclidean codebooks generated from codebook of size 16',
        'euclidean codebooks generated from codebook of size 64'
    ]
    plot_codebooks_metrics(all_metrics, all_lengths, labels,TITLE="sqrt(M)")

    pass