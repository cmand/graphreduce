'''
DRVE.py
Implements the Deletion of a Random Vertex's Edge (DRVE) graph reduction method
author: Erik Rye
date: 13 June 15
'''

import deletion as de
import networkx as nx
import os

def DRVE(graph, reduction_list, num_trials, verbose):
    if not os.path.exists('DRVE/'):
        os.mkdir('DRVE/')
    for trial in range(num_trials):
        if verbose:
            print "Starting reduction w/seed " + str(trial) + "..."
        reduced_graph = graph.copy()
        for node_num in reduction_list:
            if verbose:
                print "Reducing to graph of order " + str(node_num) + "..."
            d = de.Deletion(reduced_graph,trial)
            reduced_graph = d.DRVE(node_num)
            nx.write_gexf(reduced_graph, 'DRVE/' + str(node_num) + '-DRVE-' +
                    str(trial) + '.gexf')
            if verbose:
                print "Graph of order " + str(node_num) + " written."
            del d

