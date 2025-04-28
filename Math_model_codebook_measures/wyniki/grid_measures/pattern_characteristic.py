from class_measures_result import Results
import numpy as np
import matplotlib.pyplot as plt
import os

results = Results()

# Create the directory if it doesn't exist
output_directory = 'pattern_characteristics'
os.makedirs(output_directory, exist_ok=True)

# Assuming results is a list of objects with attributes powers, Rx_Angle, and idx
for result in results.results:
    powers = result.powers
    rx = result.Rx_Angle
    idx = result.idx
    print("plotting.... ", idx)
    # Combine rx and powers into a list of tuples and sort by rx
    sorted_pairs = sorted(zip(rx, powers))
    
    # Unzip the sorted pairs back into sorted rx and powers
    sorted_rx, sorted_powers = zip(*sorted_pairs)

    # Create a new figure
    plt.figure()
    
    # Scatter plot
    plt.scatter(sorted_rx, sorted_powers, color='blue', label='Data Points')
    
    # Line plot to connect the dots
    plt.plot(sorted_rx, sorted_powers, color='orange', linestyle='-', label='Connecting Line')
    
    # Set the title with the id
    plt.title(f'Result ID: {idx}')
    
    # Set labels
    plt.xlabel('Rx Angle')
    plt.ylabel('Power')
    
    # Set y-axis limits
    plt.ylim(-85, -50)
    
    # Add a legend
    plt.legend()
    
    # Show the grid
    plt.grid()
    
    # Save the plot to the specified directory
    plt.savefig(os.path.join(output_directory, f'plot_{idx}.png'))
    
    # Close the figure to free up memory
    plt.close()
