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
    hex_map = {
        '0000': '0', '0001': '1', '0010': '2', '0011': '3',
        '0100': '4', '0101': '5', '0110': '6', '0111': '7',
        '1000': '8', '1001': '9', '1010': 'A', '1011': 'B',
        '1100': 'C', '1101': 'D', '1110': 'E', '1111': 'F'
    }
    ret = "0x"
    a = ""
    for b in bits:
        a += str(b)
        if len(a) < 4:
            continue
        ret += hex_map[a]
        a = ""
    return ret
   
def turntohex(decimal):
    hex_string = hex(decimal)
    # Remove the '0x' prefix
    hex_string = hex_string[2:]
    # Add leading zeros to ensure the string length is 64 characters
    hex_string = '0' * (64 - len(hex_string)) + hex_string
    # Add the '0x' prefix back
    hex_string = '0x' + hex_string
    return hex_string