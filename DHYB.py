'''
DHYB.py
Implements the Deletion-Hybrid (DHYB) graph reduction method.
Valid probabilities range between 0, which is equivalent to DRE, and 1, which is
equivalent to DRVE
author: Erik Rye
date: 13 June 15
'''

import deletion as de
import networkx as nx
import os

def DHYB(graph, reduction_list, num_trials, prob, verbose):
    if not os.path.exists('DHYB-' + str(prob) + '/'):
        os.mkdir('DHYB-' + str(prob) + '/')
    for trial in range(num_trials):
        if verbose:
            print "Starting reduction w/seed " + str(trial) + "..."
        reduced_graph = graph.copy()
        for node_num in reduction_list:
            if verbose:
                print "Reducing to graph of order " + str(node_num) + "..."
            d = de.Deletion(reduced_graph,trial)
            reduced_graph = d.DHYB(prob,node_num)
            nx.write_gexf(reduced_graph, 'DHYB-' + str(prob) + '/' +
                        str(node_num) + '-DHYB-' + str(prob) + '-' + str(trial)
                        + '.gexf')
            if verbose:
                print "Graph of order " + str(node_num) + " written."
            del d 

