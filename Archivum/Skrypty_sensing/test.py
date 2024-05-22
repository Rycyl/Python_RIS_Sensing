import matplotlib.pyplot as plt
import numpy as np

# Sample data
data = [-50, -60, -70, -45, -55]

data = sorted(data, reverse=True)
# Setting up the plot
plt.figure(figsize=(8, 6))
plt.bar(range(len(data)), np.abs(data), bottom=-80)

# Setting y-axis limits
#plt.ylim(-80, 0)
#plt.gca().invert_yaxis()
# Showing the plot
plt.show()
