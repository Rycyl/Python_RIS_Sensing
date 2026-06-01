import csv
import ast  # Used for safely evaluating the string list "[...]" into a real list
import os
import matplotlib.pyplot as plt


def parse_custom_csv(filename, cut_down = True):
    parsed_data = []

    try:
        with open(filename, 'r') as csvfile:
            # Initialize DictReader with semicolon delimiter
            # This allows us to access columns by name (e.g., row['N'])
            reader = csv.DictReader(csvfile, delimiter=';')
            
            # Clean up field names (remove potential surrounding whitespace)
            reader.fieldnames = [name.strip() for name in reader.fieldnames]

            for row in reader:
                # 1. Parse N (Integer)
                # We use .strip() to remove any accidental whitespace around the number
                n_val = int(row['N'].strip())

                # 2. Parse Pattern (String)
                pattern_val = row['Pattern'].strip()

                # 3. Parse Power (Array of floats)
                # The file contains strings like "[-20.33, -21.41]"
                # ast.literal_eval safely evaluates a string containing a Python literal
                power_raw = row['Power'].strip()
                power_list = ast.literal_eval(power_raw)

                if cut_down:
                    power_list = power_list[224:1824:2]
                    #pass

                # Store the relevant data
                entry = {
                    'N': n_val,
                    'Pattern': pattern_val,
                    'Power': power_list
                }
                
                parsed_data.append(entry)

    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
    except ValueError as e:
        print(f"Error parsing value: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return parsed_data

def select_best_worst(index, results):
    temp = []
    for entry in results:
        power = entry['Power']
        temp.append(power[index])
    sorted_pow = sorted(enumerate(temp), key=lambda x: x[1])
    worst = sorted_pow[0]
    best = sorted_pow[-1]
    print(best, worst)
    return worst[0], best[0]


# --- Main Execution ---
if __name__ == "__main__":
    csv_filename = '.\\wyniki\\Test of system_26_Nov_2025_2.csv'
    
    results = parse_custom_csv(csv_filename)
    x = [i for i in range(len(results[0]["Power"]))]
    pod = 500
    worst_n, best_n = select_best_worst(pod, results)
    print(f"Best is {best_n}")
    print(f"Worst is {worst_n}")
    # 3. Print results to demonstrate success
    print("\n--- Parsed Data ---")
    for item in results:
        #print(f"N: {item['N']} (Type: {type(item['N']).__name__})")
        #print(f"Pattern: {item['Pattern']} (Type: {type(item['Pattern']).__name__})")
        #print(f"Power: {item['Power']} (Type: {type(item['Power']).__name__})")
        #print("-" * 30)
        if best_n == item['N']:
            best_power = item['Power']
            best_pattern = item['Pattern']
        elif worst_n == item['N']:
            worst_power = item['Power']
            worst_pattern = item['Pattern']
        #plt.scatter(x, item['Power'], marker="o")
    
    plt.scatter(x, best_power, label=f"Best pattern: {best_pattern}", marker='o')
    plt.scatter(x, worst_power, label=f"Worst pattern: {worst_pattern}", marker='o')
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Test")
    plt.legend()
    plt.grid(True)
    #plt.tight_layout()
    plt.show()