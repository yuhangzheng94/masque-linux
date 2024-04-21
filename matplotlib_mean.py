import numpy as np
import matplotlib.pyplot as plt

# Function to calculate the average round trip time for a file
def calculate_average_rtts(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        rtts = [float(line.strip().split(',')[3]) for line in lines]
        average_rtt = sum(rtts) / len(rtts)
        return average_rtt

# List of input files for TCP and masquerade
tcp_files = ['test/tcp_1350_1_25.txt','test/tcp_1350_5_25.txt','test/tcp_1350_10_25.txt','test/tcp_1350_15_25.txt','test/tcp_1350_25_25.txt','test/tcp_1350_50_25.txt']
# tcp_files = ['test/tcp_info_0.txt', 'test/tcp_info_0.1.txt', 'test/tcp_info_1.txt', 'test/tcp_info_2.txt']
# masquerade_files = ['test/masque_info_0.txt', 'test/masque_info_0.1.txt', 'test/masque_info_1.txt', 'test/masque_info_2.txt']
masquerade_files = ['test/masque_info_1350_1_25.txt', 'test/masque_info_1350_5_25.txt', 'test/masque_info_1350_10_25.txt', 'test/masque_info_1350_15_25.txt', 'test/masque_info_1350_25_25.txt', 'test/masque_info_1350_50_25.txt', ]

# List of delay values
# delays = ['0%', '0.1%', '1%', '2%']
delays = ['1ms', '5ms', '10ms', '15ms', '25ms', '50ms']

# Lists to store average round trip times for TCP and masquerade
average_rtts_tcp = []
average_rtts_masquerade = []

# Calculate average round trip time for each file in TCP set
for file in tcp_files:
    average_rtt = calculate_average_rtts(file)
    average_rtts_tcp.append(average_rtt)

# Calculate average round trip time for each file in masquerade set
for file in masquerade_files:
    average_rtt = calculate_average_rtts(file)
    average_rtts_masquerade.append(average_rtt)

# Set the width of the bars
bar_width = 0.35

# Set the positions of the bars on the x-axis
r1 = np.arange(len(average_rtts_tcp))
r2 = [x + bar_width for x in r1]

# Generate the chart
# plt.bar(r1, average_rtts_tcp, color='b', width=bar_width, edgecolor='white', label='TCP')
plt.bar(r2, average_rtts_masquerade, color='g', width=bar_width, edgecolor='white', label='Masquerade')

# Add x-axis ticks and labels
plt.xlabel('Delay')
plt.ylabel('Average Round Trip Time')
plt.title('Average Round Trip Time by Delay')
plt.xticks([r + bar_width/2 for r in range(len(average_rtts_tcp))], delays)

# Add legend
plt.legend()

# Display the chart
plt.tight_layout()
plt.show()