'''
DRV.py
Implements the Deletion of a Random Vertex (DRV) graph reduction method
author: Erik Rye
date: 13 June 15
'''

import deletion as de
import networkx as nx
import os

def DRV(graph, reduction_list, num_trials, verbose):
    if not os.path.exists('DRV/'):
        os.mkdir('DRV')
    for trial in range(num_trials):
        if verbose:
            print "Starting reduction w/seed " + str(trial) + "..."
        reduced_graph = graph.copy()
        for node_num in reduction_list:
            if verbose:
                print "Reducing to graph of order " + str(node_num) + "..."
            d = de.Deletion(reduced_graph,trial)
            reduced_graph = d.DRV(node_num)
            nx.write_gexf(reduced_graph, 'DRV/' + str(node_num) + '-DRV-' +
                    str(trial) + '.gexf')
            if verbose:
                print "Graph of order " + str(node_num) + " written."
            del d
