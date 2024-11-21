import os
from datetime import datetime


def create_results_folder(base_path='Wyniki'):
    """Create a subfolder in the specified base path with the current date."""
    # Get the current date in day-month format
    current_date = datetime.now().strftime("%d-%m")
    
    # Create the full path for the new folder
    results_folder = os.path.join(base_path, current_date)
    
    # Create the directory if it doesn't exist
    os.makedirs(results_folder, exist_ok=True)
    
    return results_folder

def create_trace_file_header(trace_file_name, swt, n_elements):
    i = 1
    while True:
        filename = f"{trace_file_name}_{swt}_{n_elements}_{i}.csv"
        if not os.path.exists(filename):    
            with open(filename, 'w') as file:
                file.write(f"|SWT|, {swt}\n")
                file.close()
                return filename
        else:
            i += 1
        
def write_trace_file(trace_file, trace_data):
    with open(trace_file, 'a+') as file:
        file.write(f'{str(trace_data)[1:-1]}\n')
        file.write('\n')
        file.close()
    return