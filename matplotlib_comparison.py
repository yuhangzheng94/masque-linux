import matplotlib.pyplot as plt
import csv, math

# List of CSV file names
csv_files = ['test/masquerade_cubic.txt', 'test/masquerade_reno.txt',]  # Add your file names here

# List of colors for each line
line_colors = ['red', 'blue', 'green']  # Add your desired colors here

# # Variables to store the minimum and maximum x-axis values
# x_min = float('inf')
# x_max = float('-inf')

# Iterate over each CSV file
for file, color in zip(csv_files, line_colors):
    # Lists to store data from the current file
    start_time = []
    difference = []

    # Read the CSV file and extract the data
    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            start_time.append(float(row[0]))
            difference.append(math.log(float(row[3])))

    # # Update the minimum and maximum x-axis values
    # x_min = min(x_min, min(start_time))
    # x_max = max(x_max, max(start_time))

    # Plot the line graph for the current file
    plt.plot(start_time, difference, color=color, label=file)

    # Identify outliers
    outliers = []  # Add your logic to identify outliers here
    for i in range(100):
        if (difference[i] in sorted(difference)[95:]):
            outliers.append(i)
        
    # Plot outliers with a different marker
    plt.scatter([start_time[i] for i in outliers], [difference[i] for i in outliers], color='black', marker='o')


# Set the labels and title
plt.xlabel('Start Time')
plt.ylabel('Difference')
plt.title('Line Graph')

# # Set the x-axis limits
# print(x_max, x_min)
# plt.xlim(x_min, x_max)

# Add a legend
plt.legend()

# Display the graph
plt.show()