"""
Function to draw the graph in_degree distribution plot.

created by RinSer
"""

import matplotlib.pyplot as plot


def draw(graph, plot_file, title, xlabel, ylabel, log=True):
    """
    Draws the plot of a given graph.
    Returns nothing.
    """
    plot.plot(graph.keys(), graph.values(), 'ro')
    plot.title(title)
    plot.xlabel(xlabel)
    plot.ylabel(ylabel)
    if log:
	plot.xscale('log')
	plot.yscale('log')
    plot.grid(True)
    plot.savefig(plot_file)
    plot.close()
