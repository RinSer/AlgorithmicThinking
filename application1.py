"""
This is my implementation of application #1 from the 
Algorithmic thinking course

created by RinSer
"""

import urllib2
import project1
import matplotlib.pyplot as plot


PAPERS = 27770
CITATIONS = 352768

# Load the necessary file and create the digraph dictionary
FILE_URL = 'http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt'
citations_file = urllib2.urlopen(FILE_URL)

# Dictionary to store the citations graph
citations = dict()
for line in citations_file:
    papers = line[:-1].split(' ')
    node = int(papers[0])
    edges = set([])
    for paper in papers[1:-1]:
	edges.add(int(paper))
    citations.update({node:edges})

# Check if the citations has loaded correctly
assert len(citations) == PAPERS
number_of_edges = 0;
for edges in citations.itervalues():
    number_of_edges += len(edges)
assert number_of_edges == CITATIONS

# Compute the in-degree distribution for the citations graph
citation_distribution = project1.in_degree_distribution(citations)
# Normalize the computed distribution
for key in citation_distribution.iterkeys():
    citation_distribution[key] = citation_distribution[key]/float(PAPERS)
# Check if the normalization has executed correctly
one = 0
for num in citation_distribution.itervalues():
    one += num
assert one == 1.0

# Plot the in-degree distribution for the citation graph (log/log)
plot.plot(citation_distribution.keys(), citation_distribution.values(), 'ro')
plot.title('Plot of the in-degree distribution for the citation graph (log/log)')
plot.xscale('log')
plot.xlabel('Number of citations')
plot.yscale('log')
plot.ylabel('Fraction of papers')
plot.grid(True)
plot.savefig('q1.png')
plot.close()

# Successful completion message
print 'The plot has been saved as q1.png'
