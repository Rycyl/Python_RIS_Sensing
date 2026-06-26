from class_codebook import *
from class_measures_result import Results

import copy

def select_results_for_codebook(results, codebook):
    new_results = Results(load_results=False)

    for pat in codebook.patterns: #loop throught all patterns
        for result in results.results: #loop throught all results
            if pat.pattern == result.pattern: #if current pattern is current result
                new_results.add_result(result) # add result to new results
                break #break looking for result as it was found

    return new_results

def select_results_for_ids(results, ids):
    new_results = Results(load_results=False)

    for id in ids: #loop throught all ids
        for result in results.results: #loop throught all
            if id == result.id: #if current id
                new_results.add_result(result) # add result to new
                break #break looking for result as it was found
               
    return new_results
