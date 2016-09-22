"""
The ER Algorithm implementation

created by RinSer
"""


import random


def ER(vertices, probability):
    """
    Creates a graph with number of vertices = vertices 
    and number of edges determined randomly by a given probability.
    Returns the graph.
    """
    graph = dict()
    for i in range(vertices):
		graph[i] = set([])
		for j in range(vertices):
			if i != j:
			    rand = random.random()
			    if rand < probability:
				graph[i].add(j)

    return graph

