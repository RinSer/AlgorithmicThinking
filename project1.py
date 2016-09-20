"""
My implementation of the Algorithmic thinking 
project #1.

created by RinSer
"""

# Graph constants
EX_GRAPH0 = {0:set([1, 2]), 1:set([]), 2:set([])}
EX_GRAPH1 = {0:set([1, 4, 5]), 1:set([2, 6]), 2:set([3]), 3:set([0]), 4:set([1]), 5:set([2]), 6:set([])}
EX_GRAPH2 = {0:set([1, 4, 5]), 1:set([2, 6]), 2:set([3, 7]), 3:set([7]), 4:set([1]), 5:set([2]), 6:set([]), 7:set([3]), 8:set([1, 2]), 9:set([0, 3, 4, 5, 6, 7])}


def make_complete_graph(num_nodes):
    """
    Takes the number of nodes num_nodes and returns a dictionary corresponding to a complete directed graph with the specified number of nodes. A complete graph contains all possible edges subject to the restriction that self-loops are not allowed. The nodes of the graph should be numbered 0 to num_nodes - 1 when num_nodes is positive. Otherwise, the function returns a dictionary corresponding to the empty graph.
    """
    if num_nodes > 0:
        graph = dict()
        for num_i in range(num_nodes):
            edges = list()
            for num_j in range(num_nodes):
                if num_j != num_i:
                    edges.append(num_j);
            graph.update({num_i:set(edges)})
    else:
        graph = {0:set([])}

    return graph


def compute_in_degrees(digraph):
    """
    Takes a directed graph digraph (represented as a dictionary) and computes the in-degrees for the nodes in the graph. The function should return a dictionary with the same set of keys (nodes) as digraph whose corresponding values are the number of edges whose head matches a particular node.
    """
    in_degrees = dict()
    for node in digraph.iterkeys():
	in_degree = 0
	for edges in digraph.itervalues():
	    for edge in edges:
		if edge == node:
		    in_degree += 1
	in_degrees.update({node:in_degree})

    return in_degrees


def in_degree_distribution(digraph):
    """
    Takes a directed graph digraph (represented as a dictionary) and computes the unnormalized distribution of the in-degrees of the graph. The function should return a dictionary whose keys correspond to in-degrees of nodes in the graph. The value associated with each particular in-degree is the number of nodes with that in-degree. In-degrees with no corresponding nodes in the graph are not included in the dictionary.
    """
    distribution = dict()
    in_degrees = compute_in_degrees(digraph)
    for in_degree in in_degrees.itervalues():
        if in_degree in distribution:
            distribution[in_degree] += 1
        else:
            distribution.update({in_degree:1})

    return distribution


TEST_GRAPH = make_complete_graph(5)
print TEST_GRAPH
print compute_in_degrees(TEST_GRAPH)
print in_degree_distribution(TEST_GRAPH)
print compute_in_degrees(EX_GRAPH0)
print in_degree_distribution(EX_GRAPH0)
print compute_in_degrees(EX_GRAPH1)
print in_degree_distribution(EX_GRAPH1)
print compute_in_degrees(EX_GRAPH2)
print in_degree_distribution(EX_GRAPH2)
