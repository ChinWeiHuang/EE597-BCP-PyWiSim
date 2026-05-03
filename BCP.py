"""Backpressure Collection Protocol (BCP) over a static wireless network."""
import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import math
from pywisim import EventLoop, Node, WirelessNetwork

class BCPNode(Node):
    def __init__(self, nid, is_sink=False, V=1, scheduling_method='LIFO'):
        super().__init__(nid)
        self.V = V # The V in weights = queue_diff - V*ETX
        self.queue = 0
        self.is_sink = is_sink    
        self.weight = {}
        self.payloads = []
        self.scheduling_method = scheduling_method # 'LIFO' or 'FIFO'
        self.delay = {}
    def on_receive(self, msg, sender):
        _, origin, payload = msg
        if self.is_sink:
            self.net.log(f"{self.nid} (sink) received data: '{payload}'")
        else:
            self.net.log(f"{self.nid} got '{payload}' from {origin} (via {sender})")
            self.queue += 1
        self.payloads.append(payload)
        self.delay[payload] = self.net.loop.time # record the time of arrival for this payload
        # The size of payloads should be equal to the queue size except for the sink.
    def get_etx(self, node_a, node_b):
        d = self.net.dist(node_a, node_b)
        if not self.net.loss: # no loss if self.net.loss = 0 => ETX = 1 if within range, else inf
            return 1.0 if node_b in self.net.neighbors(node_a) else float('inf')
        else: # reuse the delivery probability from pywisim
            p_delivery = (1 - self.net.loss) / (1 + math.exp(4 / self.net.R * (d - 2 * self.net.R)))
            return 1.0 / p_delivery
    def get_weight(self):
        neighbors = self.net.neighbors(self.nid)
        for n in neighbors:
            ETX = self.get_etx(self.nid, n)
            self.weight[n] = self.queue - self.net.nodes[n].queue - self.V * ETX
    def send(self):
        if self.queue == 0: return # nothing to send
        self.get_weight()
        best_neighbor = max(self.weight, key=self.weight.get)
        if self.weight[best_neighbor] > 0:
            if self.scheduling_method == 'LIFO':
                payload = self.payloads.pop() # LIFO: get the most recently received payload to send
            elif self.scheduling_method == 'FIFO':
                payload = self.payloads.pop(0) # FIFO: get the oldest received payload to send
            self.delay.pop(payload, None) # remove the payload from delay tracking since it's being sent
            self.net.log(f"{self.nid} sends '{payload}' to {best_neighbor} (weight={self.weight[best_neighbor]:.2f})")
            self.unicast(best_neighbor, ('BCP', self.nid, payload))
            self.queue -= 1
        else:
            self.net.log(f"{self.nid} has no positive weight neighbors to send its payloads. Best weight: {self.weight[best_neighbor]:.2f} to {best_neighbor}, ETX to {best_neighbor}: {self.get_etx(self.nid, best_neighbor):.2f}")
            for payload in self.payloads:
                self.delay[payload] = self.net.loop.time
    def arrival(self, payload):
        self.payloads.append(payload)
        if self.is_sink:
            self.net.log(f"{self.nid} (sink) received data: '{payload}'")
        else:
            self.net.log(f"{self.nid} got '{payload}' from external arrival")
            self.queue += 1
            self.delay[payload] = self.net.loop.time # record the time of arrival for this payload
    def print_state(self):
        self.net.log(f"{self.nid} state: queue={self.queue}, payloads={self.payloads}")
