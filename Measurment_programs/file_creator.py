import os
import time

def create_file(common_name: str, directory = 'wyniki', use_date_in_name = True):
    exit_directory = os.getcwd()
    exit_directory = os.path.join(exit_directory, directory)
    if use_date_in_name:
        date = time.strftime("%d_%b_%Y")
        common_name += f"_{date}"
    existing_files_csv = os.listdir(exit_directory)
    existing_files = []
    for file in existing_files_csv:
        file = file.split(".")[0]
        existing_files.append(file)
    
    i = 1 

    while f"{common_name}_{i}" in existing_files:
        i += 1

    file_name = f"{common_name}_{i}.csv"
    file_name = os.path.join(exit_directory, file_name)

    file_name = os.path.join(exit_directory, file_name)

    with open (file_name, "w+") as f:
        f.close()
    
    return file_name


def is_file_empty(file):
    with open(file, 'r') as f:
        return f.read(1) == ''

def save_to_file(file, data):
    empty_file = is_file_empty(file)
    with open(file, 'a+') as csvfile:
        if empty_file:
            csvfile.write("N; Pattern; Power; Rx Angle; Tx Angle; a; c; x; y; b")
            csvfile.write("\n")
        for datum in data:
            for d in datum:
                csvfile.write(str(d)+";")
            csvfile.write("\n")
        csvfile.close()
    return 
