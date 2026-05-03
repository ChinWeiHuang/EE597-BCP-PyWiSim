"""Random Walk Protocol over a static wireless network."""
import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import random
from pywisim import EventLoop, Node, WirelessNetwork

class RandomNode(Node):
    def __init__(self, nid, is_sink=False, scheduling_method='FIFO'):
        super().__init__(nid)
        self.queue = 0
        self.is_sink = is_sink    
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

    def send(self):
        if self.queue == 0: return # nothing to send
        
        neighbors = list(self.net.neighbors(self.nid))
        if not neighbors:
            self.net.log(f"{self.nid} has no neighbors to send its payloads.")
            for payload in self.payloads:
                self.delay[payload] = self.net.loop.time
            return

        # Naive approach: randomly pick any available neighbor
        best_neighbor = random.choice(neighbors)
        
        if self.scheduling_method == 'LIFO':
            payload = self.payloads.pop() # LIFO
        elif self.scheduling_method == 'FIFO':
            payload = self.payloads.pop(0) # FIFO
            
        self.delay.pop(payload, None) # remove the payload from delay tracking since it's being sent
        self.net.log(f"{self.nid} randomly sends '{payload}' to {best_neighbor}")
        self.unicast(best_neighbor, ('RANDOM', self.nid, payload))
        self.queue -= 1

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