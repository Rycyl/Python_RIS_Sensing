import os
import csv


file_name = "Virt_anal_trace_data.csv"
save_file = "Example_trace.csv"

with open(file_name, 'r') as f:
    csv_reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC, quotechar= '|')
    x = 0
    for row in csv_reader:
        x +=1
        if x == 4:
            with open("Example_trace.csv", "w+") as sf:
                sf.write(str(row)[1:-1])
                sf.close()
            break
    f.close()

print("Done")