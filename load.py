"""
Function to load the file with papers' citations.

created by RinSer
"""

import urllib2


def graph(file_url):
    """
    Loads the txt file from given file_url 
    and parses it as a graph.
    Returns a graph.
    """
    txt_file = urllib2.urlopen(file_url)

    graph = dict()
    for line in txt_file:
        papers = line[:-1].split(' ')
        node = int(papers[0])
        edges = set([])
        for paper in papers[1:-1]:
	    edges.add(int(paper))
        graph.update({node:edges})

    return graph
