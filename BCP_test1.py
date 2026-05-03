import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve() / "examples"))
import math
from pywisim import EventLoop, Node, WirelessNetwork
from BCP import BCPNode
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--scheduling", choices=["LIFO", "FIFO"], default="LIFO", help="Scheduling method")
args = parser.parse_args()

def main():
    # Configuration
    tx_range = 1
    tx_time = 0.5
    BCP_time_slot_width = 1
    sink = 'G'
    V = 1
    scheduling_method = args.scheduling # 'LIFO' or 'FIFO'
    n_pkt_total = 20
    runtime = 25 # simulation runtime in seconds
    print_flag = True
    loss=0.02

    # --- setup the network ---
    loop = EventLoop()
    net = WirelessNetwork(loop, tx_range=tx_range, tx_time=tx_time, loss=loss, seed=42, verbose=print_flag)
    for nid, x, y in [('A',0,0), ('B',1,0.5), ('C',1,-0.5), ('D',2,0.5), ('E',2,-0.5), ('F',3,0.5), ('G',3,-0.5)]:
        net.add_node(BCPNode(nid, is_sink=(nid == sink), V=V, scheduling_method=scheduling_method), x, y)

    # --- schedule packet arrivals at node A ---
    pkt_list = ["pkt " + str(i) for i in range(n_pkt_total)]
    pkt_counter = 0
    for idx_pkt in range(n_pkt_total):
        time = idx_pkt
        pkt = pkt_list[idx_pkt]
        pkt += ", gen_time=" + str(time) # append generation time to the payload for delay calculation
        # Schedule packet arrivals at node A every second starting from time 0
        loop.schedule(time, net.nodes['A'].arrival, pkt)
        pkt_list[idx_pkt] = pkt # update the pkt_list with the new payload containing generation time
        pkt_counter += 1

    # --- schedule BCP sending events for all non-sink nodes ---
    for nid in net.nodes:
        if nid != sink: # schedule all non-sink nodes to attempt sending every second
            for t in range(1, runtime, BCP_time_slot_width):
                loop.schedule(t, net.nodes[nid].send)

    loop.run(until=runtime) # run the simulation for a total of [runtime] seconds

    # --- print results and calculate average delay ---
    avg_delay = 0.0
    avg_delay_arrived = 0.0
    n_pkt_arrived = 0
    for nid in sorted(net.nodes):
        node = net.nodes[nid]
        node.print_state()
    for nid in sorted(net.nodes):
        node = net.nodes[nid]
        if node.is_sink:
            for payload in node.payloads:
                # Extract generation time from strings like "pkt 10_10"
                gen_time = float(payload.split('gen_time=')[1])
                arrival_time = node.delay[payload]
                true_delay = arrival_time - gen_time 
                avg_delay_arrived += true_delay
                n_pkt_arrived += 1
                avg_delay += true_delay
                pkt_list.remove(payload)
                if print_flag:
                    print(f"{payload} arrived at sink {nid} with delay {true_delay:.2f} seconds")
        else:
            for payload in node.payloads:
                gen_time = float(payload.split('gen_time=')[1])
                arrival_time = node.delay[payload]
                true_delay = arrival_time - gen_time 
                avg_delay += true_delay
                pkt_list.remove(payload)
                if print_flag:
                    print(f"{payload} stay at node {nid} with delay {true_delay:.2f} seconds")
    for pkt in pkt_list:
        gen_time = float(pkt.split('gen_time=')[1])
        true_delay = runtime - 1 - gen_time
        avg_delay += true_delay
    avg_delay /= n_pkt_total  # total number of packets
    print(f"\nScheduling method: {net.nodes['A'].scheduling_method}")
    print(f"\nAverage delay for all packets: {avg_delay:.2f} seconds")
    if n_pkt_arrived > 0:
        avg_delay_arrived /= n_pkt_arrived
        print(f"\nAverage delay for packets that reached the sink: {avg_delay_arrived:.2f} seconds")
    # avg_throughput = n_pkt_arrived / runtime
    
    # print(f"\nTotal packets generated: {pkt_counter}")
    # print(f"\nArrival rate: {arrival_rate} packets/second")
    # print(f"\nAverage throughput: {avg_throughput:.2f} packets/second")
    print("")
    

if __name__ == "__main__":
    main()