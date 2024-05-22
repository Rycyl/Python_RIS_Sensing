import csv
import numpy as np

def write_best_datasets_to_file(input_csv_file, output_csv_file, num_datasets=10):
    # Read data from input CSV file
    datasets = []
    with open(input_csv_file, 'r') as file:
        reader = csv.reader(file)
        rows = []
        for row in reader:
            if row[0].startswith("pomiar"):  # New dataset starts
                if len(rows) == 4:  # Process the previous dataset
                    process_dataset(rows, datasets)
                rows = []  # Start collecting new dataset rows
            rows.append(row)  # Collect row
            print(row[0])
        if len(rows) == 4:  # Process the last dataset
            process_dataset(rows, datasets)
    
    # Sort datasets by the difference between Pat 2 Power and Pat 1 Power (descending order)
    datasets.sort(key=lambda x: x[2], reverse=True)
    #print(datasets[:num_datasets])
    # Write top 'num_datasets' datasets to output CSV file
    with open(output_csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for i, dataset in enumerate(datasets[:num_datasets], 1):
            for row in dataset:  # Write the entire dataset
                writer.writerow(row)
    
    print(f"{num_datasets} best datasets have been written to {output_csv_file}")

def process_dataset(rows, datasets):
    current_dataset_number = rows[0][0].split()[1]
    current_date = ' '.join(rows[0][1:])
    data = []
    l_of_data = []
    '''
    for row in rows[1:]:
        data_leanght = int(row[0].split(';')[0])
        #data_first = row[0].split(';')[1]
        n_data = row[1:]
        n_data.insert(0, data_first)
        data.append(n_data)
        l_of_data.append(data_leanght)
        '''
    noise_level = np.array(rows[1][1:1001], dtype=float)
    pat1_power = np.array(rows[2][1:1001], dtype=float)
    pat2_power = np.array(rows[3][1:1001], dtype=float)
    #print(noise_level)
    #print(noise_level)
    # length = int(rows[0][0].split(';')[0])  # Extract length from the first value
    # noise_level = np.array([float(value.split(';')[1]) for value in rows[1][1:length+1]])
    # pat1_power = np.array([float(value.split(';')[1]) for value in rows[2][1:length+1]])
    # pat2_power = np.array([float(value.split(';')[1]) for value in rows[3][1:length+1]])

    
    # Calculate averages
    avg_pat1_power = np.mean(pat1_power)
    avg_pat2_power = np.mean(pat2_power)
    avg_noise_level = np.mean(noise_level)
    
    # Check criteria
    if avg_pat2_power > avg_pat1_power and abs(avg_pat1_power - avg_noise_level) <= abs(avg_pat2_power - avg_pat1_power):
        datasets.append((current_dataset_number, current_date, avg_pat2_power - avg_pat1_power, avg_pat1_power, avg_pat2_power, rows))




file_name = 'Pomiar_noc_sobota-52'
input_csv_file = file_name + '.csv'
output_csv_file = file_name + '_best.csv'
write_best_datasets_to_file(input_csv_file, output_csv_file)
