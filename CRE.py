'''
CRE.py
Implements the Contraction of a Random Edge (CRE) graph reduction method
author: Erik Rye
date: 13 June 15
'''

import contraction as ct
import networkx as nx
import os

def CRE(graph, reduction_list, num_trials, verbose):
    if not os.path.exists('CRE/'):
        os.mkdir('CRE/')
    for trial in range(num_trials):
        if verbose:
            print "Starting reduction w/seed " + str(trial) + "..."
        reduced_graph = graph.copy()
        for node_num in reduction_list:
            if verbose:
                print "Reducing to graph of order " + str(node_num) + "..."
            c = ct.Contraction(reduced_graph,trial)
            reduced_graph = c.CRE(node_num)
            nx.write_gexf(reduced_graph, 'CRE/' + str(node_num) + '-CRE-' +
                    str(trial) + '.gexf')
            if verbose:
                print "Graph of order " + str(node_num) + " written."
            del c
                   
