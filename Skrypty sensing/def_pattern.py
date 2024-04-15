import json
import os
import os.path
import bitarray
import binascii

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



def pattern_bin_to_hex(bits):
    ret = "0x"
    a = ""
    i = 0
    for b in bits:
        #print(i, len(a))
        i+=1
        a+=str(b)
        #print("ret:  ", ret, "    a:", a)
        if (len(a)<4):
            continue
        if a == "0000":
            ret += "0"
        elif a == "0001":
            ret += "1"
        elif a == "0010":
            ret += "2"
        elif a == "0011":
            ret += "3"
        elif a == "0100":
            ret += "4"
        elif a == "0101":
            ret += "5"
        elif a == "0110":
            ret += "6"
        elif a == "0111":
            ret += "7"
        elif a == "1000":
            ret += "8"
        elif a == "1001":
            ret += "9"
        elif a == "1010":
            ret += "A"
        elif a == "1011":
            ret += "B"
        elif a == "1100":
            ret += "C"
        elif a == "1101":
            ret += "D"
        elif a == "1110":
            ret += "E"
        elif a == "1111":
            ret += "F"
        a=""
    return ret
