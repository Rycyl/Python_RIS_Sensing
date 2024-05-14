import csv
import numpy as np

def read_data_from_file(input_csv_file):
    datasets = {}
    with open(input_csv_file, 'r') as file:
        reader = csv.reader(file)
        rows = []
        for row in reader:
            if row[0].startswith("pomiar"):
                pomiar_no = row[0].split()[1]
                date = ' '.join(row[1:])
                rows = []
            else:
                lenght = int(row[0].split(',')[0])
                rows.append(row[1:lenght+1])
                if len(rows) == 3:
                    #datasets.append((pomiar_no, date, rows))
                    data = create_data(rows)
                    datasets[pomiar_no] = (date, data)
    file.close()
    return datasets


def create_data(rows):
    noise_level = np.array(rows[0], dtype=float)
    pat1_power = np.array(rows[1], dtype=float)
    pat2_power = np.array(rows[2], dtype=float)
    
    avg_noise_level = np.mean(noise_level)
    avg_pat1_power = np.mean(pat1_power)
    avg_pat2_power = np.mean(pat2_power)
    
    noise_level = noise_level.tolist()
    pat1_power = pat1_power.tolist()
    pat2_power = pat2_power.tolist()
    
    avg_noise_level = float(avg_noise_level)
    avg_pat1_power = float(avg_pat1_power)
    avg_pat2_power = float(avg_pat2_power)
    
    ret_data = {
        "noise_level": noise_level,
        "pat1_power": pat1_power,
        "pat2_power": pat2_power,
        "avg_noise_level": avg_noise_level,
        "avg_pat1_power": avg_pat1_power,
        "avg_pat2_power": avg_pat2_power
    }
    return ret_data
    
def write_best(input_csv_file, output_csv_file,copy_file, num_datasets=10):
    datasets = read_data_from_file(input_csv_file)
    #print(datasets)
    datasets_list = list(datasets.items())
    datasets_list.sort(key=lambda x: x[1][1]["avg_pat2_power"] - x[1][1]["avg_pat1_power"], reverse=True)
    #print(datasets_list[:num_datasets])
    top_datasets = datasets_list[:num_datasets]
    with open(output_csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Pomiar No", "Date", "Avg Noise Level", "Avg Pat1 Power", "Avg Pat2 Power"])
        for dataset in top_datasets:
            pomiar_no = dataset[0]
            date = dataset[1][0]
            avg_noise_level = dataset[1][1]["avg_noise_level"]
            avg_pat1_power = dataset[1][1]["avg_pat1_power"]
            avg_pat2_power = dataset[1][1]["avg_pat2_power"]
            writer.writerow([pomiar_no, date, avg_noise_level, avg_pat1_power, avg_pat2_power])
    file.close()
    with open(copy_file, 'w', newline='') as file:
        writer = csv.writer(file)
        #writer.writerow(["Pomiar No", "Date"])
        for dataset in top_datasets:
            pomiar_no = dataset[0]
            date = dataset[1][0]
            writer.writerow([pomiar_no, date])
            noise_level = dataset[1][1]["noise_level"]
            pat1_power = dataset[1][1]["pat1_power"]
            pat2_power = dataset[1][1]["pat2_power"]
            file.write("Noise Level, ")
            writer.writerow(noise_level)
            file.write("Pattern 1 Power, ")
            writer.writerow(pat1_power)
            file.write("Pattern 2 Power, ")
            writer.writerow(pat2_power)
    file.close()


if __name__ == "__main__":
    file_name = "Pomiar_noc_sobota-52"
    input_file = file_name + ".csv"
    output_file = file_name + "_best.csv"
    copy_file = file_name + "_full_vals.csv"
    write_best(input_file, output_file, copy_file, 10)
                