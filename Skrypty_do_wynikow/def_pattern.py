import json
import os
import os.path
def check_pattern_from_hex(pattern):
    data_folder = os.path.join("..")
    file_path = os.path.join(data_folder, "RIS_patterns.json")
    # Opening JSON file
    f = open(file_path)
 
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
 
    # Iterating through the json
    # list
    for i in data['PATTERNS']:
        #print(i['HEX'])
        if(pattern==i['HEX']):
            pattern=i['DESC']
            break
    # Closing file
    f.close()
    return pattern
    
def check_pattern_from_label(pattern):
    data_folder = os.path.join("..")
    file_path = os.path.join(data_folder, "RIS_patterns.json")
    # Opening JSON file
    f = open(file_path)
 
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
 
    # Iterating through the json
    # list
    for i in data['PATTERNS']:
        #print(i['HEX'])
        if(pattern==i['DESC']):
            pattern=i['HEX']
            break
    # Closing file
    f.close()
    return pattern 
