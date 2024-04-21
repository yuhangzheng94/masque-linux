import numpy as np
import matplotlib.pyplot as plt

# Function to calculate the average one-way delay for a file
def calculate_average_delay(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        delays = [float(line.strip().split(',')[3]) for line in lines]
        average_delay = sum(delays) / len(delays)
        return average_delay

# List of input files for TCP and masquerade
tcp_files = ['test/tcp_1350_1_25.txt', 'test/tcp_1350_5_25.txt', 'test/tcp_1350_10_25.txt', 'test/tcp_1350_15_25.txt', 'test/tcp_1350_25_25.txt', 'test/tcp_1350_50_25.txt']
masquerade_files = ['test/masque_info_1350_1_25.txt', 'test/masque_info_1350_5_25.txt', 'test/masque_info_1350_10_25.txt', 'test/masque_info_1350_15_25.txt', 'test/masque_info_1350_25_25.txt', 'test/masque_info_1350_50_25.txt']

# List of one-way delay settings
delays = ['1ms', '5ms', '10ms', '15ms', '25ms', '50ms']

# Lists to store average one-way delays for TCP and masquerade
average_delays_tcp = []
average_delays_masquerade = []

# Calculate average one-way delay for each file in TCP set
for file in tcp_files:
    average_delay = calculate_average_delay(file)
    average_delays_tcp.append(np.log2(average_delay))

# Calculate average one-way delay for each file in masquerade set
for file in masquerade_files:
    average_delay = calculate_average_delay(file)
    average_delays_masquerade.append(np.log2(average_delay))

# Set the width of the bars
bar_width = 0.35

# Set the positions of the bars on the x-axis
r1 = np.arange(len(average_delays_tcp))
r2 = [x + bar_width for x in r1]

# Generate the chart
plt.bar(r1, average_delays_tcp, color='b', width=bar_width, edgecolor='white', label='TCP')
plt.bar(r2, average_delays_masquerade, color='g', width=bar_width, edgecolor='white', label='Masquerade')

# Add x-axis ticks and labels
plt.xlabel('One-way Delay')
plt.ylabel('Average One-way Delay')
plt.title('Average One-way Delay by Delay Setting')
plt.xticks([r + bar_width/2 for r in range(len(average_delays_tcp))], delays)

# Add legend
plt.legend()

# Display the chart
plt.tight_layout()
plt.show()

# import numpy as np
# import matplotlib.pyplot as plt

# # Function to calculate the average one-way delay for a file
# def calculate_average_delay(filename):
#     with open(filename, 'r') as file:
#         lines = file.readlines()
#         delays = [float(line.strip().split(',')[3]) for line in lines]
#         average_delay = sum(delays) / len(delays)
#         return average_delay

# # List of input files for TCP and masquerade
# tcp_files = ['test/tcp_1350_1_25.txt', 'test/tcp_1350_5_25.txt', 'test/tcp_1350_10_25.txt', 'test/tcp_1350_15_25.txt', 'test/tcp_1350_25_25.txt', 'test/tcp_1350_50_25.txt']
# masquerade_files = ['test/masque_info_1350_1_25.txt', 'test/masque_info_1350_5_25.txt', 'test/masque_info_1350_10_25.txt', 'test/masque_info_1350_15_25.txt', 'test/masque_info_1350_25_25.txt', 'test/masque_info_1350_50_25.txt']

# # List of one-way delay settings
# delays = ['1ms', '5ms', '10ms', '15ms', '25ms', '50ms']

# # Lists to store average one-way delays for TCP and masquerade
# average_delays_tcp = []
# average_delays_masquerade = []

# # Calculate average one-way delay for each file in TCP set
# for file in tcp_files:
#     average_delay = calculate_average_delay(file)
#     average_delays_tcp.append(average_delay)

# # Calculate average one-way delay for each file in masquerade set
# for file in masquerade_files:
#     average_delay = calculate_average_delay(file)
#     average_delays_masquerade.append(average_delay)

# # Set the width of the bars
# bar_width = 0.35

# # Set the positions of the bars on the x-axis
# r1 = np.arange(len(average_delays_tcp))
# r2 = [x + bar_width for x in r1]

# # Calculate the minimum value of the average delays
# min_delay = min(min(average_delays_tcp), min(average_delays_masquerade))

# # Generate the chart
# plt.bar(r1, np.log2(average_delays_tcp), color='b', width=bar_width, edgecolor='white', label='TCP')
# plt.bar(r2, np.log2(average_delays_masquerade), color='g', width=bar_width, edgecolor='white', label='Masquerade')

# # Add value labels to the bars
# for i, value in enumerate(average_delays_tcp):
#     plt.text(i, np.log2(value) + 0.05, f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
# for i, value in enumerate(average_delays_masquerade):
#     plt.text(i + bar_width, np.log2(value) + 0.05, f'{value:.2f}', ha='center', va='bottom', fontweight='bold')

# # Add x-axis ticks and labels
# plt.xlabel('One-way Delay')
# plt.ylabel('Logarithmic (base 2) Average One-way Delay')
# plt.title('Logarithmic (base 2) Average One-way Delay by Delay Setting')
# plt.xticks([r + bar_width/2 for r in range(len(average_delays_tcp))], delays)

# # Set the y-axis range
# plt.ylim(bottom=np.log2(min_delay))

# # Set the y-axis scale to logarithmic (base 2)
# plt.yscale('log', base=2)

# # Add legend
# plt.legend()

# # Display the chart
# plt.tight_layout()
# plt.show()