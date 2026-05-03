import re
import pandas as pd
import matplotlib.pyplot as plt

def parse_test2(filename):
    with open(filename, 'r') as f:
        content = f.read()
    content = re.sub(r'\\s*', '', content)
    
    rates = re.findall(r"Arrival rate: ([\d\.]+) packets/second", content)
    throughputs = re.findall(r"Average throughput: ([\d\.]+) packets/second", content)
    delays_all = re.findall(r"Average delay for all packets: ([\d\.]+) seconds", content)
    delays_arr = re.findall(r"Average delay for packets that reached the sink: ([\d\.]+) seconds", content)
    
    return {
        'rate': [float(r) for r in rates],
        'throughput': [float(t) for t in throughputs],
        'delay_all': [float(d) for d in delays_all],
        'delay_arr': [float(d) for d in delays_arr]
    }

data_bcp_fifo = parse_test2("BCP_test2_FIFO.txt")
data_bcp_lifo = parse_test2("BCP_test2_LIFO.txt")
data_rw_fifo = parse_test2("Random_walk_test2_FIFO.txt")
data_rw_lifo = parse_test2("Random_walk_test2_LIFO.txt")

plt.figure(figsize=(10, 6))
plt.plot(data_bcp_fifo['rate'], data_bcp_fifo['throughput'], marker='o', label='BCP FIFO')
plt.plot(data_bcp_lifo['rate'], data_bcp_lifo['throughput'], marker='s', label='BCP LIFO')
plt.plot(data_rw_fifo['rate'], data_rw_fifo['throughput'], marker='^', label='Random Walk FIFO')
plt.plot(data_rw_lifo['rate'], data_rw_lifo['throughput'], marker='x', label='Random Walk LIFO')
plt.xlabel('Arrival Rate (packets/second)')
plt.ylabel('Throughput (packets/second)')
plt.title('Throughput vs Arrival Rate')
plt.legend()
plt.grid(True)
plt.savefig('throughput_comparison.png')

plt.figure(figsize=(10, 6))
plt.plot(data_bcp_fifo['rate'], data_bcp_fifo['delay_arr'], marker='o', label='BCP FIFO')
plt.plot(data_bcp_lifo['rate'], data_bcp_lifo['delay_arr'], marker='s', label='BCP LIFO')
plt.plot(data_rw_fifo['rate'], data_rw_fifo['delay_arr'], marker='^', label='Random Walk FIFO')
plt.plot(data_rw_lifo['rate'], data_rw_lifo['delay_arr'], marker='x', label='Random Walk LIFO')
plt.xlabel('Arrival Rate (packets/second)')
plt.ylabel('Average Delay for Arrived Packets (seconds)')
plt.title('Delay vs Arrival Rate')
plt.legend()
plt.grid(True)
plt.savefig('delay_comparison_arr.png')

# Data for low arrival rates (0.2, 0.4, 0.6, 0.8)
rates_low = [0.2, 0.4, 0.6, 0.8]
bcp_fifo_low = [32.95, 17.47, 17.76, 13.72]
bcp_lifo_low = [2.01, 2.01, 2.01, 2.01]
rw_fifo_low = [3.3, 3.57, 4.1, 7.17]
rw_lifo_low = [3.2, 3.66, 4.1, 7.56]

plt.figure(figsize=(10, 6))
plt.plot(rates_low, bcp_fifo_low, marker='o', label='BCP FIFO')
plt.plot(rates_low, bcp_lifo_low, marker='s', label='BCP LIFO')
plt.plot(rates_low, rw_fifo_low, marker='^', label='Random Walk FIFO')
plt.plot(rates_low, rw_lifo_low, marker='x', label='Random Walk LIFO')
plt.xlabel('Arrival Rate (packets/second)')
plt.ylabel('Average Delay for Arrived Packets (seconds)')
plt.title('Delay vs Arrival Rate (Below Stability Limit)')
plt.legend()
plt.grid(True)
plt.savefig('delay_comparison_low_rate.png')