import csv

def get_angles(n: str):
    with open("number_encoder", newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
            if row[0]==n:
                return  "Rx=" + row[2] + " Tx=" + row[1]
