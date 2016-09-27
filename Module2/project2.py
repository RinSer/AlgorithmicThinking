"""
My implementation of Project #2 from the coursera 
Algorithmic Thinking course.

created by RinSer
"""

from collections import deque


def bfs_visited(ugraph, start_node):
    """
    Takes the undirected graph ugraph and the node start_node and returns the set consisting of all nodes that are visited by a breadth-first search that starts at start_node.
    """
    # Create an empty queue and the visited nodes set
    visited = set()
    queue = deque()
    # Add the start_node to the queue and visited set
    visited.add(start_node)
    queue.append(start_node)
    # BFS algorithm logic
    while len(queue) > 0:
        current = queue.popleft()
        for node in ugraph[current]:
            if node not in visited:
                visited.add(node)
                queue.append(node)

    return visited

def cc_visited(ugraph):
    """
    Takes the undirected graph ugraph and returns a list of sets, where each set consists of all the nodes (and nothing else) in a connected component, and there is exactly one set in the list for each connected component in ugraph and nothing else.
    """
    remaining_nodes = set()
    connected_components = list()
    # Add all the graph nodes to the unchecked nodes set
    for node in ugraph.iterkeys():
        remaining_nodes.add(node)
    
    while len(remaining_nodes) > 0:
        current_node = remaining_nodes.pop()
        ccomponent = bfs_visited(ugraph, current_node)
        connected_components.append(ccomponent)
        remaining_nodes -= ccomponent

    return connected_components

def largest_cc_size(ugraph):
    """
    Takes the undirected graph ugraph and returns the size (an integer) of the largest connected component in ugraph.
    """
    cc_sizes = list()
    ccomponents = cc_visited(ugraph)
    for ccomponent in ccomponents:
        cc_sizes.append(len(ccomponent))
    if len(cc_sizes) > 0:
        return max(cc_sizes)
    else:
        return 0

def compute_resilience(ugraph, attack_order):
    """
    Takes the undirected graph ugraph, a list of nodes attack_order and iterates through the nodes in attack_order. For each node in the list, the function removes the given node and its edges from the graph and then computes the size of the largest connected component for the resulting graph. The function should return a list whose k+1th entry is the size of the largest connected component in the graph after the removal of the first k nodes in attack_order. The first entry (indexed by zero) is the size of the largest connected component in the original graph.
    """
    resilience = list()
    resilience.append(largest_cc_size(ugraph))
    # Remove the attacked nodes and compute resilience
    for node in attack_order:
        del ugraph[node]
        for edges in ugraph.itervalues():
            if node in edges:
                edges.remove(node)
        resilience.append(largest_cc_size(ugraph))

    return resilience


### Testing
GRAPH0 = {0: set([1]),
          1: set([0, 2]),
          2: set([1, 3]),
          3: set([2])}

GRAPH1 = {0: set([1, 2, 3, 4]),
          1: set([0, 2, 3, 4]),
          2: set([0, 1, 3, 4]),
          3: set([0, 1, 2, 4]),
          4: set([0, 1, 2, 3])}

GRAPH2 = {1: set([2, 4, 6, 8]),
          2: set([1, 3, 5, 7]),
          3: set([2, 4, 6, 8]),
          4: set([1, 3, 5, 7]),
          5: set([2, 4, 6, 8]),
          6: set([1, 3, 5, 7]),
          7: set([2, 4, 6, 8]),
          8: set([1, 3, 5, 7])}

GRAPH3 = {0: set([]),
          1: set([2]),
          2: set([1]),
          3: set([4]),
          4: set([3])}

print GRAPH0
print bfs_visited(GRAPH0, 1)
print cc_visited(GRAPH0)
print compute_resilience(GRAPH0, [1, 2, 3])
print largest_cc_size(GRAPH0)
#print GRAPH1
#print bfs_visited(GRAPH1, 1)
#print cc_visited(GRAPH1)
#print compute_resilience(GRAPH1, [1, 2, 3])
#print largest_cc_size(GRAPH1)
#print GRAPH2
#print bfs_visited(GRAPH2, 1)
#print cc_visited(GRAPH2)
#print compute_resilience(GRAPH2, [1, 2, 3])
#print largest_cc_size(GRAPH2)
#print GRAPH3
#print bfs_visited(GRAPH3, 1)
#print cc_visited(GRAPH3)    
#print compute_resilience(GRAPH3, [1, 2, 3])
#print largest_cc_size(GRAPH3)
