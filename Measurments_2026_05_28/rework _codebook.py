import csv

# Define the input and output file names
input_file = 'Codebook.csv'  # Change this to your input file name
output_file = 'nCodebook.csv'  # Change this to your desired output file name

# Open the input CSV file for reading
with open(input_file, 'r', encoding='utf-8') as infile:
    # Read all lines from the input file
    lines = infile.readlines()

# Open the output CSV file for writing
with open(output_file, 'w', encoding='utf-8') as outfile:
    # Iterate through the lines and add a unique ID
    i=0
    for line in lines:
        # Strip the line of leading/trailing whitespace and split by semicolon
        line = line.strip()
        # Create a new line with the unique ID added at the beginning
        new_line = f"{i};{line}\n"
        # Write the new line to the output file
        outfile.write(new_line)
        i+=1

print(f"Processed {input_file} and saved to {output_file}.")
