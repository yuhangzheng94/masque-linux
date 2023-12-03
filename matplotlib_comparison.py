import matplotlib.pyplot as plt
import csv, math

# List of CSV file names
# csv_files = ['test/masque_info_1350_50_25.txt', 'test/masque_info_1350_25_25.txt', 'test/masque_info_1350_15_25.txt', 'test/masque_info_1350_10_25.txt', 'test/masque_info_1350_5_25.txt', 'test/masque_info_1350_1_25.txt', 'test/tcp_1350_50_25.txt','test/tcp_1350_25_25.txt','test/tcp_1350_15_25.txt','test/tcp_1350_10_25.txt','test/tcp_1350_5_25.txt','test/tcp_1350_1_25.txt']
csv_files = ['test/masque_info_0.txt','test/masque_info_0.1.txt','test/masque_info_1.txt','test/masque_info_2.txt','test/tcp_info_0.txt','test/tcp_info_0.1.txt','test/tcp_info_1.txt', 'test/tcp_info_2.txt']  # Add your file names here

# List of colors for each line
line_colors = ['red', 'blue', 'green', 'purple', 'orange', 'brown', 'yellow', 'pink','black','purple','orange', 'brown']  # Add your desired colors here

# # Variables to store the minimum and maximum x-axis values
# x_min = float('inf')
# x_max = float('-inf')

# Iterate over each CSV file
for file, color in zip(csv_files, line_colors):
    # Lists to store data from the current file
    start_time = []
    difference = []

    # count = 0

    # Read the CSV file and extract the data
    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            # count += 1
            # if (count <= 2):
            #     continue
            start_time.append(int(row[0]))
            difference.append(math.log(float(row[3])))

    # # Update the minimum and maximum x-axis values
    # x_min = min(x_min, min(start_time))
    # x_max = max(x_max, max(start_time))

    # Plot the line graph for the current file
    plt.plot(start_time, difference, color=color, label=file)

    # # Identify outliers
    # outliers = []  # Add your logic to identify outliers here
    # for i in range(20):
    #     if (difference[i] in sorted(difference)[15:]):
    #         outliers.append(i)
        
    # # Plot outliers with a different marker
    # plt.scatter([start_time[i] for i in outliers], [difference[i] for i in outliers], color='black', marker='o')


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