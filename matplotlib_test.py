import matplotlib.pyplot as plt
import csv

# Lists to store the index and time collapse values
index_values = []
time_collapse_values = []

# Read the CSV file and extract the data
with open('test/test3.txt', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        index_values.append(int(row[0]))
        time_collapse_values.append(int(row[3]))

# Create the line chart
plt.plot(index_values, time_collapse_values)

# Set the labels and title
plt.xlabel('Index')
plt.ylabel('Time Collapse')
plt.title('Line Chart')

# Display the chart
plt.show()