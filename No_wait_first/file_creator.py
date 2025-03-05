import os
import time

def create_file(common_name: str, directory = 'wyniki', use_date_in_name = True):
    exit_directory = os.getcwd()
    exit_directory = os.path.join(exit_directory, directory)
    if use_date_in_name:
        date = time.ctime()
        date = date.replace(" ", "_")
        date = date.replace(":", "_")
        common_name += f"_{date}"
    existing_files_csv = os.listdir(exit_directory)
    existing_files = []
    for file in existing_files_csv:
        file = file.split(".")[0]
        existing_files.append(file)
    
    i = 1

    for i in range(1, len(existing_files)):
        if "_".join([existing_files[i], str(i)]) in existing_files:
            i += 1
        else:
            existing_files = "_".join([existing_files[i], str(i)])
            break
    
    
    file_name = f"{common_name}_{i}.csv"

    file_name = os.path.join(exit_directory, file_name)

    with open (file_name, "w+") as f:
        f.close()
    
    return file_name

