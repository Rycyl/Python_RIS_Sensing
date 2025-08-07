import csv
import ast


def codebook_eval(codebook_name):
    patterns = []
    angles = []
    # Otwieranie pliku CSV z separatorem ';'
    with open(codebook_name, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        # Iterowanie przez wiersze w pliku
        for row in reader:
            patterns.append(row[0])
            angles.append(ast.literal_eval(row[1]))

    i = 0
    clean_patterns = []
    clean_angles = []
    used_idx = []
    while i < len(patterns):
        if(i in used_idx):
            i+=1
        else:
            clean_patterns.append(patterns[i])
            clean_angles.append(angles[i])
            j = i+1
            while j < len(patterns):
                if patterns[i] == patterns[j]:
                    used_idx.append(j)
                    print("FOUND SAME PATTERN AT:: ", i, j)
                    clean_angles[-1].extend(angles[j])
                j+=1
            i+=1

    # for i in range(len(clean_patterns)):
    #     print(clean_patterns[i], clean_angles[i])



    filename = codebook_name[0:-4] + "_v2.csv"

    with open(filename, mode='w', newline='') as file:
        for i in range(len(clean_angles)):
            #file.write(RIS_patterns[i].hex + ";" + "θ_i=" + str(degs[i][0]) + " θ_d=" + str(degs[i][1]) + "\n")
            file.write(str(i) + ";" + clean_patterns[i] + ";" + str(clean_angles[i]) + "\n")



    print(f'Data written to {filename}')