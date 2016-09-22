#!/usr/bin/env python
"""
This is my implementation of Application #1 from the 
Algorithmic thinking course

created by RinSer
"""

from datetime import datetime
import load
import project1
import plot
import er
import dpa


PAPERS = 27770
CITATIONS = 352768
FILE_URL = 'http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt'

def normalize(distribution, base):
    """
    Function that normalizes a given distribution 
    dividing each value by base.
    Checks if the sum of normalized values equals 1.
    Returns nothing mutating the initial dict.
    """
    for key in distribution.iterkeys():
        distribution[key] = distribution[key]/float(base)
    # Check if the normalization has completed correctly
    one = 0
    for num in distribution.itervalues():
        one += num
    assert int(round(one)) == 1


print 'Application #1 has started at '+str(datetime.now().time())

# Question 1

# Load the necessary file and create the digraph dictionary
citations = load.graph(FILE_URL)

# Check if the citations has loaded correctly
assert len(citations) == PAPERS
number_of_edges = 0;
for edges in citations.itervalues():
    number_of_edges += len(edges)
assert number_of_edges == CITATIONS

# Compute the in-degree distribution for the citations graph
citation_distribution = project1.in_degree_distribution(citations)
# Normalize the computed distribution
normalize(citation_distribution, PAPERS)

# Plot the in-degree distribution for the citation graph (log/log)
title = 'Plot of the in-degree distribution for the citation graph (log/log)'
xlabel = 'Number of citations'
ylabel = 'Fraction of papers'
plot.draw(citation_distribution, 'q1.png', title, xlabel, ylabel)

# Successful completion message
print 'The citations graph plot has been saved as q1.png'

# Question 2

# Compute the in-degree distribution for the simulation graph and normalize it
nodes = 10
while nodes < 1001:
    graph = er.ER(nodes, 0.5)
    graph_distribution = project1.in_degree_distribution(graph)
    # Normalize the distribution
    normalize(graph_distribution, nodes)

    # Plot the simulated graph in-degree distribution
    plot.draw(graph_distribution, 'q2_'+str(nodes)+'.png', 'ER graph with '+str(nodes)+' nodes and edge probability 1/2', 'In-Degrees', 'Fraction of nodes', False)

    print 'ER graph plot has been saved as q2_'+str(nodes)+'.png'

    nodes *= 10
	
# Questions 3-5

# The values of n and m for the application # 1
N = 27770
M = 13

dpa_distribution = project1.in_degree_distribution(dpa.DPA(N, M))
# Normalize the in-degree distribution
normalize(dpa_distribution, N)

# Plot the graph in-degrees distribution
plot.draw(dpa_distribution, 'q4.png', 'DPA graph in-degrees distribution (log/log)', 'In-Degrees', 'Fractions of nodes')

print 'DPA graph plot has been saved as q4.png'

print 'Application #1 has completed successfully at '+str(datetime.now().time())

