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