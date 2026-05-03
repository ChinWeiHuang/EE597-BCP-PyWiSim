# Performance Evaluation of BCP over Static Wireless Networks

This repository contains the implementation of the Backpressure Collection Protocol (BCP) and a Random Walk baseline for the EE597 final project at USC.

## Dependency: PyWiSim
This project requires the `PyWiSim` simulation framework to run. Because PyWiSim is a separate framework, it is not included in this repository.

## Setup Instructions
1. Clone the PyWiSim repository to your local machine.
2. Clone this repository.
3. Copy all Python scripts from this repository (`BCP.py`, `BCP_test1.py`, etc.) into the `PyWiSim` folder of your local PyWiSim repository.
4. Run the test scripts directly from that directory.

### Example Commands:
```bash
python BCP_test1.py --scheduling=LIFO
python BCP_test2.py --scheduling=FIFO --arrival_rate=0.8
python random_walk_test.py --scheduling=LIFO --arrival_rate=0.5
