import json
import csv

try:
    with open("RIS_patterns.json") as json_patterns:
        patterns_obj = json.load(json_patterns)
        patterns_data = patterns_obj["PATTERNS"]
except FileNotFoundError:
    print("File with patterns doesn't exist.")
    exit()
    


with open('wyniki/25_03_31_03/25_03_reflection_20cm_4cm_17cm.csv',"r", newline='') as input:
    with open('wyniki/25_03_31_03/25_03_reflection_20cm_4cm_17cm_copy.csv',"w", newline='') as output:
        spamreader = csv.reader(input, delimiter=";", quotechar='|')
        writer = csv.writer(output)
        for row in spamreader:
            for pattern in patterns_data:
                if row[0]==pattern["DESC"]:
                    row.append(pattern["ID"])
                    writer.writerow(row)


                    
                
