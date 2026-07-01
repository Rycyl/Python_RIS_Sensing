from pathlib import Path
import csv
import glob
import os
import tempfile
import shutil
import numpy as np

def merge_specific_files_builtin(file_list, output_filename):
    print("Merging files...")
    
    with open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
        # Set up the writer with the semicolon separator
        writer = csv.writer(outfile, delimiter=';')
        
        for index, file_path in enumerate(file_list):
            try:
                with open(file_path, 'r', newline='', encoding='utf-8') as infile:
                    reader = csv.reader(infile, delimiter=';')
                    
                    header = next(reader, None)
                    
                    # Write the header only if it's the very first file
                    if index == 0 and header is not None:
                        writer.writerow(header)
                    
                    # Write all the data rows
                    for row in reader:
                        writer.writerow(row)
                        
                print(f"Added: {file_path}")
            except FileNotFoundError:
                print(f"Warning: Could not find '{file_path}'. Skipping.")
                
    print(f"Success! Merged data saved to '{output_filename}'")


def increment_n_in_files(file_prefix, directory=".", add_value=10000, new_N = False):
    # Find all files matching the prefix
    pattern = os.path.join(directory, f"{file_prefix}*.csv")
    matching_files = glob.glob(pattern)
    
    if not matching_files:
        print(f"No files found starting with '{file_prefix}' in '{directory}'")
        return

    print(f"Found {len(matching_files)} files. Updating 'N' values...")
    i = 0
    for filepath in matching_files:
        # Create a temporary file to write to
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, newline='', encoding='utf-8')
        
        with open(filepath, 'r', newline='', encoding='utf-8') as infile, temp_file:
            # Note the semicolon delimiter!
            reader = csv.reader(infile, delimiter=';')
            writer = csv.writer(temp_file, delimiter=';')
            
            # Read and write the header as-is
            header = next(reader, None)
            if header:
                writer.writerow(header)
            
            # Loop through the data, update N, and write
            for row in reader:
                if row:  # Ensure the row isn't empty
                    # N is the first column (index 0). Convert to int, add value, back to string
                    if new_N:
                        row[0] = str(i + add_value)
                        writer.writerow(row)
                        i+=1
                    else:
                        row[0] = str(int(row[0]) + add_value)
                        writer.writerow(row)
                    
        # Replace the original file with the updated temporary file
        shutil.move(temp_file.name, filepath)
        print(f"Updated: {filepath}")

    print("All files updated successfully!")

def merge_csv_builtin(file_prefix, output_filename, directory="."):
    target_dir = Path(directory)
    
    # Find all CSV files that start with the prefix
    matching_files = list(target_dir.glob(f"{file_prefix}*.csv"))
    
    if not matching_files:
        print(f"No CSV files found starting with '{file_prefix}' in '{directory}'")
        return
        
    print(f"Found {len(matching_files)} files. Merging...")

    with open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        
        for index, file_path in enumerate(matching_files):
            with open(file_path, 'r', newline='', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                
                # If it's the first file, write the header. 
                # Otherwise, skip the header row.
                header = next(reader, None)
                if index == 0 and header is not None:
                    writer.writerow(header)
                
                # Write the remaining data rows
                for row in reader:
                    writer.writerow(row)
                    
    print(f"Success! Merged data saved to {output_filename}")

# --- Run the script ---
if __name__ == "__main__":
    # Example: Merges all files starting with "report_" into "master_report.csv"
    files_to_merge = ["1_euklides_codebook_merged.csv", "2_Arranged_codebook_merged.csv", "3_full_codebook_merged.csv"]
    merge_csv_builtin(file_prefix="euklides_codebook_128", output_filename="1_euklides_codebook_merged.csv")
    merge_csv_builtin(file_prefix="Arranged_codebook", output_filename="2_Arranged_codebook_merged.csv")
    merge_csv_builtin(file_prefix="full_codebook", output_filename="3_full_codebook_merged.csv")
    print("Normal Done")
    ref_carriers = np.linspace(0, 789, 10, dtype=np.int32)
    # n = 3
    for i, n in enumerate(ref_carriers):
        out_file_one = f"{i}_ref_strip_by_strip_carrier_{n}_merged"
        out_file_two = f"{i}_ref_strip_by_strip_carrier_{n}_merged"

        print("Doing mearg for files", (out_file_one, out_file_two))

        merge_csv_builtin(file_prefix=f"ref_strip_by_strip_carrier_{n}", output_filename=out_file_one+".csv")
        merge_csv_builtin(file_prefix=f"ref_strip_by_strip_carrier_{n}_min", output_filename=out_file_two+".csv")

        print("Fixing N for files", (out_file_one, out_file_two))

        increment_n_in_files(file_prefix=out_file_one, add_value=-1000, new_N=False)
        increment_n_in_files(file_prefix=out_file_two, add_value=-2000, new_N=False)

        print("Adding N for files", (out_file_one, out_file_two))

        increment_n_in_files(file_prefix=out_file_one, add_value=100000 + (i*100), new_N=False)
        increment_n_in_files(file_prefix=out_file_two, add_value=200000 + (i*100), new_N=False)

        files_to_merge.append(out_file_one+".csv")
        files_to_merge.append(out_file_two+".csv")

        n += 1
        
    increment_n_in_files(file_prefix="2_Arranged_codebook_merged.csv", add_value=5000, new_N=False)
    increment_n_in_files(file_prefix="3_full_codebook_merged.csv", add_value=10000, new_N=True)
    #files_to_merge = ["euklides_codebook_128_0_08_May_2026_merged.csv", "2_PK_codebook_final_08_May_2026_merged.csv", "3_ref_strp_by_strp_08_May_2026_merged_new_N.csv"]
    merge_specific_files_builtin(files_to_merge, "All_measurements_merged.csv")