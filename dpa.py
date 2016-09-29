"""
The DPA algorithm implementation.

created by RinSer
"""

import random
import project1


def DPA(n, m):
    """
    Function that creates a graph with n nodes 
    using the DPA technique.
    """
    # Create the basic graph with m nodes
    graph = project1.make_complete_graph(m)
    # Create the auxiliary list of node numbers
    node_numbers = [node for node in range(m) for i in range(m)]
    
    for i in range(m, n+1):
        new_edges = set([])
        for j in range(m):
            new_edges.add(random.choice(node_numbers))

        node_numbers.append(i)
        node_numbers.extend(list(new_edges))
        
        graph.update({i:new_edges})

    return graph

def UPA(n, m):
    """
    Function that creates a graph with n nodes 
    using the DPA technique.
    """
    # Create the basic graph with m nodes
    graph = project1.make_complete_graph(m)
    # Create the auxiliary list of node numbers
    node_numbers = [node for node in range(m) for i in range(m)]
    
    for i in range(m, n):
        new_edges = set([])
        for j in range(m):
            new_edges.add(random.choice(node_numbers))

        node_numbers.append(i)
        for _ in range(len(new_edges)):
            node_numbers.append(i)
        node_numbers.extend(list(new_edges))
        
        graph.update({i:new_edges})
        for edge in new_edges:
            graph[edge].add(i)

    return graph

