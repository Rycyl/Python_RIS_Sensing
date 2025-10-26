import pandas as pd
import matplotlib.pyplot as plt

# === Configuration ===
csv_file = "temp_data.csv"   # Change this to your CSV filename

# === Load the CSV file (semicolon-separated) ===
data = pd.read_csv(csv_file, header=None, sep=';')

# === Extract X and Y values ===
x = data.iloc[0]             # First row = x-axis
y_data = data.iloc[1:]       # Remaining rows = data series

# === Plot each row of data ===
plt.figure(figsize=(10, 6))
for i, row in y_data.iterrows():
    #print(len(row))
    plt.plot(x, row, label=f"Series {i}", marker="o")

# === Add labels, grid, legend ===
plt.xlim(5.33E9, 5.34E9)
# plt.ylim(-70,-100)
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Plot from CSV (first row = X-axis)")
#plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
