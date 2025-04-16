import matplotlib.pyplot as plt

# Create some data
x = [0, 1, 2, 3, 4, 5]
y = [0, 1, 4, 9, 16, 25]

# Create a plot
plt.plot(x, y, label='y = x^2')

# Add a horizontal line at y = 10
plt.axhline(y=10, color='r', linestyle='--', label='y = 10')

# Add labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Plot with Horizontal Line')
plt.legend()

# Show the plot
plt.show()