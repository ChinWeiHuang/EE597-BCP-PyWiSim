import matplotlib.pyplot as plt

nodes = {'A': (0,0), 'B': (1,0.5), 'C': (1,-0.5), 'D': (2,0.5), 'E': (2,-0.5), 'F': (3,0.5), 'G': (3,-0.5)}

plt.figure(figsize=(6, 4))

# Draw edges first so they are behind the nodes
edges = [('A','B'), ('A','C'), ('B','C'), ('B','D'), ('B','E'), ('C','D'), ('C','E'), ('D','E'), ('D','F'), ('D','G'), ('E','F'), ('E','G'), ('F','G')]
for n1, n2 in edges:
    x1, y1 = nodes[n1]
    x2, y2 = nodes[n2]
    plt.plot([x1, x2], [y1, y2], color='gray', linestyle='--', zorder=0)

# Draw nodes
for node, (x, y) in nodes.items():
    if node == 'A':
        color = '#98FB98' # Light green for source
    elif node == 'G':
        color = '#FFB6C1' # Light red for sink
    else:
        color = '#87CEFA' # Light blue for intermediate
    plt.plot(x, y, marker='o', markersize=30, color=color, markeredgecolor='black', zorder=1)
    plt.text(x, y, node, fontsize=12, ha='center', va='center', weight='bold', zorder=2)

plt.title('Simulated Network Topology')
plt.margins(0.15) # Adds 15% padding to both the x and y axes
plt.axis('off') # Hide axes
plt.tight_layout()
plt.savefig('topology.png', dpi=300)

print("Topology graph created.")