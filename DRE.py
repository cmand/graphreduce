'''
DRE.py
Implements the Deletion of a Random Edge (DRE) graph reduction method
author: Erik Rye
date: 13 June 15
'''

import deletion as de
import networkx as nx
import os

def DRE(graph, reduction_list, num_trials, verbose):
    if not os.path.exists('DRE/'):
        os.mkdir('DRE/')
    for trial in range(num_trials):
        if verbose:
            print "Starting reduction w/seed " + str(trial) + "..."
        reduced_graph = graph.copy()
        for node_num in reduction_list:
            if verbose:
                print "Reducing to graph of order " + str(node_num) + "..."
            d = de.Deletion(reduced_graph,trial)
            reduced_graph = d.DRE(node_num)
            nx.write_gexf(reduced_graph, 'DRE/' + str(node_num) + '-DRE-' +
                    str(trial) + '.gexf')
            if verbose:
                print "Graph of order " + str(node_num) + " written."
            del d
