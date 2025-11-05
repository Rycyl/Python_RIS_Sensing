import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === Configuration ===
csv_file = "temp_data_cfreq_p_half_rbw_no_synch_50.csv"   # Change this to your CSV filename

# === Load the CSV file (semicolon-separated) ===
data = pd.read_csv(csv_file, header=None, sep=';')

x = pd.to_numeric(data.iloc[0])         # First row = x-axis
y_data = data.iloc[1:].apply(pd.to_numeric) # Remaining rows = data series

fc = 5.36E9 - (50000/2)
span = 102400000

signal_start = fc - (80E6/2)
signal_end = fc + (80E6/2)
step = 10E3  # 10,000

steps = np.arange(signal_start, signal_end, step)

# === 4. Create the filter mask from the X-values ===
# Create boolean conditions for the 'x' Series
condition_start = x >= signal_start
condition_end = x <= signal_end
condition_step = (x in steps)

combined_mask = condition_start & condition_end & condition_step
print(combined_mask)
x_filtered = x[combined_mask]
y_data_filtered = y_data.loc[:, combined_mask]
# rozne = []
# for i in range(len(x)-1):
#     rozne.append(x[i+1]-x[i])

# print("Maks różnic: ",max(rozne))
# print("Min różnic",min(rozne))
# print("Ilość punktów: ", len(x))
# print("Start spanu: ", x[0])
# print("Koniec spanu: ", x[len(x)-2])
# print(x[len(x)-2] - x[0])
#print(y_data.idxmax())
print(x_filtered)
# === Plot each row of data ===
plt.figure(figsize=(10, 6))
for i in range(len(y_data_filtered)):
    plt.plot(
        x_filtered, 
        y_data_filtered.iloc[i], 
        marker='o', 
        linestyle='-',
        linewidth=2,
        label=f'Filtered Series {i+1}'
    )
# for i, row in y_data.iterrows():
#     #print(len(row))
#     plt.plot(x, row, label=f"Series {i}", marker="o")

# # === Add labels, grid, legend ===

# #plt.xlim(5.36E9-1E6, 5.36E9+1E6)
# # plt.ylim(-70,-100)
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Plot from CSV (first row = X-axis)")
#plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
