#!/usr/bin/env python
"""
This is my implementation of Application #2 from the 
Algorithmic thinking course

created by RinSer
"""


import random
import load
import er
import dpa
import project2
import matplotlib.pyplot as plot
import time


def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        try:
            ugraph[neighbor].remove(node)
        except KeyError:
            pass

def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order
    
def fast_targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree with a faster algorithm
    
    Returns:
    A list of nodes
    """
    # Copy the initial graph
    agraph = copy_graph(ugraph)
    nodes_number = len(agraph)
    # Initialize the degree sets
    degree_sets = list()
    for k in range(nodes_number):
        degree_sets.append(set([]))
    # Populate the degree sets
    for i in agraph.iterkeys():
        degree = len(agraph[i])
        degree_sets[degree].add(i)
    
    # Determine the attack vector
    attack_vector = list()
    i = 0
    for k in range(nodes_number-1, -1, -1):
        while len(degree_sets[k]) > 0:
            u = degree_sets[k].pop()
            for node in agraph[u]:
                try:
                    new_degree = len(agraph[node])
                except KeyError:
                    new_degree = 0
                try:
                    degree_sets[new_degree].remove(node)
                except:
                    pass
                if new_degree > 0:
                    degree_sets[new_degree-1].add(node)
            attack_vector.append(u)
            i += 1
            delete_node(agraph, u)

    return attack_vector


def random_order(ugraph):
    """
    Takes a graph and returns a list of the nodes in the 
    graph in some random order
    """
    nodes = list()
    for node in ugraph.iterkeys():
        nodes.append(node)
    # Randomize the nodes list
    random.shuffle(nodes)
    
    return nodes


NET_NODES = 1239
NET_EDGES = 3047
FILE_URL = 'http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt'


# Question 1

# Load the network graph
network = load.graph(FILE_URL)

# Check if the network graph has loaded correctly
net_nodes = len(network)
assert net_nodes == NET_NODES
net_edges = 0
for edges in network.itervalues():
    net_edges += len(edges)
net_edges = net_edges/2
assert net_edges == NET_EDGES
er_probability = round(net_edges*2/float(net_nodes**2), 3)

# Create the ER simulation graph
er_simulation = er.ER(net_nodes, er_probability)

# Create the UPA simulation graph
m = net_edges/net_nodes+1
upa_simulation = dpa.UPA(NET_NODES, m)

# Compute resilience for the graphs
net_resilience = project2.compute_resilience(network, random_order(network))
er_resilience = project2.compute_resilience(er_simulation, random_order(er_simulation))
upa_resilience = project2.compute_resilience(upa_simulation, random_order(upa_simulation))

# Plot the resilience curves
removed_number = [ i for i in range(NET_NODES+1) ]

plot.plot(removed_number, net_resilience, 'r', label='Network')
plot.plot(removed_number, er_resilience, 'b', label='ER, p=0.004')
plot.plot(removed_number, upa_resilience, 'y', label='UPA, m=3')
plot.legend()
plot.title('Random order attack network graph resilience comparison')
plot.xlabel('Number of removed nodes')
plot.ylabel('Largest connected component size')
plot.grid(True)
plot.savefig('a2q1.png')
plot.close()

print 'The plot for Question 1 has been saved as a2q1.png'


# Question 3

# Initialize lists to store the competing algorithms times and graph sizes
standard_time = list()
fast_time = list()
n_values = list()
for n in range(10, 1000, 10):
    n_values.append(n)
    # Make the testing graph
    test_graph = dpa.UPA(n, 5)
    # Test the standard targeted order algorithm
    to_start = time.time()
    targeted_order(test_graph)
    to_stop = time.time()
    standard_time.append(to_stop-to_start)
    # Test the fast targeted order algorithm
    fto_start = time.time()
    fast_targeted_order(test_graph)
    fto_stop = time.time()
    fast_time.append(fto_stop-fto_start)

# Plot the time curves
plot.plot(n_values, standard_time, 'b', label='Basic targeted order algorithm')
plot.plot(n_values, fast_time, 'r', label='Fast targeted order algorithm')
plot.legend()
plot.title('Comparison of targeted order algorithms\' running times on desktop Python')
plot.xlabel('Number of graph nodes')
plot.ylabel('Algorithm running time in seconds')
plot.grid(True)
plot.savefig('a2q3.png')
plot.close()

print 'The plot for Question 3 has been saved as a2q3.png'


# Question 4

# Load the network graph
network = load.graph(FILE_URL)

# Check if the network graph has loaded correctly
net_nodes = len(network)
assert net_nodes == NET_NODES
net_edges = 0
for edges in network.itervalues():
    net_edges += len(edges)
net_edges = net_edges/2
assert net_edges == NET_EDGES
er_probability = round(net_edges*2/float(net_nodes**2), 3)

# Create the ER simulation graph
er_simulation = er.ER(NET_NODES, er_probability)

# Create the UPA simulation graph
m = net_edges/net_nodes+1
upa_simulation = dpa.UPA(NET_NODES, m)

# Compute resilience for the graphs
net_resilience = project2.compute_resilience(network, fast_targeted_order(network))
f = fast_targeted_order(er_simulation)
er_resilience = project2.compute_resilience(er_simulation, f)
upa_resilience = project2.compute_resilience(upa_simulation, fast_targeted_order(upa_simulation))

# Plot the resilience curves
removed_number = [ i for i in range(NET_NODES+1) ]

plot.plot(removed_number, net_resilience, 'r', label='Network')
# Update the removed number
while len(er_resilience) < len(removed_number):
    er_resilience.append(0)
plot.plot(removed_number, er_resilience, 'b', label='ER, p=0.004')
plot.plot(removed_number, upa_resilience, 'y', label='UPA, m=3')
plot.legend()
plot.title('Targeted order attack network graph resilience comparison')
plot.xlabel('Number of removed nodes')
plot.ylabel('Largest connected component size')
plot.grid(True)
plot.savefig('a2q4.png')
plot.close()

print 'The plot for Question 1 has been saved as a2q4.png'

    
