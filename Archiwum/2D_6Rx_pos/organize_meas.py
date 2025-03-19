import os


def add_min_max(file_name):
    with open(file_name, "r") as f:
        lines = f.readlines()
        f.close()
    len_lines = len(lines)
    half_len = len_lines//2
    min_lines = lines[0:half_len]
    max_lines = lines[half_len:]
    min_lines.insert(0, 'MIN\n')
    max_lines.insert(0, 'MAX\n')
    min_lines.extend(max_lines)
    new_lines = min_lines[:]
    #print(new_lines)
    with open(file_name, 'w') as f:
        for line in new_lines:
            f.write(line)
        f.close()
    return

if __name__ == "__main__":
    path = os.path.join(os.getcwd(), 'Wyniki', '30-11')
    files = [file for file in os.listdir(path) if file.endswith(".csv")]
    files = [os.path.join(path, file) for file in files]
    for file in files:
        add_min_max(file)
    print("Done")
    exit()